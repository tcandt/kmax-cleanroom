# Forensic Report 27: Phase 2C.3I Files / Tasks / Downloads / Snapshots REST Reconstruction

**Status**: VERIFIED & AUDITED (Master Verifier Section 16: PASS)  
**Target Binary**: `webrtc-signaling` (Linux AMD64 SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Cleanroom Package**: `pkg/types`, `pkg/storage`, `pkg/httpapi`  
**Cumulative Verification**: **354/354 PASS (100%)** across all 11 canonical differential suites  
**Phase 2C.3I Differential Result**: **67/67 PASS (100%)**

---

## 1. Executive Summary

Phase 2C.3I reconstructs the full REST route family for files, tasks, static downloads, and in-memory snapshots:
- `/upload` (call `0x765c88`, handler `main.swqKgLrjAZT9` @ `0x758c80`)
- `/api/files` (call `0x765ca0`, handler `main.qa3RvDW` @ `0x75a2c0`)
- `/api/tasks` (call `0x765cb8`, handler `main.koVbnsD4T0d` @ `0x75afa0`)
- `/api/tasks/details` (call `0x765cd0`, handler `main.bhMId7t5J` @ `0x763ec0`)
- `/downloads/` (call `0x765d6b`, handler `Y0caeZ_zze.MB_aa9i.ServeHTTP` @ `0x6e0340`)
- `/snapshots/` (call `0x765d83`, handler `main.main.func5` @ `0x76da00`)

Reconstruction conformed to the rigorous cleanroom guidelines and user review amendments:
1. **Scope Boundary**: Exactly 6 endpoints. Zero production WebSocket/WebRTC packages, zero transport dependencies.
2. **Dual `/upload` Protocol**: Cleanly segmented into Standard File Upload (`POST /upload?name=...`, admin RBAC, raw stream to `data/downloads/`, path traversal check) vs Snapshot Ingest (`POST /upload?type=snapshot&device_id=...`, unauthenticated, in-memory map).
3. **True In-Memory Snapshots**: Verified that snapshots reside strictly in memory (`SnapshotManager`), leaving 0 on-disk snapshot directories.
4. **Task Type Recovery & Deferred Transport**: Directly recovered 3 Go runtime struct descriptors from ELF `.rodata` (`0x7ea980`, `0x7fb3c0`, `0x7f4be0`), implemented offline target immediate marking (`Device offline`), and deferred online dispatch to the transport phase (`ONLINE_DISPATCH_TRANSPORT_DEPENDENT`).
5. **Dynamic Denominator Audit**: Fully integrated into master verifier `tools/verify_phase2.py`, auditing dynamically:
   - Previous Total: 287/287
   - Phase 2C.3I Total: 67/67
   - Cumulative Total: 354/354 (100% across all 11 canonical suites).

---

## 2. Route Family & Static Function Correlation

All 6 endpoints were confirmed via `ROUTE_HANDLER_MAP.json`, ELF disassembly, and function slice analysis:

| Route Pattern | Registration Type | Call VA | Handler Symbol | Handler VA | Size (B) | Access / RBAC |
|---|---|---|---|---|---|---|
| `/upload` | `HandleFunc` | `0x765c88` | `main.swqKgLrjAZT9` | `0x758c80` | 5376 | Split: Admin-only for files, Unauthenticated for snapshots |
| `/api/files` | `HandleFunc` | `0x765ca0` | `main.qa3RvDW` | `0x75a2c0` | 3200 | Authenticated (Admin + User); GET / DELETE |
| `/api/tasks` | `HandleFunc` | `0x765cb8` | `main.koVbnsD4T0d` | `0x75afa0` | 4000 | Admin-only RBAC; POST |
| `/api/tasks/details` | `HandleFunc` | `0x765cd0` | `main.bhMId7t5J` | `0x763ec0` | 1600 | Authenticated (Admin + User); GET |
| `/downloads/` | `Handle` | `0x765d6b` | `Y0caeZ_zze.MB_aa9i.ServeHTTP` | `0x6e0340` | 96 | Static file server wrapped in CORS / StripPrefix |
| `/snapshots/` | `HandleFunc` | `0x765d83` | `main.main.func5` | `0x76da00` | 1536 | Authenticated + Device RBAC; GET / HEAD |

---

## 3. Go Runtime Type Recovery & Provenance

### 3.1 Direct Type Recovery (`DIRECT_TYPE_RECOVERY`)
All 3 task-related structures were recovered directly from Go runtime ELF type descriptors in `.rodata`:

1. `TaskCreateRequest` (VA `0x7ea980`, 72 bytes):
```go
type TaskCreateRequest struct {
    Type     string   `json:"type"`
    Targets  []string `json:"targets"`
    Payload  string   `json:"payload"`
    DestPath string   `json:"dest_path"`
}
```

2. `Task` (VA `0x7fb3c0`, 88 bytes, symbol `*main.Jh0XQJ`):
```go
type Task struct {
    TaskID    string                       `json:"task_id"`
    Type      string                       `json:"type"`
    Payload   string                       `json:"payload"`
    DestPath  string                       `json:"dest_path,omitempty"`
    CreatedAt string                       `json:"created_at"`
    Devices   map[string]*DeviceTaskStatus `json:"devices"`
}
```

3. `DeviceTaskStatus` (VA `0x7f4be0`, 72 bytes, symbol `*main.ZFJczDtV4TR`):
```go
type DeviceTaskStatus struct {
    DeviceID  string `json:"device_id"`
    Status    string `json:"status"`
    Progress  int    `json:"progress"`
    Result    string `json:"result"`
    UpdatedAt string `json:"updated_at"`
}
```

### 3.2 Generated Wire Model (`GENERATED_WIRE_MODEL`)
`/api/files` item wire projection constructed from dynamic reflection:
```go
type FileItem struct {
    Name      string `json:"name"`
    Size      int64  `json:"size"`
    UpdatedAt string `json:"updated_at"`
    URL       string `json:"url"`
}
```

---

## 4. Reconstructed Source Architecture

Reconstructed code is structured cleanly across 3 packages with complete cleanroom provenance headers:

1. `pkg/types/files_tasks.go`:
   - Contains `TaskCreateRequest`, `Task`, `DeviceTaskStatus`, `FileItem`, and error response models.
2. `pkg/storage/files_store.go`:
   - `FileManager`: Manages `data/downloads/` directory. Provides safe streamed file saving, directory listing sorted lexicographically, and deletion.
   - Enforces path traversal security: rejects filenames containing `".."`, `"."`, or invalid separators.
3. `pkg/storage/tasks_store.go`:
   - `TaskManager`: Thread-safe in-memory task map. Generates task IDs with format `task_YYYYMMDDhhmmss_<hex16>` (matching `0x825bda` and `0x82229b`).
   - Marks offline devices immediately with `"Device offline"` and status `"failed"`.
   - `SnapshotManager`: Thread-safe in-memory map storing snapshot byte slices keyed by device ID.
4. `pkg/httpapi/files_tasks_handlers.go`:
   - `HandleUpload`: Implements the dual `/upload` protocol (snapshot ingest vs standard file upload).
   - `HandleFiles`: Lists and deletes files in `data/downloads/` with CORS support.
   - `HandleTasks`: Creates batch tasks, enforcing admin-only RBAC (`403 Forbidden: admin only\n`).
   - `HandleTaskDetails`: Retrieves task details by `task_id` with authentication.
   - `HandleDownloads`: Static delivery from `data/downloads/` with CORS and `http.StripPrefix`.
   - `HandleSnapshots`: In-memory JPEG delivery with device-level permission check.

---

## 5. Differential Verification Suite (67/67 PASS)

Differential test suite `tests/differential/files_tasks/test_files_tasks_http_diff.py` executed side-by-side against the canonical Windows oracle binary (`webrtc-signaling.exe`):

- **Group 1: `/upload` Standard File** (12 tests):
  - FT-DIFF-01 .. FT-DIFF-12: Unauth (401), normal user (403), missing name (400), path traversal '.' & '..' (400), admin success (200), no-auth success (200), HTTP verbs GET/PUT/PATCH/DELETE/OPTIONS parity.
- **Group 2: `/upload` Snapshot Ingest** (8 tests):
  - FT-DIFF-13 .. FT-DIFF-20: Unauth success (200 in-memory), missing device_id (400), invalid device_id (400), verbs GET/PUT/PATCH/DELETE/OPTIONS parity.
- **Group 3: `/downloads/` Static Delivery** (4 tests):
  - FT-DIFF-21 .. FT-DIFF-24: Static download (200), HEAD (200), OPTIONS preflight (200), 404 nonexistent.
- **Group 4: `/api/files` Listing & Deletion** (11 tests):
  - FT-DIFF-25 .. FT-DIFF-35: Unauth (401), user list (200), admin list (200), OPTIONS CORS (200), delete missing name (400), delete 404, delete 200, empty list parity `[]\n`, verbs POST/PUT/PATCH rejection (405).
- **Group 5: `/api/tasks` Creation** (10 tests):
  - FT-DIFF-36 .. FT-DIFF-45: Unauth (401), user rejection (403), empty targets (400), malformed JSON (400), admin success (200), OPTIONS (200), verbs GET/PUT/PATCH/DELETE rejection (405).
- **Group 6: `/api/tasks/details`** (10 tests):
  - FT-DIFF-46 .. FT-DIFF-55: Unauth (401), missing task_id (400), 404 nonexistent, admin read (200), offline target status parity, user read (200), verbs POST/PUT/PATCH/DELETE rejection (405).
- **Group 7: `/snapshots/` Delivery** (10 tests):
  - FT-DIFF-56 .. FT-DIFF-65: Unauth (401), unassigned user (403), assigned user .jpg (200 image/jpeg), extensionless URL (200), invalid ext .png (404), nonexistent (404), HEAD (200), OPTIONS unauth (401) vs auth (200), no-auth bypass (200).
- **Group 8: In-Memory Restart Reset** (2 tests):
  - FT-DIFF-66 & FT-DIFF-67: Verified that tasks and snapshots reset cleanly upon server restart (zero persistence on disk).

**Total Differential Pass Rate**: 67/67 (100%).

---

## 6. Cumulative Verification Audit

Running `tools/verify_phase2.py`:
- 16 major audit sections checked and passed.
- Forensic gate: 18/18 invariants PASS.
- Forensic reproducibility: 21/21 artifacts machine-derived and verified.
- Master differential rate: **354/354 (100%)** across all 11 suites:
  1. `AUTH_DIFFERENTIAL_RESULTS`: 14/14
  2. `AUTH_HTTP_DIFFERENTIAL_RESULTS`: 20/20
  3. `DEVICE_HTTP_DIFFERENTIAL_RESULTS`: 23/23
  4. `USER_ADMIN_HTTP_DIFFERENTIAL_RESULTS`: 43/43
  5. `TAG_HTTP_DIFFERENTIAL_RESULTS`: 20/20
  6. `SHARE_HTTP_DIFFERENTIAL_RESULTS`: 36/36
  7. `SHORTCUT_HTTP_DIFFERENTIAL_RESULTS`: 19/19
  8. `SERVER_CONFIG_HTTP_DIFFERENTIAL_RESULTS`: 55/55
  9. `LICENSE_HTTP_DIFFERENTIAL_RESULTS`: 26/26
  10. `PERSISTENCE_DIFFERENTIAL_RESULTS`: 31/31
  11. `FILES_TASKS_HTTP_DIFFERENTIAL_RESULTS`: 67/67

**Verdict**: Phase 2C.3I is **COMPLETE, VERIFIED, AND FULLY COMPLIANT**.
