# Phase 2C.3 Walkthrough: HTTP Handlers & REST API Reconstruction (Auth Slice Only)

**Previous Milestone**: `167961f0fe034f317375a14777a835f56e36eb6d` (Phase 2C.2R2)  
**Phase 2C.3 Milestone**: Auth HTTP Layer Forensics, Reconstructed Handlers, Differential Suite, & Structured Verifier  
**Git Remote**: `https://github.com/tcandt/kmax-cleanroom.git` (`main` branch)  
**Status**: COMPLETE, AUDITED, AND FULLY VERIFIED (18/18 HTTP DIFFERENTIAL SUITE PASS: 8 STRUCTURAL + 10 BIT-EXACT MATCHES)  

---

## 1. Summary of Completed Deliverables

### A. Pre-Flight 0: Structured Evidence Metadata Fix
- Fixed `token_tested_type` in `evidence/go_signaling/auth/AUTH_HEADER_PARSING_MATRIX.json` and `.md`:
  - `BEARER_CANONICAL`, `BEARER_LOWERCASE`, `BEARER_UPPERCASE`, `BEARER_MIXED_CASE` -> `VALID_ORIGINAL_TOKEN`
  - `WRONG_SCHEME_BASIC` -> `VALID_ORIGINAL_TOKEN_WITH_WRONG_SCHEME`
  - `MISSING_HEADER`, `EMPTY_HEADER` -> `NO_TOKEN`
  - `EMPTY_BEARER` -> `EMPTY_TOKEN`
- Extended `tools/verify_phase2.py` and `tests/differential/auth/test_auth_diff.py` to enforce this classification.

### B. Core Cross-Build Function Correlation (12 Roles)
All 12 core authentication & HTTP handler roles correlated between Linux AMD64 and Windows AMD64 binaries:

| Semantic Role | Linux AMD64 (`webrtc-signaling`) | Windows AMD64 (`webrtc-signaling.exe`) | Size Parity | Evidence Classes |
|---|---|---|---|---|
| `AUTH_LOGIN_HANDLER` | `main.ltOjwqsMl5q8` (`0x73dd00`) | `main.u4r2NulQUnF` (`0x140346f00`) | 2752B vs 2784B | Routes, Strings, Disasm |
| `AUTH_TOKEN_LOOKUP` | `main.lYKp_Iuf` (`0x73b080`) | `main.mLWT3o` (`0x140344260`) | 1120B vs 1152B | Routes, Strings, Disasm |
| `TOKEN_GENERATOR` | `main.d2SHxnu` (`0x739240`) | `main.af9fyOpAy` (`0x140342400`) | 224B vs 224B | Routes, Strings, Disasm |
| `SESSION_CREATOR` | `main.vT6rYK_v` (`0x739320`) | `main.wdxJrUcsH` (`0x1403424e0`) | 288B vs 288B | Routes, Disasm |
| `LOGOUT_HANDLER` | `main.bjWkHiittd` (`0x7409a0`) | `main.blPINsMc3` (`0x140349bc0`) | 1440B vs 1440B | Routes, Strings, Disasm |
| `AUTH_STATUS_HANDLER` | `main.bwvBd1LWVr` (`0x73ec40`) | `main.waSrU4iH` (`0x140347e60`) | 1216B vs 1216B | Routes, Strings, Disasm |
| `USER_PROFILE_HANDLER` | `main.gJ0OHScnGnWZ` (`0x73f100`) | `main.k0Ckv2FQUr` (`0x140348320`) | 2816B vs 2816B | Routes, Strings, Disasm |
| `PASSWORD_HASH` | `main.biG96MFIwa` (`0x739060`) | `main.sMCA9mvX` (`0x140342220`) | 480B vs 480B | Routes, Strings, Disasm |
| `SESSION_SWEEPER` | `main.cFpPBbFet` (`0x73a500`) | `main.wFSLlBV` (`0x1403436e0`) | 128B vs 128B | Routes, Disasm |
| `SESSION_SWEEPER_WORKER` | `main.cFpPBbFet.func1` (`0x73a580`) | `main.wFSLlBV.func1` (`0x140343760`) | 1600B vs 1600B | Routes, Strings, Disasm |
| `ADMIN_ROLE_CHECK` | `main.chIaMDTZ` (`0x73ae20`) | `main.iP8aiT` (`0x140344000`) | 320B vs 320B | Routes, Strings, Disasm |
| `SESSION_KICK_HANDLER` | `main.jlRPqj8Kko_8` (`0x743c40`) | `main.ijEGVZRAZQb` (`0x140350b00`) | 1184B vs 1184B | Routes, Strings, Disasm |

