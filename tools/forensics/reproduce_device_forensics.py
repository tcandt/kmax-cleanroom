#!/usr/bin/env python3
"""
reproduce_device_forensics.py - Phase 2C.3BR Forensic Reproducibility Tool

Actually regenerates device forensic evidence artifacts into an isolated temporary directory
and performs deterministic field-by-field parity comparison against committed evidence.
"""

import sys
import json
import shutil
import re
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.generate_device_forensics import (
    generate_evidence,
    parse_elf_sections,
    parse_struct_descriptor,
    ELF_LINUX,
    OUTPUT_DIR
)

def normalize_dynamic_data(data):
    """
    Recursively normalizes ONLY ephemeral dynamic values:
    - RFC3339 timestamps
    - 64-char hex session tokens
    - Ports (29888, 29995)
    Does NOT normalize:
    - HTTP status codes, schemas, device IDs, device state, route classifications, lifecycle stages.
    """
    if isinstance(data, dict):
        norm = {}
        for k, v in data.items():
            if k in ["first_seen", "last_seen", "timestamp", "generated_at"]:
                norm[k] = "<NORMALIZED_TIMESTAMP>"
            elif k == "token" and isinstance(v, str) and len(v) == 64:
                norm[k] = "<NORMALIZED_TOKEN>"
            elif k in ["port", "url"]:
                norm[k] = re.sub(r':\d+', ':<PORT>', str(v)) if v is not None else v
            else:
                norm[k] = normalize_dynamic_data(v)
        return norm
    elif isinstance(data, list):
        return [normalize_dynamic_data(item) for item in data]
    elif isinstance(data, str):
        # Normalize timestamps inside strings
        data = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', '<NORMALIZED_TIMESTAMP>', data)
        # Normalize Bearer tokens
        data = re.sub(r'[0-9a-fA-F]{64}', '<NORMALIZED_TOKEN>', data)
        return data
    return data

