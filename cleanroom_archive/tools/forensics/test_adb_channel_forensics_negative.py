#!/usr/bin/env python3
"""
tools/forensics/test_adb_channel_forensics_negative.py

Negative mutation test suite for Phase 2C.5B6F adb-channel forensics.
Validates fail-closed behavior across all forensic invariants, anti-tautology rules,
and production safety boundaries.
"""
import copy
import json
import os
import sys
import tempfile
from pathlib import Path

ARCHIVE_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ARCHIVE_ROOT))

from tools.forensics.pclntab_parser import get_repo_root
REPO_ROOT = get_repo_root()

from tools.forensics.adb_channel.validate_adb_channel_semantics import validate_adb_channel_semantics
from tools.forensics.adb_channel.derive_adb_channel_protocol import derive_adb_channel_artifacts

EVID_DIR = REPO_ROOT / "evidence" / "go_agent" / "webrtc"
SPEC_PATH = EVID_DIR / "ADB_CHANNEL_B6F_PROTOCOL_SPEC.json"
TOP_PATH = EVID_DIR / "ADB_CHANNEL_B6F_TOPOLOGY.json"
FRAME_PATH = EVID_DIR / "ADB_CHANNEL_B6F_MESSAGE_FRAMING.json"
CG_PATH = EVID_DIR / "ADB_CHANNEL_B6F_CALLGRAPH.json"
PROV_PATH = EVID_DIR / "ADB_CHANNEL_B6F_SOURCE_PROVENANCE.json"
CONTRACT_PATH = EVID_DIR / "ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json"
ERRATA_PATH = EVID_DIR / "ADB_CHANNEL_B6F_CONTRACT_ERRATA.json"


