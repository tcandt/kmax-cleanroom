# CloudPhone Agent: Recovered Environment Variables & CLI Flags

| CLI Parameter | Environment Variable | Default Value | Functional Role |
|---|---|---|---|
| `-signaling` | `CP_AGENT_SIGNALING` | *Required* | WebSocket URL of signaling server (`ws://` or `wss://`) |
| `-id` | `CP_AGENT_ID` | `model-serial` | Unique hardware identifier for cloud phone registry |
| `-external-addr`| `CP_AGENT_EXTERNAL_ADDR`| Auto | External IP for WebRTC media routing |
| `-webrtc-port` | `CP_AGENT_WEBRTC_PORT` | `0` (dynamic) | Fixed UDP port for WebRTC container routing |
| `-resolution` | `CP_AGENT_RESOLUTION` | Native | Target capture resolution (e.g. `1080x1920`) |
| `-bitrate` | `CP_AGENT_BITRATE` | `4000000` | Video encoder bitrate (bps) |
| `-max-fps` | `CP_AGENT_MAX_FPS` | `30` / `60` | Maximum video frame rate |
| `-root` | `CP_AGENT_ROOT` | `false` | Run with root privileges (or Magisk mode) |
| `-audio` | `CP_AGENT_AUDIO` | `false` | Enable system audio capture stream |
| `-ice-servers` | `CP_AGENT_ICE_SERVERS` | Empty | Comma-separated list of STUN/TURN servers |
| `-upnp` | `CP_AGENT_UPNP` | `false` | Enable automatic UPnP port mapping |
| `-debug` | `CP_AGENT_DEBUG` | `false` | Verbose runtime logging |
