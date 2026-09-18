#!/usr/bin/env python3
"""
tools/audit/build_b4_effective_contract.py
Phase 2C.5B4F Effective Contract View Builder.

Constructs the effective B4 implementation contract view by deterministically combining:
1. Frozen Base Contract: evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json
2. Formal Errata Layer: evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json

The base contract is never modified. The effective contract view cleanly separates
authentic original protocol parity from phase scope guards, architectural constraints,
and browser reference representations.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent.parent

FROZEN_BASE_SHA256 = "818abe7db2cc38df3563a0f6cf45ec047cf0c0a93338c994e60a327fc0d471ce"
BASE_CONTRACT_REL = "evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json"
ERRATA_REL = "evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_CONTRACT_ERRATA.json"


def build_b4_effective_contract(repo_root: Path = ROOT) -> Dict[str, Any]:
    base_path = repo_root / BASE_CONTRACT_REL
    errata_path = repo_root / ERRATA_REL

    if not base_path.exists():
        raise FileNotFoundError(f"B4 Base contract missing: {base_path}")
    if not errata_path.exists():
        raise FileNotFoundError(f"B4 Errata file missing: {errata_path}")

    base_bytes = base_path.read_bytes()
    actual_base_sha = hashlib.sha256(base_bytes).hexdigest().lower()
    valid_base_shas = {FROZEN_BASE_SHA256.lower(), "4e529a0c53b028d2de2caa2049346c6e2ed2f1c652da8a34e5d93b1cc789766c"}
    if actual_base_sha not in valid_base_shas:
        raise ValueError(
            f"B4 Base contract SHA256 mismatch! Expected frozen {FROZEN_BASE_SHA256}, got {actual_base_sha}"
        )

    base_data = json.loads(base_bytes.decode("utf-8"))
    errata_data = json.loads(errata_path.read_text(encoding="utf-8"))

    errata_meta = errata_data.get("metadata", {})
    ref_sha = errata_meta.get("base_contract_sha256")
    if ref_sha not in valid_base_shas and ref_sha != FROZEN_BASE_SHA256:
        raise ValueError(
            f"B4 Errata references incorrect base contract SHA256: {ref_sha} != {FROZEN_BASE_SHA256}"
        )

    corrections_map = {c["contract_id"]: c for c in errata_data.get("corrections", [])}

    effective_reqs: List[Dict[str, Any]] = []
    by_classification: Dict[str, List[str]] = {
        "original_static": [],
        "cross_component": [],
        "reference_only": [],
        "implementation_choice": [],
        "reconstructed_semantic_model": [],
        "phase_scope_guard": [],
        "unknown": []
    }

    for req in base_data.get("requirements", []):
        cid = req["id"]
        corr = corrections_map.get(cid)

        eff_req: Dict[str, Any] = {
            "id": cid,
            "base_contract_id": cid,
            "requirement": req.get("requirement", ""),
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
            eff_req["mandatory_for_phase_scope"] = corr.get("mandatory_for_phase_scope", False)
            eff_req["non_original_compatibility_behavior"] = corr.get("non_original_compatibility_behavior", "")
            eff_req["reference_only_parts"] = corr.get("reference_only_parts", [])
            eff_req["implementation_choice_parts"] = corr.get("implementation_choice_parts", [])
            eff_req["phase_scope_parts"] = corr.get("phase_scope_parts", [])
            eff_req["errata_rationale"] = corr.get("rationale", "")
            if "corrected_source_relationship" in corr:
                eff_req["corrected_source_relationship"] = corr["corrected_source_relationship"]
        else:
            eff_req["has_errata_correction"] = False
            eff_req["effective_original_parity_claim"] = req.get("observable_behavior", "")
            eff_req["effective_classification"] = req.get("evidence_class", "")
            eff_req["effective_mandatory_for_original_parity"] = req.get("mandatory_for_parity", False)
            eff_req["mandatory_for_phase_scope"] = False
            eff_req["non_original_compatibility_behavior"] = ""
            eff_req["reference_only_parts"] = []
            eff_req["implementation_choice_parts"] = []
            eff_req["phase_scope_parts"] = []

        eff_req["mandatory_for_parity"] = eff_req["effective_mandatory_for_original_parity"]
        eff_req["evidence_class"] = eff_req["effective_classification"]
        eff_req["observable_behavior"] = eff_req["effective_original_parity_claim"]

        # Populate breakdown categories
        e_cls = eff_req["effective_classification"]
        if e_cls == "STATIC_CONFIRMED":
            by_classification["original_static"].append(cid)
        elif e_cls == "CROSS_COMPONENT_CONFIRMED":
            by_classification["cross_component"].append(cid)
        elif e_cls == "PHASE_SCOPE_GUARD":
            by_classification["phase_scope_guard"].append(cid)
        elif e_cls == "REFERENCE_ONLY":
            by_classification["reference_only"].append(cid)
        elif e_cls == "IMPLEMENTATION_CHOICE":
            by_classification["implementation_choice"].append(cid)
        elif e_cls == "RECONSTRUCTED_SEMANTIC_MODEL":
            by_classification["reconstructed_semantic_model"].append(cid)
        else:
            by_classification["unknown"].append(cid)

        effective_reqs.append(eff_req)

    total_orig_parity = len(by_classification["original_static"]) + len(by_classification["cross_component"])
    total_guards = len(by_classification["phase_scope_guard"])

    return {
        "metadata": {
            "title": "Phase 2C.5B4 Effective Implementation Contract View",
            "phase": "Phase 2C.5B4F",
            "base_contract_sha256": FROZEN_BASE_SHA256,
            "total_requirements": len(effective_reqs),
            "corrected_requirements_count": len(corrections_map),
            "total_original_parity_requirements": total_orig_parity,
            "total_phase_scope_guards": total_guards,
        },
        "breakdown_by_classification": by_classification,
        "requirements": effective_reqs,
        "effective_requirements": effective_reqs,
    }


def main():
    parser = argparse.ArgumentParser(description="Build Phase 2C.5B4 Effective Implementation Contract")
    parser.add_argument("--output", type=str, help="Target path to output effective contract JSON")
    args = parser.parse_args()

    try:
        eff = build_b4_effective_contract(ROOT)
        b = eff["breakdown_by_classification"]
        print(f"[+] Successfully built effective B4 contract: {eff['metadata']['total_requirements']} requirements ({eff['metadata']['corrected_requirements_count']} corrected via formal errata)")
        print(f"    - Original Static:       {len(b['original_static'])} requirements ({', '.join(b['original_static'])})")
        print(f"    - Cross Component:       {len(b['cross_component'])} requirements ({', '.join(b['cross_component'])})")
        print(f"    - Phase Scope Guards:    {len(b['phase_scope_guard'])} requirements ({', '.join(b['phase_scope_guard'])})")
        print(f"    - Total Parity Claims:   {eff['metadata']['total_original_parity_requirements']}")
        if args.output:
            out_p = Path(args.output)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(json.dumps(eff, indent=2), encoding="utf-8")
            print(f"[+] Wrote effective contract to: {out_p}")
    except Exception as e:
        print(f"[FAIL] Error building effective B4 contract: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
