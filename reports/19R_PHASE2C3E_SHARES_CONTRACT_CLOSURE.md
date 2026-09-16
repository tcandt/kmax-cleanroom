# Forensic Report 19R: Phase 2C.3ER Shares Contract & Provenance Closure

**Status**: VERIFIED & CLOSED  
**Commit Target**: Phase 2C.3ER Remediation  
**Differential Verdict**: PASS (36/36 test cases, 100% pass rate)  
**Historical Regression Suite**: PASS (152/152 tests across Persistence, Auth Core, Auth HTTP, Devices, Users/Admin, Tags, Shares)  
**Cleanroom Scope Guard**: PASS (0 Shortcuts, 0 License, 0 WebSocket, 0 WebRTC violations)  

---

## 1. Executive Summary & Clarification of Previous Scope

In Phase 2C.3E, 28/28 differential test cases were initially verified. However, as noted in review:
- **Scope Clarification**: The previous 28/28 suite covered 28 implemented functional cases, but **omitted strict method-gating negative branches for `/api/share/extend` and `/api/share/update`**, as well as decode error responses on body-driven routes. Therefore, the earlier 28/28 could not be considered full endpoint parity.
- **Remediation Completed (Phase 2C.3ER)**:
  1. Implemented strict HTTP method gating (`405 Method Not Allowed\n`, `text/plain; charset=utf-8`) on `HandleShareExtend` and `HandleShareUpdate`.
  2. Aligned JSON body decode failure error responses across all 5 JSON-decoding endpoints (`create`, `extend`, `update`, `revoke`, `redeem_card`) to return bit-exact HTTP 400 with `Invalid payload\n`.
  3. Expanded the differential test suite from 28 to **36 cases**, covering all wrong-method combinations on `/extend`, `/update`, `/create`, and verifying method permissiveness on body-driven routes (`/list`, `/revoke`, `/redeem_card`, `/info`).
  4. Corrected route metadata in reports and documented errata.
  5. Remapped `SharesStore.Load()` provenance to `main.wRVYHLD_` (`0x7395c0`) and `generateShareToken()` to `BEHAVIOR_SLICE` of `main.cYYycnP3` (`0x75c7e0`–`0x75c867`).
  6. Made function slices query-derived from `ROUTE_HANDLER_MAP` and `FUNCTION_MAP`, separating `machine_observation` and `semantic_annotation`.
  7. Hardened persistence, expiry, and cross-contract evidence with machine-resolved instruction facts and structured dynamic test proofs (`CROSS-01`..`03`).
  8. Upgraded `reproduce_share_forensics.py` to independently verify **all 13 artifacts** (13/13 PASS).
  9. Hardened Master Verifier (`tools/verify_phase2.py` Section 12) with status checks, machine facts, and tightened scope guards covering exact out-of-scope routes.
  10. Reverted unrelated historical test churn to parent commit `f373d57`.

---

## 2. Real Method Mismatch Remediation & Differential Expansion

### 2.1 Method Gating Parity

Original oracle analysis confirmed that `/api/share/extend` and `/api/share/update` enforce strict POST-only behavior:
```text
GET     -> 405 Method Not Allowed\n (Content-Type: text/plain; charset=utf-8)
PUT     -> 405 Method Not Allowed\n
PATCH   -> 405 Method Not Allowed\n
DELETE  -> 405 Method Not Allowed\n
HEAD    -> 405 Method Not Allowed (empty body)
OPTIONS -> 200 OK (CORS headers)
POST    -> Body-dependent (400 on invalid/missing body, 200 on success)
```

In `pkg/httpapi/shares_handlers.go`, both `HandleShareExtend` and `HandleShareUpdate` were updated with exact method checks before body decoding:
```go
if r.Method != http.MethodPost {
    w.Header().Set("Content-Type", "text/plain; charset=utf-8")
    w.WriteHeader(http.StatusMethodNotAllowed)
    w.Write([]byte("Method Not Allowed\n"))
    return
}
```

### 2.2 Decode Failure Alignment

In the original binary, when JSON decoding of the request body fails (empty body, EOF, malformed JSON), all handlers return HTTP 400 with `Invalid payload\n`:
- `HandleShareCreate` (line 132)
- `HandleShareRevoke` (line 309)
- `HandleShareExtend` (line 377)
- `HandleShareUpdate` (line 458)
- `HandleShareRedeemCard` (line 598)

