#!/usr/bin/env python3
"""
reproduce_webrtc_datachannel_forensics.py — Phase 2C.5A WebRTC & DataChannel Forensic Reproducibility Verifier

Verifies that ALL 14 canonical Phase 2C.5A WebRTC / DataChannel / Media forensic artifacts:
  1. WEBRTC_DEPENDENCY_EVIDENCE.json
  2. WEBRTC_PEERCONNECTION_CALLGRAPH.json
  3. WEBRTC_PEERCONNECTION_STATE_MACHINE.json
  4. WEBRTC_CODEC_CAPABILITY_MATRIX.json
  5. MEDIA_TRACK_CONSTRUCTION_EVIDENCE.json
  6. DATACHANNEL_LABEL_EVIDENCE.json
  7. DATACHANNEL_FRAMING_MATRIX.json
  8. DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json
  9. AGENT_HELPER_IPC_SOCKET_MATRIX.json
  10. CONTROL_INPUT_PROTOCOL_CROSSMAP.json
  11. MEDIA_PLANE_PIPELINE_EVIDENCE.json
  12. WEBRTC_AGENT_CROSS_BUILD_CORRELATION.json
  13. WEBRTC_TOPOLOGY_CROSSMAP.json
  14. PHASE2C5A_FORENSIC_GATE_RESULT.json

are 100% reproducible directly from canonical binary disassembly and artifact extraction,
with ZERO copying of canonical evidence.

Deep Semantic Validation:
- Generates into an isolated temporary directory.
- Performs deep, key-by-key, value-by-value comparison of all regenerated artifacts against canonical.
- Validates that WEBRTC_DATACHANNEL_REPRODUCIBILITY_MANIFEST.json excludes itself from its denominator.
- Validates that all 19 gate dimensions in PHASE2C5A_FORENSIC_GATE_RESULT.json pass.
- Validates strict production boundary (zero production WebRTC/DataChannel/Media source created).
- Leaves git status clean and unchanged.
"""

import os
import sys
import json
import shutil
import tempfile
import hashlib
from pathlib import Path
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.generate_webrtc_datachannel_forensics import generate_all_forensics

CANONICAL_DIR = REPO_ROOT / "evidence" / "go_agent" / "webrtc"
MANIFEST_PATH = CANONICAL_DIR / "WEBRTC_DATACHANNEL_REPRODUCIBILITY_MANIFEST.json"

EXPECTED_14_ARTIFACTS = [
    "WEBRTC_DEPENDENCY_EVIDENCE.json",
    "WEBRTC_PEERCONNECTION_CALLGRAPH.json",
    "WEBRTC_PEERCONNECTION_STATE_MACHINE.json",
    "WEBRTC_CODEC_CAPABILITY_MATRIX.json",
    "MEDIA_TRACK_CONSTRUCTION_EVIDENCE.json",
    "DATACHANNEL_LABEL_EVIDENCE.json",
    "DATACHANNEL_FRAMING_MATRIX.json",
    "DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json",
    "AGENT_HELPER_IPC_SOCKET_MATRIX.json",
    "CONTROL_INPUT_PROTOCOL_CROSSMAP.json",
    "MEDIA_PLANE_PIPELINE_EVIDENCE.json",
    "WEBRTC_AGENT_CROSS_BUILD_CORRELATION.json",
    "WEBRTC_TOPOLOGY_CROSSMAP.json",
    "PHASE2C5A_FORENSIC_GATE_RESULT.json"
]


