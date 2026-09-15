import os
import sys
import struct
from pathlib import Path

def get_repo_root() -> Path:
    env_root = os.environ.get("KMAX_CLEANROOM_ROOT")
    if env_root and Path(env_root).exists():
        return Path(env_root).resolve()
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "RULES.md").exists() or (parent / "CLEANROOM_AUDIT_LOG.md").exists():
            return parent
    return Path.cwd().resolve()

def parse_elf_sections(data: bytes):
    if len(data) < 64 or data[:4] != b"\x7fELF":
        raise ValueError("Invalid ELF header")
    ei_class = data[4]
    endian = "<" if data[5] == 1 else ">"
    fmt_ptr = "Q" if ei_class == 2 else "I"
    e_shoff = struct.unpack_from(endian + fmt_ptr, data, 40 if ei_class == 2 else 32)[0]
    e_shentsize = struct.unpack_from(endian + "H", data, 58 if ei_class == 2 else 46)[0]
    e_shnum = struct.unpack_from(endian + "H", data, 60 if ei_class == 2 else 48)[0]
    e_shstrndx = struct.unpack_from(endian + "H", data, 62 if ei_class == 2 else 50)[0]
    shstr_hdr = data[e_shoff + e_shstrndx * e_shentsize : e_shoff + (e_shstrndx + 1) * e_shentsize]
    shstr_off = struct.unpack_from(endian + fmt_ptr, shstr_hdr, 24 if ei_class == 2 else 16)[0]
    sections = {}
    for i in range(e_shnum):
        hdr = data[e_shoff + i * e_shentsize : e_shoff + (i + 1) * e_shentsize]
        sh_name_idx = struct.unpack_from(endian + "I", hdr, 0)[0]
        sh_addr = struct.unpack_from(endian + fmt_ptr, hdr, 16 if ei_class == 2 else 12)[0]
        sh_offset = struct.unpack_from(endian + fmt_ptr, hdr, 24 if ei_class == 2 else 16)[0]
        sh_size = struct.unpack_from(endian + fmt_ptr, hdr, 32 if ei_class == 2 else 20)[0]
        end = data.find(b"\x00", shstr_off + sh_name_idx)
        name = data[shstr_off + sh_name_idx : end].decode("latin1")
        sections[name] = {"addr": sh_addr, "offset": sh_offset, "size": sh_size}
    return sections

def parse_pclntab(pcln_data: bytes):
    if len(pcln_data) < 68:
        raise ValueError("Pclntab section too small for pcHeader")

    magic = struct.unpack_from("<I", pcln_data, 0)[0]
    minLC = pcln_data[6]
    ptrSize = pcln_data[7]
    if ptrSize not in (4, 8):
        raise ValueError(f"Invalid ptrSize in pcHeader: {ptrSize}")

    fmt = "<Q" if ptrSize == 8 else "<I"
    nfunc = struct.unpack_from(fmt, pcln_data, 8)[0]
    nfiles = struct.unpack_from(fmt, pcln_data, 16 if ptrSize == 8 else 12)[0]
    textStart = struct.unpack_from(fmt, pcln_data, 24 if ptrSize == 8 else 16)[0]
    funcnameOffset = struct.unpack_from(fmt, pcln_data, 32 if ptrSize == 8 else 20)[0]
    cuOffset = struct.unpack_from(fmt, pcln_data, 40 if ptrSize == 8 else 24)[0]
    filetabOffset = struct.unpack_from(fmt, pcln_data, 48 if ptrSize == 8 else 28)[0]
    pctabOffset = struct.unpack_from(fmt, pcln_data, 56 if ptrSize == 8 else 32)[0]
    pclnOffset = struct.unpack_from(fmt, pcln_data, 64 if ptrSize == 8 else 36)[0]

    # Validate funcname tab bounds
    funcname_end = cuOffset if cuOffset > funcnameOffset else len(pcln_data)

    functions = []
    prev_eOff = -1
    monotonic_ascending = True
    out_of_range_funcoff = 0
    out_of_range_nameoff = 0
    invalid_names = 0

    for i in range(nfunc):
        pos = pclnOffset + i * 8
        if pos + 8 > len(pcln_data):
            raise ValueError(f"Functab table truncated at index {i}")
        eOff, fOff = struct.unpack_from("<II", pcln_data, pos)

        if eOff < prev_eOff:
            monotonic_ascending = False
        prev_eOff = eOff

        func_va = textStart + eOff

        # _func record validation
        func_rec_pos = pclnOffset + fOff
        if func_rec_pos + 8 > len(pcln_data):
            out_of_range_funcoff += 1
            invalid_names += 1
            continue

        raw_feOff, nameOff = struct.unpack_from("<Ii", pcln_data, func_rec_pos)
        name_pos = funcnameOffset + nameOff

        if name_pos < funcnameOffset or name_pos >= funcname_end:
            out_of_range_nameoff += 1
            invalid_names += 1
            continue

        end_n = pcln_data.find(b"\x00", name_pos)
        if end_n == -1 or end_n > funcname_end:
            invalid_names += 1
            continue

        fname = pcln_data[name_pos:end_n].decode("utf-8", errors="replace")
        if len(fname) == 0 or any(c in fname for c in ["\n", "\r", "\t"]):
            invalid_names += 1
            continue

        functions.append({
            "index": i,
            "entryoff": eOff,
            "funcoff": fOff,
            "va": func_va,
            "nameOff": nameOff,
            "name": fname
        })

    # Validate terminal/sentinel entry at index nfunc
    sentinel_pos = pclnOffset + nfunc * 8
    sentinel_valid = False
    sentinel_eoff = None
    if sentinel_pos + 8 <= len(pcln_data):
        s_eOff, s_fOff = struct.unpack_from("<II", pcln_data, sentinel_pos)
        sentinel_eoff = s_eOff
        if s_eOff >= prev_eOff and s_fOff == 0:
            sentinel_valid = True

    # Calculate function sizes and check non-overlapping
    non_overlapping = True
    size_valid = True
    for i in range(len(functions)):
        if i + 1 < len(functions):
            f_size = functions[i+1]["entryoff"] - functions[i]["entryoff"]
        elif sentinel_eoff is not None:
            f_size = sentinel_eoff - functions[i]["entryoff"]
        else:
            f_size = 0

        if f_size <= 0:
            size_valid = False
            non_overlapping = False
        functions[i]["size"] = f_size

    return {
        "magic": hex(magic),
        "minLC": minLC,
        "ptrSize": ptrSize,
        "nfunc": nfunc,
        "nfiles": nfiles,
        "textStart": hex(textStart),
        "funcnameOffset": hex(funcnameOffset),
        "cuOffset": hex(cuOffset),
        "filetabOffset": hex(filetabOffset),
        "pctabOffset": hex(pctabOffset),
        "pclnOffset": hex(pclnOffset),
        "entries_parsed": len(functions),
        "monotonic_ascending": monotonic_ascending,
        "non_overlapping": non_overlapping,
        "size_valid": size_valid,
        "sentinel_valid": sentinel_valid,
        "sentinel_eoff": hex(sentinel_eoff) if sentinel_eoff is not None else None,
        "out_of_range_funcoff": out_of_range_funcoff,
        "out_of_range_nameoff": out_of_range_nameoff,
        "invalid_names": invalid_names,
        "functions": functions
    }
