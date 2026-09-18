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

def verify_clean_working_tree():
    res = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True, text=True)
    status_output = res.stdout.strip()
    if status_output:
        print(f"[FAIL] Working tree is dirty! git status --porcelain:\n{status_output}")
        return False
    print("[PASS] Working tree is strictly clean.")
    return True

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
        if not verify_clean_working_tree():
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
