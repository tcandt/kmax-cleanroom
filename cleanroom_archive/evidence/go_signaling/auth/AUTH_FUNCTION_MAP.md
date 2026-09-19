# Forensic Authentication & Session Function Map (`AUTH_FUNCTION_MAP`)

**Binary Artifact**: `webrtc-signaling` (Linux AMD64 ELF / Windows AMD64 PE)  
**SHA-256 (Linux ELF)**: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`  
**Classification**: `FORENSIC_EVIDENCE_SPECIFICATION`  
**Status**: COMPLETE (12 Core Auth & Session Subsystem Functions Mapped)

---

## 1. Summary of Authentication & Session Functions

| Binary Symbol | Virtual Address (VA) | File Offset | Size | Semantic Role | Classification | Confidence |
|---|---|---|---|---|---|---|
| `main.ltOjwqsMl5q8` | `0x73dd00` | `0x33dd00` | 2,752 B | `AUTH_LOGIN_HANDLER` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.lYKp_Iuf` | `0x73b080` | `0x33b080` | 1,120 B | `AUTH_TOKEN_LOOKUP_AND_VALIDATE` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.bjWkHiittd` | `0x7409a0` | `0x3409a0` | 1,440 B | `AUTH_LOGOUT_AND_TOKEN_REVOCATION` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.bwvBd1LWVr` | `0x73ec40` | `0x33ec40` | 1,216 B | `AUTH_STATUS_HANDLER` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.gJ0OHScnGnWZ` | `0x73f100` | `0x33f100` | 2,816 B | `USER_PROFILE_HANDLER` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.biG96MFIwa` | `0x739060` | `0x339060` | 480 B | `PASSWORD_HASH_VERIFIER` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.vT6rYK_v` | `0x739320` | `0x339320` | 288 B | `SESSION_CREATOR_AND_INSERTER` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.d2SHxnu` | `0x739240` | `0x339240` | 224 B | `SESSION_TOKEN_GENERATOR` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.cFpPBbFet` | `0x73a500` | `0x33a500` | 128 B | `SESSION_EXPIRY_WORKER_SPAWNER` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.cFpPBbFet.func1` | `0x73a580` | `0x33a580` | 1,600 B | `EXPIRED_USER_SWEEPER` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.chIaMDTZ` | `0x73ae20` | `0x33ae20` | 320 B | `ADMIN_ROLE_CHECK` | RECONSTRUCTED_FROM_BINARY | HIGH |
| `main.jlRPqj8Kko_8` | `0x743c40` | `0x343c40` | 1,184 B | `SESSION_KICK_HANDLER` | RECONSTRUCTED_FROM_BINARY | HIGH |

---

## 2. Detailed Function Forensic Specifications

### 1. `main.ltOjwqsMl5q8` — Login Route Handler
- **VA**: `0x73dd00` | **File Offset**: `0x33dd00` | **Size**: 2752 bytes
- **Semantic Role**: `AUTH_LOGIN_HANDLER`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Evidence Classes**: `INSTRUCTION_XREF`, `ROUTE_REGISTRATION`, `STRING_CONSTANTS`, `CALLER_CALLEE`, `DYNAMIC_ORACLE`
- **Route Registrations**: `POST /api/login`, `OPTIONS /api/login` (registered at `0x765a00`)
- **Strings**: `"Username and password are required"`, `"Invalid username or password"`, `"账号已到期，请联系管理员延时"`, `"token"`, `"username"`, `"role"`, `"assigned_devices"`
- **Disassembly Analysis**:
  - Validates HTTP method: `OPTIONS` returns 200 OK with CORS headers; `POST` proceeds; all other methods return 405.
  - JSON-unmarshals request into struct `{ Username string; Password string }`.
  - Trims username via `strings.TrimSpace`. If either `username == ""` or `password == ""`, returns HTTP 400 `"Username and password are required\n"`.
  - Acquires `sync.RWMutex.RLock` on `UsersStore`, looks up `user` by username. If absent, returns HTTP 401 `"Invalid username or password\n"`.
  - Checks `User.ExpiresAt`: if non-zero and `time.Now().After(user.ExpiresAt)`, returns HTTP 403 `"\u8d26\u53f7\u5df2\u5230\u671f\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\u5ef6\u65f6\n"`.
  - Calls `main.biG96MFIwa(0x739060)` passing `password` and `user.Salt`. Verifies computed hash against `user.Password` using `runtime.memequal`. If mismatch, returns HTTP 401 `"Invalid username or password\n"`.
  - Calls `main.vT6rYK_v(0x739320)` to generate token and insert 24h session.
  - Returns HTTP 200 JSON: `{"assigned_devices": user.AssignedDevices, "role": user.Role, "token": token, "username": user.Username}`.

### 2. `main.lYKp_Iuf` — Token Lookup & Auth Validation Helper
- **VA**: `0x73b080` | **File Offset**: `0x33b080` | **Size**: 1120 bytes
- **Semantic Role**: `AUTH_TOKEN_LOOKUP_AND_VALIDATE`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Evidence Classes**: `INSTRUCTION_XREF`, `FLAG_REGISTRATION`, `ENV_VAR_XREF`, `STRING_CONSTANTS`, `CALLER_CALLEE`, `DYNAMIC_ORACLE`
- **Callers**: Invoked by 31 protected route handlers across the codebase.
- **Disassembly Analysis**:
  - Checks global CLI flag `*noAuthFlag` (`0xc069a0`, `-no-auth`). If true, or if `os.Getenv("NO_AUTH") == "true"`, immediately returns `("admin", true)`.
  - Looks up `Authorization` header. If present, splits on whitespace; verifies case-insensitive `"bearer "` prefix and extracts token.
  - If header absent or empty, queries URL parameter `?token=<token>`. If missing, returns `("", false)`.
  - Acquires `sync.RWMutex.RLock` on `sessionMap`, looks up `token` (`runtime.mapaccess2_faststr`).
  - **Lazy Expiration**: If `time.Now().After(session.ExpiresAt)`, acquires `sync.Mutex.Lock` on `sessionMap`, deletes expired token (`runtime.mapdelete_faststr`), releases lock, and returns `("", false)`.
  - Acquires `sync.RWMutex.RLock` on `UsersStore`, looks up `user` by `session.Username`. If absent, returns `("", false)`.
  - Checks `User.ExpiresAt`: if non-zero and `time.Now().After(user.ExpiresAt)`, returns `("", false)`.
  - Returns `(user.Username, true)`.

### 3. `main.bjWkHiittd` — Logout & Token Revocation Handler
- **VA**: `0x7409a0` | **File Offset**: `0x3409a0` | **Size**: 1440 bytes
- **Semantic Role**: `AUTH_LOGOUT_AND_TOKEN_REVOCATION`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Route Registrations**: `POST /api/logout`, `OPTIONS /api/logout` (registered at `0x765a60`)
- **Disassembly Analysis**:
  - Extracts token from `Authorization: Bearer <token>` header or `?token=<token>` parameter.
  - If token present: acquires `sync.Mutex.Lock` on `sessionMap`, deletes token from map (`runtime.mapdelete_faststr`), releases lock.
  - Returns HTTP 200 JSON: `{"status": "success"}` (idempotent, always returns success even if token was already deleted or absent).

### 4. `main.bwvBd1LWVr` — Auth Status Handler
- **VA**: `0x73ec40` | **File Offset**: `0x33ec40` | **Size**: 1216 bytes
- **Semantic Role**: `AUTH_STATUS_HANDLER`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Route Registrations**: `GET /api/auth-status`, `OPTIONS /api/auth-status` (registered at `0x7659a0`)
- **Disassembly Analysis**:
  - Evaluates `*noAuthFlag || os.Getenv("NO_AUTH") == "true"`.
  - Sets boolean `noAuth` accordingly.
  - Returns HTTP 200 JSON: `{"noAuth": bool}` (`{"noAuth": false}` by default).

### 5. `main.gJ0OHScnGnWZ` — User Profile Handler (`/api/me`)
- **VA**: `0x73f100` | **File Offset**: `0x33f100` | **Size**: 2816 bytes
- **Semantic Role**: `USER_PROFILE_HANDLER`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Route Registrations**: `GET /api/me`, `OPTIONS /api/me` (registered at `0x765a30`)
- **Disassembly Analysis**:
  - Authenticates request via `main.lYKp_Iuf`. If false, returns HTTP 401 `"Unauthorized\n"`.
  - Acquires `sync.RWMutex.RLock` on `UsersStore` and retrieves user profile.
  - Marshals user fields into JSON response: `ai_config`, `assigned_devices`, `expires_at`, `forbid_audio`, `forbid_bitrate`, `forbid_fps`, `forbid_resolution`, `role`, `settings`, `username`.
  - Explicitly omits `password` and `salt`.

### 6. `main.biG96MFIwa` — Password Hash Verifier
- **VA**: `0x739060` | **File Offset**: `0x339060` | **Size**: 480 bytes
- **Semantic Role**: `PASSWORD_HASH_VERIFIER`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Disassembly Analysis**:
  - Concatenates `password + salt` using `runtime.concatbyte2` (order: `password` first, `salt` second).
  - Computes `crypto/sha256` digest: `Reset()`, `Write(concat)`, `Sum(nil)`.
  - Encodes 32-byte digest into 64-character lowercase hex string using lookup table at `0x8271ab` (`"0123456789abcdef"`).
  - Returns 64-char string.

### 7. `main.vT6rYK_v` — Session Creator & Inserter
- **VA**: `0x739320` | **File Offset**: `0x339320` | **Size**: 288 bytes
- **Semantic Role**: `SESSION_CREATOR_AND_INSERTER`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Disassembly Analysis**:
  - Calls `main.d2SHxnu(0x739240)` to generate 64-character random token.
  - Computes `session.ExpiresAt = time.Now().Add(24 * time.Hour)` (`0x4e94914f0000` nanoseconds).
  - Acquires `sync.Mutex.Lock` on `sessionMap`.
  - Stores 40-byte value struct `{ Username string; ExpiresAt time.Time }` into `sessionMap[token]` (`runtime.mapassign_faststr`, type descriptor `0x7c01c0`).
  - Releases lock and returns `token`.

### 8. `main.d2SHxnu` — Session Token Generator
- **VA**: `0x739240` | **File Offset**: `0x339240` | **Size**: 224 bytes
- **Semantic Role**: `SESSION_TOKEN_GENERATOR`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Disassembly Analysis**:
  - Allocates 32-byte buffer on stack (`sub rsp, 0x38`).
  - Calls `crypto/rand.Read` (`0x52a5e0`, `Y4_aOVf1Fz.ES8BvDO6y1V`) reading 32 cryptographically secure random bytes (`RANDOM_INPUT_BITS = 256`).
  - Allocates 64-byte slice via `runtime.makeslice`.
  - Encodes 32 random bytes to 64 lowercase hex characters using lookup table at `0x827245` (`"0123456789abcdef"`).
  - Converts slice to Go string via `runtime.slicebytetostring`.

### 9. `main.cFpPBbFet` — Expiry Worker Spawner
- **VA**: `0x73a500` | **File Offset**: `0x33a500` | **Size**: 128 bytes
- **Semantic Role**: `SESSION_EXPIRY_WORKER_SPAWNER`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Disassembly Analysis**:
  - Creates 1-minute ticker via `time.NewTicker(0xdf8475800 ns = 60,000,000,000 ns = 60 seconds)`.
  - Spawns background goroutine running `main.cFpPBbFet.func1(0x73a580)` using `runtime.newproc`.

### 10. `main.cFpPBbFet.func1` — Expired User Sweeper
- **VA**: `0x73a580` | **File Offset**: `0x33a580` | **Size**: 1600 bytes
- **Semantic Role**: `EXPIRED_USER_SWEEPER`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Disassembly Analysis**:
  - Loops on ticker channel (`runtime.chanrecv2`).
  - Acquires `sync.RWMutex.RLock` on `UsersStore`.
  - Scans all users: checks `user.ExpiresAt`. If `!user.ExpiresAt.IsZero() && time.Now().After(user.ExpiresAt)`, records username.
  - Releases lock on `UsersStore`.
  - For each expired username:
    - Acquires `sync.Mutex.Lock` on `sessionMap`.
    - Iterates `sessionMap`, finds all tokens where `session.Username == expiredUser.Username`.
    - Deletes matching tokens (`runtime.mapdelete_faststr`).
    - Releases lock on `sessionMap`.
    - Invokes connection kicking routines (`main.jlRPqj8Kko_8`).
    - Logs: `"[User] Account %s expired, tokens revoked and sessions kicked"`.

### 11. `main.chIaMDTZ` — Admin Role Authorization Check
- **VA**: `0x73ae20` | **File Offset**: `0x33ae20` | **Size**: 320 bytes
- **Semantic Role**: `ADMIN_ROLE_CHECK`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Disassembly Analysis**:
  - Verifies user's role from `UsersStore` equals `"admin"`.
  - If mismatch, returns HTTP 403 `"Forbidden: admin only\n"`.

### 12. `main.jlRPqj8Kko_8` — Session Kick Handler
- **VA**: `0x743c40` | **File Offset**: `0x343c40` | **Size**: 1184 bytes
- **Semantic Role**: `SESSION_KICK_HANDLER`
- **Classification**: `RECONSTRUCTED_FROM_BINARY` | **Confidence**: `HIGH`
- **Disassembly Analysis**:
  - Called during admin kick or expired user sweep.
  - Logs: `"[Admin] Kicking session for user %s (Close conn)"`.
  - Triggers peer connection termination. (Network-level side-effects deferred to networking phase).