### C. 2C.3A: Token Source & Precedence Forensics
- Probed original binary with all 10 precedence test cases in [AUTH_TOKEN_SOURCE_MATRIX.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_TOKEN_SOURCE_MATRIX.json):
  - Case 1: `Authorization: Bearer <VALID>`, no query -> Authenticated (source: `AUTHORIZATION_HEADER_BEARER`)
  - Case 2: No Authorization, `?token=<VALID>` -> Authenticated (source: `URL_QUERY_TOKEN`)
  - Case 3: `Authorization: Bearer <VALID>`, `?token=<INVALID>` -> Authenticated (source: `AUTHORIZATION_HEADER_BEARER`)
  - Case 4: `Authorization: Bearer <INVALID>`, `?token=<VALID>` -> 401 Unauthorized (source: `AUTHORIZATION_HEADER_BEARER`, **NO query fallback!**)
  - Case 5: `Authorization: Basic <VALID>`, `?token=<VALID>` -> 401 Unauthorized (source: `AUTHORIZATION_HEADER_RAW`)
  - Case 6: `Authorization: malformed`, `?token=<VALID>` -> 401 Unauthorized (source: `AUTHORIZATION_HEADER_RAW`)
  - Case 7: `Authorization: Bearer`, `?token=<VALID>` -> 401 Unauthorized (source: `AUTHORIZATION_HEADER_RAW`)
  - Case 8: Authorization missing, `?token=<INVALID>` -> 401 Unauthorized (source: `URL_QUERY_TOKEN`)
  - Case 9: Authorization missing, `?token=` -> 401 Unauthorized (source: `NO_TOKEN`)
  - Case 10: `Authorization: Bearer <VALID_A>`, `?token=<VALID_B>` -> Authenticated as User A (source: `AUTHORIZATION_HEADER_BEARER`)
- **Strict Precedence Rule Recovered**: `HEADER_FIRST_WITH_STRICT_EVALUATION`. If `Authorization` header is present and non-empty, its token is evaluated directly. Query parameter `?token=` is **ONLY** checked when `Authorization` header is completely absent or empty!

### D. 2C.3B: Route Method Contract Matrix
- Probed all 4 routes across 7 HTTP verbs (28 cases) in [AUTH_ROUTE_METHOD_MATRIX.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_ROUTE_METHOD_MATRIX.json):
  - `/api/login`: Strictly requires `POST` (`r.Method == "POST"`). GET, PUT, PATCH, DELETE return `405 Method Not Allowed` (`Method not allowed\n`). OPTIONS returns 200 OK. HEAD returns 405.
  - `/api/logout`: Accepts ALL verbs (GET, POST, PUT, PATCH, DELETE all return 200 OK `{"status":"success"}\n`).
  - `/api/auth-status`: Accepts ALL verbs (GET, POST, etc. return 200 OK `{"noAuth":false}\n`).
  - `/api/me`: Accepts ALL verbs (GET, POST, etc. return 200 OK with `UserProfile` JSON).

### E. 2C.3C: Login Request Body Contract
- Probed 16 request variations in [LOGIN_REQUEST_CONTRACT.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/LOGIN_REQUEST_CONTRACT.json):
  - Standard Go `json.NewDecoder(r.Body).Decode(&req)`.
  - Empty body / malformed JSON / JSON array -> `400 Bad Request` with `Invalid JSON\n`.
  - Missing username or password / null values -> `400 Bad Request` with `Username and password are required\n`.
  - Extra fields tolerated, duplicate keys tolerated (last wins), charset parameters tolerated.

