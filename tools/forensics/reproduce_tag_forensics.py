#!/usr/bin/env python3
"""
reproduce_tag_forensics.py - Phase 2C.3D Tag Forensic Reproducibility Tool

Verifies that all Phase 2C.3D Tag forensic artifacts are 100% reproducible
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
DEFAULT_OUTPUT_DIR = REPO_ROOT / "evidence" / "go_signaling" / "tags"

sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.generate_tag_forensics import (
    generate_evidence,
    parse_elf_sections,
    parse_struct_descriptor
)

def verify_tag_reproducibility():
    print("==================================================")
    print("PHASE 2C.3D TAG FORENSIC REPRODUCIBILITY")
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
    temp_out = REPO_ROOT / "scratch" / "reproduce_tag_forensics" / run_id
    if temp_out.exists():
        shutil.rmtree(temp_out, ignore_errors=True)
    temp_out.mkdir(parents=True, exist_ok=True)

    print(f"[*] Regenerating all tag artifacts into: {temp_out}")
    try:
        generate_evidence(output_dir=temp_out)
    except Exception as e:
        print(f"[FAIL] generate_evidence failed: {e}")
        return False

    # 3. Direct Type Descriptor Reproduction Check
    elf_bytes = ELF_LINUX.read_bytes()
    sections = parse_elf_sections(elf_bytes)
    tag_struct = parse_struct_descriptor(elf_bytes, sections, 0x7e25a0)
    config_struct = parse_struct_descriptor(elf_bytes, sections, 0x7d6f80)

    committed_type_ev = json.loads((DEFAULT_OUTPUT_DIR / "TAG_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))
    reproduced_type_ev = json.loads((temp_out / "TAG_TYPE_EVIDENCE.json").read_text(encoding="utf-8"))

    tag_match = (
        tag_struct["size_bytes"] == committed_type_ev["types"]["Tag"]["size_bytes"] == reproduced_type_ev["types"]["Tag"]["size_bytes"] == 48 and
        tag_struct["field_count"] == committed_type_ev["types"]["Tag"]["field_count"] == reproduced_type_ev["types"]["Tag"]["field_count"] == 3 and
        tag_struct["fields"] == committed_type_ev["types"]["Tag"]["fields"] == reproduced_type_ev["types"]["Tag"]["fields"]
    )
    config_match = (
        config_struct["size_bytes"] == committed_type_ev["types"]["DeviceTagsConfig"]["size_bytes"] == reproduced_type_ev["types"]["DeviceTagsConfig"]["size_bytes"] == 32 and
        config_struct["field_count"] == committed_type_ev["types"]["DeviceTagsConfig"]["field_count"] == reproduced_type_ev["types"]["DeviceTagsConfig"]["field_count"] == 2 and
        config_struct["fields"] == committed_type_ev["types"]["DeviceTagsConfig"]["fields"] == reproduced_type_ev["types"]["DeviceTagsConfig"]["fields"]
    )
    type_pass = tag_match and config_match
    print(f"[{'PASS' if type_pass else 'FAIL'}] TAG_TYPE_DESCRIPTOR_REPRODUCIBLE: {type_pass}")

    # 4. Static Binary Evidence / Route Identity Parity
    r_fam_committed = json.loads((DEFAULT_OUTPUT_DIR / "TAG_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    r_fam_reproduced = json.loads((temp_out / "TAG_ROUTE_FAMILY.json").read_text(encoding="utf-8"))
    route_match = (r_fam_committed["routes"] == r_fam_reproduced["routes"])
    print(f"[{'PASS' if route_match else 'FAIL'}] TAG_STATIC_BINARY_EVIDENCE_REPRODUCIBLE: {route_match}")

    # 5. Function Slice Reproduction Check
    f_sl_committed = json.loads((DEFAULT_OUTPUT_DIR / "TAG_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    f_sl_reproduced = json.loads((temp_out / "TAG_HTTP_FUNCTION_SLICES.json").read_text(encoding="utf-8"))
    slice_match = (f_sl_committed == f_sl_reproduced)
    print(f"[{'PASS' if slice_match else 'FAIL'}] TAG_FUNCTION_SLICE_REPRODUCIBLE: {slice_match}")

    # 6. Dynamic Invariant Checks (Field-Aware Normalization)
    committed_ops = json.loads((DEFAULT_OUTPUT_DIR / "TAG_OPERATION_CONTRACTS.json").read_text(encoding="utf-8"))
    reproduced_ops = json.loads((temp_out / "TAG_OPERATION_CONTRACTS.json").read_text(encoding="utf-8"))
    ops_match = (committed_ops == reproduced_ops)
    print(f"[{'PASS' if ops_match else 'FAIL'}] TAG_OPERATION_CONTRACTS_REPRODUCIBLE: {ops_match}")

    committed_persist = json.loads((DEFAULT_OUTPUT_DIR / "TAG_PERSISTENCE_CONTRACT.json").read_text(encoding="utf-8"))
    reproduced_persist = json.loads((temp_out / "TAG_PERSISTENCE_CONTRACT.json").read_text(encoding="utf-8"))
    persist_match = (
        committed_persist["file_name"] == reproduced_persist["file_name"] == "device_tags.json" and
        committed_persist["file_mode"] == reproduced_persist["file_mode"] == "0644" and
        committed_persist["write_mechanism"] == reproduced_persist["write_mechanism"] == "DIRECT_OS_WRITE_FILE" and
        committed_persist["atomic_tmp_rename"] == reproduced_persist["atomic_tmp_rename"] is False
    )
    print(f"[{'PASS' if persist_match else 'FAIL'}] TAG_PERSISTENCE_CONTRACT_REPRODUCIBLE: {persist_match}")

    committed_method = json.loads((DEFAULT_OUTPUT_DIR / "TAG_ROUTE_METHOD_MATRIX.json").read_text(encoding="utf-8"))
    reproduced_method = json.loads((temp_out / "TAG_ROUTE_METHOD_MATRIX.json").read_text(encoding="utf-8"))
    # Normalize volatile headers (e.g. Date)
    method_match = True
    for v in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
        c = committed_method["/api/tags"][v]
        r = reproduced_method["/api/tags"][v]
        if c["status"] != r["status"] or c["content_type"] != r["content_type"] or c["cors_origin"] != r["cors_origin"]:
            method_match = False
            break
    print(f"[{'PASS' if method_match else 'FAIL'}] TAG_METHOD_MATRIX_REPRODUCIBLE: {method_match}")

    committed_auth = json.loads((DEFAULT_OUTPUT_DIR / "TAG_AUTH_MATRIX.json").read_text(encoding="utf-8"))
    reproduced_auth = json.loads((temp_out / "TAG_AUTH_MATRIX.json").read_text(encoding="utf-8"))
    auth_match = (committed_auth == reproduced_auth)
    print(f"[{'PASS' if auth_match else 'FAIL'}] TAG_AUTH_MATRIX_REPRODUCIBLE: {auth_match}")

    # Cleanup temp
    shutil.rmtree(temp_out, ignore_errors=True)

    overall_pass = (type_pass and route_match and slice_match and ops_match and persist_match and method_match and auth_match)
    print("--------------------------------------------------")
    print(f"OVERALL REPRODUCIBILITY: {'PASS' if overall_pass else 'FAIL'}")
    print("==================================================")
    return overall_pass

if __name__ == "__main__":
    success = verify_tag_reproducibility()
    sys.exit(0 if success else 1)