def verify_reproducibility():
    print("==================================================")
    print("PHASE 2C.3BR DEVICE FORENSIC REPRODUCIBILITY AUDIT")
    print("==================================================")

    # 1. Verify binary input existence
    if not ELF_LINUX.exists():
        print(f"[FAIL] Canonical ELF binary missing: {ELF_LINUX}")
        return False
    print(f"[PASS] CANONICAL_ELF_EXISTS: {ELF_LINUX.name}")

    # 2. Run generator into isolated directory
    run_id = uuid.uuid4().hex[:8]
    temp_out = REPO_ROOT / "scratch" / "reproduce_device_forensics" / run_id
    if temp_out.exists():
        shutil.rmtree(temp_out, ignore_errors=True)
    temp_out.mkdir(parents=True, exist_ok=True)

    print(f"[*] Regenerating all 9 device artifacts into: {temp_out}")
    try:
        generate_evidence(output_dir=temp_out)
    except Exception as e:
        print(f"[FAIL] generate_evidence failed: {e}")
        return False

    # 3. Direct Type Descriptor Reproduction Check
    elf_bytes = ELF_LINUX.read_bytes()
    sections = parse_elf_sections(elf_bytes)
    dto_struct = parse_struct_descriptor(elf_bytes, sections, 0x7ff0e0)
    entry_struct = parse_struct_descriptor(elf_bytes, sections, 0x805760)

    committed_type_ev = json.loads((OUTPUT_DIR / "DEVICE_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))
    reproduced_type_ev = json.loads((temp_out / "DEVICE_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))

    dto_match = (
        dto_struct["struct_size"] == committed_type_ev["public_dto"]["struct_size"] == reproduced_type_ev["public_dto"]["struct_size"] and
        dto_struct["field_count"] == committed_type_ev["public_dto"]["field_count"] == reproduced_type_ev["public_dto"]["field_count"] == 7 and
        dto_struct["fields"] == committed_type_ev["public_dto"]["fields"] == reproduced_type_ev["public_dto"]["fields"]
    )
    entry_match = (
        entry_struct["struct_size"] == committed_type_ev["internal_registry_entry"]["struct_size"] == reproduced_type_ev["internal_registry_entry"]["struct_size"] and
        entry_struct["field_count"] == committed_type_ev["internal_registry_entry"]["field_count"] == reproduced_type_ev["internal_registry_entry"]["field_count"] == 10 and
        entry_struct["fields"] == committed_type_ev["internal_registry_entry"]["fields"] == reproduced_type_ev["internal_registry_entry"]["fields"]
    )
    type_pass = dto_match and entry_match
    print(f"[{'PASS' if type_pass else 'FAIL'}] DEVICE_TYPE_DESCRIPTOR_REPRODUCIBLE: {type_pass}")

    # 4. Static Binary Evidence / Route Identity Parity
    r_id_committed = json.loads((OUTPUT_DIR / "DEVICE_ROUTE_IDENTITY_MATRIX.json").read_text(encoding="utf-8"))
    r_id_reproduced = json.loads((temp_out / "DEVICE_ROUTE_IDENTITY_MATRIX.json").read_text(encoding="utf-8"))
    r_fam_committed = json.loads((OUTPUT_DIR / "DEVICE_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    r_fam_reproduced = json.loads((temp_out / "DEVICE_ROUTE_FAMILY.json").read_text(encoding="utf-8"))

    # Compare deterministic fields
    route_match = (
        r_id_committed["routes"] == r_id_reproduced["routes"] and
        r_fam_committed["routes"] == r_fam_reproduced["routes"]
    )
    print(f"[{'PASS' if route_match else 'FAIL'}] DEVICE_STATIC_BINARY_EVIDENCE_REPRODUCIBLE: {route_match}")

    # 5. Function Slice Reproduction Check
    f_sl_committed = json.loads((OUTPUT_DIR / "DEVICE_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    f_sl_reproduced = json.loads((temp_out / "DEVICE_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    slices_match = (
        f_sl_committed["handlers"] == f_sl_reproduced["handlers"] and
        f_sl_committed["metadata"]["derivation"] == f_sl_reproduced["metadata"]["derivation"] == "CAPSTONE_DISASSEMBLY_ANCHORS"
    )
    print(f"[{'PASS' if slices_match else 'FAIL'}] DEVICE_FUNCTION_SLICE_REPRODUCIBLE: {slices_match}")

    # 6. Dynamic Oracle Contract Parity (with timestamp/token normalization)
    dynamic_artifacts = [
        "DEVICE_EMPTY_REGISTRY_CONTRACT.json",
        "DEVICE_POPULATED_REGISTRY_CONTRACT.json",
        "DEVICE_REGISTRY_LIFECYCLE_MATRIX.json",
        "DEVICE_VISIBILITY_AUTH_MATRIX.json",
        "DEVICE_NOAUTH_CONTRACT.json"
    ]
    dynamic_match = True
    for da in dynamic_artifacts:
        comm_data = json.loads((OUTPUT_DIR / da).read_text(encoding="utf-8"))
        repr_data = json.loads((temp_out / da).read_text(encoding="utf-8"))

        norm_comm = normalize_dynamic_data(comm_data)
        norm_repr = normalize_dynamic_data(repr_data)

        if norm_comm != norm_repr:
            # Check where discrepancy is
            print(f"[FAIL] Mismatch in normalized dynamic contract: {da}")
            dynamic_match = False

    print(f"[{'PASS' if dynamic_match else 'FAIL'}] DEVICE_DYNAMIC_ORACLE_CONTRACT_REPRODUCIBLE: {dynamic_match}")

    all_pass = type_pass and route_match and slices_match and dynamic_match
    print("==================================================")
    print(f"REPRODUCIBILITY VERDICT: {'PASS' if all_pass else 'FAIL'}")
    print("==================================================")

    # Cleanup temp directory
    shutil.rmtree(temp_out, ignore_errors=True)
    return all_pass

if __name__ == "__main__":
    success = verify_reproducibility()
    sys.exit(0 if success else 1)
