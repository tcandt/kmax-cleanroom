# Phase 2C.3C Forensic Report: Users & Admin REST Reconstruction

**Document ID**: `REPORT-14-PHASE2C3C-USER-ADMIN-FORENSICS`  
**Target Binary**: `webrtc-signaling` (Linux AMD64 SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`, Windows AMD64 SHA256: `374a9d784a32cfb377b5d15a97aa3c74eaec0234a9844f2c258d4a9bf95df874`)  
**Scope**: Users & Admin REST Family Only. Excludes Tags, Shares, WebSockets (`/register_agent`, `/connect_client`), WebRTC.  
**Forensic Gate Status**: **PASS / APPROVED FOR SOURCE RECONSTRUCTION**

---

## 1. Pre-Flight A: Device Reproducibility Fix

The device forensic reproducibility tool `tools/forensics/reproduce_device_forensics.py` and generator `tools/forensics/generate_device_forensics.py` were refactored in pre-flight:
1. `generate_device_forensics.py` now accepts an explicit `output_dir` parameter.
2. `reproduce_device_forensics.py` executes `generate_evidence()` into an isolated scratch run directory (`scratch/reproduce_device_forensics/<run_id>`).
3. Verification strictly validates deterministic artifacts and normalizes only dynamic ephemeral fields (session tokens, WebSocket random keys, ephemeral ports, and ISO timestamps).
4. Evidence status is reported cleanly under 4 distinct, verified categories:
   - `DEVICE_TYPE_DESCRIPTOR_REPRODUCIBLE: PASS`
   - `DEVICE_STATIC_BINARY_EVIDENCE_REPRODUCIBLE: PASS`
   - `DEVICE_FUNCTION_SLICE_REPRODUCIBLE: PASS`
   - `DEVICE_DYNAMIC_ORACLE_CONTRACT_REPRODUCIBLE: PASS`
Device parity is closed (28/28 differential tests pass).

---

## 2. Discovered Route Family

All 11 user/admin routes were discovered directly from `ROUTE_HANDLER_MAP.json`, binary strings, and Capstone-disassembled registration calls:

| Route | Registration Call VA | Handler Symbol | Handler VA | Allowed Verbs | Auth Requirement | Semantic Role |
|---|---|---|---|---|---|---|
| `/api/admin/users` | `0x765a78` | `main.eiuBQux8` | `0x741ec0` | GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS | Admin Token | List all user accounts with status & devices |
| `/api/admin/users/create` | `0x765ac0` | `main.zrTQTiT` | `0x744140` | POST, OPTIONS | Admin Token | Create user account with credentials & role |
| `/api/admin/users/delete` | `0x765ad8` | `main._Wcin_o` | `0x745ba0` | POST, OPTIONS | Admin Token | Delete user account (cannot delete self) |
| `/api/admin/users/update` | `0x765b08` | `main.m3nYlgst` | `0x744c20` | POST, OPTIONS | Admin Token | Update permissions, expiry & media flags |
| `/api/admin/users/update_note` | `0x765af0` | `main.daDbGP` | `0x7464e0` | POST, OPTIONS | Admin Token | Update user administrative note |
| `/api/admin/users/reset_password` | `0x765b20` | `main.rmHttgOpxTKh` | `0x746e80` | POST, OPTIONS | Admin Token | Reset user password & generate fresh salt |
| `/api/admin/users/rename` | `0x765a90` | `main.sGuPXW2D` | `0x740f40` | POST, OPTIONS | Admin Token | Rename user account (see bug analysis) |
| `/api/admin/users/kick` | `0x765b38` | `main.eIddSiN_g` | `0x747880` | POST, OPTIONS | Admin Token | Terminate active user device connection |
| `/api/admin/assign` | `0x765aa8` | `main.as5uExtX` | `0x7432a0` | POST, OPTIONS | Admin Token | Assign device IDs to user account |
| `/api/register` | `0x765a18` | `main.ajyljXiIN8` | `0x73e7c0` | POST, OPTIONS | None (Disabled by default) | Public registration endpoint (403 when disabled) |
| `/api/user/ai-config` | `0x765a48` | `main.jc6UOob61gVD` | `0x73ffc0` | POST, OPTIONS | Authenticated User | Update user's personal AI configuration |

Evidence committed: `evidence/go_signaling/users/USER_ADMIN_ROUTE_FAMILY.json`.

---

## 3. Route & Method Behavior Matrix

Probing all 7 HTTP verbs (`allow_redirects=False`) against the live original binary revealed crucial routing traits:
1. **`/api/admin/users`**: Does not validate HTTP verb. Returns status 200 and the serialized user array for `GET`, `POST`, `PUT`, `PATCH`, `DELETE`. Returns 200 with empty body for `HEAD`, and 200 with CORS headers for `OPTIONS`.
2. **Mutation Handlers (`create`, `delete`, `update`, `update_note`, `reset_password`, `kick`, `assign`)**: Do not inspect `r.Method` before decoding JSON body. If sent with non-POST verbs without body, `json.NewDecoder(r.Body).Decode` fails with EOF, returning `400 Invalid JSON\n` (or for `update`: `400 Invalid payload\n`). All return 200 on `OPTIONS`.
3. **Strict POST Checkers (`rename`, `ai-config`)**: Explicitly check `r.Method == "POST"`. For any other method (except `OPTIONS`), they immediately return `405 Method not allowed\n`.
4. **Registration (`/api/register`)**: Returns `403 {"error":"Public registration is disabled. Please contact an administrator to create an account."}\n` for all HTTP verbs.

Evidence committed: `evidence/go_signaling/users/USER_ADMIN_ROUTE_METHOD_MATRIX.json`.

---

## 4. Recovered Binary Type Descriptors

Direct parsing of the Linux ELF `.rodata` runtime structType tables produced exact layouts:

### A. Storage Types
- **`main.AaXW78` (User Struct)**: VA `0x80a0c0`, size 152 bytes, 13 fields:
  - `username` (offset 0, string)
  - `password` (offset 16, string)
  - `salt` (offset 32, string)
  - `role` (offset 48, string)
  - `assigned_devices` (offset 64, []string)
  - `note` (offset 88, string)
  - `forbid_bitrate` (offset 104, bool)
  - `forbid_fps` (offset 105, bool)
  - `forbid_resolution` (offset 106, bool)
  - `forbid_audio` (offset 107, bool)
  - `settings,omitempty` (offset 112, map[string]interface{})
  - `expires_at` (offset 120, time.Time)
  - `ai_config,omitempty` (offset 144, *main.C8aP5BseiM)
- **`main.C8aP5BseiM` (AIConfig Struct)**: VA `0x7ed060`, size 64 bytes, 4 fields:
  - `ai_api_url` (offset 0, string)
  - `ai_api_key` (offset 16, string)
  - `ai_model` (offset 32, string)
  - `ai_provider` (offset 48, string)

### B. Request DTOs
- **CreateUserDTO**: VA `0x7f3020`, 72 bytes (`username`, `password`, `role`, `note`, `expire_seconds`)
- **UpdateUserDTO**: VA `0x7fe6c0`, 40 bytes (`username`, `forbid_bitrate`, `forbid_fps`, `forbid_resolution`, `forbid_audio`, `settings`, `expire_seconds`)
- **AssignDevicesDTO**: VA `0x7caba0`, 40 bytes (`username`, `devices`)
- **UpdateNoteDTO**: VA `0x7cac20`, 32 bytes (`username`, `note`)
- **ResetPasswordDTO**: VA `0x7cada0`, 32 bytes (`username`, `password`)
- **KickUserDTO**: VA `0x7cae20`, 32 bytes (`username`, `device_id`)
- **RenameUserDTO**: VA `0x7caf20`, 32 bytes (`old_username`, `new_username`)
- **DeleteUserDTO**: VA `0x7bd600`, 16 bytes (`username`)

### C. Admin User List Item Schema
Generated dynamically as `map[string]interface{}` without exposing sensitive fields:
- Includes: `username`, `role`, `assigned_devices`, `note`, `forbid_bitrate`, `forbid_fps`, `forbid_resolution`, `forbid_audio`, `settings`, `expires_at`, `online`, `active_devices`.
- Excludes: `password`, `salt`.

Evidence committed: `evidence/go_signaling/users/USER_TYPE_EVIDENCE.json`.

---

## 5. Mutation & Action Contracts

### A. List Contract (`/api/admin/users`)
- Returns JSON array of sanitized user maps.
- Sorted alphabetically by username.
- Sensitive fields (`password`, `salt`) are never exposed.
- Status: `200 OK`.

### B. Create User Contract (`/api/admin/users/create`)
- Valid minimal request: `{ "username": "...", "password": "..." }` $\rightarrow$ `200 {"status":"success"}`.
- Default role: `"user"` when `role` is omitted or empty.
- Salt generation: 16 cryptographically random bytes formatted as 32 lowercase hex characters.
- Password hash: `SHA256(password + salt)`.
- Duplicate username: `409 Username already exists\n`.
- Missing username or password: `400 Username and password are required\n`.

### C. Update Note Contract (`/api/admin/users/update_note`)
- Success: `200 {"status":"success"}`.
- Unknown user: `404 User not found\n`.
- Empty username: `400 Username is required\n`.
- Empty or null note: accepted and stored as `""`.

### D. Reset Password Contract (`/api/admin/users/reset_password`)
- Success: `200 {"status":"success"}`.
- Generates a fresh 16-byte hex salt and re-hashes password.
- Immediately enables login with new password; old password fails with 401.
- Active session tokens remain valid in memory until expiry.
- Unknown user: `404 User not found\n`.
- Missing username/password: `400 Username and new password are required\n`.

### E. Assign Devices Contract (`/api/admin/assign`)
- Success: `200 {"status":"success"}`.
- Updates `assigned_devices` slice in `users.json`.
- Unknown user: `404 User not found\n`.
- Empty username: `400 Target username is required\n`.
- Empty or null devices: accepted and stored as empty slice `[]`.

### F. Update Permissions Contract (`/api/admin/users/update`)
- Success: `200 {"code":0,"data":{...},"msg":"success"}`.
- Mutates: `forbid_bitrate`, `forbid_fps`, `forbid_resolution`, `forbid_audio`, `settings`, `expires_at` (calculated from `time.Now().Add(expire_seconds)`).
- Unknown user: `404 User not found\n`.
- Empty username: `400 username is required\n`.

### G. Kick User Contract (`/api/admin/users/kick`)
- Success: `200 {"status":"success"}`.
- Unknown user: `200 {"status":"success"}` (no-op).
- Empty username: `400 Username is required\n`.

### H. Rename User Contract & Binary Bug Analysis (`/api/admin/users/rename`)
- When `old_username == new_username`: returns `200 {"status":"success"}` without saving.
- When `old_username` does not exist: returns `404 User not found\n`.
- When `new_username` already exists: returns `409 Username already exists\n`.
- **CRITICAL FORENSIC DISCOVERY**: In the original binary `main.sGuPXW2D`, when renaming a user across different names, the handler acquires `usersLock.Lock()` (write lock at `0x741630`), updates the map, and then calls `saveUsers()` (`0x737500`), which immediately attempts to acquire `usersLock.RLock()` (read lock at `0x73752a`). In Go, an active write lock prevents any read lock on the same `sync.RWMutex`, causing the original binary to **permanently self-deadlock**.  
In cleanroom reconstruction, this deadlock must be avoided by using consistent lock scoping (e.g. calling an internal un-locked saver or releasing the lock before saving).

### I. Delete User Contract (`/api/admin/users/delete`)
- Success: `200 {"status":"success"}`. Removes user from `users.json`.
- Unknown user: `404 User not found\n`.
- Cannot delete self: `403 Cannot delete yourself\n` (admin token cannot delete its own username).
- Missing username: `400 Username is required\n`.

---

## 6. Expiry & Cross-Contract Semantics

### Expiry Semantics
- Evaluated during authentication at `/api/login`.
- If `expires_at` is non-zero and before `time.Now()`, login fails with:  
  `403 Forbidden` and body `账号已到期，请联系管理员延时\n`.
- Tokens issued prior to expiration remain valid for their normal session TTL.

### Device Assignment Cross-Contract
- The session token binds to the username.
- `/api/me` and `/devices` look up the current user state dynamically from storage upon each request.
- Updating `assigned_devices` via `/api/admin/assign` immediately alters device visibility on `/devices` and `/api/me` for active sessions without requiring re-login.

Evidence committed: `USER_ASSIGNMENT_CROSS_CONTRACT.json`.

---

## 7. Authorization Matrix

All admin endpoints strictly enforce authentication and authorization:
- `VALID_ADMIN`: Access granted (`200 OK` or valid mutation).
- `NORMAL_USER`: `403 Forbidden` (`Forbidden\n`).
- `INVALID_TOKEN`: `401 Unauthorized` (`Unauthorized\n`).
- `MISSING_TOKEN`: `401 Unauthorized` (`Unauthorized\n`).
- `NO_AUTH_SERVER_MODE` (`-no-auth`): Bypasses all token checks; grants full admin access to all routes.

Evidence committed: `evidence/go_signaling/users/USER_ADMIN_AUTH_MATRIX.json`.

---

## 8. Forensic Gate Verification Checklist

- [x] Route family discovered and verified from binary and references (11 routes)
- [x] Route/method matrix complete across 7 HTTP verbs
- [x] Direct Go runtime type descriptors recovered from ELF
- [x] Read/list behavior & response schema verified
- [x] Create contract & password/salt semantics bound to auth core
- [x] Update contracts enumerated independently (`update`, `note`, `password`, `assign`, `kick`, `rename`)
- [x] Delete contract verified (including self-deletion guard)
- [x] Authorization matrix verified across 5 client modes
- [x] Assigned devices cross-contract verified against `/devices`
- [x] Capstone function slices generated
- [x] Self-deadlock bug in original binary's `rename` fully diagnosed

**DECISION**: Forensic gate **PASS**. Proceed to cleanroom source reconstruction.
