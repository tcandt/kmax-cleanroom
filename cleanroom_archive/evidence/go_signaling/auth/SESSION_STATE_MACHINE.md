# Forensic Session State Machine (`SESSION_STATE_MACHINE.md`)

**Classification**: `STATIC_AND_DYNAMIC_CONFIRMED`  
**Subsystem**: In-Memory Session Management (`webrtc-signaling`)

---

## 1. State Machine Model

```text
       ┌───────────────────────────────┐
       │          NO_SESSION           │
       └──────────────┬────────────────┘
                      │
                      │ POST /api/login (valid credentials)
                      ▼
       ┌───────────────────────────────┐
       │         AUTHENTICATED         │
       └──────┬──────────────┬─────────┘
              │              │
              │              │ POST /api/logout
              │              ▼
              │       ┌───────────────┐
              │       │    REVOKED    │
              │       └───────────────┘
              │
              ├──────► time.Now() >= session.ExpiresAt (+24h)
              │        │
              │        ▼
              │       ┌───────────────┐
              │       │    EXPIRED    │ (lazy eviction on lookup)
              │       └───────────────┘
              │
              ├──────► time.Now() >= user.ExpiresAt
              │        │
              │        ▼
              │       ┌────────────────┐
              │       │ ACCOUNT_EXPIRED│ (rejected on lookup & swept by 1-min worker)
              │       └────────────────┘
              │
              └──────► Process Restart
                       │
                       ▼
                      ┌───────────────┐
                      │    INVALID    │ (in-memory map cleared)
                      └───────────────┘
```

---

## 2. State Invariants & Behavior

1. **NO_SESSION**:
   - Request has no `Authorization` header and no `?token=` query parameter.
   - Access to protected endpoints returns HTTP 401 `"Unauthorized
"`.

2. **AUTHENTICATED**:
   - Token is 64 lowercase hex characters.
   - Token exists in `sessionMap`.
   - `time.Now().Before(session.ExpiresAt)` is true.
   - User exists in `UsersStore` and (`user.ExpiresAt.IsZero()` OR `time.Now().Before(user.ExpiresAt)`).
   - Access to `/api/me` returns HTTP 200 with user profile.

3. **EXPIRED (Session TTL Expiration)**:
   - Evaluated lazily in `main.lYKp_Iuf` (`0x73b080`) when the token is presented.
   - Upon detecting expiration, `main.lYKp_Iuf` locks `sessionMap`, executes `delete(sessionMap, token)`, unlocks, and rejects with HTTP 401.

4. **ACCOUNT_EXPIRED (Account Expiration)**:
   - Login attempt: Returns HTTP 403 `"账号已到期，请联系管理员延时
"`.
   - Existing session lookup: Rejected with HTTP 401 `"Unauthorized
"`.
   - Background sweeper: `main.cFpPBbFet.func1` sweeps every 1 minute, revokes all tokens for expired users from `sessionMap`, kicks active connections, and logs `"[User] Account %s expired, tokens revoked and sessions kicked"`.

5. **REVOKED (Explicit Logout)**:
   - Client sends `POST /api/logout` with Bearer token.
   - `main.bjWkHiittd` deletes token from `sessionMap`.
   - Returns HTTP 200 `{"status": "success"}`.
   - Subsequent requests with this token return HTTP 401 `"Unauthorized
"`.

6. **INVALID**:
   - Random tokens, malformed strings, or tokens presented after process restart.
   - Returns HTTP 401 `"Unauthorized
"`.
