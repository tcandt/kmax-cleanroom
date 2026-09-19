#!/usr/bin/env python3
"""
tools/forensics/reproduce_adb_channel_forensics.py

Independent forensic reproducer for Phase 2C.5B6F adb-channel.
Extracts fresh disassembly, compiles intermediate fact model, deterministically re-derives
semantic artifacts, and verifies byte-for-byte equality against canonical baselines in temp.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.adb_channel.extract_adb_channel_disassembly import extract_manifest, ARM64_BINARY, AMD64_BINARY
from tools.forensics.adb_channel.derive_adb_channel_protocol import derive_adb_channel_artifacts
from tools.forensics.adb_channel.validate_adb_channel_semantics import validate_adb_channel_semantics

EVID_DIR = REPO_ROOT / "evidence" / "go_agent" / "webrtc"

EXPECTED_BINARY_HASHES = {
    "arm64": "9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4",
    "amd64": "15adc2a4c47c4d189d4e8e08e960434bdd55202d74bc3eeee0bf4713a6b8de16"
}

FROZEN_CANONICAL_HASHES = {
    "ADB_CHANNEL_B6F_PROTOCOL_SPEC.json": "fc9e91c19d660030212db8d3dc2ddca34d0b6c22624f6ae59fd4482767267303",
    "ADB_CHANNEL_B6F_TOPOLOGY.json": "2210779398554f40a4cedc956a19e89cf5592087f8ec2601eced1e00a541d7ee",
    "ADB_CHANNEL_B6F_MESSAGE_FRAMING.json": "67dec1f8db5a6553893c98e70480a3fbc1f546b8e3f29abf90d3b026738cce18",
    "ADB_CHANNEL_B6F_CALLGRAPH.json": "53a22f4e251e18072fb0ebe32d985f11553f3c72130157565c36e439ebeef412",
    "ADB_CHANNEL_B6F_SOURCE_PROVENANCE.json": "9c8ef88aa6689d42df7cec191e29a22a6dc115ec2411e3cfa31ecbd40e6823fd",
    "ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json": "1b1aba53ef39786fadafaab772e11c0611198403f8910f951a507ff4b06fc3ea",
    "ADB_CHANNEL_B6F_CONTRACT_ERRATA.json": "20f6288bb4d2ab1b3c687d7cbbcb58432268806de8af9c32fd847ad37925cdde",
    "adb_channel_disassembly_manifest.json": "8c170b6b881dbf19709079cd03de677adcc803f366e365d7ac8a72e688caf334"
}


def compute_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def reproduce_adb_channel_forensics(check_mode: bool = False):
    print("=== Phase 2C.5B6F ADB-Channel Forensic Reproducer ===")
    if check_mode:
        print("Running in --check mode (non-mutating verification)...")

    # 1. Validate Original Binary Hashes
    arm_sha = compute_sha256(Path(ARM64_BINARY))
    amd_sha = compute_sha256(Path(AMD64_BINARY))
    assert arm_sha == EXPECTED_BINARY_HASHES["arm64"], f"ARM64 binary SHA mismatch: {arm_sha}"
    assert amd_sha == EXPECTED_BINARY_HASHES["amd64"], f"AMD64 binary SHA mismatch: {amd_sha}"
    print("[PASS] Original binary SHA256 and machine-bound disassembly invariants validated")

    with tempfile.TemporaryDirectory() as td:
        t_dir = Path(td)
        t_manifest = t_dir / "adb_channel_disassembly_manifest.json"
        t_derived = t_dir / "derived"

        # 2. Fresh Disassembly Extraction into Temp
        extract_manifest(output_path=str(t_manifest))
        t_data = json.loads(t_manifest.read_text(encoding="utf-8"))
        c_data = json.loads((EVID_DIR / "adb_channel_disassembly_manifest.json").read_text(encoding="utf-8"))

        t_tc = t_data.get("toolchain", {}).get("canonical_disassembler_identity", t_data.get("toolchain", {}))
        c_tc = c_data.get("toolchain", {}).get("canonical_disassembler_identity", c_data.get("toolchain", {}))
        assert t_tc.get("sha256") == c_tc.get("sha256"), f"Disassembler SHA mismatch: {t_tc.get('sha256')} != {c_tc.get('sha256')}"
        assert t_data.get("binaries") == c_data.get("binaries"), "Disassembly snippets mismatch against canonical baseline!"
        print("[PASS] Fresh disassembly cleanly extracted in tempdir and matches canonical snippets & toolchain SHA")

        # 3. Independent Protocol Derivation in Temp
        derived = derive_adb_channel_artifacts(output_dir=str(t_derived))

        # 4. Byte-for-byte Comparison against Canonical Baselines
        for fname in derived.keys():
            t_file = t_derived / fname
            c_file = EVID_DIR / fname
            assert c_file.exists(), f"Canonical baseline missing: {c_file}"
            t_bytes = t_file.read_bytes()
            c_bytes = c_file.read_bytes()
            if t_bytes != c_bytes:
                raise AssertionError(f"Artifact '{fname}' byte mismatch against canonical baseline!")

        print("[PASS] Semantic forensic artifacts deterministically re-derived and byte-match canonical baseline")

        # 5. Execute Semantic Validator on Derived Artifacts
        val_res = validate_adb_channel_semantics(
            spec=t_derived / "ADB_CHANNEL_B6F_PROTOCOL_SPEC.json",
            topology=t_derived / "ADB_CHANNEL_B6F_TOPOLOGY.json",
            framing=t_derived / "ADB_CHANNEL_B6F_MESSAGE_FRAMING.json",
            callgraph=t_derived / "ADB_CHANNEL_B6F_CALLGRAPH.json",
            provenance=t_derived / "ADB_CHANNEL_B6F_SOURCE_PROVENANCE.json",
            contract=t_derived / "ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json",
            errata=EVID_DIR / "ADB_CHANNEL_B6F_CONTRACT_ERRATA.json"
        )
        assert val_res["status"] == "VALID"
        print("[PASS] Shared semantic validator executed against freshly derived artifacts")

    # 6. Verify Canonical Baseline Hashes on Disk
    for fname, exp_sha in FROZEN_CANONICAL_HASHES.items():
        actual_sha = compute_sha256(EVID_DIR / fname)
        assert actual_sha == exp_sha, f"Frozen hash mismatch for {fname}: got {actual_sha}, expected {exp_sha}"
        print(f"[PASS] {fname:44} {actual_sha} (MATCH)")

    print("All B6F forensic reproduction checks PASSED.")


def main():
    parser = argparse.ArgumentParser(description="Reproduce B6F adb-channel forensics")
    parser.add_argument("--check", action="store_true", help="Non-mutating verification mode")
    args = parser.parse_args()
    reproduce_adb_channel_forensics(check_mode=args.check)


if __name__ == "__main__":
    main()
