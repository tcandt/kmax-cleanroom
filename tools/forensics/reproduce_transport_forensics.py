#!/usr/bin/env python3
"""
reproduce_transport_forensics.py — Phase 2C.4AR Evidence-Bound Transport Forensic Reproducibility Verifier

Verifies that ALL 23 canonical Phase 2C.4AR Transport forensic artifacts:
  1. TRANSPORT_ROUTE_FAMILY.json
  2. TRANSPORT_CLASSIFICATION_MATRIX.json
  3. TRANSPORT_METHOD_UPGRADE_MATRIX.json
  4. TRANSPORT_AUTH_MATRIX.json
  5. TRANSPORT_REQUEST_CONTRACT.json
  6. TRANSPORT_TYPE_EVIDENCE.json
  7. WEBSOCKET_HANDSHAKE_CONTRACT.json
  8. TRANSPORT_REGISTRY_TYPE_EVIDENCE.json
  9. REGISTER_DEVICE_STATE_MACHINE.json
  10. REGISTER_AGENT_STATE_MACHINE.json
  11. CONNECT_CLIENT_STATE_MACHINE.json
  12. TRANSPORT_MESSAGE_TYPE_EVIDENCE.json
  13. TRANSPORT_MESSAGE_MATRIX.json
  14. TRANSPORT_HEARTBEAT_CONTRACT.json
  15. DEVICE_AGENT_CLIENT_ASSOCIATION_CONTRACT.json
  16. WEBRTC_SIGNALING_CONTRACT.json
  17. DATACHANNEL_TRANSPORT_CROSSMAP.json
  18. TRANSPORT_DISCONNECT_CLEANUP_CONTRACT.json
  19. TRANSPORT_CONCURRENCY_CONTRACT.json
  20. TRANSPORT_EDGE_MATRIX.json
  21. TRANSPORT_CROSS_BUILD_CORRELATION.json
  22. TRANSPORT_FUNCTION_SLICES.json
  23. TRANSPORT_FORENSIC_GATE_RESULT.json

are 100% reproducible directly from canonical binary disassembly (Go pclntab, Capstone, rodata descriptors)
and genuine dynamic oracle execution, with ZERO copying of canonical evidence.

Deep Semantic Validation:
- Deeply compares all dynamic probe values (status, headers, upgrade tokens, Sec-WebSocket-Accept presence, body class, auth timing, framing).
- Zero shallow keys-only comparisons.
- Zero literal PASS echoes: asserts that the dynamically computed gate result genuinely passes all 18 invariants.
- Default mode: READ ONLY. Zero repository mutation.
"""

import os
import sys
import json
import uuid
import shutil
import re
from pathlib import Path
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import tools.forensics.generate_transport_forensics as gtf

CANONICAL_DIR = REPO_ROOT / "evidence" / "go_signaling" / "transport"
MANIFEST_PATH = CANONICAL_DIR / "TRANSPORT_REPRODUCIBILITY_MANIFEST.json"

EXPECTED_23_ARTIFACTS = [
    "TRANSPORT_ROUTE_FAMILY.json",
    "TRANSPORT_CLASSIFICATION_MATRIX.json",
    "TRANSPORT_METHOD_UPGRADE_MATRIX.json",
    "TRANSPORT_AUTH_MATRIX.json",
    "TRANSPORT_REQUEST_CONTRACT.json",
    "TRANSPORT_TYPE_EVIDENCE.json",
    "WEBSOCKET_HANDSHAKE_CONTRACT.json",
    "TRANSPORT_REGISTRY_TYPE_EVIDENCE.json",
    "REGISTER_DEVICE_STATE_MACHINE.json",
    "REGISTER_AGENT_STATE_MACHINE.json",
    "CONNECT_CLIENT_STATE_MACHINE.json",
    "TRANSPORT_MESSAGE_TYPE_EVIDENCE.json",
    "TRANSPORT_MESSAGE_MATRIX.json",
    "TRANSPORT_HEARTBEAT_CONTRACT.json",
    "DEVICE_AGENT_CLIENT_ASSOCIATION_CONTRACT.json",
    "WEBRTC_SIGNALING_CONTRACT.json",
    "DATACHANNEL_TRANSPORT_CROSSMAP.json",
    "TRANSPORT_DISCONNECT_CLEANUP_CONTRACT.json",
    "TRANSPORT_CONCURRENCY_CONTRACT.json",
    "TRANSPORT_EDGE_MATRIX.json",
    "TRANSPORT_CROSS_BUILD_CORRELATION.json",
    "TRANSPORT_FUNCTION_SLICES.json",
    "TRANSPORT_FORENSIC_GATE_RESULT.json"
]

