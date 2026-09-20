with open('cleanroom_archive/cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe', 'rb') as f:
    buf = f.read()

keywords = [
    b'group_control_event',
    b'start_preview',
    b'stop_preview',
    b'quit_agent',
    b'command',
    b'inject_data',
    b'snapshot_update',
    b'device_msg',
    b'connect',
    b'forward'
]

for kw in keywords:
    count = buf.count(kw)
    idx = buf.find(kw)
    print(f'{kw.decode()}: count={count}, first={hex(idx)}')

# Find all occurrences of "[Signaling]" strings
import re
matches = re.findall(rb'\[Signaling\][^\x00\r\n]+', buf)
for m in set(matches):
    try:
        print(m.decode())
    except:
        pass
