#!/usr/bin/env python3
"""
tools/audit/audit_original_artifacts.py

Canonical Auditor for Original Distributed Binary Artifacts.
Reconciles all 155 entries recorded in Phase 0 (evidence/ARTIFACT_MANIFEST.json):
- 65 REQUIRED_ORIGINAL_ARTIFACT: Authentic original binaries (all materialized & hash-verified).
- 90 PURGED_FORBIDDEN_EXTERNAL_SOURCE: ScrcpyOverWebRTC submodule files explicitly purged
  during clean-room boundary remediation at commit ef14fab.
- 0 unclassified.
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

VALID_CATEGORIES = {
    "REQUIRED_ORIGINAL_ARTIFACT",
    "PURGED_FORBIDDEN_EXTERNAL_SOURCE",
    "OPTIONAL_DIAGNOSTIC",
    "GENERATED_FORENSIC_OUTPUT"
}

def audit_original_artifacts(manifest_path=None, repo_root=REPO_ROOT, check_mode=False):
    print("=" * 60)
    print("ORIGINAL ARTIFACT INVENTORY & PURGE RECONCILIATION AUDIT")
    print("=" * 60)

    if manifest_path is None:
        phase0_manifest_path = repo_root / "evidence" / "ARTIFACT_MANIFEST.json"
    else:
        phase0_manifest_path = Path(manifest_path)

    if not phase0_manifest_path.exists():
        print(f"[FAIL] Phase 0 manifest missing: {phase0_manifest_path}")
        return False

    phase0_data = json.loads(phase0_manifest_path.read_text(encoding="utf-8"))
    raw_artifacts = phase0_data.get("artifacts", [])
    total_phase0 = len(raw_artifacts)

    reconciled_artifacts = []
    required_count = 0
    purged_count = 0
    missing_required = []
    hash_mismatches = []

    for a in raw_artifacts:
        rel_path = a.get("relative_path", "")
        recorded_sha256 = a.get("sha256", "")
        full_path = repo_root / rel_path

        if rel_path.startswith("ScrcpyOverWebRTC/") or rel_path.startswith("ScrcpyOverWebRTC\\"):
            purged_count += 1
            reconciled_artifacts.append({
                "relative_path": rel_path,
                "classification": "PURGED_FORBIDDEN_EXTERNAL_SOURCE",
                "recorded_sha256": recorded_sha256,
                "remediation_reference": "commit ef14fab (reports/00A_CLEANROOM_BOUNDARY_REMEDIATION.md)",
                "materialized_in_cleanroom_tree": full_path.exists()
            })
            if full_path.exists():
                print(f"[FAIL] Purged artifact exists in clean-room tree! Contamination: {rel_path}")
                return False
        else:
            required_count += 1
            if not full_path.exists():
                missing_required.append(rel_path)
                continue

            data = full_path.read_bytes()
            actual_sha256 = hashlib.sha256(data).hexdigest()
            matches = (actual_sha256.lower() == recorded_sha256.lower())

            if not matches:
                hash_mismatches.append({
                    "path": rel_path,
                    "expected": recorded_sha256,
                    "actual": actual_sha256
                })

            reconciled_artifacts.append({
                "relative_path": rel_path,
                "classification": "REQUIRED_ORIGINAL_ARTIFACT",
                "recorded_sha256": recorded_sha256,
                "actual_sha256": actual_sha256,
                "size_bytes": len(data),
                "hash_verified": matches,
                "architecture": a.get("arch"),
                "category": a.get("category"),
                "role_description": a.get("role_description"),
                "immutable": True
            })

    print(f"Total Phase 0 Artifacts Classified: {len(reconciled_artifacts)} / {total_phase0}")
    print(f"  - REQUIRED_ORIGINAL_ARTIFACT:     {required_count}")
    print(f"  - PURGED_FORBIDDEN_EXTERNAL_SOURCE: {purged_count}")
    print(f"  - Missing Required Artifacts:     {len(missing_required)}")
    print(f"  - SHA-256 Mismatches:             {len(hash_mismatches)}")

    if total_phase0 != 155:
        print(f"[FAIL] Expected exactly 155 Phase 0 artifacts, got {total_phase0}")
        return False
    if len(reconciled_artifacts) != 155:
        print(f"[FAIL] Not all 155 artifacts were classified!")
        return False
    if required_count != 65:
        print(f"[FAIL] Expected 65 required original artifacts, got {required_count}")
        return False
    if purged_count != 90:
        print(f"[FAIL] Expected 90 purged external artifacts, got {purged_count}")
        return False
    if missing_required:
        print(f"[FAIL] Missing {len(missing_required)} required original artifacts:")
        for m in missing_required[:10]:
            print(f"  - {m}")
        return False
    if hash_mismatches:
        print(f"[FAIL] Found {len(hash_mismatches)} hash mismatches in required original artifacts:")
        for hm in hash_mismatches:
            print(f"  - {hm['path']}: expected {hm['expected']}, got {hm['actual']}")
        return False

    out_file = repo_root / "evidence" / "final" / "ORIGINAL_ARTIFACT_MANIFEST.json"
    manifest_data = {
        "metadata": {
            "title": "Final Original Artifact Inventory and Immutability Manifest",
            "phase": "Phase 3AR",
            "total_phase0_cataloged": total_phase0,
            "total_classified": len(reconciled_artifacts),
            "required_original_artifacts_count": required_count,
            "purged_external_artifacts_count": purged_count,
            "all_required_hashes_verified": True,
            "immutable_lock": True,
            "remediation_reference": "commit ef14fab (reports/00A_CLEANROOM_BOUNDARY_REMEDIATION.md)"
        },
        "classification_summary": {
            "REQUIRED_ORIGINAL_ARTIFACT": required_count,
            "PURGED_FORBIDDEN_EXTERNAL_SOURCE": purged_count,
            "OPTIONAL_DIAGNOSTIC": 0,
            "GENERATED_FORENSIC_OUTPUT": 0,
            "UNCLASSIFIED": 0
        },
        "artifacts": reconciled_artifacts
    }

    if check_mode:
        if not out_file.exists():
            print(f"[FAIL] Check mode failed: {out_file} missing")
            return False
        existing = json.loads(out_file.read_text(encoding="utf-8"))
        if existing.get("metadata", {}).get("required_original_artifacts_count") != required_count or \
           existing.get("metadata", {}).get("purged_external_artifacts_count") != purged_count:
            print(f"[FAIL] Check mode failed: count mismatch in {out_file}")
            return False
        print(f"[PASS] Original Artifact Manifest verified: 155/155 classified (65 required verified, 90 purged verified)")
        return True

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    print(f"[+] Wrote reconciled artifact inventory to {out_file}")
    print("[PASS] All 65 Required Original Artifacts Materialized & 100% Hash-Verified.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Audit Original Distributed Artifacts")
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Path to repository root")
    parser.add_argument("--manifest-file", default=None, help="Explicit Phase 0 manifest path")
    parser.add_argument("--check", action="store_true", help="Verification mode")
    args = parser.parse_args()

    success = audit_original_artifacts(
        manifest_path=args.manifest_file,
        repo_root=Path(args.repo_root),
        check_mode=args.check
    )
    if not success:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
