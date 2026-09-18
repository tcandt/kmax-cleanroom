# Phase 2C.5B5F Audit Report: WebRTC AI-Command DataChannel Forensic Extraction & Safe Schema Reconstruction

**Status**: FORMALLY CLOSED  
**Phases Covered**: Phase 2C.5B5F-A (Forensic Extraction & Baseline Freeze) + Phase 2C.5B5F-B (Safe Schema/Parser Reconstruction & Audit Gate)  
**Base Commit**: `69aa5c7306456eb8257220a19b7f6754acbb2369`  
**Step A Freeze Commit**: `ce3e2f8319f3ec7612f0049405d415b3a4a06aa6`  
**Core Verdict**: **AI command wire schema is reconstructed; runtime command execution remains intentionally unimplemented.**

---

## 1. Executive Summary & Scope Boundaries

Phase 2C.5B5F achieves formal forensic closure of the WebRTC `ai-command-channel` subsystem across the original Android ARM64 and Linux AMD64 `cloudphone-agent` binaries, establishing an authoritative protocol contract and implementing a strictly inert, clean-room safe data parser and schema.

### 1.1 Strict Tripartite Distinction
In accordance with precision corrections, all artifacts and descriptions maintain an uncompromised distinction between:
1. **ORIGINAL BINARY BEHAVIOR**: The exact machine-bound instructions, dataflow, rodata strings, and execution paths recovered from the original binaries.
2. **RECONSTRUCTED SAFE PARSER**: Clean-room Go data structures and pure decoding/encoding functions (`AICommandEnvelope`, `AICommandResponse`, `ParseAICommand`, `ValidateAICommand`, `MarshalAICommandResponse`) containing zero execution logic.
3. **DEFERRED EXECUTION BOUNDARY**: The original binary's invocation of an external process shell (`os/exec.Command("sh", "-c", req.Command)`), which is formally classified as `DEFERRED_EXECUTION_BOUNDARY` / `EXTERNAL_PROCESS_CANDIDATE` and strictly omitted from the reconstructed agent.

### 1.2 Two-Step Closure Execution
- **Step B5F-A**: Forensic extraction, protocol specification, message inventory, callgraph, provenance matrix, implementation contract freeze (`64642e153dce`), non-mutating reproducer (`--check`), and 12 negative mutation tests. Committed and pushed as `ce3e2f8`.
- **Step B5F-B**: Safe parser/schema implementation (`pkg/webrtc/ai_command.go`), unit test suite (`ai_command_test.go`), B5F boundary scanner policy in `b2_common.py`, master verifier integration (Section 25 in `verify_phase2.py`), and comprehensive audit reporting.

---

## 2. Machine-Bound Disassembly Evidence & Protocol Findings

Extraction was conducted using portable LLVM toolchain discovery (`llvm-objdump` v22.1.8) on both original agent binaries:
- **ARM64**: `cloudphone-v0.3.6 (1)/android/cloudphone-agent` (`9cc32ea3cffe...`)
- **AMD64**: `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-amd64` (`15adc2a4c47c...`)

All extracted snippets are canonically stored in `tools/forensics/ai_command/ai_command_disassembly_manifest.json` (`a5e968b78ce9...`).

### 2.1 Inbound Channel Dispatch & Label Matching
- **Channel Label**: Exact string `"ai-command-channel"` (18 bytes / `0x12`).
  - ARM64: rodata at `0x6bd173`, compared via `runtime.memequal` (`0x15440`) at `0x53f288`-`0x53f2ac`.
  - AMD64: rodata at `0xb5f1c2`, compared via `runtime.memequal` (`0x406ce0`) at `0x9e2f80`-`0x9e2fa8`.
- **Dispatcher Site**: Inside `pc.OnDataChannel` callback closure:
  - ARM64: `main.(*JJffa1S1Zv6).iIhwd_WXInS.func11` (`0x53f210`).
  - AMD64: `main.(*IDhLgq).woxaqqFN5Km.func11` (`0x9e2f20`).

### 2.2 Callback Registration & Lifecycle Scoping
- **Registered Handler**: The dispatcher sets only `(*DataChannel).OnMessage`:
  - ARM64: `0x53f45c` calls `0x499770` (`IV04EXWpwj.(*F4TaFEL9SI).OnMessage`), registering closure `0x53f5d0` (`cemlVcjsE0LQ.2`).
  - AMD64: `0x9e3129` calls `0x9244a0` (`v6LoFegGUKTA.(*W4J6chbzBu).OnMessage`), registering closure `0x9e32c0` (`drnM2wXuIb.2`).
- **Absence of OnOpen/OnClose**: "No branch-specific OnOpen or OnClose registration was recovered in the ai-command-channel dispatch path."

