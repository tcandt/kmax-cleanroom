import os
import sys
import json
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root

ELF_PATH = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
FN_MAP_PATH = REPO_ROOT / "evidence" / "go_signaling" / "FUNCTION_MAP.json"

with open(ELF_PATH, "rb") as f:
    elf = f.read()

e_phoff, = struct.unpack_from("<Q", elf, 32)
e_phentsize, e_phnum = struct.unpack_from("<HH", elf, 54)
ph_list = []
for i in range(e_phnum):
    off = e_phoff + i * e_phentsize
    p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack_from("<IIQQQQQQ", elf, off)
    if p_type == 1:
        ph_list.append((p_vaddr, p_vaddr + p_memsz, p_offset, p_filesz))

def va_to_off(va):
    for vstart, vend, off, fsz in ph_list:
        if vstart <= va < vend:
            return off + (va - vstart)
    return None

fn_map = json.loads(FN_MAP_PATH.read_text("utf-8"))
fn_by_va = {f["va"]: f for f in fn_map}

cs = Cs(CS_ARCH_X86, CS_MODE_64)
cs.detail = True

def inspect_fn(va_str, name):
    fn = fn_by_va.get(va_str)
    va = int(va_str, 16)
    size = fn["size_bytes"]
    off = va_to_off(va)
    code = elf[off : off + size]

    print(f"\n========================================================")
    print(f"DISASSEMBLY: {name} ({va_str}) - {size} bytes")
    print(f"========================================================")

    for insn in cs.disasm(code, va):
        extra = ""
        # Check for immediate constants (like time.Duration, offsets)
        for op in insn.operands:
            if op.type == 2: # immediate
                imm = op.imm
                if imm > 1000000:
                    extra += f" [imm: {imm} / 0x{imm:x}]"
                    # Check if nanoseconds
                    if imm == 86400000000000:
                        extra += " (24 hours in ns)"
                    elif imm == 604800000000000:
                        extra += " (7 days in ns)"
                    elif imm == 3600000000000:
                        extra += " (1 hour in ns)"
                    elif imm == 1800000000000:
                        extra += " (30 mins in ns)"
                    elif imm == 2592000000000000:
                        extra += " (30 days in ns)"

        # Check for RIP relative addressing
        if "rip" in insn.op_str:
            # displacement
            disp = insn.disp
            target = insn.address + insn.size + disp
            # See if target points to .rodata string or symbol
            tgt_off = va_to_off(target)
            if tgt_off and 0 <= tgt_off < len(elf):
                # Try reading string at target
                sample = elf[tgt_off : tgt_off + 32]
                printable = "".join(chr(b) if 32 <= b < 127 else "." for b in sample)
                extra += f" [rip->0x{target:x}: {printable}]"

        print(f"0x{insn.address:x}: {insn.mnemonic:<8} {insn.op_str:<32} {extra}")

inspect_fn("0x739060", "main.biG96MFIwa (Hash Password)")
inspect_fn("0x739240", "main.d2SHxnu (Generate Token)")
inspect_fn("0x739320", "main.vT6rYK_v (Create Session)")
inspect_fn("0x73b080", "main.lYKp_Iuf (Validate Session)")
