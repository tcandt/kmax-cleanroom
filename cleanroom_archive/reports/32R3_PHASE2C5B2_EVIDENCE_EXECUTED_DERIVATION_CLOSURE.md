# Phase 2C.5B2R3 — Evidence-Executed Differential Derivation & Parity Audit Closure Report

**Evaluation Timestamp**: 2026-09-17T19:20:00Z  
**Phase**: Phase 2C.5B2R3 (Evidence-Executed Differential Derivation Closure)  
**Canonical Remote Base**: `3c5a9c24ff843626f942ae58ec0f782cf782e37c`  
**Classification**: Clean-room behavioral/protocol reconstruction & verifiable audit  
**Status**: **PASS — PHASE 2C.5B2 CLOSED**  
**Boundary Gate**: Phase 2C.5B3 (`file-channel`) has **NOT** been started.

---

## 1. Executive Summary & Epistemic Tautology Elimination

In Phase 2C.5B2R2, strict enums, dynamic contract coverage, and toolchain provenance were established. However, the differential derivation tool (`tools/derive_b2_differential.py`) still relied on syntactic shortcuts:
1. Static evidence was accepted based on loose file presence with fallback `return True`.
2. Binary golden frames (`EXACT_BINARY_FRAME`) were marked `PASS` if the test name was found in `control_test.go` source text, rather than executing the test.
3. Runtime SCTP E2E (`RUNTIME_RECONSTRUCTED_E2E`) was marked `PASS` if `TestWebRTCDataChannelsE2E` was in `webrtc_e2e_test.go` source text, without executing the test or attributing individual sub-observations.
4. Semantic parity (`SEMANTIC_PARITY`) returned unconditional `PASS`.

**Phase 2C.5B2R3 completely eliminates all four shortcuts with evidence-executed derivation:**
- **Zero Production Modification**: All 7 production source files remain 100% frozen with pre-R3 SHA256 invariants preserved.
- **Attributable SCTP Subtests**: `TestWebRTCDataChannelsE2E` refactored into subtests (`input`, `clipboard_set`, `clipboard_get`) while preserving the full real SCTP DataChannel path.
- **Machine-Executed Tests**: Both golden tests and SCTP E2E tests are executed via `go test -json -count=1` and parsed at the event level.
- **Structured Static References**: All 9 static dimensions use RFC 6901 JSON pointers and type-safe value comparison across repo-relative boundaries.
- **Shared Pure Audit Primitives**: `tools/audit/b2_common.py` encapsulates whole-tree deferred channel scanning, RFC 6901 resolution, and Android prerequisite matrix evaluation without duplication.
- **Master Verifier Temp Regeneration**: Master Verifier executes `tools/derive_b2_differential.py --check --output <temp>`, verifies normalized semantic equality against canonical evidence, and executes 14 negative mutation tests (Cases A–N) without mutating canonical files.

---

## 2. Production Source Freeze & Cryptographic Verification

The B2 production implementation and module dependencies were strictly frozen throughout R3. Pre-R3 and post-R3 hashes match bit-for-bit:

| Component | File Path | Verified SHA-256 Hash | Status |
|---|---|---|---|
| Control Framing | `reconstructed_source/cloudphone-agent/pkg/webrtc/control.go` | `64cb09b302929105c34076697e45bcea1a8308fed3d161601c0681a9d133febe` | **FROZEN** |
| Clipboard Manager | `reconstructed_source/cloudphone-agent/pkg/webrtc/clipboard.go` | `1c5812b0ddaf404c5d79829baf7b165dc5e59de809cd0b5efbc6f4e65b80a714` | **FROZEN** |
| DataChannel Dispatch | `reconstructed_source/cloudphone-agent/pkg/webrtc/datachannel.go` | `7503b4b67b3d373860d03e430e02d344abdb8943295b9f887cb70ee2ca0b7c96` | **FROZEN** |
| PeerSession Coordinator | `reconstructed_source/cloudphone-agent/pkg/webrtc/peer.go` | `a316e275b1152a9526bb15c48198c49e5f5dcc07d9a2bbf0c25874c68e811bfb` | **FROZEN** |
| Agent Lifecycle | `reconstructed_source/cloudphone-agent/pkg/agent/agent.go` | `6500ebe1dc3c84811ba9d2cd26950ebeb08cc78a823d1aeda6ad8e8cced0eb66` | **FROZEN** |
| Agent Module Definition | `reconstructed_source/cloudphone-agent/go.mod` | `62758ee97e7dccbfd6834b1c26b94f5c8c3724a789bf3d3fe5733a6077fe534b` | **FROZEN** |
| Agent Checksums | `reconstructed_source/cloudphone-agent/go.sum` | `3ac9a4dc369d427e565fefdba667f825b4b79f659c75e6591e7f3be7330903a4` | **FROZEN** |
| Frozen Contract | `evidence/go_agent/webrtc/DATACHANNEL_B2_IMPLEMENTATION_CONTRACT.json` | `3d7ebd83a675b2eb2103813a063cf012def36b98b4303f146b8b1c60ebaaa6f7` | **FROZEN** |