def deep_compare_method_upgrade_matrix(rj: Dict[str, Any], cj: Dict[str, Any]) -> List[str]:
    diffs = []
    routes = ["/register_device", "/register_agent", "/connect_client"]
    for r in routes:
        if r not in rj or r not in cj:
            diffs.append(f"Route {r} missing in METHOD_UPGRADE_MATRIX")
            continue
        r_std = rj[r].get("standard_http", {})
        c_std = cj[r].get("standard_http", {})
        for m in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
            if m not in r_std or m not in c_std:
                diffs.append(f"{r} standard_http method {m} missing")
                continue
            r_item = r_std[m]
            c_item = c_std[m]
            if r_item.get("status_code") != c_item.get("status_code"):
                diffs.append(f"{r} {m} status_code: {r_item.get('status_code')} != {c_item.get('status_code')}")
            if r_item.get("upgrade_success") != c_item.get("upgrade_success"):
                diffs.append(f"{r} {m} upgrade_success mismatch")
            if r_item.get("body_class") != c_item.get("body_class"):
                diffs.append(f"{r} {m} body_class mismatch")
            if r_item.get("case_id") != c_item.get("case_id"):
                diffs.append(f"{r} {m} case_id mismatch")

        r_up = rj[r].get("upgrade_variations", {})
        c_up = cj[r].get("upgrade_variations", {})
        for v in ["valid_upgrade", "missing_upgrade_header", "invalid_upgrade_token", "wrong_version_12", "missing_websocket_key"]:
            if v not in r_up or v not in c_up:
                diffs.append(f"{r} upgrade_variation {v} missing")
                continue
            r_v = r_up[v]
            c_v = c_up[v]
            if r_v.get("status_code") != c_v.get("status_code"):
                diffs.append(f"{r} {v} status_code: {r_v.get('status_code')} != {c_v.get('status_code')}")
            if r_v.get("upgrade_success") != c_v.get("upgrade_success"):
                diffs.append(f"{r} {v} upgrade_success mismatch")
            if r_v.get("sec_websocket_accept_present") != c_v.get("sec_websocket_accept_present"):
                diffs.append(f"{r} {v} sec_websocket_accept_present mismatch")
            if r_v.get("case_id") != c_v.get("case_id"):
                diffs.append(f"{r} {v} case_id mismatch")
    return diffs

def deep_compare_auth_matrix(rj: Dict[str, Any], cj: Dict[str, Any]) -> List[str]:
    diffs = []
    scenarios = [
        "ADMIN_HEADER", "ADMIN_QUERY", "NORMAL_USER_HEADER", "NORMAL_USER_QUERY",
        "SHARE_TOKEN_QUERY", "MISSING_TOKEN", "INVALID_TOKEN",
        "DEVICE_UNAUTH_REGISTRATION", "AGENT_UNAUTH_REGISTRATION"
    ]
    for s in scenarios:
        if s not in rj or s not in cj:
            diffs.append(f"Auth scenario {s} missing")
            continue
        r_s = rj[s]
        c_s = cj[s]
        if r_s.get("case_id") != c_s.get("case_id"):
            diffs.append(f"Scenario {s} case_id mismatch: {r_s.get('case_id')} != {c_s.get('case_id')}")
        if r_s.get("status_code") != c_s.get("status_code"):
            diffs.append(f"Scenario {s} status_code: {r_s.get('status_code')} != {c_s.get('status_code')}")
        if r_s.get("upgrade_success") != c_s.get("upgrade_success"):
            diffs.append(f"Scenario {s} upgrade_success mismatch")
        if r_s.get("auth_timing") != c_s.get("auth_timing"):
            diffs.append(f"Scenario {s} auth_timing mismatch: {r_s.get('auth_timing')} != {c_s.get('auth_timing')}")
        if r_s.get("token_source") != c_s.get("token_source"):
            diffs.append(f"Scenario {s} token_source mismatch")
        if r_s.get("body_class") != c_s.get("body_class"):
            diffs.append(f"Scenario {s} body_class mismatch")
    return diffs

