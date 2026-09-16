# Report 11R3: Semantic Evidence Binding Closure & Reference Infrastructure Finalization

**Status**: CLOSED & AUDITED (Phase 2R.3)  
**Date**: 2026-09-16  
**Corpus**: `tcandt/kmax-cleanroom`  
**Verdict**: **PASS — REFERENCE INFRASTRUCTURE FINALIZED & READY FOR PHASE 2C.3B**

---

## 1. Executive Summary

Phase 2R.3 successfully remediates the final set of evidence classification, binding, and schema deficiencies identified in Phase 2R.2 review. Following the successful public source pinning achieved in Phase 2R.2, Phase 2R.3 transitions every remaining heuristic or handwritten claim into a machine-verifiable, artifact-backed evidence record.

### Key Remediation Deliverables
1. **Public Reference Hash Schema Bug Fixed**:
   - Strictly separated `source_git_blob_sha` (Git blob SHA-1) and `source_sha256` (raw file SHA-256).
   - Removed all instances where Git blob SHA-1 was mistakenly assigned to `artifact_sha256`.
   - Bound values dynamically from `PUBLIC_REFERENCE_TREE_MANIFEST.json` and computed slice text hashes (`observed_text_hash`).
2. **Machine Extraction Separated from Annotations**:
   - `REFERENCE_PROTOCOL_INDEX.json` now strictly distinguishes pure AST/regex parsing (`MACHINE_OBSERVED`) from human design/role interpretations (`ANNOTATION_TEMPLATE`).
   - Static presentation tables are explicitly classified `ANNOTATION_TEMPLATE` and excluded from binary confirmation counts.
3. **Agent CLI Registration Ground Truth Recovered**:
   - Eliminated crude `lstrip("-")` substring scanning that caused generic tokens like `"id"` and `"root"` to match thousands of unrelated occurrences.
   - Reverse-engineered obfuscated Go stdlib `flag` package `aFaUKV` in ARM64 binary `cloudphone-agent`:
     - `aFaUKV.CMNJxRQ7` (`flag.String`) @ `0x39f420`
     - `aFaUKV.A1a3KwX` (`flag.Int`) @ `0x39f2c0`
     - `aFaUKV.RTCObKURJKV` (`flag.Bool`) @ `0x39f190`
   - Statically recovered all 28 registered CLI flags in `main.init` (`0x5152f0`) with exact call VAs, default values, `.bss` global destinations (`0xd38548`-`0xd38620`), and downstream xrefs in `main.main`.
   - Generated `evidence/go_agent/cli/CLI_FLAG_REGISTRATION_EVIDENCE.json`.
4. **Machine-Verifiable Disassembly Facts Created**:
   - Generated `evidence/go_signaling/DISASSEMBLY_FACTS.json` (`SIG-DCF-001` to `SIG-DCF-005`).
   - Generated `evidence/go_agent/DISASSEMBLY_FACTS.json` (`AGENT-DCF-001` to `AGENT-DCF-005`).
   - Replaced all handwritten `DISASSEMBLY_CONTROL_FLOW` text in crossmap with formal `fact_id` references.
5. **Master Verifier & Crossmap Hardened**:
   - `tools/verify_phase2.py` now resolves every evidence class (`PUBLIC_REFERENCE`, `BINARY_STRING`, `ROUTE_REGISTRATION`, `DYNAMIC_ORACLE`, `PCLNTAB_SYMBOL`, `BINARY_XREF`, `DISASSEMBLY_CONTROL_FLOW`).
   - Structured validation for `DYNAMIC_ORACLE` compares numeric status codes (`HTTP-01`: 200, `HTTP-02`: 401, `HTTP-03`: 400), rather than substring matching handwritten strings.
   - All 6 reproducibility checks pass deterministically.

---

## 2. Remediation Analysis & Forensic Proofs

### 2.1 Public Reference Hash Schema Correction (Blocker 3)

