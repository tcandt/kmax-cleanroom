#!/usr/bin/env python3
"""
tools/audit/build_b6f_effective_contract.py
Phase 2C.5B6FR Effective Contract View Builder.

Constructs the effective B6F implementation contract view by deterministically combining:
1. Frozen Base Contract: evidence/go_agent/webrtc/ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json
2. Formal Errata Layer:  evidence/go_agent/webrtc/ADB_CHANNEL_B6F_CONTRACT_ERRATA.json

The base contract is never modified and remains frozen (SHA256: 1b1aba53ef39786fadafaab772e11c0611198403f8910f951a507ff4b06fc3ea).
The effective contract view cleanly separates authentic original protocol parity from
cross-component evidence, safety scope guards, deferred boundaries, and reference interoperability.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent.parent

FROZEN_BASE_SHA256 = "1b1aba53ef39786fadafaab772e11c0611198403f8910f951a507ff4b06fc3ea"
BASE_CONTRACT_REL = "evidence/go_agent/webrtc/ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json"
ERRATA_REL = "evidence/go_agent/webrtc/ADB_CHANNEL_B6F_CONTRACT_ERRATA.json"


def build_b6f_effective_contract(repo_root: Path = ROOT) -> Dict[str, Any]:
    base_path = repo_root / BASE_CONTRACT_REL
    errata_path = repo_root / ERRATA_REL

    if not base_path.exists():
        raise FileNotFoundError(f"B6F Base contract missing: {base_path}")
    if not errata_path.exists():
        raise FileNotFoundError(f"B6F Errata file missing: {errata_path}")

    base_bytes = base_path.read_bytes()
    actual_base_sha = hashlib.sha256(base_bytes).hexdigest().lower()
    if actual_base_sha != FROZEN_BASE_SHA256.lower():
        raise ValueError(
            f"B6F Base contract SHA256 mismatch! Expected frozen {FROZEN_BASE_SHA256}, got {actual_base_sha}"
        )

    base_data = json.loads(base_bytes.decode("utf-8"))
    errata_data = json.loads(errata_path.read_text(encoding="utf-8"))

    errata_meta = errata_data.get("metadata", {})
    ref_sha = errata_meta.get("base_contract_sha256")
    if ref_sha != FROZEN_BASE_SHA256:
        raise ValueError(
            f"B6F Errata references incorrect base contract SHA256: {ref_sha} != {FROZEN_BASE_SHA256}"
        )

    corrections_map = {}
    for c in errata_data.get("corrections", []):
        cid = c.get("base_contract_id") or c.get("contract_id")
        corrections_map[cid] = c

    effective_reqs: List[Dict[str, Any]] = []
    by_classification: Dict[str, List[str]] = {
        "original_static_evidence": [],
        "cross_component_evidence": [],
        "reference_interoperability": [],
        "reference_background": [],
        "safe_scope_guard": [],
        "defensive_validation": [],
        "deferred_execution_boundary": [],
        "audit_provenance_guard": [],
        "unknown": []
    }

    for req in base_data.get("requirements", []):
        cid = req.get("contract_id") or req.get("id")
        corr = corrections_map.get(cid)

        eff_req: Dict[str, Any] = {
            "contract_id": cid,
            "title": req.get("title", ""),
            "description": req.get("description", ""),
            "base_evidence_class": req.get("evidence_class", ""),
            "base_mandatory_for_parity": req.get("mandatory_for_parity", False),
        }

        if corr:
            eff_req["has_errata_correction"] = True
            eff_req["effective_original_parity_claim"] = corr.get("corrected_original_parity_claim", "")
            eff_req["effective_classification"] = corr.get("effective_evidence_class", req.get("evidence_class"))
            eff_req["effective_mandatory_for_original_parity"] = corr.get("effective_mandatory_for_original_parity", False)
            eff_req["mandatory_for_safe_scope"] = corr.get("mandatory_for_safe_scope", False)
            eff_req["mandatory_for_interoperability"] = corr.get("mandatory_for_interoperability", False)
            eff_req["mandatory_for_audit_scope"] = corr.get("mandatory_for_audit_scope", False)
            eff_req["non_original_compatibility_behavior"] = corr.get("non_original_compatibility_behavior", "")
            eff_req["reference_only_parts"] = corr.get("reference_only_parts", [])
            eff_req["split_effective_semantics"] = corr.get("split_effective_semantics", {})
            eff_req["errata_rationale"] = corr.get("rationale", "")
        else:
            eff_req["has_errata_correction"] = False
            eff_req["effective_original_parity_claim"] = req.get("description", "")
            eff_req["effective_classification"] = req.get("evidence_class", "")
            eff_req["effective_mandatory_for_original_parity"] = req.get("mandatory_for_parity", False)
            eff_req["mandatory_for_safe_scope"] = req.get("mandatory_for_safe_scope", False)
            eff_req["mandatory_for_interoperability"] = req.get("mandatory_for_interoperability", False)
            eff_req["mandatory_for_audit_scope"] = req.get("mandatory_for_audit_scope", False)

        e_class = eff_req["effective_classification"]
        if e_class == "STATIC_CONFIRMED":
            by_classification["original_static_evidence"].append(cid)
        elif e_class == "CROSS_COMPONENT_CONFIRMED":
            by_classification["cross_component_evidence"].append(cid)
        elif e_class in ("REFERENCE_INTEROPERABILITY", "REFERENCE_ONLY"):
            by_classification["reference_interoperability"].append(cid)
        elif e_class == "REFERENCE_BACKGROUND":
            by_classification["reference_background"].append(cid)
        elif e_class == "SAFE_SCOPE_GUARD":
            by_classification["safe_scope_guard"].append(cid)
        elif e_class == "DEFENSIVE_VALIDATION":
            by_classification["defensive_validation"].append(cid)
        elif e_class == "DEFERRED_ADB_BRIDGE_BOUNDARY":
            by_classification["deferred_execution_boundary"].append(cid)
        elif e_class == "AUDIT_PROVENANCE_GUARD":
            by_classification["audit_provenance_guard"].append(cid)
        else:
            by_classification["unknown"].append(cid)

        effective_reqs.append(eff_req)

    taxonomy_counts = {k: len(v) for k, v in by_classification.items()}

    effective_contract = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "metadata": {
            "title": "Phase 2C.5B6F ADB-Channel Effective Implementation Contract View",
            "phase": "Phase 2C.5B6FR",
            "base_contract_path": BASE_CONTRACT_REL,
            "base_contract_sha256": FROZEN_BASE_SHA256,
            "errata_path": ERRATA_REL,
            "total_requirements": len(effective_reqs),
            "taxonomy_counts": taxonomy_counts,
            "by_classification": by_classification,
            "effective_contract_rules": [
                "Base contract ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json remains strictly frozen and immutable with SHA256 1b1aba53ef39786fadafaab772e11c0611198403f8910f951a507ff4b06fc3ea.",
                "Channel label & direction (ADB-B6F-01) is split between Agent inbound consumption (STATIC_CONFIRMED) and Browser client creation (REFERENCE_INTEROPERABILITY), yielding effective classification CROSS_COMPONENT_CONFIRMED.",
                "Authentic original static evidence count is exactly 7 (ADB-B6F-02 through ADB-B6F-08).",
                "Browser client creation and ordered=true (ADB-B6F-09) are client interoperability facts and do not inflate original Agent static parity.",
                "Standard Android ADB protocol documentation (ADB-B6F-10) is REFERENCE_BACKGROUND.",
                "Deferred bridge boundary (ADB-B6F-11) and channel inertness (ADB-B6F-12) are clean-room scope constraints (DEFERRED_ADB_BRIDGE_BOUNDARY and SAFE_SCOPE_GUARD).",
                "Historical errata recording (ADB-B6F-13) is classified as AUDIT_PROVENANCE_GUARD."
            ]
        },
        "requirements": effective_reqs
    }

    return effective_contract


def main():
    parser = argparse.ArgumentParser(description="Build Phase 2C.5B6F Effective Implementation Contract View")
    parser.add_argument("--json", action="store_true", help="Print effective contract as formatted JSON")
    parser.add_argument("--check", action="store_true", help="Validate invariants and print summary")
    args = parser.parse_args()

    try:
        eff = build_b6f_effective_contract(ROOT)
        tc = eff["metadata"]["taxonomy_counts"]

        if args.json:
            print(json.dumps(eff, indent=2))
            return 0

        print("=== Phase 2C.5B6F ADB-Channel Effective Contract View ===")
        print(f"Base Contract:    {eff['metadata']['base_contract_path']} (SHA: {eff['metadata']['base_contract_sha256'][:16]}...)")
        print(f"Errata Layer:     {eff['metadata']['errata_path']}")
        print(f"Total Requirements: {eff['metadata']['total_requirements']}")
        print("Taxonomy Breakdown:")
        print(f"  - Original Static Evidence:       {tc['original_static_evidence']} (ADB-B6F-02..08)")
        print(f"  - Cross-Component Evidence:       {tc['cross_component_evidence']} (ADB-B6F-01)")
        print(f"  - Reference Interoperability:     {tc['reference_interoperability']} (ADB-B6F-09)")
        print(f"  - Reference Background:           {tc['reference_background']} (ADB-B6F-10)")
        print(f"  - Safe Scope Guard:               {tc['safe_scope_guard']} (ADB-B6F-12)")
        print(f"  - Defensive Validation:           {tc['defensive_validation']}")
        print(f"  - Deferred Execution Boundary:    {tc['deferred_execution_boundary']} (ADB-B6F-11)")
        print(f"  - Audit Provenance Guard:         {tc['audit_provenance_guard']} (ADB-B6F-13)")
        print(f"  - Unknown:                        {tc['unknown']}")

        # Invariant checks
        assert tc["original_static_evidence"] == 7, f"Expected 7 original static, got {tc['original_static_evidence']}"
        assert tc["cross_component_evidence"] == 1, f"Expected 1 cross component, got {tc['cross_component_evidence']}"
        assert tc["reference_interoperability"] == 1, f"Expected 1 reference interoperability, got {tc['reference_interoperability']}"
        assert tc["reference_background"] == 1, f"Expected 1 reference background, got {tc['reference_background']}"
        assert tc["safe_scope_guard"] == 1, f"Expected 1 safe scope guard, got {tc['safe_scope_guard']}"
        assert tc["defensive_validation"] == 0, f"Expected 0 defensive validation, got {tc['defensive_validation']}"
        assert tc["deferred_execution_boundary"] == 1, f"Expected 1 deferred boundary, got {tc['deferred_execution_boundary']}"
        assert tc["audit_provenance_guard"] == 1, f"Expected 1 audit guard, got {tc['audit_provenance_guard']}"
        assert tc["unknown"] == 0, f"Expected 0 unknown, got {tc['unknown']}"
        assert eff["metadata"]["total_requirements"] == 13, f"Expected 13 total, got {eff['metadata']['total_requirements']}"

        print("\n[PASS] All B6F Effective Contract Taxonomy Invariants verified successfully.")
        return 0
    except Exception as e:
        print(f"[FAIL] Error building B6F effective contract: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
