# WebRTC Signaling: Recovered HTTP & WebSocket Endpoints

- **Total Validated Endpoints**: 46
- **Binary Corroboration**: `webrtc-signaling` (Linux AMD64 & Windows AMD64 `.rodata`)

| Endpoint | Channel Type | Semantic Purpose | Binary Evidence Source |
|---|---|---|---|
| `/api/login` | `REST JSON` | Authentication: User & Admin login, JWT issuance | `.rodata` String Table |
| `/api/logout` | `REST JSON` | Authentication: Invalidate user session & token | `.rodata` String Table |
| `/api/auth-status` | `REST JSON` | Authentication: Query current session validity | `.rodata` String Table |
| `/api/user/ai-config` | `REST JSON` | User Configuration: AI integration settings | `.rodata` String Table |
| `/api/devices` | `REST JSON` | Device Registry: List all enrolled cloud devices & statuses | `.rodata` String Table |
| `/api/devices/list` | `REST JSON` | Device Registry: Fast listing endpoint | `.rodata` String Table |
| `/api/default_settings` | `REST JSON` | System Config: Query & update default VM bitrate/fps/size | `.rodata` String Table |
| `/api/server/addresses` | `REST JSON` | Network: Query reachable host IPs and ports | `.rodata` String Table |
| `/api/ice_servers` | `REST JSON` | WebRTC: Retrieve STUN/TURN server credentials | `.rodata` String Table |
| `/api/turn` | `REST JSON` | WebRTC: TURN server dynamic credentials/relay allocation | `.rodata` String Table |
| `/api/license_status` | `REST JSON` | Entitlement: Check current node license status & expiry | `.rodata` String Table |
| `/api/activate` | `REST JSON` | Entitlement: Submit license key for offline/online activation | `.rodata` String Table |
| `/api/share/list` | `REST JSON` | Device Sharing: List active device share tokens | `.rodata` String Table |
| `/api/share/info` | `REST JSON` | Device Sharing: Query share token metadata & access policy | `.rodata` String Table |
| `/api/share/create` | `REST JSON` | Device Sharing: Create guest share token with permissions | `.rodata` String Table |
| `/api/share/revoke` | `REST JSON` | Device Sharing: Invalidate an active share token | `.rodata` String Table |
| `/api/share/extend` | `REST JSON` | Device Sharing: Extend expiration time for shared session | `.rodata` String Table |
| `/api/share/update` | `REST JSON` | Device Sharing: Modify bitrate/audio/touch permissions | `.rodata` String Table |
| `/api/share/redeem_card` | `REST JSON` | Device Sharing: Redeem prepaid access card | `.rodata` String Table |
| `/api/admin/users` | `REST JSON` | Admin: List registered users and roles | `.rodata` String Table |
| `/api/admin/users/create` | `REST JSON` | Admin: Provision new user account | `.rodata` String Table |
| `/api/admin/users/delete` | `REST JSON` | Admin: Remove user account | `.rodata` String Table |
| `/api/admin/users/rename` | `REST JSON` | Admin: Modify username | `.rodata` String Table |
| `/api/admin/users/update` | `REST JSON` | Admin: Update user permissions and quotas | `.rodata` String Table |
| `/api/admin/users/update_note` | `REST JSON` | Admin: Set administrative note on user | `.rodata` String Table |
| `/api/admin/users/reset_password` | `REST JSON` | Admin: Force reset user password | `.rodata` String Table |
| `/api/admin/users/kick` | `REST JSON` | Admin: Force disconnect user from active sessions | `.rodata` String Table |
| `/api/admin/users/register_device` | `REST JSON` | Admin: Manually bind device to user | `.rodata` String Table |
| `/api/admin/assign` | `REST JSON` | Admin: Batch assign devices to users | `.rodata` String Table |
| `/api/files` | `REST JSON` | Storage: Enumerate APKs and uploaded media files | `.rodata` String Table |
| `/api/me/upload` | `REST JSON` | Storage: Upload APK or ROM files to server | `.rodata` String Table |
| `/api/tasks` | `REST JSON` | Task Queue: List background deployment/install tasks | `.rodata` String Table |
| `/api/tasks/details` | `REST JSON` | Task Queue: Retrieve detailed status of task execution | `.rodata` String Table |
| `/api/tags` | `REST JSON` | Organization: Device tag and label management | `.rodata` String Table |
| `/api/shortcuts` | `REST JSON` | Automation: Macro and shortcut definitions | `.rodata` String Table |
| `/api/version` | `REST JSON` | System: Query signaling server version & build tag | `.rodata` String Table |
| `/register_agent` | `WebSocket` | Agent Signaling: Device daemon registration & heartbeat channel | `.rodata` String Table |
| `/connect_client` | `WebSocket` | Client Signaling: Web browser WebRTC bridge & SDP exchange | `.rodata` String Table |
| `/snapshots` | `HTTP File` | Media: Static screenshot and preview image hosting | `.rodata` String Table |
| `/downloads` | `HTTP File` | Media: Download recorded streams / captured data | `.rodata` String Table |
| `/debug/pprof` | `Diagnostics` | Profiling: Go runtime pprof index | `.rodata` String Table |
| `/debug/pprof/cmdline` | `Diagnostics` | Profiling: Runtime command line | `.rodata` String Table |
| `/debug/pprof/profile` | `Diagnostics` | Profiling: CPU profiling sample stream | `.rodata` String Table |
| `/debug/pprof/symbol` | `Diagnostics` | Profiling: Symbol resolution lookup | `.rodata` String Table |
| `/debug/pprof/trace` | `Diagnostics` | Profiling: Execution trace generation | `.rodata` String Table |
| `/debug/license` | `Diagnostics` | Entitlement: Raw license claims debug inspection | `.rodata` String Table |
