# Forensic Report 28: Phase 2C.4A — Transport Forensic Formalization

**Status**: FORENSIC FORMALIZATION COMPLETE & REPRODUCIBLE (PASS 23/23)  
**Phase**: 2C.4A  
**Mode**: STRICT FORENSIC ONLY (Zero Production Source Implemented)  
**Commit Target**: Canonical Forensic Evidence, Generator, Reproducer, Verifier Extensions  

---

## Historical Errata
> **Historical Errata**: The prior Files/Tasks closure commit and report retained the `IR2` label in certain document headers even though the metric closure and artifact scope correspond strictly to `IR3` semantics.

---

## 1. Executive Summary

In Phase 2C.4A, all preliminary exploratory research and scratch probe observations regarding the Transport subsystem (`/register_device`, `/register_agent`, `/connect_client`) have been formalised into canonical machine-derived evidence, reproducible tooling, and formal gate invariants.

### Key Metrics
| Item | Metric / Value | Verdict |
|---|---|---|
| Target Endpoints Derived | 3/3 (`/register_device`, `/register_agent`, `/connect_client`) | **PASS** |
| Transport Classification | All 3 routes classified as `WEBSOCKET_UPGRADE` (RFC 6455) | **PASS** |
| Canonical Evidence Denominator | 23 Artifacts + 1 Reproducibility Manifest | **PASS** |
| Forensic Gate Invariants | 18/18 non-tautological invariants evaluated | **PASS** |
| Reproducibility Pass Rate | 23/23 artifacts verified via deep semantic comparison | **PASS** |
| Zero Canonical Copying | Verified: Generator and Reproducer derive dynamically | **PASS** |
| Go Type Descriptors Recovered | 6 structs (`Device`, `DeviceInfo`, `Client`, `IceServer`, `TaskProgress`, `Share`) | **PASS** |
| Message Types Bounded | 11 Confirmed runtime messages, 12 Candidate disassembly messages | **PASS** |
| Source Boundary Enforcement | 0 production Go source files written, 0 routes added to server.go | **PASS** |
| Master Verifier Verdict | `python tools/verify_phase2.py` -> **OVERALL AUDIT VERDICT: PASS** | **PASS** |

---

## 2. Route Derivation & Registration Architecture

The transport routes were rediscovered directly from `evidence/go_signaling/ROUTE_HANDLER_MAP.json` and `FUNCTION_MAP.json`:

| Route Pattern | Handler Symbol | Handler VA | Size (Bytes) | Registration Call | Direct Callees (Sample) |
|---|---|---|---|---|---|
| `/register_device` | `main.rQffYkwYhw` | `0x74e4a0` | 6,368 | `http.HandleFunc` (`0x6e22e0`) | `gorilla/websocket.(*Upgrader).Upgrade`, `runtime.newobject` |
| `/register_agent` | `main.jdUaLc5NMO5` | `0x754b40` | 11,328 | `http.HandleFunc` (`0x6e22e0`) | `gorilla/websocket.(*Upgrader).Upgrade`, `(*Conn).ReadMessage` |
| `/connect_client` | `main.id8ybRmw69lm` | `0x7507c0` | 14,208 | `http.HandleFunc` (`0x6e22e0`) | `main.lYKp_Iuf`, `main.qCbJFL34`, `gorilla/websocket.(*Upgrader).Upgrade` |

Disassembly of `main.main` confirms registration via `http.HandleFunc` calls at VAs `0x765c10` (`/register_device`), `0x765c28` (`/register_agent`), and `0x765c40` (`/connect_client`).

---

## 3. Protocol Classification & Method Upgrade Matrix