---

## 3. Evidence-Executed Derivation Engine

### 3.1 Structured Static Evidence References (9 Dimensions)
Every static dimension specifies structured locators with RFC 6901 JSON pointers, safe repo-relative paths, and type-safe value comparison:
- `DC-B2-DIM-01` (`input_channel_label`): `DATACHANNEL_LABEL_EVIDENCE.json` pointer `/confirmed_webrtc_channels/input-channel/label` $\rightarrow$ `"input-channel"` (PASS).
- `DC-B2-DIM-02` (`input_channel_ordered`): `DATACHANNEL_LABEL_EVIDENCE.json` pointer `/confirmed_webrtc_channels/input-channel/ordered` $\rightarrow$ `True` (PASS).
- `DC-B2-DIM-03` (`input_channel_json_framing`): `DATACHANNEL_FRAMING_MATRIX.json` pointer `/channels/input-channel/payload_encoding` $\rightarrow$ `"JSON_TEXT"` (PASS).
- `DC-B2-DIM-04` (`clipboard_channel_label`): `DATACHANNEL_LABEL_EVIDENCE.json` pointer `/confirmed_webrtc_channels/clipboard-channel/label` $\rightarrow$ `"clipboard-channel"` (PASS).
- `DC-B2-DIM-05` (`clipboard_channel_ordered`): `DATACHANNEL_LABEL_EVIDENCE.json` pointer `/confirmed_webrtc_channels/clipboard-channel/ordered` $\rightarrow$ `True` (PASS).
- `DC-B2-DIM-06` (`clipboard_channel_json_framing`): `DATACHANNEL_FRAMING_MATRIX.json` pointer `/channels/clipboard-channel/payload_encoding` $\rightarrow$ `"JSON_TEXT"` (PASS).
- `DC-B2-DIM-12` (`set_clipboard_handling`): `DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json` pointer `/clipboard_channel_messages/set_clipboard/classification` $\rightarrow$ `"STATIC_CONFIRMED"` (PASS).
- `DC-B2-DIM-13` (`get_clipboard_handling`): `DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json` pointer `/clipboard_channel_messages/get_clipboard/classification` $\rightarrow$ `"STATIC_CONFIRMED"` (PASS).
- `DC-B2-DIM-14` (`clipboard_response_schema`): `DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json` pointer `/clipboard_channel_messages/get_clipboard/fields/0` $\rightarrow$ `"type"` (PASS).

### 3.2 Executed Binary Golden Frame Tests (5 Dimensions)
Command: `go test -json -count=1 -run='^(TestGoldenTouchEvent|TestGoldenKeycodeEvent|TestGoldenTextEvent|TestGoldenScrollEvent|TestGoldenHardKeyboardEvent)$' ./pkg/webrtc`  
- Package Exit Code: `0` (`PASS`)
- `DC-B2-DIM-07`: `TestGoldenTouchEvent` $\rightarrow$ `Action: pass` (0.00s)
- `DC-B2-DIM-08`: `TestGoldenKeycodeEvent` $\rightarrow$ `Action: pass` (0.00s)
- `DC-B2-DIM-09`: `TestGoldenTextEvent` $\rightarrow$ `Action: pass` (0.00s)
- `DC-B2-DIM-10`: `TestGoldenScrollEvent` $\rightarrow$ `Action: pass` (0.00s)
- `DC-B2-DIM-11`: `TestGoldenHardKeyboardEvent` $\rightarrow$ `Action: pass` (0.00s)

### 3.3 Executed Runtime SCTP DataChannel E2E Tests (3 Dimensions)
Command: `go test -json -count=1 -run='^TestWebRTCDataChannelsE2E$' ./tests`  
- Package Exit Code: `0` (`PASS`)
- Parent Test: `TestWebRTCDataChannelsE2E` $\rightarrow$ `Action: pass` (0.25s)
- `DC-B2-DIM-15`: `TestWebRTCDataChannelsE2E/input` $\rightarrow$ `Action: pass` (0.02s)  
  *Path verified: Browser PeerConnection -> SCTP DataChannel -> Agent OnMessage -> ControlSink (32-byte scrcpy touch frame).*
- `DC-B2-DIM-16`: `TestWebRTCDataChannelsE2E/clipboard_set` $\rightarrow$ `Action: pass` (0.02s)  
  *Path verified: Browser PeerConnection -> SCTP DataChannel -> Agent OnMessage -> ClipboardProvider.Set.*
