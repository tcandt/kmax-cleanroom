# Phase 2C.2 Differential Parity Report: Authentication & Session Management

**Execution Timestamp**: `2026-09-15 11:28:41 UTC`  
**Original Binary**: `webrtc-signaling.exe` (Windows AMD64) / `webrtc-signaling` (Linux AMD64)  
**Reconstructed Core**: `cmd/auth-tool` (`serve-stdio` stateful test harness)  
**Status**: **ALL 12 TESTS PASS (100% PARITY)**

---

## 1. Executive Summary

Phase 2C.2 Differential Verification executed **12 side-by-side test cases** comparing the original distributed binary oracle against the reconstructed clean-room authentication core and session manager.

The test harness operated strictly through a **long-lived stateful stdio process** (`cmd/auth-tool/main.go`), ensuring in-memory session semantics were verified without disk persistence shortcuts. Expected HTTP statuses and error messages were dynamically derived from the original binary oracle.

---

## 2. Differential Test Matrix

| Test ID | Test Name | Equivalence Classification | Status | Summary & Parity Evidence |
|---|---|---|---|---|
| `TC-AUTH-01` | **Valid Password & Login Response Schema** | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit 200 OK equivalent with assigned_devices, role, token, username |
| `TC-AUTH-02` | **Invalid Password Rejection** | `SEMANTIC_MATCH` | **PASS** | Both reject invalid credentials with exact diagnostic string |
| `TC-AUTH-03` | **Unknown Username Rejection** | `SEMANTIC_MATCH` | **PASS** | Both reject unknown username with identical diagnostic error |
| `TC-AUTH-04` | **User Account with Past ExpiresAt Rejection** | `SEMANTIC_MATCH` | **PASS** | Both reject expired account with exact Chinese diagnostic string |
| `TC-AUTH-05` | **User Account with Future ExpiresAt Success** | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both allow login for accounts with valid future expiration |
| `TC-AUTH-06` | **Token Structural & Entropy Properties** | `PROPERTY_MATCH` | **PASS** | Both generate 64-char lowercase hex tokens from 32 bytes entropy with zero JWT dots |
| `TC-AUTH-07` | **Valid Session Lookup & Token Validation** | `SEMANTIC_MATCH` | **PASS** | Both validate active session token and resolve to correct account |
| `TC-AUTH-08` | **Invalid Token Rejection** | `SEMANTIC_MATCH` | **PASS** | Both reject non-existent token with Unauthorized |
| `TC-AUTH-09` | **Logout & Token Revocation** | `SEMANTIC_MATCH` | **PASS** | Both successfully revoke session token on logout, rejecting subsequent requests |
| `TC-AUTH-10` | **Multiple Concurrent Sessions on Same Account** | `SEMANTIC_MATCH` | **PASS** | Both support simultaneous independent sessions per user account |
| `TC-AUTH-11` | **Process Restart Memory-Only Invalidation** | `STATIC_AND_DYNAMIC_PARITY` | **PASS** | Both discard all sessions upon process restart (SESSION_MEMORY_ONLY) |
| `TC-AUTH-12` | **Session TTL Expiration (24h) via Mock Clock** | `STATIC_AND_RECON_RUNTIME_PARITY` | **PASS** | Reconstructed deterministic mock clock confirms 24h TTL lazy eviction |

---

## 3. Forensic Ground Truth Invariants Established

1. **Password Verification Parity**:
   - Both original and reconstructed compute hex_lower(SHA256(password + salt)).
   - Reconstructed reuses verified `pkg/storage.HashPassword` primitive with zero duplication.
   - Diagnostic errors match bit-for-bit: "Invalid username or password", "Username and password are required", and "账号已到期，请联系管理员延时".

2. **Session Memory-Only Invariant**:
   - TC-AUTH-11 proved that restarting either process immediately invalidates all active session tokens (`SESSION_MEMORY_ONLY`).
   - Zero session artifacts are written to filesystem.

3. **Session TTL vs Account Expiry Separation**:
   - TC-AUTH-04 and TC-AUTH-12 independently verified that account expiration (`User.ExpiresAt`) and session expiration (`Session.ExpiresAt`, 24h TTL) operate as distinct mechanisms.
   - Session TTL eviction operates lazily on lookup (`main.lYKp_Iuf` parity).

4. **Multi-Session Concurrency**:
   - TC-AUTH-10 proved that logging into the same account multiple times issues independent tokens. Revoking token A via logout leaves token B fully active and valid.