### 2.3 Directional Framing Resolution
Disassembly and reference evidence prove that framing differs across directions:
| Direction | Wire Transport | Framing Classification | Evidence Basis |
|---|---|---|---|
| **Browser &rarr; Agent (Request)** | WebRTC DataChannel | `JSON_TEXT` | Lane D reference (`useWebRTC.js:311`) executes `aiCommandChannel.send(JSON.stringify(...))`. Go Pion delivers payload as `[]byte` in `msg.Data` to `json.Unmarshal`. |
| **Agent &rarr; Browser (Response)** | WebRTC DataChannel | `BINARY_JSON_BYTES` | Lane A disassembly (`0x53f9e8` / `0x9e374a`) calls `(*DataChannel).Send([]byte)`, **NOT** `SendText`. Payload is JSON serialized bytes sent as a binary frame. Frontend handles both string and `ArrayBuffer` via `TextDecoder` (`REFERENCE_ONLY`). |

### 2.4 Request Struct & Validation Semantics
- **Anonymous Struct**: 32 bytes allocated at ARM64 `0x60e660` / AMD64 `0xab0be0`:
  - Field 0 (`offset 0`): `string`, tagged `json:"request_id"`
  - Field 1 (`offset 16`): `string`, tagged `json:"command"`
- **Validation Semantics**: The original disassembly proceeds directly to logging and goroutine launch upon `json.Unmarshal` success (`err == nil`). **Zero comparison or length checks are performed on `request_id` or `command`.**
  - Schema fields are classified as `KNOWN_FIELDS`.
  - Reconstructed `ValidateAICommand()` rejecting empty strings is strictly an `IMPLEMENTATION_CHOICE / DEFENSIVE_VALIDATION`, not original binary parity.
- **Malformed JSON Semantics**: On unmarshal error, the binary logs `[AI-Command] Error parsing request JSON: %v` (ARM64 `0x6d5f36`, AMD64 `0xb77ed7`) and immediately executes `ret`/`retq` (`0x53f668` / `0x9e336a`) without transmitting any response over the DataChannel (`LOG_AND_DROP`).

### 2.5 Concurrency Model
- **Goroutine per Request**: Upon valid unmarshal, the agent logs `[AI-Command] Executing P2P command (id=%s): %s` (ARM64 `0x6d86f2`, AMD64 `0xb7a693`), allocates worker closure (`0x53f740` / `0x9e3460`), and calls `runtime.newproc` (`0x5f730` / `0x451c40`).
- Classified as `GOROUTINE_PER_ACCEPTED_REQUEST = STATIC_CONFIRMED`. No worker pool, queue capacity, or rate limiter was recovered.

### 2.6 Deferred Downstream Execution Boundary
- **Worker Process Invocation**: The worker loads `"sh"` (`0x6ac000` / `0xb4e032`) and `"-c"` (`0x6ac002` / `0xb4e034`), calls `exec.Command` (`0x196e70` / `0x5a1c00`), captures stdout/stderr buffers, calls `cmd.Run`, and extracts the exit code (0 on success, `ExitCode()` on `exec.ExitError`, -1 on other failure).
- **Clean-Room Policy**: Formally classified as `DEFERRED_EXECUTION_BOUNDARY` / `EXTERNAL_PROCESS_CANDIDATE`. Strictly omitted from reconstructed source code.

### 2.7 Response Struct & Correlation Echo
- **Response Construction**: Response map built with rodata keys:
  - `"request_id"` (`0x6b3a5b` / `0xb55aee`, len 10)
  - `"exit_code"` (`0x6b1f17` / `0xb53f84`, len 9)
  - `"stdout"` (`0x6ade37` / `0xb4fe64`, len 6)
  - `"stderr"` (`0x6ade3d` / `0xb4fe6a`, len 6)
- **Serialization & Send**: Marshaled via `json.Marshal` (`0x1317c0` / `0x531b60`) and transmitted via `(*DataChannel).Send` (`0x49a3d0` / `0x9250c0`).
- **Correlation Echo**: Closure captures incoming `req.RequestID` and inserts it directly into `"request_id"`. Classified as `EXACT_REQUEST_ID_ECHO = STATIC_CONFIRMED`.

---

## 3. Formal Historical Errata & Superseded Evidence

In compliance with audit rules, historical evidence files remain immutable, while errata and superseding findings are formally cataloged in `AI_COMMAND_B5F_PROTOCOL_SPEC.json`:

