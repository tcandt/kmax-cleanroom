# Report 16: Phase 2C.3D Device Tags REST Forensics

## 1. Executive Summary & Forensic Gate Verdict

- **Phase**: 2C.3D — Device Tags REST Forensic Recovery
- **Status**: **FORENSIC_GATE_PASS**
- **Target Route**: `/api/tags` (single unified endpoint for tag management and device mappings)
- **Registration**: Registered in `main.main` (VA `0x7647a0`) via `http.HandleFunc` at call VA `0x76596c` with closure VA `0x8484e0` and handler VA `0x76d200` (`main.main.func2`)
- **Direct Project Callees Identified & Mapped**:
  - `main.bFT5Enmzua` (VA `0x769d40`, size 1632B): GET handler (lists tags and device mappings, formats JSON response)
  - `main.k7fAFNISQp_m` (VA `0x76a4c0`, size 5056B): POST handler (unmarshals `main.Svdju9`, filters by caller role, mutates in-memory tags, invokes persistence)
  - `main.rCajRnfJZ` (VA `0x737da0`, size 608B): `saveDeviceTags` persistence routine
  - `main.pVOasuBli` (VA `0x73d8a0`, size 1120B): device authorization access check
  - `main.gevbuZQhJ` (VA `0x76ba00`, size 1216B): builds response tags map and slice
- **Evidence Artifacts Committed**: 8 machine-derived JSON artifacts in `evidence/go_signaling/tags/`
- **Forensic Reproducibility**: `tools/forensics/reproduce_tag_forensics.py` verified **PASS**

---

## 2. Forensic Resolution of the 4 User Directives

### Directive 1: Candidate Operations Discovery & Classification

In accordance with cleanroom protocol, tag operations were probed without assuming prior existence.

| Candidate Operation | Classification | Mechanism & Wire Semantics | Discrete Endpoint Status |
|---|---|---|---|
| `list tags` | **`CONFIRMED_OPERATION`** | `GET /api/tags` returns HTTP 200 with schema `{"tags": [...], "deviceTags": {...}}` | N/A (Standard GET) |
| `create/add tag` | **`CONFIRMED_OPERATION`** | Declarative state addition via `POST /api/tags`: providing a new tag object in `tags` appends it | Discrete `/api/tags/add` is **`NOT_PRESENT`** (404) |
| `update/rename tag` | **`CONFIRMED_OPERATION`** | Declarative state update via `POST /api/tags`: providing an existing tag `id` updates `name` and `color` | Discrete `/api/tags/update` is **`NOT_PRESENT`** (404) |
| `delete tag` | **`CONFIRMED_OPERATION`** | Declarative state removal via `POST /api/tags`: admin omitting a tag removes it from `tags` slice | Discrete `/api/tags/delete` is **`NOT_PRESENT`** (404); `DELETE /api/tags` returns GET 200 |
| `assign tag(s) to device` | **`CONFIRMED_OPERATION`** | Declarative mapping via `POST /api/tags`: setting `deviceTags[dev_id] = [tag_ids]` | Discrete `/api/tags/assign` is **`NOT_PRESENT`** (404) |
| `remove tag(s) from device` | **`CONFIRMED_OPERATION`** | Declarative removal via `POST /api/tags`: setting `deviceTags[dev_id] = []` | Discrete `/api/tags/remove` is **`NOT_PRESENT`** (404) |

> [!IMPORTANT]
> All 7 candidate discrete REST endpoints (`/api/tags/add`, `/api/tags/delete`, `/api/tags/update`, `/api/tags/assign`, `/api/tags/remove`, `GET /api/tag`, `POST /api/tag`) were probed against the original signaling server and returned **`404 page not found\n`**. The original binary does not expose separate CRUD routes; all tag operations are mediated solely through `GET /api/tags` and `POST /api/tags`.

---

### Directive 2: Recovered Storage & Persistence Contract

