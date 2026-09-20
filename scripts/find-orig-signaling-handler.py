with open('cleanroom_archive/cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe', 'rb') as f:
    buf = f.read()

# Let's search for PE sections
pe_off = int.from_bytes(buf[0x3c:0x40], 'little')
num_sections = int.from_bytes(buf[pe_off+6:pe_off+8], 'little')
opt_hdr_size = int.from_bytes(buf[pe_off+20:pe_off+22], 'little')
sec_off = pe_off + 24 + opt_hdr_size

image_base = int.from_bytes(buf[pe_off+0x30:pe_off+0x38], 'little')
print(f'PE Image Base: {hex(image_base)}, Sections: {num_sections}')

sections = []
for i in range(num_sections):
    so = sec_off + i * 40
    name = buf[so:so+8].decode('latin1').split('\x00')[0]
    vsize = int.from_bytes(buf[so+8:so+12], 'little')
    va = int.from_bytes(buf[so+12:so+16], 'little')
    rsize = int.from_bytes(buf[so+16:so+20], 'little')
    roff = int.from_bytes(buf[so+20:so+24], 'little')
    sections.append((name, va, vsize, roff, rsize))
    print(f'{name:10} VA: {hex(va):10} VSize: {hex(vsize):10} FileOff: {hex(roff):10} Size: {hex(rsize)}')

def rva_to_off(rva):
    for name, va, vsize, roff, rsize in sections:
        if va <= rva < va + vsize:
            return roff + (rva - va)
    return None

def off_to_rva(off):
    for name, va, vsize, roff, rsize in sections:
        if roff <= off < roff + rsize:
            return va + (off - roff)
    return None

# Find references to string "Forwarding start_preview"
idx = buf.find(b'[Signaling] Forwarding start_preview')
str_rva = off_to_rva(idx)
str_va = image_base + str_rva
print(f'String at file 0x{idx:x}, RVA 0x{str_rva:x}, VA 0x{str_va:x}')

# Search for RIP-relative LEA to str_va in .text
text_sec = [s for s in sections if s[0] == '.text'][0]
t_roff = text_sec[3]
t_rsize = text_sec[4]
t_rva = text_sec[1]

for p in range(t_roff, t_roff + t_rsize - 7):
    disp = int.from_bytes(buf[p+3:p+7], 'little', signed=True)
    insn_rva = t_rva + (p - t_roff)
    insn_va = image_base + insn_rva
    if insn_va + 7 + disp == str_va:
        print(f'Found reference to start_preview log at file 0x{p:x}, VA 0x{insn_va:x}')