Each route was rigorously probed with standard HTTP requests across all 7 verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`) and WebSocket upgrade variants:

1. **Standard HTTP without Upgrade**:
   - `GET`: Returns `400 Bad Request` with message `not a websocket handshake: 'upgrade' token not found in 'Connection' header`.
   - `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`: Return `405 Method Not Allowed` or `400 Bad Request`.
2. **Upgrade Variations**:
   - Valid Upgrade Header + Key + Version 13: Upgrades with `101 Switching Protocols` (subject to authentication).
   - Missing `Upgrade: websocket` (`Connection: Upgrade` only): Returns `400 Bad Request`.
   - Invalid `Upgrade: http`: Returns `400 Bad Request`.
   - Wrong Version (`Sec-WebSocket-Version: 12`): Returns `400 Bad Request`.
   - Missing / Malformed `Sec-WebSocket-Key`: Returns `400 Bad Request`.

All 3 routes strictly classify as `WEBSOCKET_UPGRADE`.

---

## 4. Authentication Timing & Token Scopes

Probes evaluated across 5 authentication contexts (`ADMIN`, `NORMAL_USER`, `MISSING_TOKEN`, `INVALID_TOKEN`, `NO_AUTH_MODE`):

- **/connect_client**:
  - **Timing**: `PRE_UPGRADE_VALIDATION`. Authentication occurs during HTTP handshake validation *before* `101 Switching Protocols` is issued.
  - **Rejection**: Missing or invalid token returns `HTTP 401 Unauthorized` immediately during handshake.
  - **Token Sources**: Supported via `Authorization: Bearer <token>`, `?token=<token>`, or `?share_token=<token>`.
  - **NO_AUTH Mode**: Running binary with `-no-auth` allows connection without token (status 101).
- **/register_device & /register_agent**:
  - **Timing**: `UNAUTHENTICATED`. Public registration endpoints in standard mode. Handshake completes with `101 Switching Protocols` without credentials.

---

## 5. Handshake & Initial Frame Contract

RFC 6455 Handshake specifics extracted from original binary:
- **Upgrader**: `github.com/gorilla/websocket` with 1024-byte read/write buffers.
- **CheckOrigin**: Allow all (`func(r *http.Request) bool { return true }`).
- **Response Headers**: `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Accept: <SHA1-base64>`.
- **Subprotocol**: None (`Sec-WebSocket-Protocol` header is absent).
- **Initial Server Frame**: Server sends **zero** initial unsolicited frames upon connect across all 3 routes. Server idles waiting for the client's first application JSON message.
- **Frame Masking Rule**: Client-to-server frames **must** be masked per RFC 6455. Unmasked client frames trigger immediate connection termination with RFC 6455 protocol error code 1002. Server-to-client frames are unmasked.
- **Control Frames**: Ping (opcode 9) is automatically replied with Pong (opcode 10) by the Gorilla connection handler. Close (opcode 8) is echoed.

---

## 6. Type & Registry Recovery

Struct descriptors recovered directly from the binary's `.rodata` section via descriptor layout analysis:

1. **`main.Device`** (`0x7ff0e0` / `0x7ff200`, 120 bytes):
   - Fields: `device_id` (string), `device_info` (interface{}), `online` (bool), `first_seen` (time.Time), `last_seen` (time.Time), `client_count` (int), `clients` ([]Client).
2. **`main.DeviceInfo`** (wire model / interface{}):
   - Fields: `model`, `ip`, `os_version`, `screen_width`, `screen_height`, `fps`.
3. **`main.Client`** (`0x74c640`, wire model / anonymous struct):
   - Fields: `kind` (string), `name` (string), `remaining_seconds` (int64).
4. **`main.IceServer`** (`0x7e24e0`, 48 bytes):
   - Fields: `urls` ([]string), `username` (string), `credential` (string).
5. **`main.TaskProgress`** (`0x7f4be0`, 72 bytes):
   - Fields: `device_id` (string), `status` (string), `progress` (int), `result` (string), `updated_at` (string).
6. **`main.Share`** (`0x80f700`, 192 bytes):
   - Fields: `token_id`, `card_code`, `device_id`, `creator`, `created_at`, `expires_at`, `access_mode`, `require_password`, `allow_clipboard`, `allow_file_tx`, etc.

---

## 7. Separate State Machines

To prevent behavioral cross-contamination, the three state machines are modeled separately:

### A. Device Registration (`REGISTER_DEVICE_STATE_MACHINE.json`)
- **Preconditions**: None.
- **Handshake**: Upgrades to WebSocket.
- **Activation**: Waits for `{"message_type": "register", "device_id": "...", "device_info": {...}}`. Upon receipt, registers device in global registry, sets `online = true`, timestamps `first_seen` and `last_seen`, replies with `{"message_type": "config", "device_id": "...", "ice_servers": [...]}`.
- **Loop**: Handles `forward`, `unregister`, `bridge_register`.
- **Teardown**: Marks `online = false`, records `last_offline`, emits `device_list_update` broadcast.

### B. Agent Registration (`REGISTER_AGENT_STATE_MACHINE.json`)
- **Preconditions**: None.
- **Handshake**: Upgrades to WebSocket.
- **Activation**: Waits for `{"type": "agent_register", "device_id": "...", "scrcpy_addr": "...", "is_webrtc": true}`. Binds agent socket to device ID session, replies with `{"message_type": "agent_register_ok", "status": "valid"}`.
- **Loop**: Handles `heartbeat` (updating `Device.last_seen`), `forward` (relaying WebRTC offer/answer/candidate to client), `task_progress`, `command_result`, `device_metrics`.
- **Teardown**: Unbinds agent socket, notifies connected client peers.

### C. Client Connection (`CONNECT_CLIENT_STATE_MACHINE.json`)
- **Preconditions**: Valid token (admin/user) or share token required before upgrade.
- **Handshake**: Upgrades with 101.
- **Binding**: Waits for `{"type": "connect", "device_id": "..."}`. Validates access permissions. Increments device `client_count`, allocates sequential `client_id` (1, 2, ...), appends client to `device.clients`. Sends initial `config` with `ice_servers`, followed by `device_list_update` broadcast.
- **Loop**: Handles `forward` (e.g. `request-offer`, `answer`, `candidate`), `command`, `touch`, `quit_agent`.
- **Teardown**: Decrements `client_count`, removes client from `device.clients`, emits `device_list_update` broadcast.

---

## 8. Message Taxonomy & Signaling Sequence

### Confirmed Runtime Messages
1. `register` (Device -> Server)
2. `config` (Server -> Device / Client)
3. `agent_register` (Agent -> Server)
4. `agent_register_ok` (Server -> Agent)
5. `connect` (Client -> Server)
6. `forward` (Client -> Server -> Agent / Agent -> Server -> Client)
7. `device_msg` (Server -> Client)
8. `device_list_update` (Server -> Broadcast)
9. `heartbeat` (Agent -> Server)
10. `error` (Server -> Client / Peer)
11. `request-offer` (Client -> Agent via forward payload)

### WebRTC P2P Signaling Flow
```
Browser Client                     Signaling Server                     Agent (Device)
      |                                   |                                   |
      |--- forward (request-offer) ------>|                                   |
      |                                   |--- forward (request-offer, cid) ->|
      |                                   |                                   |
      |                                   |<-- forward (offer, sdp, cid) -----|
      |<-- device_msg (offer, sdp) -------|                                   |
      |                                   |                                   |
      |--- forward (answer, sdp) -------->|                                   |
      |                                   |--- forward (answer, sdp, cid) --->|
      |                                   |                                   |
      |<== ICE Candidate trickle (bidirectional via forward / device_msg) ===>|
