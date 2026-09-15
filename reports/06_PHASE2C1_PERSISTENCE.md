# Forensic Report 06: Phase 2C.1 Persistence Differential Verification

**Status**: DIFFERENTIAL VERIFICATION PASS (6 RUNTIME TESTS + 2 STATIC/DYNAMIC KERNEL PARITY TESTS)

## 1. Differential Test Results Matrix

| Test ID | Test Name | Result Class | Status | Original Evidence | Reconstructed Evidence | Parity Comparison |
|---|---|---|---|---|---|---|
| `TC-DIFF-01` | First-Run Directory Structure | `STRUCTURAL_EXACT_MATCH` | **PASS** | Files/dirs created: {'device_tags.json': 'file', 'downloads': 'dir', 'snapshots': 'dir', 'users.json': 'file'} (shares.json absent) | Files/dirs created: {'device_tags.json': 'file', 'downloads': 'dir', 'snapshots': 'dir', 'users.json': 'file'} (shares.json absent) | Both eagerly create exactly {users.json (file), device_tags.json (file), downloads/ (dir), snapshots/ (dir)} and lazily defer shares.json |
| `TC-DIFF-02` | users.json Admin Schema & Defaults | `NORMALIZED_EXACT_MATCH` | **PASS** | Admin keys (11): ['assigned_devices', 'expires_at', 'forbid_audio', 'forbid_bitrate', 'forbid_fps', 'forbid_resolution', 'note', 'password', 'role', 'salt', 'username'], role='admin', assigned=['*'], expires='0001-01-01T00:00:00Z' | Admin keys (11): ['assigned_devices', 'expires_at', 'forbid_audio', 'forbid_bitrate', 'forbid_fps', 'forbid_resolution', 'note', 'password', 'role', 'salt', 'username'], role='admin', assigned=['*'], expires='0001-01-01T00:00:00Z' | Normalized exact match on all 11 schema keys, default admin roles, assigned devices wildcard, and timestamps |
| `TC-DIFF-03` | Admin Password Hash Algorithm | `NORMALIZED_EXACT_MATCH` | **PASS** | pwd=SHA256('admin123' + salt), salt_len=32 | pwd=SHA256('admin123' + salt), salt_len=32 | Both derive default admin credentials as SHA256('admin123' + salt) with 16-byte cryptographically secure random salt |
| `TC-DIFF-04` | device_tags.json Schema & Defaults | `BIT_EXACT_MATCH` | **PASS** | Raw bytes (36B): b'{\n  "tags": [],\n  "deviceTags": {}\n}' | Raw bytes (36B): b'{\n  "tags": [],\n  "deviceTags": {}\n}' | Raw read_bytes() is 100% byte-for-byte identical across original and reconstructed first-run payloads |
| `TC-DIFF-05` | Malformed JSON Recovery Semantics | `SEMANTIC_MATCH` | **PASS** | Original: logged '[Auth] Failed to parse users file' and reset users.json with admin/admin123 | Reconstructed: logged '[Auth] Failed to parse users file' and reset users.json with admin/admin123 | Both runtimes detect corrupted users.json, catch unmarshal error, log verbatim diagnostic, and rewrite fresh default admin account |
| `TC-DIFF-06` | Unknown Field Lifecycle Parity | `SEMANTIC_MATCH` | **PASS** | Original: unknown fields tolerated on load; dropped on /api/admin/users/update_note save; 11 known fields preserved; note updated | Reconstructed: unknown fields tolerated on load; dropped on save-user; 11 known fields preserved; note updated | Both runtimes accept unmodeled fields on read-only load; both drop unmodeled fields upon struct save while preserving all known fields and mutations |
| `TC-DIFF-07` | POSIX Permission Bits Parity | `STATIC_AND_DYNAMIC_PARITY` | **PASS** | STATIC_CONFIRMED: disassembly VAs 0x737666 (0600), 0x737f15 (0644), 0x739cd9 (0600) | DYNAMIC_LINUX_CONFIRMED: WSL stat modes: users=600, tags=644, shares=600 | Static Linux AMD64 callsite disassembly matched with real Linux WSL stat(2) runtime modes |
| `TC-DIFF-08` | Atomic Save Rename Semantics | `STATIC_AND_DYNAMIC_PARITY` | **PASS** | STATIC_CONFIRMED: disassembly VA 0x739cb5 ('%s.tmp') -> 0x739cd9 (os.WriteFile) -> 0x739e12 (os.Rename) | RUNTIME_AND_SOURCE_CONFIRMED: shares.json written, .tmp cleaned (True), verified AST tmpPath+os.Rename | Both write temporary file with .tmp suffix before atomic swap to final path via os.Rename |

## 2. Classification Key

- `BIT_EXACT_MATCH`: 100% byte-for-byte identical content verified via raw `read_bytes()` comparison (e.g. `device_tags.json`).
- `STRUCTURAL_EXACT_MATCH`: Exact directory tree entries, file/directory types, and key structures matched.
- `NORMALIZED_EXACT_MATCH`: Exact schema, keys, types, and values after normalizing non-deterministic random fields (e.g. 16-byte random salt and SHA256 password hash).
- `SEMANTIC_MATCH`: Identical runtime behavior observed side-by-side between original binary and reconstructed code under identical operations and edge cases (e.g. malformed JSON reset with diagnostic logging, full unknown field lifecycle with persistence mutation).
- `STATIC_AND_DYNAMIC_PARITY`: Original static disassembly proof (x86_64 callsite arguments) verified against real Linux/WSL runtime stat(2) mode bits and atomic filesystem operations.
- `KNOWN_DIFFERENCE`: Explicitly documented intentional clean-room differences (none in Phase 2C.1).
- `UNKNOWN`: Unresolved or unmodeled behaviors (none in Phase 2C.1).

## 3. Provenance and Scope Compliance

- **Zero Authentication Handlers**: No login verification, session token issuance, or auth middleware was written.
- **Zero Network Endpoints**: No HTTP handlers, WebSocket hubs, or WebRTC data channels were included.
- **Structure Tagging**: New directories (`pkg/types/`, `pkg/storage/`) and `go.mod` are explicitly annotated as `GENERATED_BUILD_STRUCTURE` and `GENERATED_BUILD_FILE`.
- **Function-Level Provenance**: Every declared function and method has an explicit `CLEANROOM-PROVENANCE` block audited by `tools/verify_reconstructed_provenance.py`.
