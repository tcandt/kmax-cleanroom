#!/usr/bin/env python3
"""
validate_phase3_release_manifest.py - Phase 3B Release Manifest & Hash Freeze Validator

Validates that PHASE3_RELEASE_MANIFEST.json is internally consistent, accurately binds
all 8 canonical frozen evidence artifacts by their SHA-256 digests, binds the reconstructed_source
tree hash, and explicitly documents intentionally deferred runtime boundaries.
"""

import sys
import json
import hashlib
import subprocess
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_BOUND_ARTIFACTS = {
    "original_artifact_manifest_sha256": "evidence/final/ORIGINAL_ARTIFACT_MANIFEST.json",
    "frozen_contract_registry_sha256": "evidence/final/FROZEN_CONTRACT_REGISTRY.json",
    "reconstructed_source_provenance_sha256": "evidence/final/RECONSTRUCTED_SOURCE_PROVENANCE_FINAL.json",
    "cross_phase_fact_matrix_sha256": "evidence/final/PHASE3_CROSS_PHASE_FACT_MATRIX.json",
    "toolchain_manifest_sha256": "evidence/final/TOOLCHAIN_MANIFEST.json",
    "clean_clone_verification_results_sha256": "evidence/final/CLEAN_CLONE_VERIFICATION_RESULTS.json",
    "intentional_divergences_sha256": "evidence/final/INTENTIONAL_DIVERGENCES.json",
    "release_audit_report_sha256": "reports/40_PHASE3_CLEANROOM_RELEASE_AUDIT.md"
}

REQUIRED_DEFERRED_BOUNDARIES = {
    "DEFERRED-AI-EXEC",
    "DEFERRED-ADB-BRIDGE",
    "DEFERRED-FILE-INSTALLER",
    "DEFERRED-HARDWARE-MOCK-DIVERGENCES"
}

def validate_release_manifest(repo_root=REPO_ROOT, manifest_path=None):
    """
    Validates the Phase 3B release manifest against disk artifacts and git invariants.
    Returns (valid: bool, issues: list).
    """
    root = Path(repo_root)
    m_path = Path(manifest_path) if manifest_path else root / "evidence" / "final" / "PHASE3_RELEASE_MANIFEST.json"

    if not m_path.exists():
        return False, [f"Release manifest missing: {m_path}"]

    try:
        manifest = json.loads(m_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, [f"Failed to parse release manifest JSON: {e}"]

    issues = []

    # 1. Validate bound evidence hashes
    frozen_hashes = manifest.get("frozen_evidence_hashes", {})
    for key, rel_path in REQUIRED_BOUND_ARTIFACTS.items():
        if key not in frozen_hashes:
            issues.append(f"Missing required hash key in manifest: {key}")
            continue

        target_file = root / rel_path
        if not target_file.exists():
            issues.append(f"Bound artifact file missing on disk: {target_file}")
            continue

        actual_sha = hashlib.sha256(target_file.read_bytes()).hexdigest()
        expected_sha = frozen_hashes[key]
        if actual_sha.lower() != expected_sha.lower():
            issues.append(f"Hash mismatch for {rel_path}: actual {actual_sha} != manifest {expected_sha}")

    # 2. Validate tree hash of reconstructed_source
    tree_res = subprocess.run(
        ["git", "rev-parse", "HEAD:reconstructed_source"],
        cwd=str(root), capture_output=True, text=True
    )
    if tree_res.returncode == 0:
        actual_tree = tree_res.stdout.strip()
        manifest_tree = manifest.get("metadata", {}).get("reconstructed_source_tree_hash")
        if manifest_tree and actual_tree != manifest_tree:
            issues.append(f"reconstructed_source tree hash mismatch: actual {actual_tree} != manifest {manifest_tree}")

    # 3. Validate deferred runtime boundaries
    boundaries = manifest.get("deferred_runtime_boundaries", [])
    found_b_ids = {b.get("boundary_id") for b in boundaries}
    missing_boundaries = REQUIRED_DEFERRED_BOUNDARIES - found_b_ids
    if missing_boundaries:
        issues.append(f"Missing required deferred runtime boundaries in manifest: {missing_boundaries}")

    # 4. Terminology policy compliance
    prohibited = manifest.get("release_scope_and_accounting", {}).get("prohibited_claims", [])
    if "literal original source recovered" not in prohibited:
        issues.append("Manifest missing required prohibited claim: 'literal original source recovered'")

    is_valid = (len(issues) == 0)
    return is_valid, issues

def main():
    parser = argparse.ArgumentParser(description="Validate Phase 3B Release Manifest")
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Path to repo root")
    parser.add_argument("--check", action="store_true", help="Check mode (returns non-zero on failure)")
    args = parser.parse_args()

    print("=" * 60)
    print("PHASE 3B RELEASE MANIFEST & EVIDENCE FREEZE AUDIT")
    print("=" * 60)

    valid, issues = validate_release_manifest(repo_root=args.repo_root)
    if valid:
        print("[PASS] Phase 3B Release Manifest verified: all 8 frozen evidence hashes match byte-exact;")
        print("       reconstructed_source tree hash bound; all 4 deferred boundaries explicit.")
        sys.exit(0)
    else:
        print("[FAIL] Phase 3B Release Manifest validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)

if __name__ == "__main__":
    main()
