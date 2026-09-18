#!/usr/bin/env python3
"""
tools/audit/audit_frozen_contracts.py

Canonical Auditor for Frozen Contract Historical Pinning & Parity.
Verifies all 15 registered contracts:
1. Validates that freeze_commit exists in git history.
2. Extracts historical blob via `git show <freeze_commit>:<artifact_path>`.
3. Verifies historical blob SHA-256 matches historical_git_blob_sha256.
4. Verifies disk/checkout SHA-256 matches frozen_artifact_sha256.
5. If errata is present, verifies errata_freeze_commit, errata blob SHA, and errata disk SHA.
"""

import os
import sys
import json
import hashlib
import subprocess
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def audit_frozen_contracts(registry_path=None, repo_root=REPO_ROOT, check_mode=False):
    print("=" * 60)
    print("FROZEN CONTRACT HISTORICAL PINNING & PARITY AUDIT")
    print("=" * 60)

    if registry_path is None:
        registry_path = repo_root / "evidence" / "final" / "FROZEN_CONTRACT_REGISTRY.json"
    else:
        registry_path = Path(registry_path)

    if not registry_path.exists():
        print(f"[FAIL] Contract registry missing: {registry_path}")
        return False

    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[FAIL] Invalid JSON in registry: {e}")
        return False

    contracts = data.get("contracts", [])
    if len(contracts) != 15:
        print(f"[FAIL] Expected exactly 15 contracts registered, got {len(contracts)}")
        return False

    verified_contracts = 0
    failures = []

    for c in contracts:
        cid = c.get("contract_id", "")
        art_path = c.get("artifact_path", "")
        freeze_commit = c.get("freeze_commit", "")
        expected_blob_sha = c.get("historical_git_blob_sha256", "")
        expected_disk_sha = c.get("frozen_artifact_sha256", "")

        # 1. Verify freeze_commit exists
        rev_proc = subprocess.run(
            ["git", "rev-parse", "--verify", freeze_commit],
            cwd=repo_root,
            capture_output=True,
            text=True
        )
        if rev_proc.returncode != 0:
            failures.append(f"{cid}: freeze_commit {freeze_commit} does not exist in git history!")
            continue

        # 2. Extract historical blob from git
        show_proc = subprocess.run(
            ["git", "show", f"{freeze_commit}:{art_path}"],
            cwd=repo_root,
            capture_output=True
        )
        if show_proc.returncode != 0:
            failures.append(f"{cid}: git show {freeze_commit[:8]}:{art_path} failed!")
            continue

        actual_blob_sha = hashlib.sha256(show_proc.stdout).hexdigest()
        if actual_blob_sha.lower() != expected_blob_sha.lower():
            failures.append(f"{cid}: historical blob SHA mismatch! Expected {expected_blob_sha}, got {actual_blob_sha}")
            continue

        # 3. Verify disk file SHA
        full_disk_path = repo_root / art_path
        if not full_disk_path.exists():
            failures.append(f"{cid}: artifact missing on disk: {art_path}")
            continue

        actual_disk_sha = hashlib.sha256(full_disk_path.read_bytes()).hexdigest()
        if actual_disk_sha.lower() != expected_disk_sha.lower():
            failures.append(f"{cid}: disk SHA mismatch! Expected {expected_disk_sha}, got {actual_disk_sha}")
            continue

        # 4. Verify errata if applicable
        errata_path = c.get("effective_errata_path")
        if errata_path:
            err_commit = c.get("errata_freeze_commit")
            err_expected_blob_sha = c.get("errata_git_blob_sha256")
            err_expected_disk_sha = c.get("errata_artifact_sha256")

            err_rev = subprocess.run(
                ["git", "rev-parse", "--verify", err_commit],
                cwd=repo_root,
                capture_output=True,
                text=True
            )
            if err_rev.returncode != 0:
                failures.append(f"{cid} (errata): commit {err_commit} does not exist!")
                continue

            err_show = subprocess.run(
                ["git", "show", f"{err_commit}:{errata_path}"],
                cwd=repo_root,
                capture_output=True
            )
            if err_show.returncode != 0:
                failures.append(f"{cid} (errata): git show {err_commit[:8]}:{errata_path} failed!")
                continue

            actual_err_blob_sha = hashlib.sha256(err_show.stdout).hexdigest()
            if actual_err_blob_sha.lower() != err_expected_blob_sha.lower():
                failures.append(f"{cid} (errata): blob SHA mismatch! Expected {err_expected_blob_sha}, got {actual_err_blob_sha}")
                continue

            full_err_path = repo_root / errata_path
            if not full_err_path.exists():
                failures.append(f"{cid} (errata): missing on disk: {errata_path}")
                continue

            actual_err_disk_sha = hashlib.sha256(full_err_path.read_bytes()).hexdigest()
            if actual_err_disk_sha.lower() != err_expected_disk_sha.lower():
                failures.append(f"{cid} (errata): disk SHA mismatch! Expected {err_expected_disk_sha}, got {actual_err_disk_sha}")
                continue

        verified_contracts += 1

    print(f"Total Contracts Audited: {len(contracts)}")
    print(f"Successfully Verified:   {verified_contracts}")
    print(f"Failures:                {len(failures)}")

    if failures:
        print("\n[FAIL] Historical contract pinning failures:")
        for f in failures:
            print(f"  - {f}")
        return False

    print(f"\n[PASS] All 15 Frozen Contracts Verified via Historical Git Blob Pinning & Disk Hash.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Audit Frozen Contracts & Historical Pinning")
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Path to repository root")
    parser.add_argument("--registry-file", default=None, help="Explicit registry file path")
    parser.add_argument("--check", action="store_true", help="Verification mode")
    args = parser.parse_args()

    success = audit_frozen_contracts(
        registry_path=args.registry_file,
        repo_root=Path(args.repo_root),
        check_mode=args.check
    )
    if not success:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
