# Report 11R3R: Binary-Derived Disassembly Fact Closure & Forensic Extraction Finalization

**Status**: CLOSED & AUDITED (Phase 2R.3R)  
**Date**: 2026-09-16  
**Corpus**: `tcandt/kmax-cleanroom`  
**Verdict**: **PASS — DISASSEMBLY FACT DERIVATION & FORENSIC VERIFICATION CLOSED**

> [!IMPORTANT]
> **Methodological Supersession Notice**:  
> This report **supersedes** Report 11R3 Section 2.4 ("Machine-Verifiable Disassembly Facts Created") regarding fact derivation methodology.  
> In Report 11R3, `generate_disassembly_facts.py` regenerated facts deterministically from a static Python dictionary table. In Phase 2R.3R, `generate_disassembly_facts.py` was completely rewritten to forensically derive all control flow, direct calls, string xrefs, function boundaries, and argument structures **directly from canonical ELF binary bytes using Capstone disassembly and `FUNCTION_MAP.json`**. Reports 11, 11R, 11R2, and 11R3 remain historically preserved without modification.

---

## 1. Executive Summary

Phase 2R.3R addresses the final technical blocker identified in Phase 2R.3 review: transitioning `DISASSEMBLY_FACTS.json` from a deterministic Python-table generator into a true binary-derived forensic extractor, and hardening the master verifier (`verify_phase2.py`) to independently disassemble and inspect machine instructions.

### Key Deliverables & Architectural Transformations

1. **Complete Rewrite of `generate_disassembly_facts.py`**:
   - Eliminated all hardcoded authoritative result tables (`sig_facts` and `agent_facts` literal dictionaries).
   - Introduced lightweight declarative query specifications (`FACT_QUERIES_SIG` and `FACT_QUERIES_AGENT`) defining only target search patterns.
   - All concrete instruction VAs, target symbols, string offsets, instruction ranges, and argument values are derived at runtime from binary bytes via Capstone disassembly.
2. **Function Boundaries Derived from `FUNCTION_MAP.json`**:
   - `function_va`, `function_size`, and `instruction_ranges` are obtained directly from `FUNCTION_MAP.json` records (e.g. `main.id8ybRmw69lm` @ `0x7507c0` size 14208 -> `0x7507c0`-`0x753f40`).
   - Zero hard-coded address ranges in the generator.
3. **Instruction-Level Direct Call Extraction**:
   - **AMD64** (`webrtc-signaling`): decodes `call` rel32 instructions, resolves target VAs, and maps them to symbols in `FUNCTION_MAP.json` (e.g. `0x7509f7` -> `_iYIJQCvEF4X.(*ILKba3lAb4u).Upgrade`, `0x7510a2` -> `_iYIJQCvEF4X.(*Yt_Fm_GhgcEh).ReadMessage`, `0x751696` -> `main.(*LG7nmxLRaW).WriteJSON`, `0x751f6f` -> `main.(*AoIDVQHamcx).Send`).
   - **ARM64** (`cloudphone-agent`): decodes `bl` instructions and maps target VAs to symbols (e.g. `0x53e588` -> `CreateDataChannel`, `0x53e818` -> `OnDataChannel`, `0x51532c` -> `aFaUKV.CMNJxRQ7`).
4. **Instruction-Level String Xref Recovery**:
   - **AMD64**: tracks RIP-relative `lea` instructions (`lea reg, [rip + disp32]`), computes exact target VAs and file offsets, and peeks raw `.rodata` bytes to match strings (`share:`, `Conflict: this share is already in use by another guest`, `Unauthorized`, `message_type`, `WebClient connected to device %s`).
   - **ARM64**: tracks `adrp` + `add` register pairs, computes page + immediate offsets, and verifies exact string bytes in binary data.
5. **Static Argument Proof for DataChannel `ordered` Property**:
   - Disassembled `main.(*JJffa1S1Zv6).iIhwd_WXInS`:
     - At `0x53e548`: calls `runtime.newobject` (`0x2a8d0`) to allocate a heap `bool`.
     - At `0x53e550`: `mov x3, #1`.
     - At `0x53e554`: `strb w3, [x0]` stores `1` (`true`) into the allocated boolean.
     - At `0x53e54c`: saves pointer in `[sp, #0x888]`.
     - For `input-channel`: at `0x53e570`, stores pointer into `DataChannelInit` offset 0 (`Ordered *bool`), followed by `bl CreateDataChannel` at `0x53e588`.
     - For `clipboard-channel`: at `0x53e5f4`, loads `[sp, #0x888]` into `x4`, stores into options struct at `0x53e5f8`, and calls `CreateDataChannel` at `0x53e610`.
     - For `camera-channel`: at `0x53e724`, loads `[sp, #0x888]` into `x4`, stores into options struct at `0x53e728`, and calls `CreateDataChannel` at `0x53e740`.
   - All three channels statically prove `ordered = true` with `ordered_evidence = "BINARY_ARGUMENT_RECOVERY"`.
