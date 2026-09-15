import unittest
import struct
from pathlib import Path

ROOT = Path(r"D:\KMAX-CLEANROOM")
SIGNALING_LINUX = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
SIGNALING_WIN = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
AGENT_ARM64 = ROOT / "cloudphone-v0.3.6 (1)" / "android" / "cloudphone-agent"

def parse_elf_sections(data):
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

def parse_pclntab_correct(pcln_data):
    magic = struct.unpack_from("<I", pcln_data, 0)[0]
    ptrSize = pcln_data[7]
    fmt = "<Q" if ptrSize == 8 else "<I"
    nfunc = struct.unpack_from(fmt, pcln_data, 8)[0]
    textStart = struct.unpack_from(fmt, pcln_data, 24 if ptrSize == 8 else 16)[0]
    funcnameOffset = struct.unpack_from(fmt, pcln_data, 32 if ptrSize == 8 else 20)[0]
    pclnOffset = struct.unpack_from(fmt, pcln_data, 64 if ptrSize == 8 else 36)[0]

    functions = []
    invalid_count = 0
    oor_funcoff = 0
    oor_nameoff = 0
    vas = set()
    dup_vas = 0

    for i in range(nfunc):
        pos = pclnOffset + i * 8
        eOff, fOff = struct.unpack_from("<II", pcln_data, pos)
        func_va = textStart + eOff
        if func_va in vas:
            dup_vas += 1
        vas.add(func_va)

        func_record_pos = pclnOffset + fOff
        if func_record_pos + 8 > len(pcln_data):
            oor_funcoff += 1
            invalid_count += 1
            continue

        entryOff, nameOff = struct.unpack_from("<Ii", pcln_data, func_record_pos)
        name_pos = funcnameOffset + nameOff
        if name_pos < 0 or name_pos >= len(pcln_data):
            oor_nameoff += 1
            invalid_count += 1
            continue

        end_n = pcln_data.find(b"\x00", name_pos)
        if end_n == -1:
            invalid_count += 1
            continue

        fname = pcln_data[name_pos:end_n].decode("utf-8", errors="replace")
        if len(fname) == 0 or any(c in fname for c in ["\n", "\r", "\t"]):
            invalid_count += 1
            continue

        functions.append({
            "index": i,
            "va": func_va,
            "name": fname
        })

    return {
        "magic": hex(magic),
        "ptrSize": ptrSize,
        "nfunc": nfunc,
        "entries_parsed": len(functions),
        "valid_names": len(functions),
        "invalid_names": invalid_count,
        "duplicate_va": dup_vas,
        "out_of_range_funcoff": oor_funcoff,
        "out_of_range_nameoff": oor_nameoff,
        "percentage_valid": (len(functions) / nfunc) * 100 if nfunc else 0,
        "functions": functions
    }

class TestPclntabParser(unittest.TestCase):
    def test_signaling_linux(self):
        with open(SIGNALING_LINUX, "rb") as f:
            data = f.read()
        secs = parse_elf_sections(data)
        pcln_data = data[secs[".gopclntab"]["offset"] : secs[".gopclntab"]["offset"] + secs[".gopclntab"]["size"]]
        res = parse_pclntab_correct(pcln_data)
        
        self.assertEqual(res["nfunc"], 7571)
        self.assertEqual(res["valid_names"], 7571)
        self.assertEqual(res["invalid_names"], 0)
        self.assertEqual(res["out_of_range_funcoff"], 0)
        self.assertEqual(res["out_of_range_nameoff"], 0)
        self.assertEqual(res["percentage_valid"], 100.0)

        names = [f["name"] for f in res["functions"]]
        # Preserved runtime, main, reflect, sync, syscall packages
        self.assertTrue(any(n.startswith("runtime.") for n in names))
        self.assertTrue(any(n.startswith("main.") for n in names))
        self.assertTrue(any(n.startswith("reflect.") for n in names))
        self.assertTrue(any(n.startswith("sync.") for n in names))
        self.assertTrue(any(n.startswith("syscall.") for n in names))
        self.assertTrue(any("internal/abi" in n for n in names))

    def test_agent_arm64(self):
        with open(AGENT_ARM64, "rb") as f:
            data = f.read()
        secs = parse_elf_sections(data)
        pcln_data = data[secs[".gopclntab"]["offset"] : secs[".gopclntab"]["offset"] + secs[".gopclntab"]["size"]]
        res = parse_pclntab_correct(pcln_data)
        
        self.assertEqual(res["nfunc"], 15398)
        self.assertEqual(res["valid_names"], 15398)
        self.assertEqual(res["invalid_names"], 0)
        self.assertEqual(res["out_of_range_funcoff"], 0)
        self.assertEqual(res["out_of_range_nameoff"], 0)
        self.assertEqual(res["percentage_valid"], 100.0)

        names = [f["name"] for f in res["functions"]]
        self.assertTrue(any("internal/abi" in n for n in names))
        self.assertTrue(any("runtime" in n for n in names))

if __name__ == "__main__":
    unittest.main()
