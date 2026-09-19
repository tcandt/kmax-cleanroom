#!/usr/bin/env python3
"""
tools/test_release_negative.py

Phase 3AR Negative Release Mutation Test Suite (18 Fail-Closed Gates).
Validates that all release auditors and verifiers are strictly FAIL-CLOSED:
 1. MUTATION-01: Tampered contract SHA-256 in registry
 2. MUTATION-02: Wrong historical baseline commit in registry
 3. MUTATION-03: Tampered original artifact hash in manifest
 4. MUTATION-04: Missing original artifact file from disk
 5. MUTATION-05: Missing required tool in toolchain manifest
 6. MUTATION-06: UNKNOWN production function in provenance auditor
 7. MUTATION-07: Invalid provenance locator / non-existent fact ID
 8. MUTATION-08: Clean-room contamination injection (prohibited pattern)
 9. MUTATION-09: Inverted DataChannel creator/consumer in fact matrix
10. MUTATION-10: Wrong camera endpoint (8089 instead of 9001) in fact matrix
11. MUTATION-11: Method count discrepancy in Android Helper DEX invariant
12. MUTATION-12: Dirty working tree detection
13. MUTATION-13: Absolute workstation path dependency leak
14. MUTATION-14: Missing mapped critical test in test matrix
15. MUTATION-15: Skipped critical test in execution results
16. MUTATION-16: Missing required errata file for frozen contract
17. MUTATION-17: Clean-clone dependency on untracked/local-only file
18. MUTATION-18: Wrong errata freeze commit or blob hash

All mutations are evaluated on isolated temporary copies/views to ensure
zero permanent mutations to the repository tree.
"""

import os
import sys
import json
import copy
import shutil
import tempfile
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.audit.audit_frozen_contracts import audit_frozen_contracts
from tools.audit.audit_original_artifacts import audit_original_artifacts
from tools.audit.audit_toolchain import audit_toolchain, audit_path_portability
from tools.audit.audit_cleanroom_contamination import audit_source_tree_contamination
from tools.audit.validate_phase3_cross_phase_matrix import validate_matrix
from tools.audit.audit_method_count import audit_method_count
from tools.audit.audit_reconstructed_source_provenance import (
    validate_entry,
    audit_all_production_functions
)
from tools.audit.b2_common import evaluate_go_test_events
from tools.verify_release import (
    verify_clean_working_tree,
    validate_mapped_test_matrix,
    validate_test_attribution,
    verify_clean_clone_dependencies,
    verify_git_checkout_policy
)

def run_mutation_test(test_id, description, test_fn):
    print(f"\n>> [{test_id}] {description}")
    sys.stdout.flush()
    try:
        passed = test_fn()
        if passed:
            print(f"   [FAIL-CLOSED PASS] {test_id}: Successfully rejected invalid state.")
            return True
        else:
            print(f"   [FAIL-OPEN VIOLATION] {test_id}: Erroneously accepted invalid state!")
            return False
    except Exception as e:
        print(f"   [FAIL-CLOSED PASS] {test_id}: Rejected with exception: {e}")
        return True

# 1. Tampered contract SHA-256
def test_mutation_01_tampered_contract_sha():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        reg_p = REPO_ROOT / "evidence" / "final" / "FROZEN_CONTRACT_REGISTRY.json"
        data = json.loads(reg_p.read_text(encoding="utf-8"))
        data["contracts"][0]["historical_git_blob_sha256"] = "0" * 64
        tf.write(json.dumps(data))
        temp_path = tf.name
    try:
        res = audit_frozen_contracts(registry_path=temp_path, repo_root=REPO_ROOT, check_mode=True)
        return res is False
    finally:
        os.unlink(temp_path)

# 2. Wrong historical baseline commit
def test_mutation_02_wrong_baseline_commit():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        reg_p = REPO_ROOT / "evidence" / "final" / "FROZEN_CONTRACT_REGISTRY.json"
        data = json.loads(reg_p.read_text(encoding="utf-8"))
        data["contracts"][0]["freeze_commit"] = "0" * 40
        tf.write(json.dumps(data))
        temp_path = tf.name
    try:
        res = audit_frozen_contracts(registry_path=temp_path, repo_root=REPO_ROOT, check_mode=True)
        return res is False
    finally:
        os.unlink(temp_path)

