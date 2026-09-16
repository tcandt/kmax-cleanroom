# Report 13: Phase 2C.3B Device Registry & REST Differential Verification

## 1. Executive Summary

The Phase 2C.3BR Device Registry REST differential test suite executed **28 automated test cases** comparing the original `webrtc-signaling` binary against the cleanroom reconstructed HTTP server.

- **Total Test Cases**: 28
- **Passed Cases**: 28
- **Failed Cases**: 0
- **Contract Pass Rate**: **`IMPLEMENTED_DEVICE_CONTRACT_DIFFERENTIAL_PASS_RATE = 28/28`**

---

## 2. Test Case Results Matrix

| Case ID | Test Name | Classification | Verdict | Comparison Summary |
|---|---|---|---|---|
| `DEV-HTTP-01` | Empty Registry Admin Query | `BIT_EXACT_MATCH` | **PASS** | Both emit 200 OK, application/json, exact body '[]\n' |
| `DEV-HTTP-02` | Populated Registry One Device Schema & Invariants | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit 200 OK with matching 7-field schema, deep equal device_info, and valid RFC3339 timestamp invariants |
| `DEV-HTTP-03` | Populated Registry Multiple Devices Normalized DTO | `NORMALIZED_JSON_MATCH` | **PASS** | Both contain identical normalized DTOs for 2 devices under non-deterministic Go map iteration order |
| `DEV-HTTP-04` | Invalid Token Rejection | `BIT_EXACT_MATCH` | **PASS** | Both reject invalid token with 401 Unauthorized |
| `DEV-HTTP-05` | Missing Token Rejection | `BIT_EXACT_MATCH` | **PASS** | Both reject unauthenticated request with 401 Unauthorized |
| `DEV-HTTP-06` | Normal User Assigned Device Filtering | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both filter devices to only the assigned device dev-alpha-001 |
| `DEV-HTTP-07` | Normal User Unassigned Visibility | `BIT_EXACT_MATCH` | **PASS** | Both emit empty array '[]\n' for unassigned normal user |
| `DEV-HTTP-08` | Reconnected Device State Restoration | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both restore online=true when existing device reconnects |
| `DEV-HTTP-09` | Disconnect Lifecycle & Offline State | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both retain disconnected device in registry with online=false while active device remains online=true |
| `DEV-HTTP-10` | Wrong Method (GET) on /api/devices/{id} | `BIT_EXACT_MATCH` | **PASS** | Both reject non-DELETE request with 405 Method not allowed |
| `DEV-HTTP-11` | HEAD Method on /devices | `BIT_EXACT_MATCH` | **PASS** | Both return 200 OK with empty body and Content-Type: application/json for HEAD |
| `DEV-HTTP-12` | OPTIONS Preflight CORS Headers | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit 200 OK with Access-Control-Allow-Origin: * and Access-Control-Allow-Methods: GET, OPTIONS |
| `DEV-HTTP-13` | Content-Type and Raw JSON Shape | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit Content-Type: application/json with trailing newline delimiter |
| `DEV-HTTP-14` | Online & Offline Deletion Lifecycle | `BIT_EXACT_MATCH` | **PASS** | Online delete rejected with 409, offline delete succeeds with 200 {'status':'deleted'}\n |
| `DEV-HTTP-15` | POST Method on /devices | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both serve device list with 200 OK on POST /devices (matching lack of method check in binary) |
| `DEV-HTTP-16` | PUT Method on /devices | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both serve device list with 200 OK on PUT /devices (matching lack of method check in binary) |
| `DEV-HTTP-17` | PATCH Method on /devices | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both serve device list with 200 OK on PATCH /devices (matching lack of method check in binary) |
| `DEV-HTTP-18` | DELETE Method on /devices | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both serve device list with 200 OK on DELETE /devices (matching lack of method check in binary) |
| `DEV-HTTP-19` | DELETE Device as Normal Assigned User Rejection | `BIT_EXACT_MATCH` | **PASS** | Both reject non-admin delete with 403 Forbidden |
| `DEV-HTTP-20` | DELETE Device as Normal Unassigned User Rejection | `BIT_EXACT_MATCH` | **PASS** | Both reject unassigned user delete with 403 Forbidden |
| `DEV-HTTP-21` | DELETE with Missing Token Rejection | `BIT_EXACT_MATCH` | **PASS** | Both reject unauthenticated delete with 401 Unauthorized |
| `DEV-HTTP-22` | DELETE with Invalid Token Rejection | `BIT_EXACT_MATCH` | **PASS** | Both reject invalid token delete with 401 Unauthorized |
| `DEV-HTTP-23` | DELETE Nonexistent Device ID | `BIT_EXACT_MATCH` | **PASS** | Both return 404 Device not found for nonexistent device |
| `DEV-HTTP-24` | DELETE Empty Device ID on /api/devices/ | `BIT_EXACT_MATCH` | **PASS** | Both return 400 Invalid device id for empty path parameter |
| `DEV-HTTP-25` | OPTIONS on Delete Route /api/devices/{id} | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both return 200 OK with Access-Control-Allow-Methods: DELETE, OPTIONS |
| `DEV-HTTP-26` | HEAD on Delete Route /api/devices/{id} | `BIT_EXACT_MATCH` | **PASS** | Both reject HEAD request on delete handler with 405 Method not allowed |
| `DEV-HTTP-27` | ServeMux Trailing Slash Redirect Semantics | `BIT_EXACT_MATCH` | **PASS** | Both return 301 Moved Permanently with Location: /api/devices/ when trailing slash is omitted |
| `DEV-HTTP-28` | No-Auth Server Mode Unauthenticated Query | `BIT_EXACT_MATCH` | **PASS** | Both serve device list without token and report noAuth: true when started with -no-auth |

---

## 3. Verified Parity Highlights

1. **Empty Registry Serialization**: Both servers emit exact byte sequence `[]\n` with `Content-Type: application/json`.
2. **Device Data Model**: Matching 7-field JSON schema (`device_id`, `device_info`, `online`, `first_seen`, `last_seen`, `client_count`, and omitempty `clients`), field types, deep equality, and RFC3339 timestamp invariants (`first_seen <= last_seen`).
3. **Assignment Filtering**: Admin sees all devices (`*`); assigned users see only their designated device; unassigned users receive `[]\n`.
4. **Lifecycle & Deletion**: Online devices cannot be deleted (`409 Conflict: Device is online, disconnect it first\n`); offline devices are successfully removed (`200 OK: {"status":"deleted"}\n`).
5. **CORS & Preflight**: Identical headers for `OPTIONS` across listing and delete routes.
6. **ServeMux Redirect Semantics**: With redirects disabled, `/api/devices` returns `301 Moved Permanently` with `Location: /api/devices/`.
7. **Delete Route Contract Closure**: All error branches verified (401 missing/invalid token, 403 non-admin, 404 nonexistent ID, 400 empty ID, 405 wrong method/HEAD).
8. **No-Auth Server Mode**: Both servers operate unauthenticated when launched with `-no-auth`.