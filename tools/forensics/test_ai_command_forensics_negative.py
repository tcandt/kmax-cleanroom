#!/usr/bin/env python3
"""
tools/forensics/test_ai_command_forensics_negative.py
Phase 2C.5B5FR AI Command Negative Mutation & Verifier Fail-Closed Test Suite.

Executes negative mutation test cases using the shared semantic validator,
effective contract builder, and test attribution evaluators against mutated
temporary files on disk to verify that every corruption, tampered hash,
misclassification, or omitted test fails closed.
"""
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.ai_command.validate_ai_command_semantics import validate_ai_command_semantics
from tools.audit.build_b5f_effective_contract import build_b5f_effective_contract, FROZEN_BASE_SHA256

EVID_DIR = REPO_ROOT / "evidence" / "go_agent" / "webrtc"
SPEC_PATH = EVID_DIR / "AI_COMMAND_B5F_PROTOCOL_SPEC.json"
CONTRACT_PATH = EVID_DIR / "AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json"
ERRATA_PATH = EVID_DIR / "AI_COMMAND_B5F_CONTRACT_ERRATA.json"
INVENTORY_PATH = EVID_DIR / "AI_COMMAND_B5F_MESSAGE_INVENTORY.json"
CALLGRAPH_PATH = EVID_DIR / "AI_COMMAND_B5F_CALLGRAPH.json"
PROVENANCE_PATH = EVID_DIR / "AI_COMMAND_B5F_SOURCE_PROVENANCE.json"

REQUIRED_AI_TESTS = {
    "TestParseAICommand_Valid",
    "TestParseAICommand_MalformedJSON",
    "TestParseAICommand_EmptyJSON",
    "TestValidateAICommand_DefensiveChecks",
    "TestMarshalAICommandResponse_Valid",
    "TestMarshalAICommandResponse_Nil",
    "TestAICommand_CorrelationEcho",
}


def evaluate_ai_command_test_events(events: List[Dict[str, Any]], required_tests: Set[str]) -> Tuple[bool, str]:
    """
    Exact Go test attribution evaluator:
    Requires each mapped test to exist, pass, and not be skipped.
    Requires package to pass and overall run to be successful.
    """
    seen_tests = set()
    passed_tests = set()
    skipped_tests = set()
    failed_tests = set()
    package_pass = False

    for ev in events:
        test_name = ev.get("Test")
        action = ev.get("Action")
        if test_name:
            seen_tests.add(test_name)
            if action == "pass":
                passed_tests.add(test_name)
            elif action == "skip":
                skipped_tests.add(test_name)
            elif action == "fail":
                failed_tests.add(test_name)
        else:
            # Package-level event
            if action == "pass":
                package_pass = True

    # 1. Check all required tests exist
    missing = required_tests - seen_tests
    if missing:
        return False, f"Missing required unit test(s): {', '.join(sorted(missing))}"

    # 2. Check no required test was skipped
    skipped_required = required_tests.intersection(skipped_tests)
    if skipped_required:
        return False, f"Required test(s) skipped: {', '.join(sorted(skipped_required))}"

    # 3. Check no required test failed
    failed_required = required_tests.intersection(failed_tests)
    if failed_required:
        return False, f"Required test(s) failed: {', '.join(sorted(failed_required))}"

    # 4. Check all required tests passed
    unpassed = required_tests - passed_tests
    if unpassed:
        return False, f"Required test(s) did not pass: {', '.join(sorted(unpassed))}"

    # 5. Check package pass
    if not package_pass:
        return False, "Package did not report pass action"

    return True, f"All {len(required_tests)} required unit tests verified passed without skips"