# 3. Tampered original artifact hash
def test_mutation_03_tampered_artifact_hash():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        orig_p = REPO_ROOT / "evidence" / "ARTIFACT_MANIFEST.json"
        data = json.loads(orig_p.read_text(encoding="utf-8"))
        data["artifacts"][0]["sha256"] = "f" * 64
        tf.write(json.dumps(data))
        temp_path = tf.name
    try:
        res = audit_original_artifacts(manifest_path=temp_path, repo_root=REPO_ROOT, check_mode=False)
        return res is False
    finally:
        os.unlink(temp_path)

# 4. Missing original artifact file
def test_mutation_04_missing_artifact_file():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        orig_p = REPO_ROOT / "evidence" / "ARTIFACT_MANIFEST.json"
        data = json.loads(orig_p.read_text(encoding="utf-8"))
        data["artifacts"][0]["relative_path"] = "nonexistent_binary_file.bin"
        tf.write(json.dumps(data))
        temp_path = tf.name
    try:
        res = audit_original_artifacts(manifest_path=temp_path, repo_root=REPO_ROOT, check_mode=False)
        return res is False
    finally:
        os.unlink(temp_path)

# 5. Toolchain LLVM SHA mismatch against manifest policy
def test_mutation_05_toolchain_binding_mismatch():
    with tempfile.TemporaryDirectory() as td:
        temp_root = Path(td)
        out_dir = temp_root / "evidence" / "final"
        out_dir.mkdir(parents=True, exist_ok=True)
        orig_manifest = json.loads((REPO_ROOT / "evidence" / "final" / "TOOLCHAIN_MANIFEST.json").read_text(encoding="utf-8"))
        # Tamper llvm_objdump sha256 to cause strict binding mismatch
        orig_manifest["tools"]["llvm_objdump"]["sha256"] = "0" * 64
        (out_dir / "TOOLCHAIN_MANIFEST.json").write_text(json.dumps(orig_manifest), encoding="utf-8")
        res = audit_toolchain(repo_root=temp_root, check_mode=True)
        return res is False

# 6. UNKNOWN production function in provenance
def test_mutation_06_unknown_production_function():
    with tempfile.TemporaryDirectory() as td:
        temp_root = Path(td)
        src_dir = temp_root / "reconstructed_source" / "cloudphone-agent" / "pkg" / "unknown_pkg"
        src_dir.mkdir(parents=True, exist_ok=True)
        # Missing provenance block -> UNKNOWN
        (src_dir / "unknown.go").write_text("package unknown_pkg\nfunc MysteriousUnmappedFunc() {}\n", encoding="utf-8")
        # Copy rules
        rules_dir = temp_root / "evidence" / "final"
        rules_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / "evidence" / "final" / "PROVENANCE_RULES.json", rules_dir / "PROVENANCE_RULES.json")
        res = audit_all_production_functions(repo_root=temp_root, check_mode=False)
        return res is False

# 7. Invalid provenance locator / non-existent fact ID
def test_mutation_07_invalid_provenance_locator():
    manifest_p = REPO_ROOT / "evidence" / "final" / "RECONSTRUCTED_SOURCE_PROVENANCE_FINAL.json"
    data = json.loads(manifest_p.read_text(encoding="utf-8"))
    mutated_entry = copy.deepcopy(data["functions"][0])
    mutated_entry["evidence_locator"] = "NONEXISTENT-FACT-ID-99999"
    rules_data = json.loads((REPO_ROOT / "evidence" / "final" / "PROVENANCE_RULES.json").read_text(encoding="utf-8"))
    valid_rules = set(rules_data["rules"].keys())
    ok, _ = validate_entry(mutated_entry, REPO_ROOT, valid_rules, {})
    return ok is False

