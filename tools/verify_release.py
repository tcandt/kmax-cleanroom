#!/usr/bin/env python3
"""
tools/verify_release.py

Phase 3AR Master Release Verifier (Fail-Closed)
Orchestrates the 11 executable internal release gates:
 Gate 1: Phase 2 Master Verifier (Phase 2 audits, B2-B6 differential checks, Go tests/race, negative mutations)
 Gate 2: Reconstructed Source Provenance Audit (--check, UNKNOWN == 0, structural locators verified)
 Gate 3: Clean-Room Contamination Audit (--check, 0 forbidden traces in working tree and post-remediation history)
 Gate 4: Original Artifacts Inventory & Purge Verification (--check, 155/155 classified, 65 required hash-verified)
 Gate 5: Frozen Contract Registry Historical Pinning (--check, all 15 contracts verified via git blob & disk hash)
 Gate 6: Toolchain Manifest & Policy Audit (--check, zero hardcoded paths, required compilers verified)
 Gate 7: Cross-Phase Fact Matrix Semantic Invariant (--check, all 6 DataChannels reconciled with canonical facts)
 Gate 8: Android Helper Method Count DEX Invariant (--check, 1,625 = 1,061 defined + 564 non-defined fully classified)
 Gate 9: Intentional Divergences Registry Verification (camera 127.0.0.1:9001, deferred boundaries explicit)
 Gate 10: Fail-Closed Negative Mutation Suite (18 genuine fail-closed mutations)
 Gate 11: Final Working Tree Cleanliness (git status --porcelain strictly empty unless --allow-dirty)

Together with the external Independent Clean-Clone Verification Gate (Gate 12),
these constitute the 12 mandatory Phase 3AR release readiness conditions.

Exit Codes:
  0: All release gates PASS
  1: Verification failure (fail-closed)
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

def run_step(gate_number, gate_name, cmd, cwd=REPO_ROOT):
    print(f"\n>> [GATE {gate_number}/11] RUNNING: {gate_name}...")
    sys.stdout.flush()
    res = subprocess.run(cmd, cwd=cwd, text=True)
    if res.returncode != 0:
        print(f"[FAIL] Gate {gate_number} ({gate_name}) failed with exit code {res.returncode}")
        return False
    print(f"[PASS] Gate {gate_number} ({gate_name})")
    return True

REQUIRED_WEBRTC_CORE_TEST_IDS = [
    "TC-WTC-UNIT-01", "TC-WTC-UNIT-02", "TC-WTC-UNIT-03", "TC-WTC-UNIT-04",
    "TC-WTC-UNIT-05", "TC-WTC-UNIT-06", "TC-WTC-UNIT-07", "TC-WTC-UNIT-08",
    "TC-WTC-UNIT-09", "TC-WTC-UNIT-10", "TC-WTC-UNIT-11", "TC-WTC-UNIT-12",
    "TC-WTC-UNIT-13", "TC-WTC-UNIT-14", "TC-WTC-UNIT-15",
    "TC-WTC-INT-01", "TC-WTC-ORACLE-01", "TC-WTC-E2E-01"
]

CANONICAL_RELEASE_FILES = [
    "tools/verify_release.py",
    "tools/verify_phase2.py",
    "tools/test_release_negative.py",
    "evidence/final/TOOLCHAIN_MANIFEST.json",
    "evidence/final/FROZEN_CONTRACT_REGISTRY.json",
    "evidence/final/PHASE3_CROSS_PHASE_FACT_MATRIX.json",
    "evidence/final/ANDROID_METHOD_COUNT_RECONCILIATION.json",
    "evidence/final/INTENTIONAL_DIVERGENCES.json",
    "evidence/final/RECONSTRUCTED_SOURCE_PROVENANCE_FINAL.json",
    "evidence/final/PROVENANCE_RULES.json"
]

def verify_clean_working_tree(repo_root=REPO_ROOT):
    res = subprocess.run(["git", "status", "--porcelain"], cwd=repo_root, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FAIL] git status failed with exit code {res.returncode}")
        return False
    status_output = res.stdout.strip()
    if status_output:
        print(f"[FAIL] Working tree is dirty! git status --porcelain:\n{status_output}")
        return False
    print("[PASS] Working tree is strictly clean.")
    return True

def validate_mapped_test_matrix(matrix_path, required_test_ids=None):
    """
    Validates a critical test matrix:
    - Traverses levels -> cases
    - Verifies presence of all required test IDs
    - Validates id, name, package non-empty
    - Validates status == 'PASS' for all cases
    - Detects duplicate IDs
    - Validates summary.total_test_cases == actual cases count
    - Validates summary.total_passed == actual passed count
    Returns (valid: bool, issues: list).
    """
    if required_test_ids is None:
        required_test_ids = REQUIRED_WEBRTC_CORE_TEST_IDS

    p = Path(matrix_path)
    if not p.exists():
        return False, [f"Matrix file missing: {p}"]

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return False, [f"JSON parse error in {p}: {e}"]

    levels = data.get("levels", {})
    if not levels:
        return False, ["No 'levels' dictionary found in test matrix"]

    cases = []
    for lvl_name, lvl_obj in levels.items():
        lvl_cases = lvl_obj.get("cases", [])
        cases.extend(lvl_cases)

    issues = []
    seen_ids = set()
    passed_count = 0

    for c in cases:
        cid = c.get("id")
        if not cid:
            issues.append("Case found without 'id' field")
            continue
        if cid in seen_ids:
            issues.append(f"Duplicate test case ID: {cid}")
        seen_ids.add(cid)

        cname = c.get("name")
        if not cname:
            issues.append(f"Case {cid} missing 'name' field")

        pkg = c.get("package")
        if not pkg:
            issues.append(f"Case {cid} missing 'package' field")

        cstatus = c.get("status")
        if cstatus != "PASS":
            issues.append(f"Case {cid} non-passing status: {cstatus}")
        else:
            passed_count += 1

    for req_id in required_test_ids:
        if req_id not in seen_ids:
            issues.append(f"Required test ID missing from matrix: {req_id}")

    summary = data.get("summary", {})
    if "total_test_cases" in summary:
        if summary["total_test_cases"] != len(cases):
            issues.append(f"Summary total_test_cases ({summary['total_test_cases']}) != actual cases count ({len(cases)})")
    if "total_passed" in summary:
        if summary["total_passed"] != passed_count:
            issues.append(f"Summary total_passed ({summary['total_passed']}) != actual passed count ({passed_count})")

    is_valid = (len(issues) == 0)
    if not is_valid:
        print(f"[FAIL] validate_mapped_test_matrix failed: {issues}")
    return is_valid, issues

def validate_test_attribution(test_results_or_path, mandatory_test_ids=None):
    """
    Validates test execution evidence for conclusive attribution:
    - Strictly rejects any non-PASS status (e.g. SKIP, SKIPPED, UNATTRIBUTED, TODO, FAIL)
    - If mandatory_test_ids provided, ensures all are represented and passed
    Returns (valid: bool, issues: list).
    """
    if isinstance(test_results_or_path, (str, Path)):
        p = Path(test_results_or_path)
        if not p.exists():
            return False, [f"Test results file missing: {p}"]
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            return False, [f"JSON parse error: {e}"]
    else:
        data = test_results_or_path

    tests = []
    if isinstance(data, list):
        tests = data
    elif isinstance(data, dict):
        if "levels" in data:
            for lvl in data["levels"].values():
                tests.extend(lvl.get("cases", []))
        elif "tests" in data:
            tests = data["tests"]
        elif "test_cases" in data:
            tests = data["test_cases"]

    issues = []
    seen_ids = set()
    for t in tests:
        tid = t.get("id") or t.get("test_id") or t.get("name")
        status = str(t.get("status", "")).upper()
        if tid:
            seen_ids.add(tid)
        if status in ("SKIP", "SKIPPED", "IGNORED", "TODO", "UNATTRIBUTED"):
            issues.append(f"Non-conclusive status '{status}' in test {tid} (fail-closed release requirement: SKIP is forbidden)")
        elif status != "PASS":
            issues.append(f"Test {tid} has non-passing status '{status}'")

    if mandatory_test_ids:
        for mid in mandatory_test_ids:
            if mid not in seen_ids:
                issues.append(f"Mandatory test {mid} missing from execution results")

    is_valid = (len(issues) == 0)
    if not is_valid:
        print(f"[FAIL] validate_test_attribution failed: {issues}")
    return is_valid, issues

def verify_clean_clone_dependencies(repo_root=REPO_ROOT, candidate_paths=None, required_files=None):
    """
    Verifies that all candidate paths and required files are tracked in Git.
    Guarantees clean-clone reproducibility without untracked/local workstation dependencies.
    Returns (clean: bool, untracked_dependencies: list).
    """
    res = subprocess.run(["git", "ls-files"], cwd=repo_root, capture_output=True, text=True)
    if res.returncode != 0:
        return False, [f"git ls-files failed with exit code {res.returncode}"]

    tracked = set(p.replace("\\", "/") for p in res.stdout.splitlines())
    untracked_dependencies = []

    if candidate_paths:
        for p in candidate_paths:
            norm = Path(p).as_posix()
            if norm not in tracked:
                untracked_dependencies.append(norm)

    if required_files:
        for rf in required_files:
            norm = Path(rf).as_posix()
            if norm not in tracked:
                untracked_dependencies.append(norm)

    is_clean = (len(untracked_dependencies) == 0)
    if not is_clean:
        print(f"[FAIL] Clean clone dependency check failed, untracked files detected: {untracked_dependencies}")
    return is_clean, untracked_dependencies

def verify_intentional_divergences():
    div_p = REPO_ROOT / "evidence" / "final" / "INTENTIONAL_DIVERGENCES.json"
    if not div_p.exists():
        print(f"[FAIL] INTENTIONAL_DIVERGENCES.json missing at {div_p}")
        return False
    try:
        div_data = json.loads(div_p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[FAIL] Invalid JSON in INTENTIONAL_DIVERGENCES.json: {e}")
        return False
    
    divergences = div_data.get("divergences", [])
    if len(divergences) < 4:
        print(f"[FAIL] Expected at least 4 documented divergences, found {len(divergences)}")
        return False
    
    div_map = {d.get("divergence_id"): d for d in divergences}
    required_divs = ["DIVERGENCE-AI-EXEC", "DIVERGENCE-ADB-BRIDGE", "DIVERGENCE-FILE-INSTALLER", "DIVERGENCE-CAMERA-HARDWARE"]
    for rd in required_divs:
        if rd not in div_map:
            print(f"[FAIL] Missing required divergence: {rd}")
            return False
    
    cam_div = div_map["DIVERGENCE-CAMERA-HARDWARE"]
    if "127.0.0.1:9001" not in cam_div.get("original_behavior", "") or "127.0.0.1:9001" not in cam_div.get("cleanroom_behavior", ""):
        print("[FAIL] DIVERGENCE-CAMERA-HARDWARE must specify canonical endpoint 127.0.0.1:9001")
        return False
    if "8089" in cam_div.get("original_behavior", "") or "8089" in cam_div.get("cleanroom_behavior", ""):
        print("[FAIL] DIVERGENCE-CAMERA-HARDWARE contains non-canonical port 8089!")
        return False
    
    print(f"[PASS] Intentional Divergences verified ({len(divergences)} documented boundaries, camera endpoint 127.0.0.1:9001 confirmed)")
    return True

def main():
    parser = argparse.ArgumentParser(description="Phase 3AR Master Release Verifier")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow dirty working tree (diagnostic only; forbidden for release/clean-clone)")
    args = parser.parse_args()

    print("=" * 70)
    print("PHASE 3AR MASTER RELEASE VERIFICATION SUITE")
    print("Execution Mode: " + ("DIAGNOSTIC (allow-dirty)" if args.allow_dirty else "STRICT CLEAN-ROOM"))
    print("=" * 70)

    # Gate 1: Phase 2 Master Verifier
    phase2_cmd = [sys.executable, "tools/verify_phase2.py"]
    if args.allow_dirty:
        phase2_cmd.append("--allow-dirty")
    if not run_step(1, "Phase 2 Master Verifier", phase2_cmd):
        return 1

    # Gate 1 Sub-checks: Mapped Test Matrix & Conclusive Test Attribution
    mat_p = REPO_ROOT / "evidence" / "go_agent" / "webrtc" / "WEBRTC_CORE_TEST_MATRIX.json"
    mat_ok, mat_issues = validate_mapped_test_matrix(mat_p)
    if not mat_ok:
        print(f"[FAIL] Gate 1 Sub-check (Mapped Test Matrix) failed: {mat_issues}")
        return 1
    attr_ok, attr_issues = validate_test_attribution(mat_p)
    if not attr_ok:
        print(f"[FAIL] Gate 1 Sub-check (Test Attribution) failed: {attr_issues}")
        return 1
    print("[PASS] Gate 1 Sub-check: Mapped Test Matrix & Conclusive Attribution verified.")

    # Gate 2: Final Reconstructed Source Provenance Audit
    if not run_step(2, "Reconstructed Source Provenance Audit", [sys.executable, "tools/audit/audit_reconstructed_source_provenance.py", "--check"]):
        return 1

    # Gate 3: Clean-Room Contamination Audit
    if not run_step(3, "Clean-Room Contamination & History Audit", [sys.executable, "tools/audit/audit_cleanroom_contamination.py", "--check"]):
        return 1

    # Gate 4: Original Artifact Inventory Completeness & Purge Verification
    if not run_step(4, "Original Artifact Inventory & Purge Verification", [sys.executable, "tools/audit/audit_original_artifacts.py", "--check"]):
        return 1

    # Gate 5: Frozen Contract Registry Historical Pinning & Dual Hash
    if not run_step(5, "Frozen Contract Historical Pinning & Dual Hash Audit", [sys.executable, "tools/audit/audit_frozen_contracts.py", "--check"]):
        return 1

    # Gate 6: Toolchain Manifest & Policy Audit
    if not run_step(6, "Toolchain Manifest & Policy Audit", [sys.executable, "tools/audit/audit_toolchain.py", "--check"]):
        return 1

    # Gate 6 Sub-check: Clean Clone Dependencies & Repository Tracking
    deps_ok, untracked = verify_clean_clone_dependencies(repo_root=REPO_ROOT, required_files=CANONICAL_RELEASE_FILES)
    if not deps_ok:
        print(f"[FAIL] Gate 6 Sub-check (Clean-Clone Dependencies) failed: {untracked}")
        return 1
    print("[PASS] Gate 6 Sub-check: All canonical release assets tracked in Git with zero local dependencies.")

    # Gate 7: Cross-Phase Fact Matrix Semantic Invariant
    if not run_step(7, "Cross-Phase Fact Matrix Semantic Invariant", [sys.executable, "tools/audit/validate_phase3_cross_phase_matrix.py", "--check"]):
        return 1

    # Gate 8: Android Helper Method Count DEX Invariant
    if not run_step(8, "Android Helper Method Count DEX Invariant", [sys.executable, "tools/audit/audit_method_count.py", "--check"]):
        return 1

    # Gate 9: Intentional Divergences Registry Verification
    print("\n>> [GATE 9/11] RUNNING: Intentional Divergences Registry Verification...")
    if not verify_intentional_divergences():
        print("[FAIL] Gate 9 (Intentional Divergences Registry Verification) failed")
        return 1
    print("[PASS] Gate 9 (Intentional Divergences Registry Verification)")

    # Gate 10: Fail-Closed Negative Mutation Suite
    if not run_step(10, "Fail-Closed Negative Mutation Suite (18 Mutations)", [sys.executable, "tools/test_release_negative.py"]):
        return 1

    # Gate 11: Final Working Tree Cleanliness
    print("\n>> [GATE 11/11] RUNNING: Final Working Tree Cleanliness Check...")
    if not args.allow_dirty:
        if not verify_clean_working_tree(repo_root=REPO_ROOT):
            print("[FAIL] Gate 11 (Final Working Tree Cleanliness Check) failed")
            return 1
    else:
        print("[WARN] Working tree cleanliness check bypassed via --allow-dirty")
    print("[PASS] Gate 11 (Final Working Tree Cleanliness Check)")

    print("\n" + "=" * 70)
    print("PHASE 3AR RELEASE VERIFICATION VERDICT: ALL 11 INTERNAL GATES PASSED")
    print("External Requirement: Independent Clean-Clone Gate (Gate 12) must be verified separately.")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