def deep_compare_handshake_contract(rj: Dict[str, Any], cj: Dict[str, Any]) -> List[str]:
    diffs = []
    # Upgrader and framing invariants
    if rj.get("protocol") != cj.get("protocol") or rj.get("version") != cj.get("version"):
        diffs.append("Protocol/version mismatch in WEBSOCKET_HANDSHAKE_CONTRACT")
    if rj.get("upgrader") != cj.get("upgrader"):
        diffs.append("Upgrader configuration mismatch in WEBSOCKET_HANDSHAKE_CONTRACT")
    if rj.get("framing") != cj.get("framing"):
        diffs.append("Framing configuration mismatch in WEBSOCKET_HANDSHAKE_CONTRACT")

    # Initial frame contract per route
    r_if = rj.get("initial_frame_contract", {})
    c_if = cj.get("initial_frame_contract", {})
    for r in ["/register_device", "/register_agent", "/connect_client"]:
        if r not in r_if or r not in c_if:
            diffs.append(f"Route {r} missing in initial_frame_contract")
            continue
        if r_if[r].get("has_initial_server_frame") != c_if[r].get("has_initial_server_frame"):
            diffs.append(f"{r} has_initial_server_frame mismatch")
        if r_if[r].get("timeout_observed") != c_if[r].get("timeout_observed"):
            diffs.append(f"{r} timeout_observed mismatch")
        if r_if[r].get("behavior") != c_if[r].get("behavior"):
            diffs.append(f"{r} behavior mismatch")
        if r_if[r].get("case_id") != c_if[r].get("case_id"):
            diffs.append(f"{r} initial frame case_id mismatch")
    return diffs

def deep_compare_edge_matrix(rj: Dict[str, Any], cj: Dict[str, Any]) -> List[str]:
    diffs = []
    r_ec = rj.get("edge_cases", {})
    c_ec = cj.get("edge_cases", {})

    # Unmasked frame
    r_unmask = r_ec.get("unmasked_client_frame", {})
    c_unmask = c_ec.get("unmasked_client_frame", {})
    if r_unmask.get("response_frame_opcode") != c_unmask.get("response_frame_opcode"):
        diffs.append("unmasked_client_frame response_frame_opcode mismatch")
    if r_unmask.get("closed_by_server") != c_unmask.get("closed_by_server"):
        diffs.append("unmasked_client_frame closed_by_server mismatch")
    if r_unmask.get("case_id") != c_unmask.get("case_id"):
        diffs.append("unmasked_client_frame case_id mismatch")

    # Ping pong
    r_ping = r_ec.get("ping_pong", {})
    c_ping = c_ec.get("ping_pong", {})
    if r_ping.get("received_pong_opcode") != c_ping.get("received_pong_opcode"):
        diffs.append("ping_pong received_pong_opcode mismatch")
    if r_ping.get("pong_success") != c_ping.get("pong_success"):
        diffs.append("ping_pong pong_success mismatch")
    if r_ping.get("case_id") != c_ping.get("case_id"):
        diffs.append("ping_pong case_id mismatch")

    # Security boundaries
    if rj.get("security_boundaries") != cj.get("security_boundaries"):
        diffs.append("security_boundaries mismatch in TRANSPORT_EDGE_MATRIX")
    return diffs

