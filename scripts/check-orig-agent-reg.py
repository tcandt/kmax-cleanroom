with open('cleanroom_archive/cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe', 'rb') as f:
    buf = f.read()

# Let's search for "agent_register_ok" in original binary
idx = 0
while True:
    idx = buf.find(b'agent_register_ok', idx)
    if idx == -1: break
    print(f'agent_register_ok at {hex(idx)}')
    # print context around it
    s = buf[max(0, idx - 100):min(len(buf), idx + 200)].decode('latin1', errors='replace')
    clean = ''.join(c if 32 <= ord(c) < 127 else '.' for c in s)
    print(clean)
    idx += len('agent_register_ok')

# Does original signaling send "config" to agent?
idx = 0
while True:
    idx = buf.find(b'ice_servers', idx)
    if idx == -1: break
    print(f'ice_servers at {hex(idx)}')
    s = buf[max(0, idx - 100):min(len(buf), idx + 200)].decode('latin1', errors='replace')
    clean = ''.join(c if 32 <= ord(c) < 127 else '.' for c in s)
    print(clean)
    idx += len('ice_servers')
