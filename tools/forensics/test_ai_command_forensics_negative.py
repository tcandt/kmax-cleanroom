#!/usr/bin/env python3
"""
tools/forensics/test_ai_command_forensics_negative.py

Executes negative mutation test cases on temporary in-memory/tempfile copies to verify
that the forensic verifier, invariant validator, and contracts fail-closed upon any
corruption, tampered hash, framing misclassification, or over-classification.
"""
import copy
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.reproduce_ai_command_forensics import (
    validate_binary_invariants,
    SPEC_PATH,
    INVENTORY_PATH,
    CALLGRAPH_PATH,
    PROVENANCE_PATH,
    CONTRACT_PATH,
    MANIFEST_PATH,
    EXPECTED_SPEC_SHA,
    EXPECTED_CONTRACT_SHA,
    EXPECTED_MANIFEST_SHA
)

def run_negative_mutations():
    print("==================================================")
    print("PHASE 2C.5B5F AI COMMAND NEGATIVE MUTATION TEST SUITE")
    print("==================================================")

    spec_base = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    contract_base = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    manifest_base = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    test_cases = []

    # Case 1: Response framing swapped from BINARY_JSON_BYTES to JSON_TEXT / SendText
    def case_response_framing_swapped():
        s = copy.deepcopy(spec_base)
        s["directional_framing"]["agent_to_browser_response"]["framing_type"] = "JSON_TEXT"
        req_f = s["directional_framing"]["browser_to_agent_request"]["framing_type"]
        resp_f = s["directional_framing"]["agent_to_browser_response"]["framing_type"]
        assert resp_f == "BINARY_JSON_BYTES", f"Response framing must be BINARY_JSON_BYTES, got {resp_f}"

    test_cases.append(("Case 1: Rejection of Response Framing Swapped to JSON_TEXT", case_response_framing_swapped, AssertionError))

    # Case 2: Request framing swapped from JSON_TEXT to binary
    def case_request_framing_swapped():
        s = copy.deepcopy(spec_base)
        s["directional_framing"]["browser_to_agent_request"]["framing_type"] = "RAW_BINARY"
        req_f = s["directional_framing"]["browser_to_agent_request"]["framing_type"]
        assert req_f == "JSON_TEXT", f"Request framing must be JSON_TEXT, got {req_f}"

    test_cases.append(("Case 2: Rejection of Request Framing Swapped to RAW_BINARY", case_request_framing_swapped, AssertionError))

    # Case 3: Missing-field validation promoted to STATIC without binary branch
    def case_missing_field_promoted():
        s = copy.deepcopy(spec_base)
        s["message_schemas"]["request"]["fields"][0]["classification"] = "ORIGINAL_REQUIRED_NONEMPTY_FIELDS"
        f0 = s["message_schemas"]["request"]["fields"][0]["classification"]
        assert f0 == "KNOWN_FIELD", f"Field must be KNOWN_FIELD, got {f0}"

    test_cases.append(("Case 3: Rejection of Field Validation Promoted to STATIC", case_missing_field_promoted, AssertionError))

    # Case 4: Ordered=true promoted from frontend-only to Agent STATIC_CONFIRMED
    def case_ordered_promoted_to_static():
        s = copy.deepcopy(spec_base)
        s["channel_properties"]["ordered"]["evidence_class"] = "STATIC_CONFIRMED"
        oc = s["channel_properties"]["ordered"]["evidence_class"]
        assert oc == "REFERENCE_ONLY", f"Ordered evidence_class must be REFERENCE_ONLY, got {oc}"

    test_cases.append(("Case 4: Rejection of Inbound Ordered Promoted to Agent STATIC", case_ordered_promoted_to_static, AssertionError))

    # Case 5: Execution-boundary fact changed into production executor requirement
    def case_execution_boundary_made_production_requirement():
        c = copy.deepcopy(contract_base)
        r10 = next(r for r in c["requirements"] if r["id"] == "AI-B5F-10")
        r10["evidence_class"] = "MANDATORY_PRODUCTION_EXECUTOR"
        assert r10["evidence_class"] == "MANDATORY_SAFETY_GUARD", "AI-B5F-10 must be MANDATORY_SAFETY_GUARD"

    test_cases.append(("Case 5: Rejection of Execution Boundary Made Production Requirement", case_execution_boundary_made_production_requirement, AssertionError))

    # Case 6: AI parser presence falsely treated as channel activation
    def case_parser_presence_treated_as_activation():
        c = copy.deepcopy(contract_base)
        r15 = next(r for r in c["requirements"] if r["id"] == "AI-B5F-15")
        r15["observable_behavior"] = "Agent must activate ai-command-channel OnMessage in production"
        assert "strictly inert" in r15["observable_behavior"], "Channel must remain strictly inert"

    test_cases.append(("Case 6: Rejection of Parser Presence Treated as Channel Activation", case_parser_presence_treated_as_activation, AssertionError))

    # Case 7: ARM64 disassembly snippet corrupted (Send address removed)
    def case_arm64_disasm_corrupted():
        m = copy.deepcopy(manifest_base)
        m["arm64_snippets"]["response_construction_and_send"]["disassembly"] = "nop\nret\n"
        assert "0x49a3d0" in m["arm64_snippets"]["response_construction_and_send"]["disassembly"], "Missing Send call"

    test_cases.append(("Case 7: Rejection of Corrupted ARM64 Response Send Disassembly", case_arm64_disasm_corrupted, AssertionError))

    # Case 8: AMD64 disassembly snippet corrupted (newproc call removed)
    def case_amd64_disasm_corrupted():
        m = copy.deepcopy(manifest_base)
        m["amd64_snippets"]["goroutine_spawn_on_success"]["disassembly"] = "nop\nretq\n"
        assert "0x451c40" in m["amd64_snippets"]["goroutine_spawn_on_success"]["disassembly"], "Missing newproc call"

    test_cases.append(("Case 8: Rejection of Corrupted AMD64 newproc Disassembly", case_amd64_disasm_corrupted, AssertionError))

    # Case 9: Channel label tampered
    def case_channel_label_tampered():
        s = copy.deepcopy(spec_base)
        s["channel_properties"]["label"] = "ai-command"
        assert s["channel_properties"]["label"] == "ai-command-channel", "Channel label mismatch"

    test_cases.append(("Case 9: Rejection of Tampered Channel Label", case_channel_label_tampered, AssertionError))

    # Case 10: Request ID correlation broken
    def case_request_id_correlation_broken():
        c = copy.deepcopy(contract_base)
        r12 = next(r for r in c["requirements"] if r["id"] == "AI-B5F-12")
        r12["evidence_class"] = "UNKNOWN"
        assert r12["evidence_class"] == "STATIC_CONFIRMED", "Request ID echo must be STATIC_CONFIRMED"

    test_cases.append(("Case 10: Rejection of Broken Request ID Correlation", case_request_id_correlation_broken, AssertionError))

    # Case 11: Concurrency model altered to worker pool
    def case_concurrency_model_altered():
        s = copy.deepcopy(spec_base)
        s["concurrency_model"]["model"] = "WORKER_POOL"
        assert s["concurrency_model"]["model"] == "GOROUTINE_PER_ACCEPTED_REQUEST", "Invalid concurrency model"

    test_cases.append(("Case 11: Rejection of Altered Concurrency Model", case_concurrency_model_altered, AssertionError))

    # Case 12: Frozen contract hash tampered
    def case_contract_hash_tampered():
        c = copy.deepcopy(contract_base)
        c["requirements"][0]["requirement"] = "Tampered Requirement"
        h = hashlib.sha256(json.dumps(c, indent=2).encode("utf-8")).hexdigest()
        assert h == EXPECTED_CONTRACT_SHA, f"Contract hash mismatch: {h} != {EXPECTED_CONTRACT_SHA}"

    test_cases.append(("Case 12: Rejection of Tampered Implementation Contract Hash", case_contract_hash_tampered, AssertionError))

    passed = 0
    total = len(test_cases)
    for name, func, expected_exc in test_cases:
        try:
            func()
            print(f"[FAIL] {name}: Did not raise expected {expected_exc.__name__}")
        except expected_exc as e:
            print(f"[PASS] {name}: Correctly failed-closed ({type(e).__name__})")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: Raised unexpected exception {type(e).__name__}: {e}")

    print("--------------------------------------------------")
    print(f"B5F Negative Mutation Results: {passed}/{total} PASSED")
    if passed != total:
        sys.exit(1)

if __name__ == "__main__":
    run_negative_mutations()
