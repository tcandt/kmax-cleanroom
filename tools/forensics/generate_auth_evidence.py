import json
from pathlib import Path

# Load function map and callgraph
with open('evidence/go_signaling/FUNCTION_MAP.json', 'r', encoding='utf-8') as f:
    funcs = json.load(f)
fmap = {f['va']: f for f in funcs}

with open('evidence/go_signaling/CALLGRAPH.json', 'r', encoding='utf-8') as f:
    cg = json.load(f)

# Find reverse callers
callers_map = {}
for caller, callees in cg.items():
    callee_list = callees if isinstance(callees, list) else callees.get('callees', [])
    for c in callee_list:
        c_va = c if isinstance(c, str) else hex(c)
        if not c_va.startswith('0x'):
            try:
                c_va = hex(int(c_va))
            except:
                pass
        callers_map.setdefault(c_va, []).append(caller)

# Define the 12 core auth/session functions identified
auth_entries = [
    {
        "binary_symbol": "main.ltOjwqsMl5q8",
        "va": "0x73dd00",
        "file_offset": "0x33dd00",
        "size": 2752,
        "semantic_role": "AUTH_LOGIN_HANDLER",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["POST /api/login", "OPTIONS /api/login"],
        "crypto_xrefs": ["main.biG96MFIwa (0x739060 - SHA256)", "main.vT6rYK_v (0x739320 - Token Issuance)"],
        "time_xrefs": ["time.Now", "time.Time.After (User.ExpiresAt validation)"],
        "map/mutex evidence": ["sync.RWMutex.RLock (UsersStore lookup)", "sync.Mutex.Lock (sessionMap insertion via main.vT6rYK_v)"],
        "strings": ["Username and password are required", "Invalid username or password", "\u8d26\u53f7\u5df2\u5230\u671f\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\u5ef6\u65f6", "token", "username", "role", "assigned_devices"]
    },
    {
        "binary_symbol": "main.lYKp_Iuf",
        "va": "0x73b080",
        "file_offset": "0x33b080",
        "size": 1120,
        "semantic_role": "AUTH_TOKEN_LOOKUP_AND_VALIDATE",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "FLAG_REGISTRATION", "ENV_VAR_XREF", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["Called by 31 protected route handlers across server"],
        "crypto_xrefs": ["crypto/rand token lookup match"],
        "time_xrefs": ["time.Now", "time.Time.After (Session TTL check)", "time.Time.After (User.ExpiresAt check)"],
        "map/mutex evidence": ["sync.RWMutex.RLock (sessionMap lookup)", "sync.Mutex.Lock (lazy deletion on expired session)", "sync.RWMutex.RLock (UsersStore user lookup)"],
        "strings": ["Authorization", "bearer", "token", "NO_AUTH", "no-auth", "admin"]
    },
    {
        "binary_symbol": "main.bjWkHiittd",
        "va": "0x7409a0",
        "file_offset": "0x3409a0",
        "size": 1440,
        "semantic_role": "AUTH_LOGOUT_AND_TOKEN_REVOCATION",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["POST /api/logout", "OPTIONS /api/logout"],
        "crypto_xrefs": ["token revocation lookup"],
        "time_xrefs": [],
        "map/mutex evidence": ["sync.Mutex.Lock (sessionMap deletion via runtime.mapdelete_faststr)"],
        "strings": ["Authorization", "bearer", "token", "status", "success"]
    },
    {
        "binary_symbol": "main.bwvBd1LWVr",
        "va": "0x73ec40",
        "file_offset": "0x33ec40",
        "size": 1216,
        "semantic_role": "AUTH_STATUS_HANDLER",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "FLAG_REGISTRATION", "ENV_VAR_XREF", "DYNAMIC_ORACLE"],
        "route_xrefs": ["GET /api/auth-status", "OPTIONS /api/auth-status"],
        "crypto_xrefs": [],
        "time_xrefs": [],
        "map/mutex evidence": [],
        "strings": ["noAuth", "NO_AUTH", "no-auth"]
    },
    {
        "binary_symbol": "main.gJ0OHScnGnWZ",
        "va": "0x73f100",
        "file_offset": "0x33f100",
        "size": 2816,
        "semantic_role": "USER_PROFILE_HANDLER",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "ROUTE_REGISTRATION", "STRING_CONSTANTS", "CALLER_CALLEE", "DYNAMIC_ORACLE"],
        "route_xrefs": ["GET /api/me", "OPTIONS /api/me"],
        "crypto_xrefs": ["Token authentication via main.lYKp_Iuf"],
        "time_xrefs": ["ExpiresAt serialization"],
        "map/mutex evidence": ["sync.RWMutex.RLock (UsersStore lookup)"],
        "strings": ["Unauthorized", "username", "role", "assigned_devices", "settings", "expires_at", "forbid_bitrate", "forbid_fps", "forbid_resolution", "forbid_audio", "ai_config"]
    },
    {
        "binary_symbol": "main.biG96MFIwa",
        "va": "0x739060",
        "file_offset": "0x339060",
        "size": 480,
        "semantic_role": "PASSWORD_HASH_VERIFIER",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "CRYPTO_SHA256_CALLS", "HEX_ENCODING_TABLE", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.ltOjwqsMl5q8 (login) and main.aOfaLG (default admin init)"],
        "crypto_xrefs": ["runtime.concatbyte2(password, salt)", "crypto/sha256.(*digest).Reset/Write/Sum", "hex lowercase lookup table 0x8271ab"],
        "time_xrefs": [],
        "map/mutex evidence": [],
        "strings": ["0123456789abcdef"]
    },
    {
        "binary_symbol": "main.vT6rYK_v",
        "va": "0x739320",
        "file_offset": "0x339320",
        "size": 288,
        "semantic_role": "SESSION_CREATOR_AND_INSERTER",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "TIME_DURATION_CONSTANT", "STRUCT_DESCRIPTOR_XREF", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.ltOjwqsMl5q8 (login)"],
        "crypto_xrefs": ["Calls main.d2SHxnu (0x739240) for 32-byte crypto/rand token"],
        "time_xrefs": ["time.Now", "time.Time.Add(0x4e94914f0000 ns = 24h)"],
        "map/mutex evidence": ["sync.Mutex.Lock (sessionMap at 0xc068f0)", "runtime.mapassign_faststr (type descriptor 0x7c01c0, elem descriptor 0x7d6ee0)"],
        "strings": []
    },
    {
        "binary_symbol": "main.d2SHxnu",
        "va": "0x739240",
        "file_offset": "0x339240",
        "size": 224,
        "semantic_role": "SESSION_TOKEN_GENERATOR",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "CRYPTO_RAND_CALL", "HEX_ENCODING_TABLE", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.vT6rYK_v (session creation)"],
        "crypto_xrefs": ["crypto/rand.Read(32 bytes)", "hex encoding 32 bytes -> 64 lowercase hex chars"],
        "time_xrefs": [],
        "map/mutex evidence": [],
        "strings": ["0123456789abcdef"]
    },
    {
        "binary_symbol": "main.cFpPBbFet",
        "va": "0x73a500",
        "file_offset": "0x33a500",
        "size": 128,
        "semantic_role": "SESSION_EXPIRY_WORKER_SPAWNER",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "TIME_TICKER_CONSTANT", "GOROUTINE_SPAWN"],
        "route_xrefs": ["Called during server initialization in main.main"],
        "crypto_xrefs": [],
        "time_xrefs": ["time.NewTicker(0xdf8475800 ns = 1 minute)"],
        "map/mutex evidence": [],
        "strings": []
    },
    {
        "binary_symbol": "main.cFpPBbFet.func1",
        "va": "0x73a580",
        "file_offset": "0x33a580",
        "size": 1600,
        "semantic_role": "EXPIRED_USER_SWEEPER",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE", "MAP_MUTEX_EVIDENCE"],
        "route_xrefs": ["Background worker goroutine"],
        "crypto_xrefs": [],
        "time_xrefs": ["runtime.chanrecv2(ticker.C)", "time.Now", "time.Time.After(user.ExpiresAt)"],
        "map/mutex evidence": ["sync.RWMutex.RLock (UsersStore iteration)", "sync.Mutex.Lock (sessionMap token eviction for expired user)"],
        "strings": ["[User] Account %s expired, tokens revoked and sessions kicked"]
    },
    {
        "binary_symbol": "main.chIaMDTZ",
        "va": "0x73ae20",
        "file_offset": "0x33ae20",
        "size": 320,
        "semantic_role": "ADMIN_ROLE_CHECK",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE"],
        "route_xrefs": ["Called by admin endpoints after token lookup"],
        "crypto_xrefs": [],
        "time_xrefs": [],
        "map/mutex evidence": ["sync.RWMutex.RLock (UsersStore role check)"],
        "strings": ["Forbidden: admin only", "admin"]
    },
    {
        "binary_symbol": "main.jlRPqj8Kko_8",
        "va": "0x743c40",
        "file_offset": "0x343c40",
        "size": 1184,
        "semantic_role": "SESSION_KICK_HANDLER",
        "classification": "RECONSTRUCTED_FROM_BINARY",
        "confidence": "HIGH",
        "evidence_classes": ["INSTRUCTION_XREF", "STRING_CONSTANTS", "CALLER_CALLEE"],
        "route_xrefs": ["Called by main.cFpPBbFet.func1 on expired user and admin kick endpoints"],
        "crypto_xrefs": [],
        "time_xrefs": [],
        "map/mutex evidence": [],
        "strings": ["[Admin] Kicking session for user %s (Close conn)", "Forbidden: peer connection is closed"]
    }
]

# Enrich with callers and callees from function map & callgraph
for entry in auth_entries:
    va = entry['va']
    finfo = fmap.get(va, {})
    entry['callees'] = finfo.get('callees', [])
    entry['callers'] = callers_map.get(va, [])

out_dir = Path('evidence/go_signaling/auth')
out_dir.mkdir(parents=True, exist_ok=True)

with open(out_dir / 'AUTH_FUNCTION_MAP.json', 'w', encoding='utf-8') as f:
    json.dump({"metadata": {"binary": "webrtc-signaling", "total_auth_functions": len(auth_entries)}, "functions": auth_entries}, f, indent=2)

print(f"Generated {out_dir / 'AUTH_FUNCTION_MAP.json'} with {len(auth_entries)} functions")