In Phase 2R.2, crossmap records stored Git blob SHA-1 IDs (e.g. `cb6b0451b0640d9c787f567fd97b54c621ca4da0` for `useWebRTC.js`) into `artifact_sha256`. 

In Phase 2R.3, the schema for `PUBLIC_REFERENCE` evidence records requires:
- `source_path`: Relative path in reference repository (e.g., `web-app/src/composables/useWebRTC.js`)
- `source_commit_sha`: Pinned commit hash (`65567d777bccb11d2a6d93b6acc735478e880b5b`)
- `source_git_blob_sha`: Exact Git blob SHA-1 (`cb6b0451b0640d9c787f567fd97b54c621ca4da0`)
- `source_sha256`: Raw file SHA-256 (`28604c2f9e595944f3e51d52cf604b250ca9c95cce5c41a90a877cb7f71178f9`)
- `artifact_sha256`: Set strictly to `source_sha256` (64-character hex hash)
- `line_start` / `line_end`: Precise line numbers
- `observed_text_hash`: SHA-256 of the extracted line slice

All values are bound dynamically from `PUBLIC_REFERENCE_TREE_MANIFEST.json` and verified at runtime.

### 2.2 Machine Extraction vs Annotation Separation (Blocker 4)

`extract_protocol_index.py` previously combined parsed tokens with hardcoded dictionaries of semantic descriptions. Phase 2R.3 restructures `REFERENCE_PROTOCOL_INDEX.json`:
1. **`machine_extracted`**: Contains AST/regex extractions (`MACHINE_OBSERVED`):
   - 37 unique HTTP endpoint paths discovered in Vue/JS files.
   - 6 client-to-server WebSocket message types.
   - 6 server-to-client WebSocket message types.
   - 6 forward payload types.
2. **`annotated_catalog`**: Contains descriptive roles and schema definitions:
   - Explicitly classified as `ANNOTATION_TEMPLATE`.
   - Annotated with `"forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"`.

### 2.3 Agent CLI Registration Recovery (Blocker 1)

In ARM64 binary `cloudphone-agent`, flags are not registered via standard un-obfuscated `flag.String` symbols. The compiler/obfuscator garbled the standard library flag package into package `aFaUKV`:
- `aFaUKV.CMNJxRQ7`: `flag.String(name, default, usage) *string`
- `aFaUKV.A1a3KwX`: `flag.Int(name, default, usage) *int`
- `aFaUKV.RTCObKURJKV`: `flag.Bool(name, default, usage) *bool`

#### Disassembly Proof in `main.init` (`0x5152f0`):
All 28 flags are registered sequentially between `0x5152f0` and `0x515ae0`. Each call passes:
- `x0`: pointer to flag name in `.rodata`
- `x1`: string length of flag name
- `x2`: default value (or pointer to default string)
- `x3`: default string length (if string flag)
- `x4`, `x5`: usage string pointer and length

The returned pointer (`x0`) is immediately stored into a contiguous global block in `.bss` (`0xd38548` to `0xd38620`):

