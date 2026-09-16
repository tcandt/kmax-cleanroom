# Report 15: Phase 2C.3C Users & Admin REST Differential Verification

## 1. Executive Summary

The Phase 2C.3C Users & Admin REST differential test suite executed **30 automated differential test cases** directly comparing the canonical `webrtc-signaling.exe` original binary against the cleanroom reconstructed HTTP server.

- **Total Test Cases Executed**: 30
- **Passed Cases**: 30
- **Failed Cases**: 0
- **Metric**: **`IMPLEMENTED_USER_ADMIN_CONTRACT_DIFFERENTIAL_PASS_RATE = 30/30`**
- **Cleanroom Provenance**: 88/88 functions audited with complete metadata (41 RECONSTRUCTED_FROM_BINARY, 31 GENERATED_ADAPTER, 13 GENERATED_TEST_INTERFACE, 2 GENERATED_BUILD_FUNCTION, 1 RECONSTRUCTED_FROM_BEHAVIOR).
- **Scope Boundary Compliance**: STRICT PASS (0 Tags, 0 Shares, 0 WebSocket signaling, 0 WebRTC, 0 agent protocol).

---

## 2. Test Case Results Matrix

| Test ID | Test Name | Classification | Result | Parity & Wire Semantics Description |
|---|---|---|---|---|
| `USER-HTTP-01` | List Users Baseline | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both return 200 OK, application/json, matching array length and user ordering. |
| `USER-HTTP-02` | Populated List Schema & Key Omissions | `BIT_EXACT_MATCH` | **PASS** | 12-field projection; password and salt strictly omitted; active_devices empty array. |
| `USER-HTTP-03` | Normal User Admin Route Rejection (403) | `BIT_EXACT_MATCH` | **PASS** | Both emit 403 Forbidden with exact body `Forbidden\n`. |
| `USER-HTTP-04` | Missing Token Rejection (401) | `BIT_EXACT_MATCH` | **PASS** | Both emit 401 Unauthorized with exact body `Unauthorized\n`. |
| `USER-HTTP-05` | Invalid Token Rejection (401) | `BIT_EXACT_MATCH` | **PASS** | Both emit 401 Unauthorized with exact body `Unauthorized\n`. |
| `USER-HTTP-06` | Create Valid User & Disk Persistence | `BIT_EXACT_MATCH` | **PASS** | Both return 200 OK `{"status":"success"}\n`, generate 32-char hex salt, and persist SHA256. |
| `USER-HTTP-07` | Duplicate User Conflict (409) | `BIT_EXACT_MATCH` | **PASS** | Both emit 409 Conflict with exact body `Username already exists\n`. |
| `USER-HTTP-08` | Missing Fields on Create (400) | `BIT_EXACT_MATCH` | **PASS** | Both emit 400 Bad Request with exact body `Username and password are required\n`. |
| `USER-HTTP-09` | Update User Note | `BIT_EXACT_MATCH` | **PASS** | Both return 200 OK `{"status":"success"}\n` and persist updated note to disk. |
| `USER-HTTP-10` | Assign Devices to User | `BIT_EXACT_MATCH` | **PASS** | Both return 200 OK `{"status":"success"}\n` and update assigned_devices array. |
| `USER-HTTP-11` | Update User Permissions | `BIT_EXACT_MATCH` | **PASS** | Both return 200 OK with `{"code":0,"data":{...},"msg":"success"}\n` wrapping updated fields. |
| `USER-HTTP-12` | Update User Expiry | `BIT_EXACT_MATCH` | **PASS** | Both persist RFC3339 formatted expiration timestamp to storage. |
| `USER-HTTP-13` | Reset User Password | `BIT_EXACT_MATCH` | **PASS** | Both generate fresh random salt, re-hash password, and return 200 OK `{"status":"success"}\n`. |
| `USER-HTTP-14` | Login After Password Mutation | `BIT_EXACT_MATCH` | **PASS** | Old password rejected with 401; new password succeeds with 200 OK and issues valid session. |
| `USER-HTTP-15` | Delete User & Mutation | `BIT_EXACT_MATCH` | **PASS** | Both return 200 OK `{"status":"success"}\n` and delete user record from `users.json`. |
| `USER-HTTP-16` | Delete Nonexistent User (404) | `BIT_EXACT_MATCH` | **PASS** | Both emit 404 Not Found with exact body `User not found\n`. |
| `USER-HTTP-17` | Session Retained in Memory Post-Deletion | `STRUCTURAL_EXACT_MATCH` | **PASS** | Disassembly jump 0x73b459 verified: active in-memory session remains valid on `/api/me`. |
| `USER-HTTP-18` | No-Auth Mode Bypass on Admin Endpoints | `STRUCTURAL_EXACT_MATCH` | **PASS** | When `-no-auth` active, admin endpoints serve requests unauthenticated without token. |
| `USER-HTTP-19` | HEAD Method Behavior on List Users | `BIT_EXACT_MATCH` | **PASS** | Both return 200 OK with Content-Type: application/json and 0 body bytes. |
| `USER-HTTP-20` | OPTIONS and CORS Headers | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit 200 OK with `Access-Control-Allow-Origin: *` and preflight methods. |
| `USER-HTTP-21` | Persistence File Mode & JSON Contract | `BIT_EXACT_MATCH` | **PASS** | Both persist atomic JSON format to disk with consistent key serialization. |
| `USER-HTTP-22` | Dynamic Reflection on /api/me | `BIT_EXACT_MATCH` | **PASS** | Assigning devices dynamically updates `/api/me` without requiring session re-login. |
| `USER-HTTP-23` | Cannot Delete Self Guard (403) | `BIT_EXACT_MATCH` | **PASS** | Both emit 403 Forbidden with exact body `Cannot delete yourself\n`. |
| `USER-HTTP-24` | Update Note Unknown User (404) | `BIT_EXACT_MATCH` | **PASS** | Both emit 404 Not Found with exact body `User not found\n`. |
| `USER-HTTP-25` | Reset Password Unknown User (404) | `BIT_EXACT_MATCH` | **PASS** | Both emit 404 Not Found with exact body `User not found\n`. |
| `USER-HTTP-26` | Assign Devices Unknown User (404) | `BIT_EXACT_MATCH` | **PASS** | Both emit 404 Not Found with exact body `User not found\n`. |
| `USER-HTTP-27` | User Personal AI Config Update | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both accept POST /api/user/ai-config, return 200 OK, and persist 4-field AIConfig. |
| `USER-HTTP-28` | Public Registration Disabled (403) | `BIT_EXACT_MATCH` | **PASS** | Both return 403 with exact Chinese/English error message JSON object. |
| `USER-HTTP-29` | Kick User Endpoint Contract | `BIT_EXACT_MATCH` | **PASS** | Both accept POST /api/admin/users/kick, return 200 OK, and reject empty username with 400. |
| `USER-HTTP-30` | Rename User Endpoint Contract | `BIT_EXACT_MATCH` | **PASS** | Same-name returns 200; unknown returns 404; existing returns 409; binary deadlock resolved. |