def run_negative_mutations():
    print("==================================================")
    print("PHASE 2C.5B5FR AI COMMAND NEGATIVE MUTATION TEST SUITE")
    print("==================================================")

    test_cases = []

    # Case 1: Response framing swapped from BINARY_JSON_BYTES to JSON_TEXT
    def case_response_framing_swapped():
        with tempfile.TemporaryDirectory() as td:
            s_file = Path(td) / "spec.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["directional_framing"]["agent_to_browser_response"]["framing_type"] = "JSON_TEXT"
            s_file.write_text(json.dumps(s), encoding="utf-8")
            validate_ai_command_semantics(spec=s_file, contract=CONTRACT_PATH)

    test_cases.append(("Case 1: Rejection of Response Framing Swapped to JSON_TEXT", case_response_framing_swapped, ValueError))

    # Case 2: Request framing swapped to RAW_BINARY
    def case_request_framing_swapped():
        with tempfile.TemporaryDirectory() as td:
            s_file = Path(td) / "spec.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["directional_framing"]["browser_to_agent_request"]["framing_type"] = "RAW_BINARY"
            s_file.write_text(json.dumps(s), encoding="utf-8")
            validate_ai_command_semantics(spec=s_file, contract=CONTRACT_PATH)

    test_cases.append(("Case 2: Rejection of Request Framing Swapped to RAW_BINARY", case_request_framing_swapped, ValueError))

    # Case 3: Missing-field validation promoted to STATIC without binary branch
    def case_missing_field_promoted():
        with tempfile.TemporaryDirectory() as td:
            s_file = Path(td) / "spec.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["message_schemas"]["request"]["fields"][0]["classification"] = "ORIGINAL_REQUIRED_NONEMPTY_FIELDS"
            s_file.write_text(json.dumps(s), encoding="utf-8")
            validate_ai_command_semantics(spec=s_file, contract=CONTRACT_PATH)

    test_cases.append(("Case 3: Rejection of Field Validation Promoted to STATIC", case_missing_field_promoted, ValueError))

    # Case 4: Ordered=true promoted from frontend-only to Agent STATIC_CONFIRMED
    def case_ordered_promoted_to_static():
        with tempfile.TemporaryDirectory() as td:
            s_file = Path(td) / "spec.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["channel_properties"]["ordered"]["evidence_class"] = "STATIC_CONFIRMED"
            s_file.write_text(json.dumps(s), encoding="utf-8")
            validate_ai_command_semantics(spec=s_file, contract=CONTRACT_PATH)

    test_cases.append(("Case 4: Rejection of Inbound Ordered Promoted to Agent STATIC", case_ordered_promoted_to_static, ValueError))

    # Case 5: Execution-boundary fact changed into production executor requirement
    def case_execution_boundary_made_production_requirement():
        with tempfile.TemporaryDirectory() as td:
            c_file = Path(td) / "contract.json"
            c = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
            r10 = next(r for r in c["requirements"] if r["id"] == "AI-B5F-10")
            r10["evidence_class"] = "MANDATORY_PRODUCTION_EXECUTOR"
            c_file.write_text(json.dumps(c), encoding="utf-8")
            validate_ai_command_semantics(spec=SPEC_PATH, contract=c_file)

    test_cases.append(("Case 5: Rejection of Execution Boundary Made Production Requirement", case_execution_boundary_made_production_requirement, ValueError))

    # Case 6: AI parser presence falsely treated as channel activation
    def case_parser_presence_treated_as_activation():
        with tempfile.TemporaryDirectory() as td:
            c_file = Path(td) / "contract.json"
            c = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
            r15 = next(r for r in c["requirements"] if r["id"] == "AI-B5F-15")
            r15["observable_behavior"] = "Agent must activate ai-command-channel OnMessage in production"
            c_file.write_text(json.dumps(c), encoding="utf-8")
            validate_ai_command_semantics(spec=SPEC_PATH, contract=c_file)

    test_cases.append(("Case 6: Rejection of Parser Presence Treated as Channel Activation", case_parser_presence_treated_as_activation, ValueError))

    # Case 7: Response send method corrupted to SendText
    def case_response_send_text_corrupted():
        with tempfile.TemporaryDirectory() as td:
            s_file = Path(td) / "spec.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["directional_framing"]["agent_to_browser_response"]["agent_send_method"] = "(*DataChannel).SendText (string)"
            s_file.write_text(json.dumps(s), encoding="utf-8")
            validate_ai_command_semantics(spec=s_file, contract=CONTRACT_PATH)

    test_cases.append(("Case 7: Rejection of Response Send Method Swapped to SendText", case_response_send_text_corrupted, ValueError))

    # Case 8: Malformed JSON semantics broken (not LOG_AND_DROP)
    def case_malformed_json_broken():
        with tempfile.TemporaryDirectory() as td:
            s_file = Path(td) / "spec.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["message_schemas"]["request"]["malformed_json_semantics"]["behavior"] = "SEND_ERROR_RESPONSE"
            s_file.write_text(json.dumps(s), encoding="utf-8")
            validate_ai_command_semantics(spec=s_file, contract=CONTRACT_PATH)

    test_cases.append(("Case 8: Rejection of Broken Malformed JSON Semantics", case_malformed_json_broken, ValueError))

    # Case 9: Channel label tampered
    def case_channel_label_tampered():
        with tempfile.TemporaryDirectory() as td:
            s_file = Path(td) / "spec.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["channel_properties"]["label"] = "ai-command"
            s_file.write_text(json.dumps(s), encoding="utf-8")
            validate_ai_command_semantics(spec=s_file, contract=CONTRACT_PATH)

    test_cases.append(("Case 9: Rejection of Tampered Channel Label", case_channel_label_tampered, ValueError))

    # Case 10: Request ID correlation broken
    def case_request_id_correlation_broken():
        with tempfile.TemporaryDirectory() as td:
            c_file = Path(td) / "contract.json"
            c = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
            r12 = next(r for r in c["requirements"] if r["id"] == "AI-B5F-12")
            r12["evidence_class"] = "UNKNOWN"
            c_file.write_text(json.dumps(c), encoding="utf-8")
            validate_ai_command_semantics(spec=SPEC_PATH, contract=c_file)

    test_cases.append(("Case 10: Rejection of Broken Request ID Correlation", case_request_id_correlation_broken, ValueError))

    # Case 11: Concurrency model altered to worker pool
    def case_concurrency_model_altered():
        with tempfile.TemporaryDirectory() as td:
            s_file = Path(td) / "spec.json"
            s = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
            s["concurrency_model"]["model"] = "WORKER_POOL"
            s_file.write_text(json.dumps(s), encoding="utf-8")
            validate_ai_command_semantics(spec=s_file, contract=CONTRACT_PATH)

    test_cases.append(("Case 11: Rejection of Altered Concurrency Model", case_concurrency_model_altered, ValueError))

    # Case 12: Real disk tamper of frozen implementation contract bytes
    def case_contract_hash_tampered_on_disk():
        with tempfile.TemporaryDirectory() as td:
            t_root = Path(td)
            t_evid = t_root / "evidence" / "go_agent" / "webrtc"
            t_evid.mkdir(parents=True)
            # Copy base contract and errata
            shutil.copy(CONTRACT_PATH, t_evid / "AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json")
            shutil.copy(ERRATA_PATH, t_evid / "AI_COMMAND_B5F_CONTRACT_ERRATA.json")
            # Corrupt contract file on disk
            with open(t_evid / "AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json", "ab") as f:
                f.write(b"// CORRUPTION TAMPER\n")
            # Invoke effective contract builder on temp repo root
            build_b5f_effective_contract(t_root)

    test_cases.append(("Case 12: Rejection of Tampered Contract Bytes on Disk", case_contract_hash_tampered_on_disk, ValueError))

    # Case 13: Unit Test Negative Attribution - Nonexistent Mapped Test
    def case_missing_mapped_test():
        mock_events = [
            {"Test": "TestParseAICommand_Valid", "Action": "pass"},
            {"Test": "TestParseAICommand_MalformedJSON", "Action": "pass"},
            # Missing TestParseAICommand_EmptyJSON
            {"Test": "TestValidateAICommand_DefensiveChecks", "Action": "pass"},
            {"Test": "TestMarshalAICommandResponse_Valid", "Action": "pass"},
            {"Test": "TestMarshalAICommandResponse_Nil", "Action": "pass"},
            {"Test": "TestAICommand_CorrelationEcho", "Action": "pass"},
            {"Action": "pass"}  # Package pass
        ]
        ok, msg = evaluate_ai_command_test_events(mock_events, REQUIRED_AI_TESTS)
        if ok:
            raise AssertionError("Evaluator falsely passed with missing required test")
        if "Missing required unit test" not in msg:
            raise ValueError(f"Unexpected error message: {msg}")

    test_cases.append(("Case 13: Unit Test Attribution Rejection of Missing Mapped Test", case_missing_mapped_test, None))

    # Case 14: Unit Test Negative Attribution - Skipped Mapped Test
    def case_skipped_mapped_test():
        mock_events = [
            {"Test": "TestParseAICommand_Valid", "Action": "pass"},
            {"Test": "TestParseAICommand_MalformedJSON", "Action": "pass"},
            {"Test": "TestParseAICommand_EmptyJSON", "Action": "skip"},  # Skipped!
            {"Test": "TestValidateAICommand_DefensiveChecks", "Action": "pass"},
            {"Test": "TestMarshalAICommandResponse_Valid", "Action": "pass"},
            {"Test": "TestMarshalAICommandResponse_Nil", "Action": "pass"},
            {"Test": "TestAICommand_CorrelationEcho", "Action": "pass"},
            {"Action": "pass"}  # Package pass
        ]
        ok, msg = evaluate_ai_command_test_events(mock_events, REQUIRED_AI_TESTS)
        if ok:
            raise AssertionError("Evaluator falsely passed with skipped required test")
        if "skipped" not in msg:
            raise ValueError(f"Unexpected error message: {msg}")

    test_cases.append(("Case 14: Unit Test Attribution Rejection of Skipped Mapped Test", case_skipped_mapped_test, None))

    # Case 15: Unit Test Negative Attribution - Package Pass with Exact Tests Absent
    def case_package_pass_without_exact_tests():
        mock_events = [
            {"Test": "SomeOtherTest", "Action": "pass"},
            {"Action": "pass"}  # Package pass
        ]
        ok, msg = evaluate_ai_command_test_events(mock_events, REQUIRED_AI_TESTS)
        if ok:
            raise AssertionError("Evaluator falsely passed package pass without exact tests")
        if "Missing required unit test" not in msg:
            raise ValueError(f"Unexpected error message: {msg}")

    test_cases.append(("Case 15: Unit Test Attribution Rejection of Package Pass without Exact Tests", case_package_pass_without_exact_tests, None))

    passed = 0
    total = len(test_cases)
    for name, func, expected_exc in test_cases:
        try:
            func()
            if expected_exc is not None:
                print(f"[FAIL] {name}: Did not raise expected {expected_exc.__name__}")
            else:
                print(f"[PASS] {name}: Correctly failed-closed on invalid test stream")
                passed += 1
        except Exception as e:
            if expected_exc is not None:
                if isinstance(e, expected_exc):
                    print(f"[PASS] {name}: Correctly failed-closed ({type(e).__name__}: {str(e)[:70]}...)")
                    passed += 1
                else:
                    print(f"[FAIL] {name}: Raised unexpected exception {type(e).__name__}: {e}")
            else:
                print(f"[FAIL] {name}: Raised unexpected exception {type(e).__name__}: {e}")

    print("--------------------------------------------------")
    print(f"B5F Negative Mutation Results: {passed}/{total} PASSED")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    run_negative_mutations()