Disassembly of `main.rCajRnfJZ` (VA `0x737da0`) and its callee `uOfWpGI3.ZkONNWV` (VA `0x4e0da0`) directly recovered the physical write contract:

1. **File Path**: `device_tags.json` inside the server's data directory.
2. **File Mode**: `0644` octal (`0x1a4`).
   - Disassembly Anchor: `0x737f15: mov r8d, 0x1a4`.
3. **Write Mechanism**: **Direct `os.WriteFile`** (`O_WRONLY | O_CREATE | O_TRUNC = 0x241`).
   - Disassembly Anchor: `0x4e0dc6: mov ecx, 0x241; call 0x4e0420 (os.OpenFile)`.
   - **Zero Atomic Temp File**: Unlike `users.json` (which uses atomic `.tmp + rename`), `device_tags.json` performs **direct truncation and write**. Reconstructed code will faithfully adhere to direct `os.WriteFile`.
4. **JSON Serialization**: Pretty-printed with 2-space indentation via `json.MarshalIndent(v, "", "  ")`.
   - Disassembly Anchor: `0x737e3f: mov r8d, 2; lea rsi, [rip + "  "]; call 0x533e80 (json.MarshalIndent)`.
5. **Missing File Default**: When `device_tags.json` is absent on startup, the server initializes an empty in-memory state and `GET /api/tags` emits `{"tags":[],"deviceTags":{}}\n`.

---

### Directive 3: Caller Closure vs Callee Architecture

