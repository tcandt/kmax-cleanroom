# Forensic Password Verification Semantics (`PASSWORD_VERIFICATION.md`)

**Binary Symbol**: `main.biG96MFIwa` (`0x739060`)  
**Caller (Login)**: `main.ltOjwqsMl5q8` (`0x73dd00`, VA `0x73e28d`)  
**Caller (Bootstrap)**: `main.aOfaLG` (`0x736ae0`, VA `0x736db8`)  
**Classification**: `STATIC_AND_DYNAMIC_CONFIRMED`

---

## 1. Mathematical & Algorithmic Formula

The password hashing and verification algorithm in `webrtc-signaling` is:

$$\text{PasswordHash} = \text{hex\_lower}\Big(\text{SHA-256}\big(\text{password} \,\|\, \text{salt}\big)\Big)$$

### Direct Disassembly Evidence (`0x739060`)
```asm
  0x73907a: mov qword ptr [rsp + 0x118], rcx  ; salt pointer
  0x739082: mov qword ptr [rsp + 0x120], rdi  ; salt length
  0x73908a: mov qword ptr [rsp + 0x108], rax  ; password pointer
  0x739092: mov qword ptr [rsp + 0x110], rbx  ; password length
  ...
  0x7390d8: call 0x4ac380 ; crypto/sha256.(*digest).Reset
  0x739102: call 0x460de0 ; runtime.concatbyte2(password, salt)
  0x739115: call 0x4ac480 ; crypto/sha256.(*digest).Write
  0x739126: call 0x4ac740 ; crypto/sha256.(*digest).Sum
```

1. **Concatenation Order**: Strict `password + salt`. The password bytes appear first, immediately followed by the salt bytes.
2. **Byte-Level Encoding**: Raw UTF-8 bytes are passed directly into `runtime.concatbyte2`. There is no Unicode normalization (NFC/NFKD) and no trimming of the password string itself.
3. **Hex Representation**: The 32 raw bytes of the SHA-256 digest are encoded using an explicit 16-byte lookup table at VA `0x8271ab`:
   ```text
   30 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66 -> "0123456789abcdef"
   ```
   All hex digits are strictly **lowercase**.
4. **Length Invariant**: Output length is always exactly **64 ASCII characters**.

---

## 2. Login Verification & Comparison Mechanism

In `main.ltOjwqsMl5q8` (`0x73dd00`):
```asm
  0x73e28d: call 0x739060 ; main.biG96MFIwa(password, salt)
  0x73e292: cmp  qword ptr [rsp + 0x70], rbx ; compare computed len (64) with stored user.Password len
  0x73e297: jne  0x73e3bf ; mismatch -> return 401
  0x73e2a8: call 0x403600 ; runtime.memequal(computed_hash, stored_hash, 64)
  0x73e2ad: test al, al
  0x73e2af: je   0x73e3bf ; mismatch -> return 401
```

- **Comparison**: Exact length check followed by `runtime.memequal` on 64 bytes.
- **Timing Behavior**: Uses `runtime.memequal` (standard memory comparison), not `subtle.ConstantTimeCompare`.
- **Case Sensitivity**: Case-sensitive; uppercase hex hashes will fail verification because the computed hash is strictly lowercase hex.

---

## 3. Input Validation & Error Matrix

| Input Condition | Observed HTTP Status | Content-Type | Observed Response Body | Evidence Source |
|---|---|---|---|---|
| **Valid Password** | `200 OK` | `application/json` | `{"assigned_devices": [...], "role": "...", "token": "...", "username": "..."}` | Dynamic Oracle (`scratch/oracle_auth_probe_results.json`) |
| **Invalid Password** | `401 Unauthorized` | `text/plain; charset=utf-8` | `Invalid username or password\n` | Disassembly `0x73e3cf` & Dynamic Oracle |
| **Unknown Username** | `401 Unauthorized` | `text/plain; charset=utf-8` | `Invalid username or password\n` | Disassembly `0x73e42d` & Dynamic Oracle |
| **Empty Username (`""`)** | `400 Bad Request` | `text/plain; charset=utf-8` | `Username and password are required\n` | Disassembly `0x73e0c4` & Dynamic Oracle |
| **Empty Password (`""`)** | `400 Bad Request` | `text/plain; charset=utf-8` | `Username and password are required\n` | Disassembly `0x73e0c4` & Dynamic Oracle |
| **Missing Username Field** | `400 Bad Request` | `text/plain; charset=utf-8` | `Username and password are required\n` | Dynamic Oracle |
| **Missing Password Field** | `400 Bad Request` | `text/plain; charset=utf-8` | `Username and password are required\n` | Dynamic Oracle |
| **Malformed JSON** | `400 Bad Request` | `text/plain; charset=utf-8` | `Invalid JSON\n` | Disassembly `0x73e48d` & Dynamic Oracle |
| **Past `ExpiresAt` Account** | `403 Forbidden` | `text/plain; charset=utf-8` | `账号已到期，请联系管理员延时\n` | Disassembly `0x73e3fe` & Dynamic Oracle |
| **Future `ExpiresAt` Account** | `200 OK` | `application/json` | Success JSON response | Dynamic Oracle |

---

## 4. Implementation Deduplication Strategy

In Phase 2C.1, default admin credential initialization (`users.json`) required computing `SHA256(password + salt)`. That implementation exists in:
- `reconstructed_source/webrtc-signaling/pkg/storage/users_store.go` (`hashPassword`)

For Phase 2C.2, to satisfy the user mandate against duplicate password hashing logic:
1. Export `HashPassword(password, salt string) string` in `pkg/storage` (or a dedicated `pkg/auth` primitive imported by storage).
2. Use this identical verified function across both persistence bootstrapping and runtime authentication verification.
3. Preserve all 8 Phase 2C.1 differential tests and provenance metadata with zero regression.