- `DC-B2-DIM-17`: `TestWebRTCDataChannelsE2E/clipboard_get` $\rightarrow$ `Action: pass` (0.00s)  
  *Path verified: Browser PeerConnection -> SCTP DataChannel -> Agent OnMessage -> ClipboardProvider.Get -> Agent Response -> SCTP DataChannel -> Browser Client.*

### 3.4 Executed Semantic Parity: Deferred Channel Isolation (1 Dimension)
Function: `scan_deferred_channels_isolation(agent_pkg_dir)` in `tools/audit/b2_common.py`.  
- Scanned all production Go files under `reconstructed_source/cloudphone-agent/pkg`.
- Checks performed: OnMessage bindings, camera business logic, file transfer / persistence, AI commands, ADB sockets.
- Result: **0 violations detected** (PASS).

### 3.5 Bounded Android Runtime Prerequisite Matrix (1 Dimension)
Function: `evaluate_android_runtime_prerequisites()`.  
Prerequisite Evaluation on Windows AMD64 desktop:
1. `original_agent_artifact_available`: `False`
2. `compatible_android_target_available`: `False`
3. `app_process_available`: `False`
4. `helper_artifact_available`: `False`
5. `execution_context_shell_uid_2000`: `False`
6. `abstract_uds_support`: `False`
7. `safe_launch_capability`: `False`  
- Overall Result: `ENVIRONMENT_UNAVAILABLE` (0/0 original-agent parity claimed, failed=0).

### 3.6 Reference-Only & Implementation-Choice Validation (7 Dimensions)
- Explicit semantic: Provenance classification and compatibility behavior validated; excluded from original protocol parity counters.
- Reference-only dimensions (`DC-B2-DIM-19`, `DIM-20`, `DIM-21`): Verified against `evidence/reference/raw/web-app/src/composables/useWebRTC.js`.
- Implementation-choice dimensions (`DC-B2-DIM-22`, `DIM-23`, `DIM-24`, `DIM-25`): Adapter and robustness tests executed and verified.

---

## 4. Differential Result Counters & Verdict

