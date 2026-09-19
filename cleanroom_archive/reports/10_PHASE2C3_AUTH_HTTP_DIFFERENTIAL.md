# Report 10 — Phase 2C.3 Auth HTTP Differential Verification

**Target**: `webrtc-signaling` (Windows AMD64 & Linux AMD64)  
**Reconstructed Target**: `pkg/httpapi` (Standard Library `net/http`)  
**Differential Harness**: [`tests/differential/http/test_auth_http_diff.py`](file:///d:/KMAX-CLEANROOM/tests/differential/http/test_auth_http_diff.py)  
**Source Evidence**: [`evidence/go_signaling/http/AUTH_HTTP_DIFFERENTIAL_RESULTS.json`](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_HTTP_DIFFERENTIAL_RESULTS.json)  
**Verification Verdict**: **PASS — 18/18 TEST CASES PASSED**

---

## 1. Executive Summary

Phase 2C.3 reconstructed the HTTP endpoints and middleware for the four core authentication routes:
- `POST /api/login`
- `ALL  /api/logout`
- `ALL  /api/auth-status`
- `ALL  /api/me`

To ensure exact behavioral, structural, and wire-level parity against the original binary oracle without touching premature scope (WebRTC, WebSocket signaling, or administrative CRUD endpoints), an 18-case differential test suite was executed side-by-side using isolated network ports and identical data fixtures.

---

## 2. Test Execution Matrix

| Test ID | Test Name | Classification | Result | Parity Verification |
|---|---|---|---|---|
| `HTTP-01` | Login Success Schema & Token Issuance | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit 200 OK, application/json, matching 4-key JSON schema and 64-char lowercase hex token |
| `HTTP-02` | Invalid Password Rejection | `BIT_EXACT_MATCH` | **PASS** | Both emit 401 Unauthorized with exact byte string 'Invalid username or password\n' |
| `HTTP-03` | Missing Credentials Rejection | `BIT_EXACT_MATCH` | **PASS** | Both emit 400 Bad Request with exact byte string 'Username and password are required\n' |
| `HTTP-04` | Expired Account Rejection | `BIT_EXACT_MATCH` | **PASS** | Both emit 403 Forbidden with exact UTF-8 expiration notice string |
| `HTTP-05` | Malformed JSON Rejection | `BIT_EXACT_MATCH` | **PASS** | Both emit 400 Bad Request with exact byte string 'Invalid JSON\n' |
| `HTTP-06` | Valid Token Logout & Invalidation | `BIT_EXACT_MATCH` | **PASS** | Both emit 200 OK with {'status':'success'}\n and invalidate session immediately |
| `HTTP-07` | Logout Idempotency | `BIT_EXACT_MATCH` | **PASS** | Both emit 200 OK with {'status':'success'}\n on repeated/revoked logout |
| `HTTP-08` | Auth-Status Unauthenticated | `BIT_EXACT_MATCH` | **PASS** | Both emit 200 OK with exact body '{"noAuth":false}\n' |
| `HTTP-09` | Auth-Status Authenticated | `BIT_EXACT_MATCH` | **PASS** | Both emit 200 OK with exact body '{"noAuth":false}\n' |
| `HTTP-10` | User Profile Valid Canonical Bearer | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit 200 OK with identical 10-field UserProfile JSON schema and field nullability |
| `HTTP-11` | Case-Insensitive Bearer Header Parsing | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both accept bearer, BEARER, and bEaReR prefixes identically via case-insensitive scheme parsing |
| `HTTP-12` | Query Token Fallback (?token=) | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both fall back to query ?token=<token> when Authorization header is absent |
| `HTTP-13` | Header Strict Precedence Over Query | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both prioritize Authorization header strictly; invalid Bearer fails without query fallback |
| `HTTP-14` | Missing Token Rejection | `BIT_EXACT_MATCH` | **PASS** | Both emit 401 Unauthorized with exact byte string 'Unauthorized\n' |
| `HTTP-15` | Invalid Token Rejection | `BIT_EXACT_MATCH` | **PASS** | Both emit 401 Unauthorized with exact byte string 'Unauthorized\n' |
| `HTTP-16` | OPTIONS Preflight Parity | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit 200 OK with empty body and identical Access-Control-* headers across all 4 routes |
| `HTTP-17` | HEAD Request Semantics | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both handle HEAD requests with zero body bytes and matching status codes (405 login, 200 others) |
| `HTTP-18` | Content-Type & Body Wire Formatting | `BIT_EXACT_MATCH` | **PASS** | Both adhere to identical wire formatting: trailing newline \n on all responses, correct Content-Type |

---

## 3. Key Behavioral Parity Findings

1. **Token Precedence & Fallback Parity (HTTP-11, HTTP-12, HTTP-13)**:
   - Case-insensitive Bearer prefix handling (`Bearer`, `bearer`, `BEARER`, `bEaReR`) authenticated identically.
   - Fallback to query parameter `?token=` succeeded when Authorization header was absent.
   - Header strict precedence confirmed: an invalid Bearer header fails with 401 without consulting the query parameter.
2. **Method Enforcement (HTTP-01, HTTP-16, HTTP-17)**:
   - `/api/login` strictly enforces POST (rejects GET, PUT, PATCH, DELETE, HEAD with 405 Method Not Allowed).
   - `/api/logout`, `/api/auth-status`, and `/api/me` accept all HTTP verbs identically.
3. **Wire Formatting (HTTP-18)**:
   - Every single response ends with trailing newline (`\n`).
   - JSON endpoints emit `Content-Type: application/json`.
   - Error responses emit `Content-Type: text/plain; charset=utf-8`.
4. **Idempotent Logout (HTTP-06, HTTP-07)**:
   - Logout emits `{"status":"success"}\n` unconditionally on active, already-revoked, and invalid tokens.

---

## 4. Exit Gate Assessment

- [x] Query-token fallback dynamically confirmed (HTTP-12)
- [x] Header/query precedence dynamically confirmed (HTTP-13)
- [x] Method contracts recovered (HTTP-01, HTTP-16, HTTP-17)
- [x] Request JSON decode behavior recovered (HTTP-01, HTTP-03, HTTP-05)
- [x] Response schemas recovered (HTTP-01, HTTP-10)
- [x] Status codes recovered (HTTP-01..18)
- [x] CORS / OPTIONS behavior recovered (HTTP-16)
- [x] Reconstructed four auth routes compile and pass
- [x] HTTP differential suite 18/18 PASS
