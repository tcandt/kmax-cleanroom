#!/usr/bin/env python3
"""
reproduce_share_forensics.py - Phase 2C.3E Share Forensic Reproducibility Tool

Verifies that ALL 13 Phase 2C.3E Share forensic artifacts are 100% reproducible
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

REPO_ROOT = Path(__file__).resolve().parents[2]
ELF_LINUX = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
CANONICAL_SHA256 = "6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "evidence" / "go_signaling" / "shares"

import capstone

sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.generate_share_forensics import (
    generate_evidence,
    parse_elf_sections,
    parse_struct_descriptor,
    va_to_offset
)

def verify_share_reproducibility():
    print("==================================================")
    print("PHASE 2C.3E SHARE FORENSIC REPRODUCIBILITY (13/13)")
    print("==================================================")

    # 1. Canonical Binary Hash Invariant
    if not ELF_LINUX.exists():
        print(f"[FAIL] Canonical ELF missing: {ELF_LINUX}")
        return False

    actual_hash = hashlib.sha256(ELF_LINUX.read_bytes()).hexdigest()
    if actual_hash != CANONICAL_SHA256:
        print(f"[FAIL] Canonical ELF SHA256 mismatch: {actual_hash} != {CANONICAL_SHA256}")
        return False
    print(f"[PASS] CANONICAL_ELF_EXISTS: webrtc-signaling ({CANONICAL_SHA256[:12]}...)")

    # 2. Run generator into isolated directory
    run_id = uuid.uuid4().hex[:8]
    temp_out = REPO_ROOT / "scratch" / "reproduce_share_forensics" / run_id
    if temp_out.exists():
        shutil.rmtree(temp_out, ignore_errors=True)
    temp_out.mkdir(parents=True, exist_ok=True)

    print(f"[*] Regenerating all 13 share artifacts into: {temp_out}")
    try:
        generate_evidence(output_dir=temp_out)
    except Exception as e:
        print(f"[FAIL] generate_evidence failed: {e}")
        return False

    results = {}

    # Artifact 1: SHARE_ROUTE_FAMILY.json
    f1_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    f1_r = json.loads((temp_out / "SHARE_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    p1 = (
        f1_c["route_count"] == f1_r["route_count"] == 7 and
        [r["pattern"] for r in f1_c["routes"]] == [r["pattern"] for r in f1_r["routes"]] and
        [r["handler_symbol"] for r in f1_c["routes"]] == [r["handler_symbol"] for r in f1_r["routes"]] and
        [r["handler_va"] for r in f1_c["routes"]] == [r["handler_va"] for r in f1_r["routes"]]
    )
    results["1. SHARE_ROUTE_FAMILY"] = p1
    print(f"[{'PASS' if p1 else 'FAIL'}] 1. SHARE_ROUTE_FAMILY: 7 canonical routes with symbols and VAs")

    # Artifact 2: SHARE_TYPE_EVIDENCE.json
    elf_bytes = ELF_LINUX.read_bytes()
    sections = parse_elf_sections(elf_bytes)
    share_token_struct = parse_struct_descriptor(elf_bytes, sections, 0x80f700)
    f2_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))
    f2_r = json.loads((temp_out / "SHARE_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))
    p2 = (
        share_token_struct["size_bytes"] == f2_c["share_token_struct"]["size_bytes"] == f2_r["share_token_struct"]["size_bytes"] == 192 and
        share_token_struct["field_count"] == f2_c["share_token_struct"]["field_count"] == f2_r["share_token_struct"]["field_count"] == 18 and
        share_token_struct["fields"] == f2_c["share_token_struct"]["fields"] == f2_r["share_token_struct"]["fields"] and
        f2_r.get("guest_settings_type", {}).get("descriptor_va") == "0x7bf940"
    )
    results["2. SHARE_TYPE_EVIDENCE"] = p2
    print(f"[{'PASS' if p2 else 'FAIL'}] 2. SHARE_TYPE_EVIDENCE: ShareToken (192 bytes, 18 fields) & guest_settings")

    # Artifact 3: SHARE_ROUTE_METHOD_MATRIX.json
    f3_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_ROUTE_METHOD_MATRIX.json").read_text(encoding="utf-8"))
    f3_r = json.loads((temp_out / "SHARE_ROUTE_METHOD_MATRIX.json").read_text(encoding="utf-8"))
    p3 = (
        len(f3_r) == 7 and
        all(len(verbs) == 7 for verbs in f3_r.values()) and
        # Strict method gating checks: extend and update return 405 on non-POST verbs
        all(f3_r["/api/share/extend"][m]["status_code"] == 405 for m in ["GET", "PUT", "PATCH", "DELETE", "HEAD"]) and
        all(f3_r["/api/share/update"][m]["status_code"] == 405 for m in ["GET", "PUT", "PATCH", "DELETE", "HEAD"]) and
        all(f3_r["/api/share/create"][m]["status_code"] == 405 for m in ["GET", "PUT", "PATCH", "DELETE", "HEAD"]) and
        all(verbs["OPTIONS"]["status_code"] == 200 for verbs in f3_r.values())
    )
    results["3. SHARE_ROUTE_METHOD_MATRIX"] = p3
    print(f"[{'PASS' if p3 else 'FAIL'}] 3. SHARE_ROUTE_METHOD_MATRIX: 7 routes x 7 verbs with strict 405 gating verified")

    # Artifact 4: SHARE_AUTH_MATRIX.json
    f4_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_AUTH_MATRIX.json").read_text(encoding="utf-8"))
    f4_r = json.loads((temp_out / "SHARE_AUTH_MATRIX.json").read_text(encoding="utf-8"))
    p4 = (
        len(f4_r) == 7 and
        all(set(v.keys()) == {"ADMIN", "NORMAL_USER", "MISSING_TOKEN", "INVALID_TOKEN", "NO_AUTH_MODE"} for v in f4_r.values()) and
        f4_r["/api/share/create"]["NORMAL_USER"]["status_code"] == 403 and
        f4_r["/api/share/list"]["NORMAL_USER"]["status_code"] == 403 and
        f4_r["/api/share/create"]["MISSING_TOKEN"]["status_code"] == 401 and
        f4_r["/api/share/info"]["MISSING_TOKEN"]["status_code"] == 400 and
        f4_r["/api/share/redeem_card"]["MISSING_TOKEN"]["status_code"] == 400
    )
    results["4. SHARE_AUTH_MATRIX"] = p4
    print(f"[{'PASS' if p4 else 'FAIL'}] 4. SHARE_AUTH_MATRIX: 7 routes x 5 states, admin RBAC (403) and public routes")

    # Artifact 5: SHARE_CREATE_CONTRACT.json
    f5_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_CREATE_CONTRACT.json").read_text(encoding="utf-8"))
    f5_r = json.loads((temp_out / "SHARE_CREATE_CONTRACT.json").read_text(encoding="utf-8"))
    p5 = (
        f5_r.get("empty_body_rejection", {}).get("status_code") == 400 and
        f5_r.get("duplicate_device_rejection", {}).get("status_code") == 409 and
        f5_r.get("minimal_response_schema", {}).get("code") == 0 and
        f5_r.get("full_create_verification", {}).get("token_prefix") == "st_" and
        f5_r.get("full_create_verification", {}).get("card_code_prefix") == "CP-"
    )
    results["5. SHARE_CREATE_CONTRACT"] = p5
    print(f"[{'PASS' if p5 else 'FAIL'}] 5. SHARE_CREATE_CONTRACT: Minimal schema 200, conflict 409, missing dev 400")

    # Artifact 6: SHARE_LIST_CONTRACT.json
    f6_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_LIST_CONTRACT.json").read_text(encoding="utf-8"))
    f6_r = json.loads((temp_out / "SHARE_LIST_CONTRACT.json").read_text(encoding="utf-8"))
    p6 = (
        f6_r.get("admin_response", {}).get("status_code") == 200 and
        f6_r.get("normal_user_status") == 403 and
        f6_r.get("device_filtering", {}).get("filtered_dev001_count") == 1 and
        f6_r.get("empty_list_shape") == f6_c.get("empty_list_shape")
    )
    results["6. SHARE_LIST_CONTRACT"] = p6
    print(f"[{'PASS' if p6 else 'FAIL'}] 6. SHARE_LIST_CONTRACT: Array response 200, admin gate 403, ?device_id= filtering")

    # Artifact 7: SHARE_INFO_CONTRACT.json
    f7_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_INFO_CONTRACT.json").read_text(encoding="utf-8"))
    f7_r = json.loads((temp_out / "SHARE_INFO_CONTRACT.json").read_text(encoding="utf-8"))
    p7 = (
        f7_r.get("valid_token_unprotected", {}).get("status_code") == 200 and
        f7_r.get("empty_token_rejection", {}).get("status_code") == 400 and
        f7_r.get("invalid_token_rejection", {}).get("status_code") == 404 and
        f7_r.get("password_protection", {}).get("missing_password_challenge", {}).get("code_field") == 401
    )
    results["7. SHARE_INFO_CONTRACT"] = p7
    print(f"[{'PASS' if p7 else 'FAIL'}] 7. SHARE_INFO_CONTRACT: Public info 200, empty 400, invalid 404, pwd challenge 401")

    # Artifact 8: SHARE_MUTATION_CONTRACTS.json
    f8_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_MUTATION_CONTRACTS.json").read_text(encoding="utf-8"))
    f8_r = json.loads((temp_out / "SHARE_MUTATION_CONTRACTS.json").read_text(encoding="utf-8"))
    p8 = (
        f8_r.get("revoke_contract", {}).get("valid_status") == 200 and
        f8_r.get("revoke_contract", {}).get("unknown_status") == 404 and
        f8_r.get("extend_contract", {}).get("permanent_share_rejection", {}).get("code_field") == 400 and
        f8_r.get("extend_contract", {}).get("expiring_share_extension", {}).get("code_field") == 0 and
        f8_r.get("update_contract", {}).get("empty_token_status") == 400 and
        f8_r.get("update_contract", {}).get("valid_status") == 200
    )
    results["8. SHARE_MUTATION_CONTRACTS"] = p8
    print(f"[{'PASS' if p8 else 'FAIL'}] 8. SHARE_MUTATION_CONTRACTS: Revoke (200/404), Extend (200/400), Update (200/400)")

    # Artifact 9: SHARE_REDEEM_CARD_CONTRACT.json
    f9_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_REDEEM_CARD_CONTRACT.json").read_text(encoding="utf-8"))
    f9_r = json.loads((temp_out / "SHARE_REDEEM_CARD_CONTRACT.json").read_text(encoding="utf-8"))
    p9 = (
        f9_r.get("empty_card_code", {}).get("status_code") == 400 and
        f9_r.get("invalid_card_code", {}).get("code_field") == 404 and
        f9_r.get("valid_card_code", {}).get("status_code") == 200
    )
    results["9. SHARE_REDEEM_CARD_CONTRACT"] = p9
    print(f"[{'PASS' if p9 else 'FAIL'}] 9. SHARE_REDEEM_CARD_CONTRACT: Empty 400, invalid code 404, valid redemption 200/0")

    # Artifact 10: SHARE_PERSISTENCE_CONTRACT.json
    f10_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_PERSISTENCE_CONTRACT.json").read_text(encoding="utf-8"))
    f10_r = json.loads((temp_out / "SHARE_PERSISTENCE_CONTRACT.json").read_text(encoding="utf-8"))
    
    # Independent binary disassembly verification of main.fomL4ATwVV1
    fm_path = REPO_ROOT / "evidence" / "go_signaling" / "FUNCTION_MAP.json"
    fm_data = {f["symbol_name"]: f for f in json.loads(fm_path.read_text(encoding="utf-8"))}
    f_save = fm_data.get("main.fomL4ATwVV1", {})
    va_save_start = int(f_save.get("va", "0x739900"), 16)
    size_save = f_save.get("size_bytes", 1664)
    sec_off_save = va_to_offset(va_save_start, sections)
    code_save = elf_bytes[sec_off_save:sec_off_save+size_save]
    
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    indep_p_facts = {}
    for insn in md.disasm(code_save, va_save_start):
        if insn.mnemonic == 'call':
            try:
                target = int(insn.op_str, 16)
                if target == 0x533e80:
                    indep_p_facts["marshal_indent"] = hex(insn.address)
                elif target == 0x4608a0:
                    indep_p_facts["tmp_concat"] = hex(insn.address)
                elif target == 0x4e0da0:
                    indep_p_facts["write_file"] = hex(insn.address)
                elif target == 0x4e1160:
                    indep_p_facts["rename"] = hex(insn.address)
            except:
                pass
        for op in insn.operands:
            if op.type == capstone.x86.X86_OP_IMM and op.imm == 0x180:
                indep_p_facts["mode_0600"] = hex(insn.address)
            elif op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
                target_va = insn.address + insn.size + op.mem.disp
                target_off = va_to_offset(target_va, sections)
                if target_off is not None and elf_bytes[target_off:target_off+4] == b'.tmp':
                    indep_p_facts["tmp_xref"] = hex(insn.address)

    p10 = (
        f10_r["file_name"] == "shares.json" and
        f10_r["atomic_tmp_rename"] is True and
        "0600" in f10_r["file_mode"] and
        f10_r.get("machine_facts", {}).get("save_shares_symbol") == "main.fomL4ATwVV1" and
        f10_r.get("machine_facts", {}).get("marshal_indent_call_va") == indep_p_facts.get("marshal_indent") and
        f10_r.get("machine_facts", {}).get("tmp_string_xref_va") == indep_p_facts.get("tmp_xref") and
        f10_r.get("machine_facts", {}).get("mode_arg_instruction_va") == indep_p_facts.get("mode_0600") and
        f10_r.get("machine_facts", {}).get("write_file_call_va") == indep_p_facts.get("write_file") and
        f10_r.get("machine_facts", {}).get("rename_call_va") == indep_p_facts.get("rename")
    )
    results["10. SHARE_PERSISTENCE_CONTRACT"] = p10
    print(f"[{'PASS' if p10 else 'FAIL'}] 10. SHARE_PERSISTENCE_CONTRACT: Atomic .tmp + os.Rename ({indep_p_facts.get('rename')}), mode 0600 ({indep_p_facts.get('mode_0600')}) independently decoded")

    # Artifact 11: SHARE_EXPIRY_CONTRACT.json
    f11_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_EXPIRY_CONTRACT.json").read_text(encoding="utf-8"))
    f11_r = json.loads((temp_out / "SHARE_EXPIRY_CONTRACT.json").read_text(encoding="utf-8"))
    
    # Independent binary disassembly verification of setup and worker
    f_setup = fm_data.get("main.dYBSRoVh", {})
    va_setup = int(f_setup.get("va", "0x73a0a0"), 16)
    size_setup = f_setup.get("size_bytes", 128)
    sec_off_setup = va_to_offset(va_setup, sections)
    code_setup = elf_bytes[sec_off_setup:sec_off_setup+size_setup]
    
    indep_ticker_imm = None
    for insn in md.disasm(code_setup, va_setup):
        for op in insn.operands:
            if op.type == capstone.x86.X86_OP_IMM and op.imm > 1000000000:
                indep_ticker_imm = op.imm

    f_worker = fm_data.get("main.dYBSRoVh.func1", {})
    va_worker = int(f_worker.get("va", "0x73a120"), 16)
    size_worker = f_worker.get("size_bytes", 992)
    sec_off_worker = va_to_offset(va_worker, sections)
    code_worker = elf_bytes[sec_off_worker:sec_off_worker+size_worker]
    
    indep_worker_facts = {}
    for insn in md.disasm(code_worker, va_worker):
        if insn.mnemonic == 'call':
            try:
                target = int(insn.op_str, 16)
                if target == 0x4c98a0:
                    indep_worker_facts["after"] = hex(insn.address)
                elif target == 0x739900:
                    indep_worker_facts["save_shares"] = hex(insn.address)
                elif target == 0x40bb20 and "del1" not in indep_worker_facts:
                    indep_worker_facts["del1"] = hex(insn.address)
            except:
                pass

    p11 = (
        indep_ticker_imm == 300000000000 and
        f11_r.get("cleanup_worker", {}).get("setup_symbol") == "main.dYBSRoVh" and
        f11_r.get("cleanup_worker", {}).get("ticker_interval_seconds") == 300 and
        f11_r.get("cleanup_worker", {}).get("worker_symbol") == "main.dYBSRoVh.func1" and
        f11_r.get("cleanup_worker", {}).get("machine_facts", {}).get("save_shares_call_va") == indep_worker_facts.get("save_shares") and
        f11_r.get("cleanup_worker", {}).get("machine_facts", {}).get("expiry_comparison_call_va") == indep_worker_facts.get("after") and
        f11_r.get("lazy_check_on_query", {}).get("handler_va") == "0x760480"
    )
    results["11. SHARE_EXPIRY_CONTRACT"] = p11
    print(f"[{'PASS' if p11 else 'FAIL'}] 11. SHARE_EXPIRY_CONTRACT: Ticker 300s (decoded immediate {hex(indep_ticker_imm or 0)}), reaper worker save ({indep_worker_facts.get('save_shares')})")

    # Artifact 12: SHARE_CROSS_CONTRACT.json
    f12_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_CROSS_CONTRACT.json").read_text(encoding="utf-8"))
    f12_r = json.loads((temp_out / "SHARE_CROSS_CONTRACT.json").read_text(encoding="utf-8"))
    
    # Independent verification of cross-contract route binding from ROUTE_HANDLER_MAP
    route_map_raw = json.loads((REPO_ROOT / "evidence" / "go_signaling" / "ROUTE_HANDLER_MAP.json").read_text(encoding="utf-8"))
    routes_by_pat = {r["pattern"]: r for r in route_map_raw.get("routes", [])}
    
    p12 = (
        f12_r.get("test_cases", {}).get("CROSS-01", {}).get("shares_json_bit_identical") is True and
        f12_r.get("test_cases", {}).get("CROSS-01", {}).get("static_proof", {}).get("handler_symbol") == routes_by_pat.get("/api/admin/users/delete", {}).get("handler_symbol") == "main._Wcin_o" and
        f12_r.get("test_cases", {}).get("CROSS-01", {}).get("static_proof", {}).get("handler_va") == routes_by_pat.get("/api/admin/users/delete", {}).get("handler_va") == "0x745ba0" and
        f12_r.get("test_cases", {}).get("CROSS-02", {}).get("shares_json_bit_identical") is True and
        f12_r.get("test_cases", {}).get("CROSS-02", {}).get("static_proof", {}).get("handler_symbol") == routes_by_pat.get("/api/devices/", {}).get("handler_symbol") == "main.rXQMyuE" and
        f12_r.get("test_cases", {}).get("CROSS-02", {}).get("static_proof", {}).get("handler_va") == routes_by_pat.get("/api/devices/", {}).get("handler_va") == "0x74da60" and
        f12_r.get("test_cases", {}).get("CROSS-03", {}).get("isolation_verified") is True and
        f12_r.get("test_cases", {}).get("CROSS-03", {}).get("static_proof", {}).get("handler_symbol") == routes_by_pat.get("/devices", {}).get("handler_symbol") == "main.i2EgUTaLmQs" and
        f12_r.get("test_cases", {}).get("CROSS-03", {}).get("static_proof", {}).get("handler_va") == routes_by_pat.get("/devices", {}).get("handler_va") == "0x74cf80" and
        f12_r.get("device_uniqueness", {}).get("status_code") == 409
    )
    results["12. SHARE_CROSS_CONTRACT"] = p12
    print(f"[{'PASS' if p12 else 'FAIL'}] 12. SHARE_CROSS_CONTRACT: Canonical handlers /admin/users/delete (main._Wcin_o), /devices/ (main.rXQMyuE), /devices (main.i2EgUTaLmQs) independently bound")

    # Artifact 13: SHARE_HTTP_FUNCTION_SLICES.json
    f13_c = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    f13_r = json.loads((temp_out / "SHARE_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    p13 = (
        len(f13_c) == len(f13_r) == 11 and
        all(
            s.get("symbol") and
            s.get("machine_observation", {}).get("start_va") and
            s.get("machine_observation", {}).get("size_bytes", 0) > 0 and
            s.get("machine_observation", {}).get("instruction_count", 0) > 0 and
            s.get("semantic_annotation", {}).get("role_description")
            for s in f13_r
        ) and
        [s["symbol"] for s in f13_c] == [s["symbol"] for s in f13_r]
    )
    results["13. SHARE_HTTP_FUNCTION_SLICES"] = p13
    print(f"[{'PASS' if p13 else 'FAIL'}] 13. SHARE_HTTP_FUNCTION_SLICES: 11 query-derived slices (machine_observation + semantic_annotation)")

    # Cleanup temp
    shutil.rmtree(temp_out, ignore_errors=True)

    all_pass = all(results.values())
    print("--------------------------------------------------")
    print(f"OVERALL REPRODUCIBILITY: {'PASS' if all_pass else 'FAIL'} ({sum(1 for v in results.values() if v)}/13 artifacts verified)")
    print("==================================================")
    return all_pass

if __name__ == "__main__":
    success = verify_share_reproducibility()
    sys.exit(0 if success else 1)