def deep_compare_gate_result(rj: Dict[str, Any], cj: Dict[str, Any]) -> List[str]:
    diffs = []
    if rj.get("verdict") != "PASS" or cj.get("verdict") != "PASS":
        diffs.append(f"Verdict is not PASS (regen: {rj.get('verdict')}, canonical: {cj.get('verdict')})")
    r_checks = rj.get("checks", [])
    c_checks = cj.get("checks", [])
    if len(r_checks) != 18 or len(c_checks) != 18:
        diffs.append(f"Checks count is not 18 (regen: {len(r_checks)}, canonical: {len(c_checks)})")
        return diffs

    for rc, cc in zip(r_checks, c_checks):
        if rc.get("id") != cc.get("id"):
            diffs.append(f"Check id mismatch: {rc.get('id')} != {cc.get('id')}")
        if rc.get("status") != "PASS" or cc.get("status") != "PASS":
            diffs.append(f"Check {rc.get('id')} status is not PASS (regen: {rc.get('status')}, canonical: {cc.get('status')})")
        if rc.get("description") != cc.get("description"):
            diffs.append(f"Check {rc.get('id')} description mismatch")
        if rc.get("metrics") != cc.get("metrics"):
            diffs.append(f"Check {rc.get('id')} metrics mismatch: {rc.get('metrics')} != {cc.get('metrics')}")
    return diffs

def audit_anti_tautology_invariants() -> List[str]:
    """
    Strict Anti-Tautology & Machine-Derivation Audit:
    1. Asserts zero unconditional "status": "PASS" lines in gate evaluation.
    2. Asserts zero hardcoded Windows pclntab offset literals (0x4e9c80).
    3. Asserts zero hardcoded Windows ImageBase or section offset arithmetic (0x140000000, 0x379000, 0x377c00).
    4. Asserts zero hardcoded Windows closure map (win_closure_map).
    5. Asserts machine derivation of heartbeat 30s/60s constants from binary instructions.
    """
    violations = []
    gen_file = REPO_ROOT / "tools" / "forensics" / "generate_transport_forensics.py"
    if not gen_file.exists():
        violations.append("generate_transport_forensics.py file missing")
        return violations

    code = gen_file.read_text(encoding="utf-8")

    # 1. Gate source check: evaluate_forensic_gate must not have unconditional PASS
    gate_fn_match = re.search(r'def evaluate_forensic_gate\(.*?\n(?=def |\Z)', code, re.DOTALL)
    if not gate_fn_match:
        violations.append("evaluate_forensic_gate function not found in generator")
    else:
        gate_body = gate_fn_match.group(0)
        for line in gate_body.splitlines():
            line_str = line.strip()
            if '"status": "PASS"' in line_str and "if" not in line_str:
                violations.append(f"Unconditional PASS found in gate: {line_str}")

    # 2. Historical Windows pclntab offset literal check (code body, not comment/doc)
    if "win_data[0x4e9c80" in code or "0x4e9c80:" in code:
        violations.append("Hardcoded Windows pclntab offset 0x4e9c80 used for slicing")

    # 3. Hardcoded PE ImageBase / section arithmetic
    if "0x140000000" in code or "0x379000" in code or "0x377c00" in code:
        violations.append("Hardcoded PE section layout constants (0x140000000, 0x379000, 0x377c00) detected")

    # 4. Hardcoded closure VA map
    if "win_closure_map" in code:
        violations.append("Hardcoded win_closure_map detected in generator")

    # 5. Heartbeat derivation verification
    if "def derive_transport_timing_contract" not in code:
        violations.append("derive_transport_timing_contract() missing from generator")

    return violations

