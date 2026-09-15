# Cross-Build Forensic Function Correlation: Authentication Subsystem

**Analysis Target 1**: `webrtc-signaling` (Linux AMD64, SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Analysis Target 2**: `webrtc-signaling.exe` (Windows AMD64, SHA256: `374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917`)  
**Scope**: Full Correlation of 12 Core Authentication, Session, and Account Management Functions  

---

## 1. Forensic Rule: Cross-Build Symbol Garbling Disconnect

> [!WARNING]
> **Garbled Go Symbols Are Non-Deterministic Across Builds**:
> The build pipelines for Linux and Windows used independent obfuscation/build passes. Garbled symbol identifiers (e.g. `main.ltOjwqsMl5q8` vs `main.u4r2NulQUnF`) differ completely. Symbols MUST NEVER be correlated by text name alone. Every function is strictly correlated by **semantic role, route cross-references, string constants, callee execution graphs, and dynamic runtime observation**.

---

## 2. Canonical Correlation Table

| Stable Semantic Role | Linux AMD64 Symbol | Linux VA & Size | Windows AMD64 Symbol | Windows VA & Size | Route / Entry Xrefs |
|---|---|---|---|---|---|
| `AUTH_LOGIN_HANDLER` | `main.ltOjwqsMl5q8` | `0x73dd00` (2752B) | `main.u4r2NulQUnF` | `0x140346f00` (2784B) | `POST /api/login, OPTIONS /api/login` |
| `AUTH_TOKEN_LOOKUP` | `main.lYKp_Iuf` | `0x73b080` (1120B) | `main.mLWT3o` | `0x140344260` (1152B) | `Called by 31 protected route handlers across server` |
| `TOKEN_GENERATOR` | `main.d2SHxnu` | `0x739240` (224B) | `main.af9fyOpAy` | `0x140342400` (224B) | `Called by main.vT6rYK_v (0x739320)` |
| `SESSION_CREATOR` | `main.vT6rYK_v` | `0x739320` (288B) | `main.wdxJrUcsH` | `0x1403424e0` (288B) | `Called by main.ltOjwqsMl5q8 (0x73dd00)` |
| `LOGOUT_HANDLER` | `main.bjWkHiittd` | `0x7409a0` (1440B) | `main.blPINsMc3` | `0x140349bc0` (1440B) | `POST /api/logout, OPTIONS /api/logout` |
| `AUTH_STATUS_HANDLER` | `main.bwvBd1LWVr` | `0x73ec40` (1216B) | `main.waSrU4iH` | `0x140347e60` (1216B) | `GET /api/auth-status, OPTIONS /api/auth-status` |
| `USER_PROFILE_HANDLER` | `main.gJ0OHScnGnWZ` | `0x73f100` (2816B) | `main.k0Ckv2FQUr` | `0x140348320` (2816B) | `GET /api/me, OPTIONS /api/me` |
| `PASSWORD_HASH` | `main.biG96MFIwa` | `0x739060` (480B) | `main.sMCA9mvX` | `0x140342220` (480B) | `Called by main.ltOjwqsMl5q8 (login) and main.aOfaLG (admin init)` |
| `SESSION_SWEEPER` | `main.cFpPBbFet` | `0x73a500` (128B) | `main.wFSLlBV` | `0x1403436e0` (128B) | `Called during server initialization in main.main` |
| `SESSION_SWEEPER_WORKER` | `main.cFpPBbFet.func1` | `0x73a580` (1600B) | `main.wFSLlBV.func1` | `0x140343760` (1600B) | `Background worker goroutine` |
| `ADMIN_ROLE_CHECK` | `main.chIaMDTZ` | `0x73ae20` (320B) | `main.iP8aiT` | `0x140344000` (320B) | `Called by admin endpoints after token lookup` |
| `SESSION_KICK_HANDLER` | `main.jlRPqj8Kko_8` | `0x743c40` (1184B) | `main.ijEGVZRAZQb` | `0x140350b00` (1184B) | `POST /api/admin/users/kick, OPTIONS /api/admin/users/kick` |

---

## 3. Evidence Classes & Methodology

1. **Route Handler Registrations**:
   - In Linux AMD64: 43 routes registered in `main.main` (`0x747880`) via `net/http.(*ServeMux).HandleFunc`.
   - In Windows AMD64: 43 routes registered in `main.main` (`0x14036db00`) via `H0Ekdfs.XNsviZ1` (obfuscated `HandleFunc`).
   - Exact route patterns (`/api/login`, `/api/logout`, `/api/auth-status`, `/api/me`, `/api/admin/users/kick`) correlate to matching handlers.

2. **Core Primitive Structural Invariants**:
   - `TOKEN_GENERATOR`: Linux `main.d2SHxnu` (224B) and Windows `main.af9fyOpAy` (224B) both invoke `crypto/rand.Read` for 32 bytes and translate into 64-char lowercase hex via identical byte shifting and unrolled lookup loops.
   - `PASSWORD_HASH`: Linux `main.biG96MFIwa` (480B) and Windows `main.sMCA9mvX` (480B) both execute `runtime.concatbyte2(password, salt)` -> `crypto/sha256` -> hex encode.
   - `SESSION_CREATOR`: Linux `main.vT6rYK_v` (288B) and Windows `main.wdxJrUcsH` (288B) both call token generator, lock mutex, compute `time.Now().Add(24h)`, and store into `sessionMap`.
   - `SESSION_SWEEPER_WORKER`: Linux `main.cFpPBbFet.func1` (1600B) and Windows `main.wFSLlBV.func1` (1600B) both receive from 1-minute ticker, iterate users, check `time.After(user.ExpiresAt)`, and print verbatim diagnostic `[User] Account %s expired, tokens revoked and sessions kicked`.