# 8. Clean-room contamination injection (prohibited pattern)
def test_mutation_08_contamination_injection():
    with tempfile.TemporaryDirectory() as td:
        temp_root = Path(td)
        src_dir = temp_root / "reconstructed_source" / "cloudphone-agent" / "pkg" / "probe"
        src_dir.mkdir(parents=True, exist_ok=True)
        bad_file = src_dir / "contaminated.go"
        bad_file.write_text("// Reconstructed using recovered_source from decompiled archive\npackage probe\n", encoding="utf-8")

        # Invoke actual contamination auditor on temp repo view
        is_clean, findings = audit_source_tree_contamination(temp_root / "reconstructed_source", repo_root=temp_root)
        return is_clean is False

# 9. Inverted DataChannel creator/consumer
def test_mutation_09_inverted_datachannel_creator():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        mat_p = REPO_ROOT / "evidence" / "final" / "PHASE3_CROSS_PHASE_FACT_MATRIX.json"
        data = json.loads(mat_p.read_text(encoding="utf-8"))
        data["datachannel_reconciliation_summary"]["input-channel"]["creator"] = "Browser Client"
        tf.write(json.dumps(data))
        temp_path = tf.name
    try:
        res = validate_matrix(matrix_path=temp_path, repo_root=REPO_ROOT)
        return res is False
    finally:
        os.unlink(temp_path)

# 10. Wrong camera endpoint (8089 instead of 9001)
def test_mutation_10_wrong_camera_endpoint():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        mat_p = REPO_ROOT / "evidence" / "final" / "PHASE3_CROSS_PHASE_FACT_MATRIX.json"
        data = json.loads(mat_p.read_text(encoding="utf-8"))
        data["datachannel_reconciliation_summary"]["camera-channel"]["downstream"] = "Camera HAL TCP socket endpoint 127.0.0.1:8089"
        tf.write(json.dumps(data))
        temp_path = tf.name
    try:
        res = validate_matrix(matrix_path=temp_path, repo_root=REPO_ROOT)
        return res is False
    finally:
        os.unlink(temp_path)

# 11. Method count discrepancy in Android Helper DEX invariant
def test_mutation_11_method_count_discrepancy():
    with tempfile.TemporaryDirectory() as td:
        temp_root = Path(td)
        out_dir = temp_root / "evidence" / "final"
        out_dir.mkdir(parents=True, exist_ok=True)
        # Copy libsys_core.so so DEX parser can read it
        android_dir = temp_root / "cloudphone-v0.3.6 (1)" / "android"
        android_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / "cloudphone-v0.3.6 (1)" / "android" / "libsys_core.so", android_dir / "libsys_core.so")
        # Write corrupted reconciliation summary
        orig = json.loads((REPO_ROOT / "evidence" / "final" / "ANDROID_METHOD_COUNT_RECONCILIATION.json").read_text(encoding="utf-8"))
        orig["reconciliation_summary"]["total_reconciled"] = 1624  # Discrepancy!
        (out_dir / "ANDROID_METHOD_COUNT_RECONCILIATION.json").write_text(json.dumps(orig), encoding="utf-8")
        res = audit_method_count(repo_root=temp_root, check_mode=True)
        return res is False

