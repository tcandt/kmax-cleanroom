# Forensic Report 05: Go Architecture & Dependency Recovery (Phase 2B.5 Remediation)

**Project**: KMAX Clean-Room Architecture Recovery  
**Standard**: Binary Evidence-Driven Architecture Recovery  
**Status**: AUDITED & RE-VERIFIED  

---

## 1. Executive Dependency Fingerprinting

Through static `.rodata` string analysis, runtime type descriptor recovery, and clean dynamic oracle probing, the dependencies of the original distributed binaries have been identified:

| Architectural Subsystem | Target Binary | Recovered Implementation | Forensic Evidence |
|---|---|---|---|
| **HTTP Router / Mux** | `webrtc-signaling` | **Go 1.22+ Standard `net/http.ServeMux`** | String `httpmuxgo121=1`, enhanced pattern matching (`DELETE /api/devices/{id}`), 405 Method Not Allowed handling |
| **WebSocket Framework** | `webrtc-signaling` | **`github.com/gorilla/websocket`** | Verbatim errors: `websocket: request origin not allowed by Upgrader.CheckOrigin`, `websocket: response does not implement http.Hijacker` |
| **WebRTC Media Engine** | `cloudphone-agent` | **`github.com/pion/webrtc/v3` (v3.3.6)** | Verbatim binary string `Pion WebRTC v3.3.6`, `PION_LOG_%s`, `PeerConnection`, `DataChannel` API |
| **JSON Serializer** | Both | **Go Standard Library `encoding/json`** | Struct tags `json:"..."`, `json: encoding error for type %q` |
| **Persistence Layer** | `webrtc-signaling` | **Flat-File JSON in `data/`** | Runtime generation of `users.json`, `device_tags.json`, `shares.json` |
| **Authentication Model** | `webrtc-signaling` | **In-Memory Session Token + SHA256 Salted Hash** | `users.json` password hash `SHA256(password + salt)`, 32-byte hex session tokens revoked on `/api/logout` |
| **Entitlement & Licensing** | `webrtc-signaling` | **Hardware Node Lock (`machine_id`)** | Claims: `machine_id`, `max_devices`, `days_remaining`, `expires_at`, verified via `/api/license_status` |
| **Companion Helper Execution** | `cloudphone-agent` | **`app_process / com.android.helper.CoreService`** | Direct APK staging to `/data/local/tmp/libsys_core.so` with UID 2000 shell privilege drop |

## 2. Refutation of False Architectural Hypotheses

1. **Gin / Chi / Echo Frameworks**: Confirmed **ABSENT** in binary evidence. Zero occurrences of Gin context or Chi routing nodes exist. The binary uses Go standard library routing.
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

## 4. Phase 2 Final Exit Gate Verification Checklist (Phase 2B.6 Passed)

- [x] **Role counts sum exactly to total**:
  - Signaling: `1967 (Confirmed) + 38 (Inferred) + 5566 (Unknown) == 7571`
  - Agent: `2582 (Confirmed) + 135 (Inferred) + 12681 (Unknown) == 15398`
- [x] **No third-party dependency misclassified as application role**: Generic library methods (`String`, `MarshalText`, `ReadFrom`, `AcceptTCPWithConn`, `DialContext`) completely excluded from project roles.
- [x] **Confirmed roles satisfy >= 2 evidence-class rule**: Every confirmed project role is backed by at least 2 independent evidence classes (e.g. route registration closure + instruction xref + dynamic oracle confirmation).
- [x] **Pclntab structural invariants pass**: `tests/test_pclntab_parser.py` validates monotonicity, non-overlapping ranges, sentinel entry, and valid name bounds.
- [x] **Tests are path-portable**: Uses `get_repo_root()` via `Path(__file__)` and `KMAX_CLEANROOM_ROOT` without hardcoded machine paths.
- [x] **All forensic generators committed**: `tools/forensics/pclntab_parser.py`, `tools/forensics/regenerate_function_maps.py`, `tools/forensics/regenerate_role_mappings.py`.
- [x] **Clean oracle prober committed**: `tools/oracle/clean_oracle_prober.py` and `tools/oracle/fixtures/`.
- [x] **Clean checkout can reproduce derived evidence**: Can run `python tools/verify_phase2.py` in any clean clone.
- [x] **Single verification entrypoint passes**: `tools/verify_phase2.py` outputs `OVERALL AUDIT VERDICT: PASS`.
- [x] **`reconstructed_source/` remains untouched**: Zero production Go source code written.

> [!IMPORTANT]
> Execution is strictly halted at the Phase 2 Final Exit Gate. No Go source reconstruction will commence until user review and explicit approval.
