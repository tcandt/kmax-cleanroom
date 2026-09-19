import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ELF_PATH = Path("cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling")
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

cs = Cs(CS_ARCH_X86, CS_MODE_64)
cs.detail = True

def dump_fn(va, size, name):
    off = va_to_off(va)
    code = elf[off : off + size]
    print(f"\n========================================================")
    print(f"=== {name} (0x{va:x}, {size}B) ===")
    print(f"========================================================")
    for insn in cs.disasm(code, va):
        extra = ""
        for op in insn.operands:
            if op.type == 2 and op.imm > 1000:
                extra += f" [imm: {op.imm} / 0x{op.imm:x}]"
                if op.imm == 86400000000000:
                    extra += " (24 hours in ns)"
                elif op.imm == 604800000000000:
                    extra += " (7 days in ns)"
                elif op.imm == 3600000000000:
                    extra += " (1 hour in ns)"
                elif op.imm == 1800000000000:
                    extra += " (30 mins in ns)"
                elif op.imm == 2592000000000000:
                    extra += " (30 days in ns)"
        if "rip" in insn.op_str:
            disp = insn.disp
            target = insn.address + insn.size + disp
            tgt_off = va_to_off(target)
            if tgt_off and 0 <= tgt_off < len(elf):
                sample = elf[tgt_off : tgt_off + 24]
                printable = "".join(chr(b) if 32 <= b < 127 else "." for b in sample)
                extra += f" [rip->0x{target:x}: {printable}]"
        print(f"0x{insn.address:x}: {insn.mnemonic:<8} {insn.op_str:<32} {extra}")

dump_fn(0x739060, 480, "main.biG96MFIwa (Hash Password)")
dump_fn(0x739240, 224, "main.d2SHxnu (Token Generator)")
dump_fn(0x739320, 288, "main.vT6rYK_v (Session Creator)")
dump_fn(0x73ec40, 1216, "main.bwvBd1LWVr (/api/auth-status)")
dump_fn(0x7409a0, 1440, "main.bjWkHiittd (/api/logout)")
dump_fn(0x743c40, 1184, "main.jlRPqj8Kko_8 (Invalidate/Kick User Sessions)")