6. **Strict Machine vs Semantic Separation**:
   - `DISASSEMBLY_FACTS.json` explicitly partitions raw observations into `machine_observation` (`direct_calls`, `string_xrefs`, `argument_recovery`) and `semantic_annotation` (`claim`, `confidence`, `rationale`).
7. **Master Verifier (`verify_phase2.py`) Hardened**:
   - **Check 25 (CLI)**: independently re-disassembles each of the 28 call sites in `main.init`, verifies the instruction is `bl`, verifies target resolves to the expected `flag_api_symbol`, disassembles backwards to verify the string loaded into `x0` matches `flag_name.lstrip("-")`, disassembles forwards to verify the destination store to `.bss`, and verifies downstream xrefs.
   - **Check 26 (Crossmap & Disassembly Facts)**: executes a full 9-point forensic check over every fact in `DISASSEMBLY_FACTS.json`, verifying instruction existence, target symbols, string contents, and function boundary containment.
   - **PCLNTAB Resolution**: fixed dictionary lookup (`sig_fmap_by_sym`, `agent_fmap_by_sym`) preventing list membership bugs.
   - **Every Evidence Class Handled**: all active classes have explicit resolvers, with a mandatory fallback (`else: all_records_resolved = False`) guaranteeing no unknown or unhandled class can silently pass.

---

## 2. Technical Implementation Details

### 2.1 Declarative Query vs Forensically Derived Result

The generator `tools/reference/generate_disassembly_facts.py` now uses declarative queries without hardcoded instruction results:

```python
FACT_QUERIES_SIG = {
    "SIG-DCF-001": {
        "function_symbol": "main.id8ybRmw69lm",
        "callee_patterns": ["Upgrade", "ReadMessage", "WriteJSON", "Send"],
        "string_patterns": [
            "share:",
            "Conflict: this share is already in use by another guest",
            "Unauthorized",
            "message_type",
            "WebClient connected to device %s"
        ],
        "semantic_annotation": {
            "claim": "/connect_client handler upgrades HTTP connection to WebSocket, validates token/share_token query parameters, binds client to active device session, and runs bidirectional message pump.",
            "confidence": "HIGH",
            "rationale": "Direct calls to Gorilla WebSocket Upgrade and ReadMessage combined with session management strings in main.id8ybRmw69lm."
        }
    }
}
```

The derivation engine executes Capstone over the function slice determined by `FUNCTION_MAP.json` and produces the following machine-derived record:

```json
{
  "fact_id": "SIG-DCF-001",
  "artifact_path": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
  "artifact_sha256": "6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3",
  "function_symbol": "main.id8ybRmw69lm",
  "function_va": "0x7507c0",
  "function_size": 14208,
  "instruction_ranges": [
    {
      "start_va": "0x7507c0",
      "end_va": "0x753f40"
    }
  ],
  "machine_observation": {
    "direct_calls": [
      {
        "call_va": "0x7509f7",
        "target_va": "0x72fee0",
        "target_symbol": "_iYIJQCvEF4X.(*ILKba3lAb4u).Upgrade",
        "derivation": "MACHINE_DISASSEMBLY"
      },
      {
        "call_va": "0x7510a2",
        "target_va": "0x72eec0",
        "target_symbol": "_iYIJQCvEF4X.(*Yt_Fm_GhgcEh).ReadMessage",
        "derivation": "MACHINE_DISASSEMBLY"
      },
      {
        "call_va": "0x751696",
        "target_va": "0x748360",
        "target_symbol": "main.(*LG7nmxLRaW).WriteJSON",
        "derivation": "MACHINE_DISASSEMBLY"
      },
      {
        "call_va": "0x751f6f",
        "target_va": "0x74a520",
        "target_symbol": "main.(*AoIDVQHamcx).Send",
        "derivation": "MACHINE_DISASSEMBLY"
      }
    ],
    "string_xrefs": [
      {
        "instruction_va": "0x750851",
        "string_va": "0x81d5ac",
        "string_file_offset": "0x41d5ac",
        "string_value": "share:",
        "derivation": "MACHINE_INSTRUCTION_XREF"
      },
      {
        "instruction_va": "0x7509b2",
        "string_va": "0x83c057",
        "string_file_offset": "0x43c057",
        "string_value": "Conflict: this share is already in use by another guest",
        "derivation": "MACHINE_INSTRUCTION_XREF"
      },
      {
        "instruction_va": "0x751072",
        "string_va": "0x82470f",
        "string_file_offset": "0x42470f",
        "string_value": "Unauthorized",
        "derivation": "MACHINE_INSTRUCTION_XREF"
      },
      {
        "instruction_va": "0x751168",
        "string_va": "0x824727",
        "string_file_offset": "0x424727",
        "string_value": "message_type",
        "derivation": "MACHINE_INSTRUCTION_XREF"
      },
      {
        "instruction_va": "0x751560",
        "string_va": "0x836fff",
        "string_file_offset": "0x436fff",
        "string_value": "WebClient connected to device %s",
        "derivation": "MACHINE_INSTRUCTION_XREF"
      }
    ]
  },
  "semantic_annotation": {
    "claim": "/connect_client handler upgrades HTTP connection to WebSocket, validates token/share_token query parameters, binds client to active device session, and runs bidirectional message pump.",
    "confidence": "HIGH",
    "rationale": "Direct calls to Gorilla WebSocket Upgrade and ReadMessage combined with session management strings in main.id8ybRmw69lm."
  }
}
```

