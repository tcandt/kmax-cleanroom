# Forensic Report 27R: Phase 2C.3IR Files, Tasks, Downloads & Snapshots True Reproducibility & Contract Coverage Closure

**Phase**: 2C.3IR  
**Status**: COMPLETE & PASS  
**Auditor**: Cleanroom Reverse Engineering Specialist  
**Artifacts Generated**: 21/21 True Reproducible  
**Forensic Gate**: 18/18 Evaluated Non-Tautological Invariants PASS  
**Differential Coverage**: 93/93 Side-by-Side Cases PASS (67/67 Historical + 26/26 Remediation)  
**Cumulative Verification Suite**: 380/380 Canonical Differential Cases PASS  
**Target Binary**: `webrtc-signaling` (Linux AMD64 SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Secondary Binary**: `webrtc-signaling.exe` (Windows AMD64)  

---

## 1. Executive Summary

Phase 2C.3IR successfully achieves full remediation and true forensic closure for the **Files, Tasks, Downloads, and Snapshots** REST route family (`/upload`, `/api/files`, `/api/tasks`, `/api/tasks/details`, `/downloads/`, `/snapshots/`).

All requirements established in the remediation mandate have been executed and verified:
1. **Zero Transport Leakage**: Zero implementations of `/register_device`, `/register_agent`, `/connect_client`, WebSockets, WebRTC, or SPA `/`.
2. **HR3 True Forensic Reproducibility (21/21)**: All 21 canonical evidence artifacts are generated into an isolated temporary directory with `canonical_input_used: false` and validated via deep semantic comparison against committed targets.
3. **Machine Derivation**: Task descriptors (`TaskCreateRequest`, `Task`, `DeviceTaskStatus`) derived via Capstone dataflow traversal of `runtime.newobject` in `main.koVbnsD4T0d`. Function slices derived via query of `ROUTE_HANDLER_MAP.json` and `FUNCTION_MAP.json`. Zero authoritative hardcoded tables.
4. **Non-Tautological Gate (18/18)**: All gate invariants evaluate real machine/oracle evidence; zero hardcoded `true` invariants.
5. **Snapshots Directory Startup Parity Resolved**: Reconstructed server eagerly creates empty directory `data/snapshots` on startup matching oracle lifecycle, while snapshot JPEG bytes remain strictly in-memory (0 disk files).
6. **Hardened JSON Differential Comparator**: Deep field-by-field validation of Task creation and Task details DTOs without blind masking of objects containing `task_id`.
7. **Expanded Differential Suite (93/93)**: 67/67 historical cases preserved under hardened comparator + 26/26 remediation cases covering access isolation, exact file sorting fixtures with `check_body=True`, Range/Content-Range/Last-Modified/CORS delivery, and an expanded path security matrix.

---

## 2. Technical Evidence & Audit Matrix

### Item A: Scope Boundary Enforcement
- **Audited Endpoints**: Exactly 6 REST endpoints:
  - `/upload`: Dual contract (`UPLOAD_STANDARD_FILE` vs `UPLOAD_SNAPSHOT_INGEST`)
  - `/api/files`: File listing (GET) and file deletion (DELETE)
  - `/api/tasks`: Batch task creation (POST)
  - `/api/tasks/details`: Batch task status query (GET)
  - `/downloads/`: Static file delivery
  - `/snapshots/`: In-memory screen capture delivery
- **Excluded Endpoints**: Reconstructed server codebase contains zero definitions, routes, or references for `/register_device`, `/register_agent`, `/connect_client`, WebSockets (`gorilla/websocket`, `nhooyr.io/websocket`), WebRTC (`pion/webrtc`), or root SPA `/`.

### Item B: HR3 True Forensic Reproducibility (21/21)
`tools/forensics/reproduce_files_tasks_forensics.py` was executed in isolated temporary workspace:
- Generated all 21 artifacts into `scratch/reproduce_files_tasks_forensics/<uuid>/`
- Policy enforced: `canonical_input_used: false` across all 21 items
- Validated via deep semantic comparison against `evidence/go_signaling/files_tasks/`:
  - `FILES_TASKS_ROUTE_FAMILY.json`: Semantic equality PASS
  - `FILES_TASKS_METHOD_MATRIX.json`: Semantic equality PASS
  - `FILES_TASKS_AUTH_MATRIX.json`: Semantic equality PASS
  - `FILESYSTEM_ROOT_CONTRACT.json`: Semantic equality PASS
  - `UPLOAD_REQUEST_TYPE_EVIDENCE.json`: Semantic equality PASS
  - `UPLOAD_OPERATION_CONTRACT.json`: Semantic equality PASS
  - `FILE_PATH_SECURITY_CONTRACT.json`: Semantic equality PASS
  - `FILES_TYPE_EVIDENCE.json`: Semantic equality PASS
  - `FILES_LIST_CONTRACT.json`: Semantic equality PASS
  - `DOWNLOADS_STATIC_CONTRACT.json`: Semantic equality PASS
  - `SNAPSHOTS_STATIC_CONTRACT.json`: Semantic equality PASS
  - `TASK_TYPE_EVIDENCE.json`: Semantic equality PASS
  - `TASKS_OPERATION_CONTRACT.json`: Semantic equality PASS
  - `TASK_DETAILS_CONTRACT.json`: Semantic equality PASS
  - `TASK_LIFECYCLE_CONTRACT.json`: Semantic equality PASS
  - `TASK_ID_CONTRACT.json`: Semantic equality PASS
  - `FILES_TASKS_PERSISTENCE_CONTRACT.json`: Semantic equality PASS
  - `FILES_TASKS_CROSS_CONTRACT.json`: Semantic equality PASS
  - `FILES_TASKS_EDGE_MATRIX.json`: Semantic equality PASS
  - `FILES_TASKS_FUNCTION_SLICES.json`: Semantic equality PASS
  - `FILES_TASKS_FORENSIC_GATE_RESULT.json`: Semantic equality PASS
- Manifest result: **`FILES_TASKS_FORENSIC_REPRODUCIBILITY = 21/21`**

### Item C: Machine Derivation of Descriptors & Function Slices
- **Task Descriptors Derived via Capstone**:
  - Traversal of `main.koVbnsD4T0d` (0x75afa0) locating `runtime.newobject` calls:
    - Call at `0x75b2c9`: `0x7ea980` -> `TaskCreateRequest` (72B, 4 fields: `type`, `targets`, `payload`, `dest_path`)
    - Call at `0x75b432`: `0x7fb3c0` -> `Task` `*main.Jh0XQJ` (88B, 6 fields: `task_id`, `type`, `payload`, `dest_path,omitempty`, `created_at`, `devices`)
    - Call at `0x75b795`: `0x7f4be0` -> `DeviceTaskStatus` `*main.ZFJczDtV4TR` (72B, 5 fields: `device_id`, `status`, `progress`, `result`, `updated_at`)
- **Function Slices Derived via Map Queries**:
  - Slices for `main.swqKgLrjAZT9`, `main.qa3RvDW`, `main.koVbnsD4T0d`, `main.koVbnsD4T0d.func1`, `main.g0bIYv` derived by looking up start VA and size in `ROUTE_HANDLER_MAP.json` and `FUNCTION_MAP.json`.

### Item D: Hard Evaluated Forensic Gate (18/18)
`FILES_TASKS_FORENSIC_GATE_RESULT.json` evaluates non-tautological evidence:
1. `all_6_routes_derived_from_route_map`: Evaluated against `ROUTE_HANDLER_MAP.json` (PASS)
2. `wrapper_business_functions_identified`: Machine-located symbols in `FUNCTION_MAP.json` (PASS)
3. `7_verb_matrix_complete`: All 7 HTTP verbs probed across routes (PASS)
4. `auth_matrix_complete`: Roles probed dynamically (PASS)
5. `filesystem_roots_proven`: Oracle probes confirm `data/downloads` and `data/snapshots` (PASS)
6. `upload_wire_contract_proven`: Dynamic probes confirm split behavior (PASS)
7. `path_containment_behavior_classified`: Directory stripping via `filepath.Base` confirmed (PASS)
8. `api_files_schema_recovered`: Live JSON schema matching (PASS)
9. `downloads_delivery_semantics_recovered`: HTTP static server delivery confirmed (PASS)
10. `snapshots_delivery_semantics_recovered`: Live JPEG delivery confirmed (PASS)
11. `task_dtos_recovered`: Capstone machine recovery confirmed (PASS)
12. `api_tasks_operations_classified`: Shell/install/push/pull classification (PASS)
13. `api_tasks_details_selector_recovered`: Query param `task_id` parsed (PASS)
14. `task_lifecycle_classified`: Offline failure vs online transport deferral (PASS)
15. `persistence_no_persistence_proven`: Restart probes prove reset to 404 (PASS)
16. `cross_contract_edges_evidence_bound`: Graph edges between routes validated (PASS)
17. `all_unresolved_transport_dependencies_deferred`: Scope isolation verified (PASS)
18. `total_canonical_artifacts_accounted`: 21 artifacts verified (PASS)
- Gate Verdict: **PASS (18/18)**

### Item E: Snapshots Directory Startup Parity vs In-Memory Data Storage
- **Observed Oracle Lifecycle**:
  - Prior to startup: `data/snapshots` does not exist.
  - On startup: binary executes `os.MkdirAll("data/snapshots", 0755)`, creating an empty directory.
  - During operation: uploaded snapshots are stored in memory (`sync.Map`). Zero files are created in `data/snapshots`.
  - On restart: `data/snapshots` directory remains present and empty on disk, while memory store resets (404 Not Found).
- **Cleanroom Implementation**:
  - `cmd/http-server/main.go` executes `os.MkdirAll(filepath.Join(*dataDir, "snapshots"), 0755)` on startup.
  - `storage.SnapshotManager` stores snapshot JPEG bytes strictly in memory.
  - Verified in differential test group 13 (`FT-DIFF-92`, `FT-DIFF-93`).

### Item F: Hardened Differential JSON Comparator
Replaced simplistic masking with strict structural and semantic comparison:
- **Task Creation (`POST /api/tasks`)**:
  - Exact keys: `{"status", "task_id"}`
  - Status value: `"success"`
  - Normalized validation: `re.match(r"^task_\d{14}_[0-9a-f]{16}$", task_id)` on both orig and recon.
- **Task Details (`GET /api/tasks/details?task_id=...`)**:
  - Exact keys: `{"task_id", "type", "payload", "dest_path", "created_at", "devices"}`
  - Fields compared: `type`, `payload`, `dest_path`
  - Timestamps validated: `created_at` parses as valid RFC3339 timestamp in both.
  - Device map keys: exact match
  - Device entry properties: `device_id`, `status` (`failed`), `progress` (`0`), `result` (`Device offline`), `updated_at` (RFC3339 parsed).
  - Zero blind skipping of objects.

### Item G: Task Details Access Isolation
Probes on a real created task across all 6 authentication contexts:
| Context | Oracle Status | Cleanroom Status | Result |
|---|---|---|---|
| `ADMIN` | 200 OK | 200 OK | Full Task DTO returned |
| `NORMAL_USER_ASSIGNED` | 200 OK | 200 OK | Full Task DTO returned (Global Authenticated Read) |
| `NORMAL_USER_UNASSIGNED` | 200 OK | 200 OK | Full Task DTO returned (Global Authenticated Read) |
| `MISSING_TOKEN` | 401 Unauthorized | 401 Unauthorized | Access denied |
| `INVALID_TOKEN` | 401 Unauthorized | 401 Unauthorized | Access denied |
| `NO_AUTH_MODE` | 200 OK | 200 OK | Full Task DTO returned |
- Rule: **`AUTHENTICATED_GLOBAL_READ`** (Task status details are visible to any authenticated user).

### Item H: File List Exact Fixture Contract (`check_body=True`)
Tested with controlled fixture tree on both servers:
- Files: `B.txt` (3B), `a.txt` (3B), `empty.txt` (0B), `spaced file.txt` (6B), `unicode_viet.txt` (7B), `sub/nested.txt` (inside subfolder).
- Mtime: Controlled identical mtimes set on disk (`1700000000`).
- Comparison Results:
  - Exact item count: 5 (subdirectory `sub` and `sub/nested.txt` excluded).
  - Sorting: ASCII byte order (`B.txt` precedes `a.txt`).
  - Schema: Exact `{"name", "size", "updated_at", "url"}` keys.
  - Empty file: Size 0 correctly reported.
  - Mtime: Exact ISO 8601 string match with timezone (`2023-11-15T05:13:20+07:00`).

### Item I: Static Downloads Headers & Range Delivery
Tested side-by-side against `spaced file.txt`:
- `GET existing`: 200 OK, `Accept-Ranges: bytes`, `Last-Modified`, `Content-Length: 6`, `Access-Control-Allow-Origin: *`, exact payload.
- `HEAD existing`: 200 OK, identical headers, empty body.
- `Range: bytes=0-3`: 206 Partial Content, `Content-Range: bytes 0-3/6`, `Content-Length: 4`, body `b"spac"`.
- `Range: bytes=2-`: 206 Partial Content, `Content-Range: bytes 2-5/6`, `Content-Length: 4`, body `b"aced"`.
- `Invalid Range`: 416 Range Not Satisfiable, `Content-Range: bytes */6`, body `"invalid range: failed to overlap\n"`.
- `Directory without slash`: 301 Moved Permanently, `Location: sub/`.
- `Unicode filename`: 200 OK, matching bytes.
- `Zero-byte file`: 200 OK, `Content-Length: 0`, empty body.

### Item J: Expanded Path Security Matrix
- **Upload (`POST /upload?name=...`)**:
  - `dir/file.txt`: 200 OK, saves to `downloads/file.txt` (stripped to `filepath.Base`).
  - `./file2.txt`: 200 OK, saves to `downloads/file2.txt`.
  - `../file3.txt`: 200 OK, saves to `downloads/file3.txt`.
  - `a/../file4.txt`: 200 OK, saves to `downloads/file4.txt`.
  - `.leading`: 200 OK, saves to `downloads/.leading`.
  - `C:\test\win.txt`: 200 OK, saves to `downloads/win.txt`.
  - `/etc/passwd`: 200 OK, saves to `downloads/passwd`.
  - `.`: 400 Bad Request (`"Invalid file name\n"`).
  - `..`: 400 Bad Request (`"Invalid file path (path traversal detected)\n"`).
- **Delete (`DELETE /api/files?name=...`)**:
  - `DELETE ?name=.`: Original binary attempts `os.Remove("downloads")`, returning 500 error (`The directory is not empty`). Cleanroom server safely returns 404 Not Found (path base matches `.` or empty). Classified as **`INTENTIONAL_SECURITY_DIVERGENCE`** (cleanroom prevents accidental root deletion).

### Item K: Task ID Generation Internals
- **Generator Symbol**: `main.g0bIYv` (VA `0x75a1e0`, 224 bytes).
- **Format String**: `task_%s_%x` (VA `0x82229b`).
- **Timestamp Layout**: `20060102150405` (VA `0x825bda`, 14 digits).
- **Entropy Source**: `crypto/rand.Read` of 8 bytes -> formatted as 16 lowercase hex characters.
- **Regex Format**: `^task_\d{14}_[0-9a-f]{16}$`.

### Item L: Online Task Transport Branch Adapter Boundary
In `reconstructed_source/webrtc-signaling/pkg/storage/tasks_store.go`:
- Offline dispatch branch: Fully implemented and differential-verified (immediate device status `"failed"`, progress `0`, result `"Device offline"`).
- Online dispatch branch: Formally deferred to Phase 2C.4 Transport Phase with explicit adapter comment:
  ```go
  // OFFLINE_BRANCH = IMPLEMENTED_AND_DIFFERENTIAL_VERIFIED
  // ONLINE_DISPATCH = DEFERRED_TO_TRANSPORT_PHASE
  ```

### Item M: Observation Provenance & Contract Generation
All 21 artifacts contain provenance headers documenting:
- Static binary inputs (`webrtc-signaling` ELF, `webrtc-signaling.exe` PE).
- Machine derivation tools (`tools/forensics/generate_files_tasks_forensics.py`).
- Dynamic oracle observation ports.
- Zero reliance on pre-committed canonical evidence as generator input.

### Item N: Master Verifier Hardening
`tools/verify_phase2.py` section 16 re-evaluates all underlying facts:
- Route handler symbol and VA boundary in `ROUTE_HANDLER_MAP.json` and `FUNCTION_MAP.json`.
- `reproduce_files_tasks_forensics.py` execution returncode == 0 and 21/21 verified.
- `FILES_TASKS_FORENSIC_GATE_RESULT.json` 18/18 non-tautological boolean evaluation.
- `TASK_TYPE_EVIDENCE.json` derivation method `INSTRUCTION_DISASSEMBLY_NEWOBJECT_TRAVERSAL`.
- `FILESYSTEM_ROOT_CONTRACT.json` snapshot directory lifecycle `EAGER_EMPTY_DIR_ON_STARTUP` and storage `IN_MEMORY_MAP`.
- `TASK_DETAILS_CONTRACT.json` rule `AUTHENTICATED_GLOBAL_READ`.
- `FILES_TASKS_HTTP_DIFFERENTIAL_RESULTS.json` count >= 90 with Range, access isolation, and directory parity verified.

### Item O: Differential Results & Dynamic Cumulative Denominator
- **Phase 2C.3I Suite**:
  - Historical Cases: **67/67 PASSED** (under hardened deep comparator)
  - Remediation Cases: **26/26 PASSED** (access isolation, fixtures, Range, path security, snapshot startup parity)
  - Total Files/Tasks Cases: **93/93 PASSED** (100%)
- **Cumulative Master Differential Suite**:
  - Auth CLI: 21/21
  - Auth HTTP: 16/16
  - Device HTTP: 29/29
  - User Admin HTTP: 30/30
  - Tags HTTP: 20/20
  - Shares HTTP: 36/36
  - Shortcuts HTTP: 19/19
  - Server Config HTTP: 55/55
  - License HTTP: 61/61
  - Persistence HTTP: 0/0 (integrated)
  - Files & Tasks HTTP: 93/93
  - **TOTAL CUMULATIVE DIFFERENTIAL PASS RATE**: **380/380 (100% PASS)**

---

## 3. Exit Gate Compliance Checklist

| Exit Gate Requirement | Target | Achieved | Verdict |
|---|---|---|---|
| True canonical-vs-regenerated reproducibility | 21/21 | 21/21 | **PASS** |
| Zero canonical evidence copying | Strict | Zero copying | **PASS** |
| Machine derivation of Task descriptors | Capstone | 0x7ea980, 0x7fb3c0, 0x7f4be0 | **PASS** |
| Function boundaries machine-derived | Map Query | ROUTE_HANDLER_MAP & FUNCTION_MAP | **PASS** |
| Non-tautological gate invariants | 18/18 | 18/18 Evaluated | **PASS** |
| Snapshot directory startup parity | Parity | `data/snapshots` eager empty dir | **PASS** |
| Snapshot data in-memory only | 0 disk files | In-memory sync.Map (0 disk files) | **PASS** |
| Full Task JSON semantic comparison | Hardened | Status, keys, DTO, regex task_id | **PASS** |
| Task details access isolation proven | Matrix | AUTHENTICATED_GLOBAL_READ | **PASS** |
| File list exact contract proven | `check_body=True` | Count 5, ASCII sort, mtime match | **PASS** |
| Downloads Range / Last-Modified parity | 200/206/416 | Exact headers & byte ranges | **PASS** |
| Expanded path security matrix | Probed | 8 upload + 1 intentional divergence | **PASS** |
| Task ID internals machine-derived | Disassembly | `main.g0bIYv`, `task_%s_%x`, layout `20060102150405` | **PASS** |
| Online task transport branch deferred | Explicit | Clean adapter comment & boundary | **PASS** |
| Historical differential pass rate preserved | 67/67 | 67/67 PASSED | **PASS** |
| Remediation differential pass rate | 26/26 | 26/26 PASSED | **PASS** |
| Expanded Files/Tasks differential pass rate | 93/93 | 93/93 PASSED | **PASS** |
| License differential pass rate preserved | 61/61 | 61/61 PASSED | **PASS** |
| Cumulative differential pass rate | Dynamic | 380/380 PASSED | **PASS** |
| Go unit test suite | All packages | 100% PASS | **PASS** |
| Master verifier (`verify_phase2.py`) | All checks | OVERALL AUDIT VERDICT: PASS | **PASS** |
| Zero /register_device implementation | 0 tokens | Zero | **PASS** |
| Zero /register_agent implementation | 0 tokens | Zero | **PASS** |
| Zero /connect_client implementation | 0 tokens | Zero | **PASS** |
| Zero production WebSockets | 0 packages | Zero | **PASS** |
| Zero WebRTC | 0 packages | Zero | **PASS** |
| Root SPA / untouched | Untouched | Untouched | **PASS** |

---

## 4. Final Verdict

**OVERALL PHASE 2C.3IR VERDICT**: **PASS (TRUE FORENSIC CLOSURE ACHIEVED)**  
The Files, Tasks, Downloads, and Snapshots REST route family is 100% verified, independently reproducible, and structurally isolated from transport implementations.
