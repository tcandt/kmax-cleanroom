#!/usr/bin/env python3
"""
tools/audit/build_b2_effective_contract.py
Phase 2C.5B2R4 Effective Contract View Builder.

Constructs the effective B2 implementation contract view by deterministically combining:
1. Frozen Base Contract: evidence/go_agent/webrtc/DATACHANNEL_B2_IMPLEMENTATION_CONTRACT.json
2. Formal Errata Layer: evidence/go_agent/webrtc/DATACHANNEL_B2_CONTRACT_ERRATA.json

The base contract is never modified. The effective contract view cleanly separates
authentic original protocol parity from frontend reference compatibility,
Go adapter implementation choices, defensive hardening, and phase-scope guards.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent.parent

FROZEN_BASE_SHA256 = "3d7ebd83a675b2eb2103813a063cf012def36b98b4303f146b8b1c60ebaaa6f7"
BASE_CONTRACT_REL = "evidence/go_agent/webrtc/DATACHANNEL_B2_IMPLEMENTATION_CONTRACT.json"
ERRATA_REL = "evidence/go_agent/webrtc/DATACHANNEL_B2_CONTRACT_ERRATA.json"


def build_effective_contract(repo_root: Path = ROOT) -> Dict[str, Any]:
    base_path = repo_root / BASE_CONTRACT_REL
    errata_path = repo_root / ERRATA_REL

    if not base_path.exists():
        raise FileNotFoundError(f"Base contract missing: {base_path}")
    if not errata_path.exists():
        raise FileNotFoundError(f"Errata file missing: {errata_path}")

    base_bytes = base_path.read_bytes()
    actual_base_sha = hashlib.sha256(base_bytes).hexdigest()
    if actual_base_sha != FROZEN_BASE_SHA256:
        raise ValueError(
            f"Base contract SHA256 mismatch! Expected frozen {FROZEN_BASE_SHA256}, got {actual_base_sha}"
        )

    base_data = json.loads(base_bytes.decode("utf-8"))
    errata_data = json.loads(errata_path.read_text(encoding="utf-8"))

    errata_meta = errata_data.get("metadata", {})
    ref_sha = errata_meta.get("base_contract_sha256")
    if ref_sha != FROZEN_BASE_SHA256:
        raise ValueError(
            f"Errata references incorrect base contract SHA256: {ref_sha} != {FROZEN_BASE_SHA256}"
        )

    corrections_map = {c["contract_id"]: c for c in errata_data.get("corrections", [])}

    effective_reqs: List[Dict[str, Any]] = []
    for req in base_data.get("requirements", []):
        cid = req["id"]
        corr = corrections_map.get(cid)

        eff_req: Dict[str, Any] = {
            "base_contract_id": cid,
            "requirement_name": req.get("requirement", ""),
            "source_artifact": req.get("source_artifact", ""),
            "source_field_or_case": req.get("source_field_or_case", ""),
            "base_observable_behavior": req.get("observable_behavior", ""),
            "base_evidence_class": req.get("evidence_class", ""),
            "base_mandatory_for_parity": req.get("mandatory_for_parity", False),
        }

        if corr:
            eff_req["has_errata_correction"] = True
            eff_req["effective_original_parity_claim"] = corr["corrected_original_parity_claim"]
            eff_req["effective_classification"] = corr["effective_evidence_class"]
            eff_req["effective_mandatory_for_original_parity"] = corr["effective_mandatory_for_original_parity"]
            eff_req["non_original_compatibility_behavior"] = corr.get("non_original_compatibility_behavior", "")
            eff_req["reference_only_parts"] = corr.get("reference_only_parts", [])
            eff_req["implementation_choice_parts"] = corr.get("implementation_choice_parts", [])
            eff_req["phase_scope_parts"] = corr.get("phase_scope_parts", [])
            eff_req["errata_rationale"] = corr.get("rationale", "")
        else:
            eff_req["has_errata_correction"] = False
            eff_req["effective_original_parity_claim"] = req.get("observable_behavior", "")
            eff_req["effective_classification"] = req.get("evidence_class", "")
            eff_req["effective_mandatory_for_original_parity"] = req.get("mandatory_for_parity", False)
            eff_req["non_original_compatibility_behavior"] = ""
            eff_req["reference_only_parts"] = []
            eff_req["implementation_choice_parts"] = []
            eff_req["phase_scope_parts"] = []
            eff_req["errata_rationale"] = ""

        effective_reqs.append(eff_req)

    effective_contract = {
        "metadata": {
            "title": "Phase 2C.5B2 Effective DataChannel Implementation Contract",
            "phase": "Phase 2C.5B2R4",
            "base_contract_path": BASE_CONTRACT_REL,
            "base_contract_sha256": FROZEN_BASE_SHA256,
            "errata_path": ERRATA_REL,
            "total_effective_requirements": len(effective_reqs),
            "mandatory_original_parity_count": sum(
                1 for r in effective_reqs if r["effective_mandatory_for_original_parity"] is True
            ),
            "implementation_choice_count": sum(
                1 for r in effective_reqs if r["effective_classification"] == "IMPLEMENTATION_CHOICE"
            ),
            "phase_scope_guard_count": sum(
                1 for r in effective_reqs if r["effective_classification"] == "PHASE_SCOPE_GUARD"
            ),
        },
        "effective_requirements": effective_reqs,
    }

    return effective_contract


def main():
    parser = argparse.ArgumentParser(description="Phase 2C.5B2R4 Effective Contract View Builder")
    parser.add_argument("--output", type=str, help="Optional output path to write effective contract JSON")
    args = parser.parse_args()

    try:
        eff = build_effective_contract(ROOT)
        meta = eff["metadata"]
        print(f"[PASS] Successfully constructed effective contract view.")
        print(f"       Total requirements: {meta['total_effective_requirements']}")
        print(f"       Mandatory original parity: {meta['mandatory_original_parity_count']}")
        print(f"       Implementation choice: {meta['implementation_choice_count']}")
        print(f"       Phase scope guards: {meta['phase_scope_guard_count']}")

        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(json.dumps(eff, indent=2), encoding="utf-8")
            print(f"[+] Wrote effective contract view to {out_p}")
    except Exception as e:
        print(f"[FAIL] Error constructing effective contract: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
