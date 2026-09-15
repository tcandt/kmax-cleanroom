# CloudPhone Agent: WebRTC DataChannel Protocol

## 1. Discovered Channels & Message Formats

| Channel Label | Direction | Message Identifier | Purpose |
|---|---|---|---|
| `control` | Bidirectional | `group_control_event` | Multi-device coordinated touch & key event framing |
| `control` | Inbound | Binary touch packet | X, Y coordinates, action (down/move/up), pointer ID |
| `control` | Inbound | `setClipboard with paste=true` | Injects Unicode / non-ASCII text into device clipboard |
| `adb` | Bidirectional | `[ADB] OnMessage` | Transparent ADB bridge between web terminal and device adbd |
| `shell` | Bidirectional | `[Shell]` stream | Interactive PTY / shell execution session |
| `heartbeat` | Bidirectional | `HEARTBEAT-ACK` | Keepalive and latency measurement frame |

## 2. WebRTC Session Lifecycle

- Signaling connection established to `webrtc-signaling` via WebSocket (`/register_agent`).
- SDP Offer / Answer exchange using Pion WebRTC.
- ICE Candidate trickle with dynamic local/external IP replacement.
- Client disconnect trigger (`[Notification] User clicked disconnect WebRTC clients from web page`).
