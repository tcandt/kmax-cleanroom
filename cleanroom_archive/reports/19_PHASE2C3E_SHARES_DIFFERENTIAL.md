# Report 19: Phase 2C.3E Device Shares REST Differential Verification

## 1. Executive Summary

The Phase 2C.3E Device Shares REST differential test suite executed **28 automated differential test cases** directly comparing the original `webrtc-signaling.exe` canonical binary against the cleanroom reconstructed HTTP server.

- **Total Test Cases Executed**: 28
- **Passed Cases**: 28
- **Failed Cases**: 0
- **Metric**: **`IMPLEMENTED_SHARE_CONTRACT_DIFFERENTIAL_PASS_RATE = 28/28`**
- **Cleanroom Provenance**: All reconstructed functions in `pkg/types/share.go`, `pkg/storage/shares_store.go`, and `pkg/httpapi/shares_handlers.go` are annotated with strict provenance headers and verified against canonical ELF disassemblies and runtime struct type descriptors.
- **Scope Boundary Compliance**: STRICT PASS (0 Shortcuts `/api/shortcuts/*`, 0 License checks `/api/license/*`, 0 WebSocket signaling `/register_agent` / `/connect_client`, 0 WebRTC protocols).

---

## 2. Test Case Results Matrix

| Test ID | Test Name | Classification | Result | Wire & Behavioral Parity Description |
|---|---|---|---|---|
| `SHARE-HTTP-01` | Baseline List Shares Empty | `BIT_EXACT_MATCH` | **PASS** | Both return 200 OK `{"code":0,"data":[],"msg":"success"}\n` on empty initial shares state. |
| `SHARE-HTTP-02` | Missing Token Rejection on Admin Endpoints | `BIT_EXACT_MATCH` | **PASS** | Both return 401 Unauthorized `Unauthorized\n` on `/create`, `/list`, `/revoke`, `/extend`, `/update` when Authorization header is absent. |
| `SHARE-HTTP-03` | Invalid Token Rejection on Admin Endpoints | `BIT_EXACT_MATCH` | **PASS** | Both return 401 Unauthorized `Unauthorized\n` when an invalid bearer token is provided. |
| `SHARE-HTTP-04` | Normal User Forbidden on Admin Endpoints | `BIT_EXACT_MATCH` | **PASS** | Both return 403 Forbidden `Forbidden: admin only\n` when accessed by a non-admin user. |
| `SHARE-HTTP-05` | Create Share Minimal Schema & Token Format | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both generate `token` with `st_` prefix + 32 lowercase hex chars, and `card_code` formatted as `CP-XXXX-XXXX`. |
| `SHARE-HTTP-06` | Duplicate Share Creation Conflict (409) | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both return 409 Conflict with formatted message indicating existing active share with card code. |
| `SHARE-HTTP-07` | Create Share Missing Device ID (400) | `BIT_EXACT_MATCH` | **PASS** | Both return 400 Bad Request `device_id is required\n` on missing device_id. |
| `SHARE-HTTP-08` | List Shares Populated & Key Schema Parity | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both return JSON array of active shares with exact 19-key schema including `active_connections: 0`. |
| `SHARE-HTTP-09` | List Shares ?device_id= Filtering | `BIT_EXACT_MATCH` | **PASS** | Both filter active shares strictly matching the requested `?device_id=` query parameter. |
| `SHARE-HTTP-10` | Public Info Query Valid Unprotected Share | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both allow unauthenticated query via `/api/share/info?token=...`, returning full share details with device status. |
| `SHARE-HTTP-11` | Public Info Query Empty Token (400) | `BIT_EXACT_MATCH` | **PASS** | Both return 400 Bad Request `token is required\n` when token query parameter is absent. |
| `SHARE-HTTP-12` | Public Info Query Invalid Token (404) | `BIT_EXACT_MATCH` | **PASS** | Both return 404 Not Found `Share not found\n` on unknown or revoked tokens. |
| `SHARE-HTTP-13` | Public Info Password Challenge (Code 401) | `BIT_EXACT_MATCH` | **PASS** | Both return HTTP 200 `{"code":401,"data":{"require_password":true},"msg":"该分享需要访问密码"}\n` when password is missing/wrong. |
| `SHARE-HTTP-14` | Public Info Password Authentication Success | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both return HTTP 200 with code 0 and full share info when correct password parameter is provided. |
| `SHARE-HTTP-15` | Extend Permanent Share Rejection | `BIT_EXACT_MATCH` | **PASS** | Both return HTTP 200 `{"code":400,"msg":"永久有效的分享无需延时"}\n` when attempting to extend a permanent share. |
| `SHARE-HTTP-16` | Extend Expiring Share Success | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both extend expiration timestamp by requested seconds and return updated `expires_at`. |
| `SHARE-HTTP-17` | Extend Error Validation Semantics | `BIT_EXACT_MATCH` | **PASS** | Both return 400 `token is required\n` on empty token, and 404 `Share token not found\n` on nonexistent token. |
| `SHARE-HTTP-18` | Update Share Mutable Fields | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both mutate exactly `forbid_audio`, `forbid_bitrate`, `forbid_fps`, `forbid_resolution`, and `guest_settings` (struct 0x7f9640). |
| `SHARE-HTTP-19` | Update Share Missing Token (400) | `BIT_EXACT_MATCH` | **PASS** | Both return 400 Bad Request `token is required\n` when token is empty on update. |
| `SHARE-HTTP-20` | Redeem Card Valid Code (Public Access) | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both allow unauthenticated card redemption via `POST /api/share/redeem_card`, returning the associated share token. |
| `SHARE-HTTP-21` | Redeem Card Invalid Code | `BIT_EXACT_MATCH` | **PASS** | Both return HTTP 200 `{"code":404,"msg":"卡密不存在或已失效"}\n` when the card code does not exist. |
| `SHARE-HTTP-22` | Redeem Card Missing Code (400) | `BIT_EXACT_MATCH` | **PASS** | Both return 400 Bad Request `card_code is required\n` when card_code is empty. |
| `SHARE-HTTP-23` | Revoke Share Success & Deletion | `BIT_EXACT_MATCH` | **PASS** | Both return HTTP 200 `{"code":0,"msg":"success"}\n` and delete the share entry from active state and disk. |
| `SHARE-HTTP-24` | Revoke Share Missing / Unknown Token (404) | `BIT_EXACT_MATCH` | **PASS** | Both return 404 Not Found `Share token not found\n` on missing, unknown, or already-revoked tokens. |
| `SHARE-HTTP-25` | OPTIONS CORS Preflight Matrix (7 Routes) | `BIT_EXACT_MATCH` | **PASS** | All 7 routes return 200 OK with `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Headers`, and methods. |
| `SHARE-HTTP-26` | No-Auth Mode Server Bypass | `STRUCTURAL_EXACT_MATCH` | **PASS** | In `-no-auth` mode, both allow unauthenticated access to admin endpoints, treating callers as admin. |
| `SHARE-HTTP-27` | Persistence File Contract & Disk Format | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both write `shares.json` using atomic temporary file `.tmp` + `os.Rename`, mode `0600` (`0x180`), and 2-space indentation. |
| `SHARE-HTTP-28` | Cross-Contract Isolation with /devices | `BIT_EXACT_MATCH` | **PASS** | Both isolate share state from `/devices` registry; share creation/revocation does not alter device metadata fields. |

