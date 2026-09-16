# Report 12: Phase 2C.3B Device Registry & REST Forensics

## 1. Executive Summary & Forensic Gate Status

This report documents the exhaustive forensic extraction, static disassembly mapping, and dynamic oracle validation for the **Device Registry & REST layer** in `webrtc-signaling`. All investigations were completed prior to introducing any new source code in `reconstructed_source/`.

### Forensic Gate Checklist:
- [x] **/devices vs /api/devices resolved**: `/devices` is the registered REST endpoint (`main.i2EgUTaLmQs` @ `0x74cf80`) for listing devices. `/api/devices/` is a prefix handler (`main.rXQMyuE` @ `0x74da60`) specifically for deleting individual devices (`DELETE /api/devices/{deviceId}`). Requests to `/api/devices` (without trailing slash) are routed to `/api/devices/` by Go's ServeMux and return `405 Method not allowed` on GET. The frontend (`web-app/src/stores/devices.js:233`) calls `GET /devices` directly for listing and `DELETE /api/devices/${deviceId}` for deletion.
- [x] **All device REST routes enumerated**: Structured in `DEVICE_ROUTE_FAMILY.json`.
- [x] **Empty-registry response known**: Verified bit-exact response is status `200 OK`, `Content-Type: application/json`, body `[]\n` (SHA-256: `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`).
- [x] **Populated-registry response known**: Verified multi-device structure, field names, types, timestamp formats, and online status transitions recorded in `DEVICE_POPULATED_REGISTRY_CONTRACT.json`.
- [x] **Device JSON schema recovered**: Decoded directly from binary type descriptors (`0x7ff0e0` for `DeviceDTO`, `0x805760` for `DeviceEntry`), mapped in `DEVICE_TYPE_EVIDENCE.json`.
- [x] **Auth visibility matrix recovered**: Verified in `DEVICE_VISIBILITY_AUTH_MATRIX.json` (Admin sees all; User sees assigned; User with `*` sees all; User unassigned sees `[]`).
- [x] **Registry lifecycle behavior observed**: Recorded in `DEVICE_REGISTRY_LIFECYCLE_MATRIX.json` across connection, disconnection, reconnection, online deletion rejection (409 Conflict), and offline deletion success (200 OK `{"status":"deleted"}`).
- [x] **Ordering semantics classified**: Map iteration order (`runtime.mapIterStart` / `runtime.mapIterNext`), non-deterministic list order.
- [x] **Handler VA slices mapped**: Recorded in `DEVICE_HTTP_FUNCTION_SLICES.json`.
- [x] **Pre-flight disassembly errata PASS**: Verified in `reports/11R3R_ERRATA.md` and audit pass.

**GATE STATUS: PASS — Proceed to Cleanroom Source Implementation.**

---

## 2. Route Identity Reconciliation (`DEVICE_ROUTE_IDENTITY_MATRIX.json`)

The apparent discrepancy between frontend machine extraction (`/api/devices`) and binary route mapping (`/devices`) has been conclusively resolved by comparing `ROUTE_HANDLER_MAP.json`, binary disassembly, and dynamic probing:

| Route | Registration Call VA | Handler Symbol | Handler VA | Supported Verbs | Purpose / Semantic Role |
|---|---|---|---|---|---|
| `/devices` | `0x765c58` | `main.i2EgUTaLmQs` | `0x74cf80` | `GET`, `OPTIONS` | Device registry list filtered by user assignment |
| `/api/devices/` | `0x765c70` | `main.rXQMyuE` | `0x74da60` | `DELETE`, `OPTIONS` | Delete individual offline device (`DELETE /api/devices/{id}`) |
| `/api/devices` | None (handled via `/api/devices/`) | `main.rXQMyuE` | `0x74da60` | `OPTIONS`, `DELETE` (400 if ID empty) | Prefix subtree fallback; returns 405 on GET |
| `/devices/` | None | Mux catch-all | `0x748c20` | `GET` (404 Not Found) | Not registered |

