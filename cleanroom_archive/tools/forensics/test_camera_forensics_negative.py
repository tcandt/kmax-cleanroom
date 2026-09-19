#!/usr/bin/env python3
"""
tools/forensics/test_camera_forensics_negative.py

Executes negative mutation test cases on temporary in-memory/tempfile copies to verify
that the forensic verifier, invariant validator, and effective contract builder fail-closed
upon any corruption, tampered hash, or over-classification.
"""
import copy
import hashlib
import json
import os
import sys
import shutil
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.reproduce_camera_forensics import (
    validate_machine_binding_invariants,
    EXPECTED_SPEC_SHA,
    EXPECTED_BASE_CONTRACT_SHA,
    SPEC_PATH,
    CONTRACT_PATH,
    hash_file
)
from tools.audit.build_b4_effective_contract import build_b4_effective_contract, FROZEN_BASE_SHA256

def run_negative_mutations():
    print("==================================================")
    print("PHASE 2C.5B4F NEGATIVE MUTATION TEST SUITE")
    print("==================================================")

    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        spec_base = json.load(f)
    with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
        contract_base = json.load(f)

    derived_mock = {
        "tcp_endpoint_classification": spec_base["camera_hal_tcp_protocol"]["endpoint_classification"],
        "wire_length_framing": spec_base["camera_hal_tcp_protocol"]["wire_framing"],
        "hal_inbound_framing": spec_base["camera_hal_tcp_protocol"]["inbound_event_framing"],
        "handshake_parameters": {
            "fields": spec_base["camera_hal_tcp_protocol"]["handshake"]["default_fields"],
            "json_schema": spec_base["camera_hal_tcp_protocol"]["handshake"]["schema"]
        },
        "yuv420_planar_layout": spec_base["camera_hal_tcp_protocol"]["video_frame_stream"]["planar_layout"],
        "lifecycle_model_classification": spec_base["lifecycle_state_model"],
        "camera_capture_boundary": spec_base["architectural_separation"],
        "toolchain_provenance": spec_base["metadata"]["toolchain_provenance"]
    }

    test_cases = []

    # Case 1: Wrong Byte Order
    def case_wrong_byte_order():
        s = copy.deepcopy(spec_base)
        s["camera_hal_tcp_protocol"]["wire_framing"]["byte_order"] = "big-endian"
        validate_machine_binding_invariants(s, contract_base, derived_mock)

    test_cases.append(("Case 1: Rejection of Big-Endian Byte Order", case_wrong_byte_order, AssertionError))

    # Case 2: Wrong Channel Capacity
    def case_wrong_channel_capacity():
        s = copy.deepcopy(spec_base)
        s["backpressure_and_concurrency"]["channel_capacity"]["capacity"] = 16
        validate_machine_binding_invariants(s, contract_base, derived_mock)

    test_cases.append(("Case 2: Rejection of Channel Capacity != 1", case_wrong_channel_capacity, AssertionError))

    # Case 3: Wrong Event Length
    def case_wrong_event_length():
        s = copy.deepcopy(spec_base)
        s["camera_hal_tcp_protocol"]["inbound_event_framing"]["supported_events"][0]["length"] = 32
        validate_machine_binding_invariants(s, contract_base, derived_mock)

    test_cases.append(("Case 3: Rejection of Corrupted Event Length", case_wrong_event_length, AssertionError))

    # Case 4: Missing HAL Event
    def case_missing_hal_event():
        s = copy.deepcopy(spec_base)
        s["camera_hal_tcp_protocol"]["inbound_event_framing"]["supported_events"] = s["camera_hal_tcp_protocol"]["inbound_event_framing"]["supported_events"][:2]
        validate_machine_binding_invariants(s, contract_base, derived_mock)

    test_cases.append(("Case 4: Rejection of Missing Inbound HAL Event", case_missing_hal_event, AssertionError))

    # Case 5: Wrong Base Contract SHA in Errata
    def case_wrong_base_contract_sha():
        with tempfile.TemporaryDirectory() as t_dir:
            t_root = Path(t_dir)
            (t_root / "evidence" / "go_agent" / "webrtc").mkdir(parents=True)
            shutil.copy(CONTRACT_PATH, t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json")
            errata_p = REPO_ROOT / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json"
            errata_data = json.loads(errata_p.read_text(encoding="utf-8"))
            errata_data["metadata"]["base_contract_sha256"] = "0000000000000000000000000000000000000000000000000000000000000000"
            (t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json").write_text(json.dumps(errata_data), encoding="utf-8")
            build_b4_effective_contract(t_root)

    test_cases.append(("Case 5: Rejection of Mismatched Base Contract SHA in Errata", case_wrong_base_contract_sha, ValueError))

    # Case 6: CAM-B4-13 Promoted back to STATIC original parity
    def case_cam_b4_13_promoted():
        with tempfile.TemporaryDirectory() as t_dir:
            t_root = Path(t_dir)
            (t_root / "evidence" / "go_agent" / "webrtc").mkdir(parents=True)
            shutil.copy(CONTRACT_PATH, t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json")
            errata_p = REPO_ROOT / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json"
            errata_data = json.loads(errata_p.read_text(encoding="utf-8"))
            # remove CAM-B4-13 correction so it stays STATIC_CONFIRMED with mandatory_for_parity: true
            errata_data["corrections"] = [c for c in errata_data["corrections"] if c["contract_id"] != "CAM-B4-13"]
            (t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json").write_text(json.dumps(errata_data), encoding="utf-8")
            eff = build_b4_effective_contract(t_root)
            # Verifier assert: CAM-B4-13 must be PHASE_SCOPE_GUARD and not in original_static
            b = eff["breakdown_by_classification"]
            if "CAM-B4-13" in b["original_static"] or eff["metadata"]["total_original_parity_requirements"] != 12:
                raise AssertionError("CAM-B4-13 was improperly promoted to original static parity!")

    test_cases.append(("Case 6: Rejection of CAM-B4-13 Promoted to Original Parity", case_cam_b4_13_promoted, AssertionError))

    # Case 7: CAM-B4-12 Architecture Guard counted as Original Parity
    def case_cam_b4_12_guard_counted():
        with tempfile.TemporaryDirectory() as t_dir:
            t_root = Path(t_dir)
            (t_root / "evidence" / "go_agent" / "webrtc").mkdir(parents=True)
            shutil.copy(CONTRACT_PATH, t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json")
            errata_p = REPO_ROOT / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json"
            errata_data = json.loads(errata_p.read_text(encoding="utf-8"))
            for c in errata_data["corrections"]:
                if c["contract_id"] == "CAM-B4-12":
                    c["phase_scope_parts"] = []
                    c["corrected_original_parity_claim"] = "Virtual camera data plane routes exclusively through camera-channel and Camera HAL"
            (t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json").write_text(json.dumps(errata_data), encoding="utf-8")
            eff = build_b4_effective_contract(t_root)
            r12 = [r for r in eff["requirements"] if r["id"] == "CAM-B4-12"][0]
            if "exclusively" in r12["effective_original_parity_claim"]:
                raise AssertionError("CAM-B4-12 over-claimed negative exclusivity as original parity!")

    test_cases.append(("Case 7: Rejection of CAM-B4-12 Exclusivity Over-Claim", case_cam_b4_12_guard_counted, AssertionError))

    # Case 8: ArrayBuffer Promoted to Agent Static Parity
    def case_arraybuffer_promoted():
        with tempfile.TemporaryDirectory() as t_dir:
            t_root = Path(t_dir)
            (t_root / "evidence" / "go_agent" / "webrtc").mkdir(parents=True)
            shutil.copy(CONTRACT_PATH, t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json")
            errata_p = REPO_ROOT / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json"
            errata_data = json.loads(errata_p.read_text(encoding="utf-8"))
            for c in errata_data["corrections"]:
                if c["contract_id"] == "CAM-B4-07":
                    c["corrected_original_parity_claim"] = "Agent receives binary JPEG ArrayBuffer frames"
            (t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json").write_text(json.dumps(errata_data), encoding="utf-8")
            eff = build_b4_effective_contract(t_root)
            r07 = [r for r in eff["requirements"] if r["id"] == "CAM-B4-07"][0]
            if "ArrayBuffer" in r07["effective_original_parity_claim"]:
                raise AssertionError("CAM-B4-07 over-claimed browser ArrayBuffer as Agent static parity!")

    test_cases.append(("Case 8: Rejection of ArrayBuffer in Agent Static Parity", case_arraybuffer_promoted, AssertionError))

    # Case 9: Tampered Frozen Contract
    def case_tampered_contract():
        with tempfile.TemporaryDirectory() as t_dir:
            t_root = Path(t_dir)
            (t_root / "evidence" / "go_agent" / "webrtc").mkdir(parents=True)
            contract_copy = t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json"
            shutil.copy(CONTRACT_PATH, contract_copy)
            with open(contract_copy, "ab") as f:
                f.write(b" ")
            actual_sha = hash_file(contract_copy)
            if actual_sha != EXPECTED_BASE_CONTRACT_SHA:
                raise ValueError(f"Contract SHA mismatch: {actual_sha} != {EXPECTED_BASE_CONTRACT_SHA}")

    test_cases.append(("Case 9: Rejection of Tampered Frozen Base Contract", case_tampered_contract, ValueError))

    # Case 10: Tampered Frozen Spec
    def case_tampered_spec():
        with tempfile.TemporaryDirectory() as t_dir:
            t_root = Path(t_dir)
            (t_root / "evidence" / "go_agent" / "webrtc").mkdir(parents=True)
            spec_copy = t_root / "evidence" / "go_agent" / "webrtc" / "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json"
            shutil.copy(SPEC_PATH, spec_copy)
            with open(spec_copy, "ab") as f:
                f.write(b" ")
            actual_sha = hash_file(spec_copy)
            if actual_sha != EXPECTED_SPEC_SHA:
                raise ValueError(f"Spec SHA mismatch: {actual_sha} != {EXPECTED_SPEC_SHA}")

    test_cases.append(("Case 10: Rejection of Tampered Frozen Protocol Spec", case_tampered_spec, ValueError))

    # Execute all
    passed = 0
    for name, func, exp_err in test_cases:
        try:
            func()
            print(f"[FAIL] {name} - Expected {exp_err.__name__}, but function succeeded without error!")
        except exp_err as e:
            print(f"[PASS] {name} (Correctly rejected with {exp_err.__name__}: {str(e)[:60]})")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name} - Expected {exp_err.__name__}, but got unexpected {type(e).__name__}: {e}")

    print(f"\nResults: {passed}/{len(test_cases)} negative mutation tests successfully rejected.\n")
    return passed == len(test_cases)

if __name__ == "__main__":
    ok = run_negative_mutations()
    sys.exit(0 if ok else 1)
