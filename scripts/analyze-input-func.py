import capstone

with open('deploy_agent/cloudphone-agent-amd64', 'rb') as f:
    buf = f.read()

# Scan backwards from 0x5e3d05 for prologue
for p in range(0x5e3d05, 0x5e2000, -1):
    if buf[p:p+4] == b'\x49\x3b\x66\x10' or buf[p:p+4] == b'\x4d\x3b\x66\x10':
        func_start = p
        print('Function prologue at file offset:', hex(p), 'VA:', hex(p + 0x400000))
        break

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# Print all strings referenced in this function
for p in range(func_start, func_start + 0x1000):
    va = 0x401000 + (p - 0x1000)
    code = buf[p:p+7]
    for insn in cs.disasm(code, va):
        if insn.mnemonic in ['lea', 'mov'] and 'rip +' in insn.op_str:
            parts = insn.op_str.split('rip + ')
            if len(parts) > 1:
                disp_str = parts[1].replace(']', '')
                try:
                    disp = int(disp_str, 16)
                    target_va = disp + insn.address + insn.size
                    if 0x9f2000 <= target_va < 0xdf2000:
                        off = target_va - 0x9f2000 + 0x5f2000
                        s = buf[off:off+50].decode('latin1', errors='replace')
                        clean_s = ''.join(c if 32 <= ord(c) < 127 else '.' for c in s)
                        print(f'0x{va:x}: {insn.mnemonic} {insn.op_str} -> "{clean_s}"')
                except:
                    pass