def deep_compare_dicts(path: str, actual: Any, expected: Any) -> List[str]:
    diffs = []
    if type(actual) != type(expected):
        diffs.append(f"{path}: type mismatch: {type(actual).__name__} vs {type(expected).__name__}")
        return diffs

    if isinstance(actual, dict):
        all_keys = sorted(set(actual.keys()) | set(expected.keys()))
        for k in all_keys:
            sub_path = f"{path}.{k}" if path else k
            if k not in actual:
                diffs.append(f"{sub_path}: missing in regenerated output")
            elif k not in expected:
                diffs.append(f"{sub_path}: extra in regenerated output")
            else:
                diffs.extend(deep_compare_dicts(sub_path, actual[k], expected[k]))
    elif isinstance(actual, list):
        if len(actual) != len(expected):
            diffs.append(f"{path}: list length mismatch: {len(actual)} vs {len(expected)}")
        else:
            for i, (a_item, e_item) in enumerate(zip(actual, expected)):
                diffs.extend(deep_compare_dicts(f"{path}[{i}]", a_item, e_item))
    else:
        if actual != expected:
            diffs.append(f"{path}: value mismatch: {repr(actual)} != {repr(expected)}")

    return diffs


def verify_strict_production_boundary() -> List[str]:
    violations = []
    prod_root = REPO_ROOT / "reconstructed_source" / "webrtc-signaling"
    for forbidden_pkg in ["webrtc", "datachannel", "media"]:
        pkg_path = prod_root / "pkg" / forbidden_pkg
        if pkg_path.exists():
            violations.append(f"Forbidden production package exists: {pkg_path}")

    go_mod_path = prod_root / "go.mod"
    if go_mod_path.exists():
        go_mod_text = go_mod_path.read_text(encoding="utf-8")
        if "github.com/pion/webrtc" in go_mod_text:
            violations.append("Forbidden Pion WebRTC dependency found in production go.mod")

    return violations