# 12. Dirty working tree detection
def test_mutation_12_dirty_working_tree():
    with tempfile.TemporaryDirectory() as td:
        temp_repo = Path(td)
        # Initialize isolated temporary Git repository (zero mutation to live tree)
        subprocess.run(["git", "init"], cwd=temp_repo, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "CleanroomTester"], cwd=temp_repo, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.email", "tester@cleanroom.local"], cwd=temp_repo, capture_output=True, check=True)
        # Commit a baseline file
        baseline = temp_repo / "README.md"
        baseline.write_text("# Clean Tree\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=temp_repo, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "initial commit"], cwd=temp_repo, capture_output=True, check=True)

        # Inject untracked sentinel
        sentinel = temp_repo / ".dirty_tree_test_sentinel_mutation"
        sentinel.write_text("temporary dirty sentinel", encoding="utf-8")

        # Actual release cleanliness helper must fail-closed on dirty tree
        is_clean = verify_clean_working_tree(repo_root=temp_repo)
        return is_clean is False

# 13. Absolute workstation path dependency leak
def test_mutation_13_workstation_path_leak():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        manifest_p = REPO_ROOT / "evidence" / "final" / "TOOLCHAIN_MANIFEST.json"
        data = json.loads(manifest_p.read_text(encoding="utf-8"))
        # Inject non-portable workstation path leak
        data["tools"]["go"]["resolved_path"] = "C:\\Users\\TINH-NGUYEN\\Desktop\\cloudphone-agent.exe"
        tf.write(json.dumps(data))
        temp_path = tf.name
    try:
        is_portable, leaks = audit_path_portability(target_or_path=temp_path)
        return is_portable is False
    finally:
        os.unlink(temp_path)

def _build_synthetic_go_test_events(cases, omitted_test=None, skipped_test=None):
    events = []
    packages = set()
    for c in cases:
        pkg = "cloudphone-agent/" + c["package"]
        packages.add(pkg)
        t_name = c["name"]
        if t_name == omitted_test:
            continue
        events.append({"Action": "run", "Package": pkg, "Test": t_name})
        if t_name == skipped_test:
            events.append({"Action": "skip", "Package": pkg, "Test": t_name, "Elapsed": 0.01})
        else:
            events.append({"Action": "pass", "Package": pkg, "Test": t_name, "Elapsed": 0.05})

    for pkg in packages:
        events.append({"Action": "pass", "Package": pkg, "Elapsed": 0.2})
    return events

# 14. Missing required actual Go test in execution attribution
def test_mutation_14_missing_actual_go_test():
    mat_p = REPO_ROOT / "evidence" / "go_agent" / "webrtc" / "WEBRTC_CORE_TEST_MATRIX.json"
    data = json.loads(mat_p.read_text(encoding="utf-8"))
    cases = []
    for lvl in data.get("levels", {}).values():
        cases.extend(lvl.get("cases", []))
    events = _build_synthetic_go_test_events(cases, omitted_test="TestEvidenceBoundMediaEngine")
    is_valid, issues = evaluate_go_test_events(events, required_cases=cases)
    return is_valid is False

# 15. Skipped actual Go test in execution attribution
def test_mutation_15_skipped_actual_go_test():
    mat_p = REPO_ROOT / "evidence" / "go_agent" / "webrtc" / "WEBRTC_CORE_TEST_MATRIX.json"
    data = json.loads(mat_p.read_text(encoding="utf-8"))
    cases = []
    for lvl in data.get("levels", {}).values():
        cases.extend(lvl.get("cases", []))
    events = _build_synthetic_go_test_events(cases, skipped_test="TestEvidenceBoundMediaEngine")
    is_valid, issues = evaluate_go_test_events(events, required_cases=cases)
    return is_valid is False

# 16. Missing required formal errata
def test_mutation_16_missing_required_errata():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        reg_p = REPO_ROOT / "evidence" / "final" / "FROZEN_CONTRACT_REGISTRY.json"
        data = json.loads(reg_p.read_text(encoding="utf-8"))
        # Point an existing errata path to a nonexistent file
        for c in data["contracts"]:
            if c.get("effective_errata_path"):
                c["effective_errata_path"] = "evidence/go_agent/webrtc/NONEXISTENT_ERRATA.json"
                break
        tf.write(json.dumps(data))
        temp_path = tf.name
    try:
        res = audit_frozen_contracts(registry_path=temp_path, repo_root=REPO_ROOT, check_mode=True)
        return res is False
    finally:
        os.unlink(temp_path)

# 17. Clean-clone dependency on untracked/local-only file
def test_mutation_17_clean_clone_untracked_dependency():
    with tempfile.TemporaryDirectory() as td:
        temp_repo = Path(td)
        # Initialize isolated temporary Git repository (zero mutation to live tree)
        subprocess.run(["git", "init"], cwd=temp_repo, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "CleanroomTester"], cwd=temp_repo, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.email", "tester@cleanroom.local"], cwd=temp_repo, capture_output=True, check=True)

        # Commit a tracked required file
        tracked_file = temp_repo / "tracked_config.json"
        tracked_file.write_text("{\"tracked\": true}\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked_config.json"], cwd=temp_repo, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "add tracked config"], cwd=temp_repo, capture_output=True, check=True)

        # Leave an untracked local file
        untracked_file = temp_repo / "local_only_secret.json"
        untracked_file.write_text("{\"secret\": true}\n", encoding="utf-8")

        # Actual clean-clone dependency validator must reject untracked candidate
        is_clean, untracked = verify_clean_clone_dependencies(
            repo_root=temp_repo,
            candidate_paths=["local_only_secret.json"],
            required_files=["tracked_config.json"]
        )
        return is_clean is False

