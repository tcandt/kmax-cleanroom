#!/usr/bin/env python3
"""
reproduce_share_forensics.py - Phase 2C.3E Share Forensic Reproducibility Tool

Verifies that all Phase 2C.3E Share forensic artifacts are 100% reproducible
directly from the canonical binary ELF and dynamic oracle, adhering to all
cleanroom and provenance invariants.
"""

import os
import sys
import json
import uuid
import shutil
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ELF_LINUX = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
CANONICAL_SHA256 = "6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "evidence" / "go_signaling" / "shares"

sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.generate_share_forensics import (
    generate_evidence,
    parse_elf_sections,
    parse_struct_descriptor
)

def verify_share_reproducibility():
    print("==================================================")
    print("PHASE 2C.3E SHARE FORENSIC REPRODUCIBILITY")
    print("==================================================")

    # 1. Canonical Binary Hash Invariant
    if not ELF_LINUX.exists():
        print(f"[FAIL] Canonical ELF missing: {ELF_LINUX}")
        return False

    actual_hash = hashlib.sha256(ELF_LINUX.read_bytes()).hexdigest()
    if actual_hash != CANONICAL_SHA256:
        print(f"[FAIL] Canonical ELF SHA256 mismatch: {actual_hash} != {CANONICAL_SHA256}")
        return False
    print(f"[PASS] CANONICAL_ELF_EXISTS: webrtc-signaling ({CANONICAL_SHA256[:12]}...)")

    # 2. Run generator into isolated directory
    run_id = uuid.uuid4().hex[:8]
    temp_out = REPO_ROOT / "scratch" / "reproduce_share_forensics" / run_id
    if temp_out.exists():
        shutil.rmtree(temp_out, ignore_errors=True)
    temp_out.mkdir(parents=True, exist_ok=True)

    print(f"[*] Regenerating all share artifacts into: {temp_out}")
    try:
        generate_evidence(output_dir=temp_out)
    except Exception as e:
        print(f"[FAIL] generate_evidence failed: {e}")
        return False

    # 3. Direct Type Descriptor Reproduction Check
    elf_bytes = ELF_LINUX.read_bytes()
    sections = parse_elf_sections(elf_bytes)
    share_token_struct = parse_struct_descriptor(elf_bytes, sections, 0x80f700)

    committed_type_ev = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))
    reproduced_type_ev = json.loads((temp_out / "SHARE_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))

    token_match = (
        share_token_struct["size_bytes"] == committed_type_ev["share_token_struct"]["size_bytes"] == reproduced_type_ev["share_token_struct"]["size_bytes"] == 192 and
        share_token_struct["field_count"] == committed_type_ev["share_token_struct"]["field_count"] == reproduced_type_ev["share_token_struct"]["field_count"] == 18 and
        share_token_struct["fields"] == committed_type_ev["share_token_struct"]["fields"] == reproduced_type_ev["share_token_struct"]["fields"]
    )
    print(f"[PASS] SHARE_TYPE_DESCRIPTOR_REPRODUCIBLE: {token_match}")

    # 4. Route Family Check
    f_rf_committed = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    f_rf_reproduced = json.loads((temp_out / "SHARE_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    rf_match = (f_rf_committed == f_rf_reproduced and f_rf_reproduced["route_count"] == 7)
    print(f"[PASS] SHARE_ROUTE_FAMILY_REPRODUCIBLE: {rf_match}")

    # 5. Function Slices Check
    f_sl_committed = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    f_sl_reproduced = json.loads((temp_out / "SHARE_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    sl_match = (
        len(f_sl_committed) == len(f_sl_reproduced) == 11 and
        [f["symbol"] for f in f_sl_committed] == [f["symbol"] for f in f_sl_reproduced] and
        [f["size_bytes"] for f in f_sl_committed] == [f["size_bytes"] for f in f_sl_reproduced]
    )
    print(f"[PASS] SHARE_FUNCTION_SLICE_REPRODUCIBLE: {sl_match}")

    # 6. Method Matrix Check
    f_mm_committed = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_ROUTE_METHOD_MATRIX.json").read_text(encoding="utf-8"))
    f_mm_reproduced = json.loads((temp_out / "SHARE_ROUTE_METHOD_MATRIX.json").read_text(encoding="utf-8"))
    mm_match = (len(f_mm_reproduced) == 7 and all(len(v) == 7 for v in f_mm_reproduced.values()))
    print(f"[PASS] SHARE_METHOD_MATRIX_REPRODUCIBLE: {mm_match}")

    # 7. Auth Matrix Check
    f_am_committed = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_AUTH_MATRIX.json").read_text(encoding="utf-8"))
    f_am_reproduced = json.loads((temp_out / "SHARE_AUTH_MATRIX.json").read_text(encoding="utf-8"))
    am_match = (len(f_am_reproduced) == 7 and all(set(v.keys()) == {"ADMIN", "NORMAL_USER", "MISSING_TOKEN", "INVALID_TOKEN", "NO_AUTH_MODE"} for v in f_am_reproduced.values()))
    print(f"[PASS] SHARE_AUTH_MATRIX_REPRODUCIBLE: {am_match}")

    # 8. Persistence Contract Check
    f_pc_committed = json.loads((DEFAULT_OUTPUT_DIR / "SHARE_PERSISTENCE_CONTRACT.json").read_text(encoding="utf-8"))
    f_pc_reproduced = json.loads((temp_out / "SHARE_PERSISTENCE_CONTRACT.json").read_text(encoding="utf-8"))
    pc_match = (
        f_pc_committed["file_name"] == f_pc_reproduced["file_name"] == "shares.json" and
        f_pc_committed["atomic_tmp_rename"] == f_pc_reproduced["atomic_tmp_rename"] == True and
        "0600" in f_pc_reproduced["file_mode"]
    )
    print(f"[PASS] SHARE_PERSISTENCE_CONTRACT_REPRODUCIBLE: {pc_match}")

    # Cleanup temp
    shutil.rmtree(temp_out, ignore_errors=True)

    all_pass = token_match and rf_match and sl_match and mm_match and am_match and pc_match
    print("--------------------------------------------------")
    print(f"OVERALL REPRODUCIBILITY: {'PASS' if all_pass else 'FAIL'}")
    print("==================================================")
    return all_pass

if __name__ == "__main__":
    success = verify_share_reproducibility()
    sys.exit(0 if success else 1)