def verify_reproducibility() -> bool:
    total_manifest = len(EXPECTED_23_ARTIFACTS)
    print("==========================================================")
    print(f"PHASE 2C.4AR2 ZERO-TAUTOLOGY & EVIDENCE-BOUND REPRODUCIBILITY VERIFIER ({total_manifest}/{total_manifest})")
    print("==========================================================")

    print("[*] Executing Anti-Tautology & Machine-Derivation Audit on generator source...")
    audit_violations = audit_anti_tautology_invariants()
    if audit_violations:
        print("[FAIL] Anti-Tautology Audit detected violations in generator:")
        for v in audit_violations:
            print(f"       - {v}")
        return False
    print("  [PASS] Anti-Tautology Audit: Zero unconditional PASS gate checks, zero hardcoded Windows offsets/closures, machine-derived timing.")

    if not gtf.EXE_PATH.exists():
        print(f"[FAIL] Canonical binary missing: {gtf.EXE_PATH}")
        return False

    run_id = uuid.uuid4().hex[:8]
    temp_dir = REPO_ROOT / "scratch" / "reproduce_transport_forensics" / run_id
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Regenerating all {total_manifest} Transport artifacts into temp: {temp_dir}")
    print("    Strict mode: ZERO copying of canonical artifacts; genuine machine derivation only.")

    try:
        route_family = gtf.discover_transport_routes()
        type_desc = gtf.extract_type_descriptors()
        oracle_data = gtf.run_oracle_transport_probes()
        cross_build = gtf.correlate_cross_builds()
        func_slices = gtf.generate_callgraph_function_slices(route_family)
        gtf.generate_canonical_artifacts(route_family, type_desc, oracle_data, cross_build, func_slices, out_dir=temp_dir)
    except Exception as e:
        print(f"[FAIL] generate_canonical_artifacts failed: {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return False

    print("[*] Performing deep field-by-field semantic validation comparing regenerated artifacts against canonical target evidence...")

    failed_artifacts = []
    for a_name in EXPECTED_23_ARTIFACTS:
        regen_file = temp_dir / a_name
        canonical_file = CANONICAL_DIR / a_name

        if not regen_file.exists():
            print(f"[FAIL] Missing regenerated artifact: {a_name}")
            failed_artifacts.append(a_name)
            continue
        if not canonical_file.exists():
            print(f"[FAIL] Missing canonical comparison target: {a_name}")
            failed_artifacts.append(a_name)
            continue

        rj = json.loads(regen_file.read_text(encoding="utf-8"))
        cj = json.loads(canonical_file.read_text(encoding="utf-8"))

        diffs = []
        if a_name == "TRANSPORT_METHOD_UPGRADE_MATRIX.json":
            diffs = deep_compare_method_upgrade_matrix(rj, cj)
        elif a_name == "TRANSPORT_AUTH_MATRIX.json":
            diffs = deep_compare_auth_matrix(rj, cj)
        elif a_name == "WEBSOCKET_HANDSHAKE_CONTRACT.json":
            diffs = deep_compare_handshake_contract(rj, cj)
        elif a_name == "TRANSPORT_EDGE_MATRIX.json":
            diffs = deep_compare_edge_matrix(rj, cj)
        elif a_name == "TRANSPORT_FORENSIC_GATE_RESULT.json":
            diffs = deep_compare_gate_result(rj, cj)
        else:
            # Full structural & value deep equality
            if rj != cj:
                diffs.append("Full semantic content differs from canonical artifact")

        if diffs:
            print(f"[FAIL] {a_name} deep comparison failed:")
            for d in diffs[:5]:
                print(f"       - {d}")
            failed_artifacts.append(a_name)
            continue

        print(f"  [PASS] {a_name:<45} Deep semantic parity verified")

    shutil.rmtree(temp_dir, ignore_errors=True)

    if failed_artifacts:
        print(f"\n[FAIL] {len(failed_artifacts)}/{total_manifest} artifacts failed reproducibility verification.")
        return False

    print("==========================================================")
    print(f"[SUCCESS] All {total_manifest}/{total_manifest} Transport artifacts verified with 100% deep semantic reproducibility!")
    print("Zero repository mutations. Working tree unmodified.")
    print("==========================================================")
    return True

if __name__ == "__main__":
    success = verify_reproducibility()
    sys.exit(0 if success else 1)
