# Report 09 — Phase 2C.3 Auth HTTP Forensics & Contract Recovery

**Document Version**: 1.0.0  
**Target System**: `webrtc-signaling` (Linux AMD64 / Windows AMD64)  
**Execution Context**: Clean-Room Reconstruction Phase 2C.3 (Authentication Slice)  
**Forensic Gate Verdict**: **PASS — 13/13 INVARIANTS RESOLVED**

---

## 1. Executive Summary

In accordance with the Phase 2C.3 mandate, before writing any reconstructed HTTP server or handler source code, comprehensive dynamic probing against the original live binary oracle and disassembly decompilation were performed to establish the exact runtime contracts for the four authentication endpoints:
- `POST /api/login`
- `ALL  /api/logout`
- `ALL  /api/auth-status`
- `ALL  /api/me`

All contracts have been captured in machine-readable structured artifacts:
- [`AUTH_TOKEN_SOURCE_MATRIX.json`](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_TOKEN_SOURCE_MATRIX.json) & [`.md`](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_TOKEN_SOURCE_MATRIX.md)
- [`AUTH_ROUTE_METHOD_MATRIX.json`](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_ROUTE_METHOD_MATRIX.json) & [`.md`](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_ROUTE_METHOD_MATRIX.md)
- [`LOGIN_REQUEST_CONTRACT.json`](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/LOGIN_REQUEST_CONTRACT.json)
- [`AUTH_HTTP_RESPONSE_CONTRACT.json`](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_HTTP_RESPONSE_CONTRACT.json)
- [`AUTH_HTTP_FUNCTION_SLICES.json`](file:///d:/KMAX-CLEANROOM/evidence/go_signaling/http/AUTH_HTTP_FUNCTION_SLICES.json)

---

## 2. HTTP Forensic Gate Resolution Matrix

| Gate Requirement | Status | Ground Truth Recovery Finding | Primary Evidence Artifact |
|---|---|---|---|
| **1. Token Precedence** | **RESOLVED** | `HEADER_FIRST_STRICT_OVER_QUERY`: Header evaluated first; if present, query token is never consulted | `AUTH_TOKEN_SOURCE_MATRIX.json` |
| **2. Query Fallback** | **RESOLVED** | Fallback to `req.URL.Query().Get("token")` occurs ONLY when Authorization header is absent, empty, or token segment is empty | `AUTH_TOKEN_SOURCE_MATRIX.json` (Cases 2 & 10) |
| **3. Method Matrix** | **RESOLVED** | `/api/login` strictly enforces POST (405 otherwise); `/api/logout`, `/api/auth-status`, `/api/me` do NOT restrict HTTP verbs | `AUTH_ROUTE_METHOD_MATRIX.json` |
| **4. OPTIONS Preflight** | **RESOLVED** | Returns 200 OK with empty body and CORS headers across all four endpoints | `AUTH_ROUTE_METHOD_MATRIX.json` |
| **5. HEAD Semantics** | **RESOLVED** | 405 on `/api/login`; 200 OK bodyless on `/api/logout`, `/api/auth-status`, and authenticated `/api/me` | `AUTH_ROUTE_METHOD_MATRIX.json` |
| **6. Login Request Decode** | **RESOLVED** | Standard Go `json.Decoder`; rejects malformed JSON (400 'Invalid JSON'); requires non-empty username/password (400 'Username and password are required') | `LOGIN_REQUEST_CONTRACT.json` |
| **7. Exact Response Schemas** | **RESOLVED** | Exact byte-level status codes, content-types, JSON keys, and trailing newline (`\n`) for all 15 execution branches | `AUTH_HTTP_RESPONSE_CONTRACT.json` |
| **8. Logout Idempotency** | **RESOLVED** | Idempotent: returns 200 `{"status":"success"}\n` even on invalid, already revoked, or missing tokens | `AUTH_HTTP_RESPONSE_CONTRACT.json` (Branches 6-9) |
| **9. Auth-Status Schema** | **RESOLVED** | `{"noAuth":false}\n` emitted with `Content-Type: application/json` | `AUTH_HTTP_RESPONSE_CONTRACT.json` |
| **10. /api/me Schema** | **RESOLVED** | Emits 10 user fields (`ai_config`, `assigned_devices`, `expires_at`, `forbid_*`, `role`, `settings`, `username`) | `AUTH_HTTP_RESPONSE_CONTRACT.json` |
| **11. No-Auth Mode** | **RESOLVED** | `NO_AUTH` / `no-auth` environment variable bypasses lookup and authenticates as `admin` directly | Disassembly Linux `0x73b09d`, Windows `0x14034427d` |
| **12. CORS Headers** | **RESOLVED** | `Access-Control-Allow-Origin: *`, `Allow-Headers: Content-Type, Authorization`, `Allow-Methods: POST, OPTIONS` or `GET, OPTIONS` | `AUTH_ROUTE_METHOD_MATRIX.json` |
| **13. Binary Function Slices**| **RESOLVED** | VA ranges separated into 6 HTTP behavior categories with explicit non-overlapping linkage to Phase 2C.2 core | `AUTH_HTTP_FUNCTION_SLICES.json` |

---

## 3. Disassembly & Static Corroboration

### 3.1 Token Extractor (`AUTH_TOKEN_LOOKUP`: Linux `0x73b080`, Windows `0x140344260`)

```go
// Synthesized from disassembled machine instructions:
func ExtractToken(r *http.Request) string {
    // 1. Check Authorization header
    authHeader := r.Header.Get("Authorization")
    token := ""
    if authHeader != "" {
        parts := strings.Split(authHeader, " ")
        if len(parts) == 2 && strings.ToLower(parts[0]) == "bearer" {
            token = parts[1]
        } else {
            token = authHeader
        }
    }
    // 2. Query fallback only if header yielded empty token
    if token == "" {
        token = r.URL.Query().Get("token")
    }
    return token
}
```

### 3.2 CORS Helper

```go
func SetCORS(w http.ResponseWriter, methods string) {
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Methods", methods)
    w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
}
```

---

## 4. Conclusion & Forensic Gate Clearance

With all 13 forensic requirements completely resolved by live binary dynamic evidence and corroborated by assembly instructions:
- **FORENSIC GATE VERDICT: PASS**
- **AUTHORIZATION**: Proceed to Phase 2C.3G (Reconstruct Shared HTTP Layer & Auth Handlers under `pkg/httpapi/`).
