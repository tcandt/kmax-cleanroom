# Report 11R3R Errata: Disassembly Fact Derivation & Cross-Verification Hardening

## 1. Executive Summary

This errata document records the methodological refinements applied to the disassembly fact extraction pipeline and verifier infrastructure at the start of Phase 2C.3B. The behavioral conclusions and findings of **Report 11R3R** (`reports/11R3R_BINARY_FACT_DERIVATION_CLOSURE.md`) remain fully supported. However, the underlying derivation and verification mechanics have been upgraded from partial template/window constraints to **100% machine-derived instruction decoding**.

Historical Report 11R3R remains unmodified as an immutable record of the Phase 2R.3R audit.

---

## 2. Methodology Upgrades & Scope of Errata

### 2.1 Dynamic Boundary Scanning vs Hard-Coded Query Windows
- **Prior State**: `FACT_QUERIES_AGENT` in `tools/reference/generate_disassembly_facts.py` included hard-coded query search windows (`instruction_range: ("0x53e540", "0x53e5bc")`).
- **Errata Correction**: All hard-coded `instruction_range` literals have been removed from the fact queries. The extractor now takes the function boundary strictly from `FUNCTION_MAP.json` (`main.(*JJffa1S1Zv6).iIhwd_WXInS`, VA `0x53e410` to `0x53ec20`, size 2064 bytes) and dynamically discovers:
  1. The target channel name string reference (`input-channel`, `clipboard-channel`, `camera-channel`).
  2. The boolean allocation, initialization, and option-store instruction flow.
  3. The callee target `CreateDataChannel` (`0x4b95b0`).
- The reported `instruction_ranges` in `DISASSEMBLY_FACTS.json` are now dynamically bounded by the minimal instruction span discovered for each channel.

### 2.2 Machine-Derived DataChannel `ordered=true` Argument Recovery
- **Prior State**: The argument recovery dictionary in `generate_disassembly_facts.py` emitted fixed addresses and `ordered = True` metadata.
- **Errata Correction**: The extractor now decodes the ARM64 instruction stream directly:
  1. `runtime.newobject` call at `0x53e548` allocating a 1-byte heap boolean object.
  2. Pointer store to stack slot `[sp, #0x888]` at `0x53e54c`.
  3. Immediate load `mov x3, #1` at `0x53e550` (recovering `ordered_value = 1`).
  4. Byte store `strb w3, [x0]` at `0x53e554` initializing the boolean to `true`.
  5. Option store instruction (`0x53e570` for `input-channel`, `0x53e5f8` for `clipboard-channel`, `0x53e728` for `camera-channel`) writing the boolean pointer into `webrtc.DataChannelInit.Ordered`.
  6. Direct call `bl #0x4b95b0` invoking `CreateDataChannel`.
- All fields (`ordered`, `ordered_value`, `ordered_init_va`, `ordered_store_va`, `ordered_option_store_va`, `create_data_channel_call_va`) are strictly extracted from decoded instruction operands.

### 2.3 Instruction-Level String Xref Re-Decoding
- **Prior State**: The verifier checked that string bytes existed at the claimed binary file offset, but did not recompute whether the instruction at `instruction_va` actually referenced that address.
- **Errata Correction**: `tools/verify_phase2.py` now independently re-disassembles every string reference instruction:
  - **AMD64**: Decodes `lea reg, [rip +/- disp]`, computes `target_va = instruction_va + instruction_len + disp`, and asserts `hex(target_va) == fact.string_va` and binary bytes at `target_va - bias` match `fact.string_value`.
  - **ARM64**: Decodes the `adrp` page base at `instruction_va - 4` and the `add` immediate at `instruction_va`, computes `target_va = page + imm`, and asserts `hex(target_va) == fact.string_va` and binary bytes at `target_va - bias` match `fact.string_value`.

### 2.4 Instruction-Level CLI Downstream Xref Verification
- **Prior State**: Verifier checked that the downstream instruction string contained `"x27"`.
- **Errata Correction**: `tools/verify_phase2.py` now extracts the operand from the decoded instruction (`ldr/str reg, [x27, #offset]`), parses the exact offset, computes `0xd38000 + offset`, and asserts `hex(0xd38000 + offset) == xref.dest_va`. All 62 downstream CLI references are validated to resolve to their exact `.bss` variable addresses.

---

## 3. Verification Verdict

- Pre-flight verification: **PASS**
- Overall Audit: **26/26 CHECKS PASSED**
- Historical conclusions in Report 11R3R: **CONFIRMED & HARDENED**