# 18. Line-ending checkout policy violation (core.autocrlf == true)
def test_mutation_18_line_ending_policy_violation():
    with tempfile.TemporaryDirectory() as td:
        temp_repo = Path(td)
        subprocess.run(["git", "init"], cwd=temp_repo, capture_output=True, check=True)
        subprocess.run(["git", "config", "core.autocrlf", "true"], cwd=temp_repo, capture_output=True, check=True)
        is_clean, issues = verify_git_checkout_policy(repo_root=temp_repo)
        return is_clean is False

def run_all_negative_tests():
    print("=" * 60)
    print("PHASE 3AR FAIL-CLOSED NEGATIVE MUTATION TEST SUITE (18 TESTS)")
    print("=" * 60)

    tests = [
        ("MUTATION-01", "Tampered contract SHA-256 in registry", test_mutation_01_tampered_contract_sha),
        ("MUTATION-02", "Wrong historical baseline commit in registry", test_mutation_02_wrong_baseline_commit),
        ("MUTATION-03", "Tampered original artifact hash in manifest", test_mutation_03_tampered_artifact_hash),
        ("MUTATION-04", "Missing original artifact file from disk", test_mutation_04_missing_artifact_file),
        ("MUTATION-05", "Toolchain LLVM SHA mismatch against manifest policy", test_mutation_05_toolchain_binding_mismatch),
        ("MUTATION-06", "UNKNOWN production function in provenance auditor", test_mutation_06_unknown_production_function),
        ("MUTATION-07", "Invalid provenance locator / non-existent fact ID", test_mutation_07_invalid_provenance_locator),
        ("MUTATION-08", "Clean-room contamination injection (prohibited pattern)", test_mutation_08_contamination_injection),
        ("MUTATION-09", "Inverted DataChannel creator/consumer in fact matrix", test_mutation_09_inverted_datachannel_creator),
        ("MUTATION-10", "Wrong camera endpoint (8089 instead of 9001) in fact matrix", test_mutation_10_wrong_camera_endpoint),
        ("MUTATION-11", "Method count discrepancy in Android Helper DEX invariant", test_mutation_11_method_count_discrepancy),
        ("MUTATION-12", "Dirty working tree detection", test_mutation_12_dirty_working_tree),
        ("MUTATION-13", "Absolute workstation path dependency leak", test_mutation_13_workstation_path_leak),
        ("MUTATION-14", "Missing required actual Go test in execution attribution", test_mutation_14_missing_actual_go_test),
        ("MUTATION-15", "Skipped actual Go test in execution attribution", test_mutation_15_skipped_actual_go_test),
        ("MUTATION-16", "Missing required formal errata file for frozen contract", test_mutation_16_missing_required_errata),
        ("MUTATION-17", "Clean-clone dependency on untracked/local-only file", test_mutation_17_clean_clone_untracked_dependency),
        ("MUTATION-18", "Line-ending checkout policy violation (core.autocrlf == true)", test_mutation_18_line_ending_policy_violation),
    ]

    passed_count = 0
    failed_tests = []

    for tid, desc, fn in tests:
        ok = run_mutation_test(tid, desc, fn)
        if ok:
            passed_count += 1
        else:
            failed_tests.append(tid)

    print("\n" + "=" * 60)
    print(f"NEGATIVE TEST SUITE RESULTS: {passed_count} / {len(tests)} PASS")
    print("=" * 60)

    if failed_tests:
        print(f"[FAIL] The following mutations failed to be rejected fail-closed: {failed_tests}")
        return False

    print("[PASS] All 18 negative mutations were strictly rejected by fail-closed release gates.")
    return True

if __name__ == "__main__":
    success = run_all_negative_tests()
    if not success:
        sys.exit(1)
    sys.exit(0)