def run_negative_tests():
    print("==================================================")
    print("PHASE 2C.5B6F ADB-CHANNEL NEGATIVE MUTATION TEST SUITE")
    print("==================================================")

    test_cases = []

    # Case 1: Wrong Channel Label
    def case_wrong_label():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        s["channel_identity"]["label"] = "adb"
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 1: Rejection of Tampered Channel Label ('adb')", case_wrong_label, ValueError))

    # Case 2: Ownership Inversion
    def case_ownership_inversion():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        s["channel_identity"]["creator_side"] = "Agent"
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 2: Rejection of Ownership Inversion (Agent Creates Channel)", case_ownership_inversion, ValueError))

    # Case 3: Inbound Ordered Promoted to Agent STATIC
    def case_ordered_promoted():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        s["channel_identity"]["ordered_property"]["classification"] = "STATIC_CONFIRMED"
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 3: Rejection of Inbound Ordered Promoted to STATIC", case_ordered_promoted, ValueError))

    # Case 4: Response Method Swapped to SendText
    def case_sendtext_swap():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        s["directional_framing"]["agent_to_browser_response"]["api"] = "SendText (string)"
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 4: Rejection of Response API Swapped to SendText", case_sendtext_swap, ValueError))

    # Case 5: Session Sticky Flag Corrupted
    def case_sticky_flag():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        s["session_mode_lifecycle"]["is_session_sticky"] = False
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 5: Rejection of Non-Sticky Session Lifecycle", case_sticky_flag, ValueError))

    # Case 6: Header Length Corrupted
    def case_header_length():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        s["adb_packet_protocol"]["header_bytes"] = 16
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 6: Rejection of Corrupted ADB Header Length (16B instead of 24B)", case_header_length, ValueError))

    # Case 7: Header Field Offset Corrupted
    def case_field_offset():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        s["adb_packet_protocol"]["fields"][1]["offset"] = 2
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 7: Rejection of Misaligned Packet Header Field Offset", case_field_offset, ValueError))

    # Case 8: Missing State Machine Command
    def case_missing_cmd():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        del s["adb_packet_protocol"]["commands"]["CNXN"]
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 8: Rejection of Omitted CNXN Command from State Machine", case_missing_cmd, ValueError))

    # Case 9: Downstream Swapped to External TCP Bridge
    def case_tcp_swap():
        t = json.loads(TOP_PATH.read_text(encoding="utf-8"))
        t["downstream_topology"]["classification"] = "EXTERNAL_TCP_BRIDGE"
        validate_adb_channel_semantics(topology=t)
    test_cases.append(("Case 9: Rejection of External TCP Bridge Classification", case_tcp_swap, ValueError))

    # Case 10: Reachable net.Dial Falsely Marked Non-Zero
    def case_net_dial():
        t = json.loads(TOP_PATH.read_text(encoding="utf-8"))
        t["downstream_topology"]["external_tcp_bridge"]["reachable_net_dial_calls"] = 1
        validate_adb_channel_semantics(topology=t)
    test_cases.append(("Case 10: Rejection of Reachable net.Dial in External Bridge Info", case_net_dial, ValueError))

    # Case 11: Clean-Room Scope Omits Deferred Boundary
    def case_scope_boundary():
        t = json.loads(TOP_PATH.read_text(encoding="utf-8"))
        t["downstream_topology"]["clean_room_scope"] = "OPERATIONAL_BRIDGE_IMPLEMENTED"
        validate_adb_channel_semantics(topology=t)
    test_cases.append(("Case 11: Rejection of Missing DEFERRED_ADB_BRIDGE_BOUNDARY in Scope", case_scope_boundary, ValueError))

    # Case 12: Callgraph Terminal Boundary Altered
    def case_cg_boundary():
        cg = json.loads(CG_PATH.read_text(encoding="utf-8"))
        cg["nodes"]["ARM64"]["terminal_boundary"] = "PRODUCTION_EXECUTION_ATTACHED"
        validate_adb_channel_semantics(callgraph=cg)
    test_cases.append(("Case 12: Rejection of Altered Callgraph Terminal Boundary", case_cg_boundary, ValueError))

    # Case 13: Provenance Missing Dispatch Site
    def case_prov_dispatch():
        p = json.loads(PROV_PATH.read_text(encoding="utf-8"))
        f1 = next(f for f in p["facts"] if f["fact_id"] == "FACT-ADB-01")
        f1["arm64_evidence"]["va"] = "0x000000"
        validate_adb_channel_semantics(provenance=p)
    test_cases.append(("Case 13: Rejection of Corrupted Dispatch Site VA in Provenance", case_prov_dispatch, ValueError))

    # Case 14: Provenance Missing Send Callsite
    def case_prov_send():
        p = json.loads(PROV_PATH.read_text(encoding="utf-8"))
        f6 = next(f for f in p["facts"] if f["fact_id"] == "FACT-ADB-06")
        f6["arm64_evidence"]["call"] = "(*DataChannel).SendText @ 0x49a460"
        validate_adb_channel_semantics(provenance=p)
    test_cases.append(("Case 14: Rejection of SendText Substitution in Provenance", case_prov_send, ValueError))

    # Case 15: Contract Taxonomy Inflation
    def case_taxonomy_inflation():
        c = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        c["metadata"]["taxonomy_counts"]["original_static_evidence"] = 9
        validate_adb_channel_semantics(contract=c)
    test_cases.append(("Case 15: Rejection of Contract Taxonomy Inflation (9 instead of 8)", case_taxonomy_inflation, ValueError))

    # Case 16: Derivation Anti-Tautology Negative Test
    def case_derivation_anti_tautology():
        with tempfile.TemporaryDirectory() as td:
            # 1. Mutate canonical protocol spec in temp directory
            mut_spec_path = Path(td) / "ADB_CHANNEL_B6F_PROTOCOL_SPEC.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["channel_identity"]["label"] = "tampered-adb"
            mut_spec_path.write_text(json.dumps(s), encoding="utf-8")

            # 2. Run fresh derivation pipeline into temp derived dir
            t_derived = Path(td) / "derived"
            derived = derive_adb_channel_artifacts(output_dir=t_derived)

            # 3. Assert fresh derivation still produces authentic label
            fresh_spec = derived["ADB_CHANNEL_B6F_PROTOCOL_SPEC.json"]
            if fresh_spec["channel_identity"]["label"] != "adb-channel":
                raise AssertionError(f"Fresh derivation was polluted by external artifact!")

            # 4. Semantic comparison against mutated spec MUST FAIL
            validate_adb_channel_semantics(spec=mut_spec_path)
    test_cases.append(("Case 16: Derivation Anti-Tautology Rejection of External Canonical Mutation", case_derivation_anti_tautology, ValueError))

    # Case 17: Static Audit Output-Dependency Guard
    def case_output_dependency_guard():
        derive_script = REPO_ROOT / "tools" / "forensics" / "adb_channel" / "derive_adb_channel_protocol.py"
        src = derive_script.read_text(encoding="utf-8")
        forbidden_targets = [
            "ADB_CHANNEL_B6F_PROTOCOL_SPEC.json",
            "ADB_CHANNEL_B6F_TOPOLOGY.json",
            "ADB_CHANNEL_B6F_MESSAGE_FRAMING.json",
            "ADB_CHANNEL_B6F_CALLGRAPH.json",
            "ADB_CHANNEL_B6F_SOURCE_PROVENANCE.json",
            "ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json"
        ]
        for target in forbidden_targets:
            for line in src.splitlines():
                if target in line and ("read_text" in line or "read_bytes" in line or "open(" in line):
                    raise AssertionError(f"Output dependency guard failed: line reads {target}: {line}")
    test_cases.append(("Case 17: Static Audit Output-Dependency Guard for Semantic Derivation Pipeline", case_output_dependency_guard, None))

    # Case 18: Errata Missing Required Correction
    def case_errata_missing_corr():
        err = json.loads(ERRATA_PATH.read_text(encoding="utf-8"))
        err["corrections"] = [c for c in err["corrections"] if c["contract_id"] != "ADB-B6F-ERRATA-01"]
        validate_adb_channel_semantics(errata=err)
    test_cases.append(("Case 18: Rejection of Missing ADB-B6F-ERRATA-01 Correction", case_errata_missing_corr, ValueError))

    # Case 19: Reconstructed Production Tree ADB Inertness Scan
    def case_production_inertness_scan():
        from tools.audit.b2_common import scan_deferred_channels_isolation
        prod_root = REPO_ROOT / "reconstructed_source" / "cloudphone-agent" / "pkg"
        violations = scan_deferred_channels_isolation(prod_root, phase="B6F")
        if violations:
            raise AssertionError(f"Production scan failed: {violations}")
    test_cases.append(("Case 19: Reconstructed Production Tree ADB Inertness Scan", case_production_inertness_scan, None))

    # Case 20: Rejection of Browser Creator Evidence Promoted to Pure Original STATIC
    def case_promote_creator_to_static():
        s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        s["channel_identity"]["creator_evidence_class"] = "STATIC_CONFIRMED"
        validate_adb_channel_semantics(spec=s)
    test_cases.append(("Case 20: Rejection of Browser Creator Evidence Promoted to Pure Original STATIC", case_promote_creator_to_static, ValueError))

    # Case 21: Rejection of Removed OnOpen or OnClose Lifecycle Evidence
    def case_remove_lifecycle_evidence():
        cg = json.loads(CG_PATH.read_text(encoding="utf-8"))
        del cg["nodes"]["ARM64"]["onclose_registration"]
        validate_adb_channel_semantics(callgraph=cg)
    test_cases.append(("Case 21: Rejection of Removed OnOpen or OnClose Lifecycle Evidence", case_remove_lifecycle_evidence, ValueError))

    # Case 22: Rejection of Stale 'Only OnMessage / No OnClose' Lifecycle Claim
    def case_stale_only_onmessage_claim():
        cg = json.loads(CG_PATH.read_text(encoding="utf-8"))
        cg["nodes"]["ARM64"]["lifecycle_policy"] = "ONLY_ONMESSAGE"
        validate_adb_channel_semantics(callgraph=cg)
    test_cases.append(("Case 22: Rejection of Stale 'Only OnMessage / No OnClose' Lifecycle Claim", case_stale_only_onmessage_claim, ValueError))

    passed = 0
    total = len(test_cases)
    for name, func, expected_exc in test_cases:
        try:
            func()
            if expected_exc is not None:
                print(f"[FAIL] {name}: Expected {expected_exc.__name__} but succeeded unexpectedly")
            else:
                print(f"[PASS] {name}: Verified successfully")
                passed += 1
        except Exception as e:
            if expected_exc is not None and isinstance(e, expected_exc):
                print(f"[PASS] {name}: Correctly failed-closed ({e})")
                passed += 1
            elif expected_exc is None:
                print(f"[FAIL] {name}: Unexpected exception {e}")
            else:
                print(f"[FAIL] {name}: Expected {expected_exc.__name__}, got {type(e).__name__}: {e}")

    print("--------------------------------------------------")
    print(f"B6F Negative Mutation Results: {passed}/{total} PASSED")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    run_negative_tests()
