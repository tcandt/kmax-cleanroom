# Phase 2C.3G — Server Configuration REST Route Family Forensic Analysis Report

**Execution Timestamp**: `2026-09-16 07:15:00 UTC`  
**Target Canonical Binary**: `webrtc-signaling` (Linux AMD64 ELF, SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Routes Under Audit**:
1. `/api/server/addresses`
2. `/api/default_settings`
3. `/api/ice_servers`
4. `/api/version`

**Status**: **FORENSIC GATE PASSED — READY FOR RECONSTRUCTION**

---

## 1. Route Identities & Architectural Separation

From `ROUTE_HANDLER_MAP.json`, `FUNCTION_MAP.json`, and Capstone disassembly of `main.main` in the canonical binary:

| Route Pattern | Registration Call VA | Handler Symbol | Handler VA | Size (Bytes) | Role & Semantics |
|---|---|---|---|---|---|
| `/api/server/addresses` | `0x765bf8` | `main.vz0hZo0q1IzM` | `0x7632a0` | 3,072 | Environment address discovery: resolves non-loopback network interfaces and returns request host |
| `/api/default_settings` | `0x765ce8` | `main.j0yBBXR1Hjl` | `0x768980` | 3,648 | In-memory global default settings dispatcher: GET (authenticated), POST (admin only), rejects others |
| `/api/ice_servers` | `0x765d00` | `main.vREP2EE2` | `0x768500` | 1,152 | WebRTC ICE / STUN / TURN server configuration distributor |
| `/api/version` | `0x765d18` | `main.ys0CAJV5f5k` | `0x769840` | 1,248 | Public daemon metadata dispenser: version, git commit, build time |

All 4 routes are registered in `main.main` directly via `http.HandleFunc`.
- Each handler starts by writing standardized CORS headers (`Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE`, `Access-Control-Allow-Headers: Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization`).
- Each handler intercepts HTTP `OPTIONS` requests immediately after writing CORS headers and responds with `200 OK` (0 body bytes).

---

## 2. 7-Verb Method Matrix

Observed wire behavior on all 4 routes across all 7 HTTP methods (`allow_redirects=False`):

### A. `/api/server/addresses`
| Method | Status | Content-Type | Content-Length | Body Preview | Semantic Meaning |
|---|---|---|---|---|---|
| **GET** | `200 OK` | `application/json` | ~270 | `{"code":0,"data":{"addresses":[...],"current":"..."}}` | Retrieves listening & interface addresses |
| **POST** | `200 OK` | `application/json` | ~270 | `{"code":0,"data":{"addresses":[...],"current":"..."}}` | Permissive verb handling |
| **PUT** | `200 OK` | `application/json` | ~270 | `{"code":0,"data":{"addresses":[...],"current":"..."}}` | Permissive verb handling |
| **PATCH** | `200 OK` | `application/json` | ~270 | `{"code":0,"data":{"addresses":[...],"current":"..."}}` | Permissive verb handling |
| **DELETE** | `200 OK` | `application/json` | ~270 | `{"code":0,"data":{"addresses":[...],"current":"..."}}` | Permissive verb handling |
| **HEAD** | `200 OK` | `application/json` | ~270 | `""` (wire bodyless, headers preserved) | Standard HTTP HEAD parity |
| **OPTIONS** | `200 OK` | (None) | 0 | `""` | CORS preflight |

### B. `/api/default_settings`
| Method | Status | Content-Type | Content-Length | Body Preview | Semantic Meaning |
|---|---|---|---|---|---|
| **GET** | `200 OK` | `application/json` | Variable | `{}` or `{"video_bitrate":...}` | Retrieves current in-memory settings |
| **POST** | `200 OK` | `application/json` | 20 | `{"status":"success"}` | Mutates in-memory settings (Admin only) |
| **PUT** | `405 Method Not Allowed` | `text/plain; charset=utf-8` | 19 | `'Method not allowed\n'` | Disallowed verb |
| **PATCH** | `405 Method Not Allowed` | `text/plain; charset=utf-8` | 19 | `'Method not allowed\n'` | Disallowed verb |
| **DELETE** | `405 Method Not Allowed` | `text/plain; charset=utf-8` | 19 | `'Method not allowed\n'` | Disallowed verb |
| **HEAD** | `405 Method Not Allowed` | `text/plain; charset=utf-8` | 0 | `""` (wire bodyless, Content-Length: 19) | Disallowed verb HEAD |
| **OPTIONS** | `200 OK` | (None) | 0 | `""` | CORS preflight |

### C. `/api/ice_servers`
| Method | Status | Content-Type | Content-Length | Body Preview | Semantic Meaning |
|---|---|---|---|---|---|
| **GET** | `200 OK` | `application/json` | Variable | `[{"urls":["stun:stun.l.google.com:19302"]}]` | Retrieves configured ICE server slice |
| **POST** | `200 OK` | `application/json` | Variable | `[{"urls":["stun:stun.l.google.com:19302"]}]` | Permissive verb handling |
| **PUT** | `200 OK` | `application/json` | Variable | `[{"urls":["stun:stun.l.google.com:19302"]}]` | Permissive verb handling |
| **PATCH** | `200 OK` | `application/json` | Variable | `[{"urls":["stun:stun.l.google.com:19302"]}]` | Permissive verb handling |
| **DELETE** | `200 OK` | `application/json` | Variable | `[{"urls":["stun:stun.l.google.com:19302"]}]` | Permissive verb handling |
| **HEAD** | `200 OK` | `application/json` | Variable | `""` (wire bodyless, headers preserved) | Standard HTTP HEAD parity |
| **OPTIONS** | `200 OK` | (None) | 0 | `""` | CORS preflight |

### D. `/api/version`
| Method | Status | Content-Type | Content-Length | Body Preview | Semantic Meaning |
|---|---|---|---|---|---|
| **GET** | `200 OK` | `application/json` | ~75 | `{"build_time":"...","git_commit":"...","version":"..."}` | Retrieves daemon compile-time metadata |
| **POST** | `200 OK` | `application/json` | ~75 | `{"build_time":"...","git_commit":"...","version":"..."}` | Permissive verb handling |
| **PUT** | `200 OK` | `application/json` | ~75 | `{"build_time":"...","git_commit":"...","version":"..."}` | Permissive verb handling |
| **PATCH** | `200 OK` | `application/json` | ~75 | `{"build_time":"...","git_commit":"...","version":"..."}` | Permissive verb handling |
| **DELETE** | `200 OK` | `application/json` | ~75 | `{"build_time":"...","git_commit":"...","version":"..."}` | Permissive verb handling |
| **HEAD** | `200 OK` | `application/json` | ~75 | `""` (wire bodyless, headers preserved) | Standard HTTP HEAD parity |
| **OPTIONS** | `200 OK` | (None) | 0 | `""` | CORS preflight |

---

## 3. Authentication & RBAC Matrix

Observed access control behavior:

| Route | ADMIN Token | NORMAL_USER Token | NO_AUTH_MODE | MISSING Token | INVALID Token | Notes |
|---|---|---|---|---|---|---|
| `/api/version` | `200 OK` | `200 OK` | `200 OK` | `200 OK` | `200 OK` | **PUBLIC ROUTE**: Zero token verification in `main.ys0CAJV5f5k`. |
| `/api/ice_servers` | `200 OK` | `200 OK` | `200 OK` | `401 Unauthorized` | `401 Unauthorized` | Requires authenticated session (Admin or User). |
| `/api/server/addresses` | `200 OK` | `200 OK` | `200 OK` | `401 Unauthorized` | `401 Unauthorized` | Requires authenticated session (Admin or User). |
| `/api/default_settings` (GET) | `200 OK` | `200 OK` | `200 OK` | `401 Unauthorized` | `401 Unauthorized` | Read allowed for any authenticated user. |
| `/api/default_settings` (POST) | `200 OK` | **`403 Forbidden: admin only\n`** | `200 OK` | `401 Unauthorized` | `401 Unauthorized` | **ADMIN-ONLY**: Explicit role check via `0x73ae20`. |

---

## 4. Discovered Data Models & Type Descriptors

Directly recovered from canonical ELF binary sections (`.rodata`, `.data`, `.noptrdata`):

### A. ICE Server Struct (`main.Py1TDt` @ `0x7e24e0`)
- **Total Struct Size**: 56 bytes, Alignment: 8 bytes
- **ABI Validation**:
  - `Field 0`: `KWpyoL` (`[]string`, size 24 bytes, offset 0), tag: `json:"urls"`
  - `Field 1`: `Do87J_` (`string`, size 16 bytes, offset 24), tag: `json:"username,omitempty"`
  - `Field 2`: `G4kKJB5xuff` (`string`, size 16 bytes, offset 40), tag: `json:"credential,omitempty"`
  - Struct fields are strictly contiguous and non-overlapping: `0 + 24 = 24`, `24 + 16 = 40`, `40 + 16 = 56`.
- **Slice Descriptor**: `*[]main.Py1TDt` at `0x797460`.
- **CLI Configuration Precedence**:
  1. `-ice_servers`: comma-separated string, formatted as `stun:host:port` or `turn:user:pass@host:port`.
  2. `-stun_server`: deprecated fallback STUN address if `-ice_servers` is omitted.
  3. Default fallback: `[{"urls":["stun:stun.l.google.com:19302"]}]`.

### B. Default Settings Map (`*map[string]interface{}` @ `0x7bf940`)
- **Runtime Type**: `map[string]interface{}`.
- **Initial Default Value**: `{}` (empty map).
- **Storage Lifecycle**: In-memory global variable.
- **Persistence Across Restart**: **NONE**. Restarting the daemon resets default settings to initial `{}`.
- **Error Handling on POST**:
  - Empty body: `400 Bad Request` (`'Invalid JSON\n'`)
  - Malformed JSON: `400 Bad Request` (`'Invalid JSON\n'`)
  - JSON Array: `400 Bad Request` (`'Invalid JSON\n'`)
  - JSON Null: sets map variable to `nil`, responds `200 OK` (`'{"status":"success"}'`), readback produces `'null'`

### C. Server Addresses Schema
- **Envelope**:
  ```json
  {
    "code": 0,
    "data": {
      "addresses": ["host:port", "[ipv6]:port", ...],
      "current": "host:port"
    }
  }
  ```
- **Dynamic Derivation**:
  - `current`: verbatim `r.Host` from client HTTP request header.
  - `addresses[0]`: verbatim `r.Host`.
  - `addresses[1..n]`: non-loopback IP addresses discovered via `net.InterfaceAddrs()`, formatted with request host's port or daemon listening port. Loopback addresses (`127.0.0.1`, `::1`) are excluded from interface list. IPv6 addresses are bracketed `[ip]:port`.

### D. Version Globals
Directly recovered from `.data` / `.noptrdata` pointers:
- `version`: string at `0xbeee00` -> `"v0.3.6"`
- `git_commit`: string at `0xbeee10` -> `"2693ef1"`
- `build_time`: string at `0xbeee20` -> `"2026-09-07T09:58:25Z"`
- Origin: compile-time ldflags (`-X main.version=...`).

---

## 5. Scope Invariants & Strict Boundaries

1. **NO License Code**: No reference to `/api/activate`, `/api/license_status`, `/debug/license`, or licensing validation logic.
2. **NO Files / Tasks Code**: No reference to `/upload`, `/api/files`, `/api/tasks`, or task tracking logic.
3. **NO Signaling Transports**: No inclusion of WebSocket upgrader (`gorilla/websocket`), WebRTC peer connection manager (`pion/webrtc`), or `/register_device` / `/register_agent`.
4. **Clean Scope**: All 4 endpoints represent pure HTTP REST configuration and metadata services.

---

## 6. Gate Verdict

- Direct binary recovery: **100% COMPLETE**
- Dynamic oracle behavior verified: **100% PASS**
- Struct layout & ABI validation: **NON-OVERLAPPING Contiguous (56B)**
- Forensic Gate: **APPROVED TO PROCEED TO CLEANROOM RECONSTRUCTION**
