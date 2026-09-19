# Phase 2C.5B3 Report: WebRTC File-Channel Clean-Room Reconstruction

**Phase**: Phase 2C.5B3  
**Date**: 2026-09-17  
**Contract Frozen SHA-256**: `1ff71090f6a16de538cad6cf93fc4096d34a913bed4008d1172f41b83da8e17b`  
**Classification**: Clean-Room Behavioral/Protocol Reconstruction (Zero Claims of Literal Original Source)  
**Status**: CLOSED & FULLY VERIFIED  

---

## 1. Executive Summary & Scope Boundary

Phase 2C.5B3 completes the clean-room behavioral, state machine, and protocol reconstruction of the WebRTC `file-channel` inside `cloudphone-agent`:
1. **`file-channel`**: Reconstructs the hybrid text/binary file transfer protocol between the browser peer and the agent over a dedicated, ordered SCTP DataChannel.
2. **Safe `FileSink` Boundary**: Isolates filesystem operations behind a decoupled `FileSink` abstraction (`Begin`, `WriteChunk`, `Complete`, `Abort`), preventing arbitrary filesystem access or scattered I/O.
3. **Defensive Path Sanitization**: Strips directory traversal vectors (`../`, `..\`), absolute paths, Windows drive specifiers (`C:`), UNC shares (`\\`), and control characters (NUL).
4. **Deferred Package Installation**: Decouples the `install` metadata flag into an abstract `PostUploadActionHandler` hook. All actual package installation mechanisms (`pm install`, shell execution, process spawning) remain strictly deferred (`PHASE_SCOPE_GUARD`).

### Strict Phase Boundaries Maintained
- **Active Channels in B3**: `input-channel`, `clipboard-channel` (from B2), `file-channel` (reconstructed in B3).
- **Deferred Channels**: `camera-channel`, `ai-command-channel`, and `adb-channel` remain strictly inert with zero message handlers or business logic.
- **Zero Command Execution**: 0 calls to `os/exec` or `exec.Command` in `cloudphone-agent/pkg`.
- **Media Plane Boundary**: Full camera/audio hardware pipeline remains deferred to Phase B5.

---

## 2. Implementation Contract Frozen First

Prior to implementing production code in `cloudphone-agent`, the Phase 2C.5B3 contract was machine-derived from verified forensic evidence and frozen:
- **Contract Path**: `evidence/go_agent/webrtc/FILE_CHANNEL_B3_IMPLEMENTATION_CONTRACT.json`
- **Frozen SHA-256**: `1ff71090f6a16de538cad6cf93fc4096d34a913bed4008d1172f41b83da8e17b`
- **Governing Evidence Artifacts**:
  - `DATACHANNEL_LABEL_EVIDENCE.json`
  - `DATACHANNEL_FRAMING_MATRIX.json`
  - `DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json`
  - `WEBRTC_PEERCONNECTION_CALLGRAPH.json`
  - `WEBRTC_PEERCONNECTION_STATE_MACHINE.json`
  - Original Agent binary/disassembly (`cloudphone-agent` ARM64 / Windows AMD64 `0x9e3f20-0x9e3fa0`)
  - Web client evidence (`useWebRTC.js:1366,1379`, `REFERENCE_ONLY`)

The contract defines 16 formal requirements (`FILE-B3-01` through `FILE-B3-16`), categorized into strict epistemic provenance classes.

---

## 3. Recovered File-Channel Protocol & Wire Framing

### Channel Properties
- **Channel Label**: `"file-channel"`
- **Creator**: Client peer (browser / client-side WebRTC peer)
- **Reliability & Ordering**: `ordered: true`, reliable SCTP transport

### Hybrid Framing Specification

| Frame Type | Transport Framing | Payload Encoding | Purpose | Forensic Evidence |
|---|---|---|---|---|
| **Metadata Ingress** | Text (SCTP DataChannel string) | JSON (`UTF-8`) | Announces upcoming upload: filename, total byte size, SHA-256 checksum, install flag | `DATACHANNEL_FRAMING_MATRIX.json`, `useWebRTC.js:1366` |
| **Data Chunks** | Binary (SCTP DataChannel binary) | Raw bytes (`ArrayBuffer`) | Sequential file payload chunks (up to 64 KB per chunk) | `DATACHANNEL_FRAMING_MATRIX.json`, `useWebRTC.js:1379` |

### Ingress Metadata Frame Schema (`start_upload`)
```json
{
  "type": "start_upload",
  "filename": "string",
  "size": 12345,
  "sha256": "abcdef...64-hex",
  "install": true
}
```
- `type`: Must be `"start_upload"`.
- `filename`: Target basename.
- `size`: Non-negative declared file size in bytes.
- `sha256`: Optional/defensive 64-character hexadecimal SHA-256 hash.
- `install`: Boolean flag indicating if post-upload installation is requested.

---

## 4. Message State Machine & Bounded Transitions

`FileChannelHandler` enforces an explicit, deterministic state machine:

```
    +-------------------------------------------------------------+
    |                                                             |
    v                                                             |
[ IDLE ] -- (Text: start_upload) --> [ METADATA_ACCEPTED ]        |
    |                                        |                    |
    | (Binary received)                      | (First Chunk)      |
    v                                        v                    |
 [ ABORT / REJECT ]                    [ RECEIVING ]              |
                                             |                    |
                                             | (Bytes == Size &   |
                                             |  SHA256 Matches)   |
                                             v                    |
                                       [ COMPLETE ] --------------+
                                             |
                                    (PostUploadAction)
```

### Deterministic Edge-Case Handling

| Scenario | Agent Behavior | Classification |
|---|---|---|
| **Binary chunk before metadata** | Rejected, channel aborted, zero bytes written | `IMPLEMENTATION_CHOICE` |
| **Duplicate `start_upload` while receiving** | Existing transfer aborted, sink cleaned up | `IMPLEMENTATION_CHOICE` |
| **Zero-byte upload (`size = 0`)** | Immediately transitions to `COMPLETE`, verifies empty checksum, completes sink | `STATIC_CONFIRMED` |
| **Size overflow (received > declared)** | Transfer aborted, sink cleaned up, error logged | `IMPLEMENTATION_CHOICE` |
| **Early DataChannel / PeerConnection close** | Sink `Abort()` invoked, temporary file removed | `IMPLEMENTATION_CHOICE` |
| **SHA-256 checksum mismatch** | Transfer aborted, sink cleaned up, not completed | `IMPLEMENTATION_CHOICE` |
| **Malformed JSON metadata** | Rejected with error, remains in `IDLE` | `IMPLEMENTATION_CHOICE` |

---

## 5. Safe `FileSink` Boundary & Path Sanitization

### Decoupled Interface
```go
type FileSink interface {
    Begin(metadata FileMetadata) error
    WriteChunk(data []byte) error
    Complete() error
    Abort() error
}
```
Two concrete implementations are provided:
1. **`MemoryFileSink`**: Stores bytes in memory (`[]byte`) for isolated unit testing, fuzzing, and real SCTP E2E tests without disk I/O.
2. **`LocalFileSink`**: Streams chunks to a temporary sandboxed directory with safe file permissions (`0600`), atomicity via temp files, and automatic unlinking on abort.

### Defensive Path Sanitization (`SanitizeFilename`)
Sanitizes filenames to prevent path traversal attacks:
- Strips directory prefixes via `filepath.Base`.
- Disallows parent directory traversal (`..`).
- Strips Windows drive designators (`C:`) and UNC network paths (`\\server\share`).
- Replaces path separators (`/`, `\`) and NUL bytes (`\x00`).
- Fallback to safe generated name (`upload.bin`) if filename resolves to empty or `.` / `..`.

---

## 6. Install Flag & Deferred Package Installation Boundary

The `install: bool` field indicates whether an APK should be installed upon transfer completion:
- **Original Disassembly Reference**: Disassembly strings reference `/data/local/tmp` and post-upload handling at `0x9e3f70`.
- **Phase Boundary Enforcement**: In Phase 2C.5B3, package installation (`pm install`, shell invocation, `exec.Command`) is **strictly deferred** (`PHASE_SCOPE_GUARD`).
- **Decoupled Event Hook**:
  ```go
  type PostUploadActionHandler func(metadata FileMetadata, sink FileSink) error
  ```
  The handler receives notification upon clean completion without executing commands. Verifier checks confirm zero `os/exec` calls across the production tree.

---

## 7. Real SCTP WebRTC DataChannel E2E Verification

A real end-to-end integration test was executed over genuine SCTP via Pion WebRTC (`TestWebRTCDataChannelsE2E/file_upload`):
1. **Setup**: Browser client peer connects to Agent peer over WebRTC signaling.
2. **Channel Creation**: Client peer creates `file-channel` with `ordered: true`.
3. **Metadata Transmission**: Client sends JSON text frame `start_upload` with filename, size (62 bytes), SHA-256 hex, and `install=true`.
4. **Binary Chunk Transmission**: Client sends 3 distinct binary chunks (20B, 25B, 17B) over the SCTP DataChannel.
5. **Reconstruction Verification**: Agent processes chunks into `FileSink`, computes running SHA-256, reaches `COMPLETE`, and reconstructs the payload with 100% byte-exact parity.
6. **Post-Action Verification**: `PostUploadActionHandler` hook triggers with `test_e2e_app.apk`.

---

## 8. Dynamic Differential Counters & Epistemic Separation

The differential derivation tool (`tools/derive_b3_differential.py`) evaluates 22 discrete dimensions across 10 disaggregated counter families:

```json
{
  "original_static_evidence_total": 9,
  "original_static_evidence_passed": 9,
  "exact_framing_total": 3,
  "exact_framing_passed": 3,
  "reconstructed_runtime_e2e_total": 1,
  "reconstructed_runtime_e2e_passed": 1,
  "original_agent_runtime_parity_total": 0,
  "original_agent_runtime_parity_passed": 0,
  "phase_scope_guard_total": 2,
  "phase_scope_guard_passed": 2,
  "reference_only_total": 1,
  "reference_only_passed": 1,
  "implementation_choice_total": 5,
  "implementation_choice_passed": 5,
  "environment_unavailable_total": 1,
  "verified_divergence_total": 0,
  "failed_total": 0
}
```

**Overall Closure Verdict**: `PASS_PHASE_2C5B3_CLOSED`

### Epistemic Classification Summary
- **STATIC_CONFIRMED (9/9 PASS)**: Original binary strings, disassembly handler addresses (`0x9e3f20`), `start_upload` discriminator, field presence (`filename`, `size`, `sha256`, `install`).
- **EXACT_FRAMING (3/3 PASS)**: Text/JSON framing for metadata, raw binary framing for chunks, reject binary before metadata.
- **RUNTIME_RECONSTRUCTED_E2E (1/1 PASS)**: Real SCTP multi-chunk upload with byte-exact payload reconstruction.
- **ORIGINAL_AGENT_RUNTIME_PARITY (0/0, 1 ENVIRONMENT_UNAVAILABLE)**: Android device runtime remains unavailable in cleanroom host environment; explicitly recorded as unavailable rather than claimed as PASS.
- **PHASE_SCOPE_GUARD (2/2 PASS)**: Deferred channels (`camera`, `ai`, `adb`) inert; package installation (`pm install`) strictly deferred.
- **REFERENCE_ONLY (1/1 PASS)**: Frontend chunking size (64KB) traced from `useWebRTC.js`.
- **IMPLEMENTATION_CHOICE (5/5 PASS)**: Go `FileSink` abstraction, defensive `SanitizeFilename`, state machine internal names, checksum mismatch abort, concurrent cleanup.

---

## 9. Negative Mutation Test Suite

`tools/derive_b3_differential.py` includes 6 automated negative mutation tests:
1. **Mutation Case 1**: Missing `start_upload` field in artifact $\rightarrow$ **REJECTED** (`FAILED`).
2. **Mutation Case 2**: Corrupted framing matrix encoding $\rightarrow$ **REJECTED** (`FAILED`).
3. **Mutation Case 3**: Missing disassembly string xref $\rightarrow$ **REJECTED** (`FAILED`).
4. **Mutation Case 4**: Failing E2E subtest $\rightarrow$ **REJECTED** (`FAILED`).
5. **Mutation Case 5**: Missing required E2E subtest $\rightarrow$ **REJECTED** (`FAILED`).
6. **Mutation Case 6**: Dropping mandatory contract requirement $\rightarrow$ **REJECTED** (`FAILED`).

---

## 10. Concurrency & Race Verification Gate

Both reconstructed repositories were compiled and tested with `-race` enabled under LLVM-MinGW GCC:
- **`cloudphone-agent`**: `go test -race -count=1 ./...` $\rightarrow$ **PASS** (zero data races).
- **`webrtc-signaling`**: `go test -race -count=1 ./...` $\rightarrow$ **PASS** (zero data races).

---

## 11. Cleanroom Master Verifier Status

Execution of `python tools/verify_phase2.py`:
- All 22 audit sections evaluated: **22/22 PASS**.
- Zero repository mutations during verification.
- **Overall Audit Verdict**: **PASS**.