---

## 3. Discovered Behavioral Highlights & Machine Analysis

1. **Exact Role & Auth Partitioning**:
   - Admin-only routes (`POST /create`, `GET /list`, `POST /revoke`, `POST /extend`, `POST /update`): Enforce strict admin role checking in authenticated mode. Non-admin callers receive HTTP 403 `Forbidden: admin only\n`. Missing tokens receive HTTP 401 `Unauthorized\n`.
   - Public/Guest routes (`GET /api/share/info`, `POST /api/share/redeem_card`): Fully accessible without any Authorization header.
2. **Type Recovery & Layout Verification**:
   - `ShareToken` struct at VA `0x80f700` (`*main.IopTpsqKRhA`): Size 192 bytes, 18 fields.
   - `UpdateShareRequest` struct at VA `0x7f9640`: Size 24 bytes, 6 fields (`token`, `forbid_bitrate`, `forbid_fps`, `forbid_resolution`, `forbid_audio`, `guest_settings`).
   - Fields such as `allow_clipboard` and `description` are NOT decoded or updated in `/api/share/update`, which preserves exact wire parity with the original binary.
3. **Cryptographic & Token Semantics**:
   - Share Token ID: `"st_"` + 32 lowercase hex characters generated from 16 bytes of cryptographically secure random bytes (`crypto/rand`).
   - Card Code: `"CP-%s-%s"` where each 4-character chunk is chosen uniformly from the Crockford base32 alphabet at VA `0x8312b7`: `"23456789ABCDEFGHJKLMNPQRSTUVWXYZ"`.
   - Share Password: Plain SHA256 hex digest (64 chars) without salt, verified against `password_hash` stored in memory and on disk.
4. **Persistence Architecture (`shares.json`)**:
   - File permissions: Mode `0600` (`0x180` octal confirmed in disassembly at `0x739cd9: mov r8d, 0x180`).
   - Mechanism: Atomic write via temporary file `shares.json.tmp` followed by `os.Rename` (`0x4e1160`).
   - Format: JSON array with 2-space indentation (`json.MarshalIndent(v, "", "  ")`).
5. **Background Reaper Lifecycle**:
   - Reaper goroutine spawned at `0x73a120` (`main.dYBSRoVh.func1`) periodically purges expired shares and flushes updated state to `shares.json`.
6. **Device Uniqueness Constraint**:
   - Each device may have at most 1 active share. Attempting to create a second share for a device returns HTTP 409 Conflict with message `"该设备已存在活跃分享（卡密 %s），请先撤销或对其延时"`.

---

## 4. Full Regression Verification

Across the complete cleanroom verification suite:
- **Phase 2C.1 Persistence Differential**: 8/8 PASS
- **Phase 2C.2 Auth Differential**: 12/12 PASS
- **Phase 2C.3 Auth HTTP Differential**: 18/18 PASS
- **Phase 2C.3BR Device Registry Differential**: 28/28 PASS
- **Phase 2C.3C Users & Admin Differential**: 30/30 PASS
- **Phase 2C.3D Device Tags Differential**: 20/20 PASS
- **Phase 2C.3E Device Shares Differential**: 28/28 PASS
- **Total Differential Test Cases Passing**: **144 / 144**
- **Cleanroom Go Unit Tests (`go test ./...`)**: PASS
- **Provenance Auditor (`tools/verify_reconstructed_provenance.py`)**: 110/110 functions PASS
- **Master Verifier (`tools/verify_phase2.py`)**: Section 12 PASS