1. **Directional Framing Supersession**:
   - *Historical Artifact*: `evidence/go_agent/webrtc/DATACHANNEL_FRAMING_MATRIX.json` previously noted `JSON_TEXT_IN_ARRAYBUFFER`.
   - *Superseded By*: Independent directional framing in B5F: Request is `JSON_TEXT`, Response is `BINARY_JSON_BYTES` via `(*DataChannel).Send([]byte)`.
2. **Inbound Ordered Classification Erratum**:
   - *Historical Artifact*: `evidence/go_agent/webrtc/DATACHANNEL_LABEL_EVIDENCE.json` previously marked inbound channel ordered property as `STATIC_CONFIRMED (Disassembly passes ordered=1 byte pointer to CreateDataChannel)`.
   - *Erratum Corrected*: The agent binary never invokes `CreateDataChannel` for inbound channels and does not check the ordered flag. `ordered=true` is strictly `REFERENCE_ONLY` from browser creation in `useWebRTC.js:359`.

---

## 4. Reconstructed Safe Parser Implementation

The safe parser is located in `reconstructed_source/cloudphone-agent/pkg/webrtc/ai_command.go`:
- **Data Structures**:
  - `type AICommandEnvelope struct { RequestID string, Command string }`
  - `type AICommandResponse struct { RequestID string, ExitCode int, Stdout string, Stderr string }`
- **Functions**:
  - `ParseAICommand(data []byte) (*AICommandEnvelope, error)`: pure JSON decoder.
  - `ValidateAICommand(cmd *AICommandEnvelope) error`: defensive non-empty validation (`IMPLEMENTATION_CHOICE`).
  - `MarshalAICommandResponse(resp *AICommandResponse) ([]byte, error)`: JSON byte encoder for binary DataChannel send.
- **Safety Enforcement**:
  - Zero imports of `os/exec`.
  - Zero command execution calls (`exec.Command`, `sh -c`, `os.StartProcess`).
  - Zero executor interfaces or abstractions (`CommandRunner`, `ProcessRunner`, `ShellExecutor`).
  - Channel remains unattached in `datachannel.go` and `peer.go`.

---

## 5. Phase Policy & Boundary Scanner Hardening

`tools/audit/b2_common.py` was updated with the explicit `phase="B5F"` policy:
- **ACTIVE_RUNTIME**: `input`, `clipboard`, `file`, `camera`.
- **ACTIVE_SAFE**: AI parser and schema symbols (`AICommandEnvelope`, `AICommandResponse`, `ParseAICommand`, `ValidateAICommand`, `MarshalAICommandResponse`).
- **DEFERRED_EXECUTION**: AI OnMessage handler, AI command executor, external process boundary, ADB channel.
- **Historical Invariant Protection**: Historical B2, B3, and B4 scans are pinned to their respective baseline commits (`c84d34aa`, `2a039510`, `7e94bd48`), preserving their original scanner policies without weakening.

---

## 6. Verification Results

All automated verification gates pass cleanly:

### 6.1 Unit Tests & Race Detection
```text
=== RUN   TestParseAICommand_Valid
--- PASS: TestParseAICommand_Valid (0.00s)
=== RUN   TestParseAICommand_MalformedJSON
--- PASS: TestParseAICommand_MalformedJSON (0.00s)
=== RUN   TestParseAICommand_EmptyJSON
--- PASS: TestParseAICommand_EmptyJSON (0.00s)
=== RUN   TestValidateAICommand_DefensiveChecks
--- PASS: TestValidateAICommand_DefensiveChecks (0.00s)
=== RUN   TestMarshalAICommandResponse_Valid
--- PASS: TestMarshalAICommandResponse_Valid (0.00s)
=== RUN   TestMarshalAICommandResponse_Nil
--- PASS: TestMarshalAICommandResponse_Nil (0.00s)
=== RUN   TestAICommand_CorrelationEcho
--- PASS: TestAICommand_CorrelationEcho (0.00s)
PASS: ok cloudphone-agent/pkg/webrtc
```

### 6.2 Forensic Reproducer (`--check`)
```text
=== Phase 2C.5B5F AI-Command Channel Forensic Reproducer ===
Running in --check mode (non-mutating verification)...
✓ Binary disassembly and semantic invariants validated
✓ Disassembly extraction cleanly regenerated in tempdir and matches frozen SHA
✓ AI_COMMAND_B5F_PROTOCOL_SPEC.json:         aef2aac903e0... (MATCH)
✓ AI_COMMAND_B5F_MESSAGE_INVENTORY.json:     3fa26da4d0c5... (MATCH)
✓ AI_COMMAND_B5F_CALLGRAPH.json:             331952995081... (MATCH)
✓ AI_COMMAND_B5F_SOURCE_PROVENANCE.json:     0bfedc7aff06... (MATCH)
✓ AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json: 64642e153dce... (MATCH)
✓ ai_command_disassembly_manifest.json:      a5e968b78ce9... (MATCH)
All B5F forensic reproduction checks PASSED.
```

