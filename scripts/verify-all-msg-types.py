with open('cleanroom_archive/cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe', 'rb') as f:
    buf = f.read()

import re

# Find all occurrences of message_type in JSON or code
# Typically: "message_type" == "..."
# Let's search for strings that are used in message dispatching
patterns = [
    rb'connect',
    rb'forward',
    rb'start_preview',
    rb'stop_preview',
    rb'quit_agent',
    rb'group_control_event',
    rb'inject_data',
    rb'command',
    rb'command_result',
    rb'device_msg',
    rb'device_list_update',
    rb'agent_register',
    rb'agent_register_ok',
    rb'heartbeat',
    rb'client_disconnected',
    rb'snapshot_update',
    rb'global_settings_updated',
    rb'tags_update',
    rb'device_metrics',
    rb'task_status_updated',
    rb'license_update'
]

for p in patterns:
    print(f'{p.decode()}: count = {buf.count(p)}')
