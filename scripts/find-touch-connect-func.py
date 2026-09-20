import capstone

with open('deploy_agent/cloudphone-agent-amd64', 'rb') as f:
    buf = f.read()

# 0x9c9618 is file offset 0x5c9618
for p in range(0x5c9618, 0x5c8000, -1):
    if buf[p:p+4] == b'\x49\x3b\x66\x10' or buf[p:p+4] == b'\x4d\x3b\x66\x10':
        print('Function prologue for touch connect at:', hex(p), 'VA:', hex(p + 0x400000))
        break