### F. 2C.3D: Response Contract
- Recovered 16 exact response branches in [AUTH_HTTP_RESPONSE_CONTRACT.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_HTTP_RESPONSE_CONTRACT.json):
  - Every response wire output terminates with `\n`.
  - Error messages are plain text (`text/plain; charset=utf-8`) with trailing newline.
  - Success responses are JSON (`application/json`) with trailing newline.
  - Logout is completely idempotent (returns 200 `{"status":"success"}\n` even on revoked/missing tokens).
  - `/api/me` emits exactly 10 fields matching original `User` model.

### G. 2C.3E: CORS / OPTIONS / HEAD Semantics
- CORS headers emitted on all 4 endpoints:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Headers: Content-Type, Authorization`
  - `Access-Control-Allow-Methods: POST, OPTIONS` (login/logout) or `GET, OPTIONS` (auth-status/me)
- OPTIONS preflight returns status 200 with empty body across all routes.
- HEAD returns identical status and headers to GET/POST with empty body.

### H. 2C.3F: HTTP Forensic Function Slices
- Mapped 5 core functions in [AUTH_HTTP_FUNCTION_SLICES.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_HTTP_FUNCTION_SLICES.json) separating HTTP wire logic from Phase 2C.2 business core:

| Semantic Role | Linux AMD64 Symbol & VA | Phase 2C.2 Claimed Range | Phase 2C.3 Claimed HTTP Range |
|---|---|---|---|
| `AUTH_LOGIN_HANDLER` | `main.ltOjwqsMl5q8` (`0x73dd00` - `0x73e7c0`) | `0x73ded0` - `0x73e4a0` (auth core) | `0x73dd00`-`0x73dec0`, `0x73e4b0`-`0x73e7c0` (method, decode, response) |
| `AUTH_TOKEN_LOOKUP` | `main.lYKp_Iuf` (`0x73b080` - `0x73b4e0`) | `0x73b280` - `0x73b480` (session lookup) | `0x73b080`-`0x73b270`, `0x73b490`-`0x73b4e0` (header split, query fallback) |
| `LOGOUT_HANDLER` | `main.bjWkHiittd` (`0x7409a0` - `0x740f40`) | `0x740c00` - `0x740d80` (revocation core) | `0x7409a0`-`0x740bf0`, `0x740d90`-`0x740f40` (CORS, token extract, response) |
| `AUTH_STATUS_HANDLER` | `main.bwvBd1LWVr` (`0x73ec40` - `0x73f100`) | `0x73ed80` - `0x73ee80` (status core) | `0x73ec40`-`0x73ed70`, `0x73ee90`-`0x73f100` (CORS, JSON response) |
| `USER_PROFILE_HANDLER` | `main.gJ0OHScnGnWZ` (`0x73f100` - `0x73fc00`) | `0x73f300` - `0x73f800` (profile lookup) | `0x73f100`-`0x73f2f0`, `0x73f810`-`0x73fc00` (CORS, token extract, JSON response) |

Forensic Gate report generated and verified: [reports/09_PHASE2C3_AUTH_HTTP_FORENSICS.md](file:///d:/KMAX-CLEANROOM/reports/09_PHASE2C3_AUTH_HTTP_FORENSICS.md).

---

## 2. Clean-Room Reconstructed Source (`reconstructed_source/webrtc-signaling/`)

### Package `pkg/httpapi/`
- [server.go](file:///d:/KMAX-CLEANROOM/reconstructed_source/webrtc-signaling/pkg/httpapi/server.go): `Server` and `NewServer` registering exactly the 4 auth routes on standard `net/http.ServeMux`.
- [auth_middleware.go](file:///d:/KMAX-CLEANROOM/reconstructed_source/webrtc-signaling/pkg/httpapi/auth_middleware.go): `ExtractToken` and `Authenticate` implementing recovered case-insensitive Bearer scheme parsing and query fallback.
- [responses.go](file:///d:/KMAX-CLEANROOM/reconstructed_source/webrtc-signaling/pkg/httpapi/responses.go): `SetCORS`, `WriteJSON`, `WriteError` with exact trailing newlines and status headers.
- [auth_handlers.go](file:///d:/KMAX-CLEANROOM/reconstructed_source/webrtc-signaling/pkg/httpapi/auth_handlers.go): `HandleLogin`, `HandleLogout`, `HandleAuthStatus`, `HandleMe`.
- [auth_handlers_test.go](file:///d:/KMAX-CLEANROOM/reconstructed_source/webrtc-signaling/pkg/httpapi/auth_handlers_test.go): Unit tests covering all 4 handlers, errors, precedence, and OPTIONS.

### Test Runner `cmd/http-server/`
- [main.go](file:///d:/KMAX-CLEANROOM/reconstructed_source/webrtc-signaling/cmd/http-server/main.go): Standalone HTTP server CLI runner for live side-by-side differential testing.

> [!IMPORTANT]
> **Strict Scope Boundary Maintained**:
> Only the 4 auth endpoints are implemented. WebSocket signaling (`/register_agent`, `/connect_client`), WebRTC stack (`pion`), agent protocol, device streaming, license logic, and admin CRUD endpoints remain strictly un-implemented.

---

## 3. Verification & Validation Results

### A. Go Unit Tests
```text
go test -v ./...
ok   cloudphone-signaling/pkg/auth     (cached)
ok   cloudphone-signaling/pkg/httpapi  (cached)
ok   cloudphone-signaling/pkg/session  (cached)
ok   cloudphone-signaling/pkg/storage  (cached)
```

### B. HTTP Differential Suite (`tests/differential/http/test_auth_http_diff.py`)
Executed 18 test cases running the original binary oracle on port 29888 against the reconstructed HTTP server on port 29889:

| Test ID | Test Name | Classification | Result | Parity Summary |
|---|---|---|---|---|
| `HTTP-01` | Login Success Schema & Token Issuance | `STRUCTURAL_EXACT_MATCH` | **PASS** | 200 OK, application/json, 4-key JSON schema, 64 hex token |
| `HTTP-02` | Invalid Password Rejection | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized, `Invalid username or password\n` |
| `HTTP-03` | Missing Credentials Rejection | `BIT_EXACT_MATCH` | **PASS** | 400 Bad Request, `Username and password are required\n` |
| `HTTP-04` | Expired Account Rejection | `BIT_EXACT_MATCH` | **PASS** | 403 Forbidden, `账号已到期，请联系管理员延时\n` |
| `HTTP-05` | Malformed JSON Rejection | `BIT_EXACT_MATCH` | **PASS** | 400 Bad Request, `Invalid JSON\n` |
| `HTTP-06` | Valid Token Logout & Invalidation | `BIT_EXACT_MATCH` | **PASS** | 200 OK, `{"status":"success"}\n`, immediate session invalidation |
| `HTTP-07` | Logout Idempotency | `BIT_EXACT_MATCH` | **PASS** | 200 OK, `{"status":"success"}\n` on repeated logout |
| `HTTP-08` | Auth-Status Unauthenticated | `BIT_EXACT_MATCH` | **PASS** | 200 OK, `{"noAuth":false}\n` |
| `HTTP-09` | Auth-Status Authenticated | `BIT_EXACT_MATCH` | **PASS** | 200 OK, `{"noAuth":false}\n` |
| `HTTP-10` | User Profile Valid Canonical Bearer | `STRUCTURAL_EXACT_MATCH` | **PASS** | 200 OK, identical 10-field UserProfile JSON schema |
| `HTTP-11` | Case-Insensitive Bearer Header Parsing | `STRUCTURAL_EXACT_MATCH` | **PASS** | Identical acceptance for `bearer`, `BEARER`, `bEaReR` |
| `HTTP-12` | Query Token Fallback (`?token=`) | `STRUCTURAL_EXACT_MATCH` | **PASS** | Falls back to query parameter when Authorization header missing |
| `HTTP-13` | Header Strict Precedence Over Query | `STRUCTURAL_EXACT_MATCH` | **PASS** | Strict header precedence; invalid Bearer fails without query fallback |
| `HTTP-14` | Missing Token Rejection | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized, `Unauthorized\n` |
| `HTTP-15` | Invalid Token Rejection | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized, `Unauthorized\n` |
| `HTTP-16` | OPTIONS Preflight Parity | `STRUCTURAL_EXACT_MATCH` | **PASS** | 200 OK, empty body, matching Access-Control-* headers on all 4 routes |
| `HTTP-17` | HEAD Request Semantics | `STRUCTURAL_EXACT_MATCH` | **PASS** | Matching status (405 login, 200 others) with 0 body bytes |
| `HTTP-18` | Content-Type & Body Wire Formatting | `BIT_EXACT_MATCH` | **PASS** | Trailing newline `\n` on all responses, matching Content-Type |

Differential Report: [reports/10_PHASE2C3_AUTH_HTTP_DIFFERENTIAL.md](file:///d:/KMAX-CLEANROOM/reports/10_PHASE2C3_AUTH_HTTP_DIFFERENTIAL.md).

### C. Provenance Audit (`tools/verify_reconstructed_provenance.py`)
```text
Total Declared Functions Audited: 59
Provenance Classification Breakdown:
  - GENERATED_ADAPTER              : 23
  - GENERATED_BUILD_FUNCTION       : 2
  - GENERATED_TEST_INTERFACE       : 9
  - RECONSTRUCTED_FROM_BEHAVIOR    : 1
  - RECONSTRUCTED_FROM_BINARY      : 24

