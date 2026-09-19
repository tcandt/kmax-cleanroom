# Forensic Report 25: Phase 2C.3H License & Entitlement REST Reconstruction

**Status**: VERIFIED & AUDITED (Master Verifier Section 15: PASS)  
**Target Binary**: `webrtc-signaling` (Linux AMD64 SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Cleanroom Package**: `pkg/license`, `pkg/types`, `pkg/httpapi`  
**Cumulative Verification**: **244/244 PASS (100%)** across all 9 differential suites  
**Phase 2C.3H Differential Result**: **26/26 PASS (100%)**

---

## 1. Executive Summary

Phase 2C.3H successfully reconstructs the complete HTTP REST route family for server licensing, machine entitlement, and promotional capabilities:
- `/api/activate` (call `0x7659b8`, handler `main.jcraNgV8Jg` @ `0x74b6c0`)
- `/api/license_status` (call `0x7659d0`, handler `main.xdGI1n` @ `0x74c220`)
- `/debug/license` (call `0x7659e8`, handler `main.yyDyfaokeO` @ `0x74bf60`)

Reconstruction adhered strictly to cleanroom guidelines:
1. **Zero Keygen & Zero Bypass**: No attempt to generate fake activation keys or subvert the digital signature validation logic. Genuine original rejection paths (`{"error":"授权码格式错误"}\n`) and unactivated promotional status are reproduced with bit/character exactness.
2. **Deterministic Built-In Promo State**: In the absence of a verified license key on disk (`license.txt`), the server operates in unactivated promo mode with 13 deterministic status fields (e.g., `promo: true`, `max_devices: 20`, `post_promo_max_devices: 10`, `status: "valid"`, `expires_at: "2026-11-01"`).
3. **Local Offline Cryptography**: Forensic callgraph slicing confirmed that activation validation involves 0 outbound network or HTTP calls (`LICENSE_NETWORK_DEPENDENCY.json`).
4. **Dynamic Denominator & Semantic Forensic Gate**: Provenance and reproducibility gates were cleared before and after source generation, with dynamic denominator calculation dynamically summing canonical differential results.

---

## 2. Route Family & Registration Architecture

All 3 routes were machine-derived directly from `ROUTE_HANDLER_MAP.json` and ELF disassembly:

| Route Pattern | Handler Symbol | Handler VA | Registration Call VA | Middleware / Wrapper | Public / Auth Gating |
|---|---|---|---|---|---|
| `/api/activate` | `main.jcraNgV8Jg` | `0x74b6c0` | `0x7659b8` | Direct handler | Public payload validation (no auth token required) |
| `/api/license_status` | `main.xdGI1n` | `0x74c220` | `0x7659d0` | Direct handler | Public (no auth required); permissive on all 7 verbs |
| `/debug/license` | `main.yyDyfaokeO` | `0x74bf60` | `0x7659e8` | Direct handler | Public, but gated by `-debug` CLI flag (404 without `-debug`) |

---

## 3. Type Recovery & Data Layout

### 3.1 Activation Request Payload DTO
Derived from ELF struct descriptor at VA `0x7bd580`:
```go
// struct { GJjLo4tZRb string "json:\"license\"" }
type ActivationRequest struct {
    License string `json:"license"`
}
```
- Total struct size: 16 bytes (1 Go AMD64 string header: 8-byte pointer + 8-byte length).
- JSON field name tag is `json:"license"` (not `"key"` or `"activation_code"`).

### 3.2 License Status Response (13 Keys)
Constructed dynamically by `main.J_5lH4w6CU` (`0x735400`) using Go map descriptor `0x7bf940` (`map[string]interface{}`) with 13 entries:
```json
{
  "activated": false,
  "current_devices": 0,
  "customer": "",
  "days_remaining": 46,
  "error_msg": "",
  "expires_at": "2026-11-01",
  "license_expired": false,
  "license_source": "built-in",
  "machine_id": "XXXX-XXXX-XXXX-XXXX",
  "max_devices": 20,
  "post_promo_max_devices": 10,
  "promo": true,
  "status": "valid"
}
```
- `machine_id`: 16 hexadecimal uppercase characters formatted in 4 groups separated by hyphens. Derived deterministically from machine hardware properties.
- `expires_at`: Initial promo expiration date loaded from global string at `0xbeed90` (`"2026-11-01"`).
- `days_remaining`: Calculated dynamically as calendar day difference between UTC `now` and `expires_at`.

### 3.3 Persistence Specification
- **File Name**: `license.txt` (recovered from global string at `0xbeeda0`).
- **File Permissions**: Mode `0644` (`0x1a4`), written via `os.WriteFile` (`0x73487a`).
- **State Idempotency**: Failed activations do NOT mutate state or write `license.txt` to disk (`DOES_NOT_MUTATE_STATE`).

---

## 4. Reconstructed Source Architecture

The cleanroom implementation is structured into 3 modular files with 100% provenance annotations:
1. `pkg/types/license.go`:
   - `ActivationRequest`: JSON payload DTO.
   - `LicenseStatusResponse`: 13-field status projection.
   - `ActivationSuccessResponse` & `ActivationErrorResponse`: Exact status envelopes.
2. `pkg/license/manager.go`:
   - Thread-safe license state manager (`sync.RWMutex`).
   - Generates persistent `machine_id` matching binary format.
   - Reads/writes `license.txt` with mode `0644`.
   - Genuine rejection logic preserving original error messages.
3. `pkg/httpapi/license_handlers.go`:
   - `HandleActivate`: Gated to `POST, OPTIONS`, validates JSON, enforces payload constraints, applies CORS headers.
   - `HandleLicenseStatus`: Permissive on all HTTP verbs, returns unactivated built-in promo baseline.
   - `HandleDebugLicense`: Mirrors `/api/license_status` when `server.debug` is true; returns 404 text response `Not found\n` when `-debug` is disabled.

---

## 5. Differential Verification Suite (26/26 PASS)

The differential verification suite (`tests/differential/license/test_license_http_diff.py`) ran against the canonical binary oracle across 26 discrete cases:

| Case ID | Description | Oracle Status | Recon Status | Verdict |
|---|---|---|---|---|
| `LICENSE-HTTP-01` | `/api/license_status` baseline unactivated entitlement (13 keys, built-in promo) | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-02` | `/debug/license` status baseline parity when `-debug` is enabled | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-03` | `/debug/license` returns 404 when `-debug` flag is omitted | 404 Not found | 404 Not found | **PASS** |
| `LICENSE-HTTP-04` | `/api/license_status` public access without auth token | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-05` | `/api/license_status` public access with invalid Bearer token | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-06` | `/api/license_status` normal user access parity | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-07` | `/api/license_status` `-no-auth` mode access parity | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-08` | `/api/license_status` OPTIONS CORS preflight headers parity | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-09` | `/api/license_status` HEAD request parity (200 OK, empty wire body) | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-10-POST` | `/api/license_status` permissive verb POST parity | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-10-PUT` | `/api/license_status` permissive verb PUT parity | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-10-PATCH`| `/api/license_status` permissive verb PATCH parity | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-10-DELETE`| `/api/license_status` permissive verb DELETE parity | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-11-GET` | `/api/activate` method GET rejection parity (405 Method not allowed) | 405 | 405 | **PASS** |
| `LICENSE-HTTP-11-PUT` | `/api/activate` method PUT rejection parity (405 Method not allowed) | 405 | 405 | **PASS** |
| `LICENSE-HTTP-11-PATCH`| `/api/activate` method PATCH rejection parity (405 Method not allowed) | 405 | 405 | **PASS** |
| `LICENSE-HTTP-11-DELETE`| `/api/activate` method DELETE rejection parity (405 Method not allowed) | 405 | 405 | **PASS** |
| `LICENSE-HTTP-11-HEAD` | `/api/activate` method HEAD rejection parity (405 Method not allowed) | 405 | 405 | **PASS** |
| `LICENSE-HTTP-12` | `/api/activate` OPTIONS CORS preflight headers parity | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-13` | `/api/activate` empty POST body rejection parity (400 Invalid JSON payload) | 400 | 400 | **PASS** |
| `LICENSE-HTTP-14` | `/api/activate` malformed JSON body rejection parity (400 Invalid JSON payload) | 400 | 400 | **PASS** |
| `LICENSE-HTTP-15` | `/api/activate` empty JSON object rejection parity (`400 {"error":"授权码格式错误"}`) | 400 | 400 | **PASS** |
| `LICENSE-HTTP-16` | `/api/activate` empty license string rejection parity (`400 {"error":"授权码格式错误"}`) | 400 | 400 | **PASS** |
| `LICENSE-HTTP-17` | `/api/activate` invalid synthetic license key rejection parity (`400 {"error":"授权码格式错误"}`) | 400 | 400 | **PASS** |
| `LICENSE-HTTP-18` | `/api/activate` state idempotency after failed activation (no disk mutation) | 200 OK | 200 OK | **PASS** |
| `LICENSE-HTTP-19` | `/api/activate` validates payload without requiring auth token | 400 | 400 | **PASS** |

---

## 6. Master Verifier Audit & Cumulative Totals

Master verification script `tools/verify_phase2.py` was extended with Section 15. All 15 audit sections passed unconditionally:
- **Section 15.1**: 10/10 License Forensic Evidence Files Verified.
- **Section 15.2**: License Semantic Forensic Success Gate Evaluated (12/12 Invariants PASS).
- **Section 15.3**: License Route Family & Symbols Verified.
- **Section 15.4**: License Type Evidence & Payload Contract Verified.
- **Section 15.5**: License Method & Auth Matrices Verified.
- **Section 15.6**: Cleanroom Source Provenance Audited (145/145 functions annotated).
- **Section 15.7**: License Forensic Reproducibility Tool Verified (`10/10 REPRODUCIBLE`).
- **Section 15.8**: License REST Differential Results Verified (`26/26 PASS`).
- **Section 15.9**: Dynamic Cumulative Differential Denominator:

$$\text{CUMULATIVE\_PASS\_RATE} = \frac{\sum_{i=1}^{9} \text{Passed}_i}{\sum_{i=1}^{9} \text{Total}_i} = \frac{244}{244} = 100\%$$

Breakdown by Canonical Suite:
1. `AUTH_DIFFERENTIAL_RESULTS.json`: **12/12**
2. `AUTH_HTTP_DIFFERENTIAL_RESULTS.json`: **18/18**
3. `DEVICE_HTTP_DIFFERENTIAL_RESULTS.json`: **28/28**
4. `USER_ADMIN_HTTP_DIFFERENTIAL_RESULTS.json`: **30/30**
5. `TAG_HTTP_DIFFERENTIAL_RESULTS.json`: **20/20**
6. `SHARE_HTTP_DIFFERENTIAL_RESULTS.json`: **36/36**
7. `SHORTCUT_HTTP_DIFFERENTIAL_RESULTS.json`: **19/19**
8. `SERVER_CONFIG_HTTP_DIFFERENTIAL_RESULTS.json`: **55/55**
9. `LICENSE_HTTP_DIFFERENTIAL_RESULTS.json`: **26/26**
- **Cumulative Total**: **244/244 PASS (100%)**
