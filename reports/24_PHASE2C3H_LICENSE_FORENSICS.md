# Phase 2C.3H — License & Entitlement REST Route Family Forensic Analysis Report

**Execution Timestamp**: `2026-09-16 08:58:00 UTC`  
**Target Canonical Binary**: `webrtc-signaling` (Linux AMD64 ELF, SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Routes Under Audit**:
1. `/api/activate` (call `0x7659b8`, handler `main.jcraNgV8Jg` @ `0x74b6c0`)
2. `/api/license_status` (call `0x7659d0`, handler `main.xdGI1n` @ `0x74c220`)
3. `/debug/license` (call `0x7659e8`, handler `main.yyDyfaokeO` @ `0x74bf60`)

**Status**: **FORENSIC DISCOVERY COMPLETE — EVALUATING SEMANTIC GATE**

---

## 1. Route Identities & Architectural Separation

From [ROUTE_HANDLER_MAP.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/ROUTE_HANDLER_MAP.json), [FUNCTION_MAP.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/FUNCTION_MAP.json), and whole-function Capstone disassembly:

| Route Pattern | Registration Call VA | Handler Symbol | Handler VA | Size (Bytes) | Role & Semantics |
|---|---|---|---|---|---|
| `/api/activate` | `0x7659b8` | `main.jcraNgV8Jg` | `0x74b6c0` | 2,208 | Commercial license key activation endpoint: accepts JSON with `license` field, executes digital signature verification, persists to `license.txt` on success |
| `/api/license_status` | `0x7659d0` | `main.xdGI1n` | `0x74c220` | 1,056 | Public entitlement status dispenser: returns 13-field JSON state including machine ID, expiration date, max devices, and promotional flag |
| `/debug/license` | `0x7659e8` | `main.yyDyfaokeO` | `0x74bf60` | 704 | Diagnostic license endpoint: active only when `-debug` CLI flag is specified; returns identical 13-field state or 404 Not Found |

---

## 2. 7-Verb Method Matrix

Observed wire behavior across all 3 routes across all 7 HTTP methods (`allow_redirects=False`):

### A. `/api/activate`
- **POST**: Accepts JSON `{"license":"..."}`. If valid JSON with invalid key, returns `400 Bad Request` with `{"error":"授权码格式错误"}\n`. If empty/malformed body, returns `400 Bad Request` with `Invalid JSON payload\n`.
- **OPTIONS**: Returns `200 OK` (0 body bytes) with CORS headers:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Methods: POST, OPTIONS`
  - `Access-Control-Allow-Headers: Content-Type, Authorization`
- **GET, PUT, PATCH, DELETE, HEAD**: Return `405 Method Not Allowed` (`Method not allowed\n`).

### B. `/api/license_status`
- **GET, POST, PUT, PATCH, DELETE**: Return `200 OK` with 13-field JSON body. Permissive verb handling matching other read-only signaling endpoints.
- **HEAD**: Returns `200 OK` bodyless (headers preserved).
- **OPTIONS**: Returns `200 OK` bodyless (Content-Length: 0) with CORS headers:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Methods: GET, OPTIONS`
  - `Access-Control-Allow-Headers: Content-Type, Authorization`

### C. `/debug/license`
- **GET, POST, PUT, PATCH, DELETE**: When `-debug` is enabled: `200 OK` with 13-field JSON body. When `-debug` is disabled: `404 Not Found` (`Not found\n`).
- **OPTIONS**: Evaluated like standard requests (zero CORS headers emitted by this debug handler).

---

## 3. Authentication & RBAC Matrix

Probed across all 5 standard authentication modes:

| Route | ADMIN Token | NORMAL_USER Token | MISSING_TOKEN | INVALID_TOKEN | NO_AUTH_MODE | Access Classification |
|---|---|---|---|---|---|---|
| `/api/license_status` | `200 OK` | `200 OK` | `200 OK` | `200 OK` | `200 OK` | **PUBLIC**: No authentication required. |
| `/debug/license` | `200 OK` | `200 OK` | `200 OK` | `200 OK` | `200 OK` | **PUBLIC (Gated by `-debug`)**: No token required; returns 404 when `-debug` omitted. |
| `/api/activate` | `400 Rejection` | `400 Rejection` | `400 Rejection` | `400 Rejection` | `400 Rejection` | **PUBLIC**: No token required; validates payload directly. |

---

## 4. Recovered Data Types & Descriptors

Directly recovered from canonical ELF binary sections (`.rodata`, `.data`):

### A. Activation Request Payload (`0x7bd580`)
- **Go Runtime Type**: `*struct { GJjLo4tZRb string "json:\"license\"" }`
- **Size**: 16 bytes (pointer + length)
- **Field 0**: `GJjLo4tZRb` (`string`, offset 0, tag: `json:"license"`)

### B. Status Response Map (`0x7bf940`)
- **Go Runtime Type**: `map[string]interface{}` (allocated size: 13)
- **13 Fields**:
  1. `activated`: `bool` (default `false`)
  2. `current_devices`: `int` (default `0`)
  3. `customer`: `string` (default `""`)
  4. `days_remaining`: `int` (calculated relative to `expires_at`)
  5. `error_msg`: `string` (default `""`)
  6. `expires_at`: `string` (initial `2026-11-01` from `0xbeed90`)
  7. `license_expired`: `bool` (default `false`)
  8. `license_source`: `string` (initial `"built-in"` from `0x81ff75`)
  9. `machine_id`: `string` (generated from `main.ZbJsqTIiz3ML` @ `0x732ec0`)
  10. `max_devices`: `int` (default `20`)
  11. `post_promo_max_devices`: `int` (default `10`)
  12. `promo`: `bool` (default `true`)
  13. `status`: `string` (default `"valid"`)

### C. Error and Success Responses (`0x7c0340`)
- **Error Response**: `map[string]string` with key `"error"`: `"授权码格式错误"` (or `"Invalid JSON payload\n"` on decode failure).
- **Success Response**: `map[string]string` with keys `"status"`: `"success"` and `"message"`: `"激活码更新成功"`.

---

## 5. Persistence Contract

- **Filename**: `license.txt` (stored in `.data` at `0xbeeda0`).
- **File Mode**: `0644` (0x1a4) written via `os.WriteFile`.
- **Loading**: Checked and loaded at daemon startup in `main.LvbcDRl_uhc4` (`0x733fe0`).
- **Saving**: Persisted upon successful activation in `main.ODSX7KW` (`0x73487a`).
- **Failure Logging**: `[License] 写入本地授权文件失败：%v` (`0x838880`).
- **Lifecycle Invariant**: `license.txt` does not exist on fresh installation; failed activations do not create or touch `license.txt`.

---

## 6. Network Dependency & Offline Validation Architecture

- **Callgraph Traversal**:
  - `main.jcraNgV8Jg` calls `main.ODSX7KW`.
  - `main.ODSX7KW` calls `main.PmtRXo` for base64 decoding and cryptographic signature verification (`ETQ5mBYyCQ.HER71Q`).
  - Neither `main.ODSX7KW` nor `main.PmtRXo` contains any outbound HTTP client or socket dialing.
- **Classification**: **LOCAL OFFLINE CRYPTOGRAPHIC VALIDATION**.
- **Remote Activation Success**: Formally classified as `UNKNOWN_REMOTE_SUCCESS`. Zero synthetic traffic is sent to external services.