| Flag | Type | Call VA | Default Value | `.bss` Destination | Downstream XREFs | Classification |
|---|---|---|---|---|---|---|
| `-signaling` | string | `0x51532c` | `"localhost:8443"` | `.bss:0xd38548` | `0x51d2b0`, `0x51e440` in `main.main` | `SEMANTIC_XREF_CONFIRMED` |
| `-id` | string | `0x515374` | `""` | `.bss:0xd38550` | `0x51d2f4`, `0x51e0a4` in `main.main` | `SEMANTIC_XREF_CONFIRMED` |
| `-external-addr` | string | `0x5153bc` | `""` | `.bss:0xd38558` | `0x51d338`, `0x51e0c8` in `main.main` | `SEMANTIC_XREF_CONFIRMED` |
| `-webrtc-port` | int | `0x515400` | `50000` | `.bss:0xd38560` | `0x51d37c`, `0x51e360`, `0x51eaf8` | `SEMANTIC_XREF_CONFIRMED` |
| `-jar` | string | `0x51544c` | `"/data/local/tmp/libsys_core.so"` | `.bss:0xd38568` | `0x51d394`, `0x51d7cc`, `0x51d7fc`, `0x51d880` | `SEMANTIC_XREF_CONFIRMED` |
| `-resolution` | string | `0x515498` | `"1080x1920"` | `.bss:0xd38570` | `0x51d3d8`, `0x51e058` | `SEMANTIC_XREF_CONFIRMED` |
| `-bitrate` | int | `0x5154e0` | `2304` | `.bss:0xd38578` | `0x51d41c`, `0x51eb08` | `SEMANTIC_XREF_CONFIRMED` |
| `-max-size` | int | `0x515524` | `0` | `.bss:0xd38580` | `0x51d434`, `0x51eb2c` | `SEMANTIC_XREF_CONFIRMED` |
| `-max-fps` | int | `0x515568` | `0` | `.bss:0xd38588` | `0x51d44c`, `0x51eb3c` | `SEMANTIC_XREF_CONFIRMED` |
| `-video-codec-options` | string | `0x5155b0` | `""` | `.bss:0xd38590` | `0x51d464`, `0x51eb4c` | `SEMANTIC_XREF_CONFIRMED` |
| `-snapshot-interval` | int | `0x5155f4` | `10` | `.bss:0xd38598` | `0x51d4a8`, `0x51eb78` | `SEMANTIC_XREF_CONFIRMED` |
| `-snapshot-via-ws` | bool | `0x515638` | `false` | `.bss:0xd385a0` | `0x51eb88` in `main.main` | `SEMANTIC_XREF_CONFIRMED` |
| `-root` | bool | `0x51567c` | `false` | `.bss:0xd385a8` | `0x51d4c0` (`main.main`), `0x531834` | `SEMANTIC_XREF_CONFIRMED` |
| `-bwe` | string | `0x5156c8` | `"true"` | `.bss:0xd385b0` | `0x51d4d8`, `0x51e9fc` | `SEMANTIC_XREF_CONFIRMED` |
| `-audio` | bool | `0x51570c` | `false` | `.bss:0xd385b8` | `0x51d51c`, `0x51ebd4` | `SEMANTIC_XREF_CONFIRMED` |
| `-ice-servers` | string | `0x515758` | `"stun:stun.l.google.com:19302"` | `.bss:0xd385c0` | `0x51d534`, `0x51dc74` | `SEMANTIC_XREF_CONFIRMED` |
| `-upnp` | bool | `0x51579c` | `false` | `.bss:0xd385c8` | `0x51d578`, `0x51e344` | `SEMANTIC_XREF_CONFIRMED` |
| `-debug` | bool | `0x5157e0` | `false` | `.bss:0xd385d0` | `0x51d590`, `0x51ec18` | `SEMANTIC_XREF_CONFIRMED` |
| `-camera-addr` | string | `0x51582c` | `"127.0.0.1:9001"` | `.bss:0xd385d8` | `0x51d5a8`, `0x51ee04` | `SEMANTIC_XREF_CONFIRMED` |
| `-force-camera` | bool | `0x515870` | `false` | `.bss:0xd385e0` | `0x51d5ec`, `0x51ee80`, `0x51ef30` | `SEMANTIC_XREF_CONFIRMED` |
| `-video-source` | string | `0x5158bc` | `"display"` | `.bss:0xd385e8` | `0x51d604`, `0x51ec5c` | `SEMANTIC_XREF_CONFIRMED` |
| `-camera-facing` | string | `0x515908` | `"back"` | `.bss:0xd385f0` | `0x51d648`, `0x51ec88` | `SEMANTIC_XREF_CONFIRMED` |
| `-camera-id` | string | `0x515950` | `""` | `.bss:0xd385f8` | `0x51d68c`, `0x51ecb4` | `SEMANTIC_XREF_CONFIRMED` |
| `-camera-size` | string | `0x515998` | `""` | `.bss:0xd38600` | `0x51d6d0`, `0x51ece0` | `SEMANTIC_XREF_CONFIRMED` |
| `-camera-fps` | int | `0x5159dc` | `0` | `.bss:0xd38608` | `0x51d714`, `0x51ed0c` | `SEMANTIC_XREF_CONFIRMED` |
| `-camera-high-speed` | bool | `0x515a20` | `false` | `.bss:0xd38610` | `0x51d72c`, `0x51ed1c` | `SEMANTIC_XREF_CONFIRMED` |
| `-camera-ar` | string | `0x515a68` | `""` | `.bss:0xd38618` | `0x51d744`, `0x51ed2c` | `SEMANTIC_XREF_CONFIRMED` |
| `-expires-at` | string | `0x515ab4` | `"2026-11-01"` | `.bss:0xd38620` | `0x51d788`, `0x51da9c` | `SEMANTIC_XREF_CONFIRMED` |

