import capstone

with open('deploy_agent/cloudphone-agent-amd64', 'rb') as f:
    buf = f.read()

# Let's search for "group_control_event" in agent binary!
idx = buf.find(b'group_control_event')
print('group_control_event in agent binary:', idx)
if idx != -1:
    print('Found group_control_event in agent at:', hex(idx))
else:
    print('NOT found in agent binary!')

# What about start_preview and stop_preview in agent binary?
print('start_preview in agent:', buf.find(b'start_preview'))
print('stop_preview in agent:', buf.find(b'stop_preview'))
