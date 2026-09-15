# Forensic Report 06: Phase 2C.1 Persistence Differential Verification

**Status**: DIFFERENTIAL VERIFICATION PASS

## 1. Differential Test Results

| Test ID | Test Name | Result Class | Status | Forensic Details |
|---|---|---|---|---|
| `TC-DIFF-01` | First-Run Directory Structure | `EXACT_MATCH` | **PASS** | Items: {'snapshots', 'device_tags.json', 'downloads', 'users.json'} (shares.json correctly absent in both) |
| `TC-DIFF-02` | users.json Admin Schema & Defaults | `EXACT_MATCH` | **PASS** | Keys (11): ['assigned_devices', 'expires_at', 'forbid_audio', 'forbid_bitrate', 'forbid_fps', 'forbid_resolution', 'note', 'password', 'role', 'salt', 'username'] |
| `TC-DIFF-03` | Admin Password Hash Algorithm | `EXACT_MATCH` | **PASS** | SHA256(pwd+salt) matched for both (salt lengths: 32/32) |
| `TC-DIFF-04` | device_tags.json Schema & Defaults | `EXACT_MATCH` | **PASS** | Content match: {'tags': [], 'deviceTags': {}} |
| `TC-DIFF-05` | Malformed JSON Recovery Semantics | `SEMANTIC_MATCH` | **PASS** | Successfully recovered corrupted users.json with default admin account |
| `TC-DIFF-06` | Unknown Field Tolerance | `SEMANTIC_MATCH` | **PASS** | Parser successfully loaded record containing unmodeled JSON fields |
| `TC-DIFF-07` | POSIX Permission Bits Parity | `STATIC_CONFIRMED` | **PASS** | users.json=0600 (0x180), device_tags.json=0644 (0x1a4), shares.json=0600 (0x180) |
| `TC-DIFF-08` | Atomic Save Rename Semantics | `STATIC_CONFIRMED` | **PASS** | shares.json uses .tmp temp file write + os.Rename atomic swap |

## 2. Classification Key

- `EXACT_MATCH`: 100% bit-for-bit or deterministic schema/value equivalence.
- `SEMANTIC_MATCH`: Identical behavioral handling of runtime states (recovery, tolerance).
- `STATIC_CONFIRMED`: Disassembly proof from original Linux binary instructions where OS runtime cannot execute POSIX semantics natively.
- `KNOWN_DIFFERENCE`: Explicitly documented intentional clean-room differences (none in Phase 2C.1).
- `UNKNOWN`: Unresolved or unmodeled behaviors (none in Phase 2C.1).

## 3. Provenance and Scope Compliance

- **Zero Authentication Handlers**: No login verification, session token issuance, or auth middleware was written.
- **Zero Network Endpoints**: No HTTP handlers, WebSocket hubs, or WebRTC data channels were included.
- **Structure Tagging**: New directories (`pkg/types/`, `pkg/storage/`) and `go.mod` are explicitly annotated as `GENERATED_BUILD_STRUCTURE` and `GENERATED_BUILD_FILE`.