### 6.3 Negative Mutation Test Suite
```text
[PASS] Case 1: Rejection of Response Framing Swapped to JSON_TEXT (AssertionError)
[PASS] Case 2: Rejection of Request Framing Swapped to RAW_BINARY (AssertionError)
[PASS] Case 3: Rejection of Field Validation Promoted to STATIC (AssertionError)
[PASS] Case 4: Rejection of Inbound Ordered Promoted to Agent STATIC (AssertionError)
[PASS] Case 5: Rejection of Execution Boundary Made Production Requirement (AssertionError)
[PASS] Case 6: Rejection of Parser Presence Treated as Channel Activation (AssertionError)
[PASS] Case 7: Rejection of Corrupted ARM64 Response Send Disassembly (AssertionError)
[PASS] Case 8: Rejection of Corrupted AMD64 newproc Disassembly (AssertionError)
[PASS] Case 9: Rejection of Tampered Channel Label (AssertionError)
[PASS] Case 10: Rejection of Broken Request ID Correlation (AssertionError)
[PASS] Case 11: Rejection of Altered Concurrency Model (AssertionError)
[PASS] Case 12: Rejection of Tampered Implementation Contract Hash (AssertionError)
B5F Negative Mutation Results: 12/12 PASSED
```

### 6.4 Master Verifier Summary (`tools/verify_phase2.py`)
```text
[PASS] Phase 2C.5B5F Frozen Forensic Contract Invariant
[PASS] Phase 2C.5B5F Forensic Reproducer & Negative Mutation Invariant
[PASS] Phase 2C.5B5F Directional Framing & Errata Invariant
[PASS] Phase 2C.5B5F Safe Parser & Unit Tests Invariant
[PASS] Phase 2C.5B5F Production Boundary & Channel Inertness Invariant
[PASS] Phase 2C.5B5F Historical Non-Regression & Differential Stability Invariant
[PASS] Master Verifier Non-Mutating Audit Invariant (Working tree clean)
OVERALL AUDIT VERDICT: PASS
```

---

## 7. Artifact Manifest & Cryptographic Signatures

| Artifact Path | SHA-256 Checksum | Classification |
|---|---|---|
| `evidence/go_agent/webrtc/AI_COMMAND_B5F_PROTOCOL_SPEC.json` | `aef2aac903e0fc1be312dc4c1bbf0e53eb5cb24c25ca373b06127c53fd36501f` | FROZEN_FORENSIC_BASELINE |
| `evidence/go_agent/webrtc/AI_COMMAND_B5F_MESSAGE_INVENTORY.json` | `3fa26da4d0c5474ea9592c3bb4e4abef180dd7d715030aa8cfa5917abcc3579b` | FROZEN_FORENSIC_BASELINE |
| `evidence/go_agent/webrtc/AI_COMMAND_B5F_CALLGRAPH.json` | `331952995081030871416960df82ce4517f755cadfdb2e8fe9a50631babc9e15` | FROZEN_FORENSIC_BASELINE |
| `evidence/go_agent/webrtc/AI_COMMAND_B5F_SOURCE_PROVENANCE.json` | `0bfedc7aff0661a951e4a9970a3d025812f65d2b6dfb1852e024fbb083661ccc` | FROZEN_FORENSIC_BASELINE |
| `evidence/go_agent/webrtc/AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json` | `64642e153dcefaa2857fdc37f16b7dc076915c56aa1b3777519eb0c0d6dbdf65` | FROZEN_FORENSIC_BASELINE |
| `tools/forensics/ai_command/ai_command_disassembly_manifest.json` | `a5e968b78ce9c73abdf43c170d2d6f561be8428cb55ee9397b109faafdaf2217` | DISASSEMBLY_MANIFEST |
| `tools/forensics/ai_command/extract_ai_command_disassembly.py` | — | REPO_LOCAL_TOOLING |
| `tools/forensics/reproduce_ai_command_forensics.py` | — | FORENSIC_REPRODUCER |
| `tools/forensics/test_ai_command_forensics_negative.py` | — | NEGATIVE_MUTATION_SUITE |
| `reconstructed_source/cloudphone-agent/pkg/webrtc/ai_command.go` | — | RECONSTRUCTED_SAFE_PARSER |
| `reconstructed_source/cloudphone-agent/pkg/webrtc/ai_command_test.go` | — | UNIT_TEST_SUITE |
| `reports/35F_PHASE2C5B5_AI_COMMAND_FORENSIC_SCHEMA.md` | — | AUDIT_REPORT |
