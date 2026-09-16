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

## 5. Phase 2R / 2R.1: Reference Intelligence Normalization & Reproducibility Closure

**Milestone**: `PHASE_2R.1_REFERENCE_EVIDENCE_REMEDIATION`  
**Report**: [Report 11R](file:///d:/KMAX-CLEANROOM/reports/11R_REFERENCE_EVIDENCE_REMEDIATION.md) (Supersedes historical Report 11)  
**Cleanroom Commit Baseline**: `906b9aff14d25a8743bcef1ce223acd3ece32e47`  
**Reference Sources Pinned**:
- `tcandt/scrcpyoverwebrtc`: `65567d777bccb11d2a6d93b6acc735478e880b5b`
- `hqw700/cloudphone-official`: `ceb66b20ad4c6f7b217d38852ea9ec2bd70fcd39`  
**Status**: COMPLETE, AUDITED, AND FULLY VERIFIED (26/26 MASTER VERIFIER INVARIANTS PASS)

### A. Canonical Artifact Identity Repair & Census
- Reconciled [BASELINE.json](file:///d:/KMAX-CLEANROOM/evidence/reference/BASELINE.json) with exact canonical hashes in `EXPECTED_HASHES`:
  - `cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling`: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`
  - `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe`: `374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917`
  - `cloudphone-v0.3.6 (1)/android/cloudphone-agent`: `9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4`
- Formalized canonical vs supplemental census in [ARTIFACT_IDENTITY_AUDIT.md](file:///d:/KMAX-CLEANROOM/evidence/reference/ARTIFACT_IDENTITY_AUDIT.md) and [ARTIFACT_IDENTITY_AUDIT.json](file:///d:/KMAX-CLEANROOM/evidence/reference/ARTIFACT_IDENTITY_AUDIT.json). `agentd/cloudphone-agent-amd64` classified as `SUPPLEMENTAL_DISTRIBUTED_ARTIFACT`; `agentd/cloudphone-agent-arm64` classified as `BYTE_IDENTICAL_ALIAS`. Zero symbol/VA mixing.

### B. Reference External-Read Exception & Pinned Content Hashes
- Formalized authorized Lane B external-read exception in [REFERENCE_ACCESS_AUDIT.json](file:///d:/KMAX-CLEANROOM/evidence/reference/REFERENCE_ACCESS_AUDIT.json) (`AUTHORIZED_REFERENCE_LANE_EXTERNAL_READ`). Confirmed Lane A source reconstruction remained strictly isolated.
- Materialized all 12 reference source files into immutable local snapshots under `evidence/reference/raw/`.
- Cryptographically pinned all 12 files with git blob SHA, SHA256, byte size, and line count in [REFERENCE_SOURCE_HASHES.json](file:///d:/KMAX-CLEANROOM/evidence/reference/REFERENCE_SOURCE_HASHES.json).

### C. Committed Extraction Tooling & Reproducibility
- Committed all 5 extraction scripts and master reproducibility verifier into `tools/reference/`:
  - [extract_protocol_index.py](file:///d:/KMAX-CLEANROOM/tools/reference/extract_protocol_index.py)
  - [extract_datachannels.py](file:///d:/KMAX-CLEANROOM/tools/reference/extract_datachannels.py)
  - [extract_signaling_state_machine.py](file:///d:/KMAX-CLEANROOM/tools/reference/extract_signaling_state_machine.py)
  - [extract_agent_cli.py](file:///d:/KMAX-CLEANROOM/tools/reference/extract_agent_cli.py)
  - [build_reference_crossmap.py](file:///d:/KMAX-CLEANROOM/tools/reference/build_reference_crossmap.py)
  - [reproduce_reference_evidence.py](file:///d:/KMAX-CLEANROOM/tools/reference/reproduce_reference_evidence.py)
- All tools read exclusively from local snapshots in `evidence/reference/raw/`.
- `reproduce_reference_evidence.py` regenerates into a temp directory and performs bit/key exact verification across all 5 JSON matrices with zero discrepancies (**PASS**).

### D. Corrected WebRTC DataChannel Protocol Matrix
- Corrected `input-channel` in [DATACHANNEL_REFERENCE_MATRIX.json](file:///d:/KMAX-CLEANROOM/evidence/reference/DATACHANNEL_REFERENCE_MATRIX.json) to JSON string framing (`type: 'touch'` / `type: 'inject_scroll'`) directly observed in `useWebRTC.js:1031-1044, 1141-1152`. Demoted binary control protocol claim to `UNPROVEN_HYPOTHESIS`.
- Downgraded unproven `ordered` and `binaryType` properties on agent-created channels (`input-channel`, `clipboard-channel`, `camera-channel`) to `UNKNOWN_FROM_FRONTEND`.
- Browser-created channels (`file-channel`, `ai-command-channel`, `adb-channel`) verified from direct frontend source code.

### E. Corrected Client Signaling State Machine
- Purged unsupported speculative timeouts (10s, 5s, 15s, 3s) from T01–T06, T08 in [CLIENT_SIGNALING_STATE_MACHINE.json](file:///d:/KMAX-CLEANROOM/evidence/reference/CLIENT_SIGNALING_STATE_MACHINE.json); all set to `null` with `timeout_evidence: "NOT_OBSERVED"`.
- Retained `timeout_ms: 15000` solely for T07 (`executeCommandP2P`) where directly observed in source.
- Removed speculative automatic TCP fallback to `useWebSocketStream` from T06; verified that frontend only emits `message_type: 'webrtc_failed'`.

### F. Granular Evidence Classes & Strong Multi-Evidence Gate
- Replaced coarse `STATIC_BINARY_EVIDENCE` with 8 granular binary classes in [REFERENCE_TO_BINARY_CROSSMAP.json](file:///d:/KMAX-CLEANROOM/evidence/reference/REFERENCE_TO_BINARY_CROSSMAP.json).
- Enforced strong multi-evidence gate: `BINARY_SEMANTIC_CONFIRMED` requires `PUBLIC_REFERENCE` + at least 2 independent binary classes (23 items confirmed; 1 corroborated).

### G. Reclassified Agent CLI Flags
- Reclassified all 10 flags in [AGENT_CLI_REFERENCE_MATRIX.json](file:///d:/KMAX-CLEANROOM/evidence/reference/AGENT_CLI_REFERENCE_MATRIX.json).
- Documented flags (`-id`, `-signaling`, `-jar`, `-external-addr`, `-webrtc-port`, `-root`) confirmed with `SEMANTIC_XREF_CONFIRMED` or `FLAG_REGISTRATION_CONFIRMED` (HIGH confidence).
- Undocumented flags (`-camera-addr`, `-camera-size`, `-camera-facing`, `-ice-servers`) classified as `STRING_PRESENT` with `MEDIUM_INFERRED` confidence. Supplemental artifact explicitly cited.

### H. Mathematically Defined Progress & Coverage Metrics
- In [Report 11R](file:///d:/KMAX-CLEANROOM/reports/11R_REFERENCE_EVIDENCE_REMEDIATION.md), replaced unsupported percentages with deterministically measured metrics:
  - `SIGNALING_FUNCTION_TABLE_COVERAGE`: 7,571 / 7,571 (100.0%)
  - `AGENT_FUNCTION_TABLE_COVERAGE`: 15,398 / 15,398 (100.0%)
  - `ROUTE_DISCOVERY_COVERAGE`: 43 / 43 (100.0%)
  - `FRONTEND_ROUTE_BINARY_MATCH`: 35 / 37 (94.6%)
  - `RECONSTRUCTED_ROUTE_COUNT`: 4 / 43 (9.3%)
  - `IMPLEMENTED_SURFACE_DIFFERENTIAL_PASS_RATE`: 38 / 38 (100.0%)
  - `ESTIMATED_FUNCTIONAL_RECONSTRUCTION_PROGRESS`: ~15–20% (ESTIMATE, NOT A FORENSIC COVERAGE METRIC)

---

## 6. Phase 2R.1 Exit Gate Checklist

- [x] Canonical artifact hashes repaired in `BASELINE.json` (matches `EXPECTED_HASHES`).
- [x] Supplemental agent artifact classified (`agentd/cloudphone-agent-amd64`).
- [x] No artifact identity mixing between ARM64 Android and AMD64 Linux.
- [x] Reference external-read audit recorded (`REFERENCE_ACCESS_AUDIT.json`).
- [x] All 12 reference files content-hashed and materialized (`REFERENCE_SOURCE_HASHES.json`).
- [x] Extraction tools committed under `tools/reference/`.
- [x] Phase 2R evidence reproducible from pinned inputs (`reproduce_reference_evidence.py` PASS).
- [x] `input-channel` JSON framing corrected; binary protocol hypothesis demoted.
- [x] Unsupported DataChannel properties downgraded to `UNKNOWN_FROM_FRONTEND`.
- [x] Unsupported signaling timeouts removed (nullified with `NOT_OBSERVED`).
- [x] Unsupported TCP fallback removed from state machine.
- [x] Granular evidence classes implemented (8 independent classes).
- [x] Strong multi-evidence rule enforced ($\ge 2$ independent binary classes for confirmed).
- [x] CLI flag semantics no longer inferred from string presence alone; rodata flags marked `STRING_PRESENT`.
- [x] Coverage metrics mathematically defined with explicit numerators/denominators in Report 11R.
- [x] Previous persistence (8/8), auth core (12/12), and auth HTTP (18/18) suites still PASS.
- [x] Provenance auditor passes 59/59 declared functions.
- [x] Master verifier `tools/verify_phase2.py` passes all 26 invariant checks.
- [x] Zero Phase 2C.3B backend source written (strict HOLD maintained).

**PHASE 2R.1 COMPLETE.**

---

# Phase 2C.3BR Walkthrough: Device Registry Contract & Evidence Closure

**Milestone**: Phase 2C.3BR Device Registry Remediation & Contract Closure  
**Status**: COMPLETE, AUDITED, AND FULLY VERIFIED (`IMPLEMENTED_DEVICE_CONTRACT_DIFFERENTIAL_PASS_RATE = 28/28`)  

## 1. Executive Summary & Remediation Deliverables

In Phase 2C.3BR, all 7 identified hold/remediation items were rigorously addressed without touching out-of-scope modules (Users, Admin, Tags, Shares, WebSocket signaling):

1. **`/api/devices` Route Identity & ServeMux Redirect Semantics**:
   - Re-probed with `allow_redirects=False` recording `initial_status`, `Location`, and redirection behavior.
   - Proved that `/api/devices` returns `301 Moved Permanently` with `Location: /api/devices/` across all 7 verbs (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS).
   - Proved that `/api/devices` is NOT an alias, but Go `http.ServeMux` trailing-slash redirect to registered prefix route `/api/devices/`.
   - Updated [DEVICE_ROUTE_IDENTITY_MATRIX.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/devices/DEVICE_ROUTE_IDENTITY_MATRIX.json) and enforced in `DEV-HTTP-27`.

2. **`/devices` All-Method Contract Parity**:
   - Analyzed `main.i2EgUTaLmQs` (`0x74cf80`) machine instructions; confirmed absence of method checking (`r.Method == "GET"`).
   - Updated [DEVICE_ROUTE_FAMILY.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/devices/DEVICE_ROUTE_FAMILY.json) to reflect supported methods: `["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]`.
   - Added differential cases `DEV-HTTP-15` (POST), `DEV-HTTP-16` (PUT), `DEV-HTTP-17` (PATCH), and `DEV-HTTP-18` (DELETE), all passing with 200 OK.

3. **100% Binary-Derived Type Descriptors**:
   - Completely rewrote `tools/forensics/generate_device_forensics.py` to eliminate hardcoded field dictionaries and VAs.
   - Implemented dynamic Go runtime `structType` parser decoding ELF `.rodata` and type metadata directly from binary bytes:
     - `DeviceDTO` (`0x7ff0e0`): 120 bytes, 7 fields (`device_id`, `device_info`, `online`, `first_seen`, `last_seen`, `client_count`, `clients,omitempty`).
     - `DeviceEntry` (`0x805760`): 128 bytes, exactly 10 fields (`f0` to `f9`).
   - Regenerated [DEVICE_TYPE_EVIDENCE.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/devices/DEVICE_TYPE_EVIDENCE.json) purely from raw ELF machine bytes.

4. **Internal `DeviceEntry` Field Count & Provenance Reconciliation**:
   - Reconciled field count from binary: exact 10 fields (the historical "11 fields" was an unverified claim, now corrected).
   - In [pkg/types/device.go](file:///d:/KMAX-CLEANROOM/reconstructed_source/webrtc-signaling/pkg/types/device.go):
     - `DeviceDTO`: Classified as `DIRECT_TYPE_RECOVERY`.
     - `DeviceEntry`: Classified as `RECONSTRUCTED_FROM_BEHAVIOR` with explicit warning `NOT_LAYOUT_EQUIVALENT_TO_ORIGINAL_DEVICEENTRY`.
     - `webrtc_flag`: Honestly classified as `DEFERRED_INTERNAL_FIELD / PHASE_2C4_OR_2C6`.

5. **Machine-Derived Function Slices**:
   - Rewrote slice extraction in `generate_device_forensics.py` using Capstone disassembly bounded by `FUNCTION_MAP.json`.
   - Extracted direct calls, mutex locks, JSON serialization calls, and string xrefs from raw instruction bytes in [DEVICE_HTTP_FUNCTION_SLICES.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/devices/DEVICE_HTTP_FUNCTION_SLICES.json).

6. **Expanded Differential Coverage (28/28 Cases)**:
   - Expanded differential test suite from 14 to 28 cases covering all delete authorization/error branches, all `/devices` HTTP methods, OPTIONS preflight, HEAD semantics, ServeMux redirects, and No-Auth server mode.
   - Passed with `IMPLEMENTED_DEVICE_CONTRACT_DIFFERENTIAL_PASS_RATE = 28/28`.
   - Published [reports/13R_PHASE2C3B_DEVICE_CONTRACT_CLOSURE.md](file:///d:/KMAX-CLEANROOM/reports/13R_PHASE2C3B_DEVICE_CONTRACT_CLOSURE.md).

7. **No-Auth Server Mode Dynamic Contract**:
   - Launched isolated original binary with `-no-auth` flag.
   - Verified `/api/auth-status` returns 200 `{"noAuth":true}` and `/devices` serves unauthenticated queries.
   - Generated [evidence/go_signaling/devices/DEVICE_NOAUTH_CONTRACT.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/devices/DEVICE_NOAUTH_CONTRACT.json) and tested via `DEV-HTTP-28`.

8. **Forensic Reproducibility Pipeline**:
   - Created [tools/forensics/reproduce_device_forensics.py](file:///d:/KMAX-CLEANROOM/tools/forensics/reproduce_device_forensics.py) which regenerates all 9 device artifacts into a temporary directory and verifies deterministic bit/key parity (**PASS**).

---

## 2. Test Suite Summary Matrix (28 Cases)

| Test ID | Test Name | Classification | Result |
|---|---|---|---|
| `DEV-HTTP-01` | Empty Registry Admin Query | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-02` | Populated Registry One Device Schema & Invariants | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-03` | Populated Registry Multiple Devices Normalized DTO | `NORMALIZED_JSON_MATCH` | **PASS** |
| `DEV-HTTP-04` | Invalid Token Rejection | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-05` | Missing Token Rejection | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-06` | Normal User Assigned Device Filtering | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-07` | Normal User Unassigned Visibility | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-08` | Reconnected Device State Restoration | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-09` | Disconnect Lifecycle & Offline State | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-10` | Wrong Method (GET) on /api/devices/{id} | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-11` | HEAD Method on /devices | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-12` | OPTIONS Preflight CORS Headers | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-13` | Content-Type and Raw JSON Shape | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-14` | Online & Offline Deletion Lifecycle | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-15` | POST Method on /devices | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-16` | PUT Method on /devices | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-17` | PATCH Method on /devices | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-18` | DELETE Method on /devices | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-19` | DELETE Device as Normal Assigned User Rejection | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-20` | DELETE Device as Normal Unassigned User Rejection | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-21` | DELETE with Missing Token Rejection | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-22` | DELETE with Invalid Token Rejection | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-23` | DELETE Nonexistent Device ID | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-24` | DELETE Empty Device ID on /api/devices/ | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-25` | OPTIONS on Delete Route /api/devices/{id} | `STRUCTURAL_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-26` | HEAD on Delete Route /api/devices/{id} | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-27` | ServeMux Trailing Slash Redirect Semantics | `BIT_EXACT_MATCH` | **PASS** |
| `DEV-HTTP-28` | No-Auth Server Mode Unauthenticated Query | `BIT_EXACT_MATCH` | **PASS** |

---

## 3. Exit Gate Verification Checklist

- [x] `/api/devices` initial redirect semantics proven with redirects off (301 Moved Permanently)
- [x] `/devices` all-method behavior differential verified (all 7 verbs return 200 OK)
- [x] `DeviceDTO` type evidence machine-derived (parsed directly from ELF bytes at `0x7ff0e0`)
- [x] `DeviceEntry` field count resolved (exact 10 fields verified from runtime descriptor at `0x805760`)
- [x] Simplified internal struct no longer mislabeled direct recovery (`RECONSTRUCTED_FROM_BEHAVIOR`)
- [x] `webrtc_flag` classified honestly (`DEFERRED_INTERNAL_FIELD / PHASE_2C4_OR_2C6`)
- [x] HTTP function slices machine-derived (Capstone disassembly instruction tracking)
- [x] Device verifier validates underlying evidence (re-derives routes, type descriptors, function boundaries)
- [x] Delete authorization/error branches differential verified (401, 403, 404, 400, 405)
- [x] Exact DTO schema/type comparison added (`DEV-HTTP-02`)
- [x] No-Auth server mode dynamically tested (`DEV-HTTP-28` and `DEVICE_NOAUTH_CONTRACT.json`)
- [x] Lifecycle duplicate/abrupt cases observed (`DEVICE_REGISTRY_LIFECYCLE_MATRIX.json`)
- [x] Device forensic reproduction tool PASS (`reproduce_device_forensics.py`)
- [x] Persistence differential tests 8/8 PASS
- [x] Auth core differential tests 12/12 PASS
- [x] Auth HTTP differential tests 18/18 PASS
- [x] Device differential cases 28/28 PASS
- [x] Users/Admin differential cases 30/30 PASS
- [x] Provenance auditor 88/88 declared functions PASS
- [x] Master verifier `tools/verify_phase2.py` OVERALL AUDIT VERDICT: PASS
- [x] Zero production WebSocket implementation
- [x] Zero WebRTC implementation
- [x] Tags/Shares untouched

---

# Phase 2C.3C: Users & Admin REST Reconstruction

## 1. Overview & Forensic Gate Pass

- **Pre-Flight A Completed**: Corrected wording in `reproduce_device_forensics.py` and master verifier to distinguish static type reproducibility from committed dynamic invariants. Both `reproduce_device_forensics.py` and `reproduce_user_admin_forensics.py` regenerate evidence into isolated temporary scratch directories before canonical normalization and parity checks.
- **Route Family Discovered (11 routes)**:
  - `/api/admin/users` (List users, 0x741ec0)
  - `/api/admin/users/create` (Create user, 0x744140)
  - `/api/admin/users/delete` (Delete user, 0x745ba0)
  - `/api/admin/users/update` (Update permissions/expiry, 0x744c20)
  - `/api/admin/users/update_note` (Update note, 0x7464e0)
  - `/api/admin/users/reset_password` (Reset password, 0x746e80)
  - `/api/admin/users/rename` (Rename user, 0x740f40)
  - `/api/admin/users/kick` (Kick user, 0x747880)
  - `/api/admin/assign` (Assign devices, 0x7432a0)
  - `/api/register` (Public registration, 0x73e7c0)
  - `/api/user/ai-config` (User personal AI config, 0x73ffc0)
- **Direct Type Recovery from Binary ELF**:
  - `User` structType descriptor at `0x80a0c0` (152 bytes, 13 fields: YpukG23I, A13r7C, H8f8eOCvpE, Nddaca, IrGKkzPChN, GQdUwM, REj4vX, hYw0Qj, CEvG8R, tE7WfS, q_fDcg, dY9iT6, v_2v0W).
  - `AIConfig` structType descriptor at `0x7ed060` (64 bytes, 4 fields: ai_api_url, ai_api_key, ai_model, ai_provider).
  - 8 request DTO descriptors parsed directly from binary bytes.

## 2. Differential Test Results Matrix (30/30 PASS)

| Test ID | Test Name | Classification | Result | Notes |
|---|---|---|---|---|
| `USER-HTTP-01` | List Users Baseline | `STRUCTURAL_EXACT_MATCH` | **PASS** | 200 OK, application/json, matching array length & user ordering |
| `USER-HTTP-02` | Populated List Schema & Key Omissions | `BIT_EXACT_MATCH` | **PASS** | 12-field projection; password and salt strictly omitted |
| `USER-HTTP-03` | Normal User Admin Route Rejection (403) | `BIT_EXACT_MATCH` | **PASS** | 403 Forbidden with exact body `Forbidden\n` |
| `USER-HTTP-04` | Missing Token Rejection (401) | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized with exact body `Unauthorized\n` |
| `USER-HTTP-05` | Invalid Token Rejection (401) | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized with exact body `Unauthorized\n` |
| `USER-HTTP-06` | Create Valid User & Disk Persistence | `BIT_EXACT_MATCH` | **PASS** | 200 OK `{"status":"success"}\n`, 32-char hex salt, SHA256 stored |
| `USER-HTTP-07` | Duplicate User Conflict (409) | `BIT_EXACT_MATCH` | **PASS** | 409 Conflict with exact body `Username already exists\n` |
| `USER-HTTP-08` | Missing Fields on Create (400) | `BIT_EXACT_MATCH` | **PASS** | 400 Bad Request with exact body `Username and password are required\n` |
| `USER-HTTP-09` | Update User Note | `BIT_EXACT_MATCH` | **PASS** | 200 OK `{"status":"success"}\n`, note persisted |
| `USER-HTTP-10` | Assign Devices to User | `BIT_EXACT_MATCH` | **PASS** | 200 OK `{"status":"success"}\n`, assigned_devices updated |
| `USER-HTTP-11` | Update User Permissions | `BIT_EXACT_MATCH` | **PASS** | 200 OK `{"code":0,"data":{...},"msg":"success"}\n` |
| `USER-HTTP-12` | Update User Expiry | `BIT_EXACT_MATCH` | **PASS** | Expiration timestamp updated in ISO8601/RFC3339 format |
| `USER-HTTP-13` | Reset User Password | `BIT_EXACT_MATCH` | **PASS** | Generates fresh salt, re-hashes password, returns 200 OK |
| `USER-HTTP-14` | Login After Password Mutation | `BIT_EXACT_MATCH` | **PASS** | Old password rejected (401), new password authenticated (200) |
| `USER-HTTP-15` | Delete User & Mutation | `BIT_EXACT_MATCH` | **PASS** | 200 OK `{"status":"success"}\n`, removed from `users.json` |
| `USER-HTTP-16` | Delete Nonexistent User (404) | `BIT_EXACT_MATCH` | **PASS** | 404 Not Found with exact body `User not found\n` |
| `USER-HTTP-17` | Session Retained in Memory Post-Deletion | `STRUCTURAL_EXACT_MATCH` | **PASS** | Matches binary jump 0x73b459: active in-memory session valid on `/api/me` |
| `USER-HTTP-18` | No-Auth Mode Bypass on Admin Endpoints | `STRUCTURAL_EXACT_MATCH` | **PASS** | No-auth server mode bypasses admin token requirement |
| `USER-HTTP-19` | HEAD Method Behavior on List Users | `BIT_EXACT_MATCH` | **PASS** | 200 OK with Content-Type: application/json and 0 body bytes |
| `USER-HTTP-20` | OPTIONS and CORS Headers | `STRUCTURAL_EXACT_MATCH` | **PASS** | 200 OK with `Access-Control-Allow-Origin: *` |
| `USER-HTTP-21` | Persistence File Mode & JSON Contract | `BIT_EXACT_MATCH` | **PASS** | Atomic JSON format on disk matches original |
| `USER-HTTP-22` | Dynamic Reflection on /api/me | `BIT_EXACT_MATCH` | **PASS** | Device assignment mutation immediately visible in `/api/me` |
| `USER-HTTP-23` | Cannot Delete Self Guard (403) | `BIT_EXACT_MATCH` | **PASS** | 403 Forbidden with exact body `Cannot delete yourself\n` |
| `USER-HTTP-24` | Update Note Unknown User (404) | `BIT_EXACT_MATCH` | **PASS** | 404 Not Found with exact body `User not found\n` |
| `USER-HTTP-25` | Reset Password Unknown User (404) | `BIT_EXACT_MATCH` | **PASS** | 404 Not Found with exact body `User not found\n` |
| `USER-HTTP-26` | Assign Devices Unknown User (404) | `BIT_EXACT_MATCH` | **PASS** | 404 Not Found with exact body `User not found\n` |
| `USER-HTTP-27` | User Personal AI Config Update | `STRUCTURAL_EXACT_MATCH` | **PASS** | 200 OK and 4-field AIConfig persisted to users.json |
| `USER-HTTP-28` | Public Registration Disabled (403) | `BIT_EXACT_MATCH` | **PASS** | 403 Forbidden with exact error JSON message |
| `USER-HTTP-29` | Kick User Endpoint Contract | `BIT_EXACT_MATCH` | **PASS** | 200 OK on valid kick, 400 on empty username |
| `USER-HTTP-30` | Rename User Endpoint Contract | `BIT_EXACT_MATCH` | **PASS** | Same-name 200, unknown 404, conflict 409; deadlock bug resolved |

Metric: **`IMPLEMENTED_USER_ADMIN_CONTRACT_DIFFERENTIAL_PASS_RATE = 30/30`**
Intentional Divergence: **`DIVERGENCE-USER-01`** (Cross-User Rename deadlock bugfix verified via `USER-DIVERGENCE-01`).

---

# Phase 2C.3D: Device Tags REST Reconstruction (`/api/tags`)

## 1. Overview & Forensic Gate Pass

- **Pre-Flight Refinements A–D Completed**:
  - Derived all 11 Users/Admin routes dynamically from [ROUTE_HANDLER_MAP.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/ROUTE_HANDLER_MAP.json) with call VA, handler VA, and symbol validation.
  - Documented `DIVERGENCE-USER-01` in [USER_INTENTIONAL_DIVERGENCES.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/users/USER_INTENTIONAL_DIVERGENCES.json) and verified deadlock bugfix in `USER-DIVERGENCE-01` while preserving the 30/30 denominator.
  - Replaced fixed instruction windows with dynamic function boundary lookup from [FUNCTION_MAP.json](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/FUNCTION_MAP.json).
  - Verified SHA256 password hash mathematical invariant check in `reproduce_user_admin_forensics.py`.
- **Forensic Discovery on `/api/tags`**:
  - Route registration: `/api/tags` registered at call VA `0x76596c` to `main.main.func2` (VA `0x76d200`, size: 704 bytes).
  - Wrapper & Direct Project Callees:
    - `main.main.func2` (`0x76d200`): Injects CORS headers (`Access-Control-Allow-Origin: *`), routes `OPTIONS` immediately (200), routes `POST` to `main.k7fAFNISQp_m`, and routes all other HTTP verbs (`GET`, `PUT`, `DELETE`, `PATCH`, `HEAD`) to `main.bFT5Enmzua`.
    - `main.bFT5Enmzua` (`0x769d40`, size: 1632 bytes): Read handler. Authenticates caller, emits 401 on missing/invalid token, returns `{"tags": [...], "deviceTags": {...}}`.
    - `main.k7fAFNISQp_m` (`0x76a4c0`, size: 5056 bytes): Write handler. Authenticates caller, decodes body into `types.DeviceTagsConfig`. Admin role (`admin`) performs full state replacement; non-admin (`user`) performs scoped tag merge (in-place update + append) and scoped device assignment mutation filtered by user's assigned devices via `main.pVOasuBli` (`0x73d8a0`). Persists via `main.rCajRnfJZ` (`0x737da0`).
    - `main.rCajRnfJZ` (`0x737da0`, size: 608 bytes): Direct `os.WriteFile` with `O_WRONLY|O_CREATE|O_TRUNC` (`0x241`) and mode `0644` (`0x1a4`). **NO atomic `.tmp` rename**.
    - `main.w3H7BXxDC` (`0x737880`, size: 928 bytes): Reads `device_tags.json` on startup, falls back to `{"tags": [], "deviceTags": {}}` and logs `[Tags] Initialized device_tags.json with empty list`.
- **Candidate Operations Formally Evaluated**:
  - Evaluated 6 candidate operations: all 6 confirmed on `/api/tags` (`CONFIRMED_OPERATION`).
  - Probed 7 discrete sub-routes (`/api/tags/add`, `/api/tags/delete`, `/api/tags/update`, `/api/tags/assign`, `/api/tags/remove`, `GET /api/tag`, `POST /api/tag`): all confirmed `NOT_PRESENT` (404 Not Found).
- **Type Descriptors Recovered from Binary ELF**:
  - `Tag`: structType descriptor at `0x7e25a0` (48 bytes, 3 fields: `id`, `name`, `color`).
  - `DeviceTagsConfig`: structType descriptor at `0x7d6f80` (32 bytes, 2 fields: `tags`, `deviceTags`).

## 2. Differential Test Results Matrix (20/20 PASS)

| Test ID | Test Name | Classification | Result | Notes |
|---|---|---|---|---|
| `TAG-HTTP-01` | Baseline List Tags & Device Mappings | `BIT_EXACT_MATCH` | **PASS** | 200 OK, `{"tags":[],"deviceTags":{}}` matching original |
| `TAG-HTTP-02` | Missing Token Rejection on GET | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized with exact body `Unauthorized\n` |
| `TAG-HTTP-03` | Invalid Token Rejection on GET | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized with exact body `Unauthorized\n` |
| `TAG-HTTP-04` | Missing Token Rejection on POST | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized with exact body `Unauthorized\n` |
| `TAG-HTTP-05` | Invalid Token Rejection on POST | `BIT_EXACT_MATCH` | **PASS** | 401 Unauthorized with exact body `Unauthorized\n` |
| `TAG-HTTP-06` | Normal User GET Allowed | `BIT_EXACT_MATCH` | **PASS** | Normal authenticated user can read tags configuration |
| `TAG-HTTP-07` | Admin Full State Update & Persistence | `BIT_EXACT_MATCH` | **PASS** | Full replacement of tags list and device mappings, 200 `{"status":"success"}\n` |
| `TAG-HTTP-08` | Non-Admin Scoped Device Mutation | `BIT_EXACT_MATCH` | **PASS** | Non-admin can only mutate assigned devices; unassigned ignored |
| `TAG-HTTP-09` | Non-Admin Tag Append Merge | `STRUCTURAL_EXACT_MATCH` | **PASS** | New tags appended without destroying existing tag list |
| `TAG-HTTP-10` | Non-Admin In-Place Tag Update | `STRUCTURAL_EXACT_MATCH` | **PASS** | Existing tags matching ID updated in-place |
| `TAG-HTTP-11` | Empty Body Rejection on POST | `BIT_EXACT_MATCH` | **PASS** | 400 Bad Request with exact body `Invalid JSON\n` |
| `TAG-HTTP-12` | Invalid JSON Syntax Rejection on POST | `BIT_EXACT_MATCH` | **PASS** | 400 Bad Request with exact body `Invalid JSON\n` |
| `TAG-HTTP-13` | Empty JSON Object Acceptance | `BIT_EXACT_MATCH` | **PASS** | `{}` accepted, returns 200 `{"status":"success"}\n` |
| `TAG-HTTP-14` | Non-POST Verbs Routed to GET | `BIT_EXACT_MATCH` | **PASS** | `PUT`, `DELETE`, `PATCH` routed to GET handler |
| `TAG-HTTP-15` | HEAD Method Behavior | `BIT_EXACT_MATCH` | **PASS** | 200 OK with 0 body bytes and Content-Type: application/json |
| `TAG-HTTP-16` | OPTIONS CORS Preflight | `BIT_EXACT_MATCH` | **PASS** | 200 OK with Access-Control-Allow-Origin: * and methods |
| `TAG-HTTP-17` | No-Auth Mode Bypass | `BIT_EXACT_MATCH` | **PASS** | No-auth server mode bypasses authentication on `/api/tags` |
| `TAG-HTTP-18` | Persistence Formatting & Direct Write | `BIT_EXACT_MATCH` | **PASS** | Direct `os.WriteFile`, mode 0644, 2-space indentation |
| `TAG-HTTP-19` | Candidate Sub-Routes NOT_PRESENT (404) | `BIT_EXACT_MATCH` | **PASS** | All 7 probed sub-routes confirm 404 NOT_PRESENT |
| `TAG-HTTP-20` | Cross-Contract Isolation With /devices | `BIT_EXACT_MATCH` | **PASS** | Tags operations do not mutate device registry or online status |

Metric: **`IMPLEMENTED_TAG_CONTRACT_DIFFERENTIAL_PASS_RATE = 20/20`**

## 3. Master Verification Audit

- `python tools/verify_phase2.py`: **`OVERALL AUDIT VERDICT: PASS`** across all 11 sections.
- Reconstructed function provenance: 94 functions audited, 0 missing headers, 0 missing metadata fields.



