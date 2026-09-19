# Report 26: Phase 2C.3I Files / Tasks / Downloads / Snapshots Forensics & Gate Evaluation

**Phase**: 2C.3I  
**Date**: 2026-09-16  
**Status**: APPROVED & GATE PASSED (18/18 Invariants PASS, 21/21 Artifacts Machine-Derived)  
**Binary Targets**:
- Linux AMD64: `canonical_builds/linux_amd64/webrtc-signaling` (`6865f05fe598...`)
- Windows AMD64: `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe`

---

## 1. Executive Summary

In accordance with the **HR3 True Forensic Reproducibility** standard and user review amendments:
1. All 6 canonical routes (`/upload`, `/api/files`, `/api/tasks`, `/api/tasks/details`, `/downloads/`, `/snapshots/`) were resolved directly from `ROUTE_HANDLER_MAP.json` and binary symbols.
2. All 21 canonical forensic artifacts were machine-derived directly from binaries, callgraph disassembly, and fresh isolated oracle executions without any copying (`shutil.copy` / `copy2`) or read-and-reemit of canonical evidence.
3. The forensic gate evaluated **18/18 invariants as PASS** in `FILES_TASKS_FORENSIC_GATE_RESULT.json`.
4. Full 21/21 artifact reproducibility verified in `tools/forensics/reproduce_files_tasks_forensics.py` with `canonical_input_used: false` on all artifacts.

---

## 2. Route Family & Static Function Correlation

| Route Pattern | Registration Type | Call VA | Handler Symbol | Handler VA | Size (B) | Semantic Role |
|---|---|---|---|---|---|---|
| `/upload` | `HandleFunc` | `0x765c88` | `main.swqKgLrjAZT9` | `0x758c80` | 5376 | `FILE_TRANSMISSION_AND_TASK_MANAGER` |
| `/api/files` | `HandleFunc` | `0x765ca0` | `main.qa3RvDW` | `0x75a2c0` | 3200 | `FILE_TRANSMISSION_AND_TASK_MANAGER` |
| `/api/tasks` | `HandleFunc` | `0x765cb8` | `main.koVbnsD4T0d` | `0x75afa0` | 4000 | `FILE_TRANSMISSION_AND_TASK_MANAGER` |
| `/api/tasks/details` | `HandleFunc` | `0x765cd0` | `main.bhMId7t5J` | `0x763ec0` | 1600 | `FILE_TRANSMISSION_AND_TASK_MANAGER` |
| `/downloads/` | `Handle` | `0x765d6b` | `Y0caeZ_zze.MB_aa9i.ServeHTTP` | `0x6e0340` | 96 | `STATIC_FILE_SERVER` |
| `/snapshots/` | `HandleFunc` | `0x765d83` | `main.main.func5` | `0x76da00` | 1536 | `SNAPSHOT_HANDLER` |

### Download Wrapper Hierarchy
- Outer: `http.StripPrefix("/downloads/", ...)` (`main.main.Op3UlgB95u.func8` at `0x766f40`, 704B)
- Inner: `main.main.func4` (`0x76d760`, 672B) which applies CORS headers (`Access-Control-Allow-Origin: *`, `Access-Control-Allow-Headers: Content-Type, Authorization`), intercepts `OPTIONS` -> `200 OK`, cleans path (`filepath.Clean`), joins with `dataDir/downloads`, and calls `http.ServeFile` (`0x6afb20`).

---

## 3. Wire Contracts & Empirical Protocols

### A. Split `/upload` Protocol
1. **Standard File Upload (`UPLOAD_STANDARD_FILE`)**:
   - `POST /upload?name=<filename>`
   - Authenticated (`401 Unauthorized` if missing/invalid).
   - Admin-only RBAC (`403 Forbidden: Only administrators can upload files` if non-admin).
   - Filename path traversal rejection: rejects literal `"."` or `".."` with `400 Invalid file path (path traversal detected)\n`. Uses `filepath.Base` for containment.
   - Body: raw stream copied directly into `data/downloads/<filename>`.
   - Response: `200 OK`, body `'Uploaded to <filename>'`.
2. **Snapshot Ingest (`UPLOAD_SNAPSHOT_INGEST`)**:
   - `POST /upload?type=snapshot&device_id=<id>`
   - Unauthenticated device/agent ingest endpoint.
   - Requires `device_id` parameter (`400 Missing device_id\n` or `400 Invalid device_id\n`).
   - Body: raw JPEG image bytes.
   - Stores in in-memory snapshot map keyed by `<device_id>`.
   - Response: `200 OK`, body `'Uploaded to memory for <id>.jpg'`.