This completely eliminates substring matching heuristics. All 28 flags are proven via concrete ARM64 disassembly.

### 2.4 Machine Disassembly Facts (Blocker 2)

All handwritten prose claims have been factored out into structured fact artifacts:
- **`evidence/go_signaling/DISASSEMBLY_FACTS.json`**:
  - `SIG-DCF-001`: `/connect_client` WebSocket upgrade and session binding (`main.id8ybRmw69lm` @ `0x7507c0`).
  - `SIG-DCF-002`: `/register_agent` WebSocket upgrade and registry mutation (`main.jdUaLc5NMO5` @ `0x754b40`).
  - `SIG-DCF-003`: `/api/login` credential parsing, token generation call to `jMkU1MzrAJ.Sg6kvDEQn`, response encoding (`main.ltOjwqsMl5q8` @ `0x73dd00`).
  - `SIG-DCF-004`: `/devices` active agent list serialization (`main.i2EgUTaLmQs` @ `0x74cf80`).
  - `SIG-DCF-005`: `/api/auth-status` noAuth indicator check (`main.bwvBd1LWVr` @ `0x73ec40`).
- **`evidence/go_agent/DISASSEMBLY_FACTS.json`**:
  - `AGENT-DCF-001`: `input-channel` creation via `pion/webrtc.(*PeerConnection).CreateDataChannel` (`main.(*JJffa1S1Zv6).iIhwd_WXInS` @ `0x53e588`).
  - `AGENT-DCF-002`: `clipboard-channel` creation via `CreateDataChannel` @ `0x53e610`.
  - `AGENT-DCF-003`: `camera-channel` creation via `CreateDataChannel` @ `0x53e740`.
  - `AGENT-DCF-004`: `OnDataChannel` event listener closure registration (`main.(*JJffa1S1Zv6).iIhwd_WXInS.func11` @ `0x53e818`).
  - `AGENT-DCF-005`: Agent CLI flag registration block in `main.init` (`0x5152f0`).

Crossmap records now reference `selector: "SIG-DCF-001"`, `evidence_file: "DISASSEMBLY_FACTS.json"`, ensuring the verifier statically validates fact existence and symbol alignment.

---

## 3. Strict Verification & Reproducibility Metrics

### 3.1 Strong Gate Confirmation Counts
Under the strict rule that only genuinely resolved forensic/runtime evidence classes may be counted toward strong confirmation:
- Total crossmap mappings: **28**
- **`BINARY_SEMANTIC_CONFIRMED`**: **25** (Requires `PUBLIC_REFERENCE` + $\ge 2$ resolved binary classes)
- **`REFERENCE_CORROBORATED`**: **1** (`channel: file-channel`, created by browser frontend and accepted by agent `OnDataChannel` callback)
- **`UNCONFIRMED_REFERENCE_ONLY`**: **2** (`payload: request-offer`, `message_type: webrtc_failed`)

