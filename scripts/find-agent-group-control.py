with open('deploy_agent/cloudphone-agent-amd64', 'rb') as f:
    buf = f.read()

idx = 7733506
print('Context around 0x760102:')
s = buf[idx-50:idx+150].decode('latin1', errors='replace')
clean = ''.join(c if 32 <= ord(c) < 127 else '.' for c in s)
print(clean)

# Find references to this string in agent
rodata_va = 0x9f2000
rodata_off = 0x5f2000
text_va = 0x401000
text_off = 0x1000
str_va = rodata_va + (idx - rodata_off)

print(f'str_va: 0x{str_va:x}')

for p in range(text_off, text_off + 0x5f0000):
    disp = int.from_bytes(buf[p+3:p+7], 'little', signed=True)
    insn_va = text_va + (p - text_off)
    if insn_va + 7 + disp == str_va:
        print(f'Found reference to group_control_event at file 0x{p:x}, VA 0x{insn_va:x}')
