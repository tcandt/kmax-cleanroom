#!/usr/bin/env python3
"""
tools/forensics/reproduce_ai_command_forensics.py
Phase 2C.5B5FR AI Command Channel Forensic Reproducer.

Reproduces and validates the frozen AI command forensic interpretation against original
binary disassembly, derived semantic artifacts, effective contracts, and supporting evidence.

Modes:
  --check (default): Non-mutating verification. Regenerates disassembly and derived
                     forensic JSON in a temporary directory, asserts cryptographic match
                     against frozen canonical values, validates machine-binding invariants,
                     runs the shared semantic validator, and leaves repository untouched.
  --write:           Explicitly writes regenerated canonical artifacts to evidence/ directory.

Usage:
  python tools/forensics/reproduce_ai_command_forensics.py --check
  python tools/forensics/reproduce_ai_command_forensics.py --write
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS_AI = REPO_ROOT / "tools" / "forensics" / "ai_command"
EVIDENCE_DIR = REPO_ROOT / "evidence" / "go_agent" / "webrtc"

SPEC_PATH = EVIDENCE_DIR / "AI_COMMAND_B5F_PROTOCOL_SPEC.json"
INVENTORY_PATH = EVIDENCE_DIR / "AI_COMMAND_B5F_MESSAGE_INVENTORY.json"
CALLGRAPH_PATH = EVIDENCE_DIR / "AI_COMMAND_B5F_CALLGRAPH.json"
PROVENANCE_PATH = EVIDENCE_DIR / "AI_COMMAND_B5F_SOURCE_PROVENANCE.json"
CONTRACT_PATH = EVIDENCE_DIR / "AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json"
ERRATA_PATH = EVIDENCE_DIR / "AI_COMMAND_B5F_CONTRACT_ERRATA.json"
MANIFEST_PATH = TOOLS_AI / "ai_command_disassembly_manifest.json"

EXPECTED_SPEC_SHA = "aef2aac903e0fc1be312dc4c1bbf0e53eb5cb24c25ca373b06127c53fd36501f"
EXPECTED_INVENTORY_SHA = "3fa26da4d0c5474ea9592c3bb4e4abef180dd7d715030aa8cfa5917abcc3579b"
EXPECTED_CALLGRAPH_SHA = "331952995081030871416960df82ce4517f755cadfdb2e8fe9a50631babc9e15"
EXPECTED_PROVENANCE_SHA = "0bfedc7aff0661a951e4a9970a3d025812f65d2b6dfb1852e024fbb083661ccc"
EXPECTED_CONTRACT_SHA = "64642e153dcefaa2857fdc37f16b7dc076915c56aa1b3777519eb0c0d6dbdf65"
EXPECTED_MANIFEST_SHA = "a5e968b78ce9c73abdf43c170d2d6f561be8428cb55ee9397b109faafdaf2217"

ARM64_EXPECTED_SHA = "9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4"
AMD64_EXPECTED_SHA = "15adc2a4c47c4d189d4e8e08e960434bdd55202d74bc3eeee0bf4713a6b8de16"

sys.path.insert(0, str(REPO_ROOT))
from tools.forensics.ai_command.extract_ai_command_disassembly import (
    discover_llvm_objdump,
    verify_toolchain,
    extract_all,
    ARM64_BINARY,
    AMD64_BINARY
)
from tools.forensics.ai_command.derive_ai_command_protocol import derive_ai_command_artifacts
from tools.forensics.ai_command.validate_ai_command_semantics import validate_ai_command_semantics
from tools.audit.build_b5f_effective_contract import build_b5f_effective_contract, FROZEN_BASE_SHA256


def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().lower()


def validate_binary_invariants():
    # 1. Binary hashes
    arm_sha = hash_file(ARM64_BINARY)
    if arm_sha != ARM64_EXPECTED_SHA:
        raise ValueError(f"ARM64 binary SHA mismatch: got {arm_sha}, expected {ARM64_EXPECTED_SHA}")
    amd_sha = hash_file(AMD64_BINARY)
    if amd_sha != AMD64_EXPECTED_SHA:
        raise ValueError(f"AMD64 binary SHA mismatch: got {amd_sha}, expected {AMD64_EXPECTED_SHA}")

    # 2. Toolchain check
    disasm_path, _ = discover_llvm_objdump()
    v = verify_toolchain(disasm_path)
    if v["status"] not in ("SAME_CANONICAL_TOOLCHAIN", "DIFFERENT_VERIFIED_TOOLCHAIN"):
        raise ValueError(f"Toolchain verification failed: {v}")

    # 3. Read manifest and verify machine-bound invariants
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    arm_snippets = manifest["arm64_snippets"]
    amd_snippets = manifest["amd64_snippets"]

    # Invariant A: Inbound label check for "ai-command-channel" (18 bytes = 0x12)
    arm_label = arm_snippets["inbound_dispatch_label_check"]["disassembly"]
    assert "#0x12" in arm_label, "ARM64 label check missing length 0x12"
    assert "0x15440" in arm_label, "ARM64 label check missing runtime.memequal (0x15440)"
    amd_label = amd_snippets["inbound_dispatch_label_check"]["disassembly"]
    assert "$0x12" in amd_label, "AMD64 label check missing length 0x12"
    assert "0x406ce0" in amd_label, "AMD64 label check missing runtime.memequal (0x406ce0)"

    # Invariant B: Callback registration uses OnMessage only (no OnOpen/OnClose)
    arm_reg = arm_snippets["onmessage_callback_registration"]["disassembly"]
    assert "0x499770" in arm_reg, "ARM64 OnMessage call missing (0x499770)"
    amd_reg = amd_snippets["onmessage_callback_registration"]["disassembly"]
    assert "0x9244a0" in amd_reg, "AMD64 OnMessage call missing (0x9244a0)"

    # Invariant C: Unmarshal error logs and drops without response
    arm_unmarshal = arm_snippets["json_unmarshal_and_validation_branch"]["disassembly"]
    assert "0x12c600" in arm_unmarshal, "ARM64 json.Unmarshal missing (0x12c600)"
    assert "ret" in arm_unmarshal, "ARM64 error return missing"
    amd_unmarshal = amd_snippets["json_unmarshal_and_validation_branch"]["disassembly"]
    assert "0x52ba00" in amd_unmarshal, "AMD64 json.Unmarshal missing (0x52ba00)"
    assert "retq" in amd_unmarshal, "AMD64 error return missing"

    # Invariant D: Goroutine spawn via runtime.newproc
    arm_spawn = arm_snippets["goroutine_spawn_on_success"]["disassembly"]
    assert "0x5f730" in arm_spawn, "ARM64 runtime.newproc call missing (0x5f730)"
    amd_spawn = amd_snippets["goroutine_spawn_on_success"]["disassembly"]
    assert "0x451c40" in amd_spawn, "AMD64 runtime.newproc call missing (0x451c40)"

    # Invariant E: Downstream process execution boundary (exec.Command)
    arm_exec = arm_snippets["external_process_invocation"]["disassembly"]
    assert "0x196e70" in arm_exec, "ARM64 exec.Command call missing (0x196e70)"
    assert "0x197f00" in arm_exec, "ARM64 cmd.Run call missing (0x197f00)"
    amd_exec = amd_snippets["external_process_invocation"]["disassembly"]
    assert "0x5a1c00" in amd_exec, "AMD64 exec.Command call missing (0x5a1c00)"
    assert "0x5a2ea0" in amd_exec, "AMD64 cmd.Run call missing (0x5a2ea0)"

    # Invariant F: Response send method is (*DataChannel).Send ([]byte) - BINARY_JSON_BYTES
    arm_send = arm_snippets["response_construction_and_send"]["disassembly"]
    assert "0x49a3d0" in arm_send, "ARM64 (*DataChannel).Send missing (0x49a3d0)"
    assert "0x1317c0" in arm_send, "ARM64 json.Marshal missing (0x1317c0)"
    amd_send = amd_snippets["response_construction_and_send"]["disassembly"]
    assert "0x9250c0" in amd_send, "AMD64 (*DataChannel).Send missing (0x9250c0)"
    assert "0x531b60" in amd_send, "AMD64 json.Marshal missing (0x531b60)"

    # Invariant G: Shared semantic validator execution
    validate_ai_command_semantics(
        spec=SPEC_PATH,
        contract=CONTRACT_PATH,
        inventory=INVENTORY_PATH,
        callgraph=CALLGRAPH_PATH,
        provenance=PROVENANCE_PATH
    )


def run_check():
    print("=== Phase 2C.5B5FR AI-Command Channel Forensic Reproducer ===")
    print("Running in --check mode (non-mutating verification)...")

    # Step 1: Original binary and disassembly invariants
    validate_binary_invariants()
    print("✓ Original binary SHA256 and machine-bound disassembly invariants validated")

    # Step 2: Fresh disassembly extraction in tempdir
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_manifest = os.path.join(tmpdir, "ai_command_disassembly_manifest.json")
        extract_all(output_file=tmp_manifest)
        tmp_hash = hash_file(tmp_manifest)
        if tmp_hash != EXPECTED_MANIFEST_SHA:
            raise ValueError(f"Regenerated manifest SHA mismatch: got {tmp_hash}, expected {EXPECTED_MANIFEST_SHA}")
        print("✓ Fresh disassembly cleanly extracted in tempdir and matches frozen SHA")

        # Step 3: Fresh derived forensic JSON from manifest in tempdir
        tmp_derived_dir = os.path.join(tmpdir, "derived")
        derived_artifacts = derive_ai_command_artifacts(
            manifest_path=Path(tmp_manifest),
            output_dir=Path(tmp_derived_dir)
        )
        for fname in ["AI_COMMAND_B5F_PROTOCOL_SPEC.json", "AI_COMMAND_B5F_MESSAGE_INVENTORY.json", "AI_COMMAND_B5F_CALLGRAPH.json", "AI_COMMAND_B5F_SOURCE_PROVENANCE.json"]:
            fresh_bytes = (Path(tmp_derived_dir) / fname).read_bytes()
            canon_bytes = (EVIDENCE_DIR / fname).read_bytes()
            if fresh_bytes != canon_bytes:
                raise ValueError(f"Freshly derived {fname} bytes differ from canonical baseline")
        print("✓ Semantic forensic artifacts deterministically re-derived and byte-match canonical baseline")

    # Step 4: Fresh effective interpretation via errata layer
    eff = build_b5f_effective_contract(REPO_ROOT)
    tc = eff["metadata"]["taxonomy_counts"]
    assert tc["original_static_evidence"] == 9, f"Expected 9 original static evidence, got {tc['original_static_evidence']}"
    assert tc["cross_component_evidence"] == 0, f"Expected 0 cross component evidence, got {tc['cross_component_evidence']}"
    assert tc["safe_scope_guard"] == 2, f"Expected 2 safe scope guards, got {tc['safe_scope_guard']}"
    assert tc["reference_interoperability"] == 2, f"Expected 2 reference interop, got {tc['reference_interoperability']}"
    assert tc["defensive_validation"] == 1, f"Expected 1 defensive validation, got {tc['defensive_validation']}"
    assert tc["deferred_execution_boundary"] == 1, f"Expected 1 deferred boundary, got {tc['deferred_execution_boundary']}"
    assert tc["audit_provenance_guard"] == 1, f"Expected 1 audit provenance guard, got {tc['audit_provenance_guard']}"
    assert tc["unknown"] == 0, f"Expected 0 unknown, got {tc['unknown']}"
    print("✓ Effective contract view built: 9 static, 2 safe scope, 2 reference interop, 1 defensive, 1 deferred, 1 audit provenance, 0 unknown")

    # Step 5: Canonical semantic comparison via shared validator
    sem_res = validate_ai_command_semantics(
        spec=SPEC_PATH,
        contract=CONTRACT_PATH,
        inventory=INVENTORY_PATH,
        callgraph=CALLGRAPH_PATH,
        provenance=PROVENANCE_PATH
    )
    print("✓ Shared semantic validator executed against canonical artifacts (PASS)")

    # Step 6: Frozen SHA verification
    spec_sha = hash_file(SPEC_PATH)
    inv_sha = hash_file(INVENTORY_PATH)
    cg_sha = hash_file(CALLGRAPH_PATH)
    prov_sha = hash_file(PROVENANCE_PATH)
    contract_sha = hash_file(CONTRACT_PATH)
    manifest_sha = hash_file(MANIFEST_PATH)

    assert spec_sha == EXPECTED_SPEC_SHA, f"Protocol spec SHA mismatch: {spec_sha} != {EXPECTED_SPEC_SHA}"
    assert inv_sha == EXPECTED_INVENTORY_SHA, f"Message inventory SHA mismatch: {inv_sha} != {EXPECTED_INVENTORY_SHA}"
    assert cg_sha == EXPECTED_CALLGRAPH_SHA, f"Callgraph SHA mismatch: {cg_sha} != {EXPECTED_CALLGRAPH_SHA}"
    assert prov_sha == EXPECTED_PROVENANCE_SHA, f"Provenance SHA mismatch: {prov_sha} != {EXPECTED_PROVENANCE_SHA}"
    assert contract_sha == EXPECTED_CONTRACT_SHA, f"Contract SHA mismatch: {contract_sha} != {EXPECTED_CONTRACT_SHA}"
    assert manifest_sha == EXPECTED_MANIFEST_SHA, f"Manifest SHA mismatch: {manifest_sha} != {EXPECTED_MANIFEST_SHA}"

    print(f"✓ AI_COMMAND_B5F_PROTOCOL_SPEC.json:         {spec_sha} (MATCH)")
    print(f"✓ AI_COMMAND_B5F_MESSAGE_INVENTORY.json:     {inv_sha} (MATCH)")
    print(f"✓ AI_COMMAND_B5F_CALLGRAPH.json:             {cg_sha} (MATCH)")
    print(f"✓ AI_COMMAND_B5F_SOURCE_PROVENANCE.json:     {prov_sha} (MATCH)")
    print(f"✓ AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json: {contract_sha} (MATCH)")
    print(f"✓ ai_command_disassembly_manifest.json:      {manifest_sha} (MATCH)")
    print("All B5F forensic reproduction checks PASSED.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 2C.5B5F AI Command Forensic Reproducer")
    parser.add_argument("--check", action="store_true", default=True, help="Validate without modifying working tree")
    parser.add_argument("--write", action="store_true", help="Regenerate artifacts directly into evidence directory")
    args = parser.parse_args()

    if args.write:
        print("Writing regenerated manifest and derived artifacts...")
        extract_all(output_file=str(MANIFEST_PATH))
        derive_ai_command_artifacts(manifest_path=MANIFEST_PATH, output_dir=EVIDENCE_DIR)
        print("Done.")
    else:
        run_check()