```

### WebRTC DataChannel Separation
Signaling transport over WebSocket is strictly distinguished from the WebRTC DataChannel plane:
- Channels: `control` (touch events, keyboard, clipboard), `adb` (ADB bridge), `shell` (PTY stream), `heartbeat` (`HEARTBEAT-ACK`).
- DataChannel traffic is peer-to-peer and completely bypasses the signaling server once the WebRTC connection is established.
- WebRTC / Pion implementation is strictly excluded from Phase 2C.4.

---

## 9. Canonical Evidence Files (23 Artifacts + 1 Manifest)

All generated into `evidence/go_signaling/transport/`:
1. `TRANSPORT_ROUTE_FAMILY.json`
2. `TRANSPORT_CLASSIFICATION_MATRIX.json`
3. `TRANSPORT_METHOD_UPGRADE_MATRIX.json`
4. `TRANSPORT_AUTH_MATRIX.json`
5. `TRANSPORT_REQUEST_CONTRACT.json`
6. `TRANSPORT_TYPE_EVIDENCE.json`
7. `WEBSOCKET_HANDSHAKE_CONTRACT.json`
8. `TRANSPORT_REGISTRY_TYPE_EVIDENCE.json`
9. `REGISTER_DEVICE_STATE_MACHINE.json`
10. `REGISTER_AGENT_STATE_MACHINE.json`
11. `CONNECT_CLIENT_STATE_MACHINE.json`
12. `TRANSPORT_MESSAGE_TYPE_EVIDENCE.json`
13. `TRANSPORT_MESSAGE_MATRIX.json`
14. `TRANSPORT_HEARTBEAT_CONTRACT.json`
15. `DEVICE_AGENT_CLIENT_ASSOCIATION_CONTRACT.json`
16. `WEBRTC_SIGNALING_CONTRACT.json`
17. `DATACHANNEL_TRANSPORT_CROSSMAP.json`
18. `TRANSPORT_DISCONNECT_CLEANUP_CONTRACT.json`
19. `TRANSPORT_CONCURRENCY_CONTRACT.json`
20. `TRANSPORT_EDGE_MATRIX.json`
21. `TRANSPORT_CROSS_BUILD_CORRELATION.json`
22. `TRANSPORT_FUNCTION_SLICES.json`
23. `TRANSPORT_FORENSIC_GATE_RESULT.json`
24. `TRANSPORT_REPRODUCIBILITY_MANIFEST.json`

---

## 10. Reproducibility Tooling & Invariant Verification

- `tools/forensics/generate_transport_forensics.py`: Generates all canonical evidence via fresh binary analysis and dynamic oracle execution.
- `tools/forensics/reproduce_transport_forensics.py`: Standalone read-only reproducer. Regenerates into a temporary scratch directory and validates 23/23 artifacts via deep semantic comparison with canonical evidence, leaving zero repository modifications.
- `tools/verify_phase2.py`: Extended with Section 17 auditing all 9 Phase 2C.4A forensic checks, source boundary enforcement, and working tree cleanliness.

---

## 11. Source Boundary Audit

Strict forensic boundary enforcement confirmed:
- `pkg/transport/`: DOES NOT EXIST.
- `pkg/websocket/`: DOES NOT EXIST.
- `pkg/webrtc/`: DOES NOT EXIST.
- `server.go`: Transport routes `/register_device`, `/register_agent`, `/connect_client` are **not** registered.
- `go.mod`: No `gorilla/websocket`, `nhooyr/websocket`, or `pion/webrtc` dependencies added.

Phase 2C.4A is 100% complete and verified. Phase 2C.4B (production source reconstruction) remains untouched awaiting explicit user direction.