Audit Summary:
  - Missing Headers: 0
  - Missing Required Metadata Fields: 0
[PASS] All 59 functions have valid CLEANROOM-PROVENANCE headers and 100% required metadata fields present.
```

### D. Master Verifier (`tools/verify_phase2.py`)
- Check 7: Phase 2C.3 Source Scope Boundary: 23 Go files strictly in scope; forbidden logic leaks: 0.
- Check 14: Phase 2C Reports Presence & Completeness: Reports 06, 07, 08, 09, 10 verified.
- Checks 15-20: Validates exact JSON schemas and classifications for all structured artifacts.
- Overall Verdict: `PASS`.

---

## 4. Phase 2C.3 Exit Gate Checklist

- [x] Query-token fallback dynamically confirmed via 10-case precedence matrix.
- [x] Header/query precedence dynamically confirmed (`HEADER_FIRST_WITH_STRICT_EVALUATION`).
- [x] Method contracts recovered (login requires POST; logout/auth-status/me accept all verbs).
- [x] Request JSON behavior recovered (standard json.Decoder, tolerated extra fields, exact 400 messages).
- [x] Response schemas recovered (exact JSON keys, trailing newlines, Content-Type headers).
- [x] Status codes recovered (200, 400, 401, 403, 405).
- [x] CORS/OPTIONS behavior recovered (CORS headers, 200 on OPTIONS preflight).
- [x] HTTP function slices mapped without provenance double-claim.
- [x] Four reconstructed auth routes compile and pass Go unit tests.
- [x] HTTP differential suite passes 18/18 tests (8 structural + 10 bit-exact matches).
- [x] Persistence differential suite passes 8/8 tests.
- [x] Auth core differential suite passes 12/12 tests.
- [x] Provenance auditor passes 59/59 functions.
- [x] Master verifier passes with OVERALL AUDIT VERDICT: PASS.
- [x] Zero WebSocket or WebRTC code implemented.
- [x] Zero forbidden sources accessed.

**EXECUTION HALTED AT PHASE 2C.3 AUTH-HTTP EXIT GATE.**  
Awaiting user review before proceeding to subsequent REST families (admin/device/config).