From [`evidence/go_agent/webrtc/DATACHANNEL_B2_DIFFERENTIAL_RESULT.json`](file:///d:/KMAX-CLEANROOM/evidence/go_agent/webrtc/DATACHANNEL_B2_DIFFERENTIAL_RESULT.json):

```json
{
  "counters": {
    "static_protocol_evidence_total": 9,
    "static_protocol_evidence_passed": 9,
    "exact_binary_frame_total": 5,
    "exact_binary_frame_passed": 5,
    "reconstructed_runtime_e2e_total": 3,
    "reconstructed_runtime_e2e_passed": 3,
    "original_agent_runtime_parity_total": 0,
    "original_agent_runtime_parity_passed": 0,
    "semantic_parity_total": 1,
    "semantic_parity_passed": 1,
    "reference_only_total": 3,
    "implementation_choice_total": 4,
    "environment_unavailable_total": 1,
    "verified_divergence_total": 0,
    "failed_total": 0
  },
  "overall_verdict": "PASS_PHASE_2C5B2_CLOSED"
}
```

---

## 5. Extended Negative Mutation Testing (14/14 Cases Rejected)

Master Verifier Section 21.4 executes 14 negative mutation tests in memory against isolated copies of the payload, verifying both evaluator and validator fail-closed behavior:

| Case | Mutation Injected | Expected Rejection Reason | Status |
|---|---|---|---|
| **Case A** | STATIC result `PASS` $\rightarrow$ `FAILED` | `failed_total > 0` | **PASS** (Rejected) |
| **Case B** | STATIC result `PASS` $\rightarrow$ `"FAIL"` | Illegal enum string | **PASS** (Rejected) |
| **Case C** | Delete mandatory contract dimension (`DC-B2-01`) | Uncovered mandatory requirement | **PASS** (Rejected) |
| **Case D** | Duplicate dimension ID | Duplicate dimension ID detected | **PASS** (Rejected) |
| **Case E** | Tamper stored counter (`total`: 9 $\rightarrow$ 10) | Counter mismatch | **PASS** (Rejected) |
| **Case F** | Remove `evidence_basis` | Empty evidence basis | **PASS** (Rejected) |
| **Case G** | Original runtime $\rightarrow$ `PASS` without oracle | Oracle absence invariant | **PASS** (Rejected) |
| **Case H** | Static locator pointing to nonexistent artifact | Evaluator returns `FAILED` | **PASS** (Rejected) |
| **Case I** | Static json_pointer pointing to nonexistent field | Pointer resolution returns `FAILED` | **PASS** (Rejected) |
| **Case J** | Static expected value mismatch | Type-safe comparison returns `FAILED` | **PASS** (Rejected) |
| **Case K** | Simulated golden test execution failure | Golden evaluator returns `FAILED` | **PASS** (Rejected) |
| **Case L** | Mapped golden test missing from test events | Golden evaluator returns `FAILED` | **PASS** (Rejected) |
| **Case M** | SCTP E2E subtest failure (`Action: fail`) | E2E evaluator returns `FAILED` | **PASS** (Rejected) |
| **Case N** | Injected deferred-channel scanner violation | Semantic evaluator returns `FAILED` | **PASS** (Rejected) |

---

## 6. Portable Toolchain Discovery & Concurrency Gate

Discovered Toolchain:
- **Discovery Method**: `WINDOWS_USER_REGISTRY_PATH` (`HKCU\Environment\Path`)
- **Compiler**: `gcc.exe`
- **Compiler Version**: `clang version 22.1.8 (Target: x86_64-w64-windows-gnu)`
- **Compiler SHA-256**: `a8b7a614eeadd9105f814be3701a7f312cda4cea51751b75b408c16100c94e85`
- **Toolchain Provenance Status**: `SAME_CANONICAL_TOOLCHAIN` (matches canonical [`evidence/metadata/TOOLCHAIN.json`](file:///d:/KMAX-CLEANROOM/evidence/metadata/TOOLCHAIN.json))

Executed Race Detection:
- `cloudphone-agent`: `go test -race -count=1 ./...` $\rightarrow$ **PASS** (0 data races)
- `webrtc-signaling`: `go test -race -count=1 ./...` $\rightarrow$ **PASS** (0 data races)

---

## 7. Full Regression Suite Results

All regressions executed uncached (`-count=1`):

1. **B2 Differential Regeneration & Self-Audit**:
   `python tools/derive_b2_differential.py --check` $\rightarrow$ **PASS** (`PASS_PHASE_2C5B2_CLOSED`)
2. **WebRTC & DataChannel Forensic Reproducibility**:
   `python tools/forensics/reproduce_webrtc_datachannel_forensics.py` $\rightarrow$ **PASS** (**14/14** artifacts verified)
3. **Transport Forensic Reproducibility**:
   `python tools/forensics/reproduce_transport_forensics.py` $\rightarrow$ **PASS** (**23/23** artifacts verified)
4. **Transport Differential Parity Test**:
   `python tools/transport_differential_test.py` $\rightarrow$ **PASS** (**48/48** exact parity cases passed)
5. **Go Unit & E2E Tests**:
   - `cloudphone-agent`: `go test ./...` $\rightarrow$ **PASS** (18 test cases + 3 subtests)
   - `webrtc-signaling`: `go test ./...` $\rightarrow$ **PASS** (all packages)
6. **Master Verifier (`python tools/verify_phase2.py`)**:
   - Section 21.2: Deferred Channels Strict Isolation Audit $\rightarrow$ **PASS** (0 violations)
   - Section 21.3: Input & Clipboard Real SCTP DataChannel E2E Parity $\rightarrow$ **PASS**
   - Section 21.4: Dynamic derivation, temp regeneration, 14/14 mutations $\rightarrow$ **PASS**
   - Section 21.5: Concurrency and Race Gate (`go test -race ./...`) $\rightarrow$ **PASS** (`SAME_CANONICAL_TOOLCHAIN`)
   - Section 21.6: Non-Mutating Audit Invariant $\rightarrow$ **PASS** (`git status --porcelain` empty)
   - **OVERALL AUDIT VERDICT: PASS**

---

## 8. Final Closure Verdict

| Component | Status | Verification Authority |
|---|---:|---|
| B2 Production Implementation | **PASS** | Frozen pre-R3 SHA256 hashes verified |
| Binary Golden Framing | **PASS** | `go test -json -count=1` executed, 5/5 subtest events passed |
| Real SCTP Input & Clipboard E2E | **PASS** | `go test -json -count=1` executed, 3/3 subtest events passed |
| Static Protocol Evidence | **PASS** | 9/9 structured RFC 6901 pointers resolved and type-safe matched |
| Deferred Channel Strict Isolation | **PASS** | Whole-tree scanner verified 0 violations |
| Original Agent Environment Attribution | **PASS** | Prerequisite matrix evaluated, recorded as `ENVIRONMENT_UNAVAILABLE` |
| Differential Derivation Independence | **PASS** | Temp regeneration matches canonical, 14/14 mutations rejected |
| Concurrency & Race Safety | **PASS** | `go test -race -count=1 ./...` executed cleanly with canonical toolchain |
| **Phase 2C.5B2 Final Closure** | **CLOSED** | Formal closure criteria fully satisfied |

**EXECUTION IS STOPPED. Phase 2C.5B3 (`file-channel`) has NOT been started.**