def run_reproducibility_verification() -> Dict[str, Any]:
    print("=" * 70)
    print("PHASE 2C.5A WEBRTC & DATACHANNEL FORENSIC REPRODUCIBILITY VERIFIER")
    print("=" * 70)

    # 1. Check Canonical Directory & Manifest Existence
    if not CANONICAL_DIR.exists():
        print(f"[-] ERROR: Canonical directory not found: {CANONICAL_DIR}")
        return {"verdict": "FAIL", "reason": "CANONICAL_DIR_NOT_FOUND"}

    if not MANIFEST_PATH.exists():
        print(f"[-] ERROR: Manifest not found: {MANIFEST_PATH}")
        return {"verdict": "FAIL", "reason": "MANIFEST_NOT_FOUND"}

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_artifacts = manifest.get("artifacts", {})

    # Verify manifest denominator excludes itself
    if "WEBRTC_DATACHANNEL_REPRODUCIBILITY_MANIFEST.json" in manifest_artifacts:
        print("[-] ERROR: Manifest includes itself in artifact list!")
        return {"verdict": "FAIL", "reason": "MANIFEST_INCLUDES_ITSELF"}

    if len(manifest_artifacts) != len(EXPECTED_14_ARTIFACTS):
        print(f"[-] ERROR: Manifest count {len(manifest_artifacts)} != expected {len(EXPECTED_14_ARTIFACTS)}")
        return {"verdict": "FAIL", "reason": "MANIFEST_COUNT_MISMATCH"}

    # 2. Verify Canonical SHA-256 Hashes
    print("[+] Verifying canonical SHA-256 hashes against manifest...")
    for filename, meta in manifest_artifacts.items():
        fpath = CANONICAL_DIR / filename
        if not fpath.exists():
            print(f"[-] Missing canonical artifact: {filename}")
            return {"verdict": "FAIL", "reason": f"MISSING_{filename}"}
        content = fpath.read_bytes()
        actual_sha = hashlib.sha256(content).hexdigest()
        if actual_sha != meta["sha256"]:
            print(f"[-] Hash mismatch for {filename}: {actual_sha} != {meta['sha256']}")
            return {"verdict": "FAIL", "reason": f"HASH_MISMATCH_{filename}"}
        if len(content) != meta["size_bytes"]:
            print(f"[-] Size mismatch for {filename}: {len(content)} != {meta['size_bytes']}")
            return {"verdict": "FAIL", "reason": f"SIZE_MISMATCH_{filename}"}

    print(f"[+] All {len(EXPECTED_14_ARTIFACTS)} canonical artifacts match manifest exactly.")

    # 3. Regenerate into Temporary Directory
    temp_dir = Path(tempfile.mkdtemp(prefix="repro_webrtc_"))
    try:
        print(f"[+] Regenerating forensics into isolated temporary directory: {temp_dir}")
        res = generate_all_forensics(temp_dir)
        print(f"[+] Generator completed. Generated {res['total_artifacts']} files. Verdict: {res['gate_verdict']}")

        # 4. Deep Compare Each Artifact
        print("[+] Deep comparing regenerated artifacts against canonical...")
        total_diffs = 0
        for filename in EXPECTED_14_ARTIFACTS:
            regen_file = temp_dir / filename
            canon_file = CANONICAL_DIR / filename

            if not regen_file.exists():
                print(f"[-] Regenerated file missing: {filename}")
                return {"verdict": "FAIL", "reason": f"REGEN_FILE_MISSING_{filename}"}

            regen_json = json.loads(regen_file.read_text(encoding="utf-8"))
            canon_json = json.loads(canon_file.read_text(encoding="utf-8"))

            diffs = deep_compare_dicts(filename, regen_json, canon_json)
            if diffs:
                print(f"[-] Differences found in {filename}:")
                for d in diffs[:10]:
                    print(f"    - {d}")
                total_diffs += len(diffs)
            else:
                print(f"  [OK] {filename}: 100% exact parity")

        if total_diffs > 0:
            print(f"[-] Total semantic differences: {total_diffs}")
            return {"verdict": "FAIL", "reason": "SEMANTIC_DIFFS_DETECTED", "diff_count": total_diffs}

        # 5. Validate Gate Result Invariants
        print("[+] Validating Phase 2C.5A forensic gate result...")
        gate_path = CANONICAL_DIR / "PHASE2C5A_FORENSIC_GATE_RESULT.json"
        gate_data = json.loads(gate_path.read_text(encoding="utf-8"))
        summary = gate_data.get("gate_summary", {})

        if summary.get("verdict") != "PASS_PHASE_2C5A_CLOSED":
            print(f"[-] Gate verdict is not PASS: {summary.get('verdict')}")
            return {"verdict": "FAIL", "reason": "GATE_NOT_PASSED"}

        if summary.get("passed_dimensions") != 19 or summary.get("total_dimensions") != 19:
            print(f"[-] Gate dimensions mismatch: {summary.get('passed_dimensions')}/19 passed")
            return {"verdict": "FAIL", "reason": "GATE_DIMENSIONS_MISMATCH"}

        print(f"[+] Gate validated: 19/19 dimensions passed. Verdict: {summary.get('verdict')}")

        # 6. Verify Strict Production Boundary
        print("[+] Verifying strict production boundary...")
        boundary_violations = verify_strict_production_boundary()
        if boundary_violations:
            for v in boundary_violations:
                print(f"[-] BOUNDARY VIOLATION: {v}")
            return {"verdict": "FAIL", "reason": "BOUNDARY_VIOLATIONS", "violations": boundary_violations}

        print("[+] Production boundary intact: ZERO production WebRTC/DataChannel/Media code.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("=" * 70)
    print("PHASE 2C.5A FORENSIC REPRODUCIBILITY VERIFICATION: PASS")
    print(f"All {len(EXPECTED_14_ARTIFACTS)} artifacts 100% reproducible directly from binaries.")
    print("=" * 70)

    return {
        "verdict": "PASS",
        "total_artifacts_verified": len(EXPECTED_14_ARTIFACTS),
        "gate_dimensions": 19,
        "gate_verdict": "PASS_PHASE_2C5A_CLOSED",
        "production_boundary": "STRICT_ZERO_PRODUCTION_CODE"
    }


def main():
    res = run_reproducibility_verification()
    if res.get("verdict") != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