The entry handler `main.main.func2` (VA `0x76d200`, 704 bytes) is an outer router/closure registered on ServeMux pattern `/api/tags`:
- Sets CORS response headers:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Headers: Content-Type, Authorization`
  - `Access-Control-Allow-Methods: GET, OPTIONS` (on GET) / `POST, OPTIONS` (on POST)
- Dispatches method:
  - `OPTIONS` -> 200 OK with empty body.
  - `POST` -> delegates to `main.k7fAFNISQp_m` (VA `0x76a4c0`).
  - All other verbs (`GET`, `PUT`, `DELETE`, `PATCH`, `HEAD`) -> delegates to `main.bFT5Enmzua` (VA `0x769d40`).

#### Direct Project Callee Semantics
1. **`main.bFT5Enmzua` (GET Handler, 0x769d40, 1632B)**:
   - Validates session token via `main.lYKp_Iuf` (0x73b080).
   - Extracts current in-memory tags list and deviceTags map.
   - Marshals to JSON and writes HTTP 200.
2. **`main.k7fAFNISQp_m` (POST Handler, 0x76a4c0, 5056B)**:
   - Validates session token via `main.lYKp_Iuf` (0x73b080).
   - Decodes JSON body into `*main.Svdju9` (tags + deviceTags) via `json.Unmarshal` (0x52db00). Returns `400 Invalid JSON\n` on syntax error.
   - Evaluates caller role:
     - **Admin (`role == "admin"`)**: Performs full replacement of `tags` slice and `deviceTags` map.
     - **Non-Admin (`role == "user"`)**:
       - Merges `tags`: updates existing tags by ID in place; appends new tags to slice.
       - Iterates `req.DeviceTags`: calls `main.pVOasuBli` (0x73d8a0) to verify if the caller is assigned to that device. Only updates assigned devices; ignores unauthorized/unassigned devices; preserves existing tags of other devices.
   - Calls `main.rCajRnfJZ` (0x737da0) to persist to `device_tags.json`.
   - Emits HTTP 200 `{"status":"success"}\n`.

---

### Directive 4: Pre-Flight Users/Admin Verification

All Pre-Flight Refinements A, B, C, D on Phase 2C.3C were completed and validated:
- Pre-flight A: `USER_ADMIN_ROUTE_FAMILY.json` dynamically derived from `ROUTE_HANDLER_MAP.json`.
- Pre-flight B: `USER_ADMIN_FUNCTION_SLICES.json` bounds derived from `FUNCTION_MAP.json`.
- Pre-flight C: `DIVERGENCE-USER-01` documented in `USER_INTENTIONAL_DIVERGENCES.json`, tested via `USER-DIVERGENCE-01`, pass rate denominator preserved at 30/30.
- Pre-flight D: Field-aware normalization and password hash invariant verified.
- `tools/verify_phase2.py` updated and passed.

---

## 3. ELF Go Runtime Type Descriptors

Directly parsed from `.rodata` and type tables of the canonical Linux AMD64 binary:

### 1. `Tag` Struct (`main.UeyzO4kumc`)
- **Descriptor VA**: `0x7e25a0`
- **Size**: 48 bytes (0x30)
- **Kind**: 25 (Struct)
- **Field Count**: 3
- **Fields**:
  - Offset 0 (16B): `id` (`string`, type VA `0x79e2c0`)
  - Offset 16 (16B): `name` (`string`, type VA `0x79e2c0`)
  - Offset 32 (16B): `color` (`string`, type VA `0x79e2c0`)

### 2. `DeviceTagsConfig` DTO (`main.Svdju9`)
- **Descriptor VA**: `0x7d6f80`
- **Size**: 32 bytes (0x20)
- **Kind**: 25 (Struct)
- **Field Count**: 2
- **Fields**:
  - Offset 0 (24B): `tags` (`[]main.UeyzO4kumc`, slice type VA `0x7969a0`)
  - Offset 24 (8B): `deviceTags` (`map[string][]string`, map type VA `0x7bf9c0`)

---

## 4. Route Method & Authorization Matrices

### Method Matrix on `/api/tags`
| Verb | Status | Content-Type | CORS Origin | Allowed Methods Header | Note |
|---|---|---|---|---|---|
| `GET` | 200 | `application/json` | `*` | `GET, OPTIONS` | Lists tags & device mappings |
| `POST` | 400 (empty) / 200 (valid) | `text/plain` (400) / `application/json` (200) | `*` | `POST, OPTIONS` | Mutates tags & device mappings |
| `PUT` | 200 | `application/json` | `*` | `GET, OPTIONS` | Routed by closure to GET handler |
| `PATCH` | 200 | `application/json` | `*` | `GET, OPTIONS` | Routed by closure to GET handler |
| `DELETE` | 200 | `application/json` | `*` | `GET, OPTIONS` | Routed by closure to GET handler |
| `HEAD` | 200 | `application/json` | `*` | `GET, OPTIONS` | 0 body bytes |
| `OPTIONS` | 200 | None | `*` | Injected by closure | 0 body bytes |

### Auth Matrix
| Method | ADMIN | NORMAL_USER | MISSING_TOKEN | INVALID_TOKEN | NO_AUTH_MODE |
|---|---|---|---|---|---|
| `GET /api/tags` | 200 | 200 | 401 (`Unauthorized\n`) | 401 (`Unauthorized\n`) | 200 |
| `POST /api/tags` | 200 (Full Replace) | 200 (Scoped Merge) | 401 (`Unauthorized\n`) | 401 (`Unauthorized\n`) | 200 (Acts as Admin) |

---

## 5. Cleanroom Reconstruction Blueprint

Now that the forensic gate has formally passed, cleanroom source reconstruction can proceed:
1. `pkg/storage/tags_store.go`:
   - Holds `TagsStore` managing `tags []Tag` and `deviceTags map[string][]string` guarded by `sync.RWMutex`.
   - Persistence implements direct `os.WriteFile(path, data, 0644)` formatted with `json.MarshalIndent(..., "", "  ")`.
   - Mutation logic mirrors `main.k7fAFNISQp_m`: admin full replace vs non-admin scoped merge.
2. `pkg/httpapi/tags_handlers.go`:
   - Implements `ServeHTTP` router matching `main.main.func2`: CORS headers, OPTIONS preflight, POST delegation, GET/fallback delegation.
   - Enforces session token extraction (Header `Bearer` or Cookie `token`).
3. Registration in `server.go`:
   - Registered at `/api/tags` on `http.ServeMux`.