In the public frontend (`web-app/src/stores/devices.js`):
- Line 233: `const res = await fetch('/devices')` -> exact call to `/devices` to list devices.
- Line 795: `await fetch(`/api/devices/${encodeURIComponent(deviceId)}`, { method: 'DELETE', ... })` -> exact call to `/api/devices/{deviceId}` to delete device.

Binary routing and frontend implementation are in complete parity.

---

## 3. Data Model Recovery (`DEVICE_TYPE_EVIDENCE.json`)

The data model was recovered by parsing Go type descriptors in `.rodata`:

### 3.1 Public DTO Struct (`0x7ff0e0`, Size: 120 bytes)
| Field Name (Obfuscated) | JSON Tag | Type | Offset | Notes |
|---|---|---|---|---|
| `NOnUogldoZjn` | `device_id` | `string` | `0x0` | Device identifier |
| `Yq4QMsuW` | `device_info` | `interface{}` | `0x10` | Arbitrary device metadata map (brand, model, sdk) |
| `HkLpT8` | `online` | `bool` | `0x20` | True if WebSocket agent is currently connected |
| `AzWfQXm6` | `first_seen` | `time.Time` | `0x28` | Timestamp when device was first registered |
| `A1BCftA3Oo` | `last_seen` | `time.Time` | `0x40` | Timestamp of last heartbeat or connection activity |
| `ZAfO5Ejq6l6` | `client_count` | `int` | `0x58` | Number of active web clients viewing this device |
| `TEZwlSS` | `clients,omitempty` | `[]interface{}` | `0x60` | Omitted from JSON output when nil/empty |

### 3.2 Internal Registry Struct (`0x805760`, Size: 128 bytes)
Stored in global map `map[string]*DeviceEntry`:
- Protected by global registry RWMutex (`0xbee020`) and per-device RWMutex at offset `0x68`.
- Contains active WebSocket connection pointer at offset `0x20`, connected clients map at `0x28`, and online status flag at `0x35`.

---

## 4. Authorization & Assignment Filtering (`DEVICE_VISIBILITY_AUTH_MATRIX.json`)

Binary disassembly of `main.pVOasuBli` (`0x73d8a0`) reveals the exact device filtering rules:

1. **Unauthenticated / Missing / Invalid Token**:
   - `main.lYKp_Iuf` fails -> `401 Unauthorized`.
2. **Admin Role (`role == "admin"`)**:
   - Checked at `0x73da25`-`0x73da48`. Returns `true` immediately; admin sees all devices in registry.
3. **Normal User (`role != "admin"`)**:
   - Iterates user's `assigned_devices` slice (`0x73dc49`-`0x73dcac`):
     - If any entry is `"*"`: returns `true` (wildcard assignment sees all devices).
     - If entry matches current device's `device_id`: returns `true` (device is visible).
     - If slice exhausted with no match: returns `false` (device is omitted from list).
4. **Share Token Authentication (`user` starts with `"share:"`)**:
   - Looks up share token; if matching `device_id`, device is visible.

---

## 5. Deletion & Lifecycle Semantics

Binary disassembly of `main.rXQMyuE` (`0x74da60`) and dynamic testing reveal:
- **Method Restriction**: Only `DELETE` and `OPTIONS` are supported. Any other method returns `405 Method not allowed\n`.
- **Role Restriction**: Requires `admin` role. Non-admin users receive `403 Forbidden\n`.
- **Target Extraction**: Extracts `deviceId` by trimming `/api/devices/` prefix. If empty, returns `400 Invalid device id\n`.
- **Existence Check**: Looks up device in registry map. If absent, returns `404 Device not found\n`.
- **Online Guard**: Checks `device.online`. If `online == true`, returns `409 Conflict` with body `Device is online, disconnect it first\n`.
- **Offline Deletion**: If `online == false`, removes entry from global map and returns `200 OK` with body `{"status":"deleted"}`.
