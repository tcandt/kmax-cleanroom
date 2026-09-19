# Report 13: Phase 2C.3B Device Registry & REST Differential Verification

## 1. Executive Summary

The Phase 2C.3B Device Registry REST differential test suite executed **14 automated test cases** comparing the original `webrtc-signaling` binary against the cleanroom reconstructed HTTP server.

- **Total Test Cases**: 14
- **Passed Cases**: 14
- **Failed Cases**: 0
- **Verdict**: **PASS (100% PARITY)**

---

## 2. Test Case Results Matrix

| Case ID | Test Name | Classification | Verdict | Comparison Summary |
|---|---|---|---|---|
| `DEV-HTTP-01` | Empty Registry Admin Query | `BIT_EXACT_MATCH` | **PASS** | Both emit 200 OK, application/json, exact body '[]\n' |
| `DEV-HTTP-02` | Populated Registry One Device | `STRUCTURAL_EXACT_MATCH` | **PASS** | Both emit 200 OK with matching 1-device JSON schema, online=true, client_count=0, and timestamps |
| `DEV-HTTP-03` | Populated Registry Multiple Devices | `NORMALIZED_JSON_MATCH` | **PASS** | Both contain exact 2 registered devices under non-deterministic map iteration order |
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
| `DEV-HTTP-14` | Route Identity & Deletion Lifecycle | `BIT_EXACT_MATCH` | **PASS** | Online delete rejected with 409, offline delete succeeds with 200 {'status':'deleted'}, GET /api/devices returns 405 |

---

## 3. Verified Parity Highlights

1. **Empty Registry Serialization**: Both servers emit exact byte sequence `[]\n` with `Content-Type: application/json`.
2. **Device Data Model**: Matching 7-field JSON schema (`device_id`, `device_info`, `online`, `first_seen`, `last_seen`, `client_count`, and omitempty `clients`).
3. **Assignment Filtering**: Admin sees all devices (`*`); assigned users see only their designated device; unassigned users receive `[]\n`.
4. **Lifecycle & Deletion**: Online devices cannot be deleted (`409 Conflict: Device is online, disconnect it first`); offline devices are successfully removed (`200 OK: {"status":"deleted"}`).
5. **CORS & Preflight**: Identical headers for `OPTIONS` (`Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET, OPTIONS`).
6. **Route Identity**: Conclusively verified that `/devices` is the list route and `/api/devices/` is the prefix deletion route.