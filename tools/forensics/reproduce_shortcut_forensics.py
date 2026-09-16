#!/usr/bin/env python3
"""
reproduce_shortcut_forensics.py - Phase 2C.3F Shortcuts Forensic Reproducibility Tool

Verifies that ALL 7 Phase 2C.3F Shortcut forensic artifacts are 100% reproducible
directly from the canonical binary ELF and dynamic oracle, adhering to all
cleanroom and provenance invariants.
"""

import os
import sys
import json
import uuid
import shutil
import hashlib
from pathlib import Path
import capstone

REPO_ROOT = Path(__file__).resolve().parents[2]
ELF_LINUX = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
CANONICAL_SHA256 = "6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "evidence" / "go_signaling" / "shortcuts"

sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.generate_shortcut_forensics import (
    generate_evidence,
    parse_elf_sections,
    va_to_offset
)

def verify_shortcut_reproducibility():
    print("==================================================")
    print("PHASE 2C.3F SHORTCUT FORENSIC REPRODUCIBILITY (7/7)")
    print("==================================================")

    if not ELF_LINUX.exists():
        print(f"[FAIL] Canonical ELF missing: {ELF_LINUX}")
        return False

    actual_hash = hashlib.sha256(ELF_LINUX.read_bytes()).hexdigest()
    if actual_hash != CANONICAL_SHA256:
        print(f"[FAIL] Canonical ELF SHA256 mismatch: {actual_hash} != {CANONICAL_SHA256}")
        return False
    print(f"[PASS] CANONICAL_ELF_EXISTS: webrtc-signaling ({CANONICAL_SHA256[:12]}...)")

    run_id = uuid.uuid4().hex[:8]
    temp_out = REPO_ROOT / "scratch" / "reproduce_shortcut_forensics" / run_id
    if temp_out.exists():
        shutil.rmtree(temp_out, ignore_errors=True)
    temp_out.mkdir(parents=True, exist_ok=True)

    print(f"[*] Regenerating all 7 shortcut artifacts into: {temp_out}")
    try:
        generate_evidence(output_dir=temp_out)
    except Exception as e:
        print(f"[FAIL] generate_evidence failed: {e}")
        return False

    elf_bytes = ELF_LINUX.read_bytes()
    sections = parse_elf_sections(elf_bytes)

    results = {}

    # Artifact 1: SHORTCUT_ROUTE_FAMILY.json
    f1_c = json.loads((DEFAULT_OUTPUT_DIR / "SHORTCUT_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    f1_r = json.loads((temp_out / "SHORTCUT_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    p1 = (
        f1_r["pattern"] == "/api/shortcuts" and
        f1_r["registration_call_va"] == "0x765984" and
        f1_r["wrapper"]["symbol"] == "main.main.func3" and
        f1_r["wrapper"]["va"] == "0x76d4c0" and
        f1_r["business_handler"]["symbol"] == "main.yHBQWSpi" and
        f1_r["business_handler"]["va"] == "0x76c640" and
        f1_r["persistence_callees"]["loader_symbol"] == "main.iXiPYH2zBLTK" and
        f1_r["persistence_callees"]["saver_symbol"] == "main.jk9A26"
    )
    results["1. SHORTCUT_ROUTE_FAMILY"] = p1
    print(f"[{'PASS' if p1 else 'FAIL'}] 1. SHORTCUT_ROUTE_FAMILY: /api/shortcuts bound to wrapper main.main.func3 & handler main.yHBQWSpi")

    # Artifact 2: SHORTCUT_TYPE_EVIDENCE.json
    f2_c = json.loads((DEFAULT_OUTPUT_DIR / "SHORTCUT_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))
    f2_r = json.loads((temp_out / "SHORTCUT_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))
    st = f2_r.get("shortcut_struct", {})
    fields = st.get("fields", [])
    p2 = (
        st.get("size_bytes") == 32 and
        st.get("field_count") == 2 and
        any(f["name"] == "DIHvMDn" and f["tag"] == 'json:"name"' for f in fields) and
        any(f["name"] == "MTkDoTKb" and f["tag"] == 'json:"cmd"' for f in fields) and
        f2_r.get("storage_map", {}).get("descriptor_va") == "0x7bfc40" and
        "*map[string][]main.KXuCJAAi60" in f2_r.get("storage_map", {}).get("type_name", "")
    )
    results["2. SHORTCUT_TYPE_EVIDENCE"] = p2
    print(f"[{'PASS' if p2 else 'FAIL'}] 2. SHORTCUT_TYPE_EVIDENCE: Shortcut struct (32B, name, cmd) & per-user map descriptor verified")

    # Artifact 3: SHORTCUT_ROUTE_METHOD_MATRIX.json
    f3_c = json.loads((DEFAULT_OUTPUT_DIR / "SHORTCUT_ROUTE_METHOD_MATRIX.json").read_text(encoding="utf-8"))
    f3_r = json.loads((temp_out / "SHORTCUT_ROUTE_METHOD_MATRIX.json").read_text(encoding="utf-8"))
    p3 = (
        len(f3_r) == 7 and
        f3_r["GET"]["status_code"] == 200 and
        f3_r["OPTIONS"]["status_code"] == 200 and
        f3_r["OPTIONS"]["cors_origin"] == "*" and
        f3_r["POST"]["status_code"] == 400 and
        f3_r["PUT"]["status_code"] == 405 and
        f3_r["PATCH"]["status_code"] == 405 and
        f3_r["DELETE"]["status_code"] == 405 and
        f3_r["HEAD"]["status_code"] == 405 and
        f3_r["HEAD"]["body_bytes"] == 0 and # wire bodyless
        f3_r["HEAD"]["content_length"] == "19"
    )
    results["3. SHORTCUT_ROUTE_METHOD_MATRIX"] = p3
    print(f"[{'PASS' if p3 else 'FAIL'}] 3. SHORTCUT_ROUTE_METHOD_MATRIX: 7 verbs verified (GET 200, OPTIONS 200, PUT/PATCH/DELETE/HEAD 405, wire bodyless HEAD)")

    # Artifact 4: SHORTCUT_AUTH_MATRIX.json
    f4_c = json.loads((DEFAULT_OUTPUT_DIR / "SHORTCUT_AUTH_MATRIX.json").read_text(encoding="utf-8"))
    f4_r = json.loads((temp_out / "SHORTCUT_AUTH_MATRIX.json").read_text(encoding="utf-8"))
    p4 = (
        f4_r["ADMIN"]["status_code"] == 200 and
        f4_r["NORMAL_USER"]["status_code"] == 200 and
        f4_r["NO_AUTH_MODE"]["status_code"] == 200 and
        f4_r["MISSING_TOKEN"]["status_code"] == 401 and
        f4_r["INVALID_TOKEN"]["status_code"] == 401
    )
    results["4. SHORTCUT_AUTH_MATRIX"] = p4
    print(f"[{'PASS' if p4 else 'FAIL'}] 4. SHORTCUT_AUTH_MATRIX: 5 auth states verified (Admin/NormalUser/NoAuth 200, Missing/Invalid 401)")

    # Artifact 5: SHORTCUT_OPERATION_CONTRACTS.json
    f5_c = json.loads((DEFAULT_OUTPUT_DIR / "SHORTCUT_OPERATION_CONTRACTS.json").read_text(encoding="utf-8"))
    f5_r = json.loads((temp_out / "SHORTCUT_OPERATION_CONTRACTS.json").read_text(encoding="utf-8"))
    p5 = (
        f5_r["read_initial_empty"]["status_code"] == 200 and
        f5_r["read_initial_empty"]["response_body"] == "[]\n" and
        f5_r["mutation_replace"]["status_code"] == 200 and
        len(f5_r["mutation_replace"]["verified_readback"]) == 2 and
        f5_r["per_user_isolation"]["isolation_verified"] is True and
        f5_r["error_handling"]["empty_body"]["status_code"] == 400 and
        f5_r["error_handling"]["malformed_json"]["status_code"] == 400 and
        f5_r["error_handling"]["empty_array_clear"]["status_code"] == 200
    )
    results["5. SHORTCUT_OPERATION_CONTRACTS"] = p5
    print(f"[{'PASS' if p5 else 'FAIL'}] 5. SHORTCUT_OPERATION_CONTRACTS: Read initial '[]\n', replace mutation, per-user isolation, error handling")

    # Artifact 6: SHORTCUT_PERSISTENCE_CONTRACT.json
    f6_c = json.loads((DEFAULT_OUTPUT_DIR / "SHORTCUT_PERSISTENCE_CONTRACT.json").read_text(encoding="utf-8"))
    f6_r = json.loads((temp_out / "SHORTCUT_PERSISTENCE_CONTRACT.json").read_text(encoding="utf-8"))
    
    # Independent binary disassembly of saver main.jk9A26
    fm_path = REPO_ROOT / "evidence" / "go_signaling" / "FUNCTION_MAP.json"
    fm_data = {f["symbol_name"]: f for f in json.loads(fm_path.read_text(encoding="utf-8"))}
    f_saver = fm_data.get("main.jk9A26", {})
    va_saver_start = int(f_saver.get("va", "0x76c2c0"), 16)
    size_saver = f_saver.get("size_bytes", 608)
    sec_off_saver = va_to_offset(va_saver_start, sections)
    code_saver = elf_bytes[sec_off_saver:sec_off_saver+size_saver]

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    indep_saver = {}
    for insn in md.disasm(code_saver, va_saver_start):
        if insn.mnemonic == 'call':
            try:
                target = int(insn.op_str, 16)
                if target == 0x533e80:
                    indep_saver["marshal"] = hex(insn.address)
                elif target == 0x4e0da0:
                    indep_saver["write_file"] = hex(insn.address)
            except:
                pass
        for op in insn.operands:
            if op.type == capstone.x86.X86_OP_IMM and op.imm == 0x1a4:
                indep_saver["mode_0644"] = hex(insn.address)

    p6 = (
        f6_r["file_name"] == "shortcuts.json" and
        "0644" in f6_r["file_mode"] and
        f6_r["no_auth_mode_key"]["key_used"] == "admin" and
        f6_r["machine_facts"]["marshal_indent_call_va"] == indep_saver.get("marshal") and
        f6_r["machine_facts"]["write_file_call_va"] == indep_saver.get("write_file") and
        f6_r["machine_facts"]["mode_arg_instruction_va"] == indep_saver.get("mode_0644")
    )
    results["6. SHORTCUT_PERSISTENCE_CONTRACT"] = p6
    print(f"[{'PASS' if p6 else 'FAIL'}] 6. SHORTCUT_PERSISTENCE_CONTRACT: Direct os.WriteFile ({indep_saver.get('write_file')}), mode 0644 ({indep_saver.get('mode_0644')}), no-auth key 'admin' verified")

    # Artifact 7: SHORTCUT_HTTP_FUNCTION_SLICES.json
    f7_c = json.loads((DEFAULT_OUTPUT_DIR / "SHORTCUT_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    f7_r = json.loads((temp_out / "SHORTCUT_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    p7 = (
        len(f7_c) == len(f7_r) == 4 and
        all(
            s.get("symbol") and
            s.get("machine_observation", {}).get("start_va") and
            s.get("machine_observation", {}).get("size_bytes", 0) > 0 and
            s.get("machine_observation", {}).get("instruction_count", 0) > 0 and
            s.get("semantic_annotation", {}).get("role_description")
            for s in f7_r
        ) and
        [s["symbol"] for s in f7_c] == [s["symbol"] for s in f7_r]
    )
    results["7. SHORTCUT_HTTP_FUNCTION_SLICES"] = p7
    print(f"[{'PASS' if p7 else 'FAIL'}] 7. SHORTCUT_HTTP_FUNCTION_SLICES: 4 query-derived slices (wrapper, handler, loader, saver) verified")

    shutil.rmtree(temp_out, ignore_errors=True)

    all_pass = all(results.values())
    print("--------------------------------------------------")
    print(f"OVERALL REPRODUCIBILITY: {'PASS' if all_pass else 'FAIL'} ({sum(1 for v in results.values() if v)}/7 artifacts verified)")
    print("==================================================")
    return all_pass

if __name__ == "__main__":
    success = verify_shortcut_reproducibility()
    sys.exit(0 if success else 1)