### 2.2 DataChannel `ordered = true` Static Forensic Proof

In `cloudphone-agent` (ARM64), `main.(*JJffa1S1Zv6).iIhwd_WXInS` (`0x53c730`-`0x53f210`) initializes WebRTC DataChannels using `pion/webrtc.PeerConnection.CreateDataChannel`. The `DataChannelInit` struct in Pion WebRTC Go has the following layout:
- Offset 0 (`0x00`): `Ordered *bool`
- Offset 8 (`0x08`): `MaxPacketLifeTime *uint16`
- Offset 16 (`0x10`): `MaxRetransmits *uint16`
- Offset 24 (`0x18`): `Protocol *string`
- Offset 40 (`0x28`): `Negotiated *bool`
- Offset 48 (`0x30`): `ID *uint16`

The disassembly of `cloudphone-agent` proves the initialization of `Ordered`:
```asm
0x53e540: adrp x0, #0x5ac000
0x53e544: add  x0, x0, #0x180          ; type descriptor for bool
0x53e548: bl   #0x2a8d0                ; runtime.newobject (allocates heap bool)
0x53e54c: str  x0, [sp, #0x888]        ; save pointer to heap bool
0x53e550: mov  x3, #1                  ; load immediate 1 (true)
0x53e554: strb w3, [x0]                ; *bool_ptr = 1 (true)

; --- input-channel initialization ---
0x53e570: str  x0, [sp, #0x618]        ; store bool_ptr to DataChannelInit.Ordered (offset 0)
0x53e578: adrp x1, #0x6b8000
0x53e57c: add  x1, x1, #0x548          ; "input-channel" string pointer
0x53e580: mov  x2, #0xd                ; len = 13
0x53e588: bl   #0x4b95b0               ; CreateDataChannel

; --- clipboard-channel initialization ---
0x53e5f4: ldr  x4, [sp, #0x888]        ; reload pointer to true bool
0x53e5f8: str  x4, [sp, #0x5e8]        ; store to DataChannelInit.Ordered (offset 0)
0x53e5fc: adrp x1, #0x6bc000
0x53e604: add  x1, x1, #0x175          ; "clipboard-channel" string pointer
0x53e608: mov  x2, #0x11               ; len = 17
0x53e610: bl   #0x4b95b0               ; CreateDataChannel

; --- camera-channel initialization ---
0x53e724: ldr  x4, [sp, #0x888]        ; reload pointer to true bool
0x53e728: str  x4, [sp, #0x5b8]        ; store to DataChannelInit.Ordered (offset 0)
0x53e72c: adrp x1, #0x6b9000
0x53e734: add  x1, x1, #0x3ba          ; "camera-channel" string pointer
0x53e738: mov  x2, #0xe                ; len = 14
0x53e740: bl   #0x4b95b0               ; CreateDataChannel
```

This establishes undeniable, instruction-level static proof that `ordered = true` is passed to `CreateDataChannel` for `input-channel`, `clipboard-channel`, and `camera-channel`.

### 2.3 Master Verifier 9-Point Disassembly Fact Resolution

In `tools/verify_phase2.py` Check 26, each `DISASSEMBLY_CONTROL_FLOW` evidence record undergoes independent verification:
1. **Artifact SHA Integrity**: matches canonical binary SHA-256 (`6865f05...` for signaling, `9cc32ea...` for agent).
2. **Function Symbol Existence**: symbol exists in `FUNCTION_MAP.json`.
3. **Boundary Agreement**: `function_va` and `function_size` match `FUNCTION_MAP.json`.
4. **Instruction Existence**: every direct call instruction exists at the exact VA as a `call` (AMD64) or `bl` (ARM64).
5. **Decoded Target Symbol**: the decoded destination address resolves to the claimed `target_symbol` in `FUNCTION_MAP.json`.
6. **Instruction Xref Existence**: every string xref instruction exists at the exact VA.
7. **Referenced String Bytes**: raw binary bytes at `string_file_offset` bit-exact match `string_value`.
8. **Boundary Containment**: all instruction ranges and xref VAs reside strictly inside the function boundary `[va, va + size)`.
9. **Argument Recovery Integrity**: `ordered = true` with `ordered_evidence = "BINARY_ARGUMENT_RECOVERY"` validated against instructions.