---

## 3. Discovered Behavioral Highlights & Machine Analysis

1. **ServeMux Routing & Non-Gating Verbs**:
   The original binary registers routes on standard Go `http.ServeMux`. For endpoints that read a JSON body directly without an explicit `if r.Method != "POST"` check, non-POST requests with empty bodies return `400 Invalid JSON\n` (or `400 Username and password are required\n`), while OPTIONS returns `200 OK` with CORS headers.

2. **Self-Deletion Guard**:
   In `HandleAdminDeleteUser` (`main._Wcin_o` at 0x745ba0), the server explicitly checks if the target username equals the caller's authenticated username. If so, it aborts with `403 Cannot delete yourself\n`. In `-no-auth` mode, this guard is bypassed.

3. **In-Memory Session Persistence Post User Deletion**:
   In `ValidateSession` / `main.lYKp_Iuf` (VA 0x73b3e1 to 0x73b459), when a session token is active in memory, deleting the user from persistent `users.json` does not revoke the token; the binary returns `(sess.Username, nil)` without error, allowing `/api/me` to project a fallback profile.

4. **Cross-User Rename Deadlock Bug in Original Binary**:
   In `main.sGuPXW2D` (VA 0x740f40), when renaming across distinct usernames, the handler acquires `usersLock.Lock()` (write lock at 0x741630) and calls `saveUsers()` (0x737500), which immediately attempts to acquire `usersLock.RLock()` (read lock at 0x73752a). This causes the original binary to permanently hang on cross-user renames. The cleanroom implementation in `pkg/storage/users_store.go` resolves this cleanly while matching the exact REST API contract.

5. **Cross-Contract Dynamic Binding**:
   Mutating assigned devices via `/api/admin/assign` immediately reflects in the live session's `/api/me` profile and dynamically updates the device visibility filtering in `/devices` without requiring the user to re-authenticate.

---

## 4. Reproducibility & Regression Verification

- **Regenerated In Isolated Directory**: `tools/forensics/reproduce_user_admin_forensics.py` executed against original binary into `scratch/reproduce_user_admin_forensics/<run-id>`:
  - `USER_TYPE_DESCRIPTOR_REPRODUCIBLE`: **PASS** (13 fields on User struct 0x80a0c0, 4 fields on AIConfig 0x7ed060)
  - `USER_STATIC_BINARY_EVIDENCE_REPRODUCIBLE`: **PASS** (11 confirmed routes)
  - `USER_FUNCTION_SLICE_REPRODUCIBLE`: **PASS** (11 Capstone disassembly slices)
  - `USER_DYNAMIC_ORACLE_CONTRACT_REPRODUCIBLE`: **PASS** (All 7 dynamic contract files match committed evidence)
- **Full Regression Suite**:
  - Persistence differential: **8/8 PASS**
  - Auth core differential: **12/12 PASS**
  - Auth HTTP differential: **18/18 PASS**
  - Device REST differential: **28/28 PASS**
  - Users/Admin differential: **30/30 PASS**
  - Unit tests (`go test ./...`): **PASS**
  - Provenance audit (`verify_reconstructed_provenance.py`): **88/88 functions PASS**
  - Master verifier (`verify_phase2.py`): **PASS**

---

## 5. Addendum: Documented Intentional Bugfix Divergences

| Divergence ID | Route | Classification | Original Behavior | Cleanroom Reconstructed Behavior | Target Verification Test |
|---|---|---|---|---|---|
| `DIVERGENCE-USER-01` | `/api/admin/users/rename` | `INTENTIONAL_BUGFIX_DIVERGENCE` | Deadlock / Permanent Hang (recursive RWMutex acquisition: write lock at `0x741630` in `main.sGuPXW2D`, read lock at `0x73752a` in `saveUsers`) | Clean lock handling without self-deadlock, HTTP 200 `{"status":"success"}\n`, persists to `users.json` | `USER-DIVERGENCE-01` (bounded differential timeout) |

> [!NOTE]
> As governed by cleanroom protocol, `USER-DIVERGENCE-01` is classified as a bounded divergence test confirming that the original server hangs until timeout while the reconstructed server completes successfully with exact schema and persistence parity. The primary differential pass rate denominator remains **30/30** for standard wire parity test cases.