### B. `/api/files` Protocol
- Allowed verbs: `GET`, `DELETE`, `OPTIONS`. All others return `405 Method not allowed\n`.
- Authenticated (admin and normal users permitted).
- `GET /api/files`: lists files in `data/downloads/`. Directories excluded. Sorted lexicographically by filename.
  - JSON item schema: `{"name": string, "size": int64, "updated_at": string (RFC3339), "url": "/downloads/{name}"}`.
  - Classification: `GENERATED_WIRE_MODEL`.
- `DELETE /api/files?name=<filename>`:
  - Missing `name` -> `400 Missing name parameter\n`.
  - Non-existent file -> `404 File not found\n`.
  - Success -> deletes file from disk, returns `200 OK`, `'{"status":"success"}'`.

### C. Static Deliveries: `/downloads/` and `/snapshots/`
- `/downloads/`: Static file delivery from `data/downloads/`. Supports `Accept-Ranges: bytes`, HTTP 206 Partial Content, `Last-Modified`, `HEAD`, directory redirect `301 Moved Permanently` (`Location: ./`).
- `/snapshots/`: In-memory snapshot delivery (`main.main.func5`).
  - URL format: `/snapshots/<device_id>.jpg` or `/snapshots/<device_id>`.
  - Authenticated: `401 Unauthorized\n`.
  - RBAC: Validates device access via `main.pVOasuBli` (`403 Forbidden\n` if device not assigned).
  - Missing snapshot in memory: `404 404 page not found\n`.
  - Success: `200 OK`, `Content-Type: image/jpeg`, `Cache-Control: no-cache, no-store, must-revalidate`, `Access-Control-Allow-Origin: *`.
  - Snapshot producer: `PRODUCER_DEFERRED_TO_TRANSPORT_PHASE`.

### D. Tasks API: `/api/tasks` and `/api/tasks/details`
- `/api/tasks`: `POST`, `OPTIONS`.
  - Admin-only RBAC (`main.chIaMDTZ` -> `403 Forbidden: Administrator role required\n`).
  - Request DTO (recovered from ELF descriptor `0x7ea980`, 72B):
    `{"type": string, "targets": []string, "payload": string, "dest_path": string}`
  - If `targets` is empty -> `400 Targets cannot be empty\n`.
  - Response: `{"status":"success","task_id":"task_YYYYMMDDhhmmss_<hex16>"}\n`.
  - Task ID format (`0x82229b` and `0x825bda`): prefix `task_`, timestamp in local time `20060102150405`, random 16-hex string.
  - Storage: In-memory map (`map[string]*types.Task`). No on-disk persistence.
  - Offline targets: Immediately marked `{"status":"failed","progress":0,"result":"Device offline","updated_at":"..."}`.
  - Online target dispatch: `ONLINE_DISPATCH_TRANSPORT_DEPENDENT` (deferred to transport phase).
- `/api/tasks/details`: `GET ?task_id=...`, `OPTIONS`.
  - Authenticated (admin and normal users permitted).
  - Missing `task_id` -> `400 Missing task_id parameter\n`.
  - Unknown task -> `404 Task not found\n`.
  - Success -> `200 OK`, full Task DTO (descriptor `0x7fb3c0`).

---

## 4. Go Runtime Type Recovery (ELF .rodata)

All 3 task-related structs recovered directly from ELF runtime type descriptors:
1. `TaskCreateRequest` (`0x7ea980`, 72 bytes):
   - `type` (offset 0, tag `json:"type"`)
   - `targets` (offset 16, tag `json:"targets"`, `[]string`)
   - `payload` (offset 40, tag `json:"payload"`)
   - `dest_path` (offset 56, tag `json:"dest_path"`)
2. `Task` (`0x7fb3c0`, 88 bytes, symbol `*main.Jh0XQJ`):
   - `task_id` (offset 0, tag `json:"task_id"`)
   - `type` (offset 16, tag `json:"type"`)
   - `payload` (offset 32, tag `json:"payload"`)
   - `dest_path` (offset 48, tag `json:"dest_path,omitempty"`)
   - `created_at` (offset 64, tag `json:"created_at"`)
   - `devices` (offset 80, tag `json:"devices"`, `map[string]*DeviceTaskStatus`)
3. `DeviceTaskStatus` (`0x7f4be0`, 72 bytes, symbol `*main.ZFJczDtV4TR`):
   - `device_id` (offset 0, tag `json:"device_id"`)
   - `status` (offset 16, tag `json:"status"`)
   - `progress` (offset 32, tag `json:"progress"`)
   - `result` (offset 40, tag `json:"result"`)
   - `updated_at` (offset 56, tag `json:"updated_at"`)

---

## 5. Forensic Gate Verdict: PASS (18/18)

All 18 required non-transport invariants evaluated to `True` in `FILES_TASKS_FORENSIC_GATE_RESULT.json`.
Forensic gate is **OFFICIALLY CLEARED**. Cleanroom source code reconstruction may now proceed.