---

## 3. Verification & Reproducibility Audit

### 3.1 Verification Suite Results

| Test / Check Suite | Target Artifacts | Invariant Tested | Result |
|---|---|---|---|
| Check 01: Artifact Hashes | 3 original binaries | SHA-256 bit-exact equality | **PASS** |
| Check 02-03: Pclntab & Maps | `FUNCTION_MAP.json`, `CALLGRAPH.json` | Monotonicity, non-overlap, size parity | **PASS** |
| Check 04-09: Role Mappings | `ROLE_MAPPING.json` | 0 leaks, mathematical sum parity | **PASS** |
| Check 10-11: Route Extraction | `ROUTE_HANDLER_MAP.json` | 43 routes discovered, 0 unresolved | **PASS** |
| Check 12: Scope Boundary | `reconstructed_source/` | 23 .go files, zero unauthorized code | **PASS** |
| Check 13: Source Provenance | `reconstructed_source/` | 59/59 cleanroom provenance headers | **PASS** |
| Check 14-23: Auth Differentials | `AUTH_HTTP_DIFFERENTIAL_RESULTS.json` | 18/18 HTTP cases bit-exact pass | **PASS** |
| Check 24: Pinned References | `PUBLIC_REFERENCE_TREE_MANIFEST.json` | Git blob SHA-1 & file SHA-256 match | **PASS** |
| Check 25: CLI Registration Proof | `CLI_FLAG_REGISTRATION_EVIDENCE.json` | 28 flags verified via Capstone re-disasm | **PASS** |
| Check 26: Disassembly Facts & Crossmap | `REFERENCE_TO_BINARY_CROSSMAP.json` | 28 mappings, 9-point fact verification | **PASS** |

### 3.2 Six Reproducibility Checks (`reproduce_reference_evidence.py`)

All six reproducibility statuses pass deterministically when regenerating into an isolated temporary directory:
1. `PUBLIC_GIT_INPUT_REPRODUCIBLE`: **PASS** (10/10 pinned git blobs match)
2. `SOURCE_MACHINE_EXTRACTION_REPRODUCIBLE`: **PASS** (protocol index, datachannel matrix, state machine bit-exact)
3. `ANNOTATION_BINDINGS_VALID`: **PASS** (all line slice hashes match)
4. `CLI_BINARY_EXTRACTION_REPRODUCIBLE`: **PASS** (all 28 flag registrations bit-exact)
5. `DISASSEMBLY_FACTS_REPRODUCIBLE`: **PASS** (all 10 disassembly facts forensically regenerated from binary disassembly)
6. `CROSSMAP_EVIDENCE_RESOLUTION_PASS`: **PASS** (28/28 crossmap mappings resolve 100% of underlying evidence records)

---

## 4. Recomputed Crossmap Confirmation Status

Following the forensic disassembly derivation and removal of unused declared classes (`TYPE_DESCRIPTOR`, `NETWORK_CAPTURE`), the crossmap status was recomputed strictly according to the multi-evidence rule:
- `BINARY_SEMANTIC_CONFIRMED`: **25** (requires `PUBLIC_REFERENCE` + $\ge 2$ independent resolved binary classes)
- `REFERENCE_CORROBORATED`: **1** (requires `PUBLIC_REFERENCE` + $1$ resolved binary class)
- `UNCONFIRMED_REFERENCE_ONLY`: **2** (no binary evidence currently confirmed)
- **Total Mappings**: **28**

Every single evidence record attached to these mappings is backed by a verified physical artifact and resolved by `verify_phase2.py`.

---

## 5. Phase 2R Final Closure Verdict

With Phase 2R.3R complete:
- **No hardcoded disassembly facts remain.**
- **All direct calls, string xrefs, function boundaries, and argument values are derived from machine instructions.**
- **The verifier independently verifies Capstone disassembly at every call site.**
- **PCLNTAB lookup is fixed to use symbol maps.**
- **Every declared evidence class is explicitly handled and verified.**
- **Zero source code in `reconstructed_source/` was touched.**
- **Phase 2C.3B remains unopened until user authorization.**

**Reference Evidence Infrastructure is officially CLOSED.**
Proceed directly to **Phase 2C.3B (Devices & Registry REST Reconstruction)** upon authorization.
