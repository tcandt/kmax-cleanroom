with open('cleanroom_archive/cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe', 'rb') as f:
    buf = f.read()

def find_context(term):
    idx = 0
    while True:
        idx = buf.find(term.encode(), idx)
        if idx == -1: break
        print(f'=== Term "{term}" at offset {hex(idx)} ===')
        s = buf[max(0, idx - 100):min(len(buf), idx + 200)].decode('latin1', errors='replace')
        clean = ''.join(c if 32 <= ord(c) < 127 else '.' for c in s)
        print(clean)
        idx += len(term)

find_context('group_control_event')
find_context('start_preview')
find_context('quit_agent')