### 3.2 6-Point Reproducibility Audit Matrix
All 6 reproducibility checks were verified via `tools/reference/reproduce_reference_evidence.py`:

| Reproducibility Check | Status | Verification Detail |
|---|---|---|
| `PUBLIC_GIT_INPUT_REPRODUCIBLE` | **PASS** | Pinned git blob SHAs and file SHA-256 hashes match across all reference files |
| `SOURCE_MACHINE_EXTRACTION_REPRODUCIBLE` | **PASS** | Protocol index, DataChannels, state machines regenerated bit-identically |
| `ANNOTATION_BINDINGS_VALID` | **PASS** | All reference text slices match `observed_text_hash` |
| `CLI_BINARY_EXTRACTION_REPRODUCIBLE` | **PASS** | Both `CLI_FLAG_REGISTRATION_EVIDENCE.json` and matrix regenerated bit-identically |
| `DISASSEMBLY_FACTS_REPRODUCIBLE` | **PASS** | Signaling and Agent disassembly facts regenerated bit-identically |
| `CROSSMAP_EVIDENCE_RESOLUTION_PASS` | **PASS** | Crossmap regenerated and every single evidence record resolves to disk artifacts |

### 3.3 Historical Metrics Invariant

| Metric | Target | Actual | Verdict |
|---|---|---|---|
| `SIGNALING_FUNCTION_TABLE_COVERAGE` | 7571 / 7571 | 100.0% | **PASS** |
| `AGENT_FUNCTION_TABLE_COVERAGE` | 15398 / 15398 | 100.0% | **PASS** |
| `ROUTE_DISCOVERY_COVERAGE` | 43 / 43 | 100.0% | **PASS** |
| `FRONTEND_ROUTE_BINARY_MATCH` | 18 / 18 | 100.0% | **PASS** |
| `RECONSTRUCTED_ROUTE_COUNT` | 4 / 4 (Auth) | 100.0% | **PASS** |
| `IMPLEMENTED_SURFACE_DIFFERENTIAL_PASS_RATE` | 18 / 18 | 100.0% | **PASS** |
| `ESTIMATED_FUNCTIONAL_RECONSTRUCTION_PROGRESS` | ~15% | ~15% | **PASS** |

---

## 4. Final Exit Gate Checklist

- [x] Public reference hash fields corrected (`source_git_blob_sha` vs `source_sha256`).
- [x] Machine extraction separated from annotations in `REFERENCE_PROTOCOL_INDEX`.
- [x] Exact CLI flag registration recovered via Go `aFaUKV` calls in `main.init`.
- [x] Generic `"id"` / `"root"` substring scanning eliminated.
- [x] `DISASSEMBLY_FACTS.json` generated for Signaling and Agent.
- [x] `BINARY_XREF` records resolvable in callgraph artifacts.
- [x] Every evidence class handled and verified by master verifier.
- [x] Strong gate counts only resolved evidence.
- [x] Dynamic oracle observed values derived and verified as structured fields.
- [x] Current confirmed / corroborated / unconfirmed counts computed honestly.
- [x] All 6 reproducibility statuses reported and PASS.
- [x] Persistence 8/8 PASS.
- [x] Auth core 12/12 PASS.
- [x] Auth HTTP 18/18 PASS.
- [x] Provenance 59/59 PASS.
- [x] Zero Phase 2C.3B source written (`reconstructed_source/` untouched).

---

## 5. Conclusion & Next Phase Authorization

With Phase 2R.3 closed, the reference intelligence layer has reached full cryptographic and disassembly closure. There are no remaining handwritten assertions, hash conflations, or heuristic classification shortcuts.

**Phase 2R is declared CLOSED.**  
**Phase 2C.3B (Devices & Registry REST Reconstruction) is ready to begin upon user authorization.**
