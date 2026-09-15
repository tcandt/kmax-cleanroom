# Forensic Protocol Specification (Phase 2A / Phase 2 Remediation)

**Project**: KMAX Clean-Room Reverse Engineering & Behavior Recovery  
**Classification Standard**: Evidence-Driven Protocol Contracts (Static Disassembly + Clean Isolated Dynamic Oracle)  
**Status**: AUDITED & RE-VERIFIED  

---

## 1. Scope & Forensic Methodology

This document formalizes protocol contracts across the KMAX / CloudPhone distributed architecture. **Every claim is individually classified by its strongest available evidence. Not all contracts have been dynamically verified.**

Evidence is derived from three rigorous sources:
1. **Static Binary Disassembly**: `.rodata` string tables, `.gopclntab` function boundaries, and instruction-level disassembly of route registration in `main.main` (`webrtc-signaling`) and handler routines.
2. **Clean Dynamic Black-Box Oracle Probing**: Controlled local execution of the original binary (`webrtc-signaling.exe`) on isolated ports, testing all HTTP verbs independently with fresh, unpoisoned session tokens per endpoint, deterministic data fixtures (`users.json`, `shares.json`, `device_tags.json`), and `/api/logout` isolated strictly at the end.
3. **Bytecode Corroboration**: Direct cross-correlation with decompiled Android Helper classes (`ControlMessageReader.java`, `DesktopConnection.java`, `Streamer.java`).

### Evidence Classification Taxonomy
- `STATIC_AND_DYNAMIC_REGISTERED`: Route registered in binary control flow (`main.main`) and confirmed responsive via dynamic oracle probing.
- `STATIC_REGISTERED_ROUTE`: Route registered in binary control flow, but serves static assets or requires specific runtime attachments.
- `DYNAMIC_REGISTERED_ROUTE`: Route responsive dynamically under a prefix handler without a dedicated `main.main` registration string.
- `STATIC_STRING_CANDIDATE / NOT_RUNTIME_REGISTERED`: String candidate present in `.rodata` or frontend assets, but NOT registered in routing control flow and confirmed non-responsive (404 for all HTTP methods) by the dynamic oracle.
- `UNKNOWN_ROUTE_STATUS`: Insufficient static or dynamic evidence.

---

## 2. Master Route & Endpoint Verification Matrix

