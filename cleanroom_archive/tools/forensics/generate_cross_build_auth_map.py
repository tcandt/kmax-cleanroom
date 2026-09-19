import json
from pathlib import Path

LINUX_SHA = "6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3"
WIN_SHA = "374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917"

linux_entries = [
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.ltOjwqsMl5q8",
        "VA": "0x73dd00",
        "file_offset": "0x33dd00",
        "function_size": 2752,
        "semantic_role": "AUTH_LOGIN_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["POST /api/login", "OPTIONS /api/login"],
        "callee_patterns": ["main.biG96MFIwa (0x739060 - SHA256)", "main.vT6rYK_v (0x739320 - Session Creator)", "time.Time.After (User.ExpiresAt)"],
        "string_constants": ["Username and password are required", "Invalid username or password", "\\u8d26\\u53f7\\u5df2\\u5230\\u671f\\uff0c\\u8bf7\\u8054\\u7cfb\\u7ba1\\u7406\\u5458\\u5ef6\\u65f6", "token", "username", "role", "assigned_devices"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.lYKp_Iuf",
        "VA": "0x73b080",
        "file_offset": "0x33b080",
        "function_size": 1120,
        "semantic_role": "AUTH_TOKEN_LOOKUP",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "FLAG_REGISTRATION", "ENV_VAR_XREF", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["Called by 31 protected route handlers across server"],
        "callee_patterns": ["sync.RWMutex.RLock (sessionMap)", "runtime.mapaccess2_faststr", "time.Time.After (Session TTL)", "runtime.mapdelete_faststr (lazy eviction)", "runtime.mapaccess2 (UsersStore user)"],
        "string_constants": ["Authorization", "bearer", "token", "NO_AUTH", "no-auth", "admin"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.d2SHxnu",
        "VA": "0x739240",
        "file_offset": "0x339240",
        "function_size": 224,
        "semantic_role": "TOKEN_GENERATOR",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "CRYPTO_RAND_CALL", "HEX_ENCODING_TABLE", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.vT6rYK_v (0x739320)"],
        "callee_patterns": ["crypto/rand.Read (32 bytes)", "runtime.makeslice (64 bytes)", "hex lookup table 0x8271ab", "runtime.slicebytetostring"],
        "string_constants": ["0123456789abcdef"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.vT6rYK_v",
        "VA": "0x739320",
        "file_offset": "0x339320",
        "function_size": 288,
        "semantic_role": "SESSION_CREATOR",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "TIME_DURATION_CONSTANT", "STRUCT_DESCRIPTOR_XREF", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.ltOjwqsMl5q8 (0x73dd00)"],
        "callee_patterns": ["main.d2SHxnu (0x739240 - token generator)", "sync.Mutex.Lock", "time.Now", "time.Time.Add (0x4e94914f0000 ns = 24h)", "runtime.mapassign_faststr", "sync.Mutex.Unlock"],
        "string_constants": []
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.bjWkHiittd",
        "VA": "0x7409a0",
        "file_offset": "0x3409a0",
        "function_size": 1440,
        "semantic_role": "LOGOUT_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["POST /api/logout", "OPTIONS /api/logout"],
        "callee_patterns": ["Extract Bearer token", "sync.Mutex.Lock", "runtime.mapdelete_faststr", "sync.Mutex.Unlock", "json.Marshal({\"status\":\"success\"})"],
        "string_constants": ["Authorization", "bearer", "token", "status", "success"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.bwvBd1LWVr",
        "VA": "0x73ec40",
        "file_offset": "0x33ec40",
        "function_size": 1216,
        "semantic_role": "AUTH_STATUS_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "FLAG_REGISTRATION", "ENV_VAR_XREF", "DYNAMIC_ORACLE"],
        "route_xrefs": ["GET /api/auth-status", "OPTIONS /api/auth-status"],
        "callee_patterns": ["Check noAuth flag / NO_AUTH env", "main.lYKp_Iuf (optional token auth)", "json.Marshal({\"noAuth\": bool, ...})"],
        "string_constants": ["noAuth", "NO_AUTH", "no-auth"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.gJ0OHScnGnWZ",
        "VA": "0x73f100",
        "file_offset": "0x33f100",
        "function_size": 2816,
        "semantic_role": "USER_PROFILE_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["GET /api/me", "OPTIONS /api/me"],
        "callee_patterns": ["main.lYKp_Iuf (token auth)", "sync.RWMutex.RLock (UsersStore)", "json.Marshal(User details)"],
        "string_constants": ["Unauthorized", "username", "role", "assigned_devices", "settings", "expires_at"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.biG96MFIwa",
        "VA": "0x739060",
        "file_offset": "0x339060",
        "function_size": 480,
        "semantic_role": "PASSWORD_HASH",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "CRYPTO_SHA256_CALLS", "HEX_ENCODING_TABLE", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.ltOjwqsMl5q8 (login) and main.aOfaLG (admin init)"],
        "callee_patterns": ["runtime.concatbyte2(password, salt)", "crypto/sha256.(*digest).Reset/Write/Sum", "hex lookup table 0x8271ab", "runtime.slicebytetostring"],
        "string_constants": ["0123456789abcdef"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.cFpPBbFet",
        "VA": "0x73a500",
        "file_offset": "0x33a500",
        "function_size": 128,
        "semantic_role": "SESSION_SWEEPER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "TIME_TICKER_CONSTANT", "GOROUTINE_SPAWN"],
        "route_xrefs": ["Called during server initialization in main.main"],
        "callee_patterns": ["time.NewTicker(0xdf8475800 ns = 1 minute)", "runtime.newproc(main.cFpPBbFet.func1)"],
        "string_constants": []
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.cFpPBbFet.func1",
        "VA": "0x73a580",
        "file_offset": "0x33a580",
        "function_size": 1600,
        "semantic_role": "SESSION_SWEEPER_WORKER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE", "MAP_MUTEX_EVIDENCE"],
        "route_xrefs": ["Background worker goroutine"],
        "callee_patterns": ["runtime.chanrecv2(ticker.C)", "time.Now", "time.Time.After(user.ExpiresAt)", "sync.Mutex.Lock (sessionMap evictions)"],
        "string_constants": ["[User] Account %s expired, tokens revoked and sessions kicked"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.chIaMDTZ",
        "VA": "0x73ae20",
        "file_offset": "0x33ae20",
        "function_size": 320,
        "semantic_role": "ADMIN_ROLE_CHECK",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE"],
        "route_xrefs": ["Called by admin endpoints after token lookup"],
        "callee_patterns": ["sync.RWMutex.RLock (UsersStore role check)", "string compare == 'admin'"],
        "string_constants": ["Forbidden: admin only", "admin"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
        "sha256": LINUX_SHA,
        "os": "linux",
        "arch": "amd64",
        "binary_symbol": "main.jlRPqj8Kko_8",
        "VA": "0x743c40",
        "file_offset": "0x343c40",
        "function_size": 1184,
        "semantic_role": "SESSION_KICK_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE"],
        "route_xrefs": ["POST /api/admin/users/kick", "OPTIONS /api/admin/users/kick"],
        "callee_patterns": ["main.chIaMDTZ (admin check)", "sync.Mutex.Lock", "runtime.mapdelete_faststr", "sync.Mutex.Unlock"],
        "string_constants": ["username", "status", "success"]
    }
]

win_entries = [
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.u4r2NulQUnF",
        "VA": "0x140346f00",
        "file_offset": "0x346500",
        "function_size": 2784,
        "semantic_role": "AUTH_LOGIN_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["POST /api/login", "OPTIONS /api/login"],
        "callee_patterns": ["main.sMCA9mvX (0x140342220 - SHA256)", "main.wdxJrUcsH (0x1403424e0 - Session Creator)", "time.Time.After (User.ExpiresAt)"],
        "string_constants": ["Username and password are required", "Invalid username or password", "\\u8d26\\u53f7\\u5df2\\u5230\\u671f\\uff0c\\u8bf7\\u8054\\u7cfb\\u7ba1\\u7406\\u5458\\u5ef6\\u65f6", "token", "username", "role", "assigned_devices"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.mLWT3o",
        "VA": "0x140344260",
        "file_offset": "0x343860",
        "function_size": 1152,
        "semantic_role": "AUTH_TOKEN_LOOKUP",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "FLAG_REGISTRATION", "ENV_VAR_XREF", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["Called by 31 protected route handlers across server"],
        "callee_patterns": ["sync.RWMutex.RLock (sessionMap)", "runtime.mapaccess2_faststr", "time.Time.After (Session TTL)", "runtime.mapdelete_faststr (lazy eviction)", "runtime.mapaccess2 (UsersStore user)"],
        "string_constants": ["Authorization", "bearer", "token", "NO_AUTH", "no-auth", "admin"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.af9fyOpAy",
        "VA": "0x140342400",
        "file_offset": "0x341a00",
        "function_size": 224,
        "semantic_role": "TOKEN_GENERATOR",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "CRYPTO_RAND_CALL", "HEX_ENCODING_TABLE", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.wdxJrUcsH (0x1403424e0)"],
        "callee_patterns": ["crypto/rand.Read (32 bytes)", "runtime.makeslice (64 bytes)", "hex lookup table", "runtime.slicebytetostring"],
        "string_constants": ["0123456789abcdef"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.wdxJrUcsH",
        "VA": "0x1403424e0",
        "file_offset": "0x341ae0",
        "function_size": 288,
        "semantic_role": "SESSION_CREATOR",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "TIME_DURATION_CONSTANT", "STRUCT_DESCRIPTOR_XREF", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.u4r2NulQUnF (0x140346f00)"],
        "callee_patterns": ["main.af9fyOpAy (0x140342400 - token generator)", "sync.Mutex.Lock", "time.Now", "time.Time.Add (0x4e94914f0000 ns = 24h)", "runtime.mapassign_faststr", "sync.Mutex.Unlock"],
        "string_constants": []
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.blPINsMc3",
        "VA": "0x140349bc0",
        "file_offset": "0x3491c0",
        "function_size": 1440,
        "semantic_role": "LOGOUT_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["POST /api/logout", "OPTIONS /api/logout"],
        "callee_patterns": ["Extract Bearer token", "sync.Mutex.Lock", "runtime.mapdelete_faststr", "sync.Mutex.Unlock", "json.Marshal({\"status\":\"success\"})"],
        "string_constants": ["Authorization", "bearer", "token", "status", "success"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.waSrU4iH",
        "VA": "0x140347e60",
        "file_offset": "0x347460",
        "function_size": 1216,
        "semantic_role": "AUTH_STATUS_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "FLAG_REGISTRATION", "ENV_VAR_XREF", "DYNAMIC_ORACLE"],
        "route_xrefs": ["GET /api/auth-status", "OPTIONS /api/auth-status"],
        "callee_patterns": ["Check noAuth flag / NO_AUTH env", "main.mLWT3o (optional token auth)", "json.Marshal({\"noAuth\": bool, ...})"],
        "string_constants": ["noAuth", "NO_AUTH", "no-auth"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.k0Ckv2FQUr",
        "VA": "0x140348320",
        "file_offset": "0x347920",
        "function_size": 2816,
        "semantic_role": "USER_PROFILE_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["GET /api/me", "OPTIONS /api/me"],
        "callee_patterns": ["main.mLWT3o (token auth)", "sync.RWMutex.RLock (UsersStore)", "json.Marshal(User details)"],
        "string_constants": ["Unauthorized", "username", "role", "assigned_devices", "settings", "expires_at"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.sMCA9mvX",
        "VA": "0x140342220",
        "file_offset": "0x341820",
        "function_size": 480,
        "semantic_role": "PASSWORD_HASH",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "CRYPTO_SHA256_CALLS", "HEX_ENCODING_TABLE", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.u4r2NulQUnF (login)"],
        "callee_patterns": ["runtime.concatbyte2(password, salt)", "crypto/sha256.(*digest).Reset/Write/Sum", "hex lookup table", "runtime.slicebytetostring"],
        "string_constants": ["0123456789abcdef"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.wFSLlBV",
        "VA": "0x1403436e0",
        "file_offset": "0x342ce0",
        "function_size": 128,
        "semantic_role": "SESSION_SWEEPER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "TIME_TICKER_CONSTANT", "GOROUTINE_SPAWN"],
        "route_xrefs": ["Called during server initialization in main.main"],
        "callee_patterns": ["time.NewTicker(0xdf8475800 ns = 1 minute)", "runtime.newproc(main.wFSLlBV.func1)"],
        "string_constants": []
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.wFSLlBV.func1",
        "VA": "0x140343760",
        "file_offset": "0x342d60",
        "function_size": 1600,
        "semantic_role": "SESSION_SWEEPER_WORKER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE", "MAP_MUTEX_EVIDENCE"],
        "route_xrefs": ["Background worker goroutine"],
        "callee_patterns": ["runtime.chanrecv2(ticker.C)", "time.Now", "time.Time.After(user.ExpiresAt)", "sync.Mutex.Lock (sessionMap evictions)"],
        "string_constants": ["[User] Account %s expired, tokens revoked and sessions kicked"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.iP8aiT",
        "VA": "0x140344000",
        "file_offset": "0x343600",
        "function_size": 320,
        "semantic_role": "ADMIN_ROLE_CHECK",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE"],
        "route_xrefs": ["Called by admin endpoints after token lookup"],
        "callee_patterns": ["sync.RWMutex.RLock (UsersStore role check)", "string compare == 'admin'"],
        "string_constants": ["Forbidden: admin only", "admin"]
    },
    {
        "artifact": "cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe",
        "sha256": WIN_SHA,
        "os": "windows",
        "arch": "amd64",
        "binary_symbol": "main.ijEGVZRAZQb",
        "VA": "0x140350b00",
        "file_offset": "0x350100",
        "function_size": 1184,
        "semantic_role": "SESSION_KICK_HANDLER",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE"],
        "route_xrefs": ["POST /api/admin/users/kick", "OPTIONS /api/admin/users/kick"],
        "callee_patterns": ["main.iP8aiT (admin check)", "sync.Mutex.Lock", "runtime.mapdelete_faststr", "sync.Mutex.Unlock"],
        "string_constants": ["username", "status", "success"]
    }
]

# Write canonical per-artifact maps
p_linux = Path("evidence/go_signaling/auth/linux_amd64/AUTH_FUNCTION_MAP.json")
p_win = Path("evidence/go_signaling/auth/windows_amd64/AUTH_FUNCTION_MAP.json")
p_linux.write_text(json.dumps(linux_entries, indent=2), encoding="utf-8")
p_win.write_text(json.dumps(win_entries, indent=2), encoding="utf-8")

# Write root AUTH_FUNCTION_MAP.json as Linux canonical reference
p_root = Path("evidence/go_signaling/auth/AUTH_FUNCTION_MAP.json")
p_root.write_text(json.dumps(linux_entries, indent=2), encoding="utf-8")

# Cross-build correlation
correlation = []
for le in linux_entries:
    role = le["semantic_role"]
    we = next(w for w in win_entries if w["semantic_role"] == role)
    correlation.append({
        "semantic_role": role,
        "linux_amd64": {
            "symbol": le["binary_symbol"],
            "va": le["VA"],
            "file_offset": le["file_offset"],
            "size": le["function_size"]
        },
        "windows_amd64": {
            "symbol": we["binary_symbol"],
            "va": we["VA"],
            "file_offset": we["file_offset"],
            "size": we["function_size"]
        },
        "correlation_evidence": {
            "route_xrefs": le["route_xrefs"],
            "string_constants": [s for s in le["string_constants"] if s in we["string_constants"]],
            "functional_behavior": f"Parity across size ({le['function_size']} vs {we['function_size']}) and callee sequence"
        }
    })

p_corr_json = Path("evidence/go_signaling/auth/AUTH_CROSS_BUILD_CORRELATION.json")
p_corr_json.write_text(json.dumps(correlation, indent=2), encoding="utf-8")

# Generate Markdown
rows = []
for c in correlation:
    l = c["linux_amd64"]
    w = c["windows_amd64"]
    rows.append(
        f"| `{c['semantic_role']}` | `{l['symbol']}` | `{l['va']}` ({l['size']}B) | `{w['symbol']}` | `{w['va']}` ({w['size']}B) | `{', '.join(c['correlation_evidence']['route_xrefs'])}` |"
    )

md_content = f"""# Cross-Build Forensic Function Correlation: Authentication Subsystem

**Analysis Target 1**: `webrtc-signaling` (Linux AMD64, SHA256: `{LINUX_SHA}`)  
**Analysis Target 2**: `webrtc-signaling.exe` (Windows AMD64, SHA256: `{WIN_SHA}`)  
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
{chr(10).join(rows)}

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
"""

p_corr_md = Path("evidence/go_signaling/auth/AUTH_CROSS_BUILD_CORRELATION.md")
p_corr_md.write_text(md_content, encoding="utf-8")

print("Generated canonical maps and cross-build correlation.")