All 5 handlers were updated to check `err := json.NewDecoder(r.Body).Decode(&req); err != nil` and emit HTTP 400 with `Invalid payload\n`.

### 2.3 Expanded Differential Suite Results (36/36 PASS)

| Test ID | Name | Method & Route | Classification | Verdict |
|---|---|---|---|---|
| SHARE-HTTP-01 | Baseline List Shares Empty | GET /api/share/list | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-02 | Missing Token Rejection | Admin Endpoints | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-03 | Invalid Token Rejection | Admin Endpoints | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-04 | Normal User Forbidden | Admin Endpoints | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-05 | Create Share Minimal Schema & Token Format | POST /api/share/create | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-06 | Duplicate Share Creation Conflict (409) | POST /api/share/create | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-07 | Create Share Missing Device ID (400) | POST /api/share/create | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-08 | List Shares Populated & Schema Parity | GET /api/share/list | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-09 | List Shares ?device_id= Filtering | GET /api/share/list | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-10 | Public Info Query Valid Unprotected | GET /api/share/info | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-11 | Public Info Query Empty Token (400) | GET /api/share/info | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-12 | Public Info Query Invalid Token (404) | GET /api/share/info | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-13 | Public Info Password Challenge (Code 401) | GET /api/share/info | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-14 | Public Info Password Auth Success | GET /api/share/info | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-15 | Extend Permanent Share Rejection | POST /api/share/extend | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-16 | Extend Expiring Share Success | POST /api/share/extend | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-17 | Extend Error Validation Semantics | POST /api/share/extend | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-18 | Update Share Mutable Fields | POST /api/share/update | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-19 | Update Share Missing Token (400) | POST /api/share/update | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-20 | Redeem Card Valid Code (Public) | POST /api/share/redeem_card | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-21 | Redeem Card Invalid Code | POST /api/share/redeem_card | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-22 | Redeem Card Missing Code (400) | POST /api/share/redeem_card | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-23 | Revoke Share Success & Deletion | POST /api/share/revoke | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-24 | Revoke Share Missing / Unknown Token (404)| POST /api/share/revoke | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-25 | OPTIONS CORS Preflight Matrix (7 Routes) | OPTIONS all 7 routes | BIT_EXACT_MATCH | PASS |
| SHARE-HTTP-26 | No-Auth Mode Server Bypass | /api/share/* | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-27 | Persistence File Contract & Format | Disk check shares.json | STRUCTURAL_EXACT_MATCH | PASS |
| SHARE-HTTP-28 | Cross-Contract Isolation with /devices | GET /devices | BIT_EXACT_MATCH | PASS |
| **SHARE-HTTP-29** | **GET Method on /api/share/extend (405)** | GET /api/share/extend | **BIT_EXACT_MATCH** | **PASS** |
| **SHARE-HTTP-30** | **PUT/PATCH/DELETE on /extend (405)** | Non-POST on /extend | **BIT_EXACT_MATCH** | **PASS** |
| **SHARE-HTTP-31** | **HEAD Method on /api/share/extend (405)** | HEAD /api/share/extend | **BIT_EXACT_MATCH** | **PASS** |
| **SHARE-HTTP-32** | **GET Method on /api/share/update (405)** | GET /api/share/update | **BIT_EXACT_MATCH** | **PASS** |
| **SHARE-HTTP-33** | **PUT/PATCH/DELETE on /update (405)** | Non-POST on /update | **BIT_EXACT_MATCH** | **PASS** |
| **SHARE-HTTP-34** | **HEAD Method on /api/share/update (405)** | HEAD /api/share/update | **BIT_EXACT_MATCH** | **PASS** |
| **SHARE-HTTP-35** | **Non-POST Verbs on /api/share/create (405)**| Non-POST on /create | **BIT_EXACT_MATCH** | **PASS** |
| **SHARE-HTTP-36** | **Method Permissiveness on Non-Gating** | /list, /revoke, /redeem, /info | **STRUCTURAL_EXACT_MATCH** | **PASS** |

**Final Pass Rate**: `IMPLEMENTED_SHARE_CONTRACT_DIFFERENTIAL_PASS_RATE = 36/36` (100%).

---

## 3. Metadata Errata & Disassembly Provenance Corrections

### 3.1 Route Handler Metadata Errata

In the initial Phase 2C.3E narrative text, handler VAs for `/api/share/revoke` and `/api/share/redeem_card` were mistakenly copied from scratch probe addresses. The canonical ground truth in `evidence/go_signaling/ROUTE_HANDLER_MAP.json` and `evidence/go_signaling/shares/SHARE_ROUTE_FAMILY.json` is:

| Route Pattern | Canonical Symbol | Canonical VA | Canonical Size |
|---|---|---|---|
| `/api/share/revoke` | `main.nFuQn_o` | `0x75e5a0` | 2,176 bytes |
| `/api/share/redeem_card` | `main.iSjKlH94xCO` | `0x761a20` | 6,272 bytes |

Reconstructed source code in `pkg/httpapi/shares_handlers.go` was verified to already use these exact canonical symbols and VAs.

### 3.2 `SharesStore.Load()` Provenance Correction

- **Defect**: Previously mapped to `main.fomL4ATwVV1` (`0x739900`), which is `saveShares`.
- **Correction**: Verified via `FUNCTION_MAP.json` and disassembly that `main.wRVYHLD_` (VA `0x7395c0`, size 736 bytes) is the actual `loadShares` routine.
- **Reconstructed Mapping**: Updated `pkg/storage/shares_store.go`:
  ```go
  // CLEANROOM-PROVENANCE:
  // Classification: RECONSTRUCTED_FROM_BINARY
  // Binary Symbol: main.wRVYHLD_
  // VA: 0x7395c0
  // Evidence: shares.json load lifecycle, os.ReadFile, unmarshal into in-memory map
  // Confidence: HIGH
  func (s *SharesStore) Load() error
  ```

### 3.3 `generateShareToken()` Provenance Classification

- **Defect**: Previously mapped to `main.vT6rYK_v` (`0x739320`), which Auth forensics proved is `SESSION_CREATOR`.
- **Disassembly Trace**: In `main.cYYycnP3` (`0x75c240`), share token generation is implemented directly inline at `0x75c7e0`–`0x75c867`:
  - `0x75c7ea: call 0x52a5e0` (`crypto/rand.Read`, 16 random bytes)
  - `0x75c826`: hex encodes lowercase characters via byte lookup table at `0xcaaed`
  - `0x75c85b: call 0x4608a0` (`runtime.concatstring2` with prefix `"st_"`)
- **Reconstructed Mapping**: Updated `pkg/httpapi/shares_handlers.go`:
  ```go
  // CLEANROOM-PROVENANCE:
  // Classification: RECONSTRUCTED_FROM_BINARY
  // Mapping Scope: BEHAVIOR_SLICE
  // Binary Symbol: main.cYYycnP3
  // VA: 0x75c7e0
  // Evidence: inlined 16-byte random read, lowercase hex encoding, and st_ prefix concatenation (0x75c7e0-0x75c867)
  // Confidence: HIGH
  func generateShareToken() string
  ```

---

## 4. Hardened Evidence Artifacts

### 4.1 Persistence Machine Facts (`SHARE_PERSISTENCE_CONTRACT.json`)

Independent Capstone disassembly of `main.fomL4ATwVV1` (`0x739900`, 1664 bytes) resolved the exact machine instruction facts:
- `0x739bc9: call 0x533e80` (`json.MarshalIndent`, 2-space formatting)
- `0x739ca9: lea rdi, [rip + 0xe2368]` (references string `".tmp"` at `0x81c018`, length 4)
- `0x739cb5: call 0x4608a0` (`runtime.concatstring2`, constructs `<filePath>.tmp`)
- `0x739cd9: mov r8d, 0x180` (permission argument `0x180` = `0600` octal)
- `0x739ce0: call 0x4e0da0` (`os.WriteFile`)
- `0x739e12: call 0x4e1160` (`os.Rename`, atomic rename from `.tmp` to target file)

### 4.2 Expiry Machine Facts (`SHARE_EXPIRY_CONTRACT.json`)

- **Setup Symbol**: `main.dYBSRoVh` (`0x73a0a0`)
  - `0x73a0ae: movabs rax, 0x45d964b800` (sets ticker interval: `0x45d964b800` ns = 300 seconds = 5 minutes)
  - `0x73a0b8: call 0x4c9680` (`time.NewTicker`)
  - `0x73a0fa: call 0x44f9c0` (`runtime.newproc`, spawns cleanup goroutine)
- **Worker Symbol**: `main.dYBSRoVh.func1` (`0x73a120`, 992 bytes)
  - `0x73a180: call runtime.chanrecv2` (awaits ticker tick)
  - `0x73a1a2: call time.Now`
  - `0x73a1c0: call sync.(*Mutex).Lock`
  - `0x73a202: call runtime.mapIterStart`
  - `0x73a357: call time.Time.After` (checks `now.After(token.ExpiresAt)`)
  - `0x73a3b3, 0x73a3d8: call runtime.mapdelete_faststr` (removes expired tokens)
  - `0x73a220: call sync.(*Mutex).Unlock`
  - `0x73a248: call main.fomL4ATwVV1` (`saveShares`, persists cleaned state to disk)
- **Lazy Query Check**: `main.busbgD` (`0x760480`) verifies `now.Before(expires_at)` on `GET /api/share/info`.

### 4.3 Cross-Contract Structured Evidence (`SHARE_CROSS_CONTRACT.json`)

- **`CROSS-01`**: Deletion of user via `POST /api/admin/users/delete` leaves `shares.json` bit-identical. Callgraph proof: `main.d709Uf_4gI` (`0x742b80`) has 0 calls to share functions.
- **`CROSS-02`**: Deletion of device via `DELETE /api/devices/{id}` leaves `shares.json` bit-identical. Callgraph proof: `main.tP8uF9S8U7K` (`0x74da60`) has 0 calls to share functions.
- **`CROSS-03`**: `GET /devices` returns device entries without leaking any share tokens. Callgraph proof: `main.q601l9` (`0x74cf00`) has 0 references to `SharesStore`.

### 4.4 Query-Derived Function Slices (`SHARE_HTTP_FUNCTION_SLICES.json`)

All 11 function slices are query-derived from `ROUTE_HANDLER_MAP.json` and `FUNCTION_MAP.json` with strict separation of machine observations from semantic annotations:
- `symbol`: symbol name
- `machine_observation`: `start_va`, `size_bytes`, `end_va`, `instruction_count`, `machine_call_facts`, `string_xrefs`, `assembly_preview`
- `semantic_annotation`: `route`, `role_description`

---

## 5. True Forensic Reproducibility (13/13 Verified)

`tools/forensics/reproduce_share_forensics.py` was rewritten to independently regenerate and verify **all 13 artifacts**:
1. `SHARE_ROUTE_FAMILY.json`: PASS
2. `SHARE_TYPE_EVIDENCE.json`: PASS
3. `SHARE_ROUTE_METHOD_MATRIX.json`: PASS
4. `SHARE_AUTH_MATRIX.json`: PASS
5. `SHARE_CREATE_CONTRACT.json`: PASS
6. `SHARE_LIST_CONTRACT.json`: PASS
7. `SHARE_INFO_CONTRACT.json`: PASS
8. `SHARE_MUTATION_CONTRACTS.json`: PASS
9. `SHARE_REDEEM_CARD_CONTRACT.json`: PASS
10. `SHARE_PERSISTENCE_CONTRACT.json`: PASS
11. `SHARE_EXPIRY_CONTRACT.json`: PASS
12. `SHARE_CROSS_CONTRACT.json`: PASS
13. `SHARE_HTTP_FUNCTION_SLICES.json`: PASS

**Overall Tool Verdict**: `OVERALL REPRODUCIBILITY: PASS (13/13 artifacts verified)`.

---

## 6. Scope Isolation Guard & Historical Commit Cleanliness

### 6.1 Strict Cleanroom Scope Guard

`tools/verify_phase2.py` Check 12.10 enforces exact forbidden tokens:
- Exact routes: `/api/shortcuts`, `/api/activate`, `/api/license_status`, `/debug/license`, `/register_agent`, `/connect_client`
- Transport packages: `websocket.Upgrader`, `github.com/pion/webrtc`, `nhooyr.io/websocket`, `gorilla/websocket`

Audit across all Go files in `reconstructed_source/webrtc-signaling`: **0 violations found**.

### 6.2 Scope Hygiene

All unrelated historical files accidentally modified by previous test runs were restored to parent commit `f373d5766fd1bd24e017625dab671c717a077e0c`:
- `evidence/go_signaling/auth/AUTH_HEADER_PARSING_MATRIX.json`
- `evidence/go_signaling/auth/AUTH_HEADER_PARSING_MATRIX.md`
- `reports/08_PHASE2C2_AUTH_DIFFERENTIAL.md`
- `evidence/go_signaling/users/USER_ADMIN_HTTP_DIFFERENTIAL_RESULTS.json`
- `evidence/go_signaling/tags/TAG_HTTP_DIFFERENTIAL_RESULTS.json`

---

## 7. Exit Gate Checklist

| Gate Item | Status | Evidence |
|---|---|---|
| Extend wrong-method behavior matches original | PASS | SHARE-HTTP-29..31 (405 Method Not Allowed) |
| Update wrong-method behavior matches original | PASS | SHARE-HTTP-32..34 (405 Method Not Allowed) |
| Expanded Shares differential suite PASS | PASS | `IMPLEMENTED_SHARE_CONTRACT_DIFFERENTIAL_PASS_RATE = 36/36` |
| Canonical revoke/redeem handler metadata corrected | PASS | Report 19R Section 3.1 & `ROUTE_HANDLER_MAP.json` |
| `SharesStore.Load()` provenance corrected | PASS | Mapped to `main.wRVYHLD_` (`0x7395c0`) |
| `generateShareToken()` provenance corrected | PASS | `BEHAVIOR_SLICE` of `main.cYYycnP3` (`0x75c7e0`–`0x75c867`) |
| Function slices derive from `FUNCTION_MAP`/`CALLGRAPH` | PASS | Query-derived 11 slices in `SHARE_HTTP_FUNCTION_SLICES.json` |
| Persistence facts machine-resolved | PASS | Disassembly instructions at `0x739bc9`, `0x739ca9`, `0x739cd9`, `0x739ce0`, `0x739e12` |
| Expiry claims evidence-bound | PASS | Setup `0x73a0a0`, ticker `0x45d964b800` (300s), worker `0x73a120` |
| Cross-contract claims dynamically supported | PASS | `CROSS-01`..`03` tests PASS + callgraph proofs |
| Share reproducibility honestly verifies all 13 artifacts | PASS | `reproduce_share_forensics.py` PASS (13/13) |
| Master verifier checks method statuses & binary facts | PASS | `verify_phase2.py` Check 12.1–12.10 ALL PASS |
| Scope guard covers exact Shortcuts/License routes | PASS | 0 violations across reconstructed source |
| Unrelated volatile historical evidence reverted | PASS | Restored to `f373d57` |
| Persistence 8/8 PASS | PASS | `test_persistence_diff.py` PASS |
| Auth core 12/12 PASS | PASS | `test_auth_diff.py` PASS |
| Auth HTTP 18/18 PASS | PASS | `test_auth_http_diff.py` PASS |
| Devices 28/28 PASS | PASS | `test_devices_http_diff.py` PASS |
| Users/admin 30/30 PASS | PASS | `test_users_admin_http_diff.py` PASS |
| Tags 20/20 PASS | PASS | `test_tags_http_diff.py` PASS |
| Shares 36/36 PASS | PASS | `test_shares_http_diff.py` PASS |
| Go unit tests PASS | PASS | `go test ./...` PASS |
| Provenance auditor PASS | PASS | `verify_reconstructed_provenance.py` (110/110 functions PASS) |
| Master verifier PASS | PASS | `verify_phase2.py` OVERALL AUDIT VERDICT: PASS |
| Zero Shortcuts implementation | PASS | 0 occurrences |
| Zero License implementation | PASS | 0 occurrences |
| Zero production WebSocket | PASS | 0 occurrences |
| Zero WebRTC | PASS | 0 occurrences |

---

## 8. Conclusion

Phase 2C.3ER is formally **CLOSED**. All method-gating mismatches, provenance errors, report discrepancies, and verifier/reproducibility gaps are completely resolved. All cleanroom boundaries are preserved. The codebase is fully verified and ready for the next REST subsystem.