| # | Route Pattern | Allowed Method(s) | Auth Required | Request Schema | Response Schema | Evidence Classification |
|---|---|---|---|---|---|---|
| 1 | `/api/login` | `POST, OPTIONS` | None | `{username: str, password: str}` | `{token: str, username: str, role: str, assigned_devices: []}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 2 | `/api/auth-status` | `GET, POST, OPTIONS` | None | None | `{noAuth: bool}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 3 | `/api/user/ai-config` | `POST, OPTIONS` | Bearer Token | AI configuration payload | Status confirmation | `STATIC_AND_DYNAMIC_REGISTERED` |
| 4 | `/api/devices` | `DELETE, OPTIONS` | Bearer Token | `DELETE /api/devices/{id}` | `{status: 'success'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 5 | `/api/devices/` | `GET, POST, DELETE, OPTIONS` | Bearer Token | Path-based device routing | Device records / control | `STATIC_AND_DYNAMIC_REGISTERED` |
| 6 | `/api/default_settings` | `GET, POST, OPTIONS` | Bearer Token | Settings JSON | `{}` (default configuration) | `STATIC_AND_DYNAMIC_REGISTERED` |
| 7 | `/api/server/addresses` | `GET, OPTIONS` | Bearer Token | None | `{code: 0, data: {addresses: []}}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 8 | `/api/ice_servers` | `GET, POST, OPTIONS` | Bearer Token | None | `[{urls: ['stun:stun.l.google.com:19302']}]` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 9 | `/api/license_status` | `GET, OPTIONS` | None | None | `{status: str, machine_id: str, ...}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 10 | `/api/activate` | `POST, OPTIONS` | None | `{key: str}` | `{status: 'activated'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 11 | `/api/share/list` | `GET, OPTIONS` | Bearer Token | None | `{code: 0, data: []}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 12 | `/api/share/info` | `GET, POST, OPTIONS` | None (?token= param) | `?token=STRING` | `{device_id: str, ...}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 13 | `/api/share/create` | `POST, OPTIONS` | Bearer Token | `{device_id: str, expire_seconds: int}` | `{token: str, ...}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 14 | `/api/share/revoke` | `POST, OPTIONS` | Bearer Token | `{token: str}` | `{status: 'revoked'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 15 | `/api/share/extend` | `POST, OPTIONS` | Bearer Token | `{token: str, extend_seconds: int}` | `{expires_at: str}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 16 | `/api/share/update` | `POST, OPTIONS` | Bearer Token | `{token: str, guest_settings: {}}` | `{status: 'updated'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 17 | `/api/share/redeem_card` | `POST, OPTIONS` | None | `{card_code: str}` | `{status: 'redeemed'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 18 | `/api/admin/users` | `GET, OPTIONS` | Bearer Token (Admin) | None | `[{username: str, role: str, ...}]` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 19 | `/api/admin/users/create` | `POST, OPTIONS` | Bearer Token (Admin) | `{username: str, password: str, role: str}` | `{status: 'created'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 20 | `/api/admin/users/delete` | `POST, DELETE, OPTIONS`| Bearer Token (Admin) | `{username: str}` | `{status: 'deleted'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 21 | `/api/admin/users/rename` | `POST, OPTIONS` | Bearer Token (Admin) | `{old_username: str, new_username: str}` | `{status: 'renamed'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 22 | `/api/admin/users/update` | `POST, OPTIONS` | Bearer Token (Admin) | `{username: str, assigned_devices: []}` | `{status: 'updated'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 23 | `/api/admin/users/update_note` | `POST, OPTIONS` | Bearer Token (Admin) | `{username: str, note: str}` | `{status: 'updated'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 24 | `/api/admin/users/reset_password` | `POST, OPTIONS` | Bearer Token (Admin) | `{username: str, new_password: str}` | `{status: 'reset'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 25 | `/api/admin/users/kick` | `POST, OPTIONS` | Bearer Token (Admin) | `{username: str}` | `{status: 'kicked'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 26 | `/api/admin/assign` | `POST, OPTIONS` | Bearer Token (Admin) | `{devices: [], users: []}` | `{status: 'assigned'}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 27 | `/api/files` | `GET, OPTIONS` | Bearer Token | None | `[]` (file inventory) | `STATIC_AND_DYNAMIC_REGISTERED` |
| 28 | `/upload` | `POST, OPTIONS` | Bearer Token | Multipart Form Data (`file`) | File upload confirmation | `STATIC_AND_DYNAMIC_REGISTERED` |
| 29 | `/api/tasks` | `POST, OPTIONS` | Bearer Token | `{task_type: str, device_id: str}` | `{task_id: str}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 30 | `/api/tasks/details` | `GET, OPTIONS` | Bearer Token | `?id=TASK_ID` | `{task_id: str, status: str}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 31 | `/api/tags` | `GET, POST, OPTIONS` | Bearer Token | `{tags: [], deviceTags: {}}` | `{tags: [], deviceTags: {}}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 32 | `/api/shortcuts` | `GET, POST, OPTIONS` | Bearer Token | `[]` | `[]` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 33 | `/api/version` | `GET, OPTIONS` | None | None | `{version: str, git_commit: str, build_time: str}` | `STATIC_AND_DYNAMIC_REGISTERED` |
| 34 | `/register_device` | `GET, POST, OPTIONS` | Bearer Token | Device handshake parameters | Registration state | `STATIC_AND_DYNAMIC_REGISTERED` |
| 35 | `/register_agent` | `GET (Upgrade: ws)` | Agent Handshake | `{type: 'register', device_info: {}}` | Registration confirmation | `STATIC_AND_DYNAMIC_REGISTERED` |
| 36 | `/connect_client` | `GET (Upgrade: ws)` | Bearer or ?token= | `{type: 'offer', sdp: str}` | SDP Answer & ICE candidates | `STATIC_AND_DYNAMIC_REGISTERED` |
| 37 | `/devices` | `GET, OPTIONS` | Bearer Token | Query filters | Device summary | `STATIC_AND_DYNAMIC_REGISTERED` |
| 38 | `/snapshots/` | `GET` | Bearer Token / Session | `GET /snapshots/{file}` | JPEG/PNG stream | `STATIC_REGISTERED_ROUTE` |
| 39 | `/` | `GET` | None | None | Static Web Application HTML | `STATIC_AND_DYNAMIC_REGISTERED` |
| 40 | `/debug/license` | `GET` | None | None | Machine ID and license state | `STATIC_AND_DYNAMIC_REGISTERED` |
| 41 | `/api/devices/list` | `GET, OPTIONS` | Bearer Token | Device list parameters | Sub-route under `/api/devices/` | `DYNAMIC_REGISTERED_ROUTE` |
| 42 | `/downloads` | `GET, OPTIONS` | Bearer Token | File retrieval path | File stream | `DYNAMIC_REGISTERED_ROUTE` |
| 43 | `/debug/pprof` | `GET` | Bearer Token | None | Profiler index | `DYNAMIC_REGISTERED_ROUTE` |
| 44 | `/debug/pprof/cmdline` | `GET` | Bearer Token | None | Command line text | `DYNAMIC_REGISTERED_ROUTE` |
| 45 | `/debug/pprof/symbol` | `GET, POST` | Bearer Token | Symbol names | Symbol mappings | `DYNAMIC_REGISTERED_ROUTE` |
| 46 | `/debug/pprof/trace` | `GET` | Bearer Token | Trace parameters | Trace binary stream | `DYNAMIC_REGISTERED_ROUTE` |
| 47 | `/api/turn` | `NONE (404 all verbs)`| N/A | N/A | 404 page not found | `STATIC_STRING_CANDIDATE / NOT_RUNTIME_REGISTERED` |
| 48 | `/api/admin/users/register_device` | `NONE (404 all verbs)` | N/A | N/A | 404 page not found | `STATIC_STRING_CANDIDATE / NOT_RUNTIME_REGISTERED` |
| 49 | `/debug/pprof/profile` | `NONE (404)` | N/A | N/A | 404 page not found | `STATIC_STRING_CANDIDATE / NOT_RUNTIME_REGISTERED` |
| 50 | `/api/logout` | `ANY (POST/GET/PUT/DELETE)`| Session Token | None | `{status: 'success'}` (Revokes Token) | `STATIC_AND_DYNAMIC_REGISTERED` |

> [!IMPORTANT]
> **Resolution of the `/api/turn` Discrepancy**:
> `/api/turn` was previously listed as a confirmed endpoint due to its presence as a string in `.rodata`. Disassembly of `main.main` reveals that it is **never registered** in the HTTP multiplexer. Dynamic black-box probing against the original binary across all HTTP methods (GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD) returns `404 page not found`. It is correctly reclassified as `STATIC_STRING_CANDIDATE / NOT_RUNTIME_REGISTERED`.

> [!NOTE]
> **Dynamic Oracle Isolation & `/api/logout` Ordering**:
> Probing `/api/logout` revokes the active session token in memory. In the remediated oracle test suite, every endpoint was evaluated in an isolated session with fresh credentials. `/api/logout` was tested strictly last, preventing token invalidation cascade across other authenticated endpoints.

---

## 3. WebSocket Signaling State Machine

### 3.1. `/register_agent` Protocol
1. **Handshake**: Initiated by `cloudphone-agent` via HTTP GET with headers `Upgrade: websocket` and `Connection: Upgrade`.
2. **Registration Frame** (Agent -> Server):
   ```json
   {
     "type": "register",
     "device_info": {
       "id": "<device_serial>",
       "name": "<model_name>",
       "width": 1080,
       "height": 1920,
       "camera_facing": "front/back",
       "camera_zoom": 1.0
     }
   }
   ```
3. **Server Registry State Transition**: Server registers agent in memory (`[Agent] Fat Device %s registered`), caches device info, and marks device online.
4. **Heartbeat Protocol**: Gorilla ping-pong handler (`SetPingHandler` / `SetPongHandler`). Interval 30s. Missing 2 pings triggers connection teardown.
5. **Client Connect Request** (Server -> Agent):
   ```json
   {
     "type": "offer_request",
     "client_id": "<uuid>",
     "ice_servers": [{"urls": ["stun:stun.l.google.com:19302"]}]
   }
   ```
6. **SDP / ICE Relay**: Bidirectional exchange of `offer`, `answer`, and `candidate` payloads between agent and server.

### 3.2. `/connect_client` Protocol
1. **Authentication**: Client connects with `?token=<share_token>` or HTTP header `Authorization: Bearer <session_token>`. Unauthenticated requests rejected with `401 Unauthorized`.
2. **Device Binding**: Client requests session for `device_id`.
3. **SDP Offer Exchange**: Client sends SDP offer; server proxies offer to corresponding agent; agent creates answer using Pion WebRTC v3.3.6 and sends answer back to client.
4. **Tear-Down Event**: Server handles disconnect notification (`[Notification] User clicked disconnect WebRTC clients from web page`) and tears down peer connection.

---

## 4. Android IPC & Helper Protocol Contracts

### 4.1. Local Abstract UNIX Domain Sockets
The agent communicates with `com.android.helper.CoreService` over 4 abstract UNIX Domain Sockets:
1. `@scrcpy`: Video elementary stream. Frame packets preceded by 12-byte header:
   - `PTS_AND_FLAGS`: 8 bytes Big-Endian uint64 (Bit 63: Config frame flag; Bits 0-62: Presentation Timestamp in microseconds).
   - `PACKET_LENGTH`: 4 bytes Big-Endian uint32 (Payload size in bytes).
2. `@scrcpy_audio`: Raw PCM or Opus audio packet stream.
3. `@scrcpy_control`: Binary input commands parsed by `ControlMessageReader.java`.
4. `@scrcpy_touch`: Fast touch event injection channel.

### 4.2. Binary Control Packet Specifications (`@scrcpy_control`)
Corroborated by `ControlMessageReader.java`:
- `Type 0: INJECT_KEYCODE`: `[0x00] [ACTION: u8] [KEYCODE: u32 BE] [REPEAT: u32 BE] [METASTATE: u32 BE]`
- `Type 1: INJECT_TEXT`: `[0x01] [LEN: u32 BE] [UTF8_BYTES: LEN bytes]`
- `Type 2: INJECT_TOUCH_EVENT`: `[0x02] [ACTION: u8] [POINTER_ID: u64 BE] [X: u32 BE] [Y: u32 BE] [WIDTH: u16 BE] [HEIGHT: u16 BE] [PRESSURE: u16 BE] [BUTTONS: u32 BE]`
- `Type 3: INJECT_SCROLL_EVENT`: `[0x03] [X: u32 BE] [Y: u32 BE] [WIDTH: u16 BE] [HEIGHT: u16 BE] [HSCROLL: i32 BE] [VSCROLL: i32 BE]`
- `Type 19: SET_BITRATE`: `[0x13] [BITRATE_BPS: u32 BE]` (Dynamic bitrate throttling)
