#!/usr/bin/env python3
"""
reproduce_user_admin_forensics.py - Phase 2C.3C User/Admin Forensic Reproducibility Tool

Regenerates all 10 user/admin forensic artifacts into an isolated scratch directory
and performs rigorous deterministic field-by-field parity comparison against committed evidence.
"""

import sys
import json
import shutil
import re
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.generate_user_admin_forensics import (
    generate_evidence,
    parse_elf_sections,
    parse_struct_descriptor,
    ELF_LINUX,
    DEFAULT_OUTPUT_DIR
)

def normalize_dynamic_data(data):
    """
    Recursively normalizes ONLY ephemeral dynamic values:
    - RFC3339 timestamps
    - 64-char hex session tokens
    - Ports
    Does NOT normalize:
    - HTTP status codes, JSON schemas, routes, verbs, roles, salt lengths, auth outcomes.
    """
    if isinstance(data, dict):
        norm = {}
        for k, v in data.items():
            if k in ["first_seen", "last_seen", "timestamp", "generated_at"]:
                norm[k] = "<NORMALIZED_TIMESTAMP>"
            elif k in ["token", "admin_token", "normal_token"] and isinstance(v, str) and len(v) == 64:
                norm[k] = "<NORMALIZED_TOKEN>"
            elif k in ["port", "url"]:
                norm[k] = re.sub(r':\d+', ':<PORT>', str(v)) if v is not None else v
            else:
                norm[k] = normalize_dynamic_data(v)
        return norm
    elif isinstance(data, list):
        return [normalize_dynamic_data(item) for item in data]
    elif isinstance(data, str):
        data = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', '<NORMALIZED_TIMESTAMP>', data)
        data = re.sub(r'[0-9a-fA-F]{64}', '<NORMALIZED_TOKEN>', data)
        return data
    return data

def verify_reproducibility():
    print("==================================================")
    print("PHASE 2C.3C USERS/ADMIN FORENSIC REPRODUCIBILITY")
    print("==================================================")

    # 1. Verify binary input existence
    if not ELF_LINUX.exists():
        print(f"[FAIL] Canonical ELF binary missing: {ELF_LINUX}")
        return False
    print(f"[PASS] CANONICAL_ELF_EXISTS: {ELF_LINUX.name}")

    # 2. Run generator into isolated directory
    run_id = uuid.uuid4().hex[:8]
    temp_out = REPO_ROOT / "scratch" / "reproduce_user_admin_forensics" / run_id
    if temp_out.exists():
        shutil.rmtree(temp_out, ignore_errors=True)
    temp_out.mkdir(parents=True, exist_ok=True)

    print(f"[*] Regenerating all 10 user/admin artifacts into: {temp_out}")
    try:
        generate_evidence(output_dir=temp_out)
    except Exception as e:
        print(f"[FAIL] generate_evidence failed: {e}")
        return False

    # 3. Direct Type Descriptor Reproduction Check
    elf_bytes = ELF_LINUX.read_bytes()
    sections = parse_elf_sections(elf_bytes)
    user_struct = parse_struct_descriptor(elf_bytes, sections, 0x80a0c0)
    ai_struct = parse_struct_descriptor(elf_bytes, sections, 0x7ed060)

    committed_type_ev = json.loads((DEFAULT_OUTPUT_DIR / "USER_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))
    reproduced_type_ev = json.loads((temp_out / "USER_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))

    user_match = (
        user_struct["size_bytes"] == committed_type_ev["storage_types"]["User"]["size_bytes"] == reproduced_type_ev["storage_types"]["User"]["size_bytes"] and
        user_struct["field_count"] == committed_type_ev["storage_types"]["User"]["field_count"] == reproduced_type_ev["storage_types"]["User"]["field_count"] == 13 and
        user_struct["fields"] == committed_type_ev["storage_types"]["User"]["fields"] == reproduced_type_ev["storage_types"]["User"]["fields"]
    )
    ai_match = (
        ai_struct["size_bytes"] == committed_type_ev["storage_types"]["AIConfig"]["size_bytes"] == reproduced_type_ev["storage_types"]["AIConfig"]["size_bytes"] and
        ai_struct["field_count"] == committed_type_ev["storage_types"]["AIConfig"]["field_count"] == reproduced_type_ev["storage_types"]["AIConfig"]["field_count"] == 4 and
        ai_struct["fields"] == committed_type_ev["storage_types"]["AIConfig"]["fields"] == reproduced_type_ev["storage_types"]["AIConfig"]["fields"]
    )
    type_pass = user_match and ai_match
    print(f"[{'PASS' if type_pass else 'FAIL'}] USER_TYPE_DESCRIPTOR_REPRODUCIBLE: {type_pass}")

    # 4. Static Binary Evidence / Route Identity Parity
    r_fam_committed = json.loads((DEFAULT_OUTPUT_DIR / "USER_ADMIN_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    r_fam_reproduced = json.loads((temp_out / "USER_ADMIN_ROUTE_FAMILY.json").read_text(encoding="utf-8"))

    route_match = (r_fam_committed["routes"] == r_fam_reproduced["routes"])
    print(f"[{'PASS' if route_match else 'FAIL'}] USER_STATIC_BINARY_EVIDENCE_REPRODUCIBLE: {route_match}")

    # 5. Function Slice Reproduction Check
    f_sl_committed = json.loads((DEFAULT_OUTPUT_DIR / "USER_ADMIN_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    f_sl_reproduced = json.loads((temp_out / "USER_ADMIN_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    slice_match = (f_sl_committed == f_sl_reproduced)
    print(f"[{'PASS' if slice_match else 'FAIL'}] USER_FUNCTION_SLICE_REPRODUCIBLE: {slice_match}")

    # 6. Dynamic Oracle Contract Reproduction Check (Normalized)
    dynamic_files = [
        "USER_ADMIN_ROUTE_METHOD_MATRIX.json",
        "USER_ADMIN_READ_CONTRACT.json",
        "USER_CREATE_CONTRACT.json",
        "USER_UPDATE_CONTRACTS.json",
        "USER_DELETE_CONTRACT.json",
        "USER_ASSIGNMENT_CROSS_CONTRACT.json",
        "USER_ADMIN_AUTH_MATRIX.json"
    ]

    oracle_matches = []
    for fname in dynamic_files:
        c_data = normalize_dynamic_data(json.loads((DEFAULT_OUTPUT_DIR / fname).read_text(encoding="utf-8")))
        r_data = normalize_dynamic_data(json.loads((temp_out / fname).read_text(encoding="utf-8")))
        matched = (c_data == r_data)
        if not matched:
            print(f"[-] Dynamic mismatch in: {fname}")
        oracle_matches.append(matched)

    oracle_pass = all(oracle_matches)
    print(f"[{'PASS' if oracle_pass else 'FAIL'}] USER_DYNAMIC_ORACLE_CONTRACT_REPRODUCIBLE: {oracle_pass}")

    overall = type_pass and route_match and slice_match and oracle_pass
    print("--------------------------------------------------")
    print(f"OVERALL REPRODUCIBILITY: {'PASS' if overall else 'FAIL'}")
    print("==================================================")
    return overall

if __name__ == "__main__":
    success = verify_reproducibility()
    sys.exit(0 if success else 1)
