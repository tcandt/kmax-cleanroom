# Phase 2C.3F — Shortcuts REST Route Family Forensic Analysis Report

**Execution Timestamp**: `2026-09-16 05:03:30 UTC`  
**Target Canonical Binary**: `webrtc-signaling` (Linux AMD64 ELF, SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Route Under Audit**: `/api/shortcuts`  
**Status**: **FORENSIC GATE PASSED — READY FOR RECONSTRUCTION**

---

## 1. Route Identity & Architectural Separation

From `ROUTE_HANDLER_MAP.json` and Capstone disassembly:
- **Route Pattern**: `/api/shortcuts`
- **Registration Call VA**: `0x765984` in `main.main` (`http.HandleFunc`)
- **Wrapper Closure**: `main.main.func3` (VA `0x76d4c0`, 672 bytes)
  - Injects CORS headers:
    - `Access-Control-Allow-Origin: *`
    - `Access-Control-Allow-Methods: GET, POST, OPTIONS`
    - `Access-Control-Allow-Headers: Content-Type, Authorization`
  - Handles `OPTIONS` verb directly: returns `200 OK` with empty body
  - Dispatches all non-OPTIONS requests to the business handler at `0x76c640`
- **Dispatched Business Handler**: `main.yHBQWSpi` (VA `0x76c640`, 1856 bytes)
  - Authenticates request via `main.lYKp_Iuf` (VA `0x73b080`)
  - Routes `GET` to slice serialization
  - Routes `POST` to body unmarshaling, map update, and persistence
  - Rejects any other HTTP method with `405 Method not allowed\n`
- **Persistence Callees**:
  - `loadShortcuts`: `main.iXiPYH2zBLTK` (VA `0x76bf20`, 640 bytes), invoked at server startup (`0x7658d4`) in `main.main`.
  - `saveShortcuts`: `main.jk9A26` (VA `0x76c2c0`, 608 bytes), invoked after successful mutation in `main.yHBQWSpi`.

---

## 2. 7-Verb Method Matrix

Observed wire behavior on `/api/shortcuts` (`allow_redirects=False`):

| Method | Status | Content-Type | Body Bytes | Wire Body Preview | Semantic Meaning |
|---|---|---|---|---|---|
| **GET** | `200 OK` | `application/json` | Variable | `'[]\n'` (empty) or JSON array | Retrieves calling user's shortcuts |
| **POST** | `200 OK` / `400 Bad Request` | `application/json` / `text/plain` | Variable | `'{"status":"success"}\n'` / `'Invalid JSON\n'` | Mutates/replaces user shortcuts |
| **OPTIONS** | `200 OK` | (None) | 0 | `''` | CORS preflight with full access headers |
| **PUT** | `405 Method Not Allowed` | `text/plain; charset=utf-8` | 19 | `'Method not allowed\n'` | Disallowed verb |
| **PATCH** | `405 Method Not Allowed` | `text/plain; charset=utf-8` | 19 | `'Method not allowed\n'` | Disallowed verb |
| **DELETE** | `405 Method Not Allowed` | `text/plain; charset=utf-8` | 19 | `'Method not allowed\n'` | Disallowed verb |
| **HEAD** | `405 Method Not Allowed` | `text/plain; charset=utf-8` | 0 | `''` (Wire bodyless, Content-Length: 19) | HEAD on disallowed verb |

---

## 3. Auth Matrix

Observed access control behavior:

| Client State | Status Code | Content-Type | Response Body | Semantic Result |
|---|---|---|---|---|
| **ADMIN** | `200 OK` | `application/json` | `'[]\n'` | Allowed (Admin personal shortcuts) |
| **NORMAL_USER** | `200 OK` | `application/json` | `'[]\n'` | Allowed (Normal user personal shortcuts) |
| **NO_AUTH_MODE** | `200 OK` | `application/json` | `'[]\n'` | Allowed (Bypasses token, uses `"admin"` key) |
| **MISSING_TOKEN** | `401 Unauthorized` | `text/plain; charset=utf-8` | `'Unauthorized\n'` | Rejection on missing Authorization header |
| **INVALID_TOKEN** | `401 Unauthorized` | `text/plain; charset=utf-8` | `'Unauthorized\n'` | Rejection on invalid Bearer token |

---

## 4. Discovered Data Models & Type Descriptors

Directly recovered from ELF metadata (`.rodata`):
1. **Shortcut Struct**: `main.KXuCJAAi60` (VA `0x7d70c0`, size 32 bytes)
   - Field 0: `DIHvMDn` (`string`, offset 0, JSON tag: `json:"name"`)
   - Field 1: `MTkDoTKb` (`string`, offset 16, JSON tag: `json:"cmd"`)
2. **Top-Level Storage Map**: `*map[string][]main.KXuCJAAi60` (VA `0x7bfc40`)
   - Key: `string` (Username of the authenticated user)
   - Value: `[]Shortcut` (Slice of shortcuts for that user)

---

## 5. Operations & Mutation Surface

1. **Read Operation (`GET /api/shortcuts`)**:
   - Looks up calling username in `shortcutsMap`.
   - If not present or empty, encodes empty array: returns `'[]\n'` with `Content-Type: application/json`.
   - If present, encodes `[]Shortcut`.
2. **Mutation Operation (`POST /api/shortcuts`)**:
   - Decodes body as `[]Shortcut`.
   - If body is empty, not a JSON array, or malformed: returns `400 Bad Request` with `'Invalid JSON\n'`.
   - If valid: replaces entire slice for caller username: `shortcutsMap[username] = shortcuts`.
   - Invokes `saveShortcuts` to persist map to disk.
   - Emits `200 OK` with JSON `{"status":"success"}\n`.
3. **Per-User Isolation**:
   - User Alpha shortcuts and Admin shortcuts are stored in separate keys in the map and persisted as separate keys in `shortcuts.json`.
   - Mutations by User Alpha do not affect Admin, and vice versa.

---

## 6. Persistence Contract

Disassembled from `main.jk9A26` and `main.main`:
- **File Name**: `shortcuts.json`
- **File Path**: `filepath.Join(dataDir, "shortcuts.json")` (constructed in `main.main` at `0x765298`)
- **Write Mechanism**: Direct `os.WriteFile` (`0x76c435`) without atomic rename.
- **File Permissions**: Mode `0644` (`0x1a4`, instruction `0x76c426: mov r8d, 0x1a4`).
- **Indentation**: 2 spaces via `json.MarshalIndent` (`0x76c360`).
- **Load Lifecycle**: Loaded at startup in `main.main` via `main.iXiPYH2zBLTK` (`0x7658d4`).
- **No-Auth Mode Key**: Proved by dynamic execution in `-no-auth` mode:
  ```json
  {
    "admin": [
      {
        "name": "NoAuth Key",
        "cmd": "input keyevent 82"
      }
    ]
  }
  ```
  The storage key used in `-no-auth` mode is `"admin"`.

---

## 7. Forensic Gate Verdict

- [x] Route binding confirmed (`/api/shortcuts` at `0x765984`)
- [x] Wrapper (`main.main.func3 @ 0x76d4c0`) and business handler (`main.yHBQWSpi @ 0x76c640`) mapped
- [x] Loader (`0x76bf20`) and saver (`0x76c2c0`) mapped
- [x] 7-verb matrix captured (GET 200, OPTIONS 200, PUT/PATCH/DELETE/HEAD 405)
- [x] Wire bodyless HEAD confirmed
- [x] Auth matrix captured (Admin/User/NoAuth 200, Missing/Invalid 401)
- [x] Shortcut struct recovered (`name`, `cmd`, 32 bytes)
- [x] Per-user storage map recovered (`map[string][]Shortcut`)
- [x] Replace mutation semantics confirmed
- [x] `shortcuts.json` persistence confirmed (mode `0644`, direct `os.WriteFile`, 2 spaces)
- [x] No-auth mode storage key proven to be `"admin"`
- [x] 7/7 reproducibility tool independently verified

**VERDICT: GATE PASSED. PROCEEDING TO CLEANROOM RECONSTRUCTION.**
