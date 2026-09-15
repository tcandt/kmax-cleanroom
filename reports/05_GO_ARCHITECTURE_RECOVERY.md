# Forensic Report 05: Go Architecture & Dependency Recovery (Phase 2B.5)

**Project**: KMAX Clean-Room Architecture Recovery  **Standard**: 100% Binary Evidence-Driven (Zero Guesswork)  **Status**: COMPLETED & VERIFIED  
---

## 1. Executive Dependency Fingerprinting

Through combined static `.rodata` string analysis, runtime type descriptor recovery, and dynamic oracle probing, the dependencies of the original distributed binaries have been conclusively identified without guesswork:

| Architectural Subsystem | Target Binary | Recovered Implementation | Forensic Evidence |
|---|---|---|---|
| **HTTP Router / Mux** | `webrtc-signaling` | **Go 1.22+ Standard `net/http.ServeMux`** | String `httpmuxgo121=1`, enhanced pattern matching (`DELETE /api/devices/{id}`), 405 Method Not Allowed handling |
| **WebSocket Framework** | `webrtc-signaling` | **`github.com/gorilla/websocket`** | Verbatim errors: `websocket: request origin not allowed by Upgrader.CheckOrigin`, `websocket: response does not implement http.Hijacker` |
| **WebRTC Media Engine** | `cloudphone-agent` | **`github.com/pion/webrtc/v3` (v3.3.6)** | Verbatim binary string `Pion WebRTC v3.3.6`, `PION_LOG_%s`, `PeerConnection`, `DataChannel` API |
| **JSON Serializer** | Both | **Go Standard Library `encoding/json`** | Intact struct tags `json:"..."`, `json: encoding error for type %q` |
| **Persistence Layer** | `webrtc-signaling` | **Flat-File JSON in `data/`** | Runtime generation of `users.json`, `device_tags.json`, `shares.json` |
| **Authentication Model** | `webrtc-signaling` | **In-Memory Session Token + SHA256 Salted Hash** | `users.json` password hash `SHA256(password + salt)`, 32-byte crypto/rand hex session tokens |
| **Entitlement & Licensing** | `webrtc-signaling` | **Hardware Node Lock (`machine_id`)** | Claims: `machine_id`, `max_devices`, `days_remaining`, `expires_at`, verified via `/api/license_status` |
| **Companion Helper Execution** | `cloudphone-agent` | **`app_process / com.android.helper.CoreService`** | Direct APK staging to `/data/local/tmp/libsys_core.so` with UID 2000 shell privilege drop |

## 2. Refutation of False Architectural Hypotheses

1. **Gin / Chi / Echo Frameworks**: Confirmed **ABSENT** in binary evidence. Zero occurrences of Gin context or Chi routing nodes exist. The binary uses Go 1.22 standard `net/http.ServeMux`.
2. **SQLite / PostgreSQL / MySQL**: Confirmed **ABSENT**. Persistence relies purely on flat-file JSON serialization (`users.json`, `shares.json`, `device_tags.json`).
3. **JWT Multi-Segment Base64 Tokens**: Confirmed **ABSENT**. The server uses 64-character hexadecimal opaque session tokens mapped in-memory and revoked upon `/api/logout`.

## 3. Concurrency, Goroutine & Channel Topologies

### 3.1. WebRTC Signaling Server Topology
- **Main Goroutine**: Parses CLI flags (`-port`, `-data`, `-assets`, `-debug`, `-tls`), loads `users.json` and `shares.json`, registers `net/http` route handlers, and starts `http.ListenAndServe` / `http.ListenAndServeTLS`.
- **Agent WebSocket Dispatcher Goroutine**: 1 read-pump and 1 write-pump per active agent connection (`/register_agent`). Synchronized via mutexes over device registry maps `map[string]*AgentConnection`.
- **Client WebSocket Dispatcher Goroutine**: 1 read-pump and 1 write-pump per connected web browser (`/connect_client`).
- **Session & License Watchdog**: Periodic ticker checking expired share links and user validity every 60 seconds (`[User] Account %s expired, tokens revoked and sessions kicked`).

### 3.2. CloudPhone Agent Daemon Topology
- **Main Bootstrap Goroutine**: Validates `/data/local/tmp/libsys_core.so` SHA256, drops privileges to shell UID 2000, spawns `app_process` helper process, and dials UDS sockets.
- **Scrcpy Video Ingestion Goroutine**: Reads 12-byte header frames from `scrcpy` UDS socket, parses NAL units, feeds video samples into Pion WebRTC video track.
- **Scrcpy Audio Ingestion Goroutine**: Reads raw audio/Opus frames from `scrcpy_audio` UDS socket and feeds into Pion WebRTC audio track.
- **Control Channel Goroutine**: Reads binary touch/key events from WebRTC DataChannel `control` and writes binary packets to `scrcpy_control` UDS socket.
- **Signaling Client Goroutine**: Maintains persistent WebSocket connection to `webrtc-signaling` (`/register_agent`), listens for incoming WebRTC offer requests, and responds with SDP answers.
- **Dynamic Bitrate Governor**: Monitors WebRTC packet loss / RTT; issues Type 19 (`SET_BITRATE`) control packets to helper in real-time (`[Agent] Dynamically adjusted scrcpy-server video bitrate to %d bps`).

## 4. Phase 2 Exit Gate Validation Status

- [x] All 46 route candidates classified with method & schema verification
- [x] HTTP methods verified via dynamic oracle probing (GET/POST/PUT/DELETE/OPTIONS)
- [x] Auth behavior and token lifecycle mapped (login, logout revocation, admin access)
- [x] Request schemas mapped from oracle errors and `.rodata` JSON tags
- [x] Response schemas verified against runtime oracle outputs
- [x] WebSocket state machines mapped for `/register_agent` and `/connect_client`
- [x] DataChannel binary and JSON framing mapped and correlated with Android helper
- [x] Helper IPC lifecycle, privilege dropping, and 4 UDS socket names mapped
- [x] Signaling role mapping generated with exact garbled symbols
- [x] Agent role mapping generated with exact garbled symbols
- [x] Dependencies fingerprinted without guessing (Go 1.22 net/http, gorilla/websocket, Pion v3.3.6, flatfile JSON)
- [x] Architecture report generated
- [x] Zero external repositories or forbidden source code accessed
