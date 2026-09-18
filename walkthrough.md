# Walkthrough: Phase 2C.5B5F AI-Command Channel Forensic & Schema Reconstruction

**Status**: CLOSED & PASS  
**Base Commit**: `69aa5c7306456eb8257220a19b7f6754acbb2369`  
**Step B5F-A Commit**: `ce3e2f8319f3ec7612f0049405d415b3a4a06aa6`  
**Step B5F-B Commit**: `dc4320f92ce5ef6b0744c66ff6d6350f58097d74`  
**Core Verdict**: **AI command wire schema is reconstructed; runtime command execution remains intentionally unimplemented.**

---

## 1. Two-Step Execution Overview

In strict adherence to the approved B5F plan and all 25 precision rules:
1. **Step B5F-A (Forensic Freeze)**:
   - Disassembly extraction performed via portable LLVM toolchain discovery (`llvm-objdump` v22.1.8) on ARM64 (`cloudphone-agent`) and AMD64 (`cloudphone-agent-amd64`).
   - Symmetrical 6-stage disassembly manifest created: `tools/forensics/ai_command/ai_command_disassembly_manifest.json` (`a5e968b78ce9...`).
   - Protocol specification (`AI_COMMAND_B5F_PROTOCOL_SPEC.json`), message inventory (`AI_COMMAND_B5F_MESSAGE_INVENTORY.json`), callgraph (`AI_COMMAND_B5F_CALLGRAPH.json`), and evidence provenance (`AI_COMMAND_B5F_SOURCE_PROVENANCE.json`) compiled.
   - Implementation contract (`AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json`) frozen with SHA-256 `64642e153dcefaa2857fdc37f16b7dc076915c56aa1b3777519eb0c0d6dbdf65`.
   - Non-mutating reproducer (`reproduce_ai_command_forensics.py --check`) and 12-case negative mutation suite (`test_ai_command_forensics_negative.py`) created.
   - Committed and pushed as `ce3e2f8`.
2. **Step B5F-B (Safe Schema & Verification)**:
   - Clean-room safe parser and schema implemented in `reconstructed_source/cloudphone-agent/pkg/webrtc/ai_command.go` (zero `os/exec`, zero process launch, zero execution adapters).
   - Comprehensive unit test suite created in `reconstructed_source/cloudphone-agent/pkg/webrtc/ai_command_test.go`.
   - Phase policy `B5F` implemented in `tools/audit/b2_common.py`.
   - Historical differential evaluators (`derive_b2_differential.py`, `derive_b3_differential.py`, `derive_b4_differential.py`) pinned to baseline manifests per Rule 15.
   - Master verifier (`tools/verify_phase2.py`) updated with Section 25 (6 comprehensive B5F checks).
   - Audit report `reports/35F_PHASE2C5B5_AI_COMMAND_FORENSIC_SCHEMA.md` created.
   - Committed and pushed as `dc4320f`.

---

## 2. Key Forensic Precision Corrections Implemented

| Area | Former / Inexact State | B5F Authoritative Forensic Invariant | Classification |
|---|---|---|---|
| **Directional Framing** | Generic "JSON text" or "JSON_TEXT_IN_ARRAYBUFFER" | **Directional Split**: Browser &rarr; Agent request is `JSON_TEXT` (text frame in Lane D); Agent &rarr; Browser response is `BINARY_JSON_BYTES` sent via `(*DataChannel).Send([]byte)` (`0x49a3d0` / `0x9250c0`), NOT `SendText`. | `STATIC_CONFIRMED` |
| **Ordered Property** | Marked `STATIC_CONFIRMED` for inbound channel | `ordered=true` is set by browser `pc.createDataChannel('ai-command-channel', { ordered: true })`. Agent does not inspect or validate channel ordered flag. | `REFERENCE_ONLY` |
| **Request Validation** | Inferred required fields from struct | Original binary performs zero non-empty checks. Fields `request_id` and `command` are `KNOWN_FIELDS`. Non-empty rejection in `ValidateAICommand()` is `IMPLEMENTATION_CHOICE / DEFENSIVE_VALIDATION`. | `STATIC_CONFIRMED` / `DEFENSIVE_VALIDATION` |
| **Malformed JSON** | Inferred silent drop from frontend | Disassembly machine-binds: logs `[AI-Command] Error parsing request JSON: %v` (`0x6d5f36` / `0xb77ed7`) and immediately returns (`ret` / `retq`) with zero response sent over DataChannel (`LOG_AND_DROP`). | `STATIC_CONFIRMED` |
| **RequestID Correlation** | Frontend Promise-map assumption | Worker closure captures `req.RequestID` and inserts it directly into response map key `"request_id"`. | `STATIC_CONFIRMED` |
| **Execution Boundary** | Vague "AI automation engine" | Explicitly identified as external process boundary: `os/exec.Command("sh", "-c", req.Command)`. Clean-room agent strictly omits execution. | `DEFERRED_EXECUTION_BOUNDARY` |
| **Concurrency** | Unspecified | Spawns worker goroutine via `runtime.newproc` (`0x5f730` / `0x451c40`) per accepted request. No worker pool or rate limiter. | `STATIC_CONFIRMED` |

---

## 3. Verification & Test Evidence

### 3.1 Go Unit Tests
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

### 3.2 B5F Forensic Reproducer (`--check`)
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

### 3.3 B5F Negative Mutation Test Suite
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

### 3.4 Historical Differential & Master Verifier Gates
- `python tools/derive_b2_differential.py --check` &rarr; `PASS` (0 failures, exact match)
- `python tools/derive_b3_differential.py --check` &rarr; `PASS` (0 failures, exact match)
- `python tools/derive_b4_differential.py --check` &rarr; `PASS` (0 failures, 21/21 mutations rejected)
- `python tools/verify_phase2.py` &rarr; `OVERALL AUDIT VERDICT: PASS` (all 26 sections pass, tree strictly clean)

---

## 4. Cryptographic Signatures

| Artifact | SHA-256 Checksum |
|---|---|
| `AI_COMMAND_B5F_PROTOCOL_SPEC.json` | `aef2aac903e0fc1be312dc4c1bbf0e53eb5cb24c25ca373b06127c53fd36501f` |
| `AI_COMMAND_B5F_MESSAGE_INVENTORY.json` | `3fa26da4d0c5474ea9592c3bb4e4abef180dd7d715030aa8cfa5917abcc3579b` |
| `AI_COMMAND_B5F_CALLGRAPH.json` | `331952995081030871416960df82ce4517f755cadfdb2e8fe9a50631babc9e15` |
| `AI_COMMAND_B5F_SOURCE_PROVENANCE.json` | `0bfedc7aff0661a951e4a9970a3d025812f65d2b6dfb1852e024fbb083661ccc` |
| `AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json` | `64642e153dcefaa2857fdc37f16b7dc076915c56aa1b3777519eb0c0d6dbdf65` |
| `tools/forensics/ai_command/ai_command_disassembly_manifest.json` | `a5e968b78ce9c73abdf43c170d2d6f561be8428cb55ee9397b109faafdaf2217` |

---

## 5. Scope & Safety Invariant

- **Zero OS/Exec**: `os/exec`, `exec.Command`, `sh -c`, `os.StartProcess` strictly absent from reconstructed code.
- **Zero Production Business Handler**: `ai-command-channel` has zero `OnMessage` business handler attached in `cloudphone-agent` production runtime.
- **Inert ADB**: `adb-channel` remains completely unattached and inert.
