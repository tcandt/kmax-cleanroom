import capstone

with open('cleanroom_archive/cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe', 'rb') as f:
    buf = f.read()

# Function containing 0x35b997
# Scan backwards for function prologue
func_start = 0x35b997
for p in range(0x35b997, 0x350000, -1):
    if buf[p:p+4] == b'\x49\x3b\x66\x10' or buf[p:p+4] == b'\x4d\x3b\x66\x10':
        func_start = p
        print('Function prologue at file offset:', hex(p), 'VA:', hex(0x140000000 + 0x1000 + (p - 0x600)))
        break

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

# Find all string references in this function
for p in range(func_start, func_start + 0x3000):
    va = 0x140000000 + 0x1000 + (p - 0x600)
    code = buf[p:p+7]
    for insn in cs.disasm(code, va):
        if insn.mnemonic in ['lea', 'mov'] and 'rip +' in insn.op_str:
            parts = insn.op_str.split('rip + ')
            if len(parts) > 1:
                disp_str = parts[1].replace(']', '')
                try:
                    disp = int(disp_str, 16)
                    target_va = disp + insn.address + insn.size
                    target_rva = target_va - 0x140000000
                    if 0x379000 <= target_rva < 0x7c8000:
                        off = 0x377c00 + (target_rva - 0x379000)
                        s = buf[off:off+60].decode('latin1', errors='replace')
                        clean_s = ''.join(c if 32 <= ord(c) < 127 else '.' for c in s)
                        print(f'0x{va:x}: {insn.mnemonic} {insn.op_str} -> "{clean_s}"')
                except:
                    pass
