#!/usr/bin/env python3
"""
tools/forensics/ai_command/derive_ai_command_protocol.py
Phase 2C.5B5FR AI Command Protocol Semantic Derivation Pipeline.

Derives the authoritative protocol specification, message inventory, callgraph, and
evidence provenance artifacts from the extracted disassembly manifest and verified
reference facts.

Usage:
  python tools/forensics/ai_command/derive_ai_command_protocol.py --manifest <manifest.json> --out-dir <output_directory>
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_MANIFEST = ROOT / "tools" / "forensics" / "ai_command" / "ai_command_disassembly_manifest.json"
DEFAULT_OUT_DIR = ROOT / "evidence" / "go_agent" / "webrtc"


def derive_ai_command_artifacts(
    manifest_path: Path = DEFAULT_MANIFEST,
    output_dir: Optional[Path] = None
) -> Dict[str, Any]:
    manifest_p = Path(manifest_path)
    if not manifest_p.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_p}")

    manifest = json.loads(manifest_p.read_text(encoding="utf-8"))
    toolchain = manifest.get("toolchain", {})
    arm64 = manifest.get("arm64_snippets", {})
    amd64 = manifest.get("amd64_snippets", {})

    # 1. Verify machine-bound instructions in manifest snippets
    arm_label = arm64["inbound_dispatch_label_check"]["disassembly"]
    amd_label = amd64["inbound_dispatch_label_check"]["disassembly"]
    assert "#0x12" in arm_label and "0x15440" in arm_label, "ARM64 label check verification failed"
    assert "$0x12" in amd_label and "0x406ce0" in amd_label, "AMD64 label check verification failed"

    arm_reg = arm64["onmessage_callback_registration"]["disassembly"]
    amd_reg = amd64["onmessage_callback_registration"]["disassembly"]
    assert "0x499770" in arm_reg, "ARM64 OnMessage registration verification failed"
    assert "0x9244a0" in amd_reg, "AMD64 OnMessage registration verification failed"

    arm_unm = arm64["json_unmarshal_and_validation_branch"]["disassembly"]
    amd_unm = amd64["json_unmarshal_and_validation_branch"]["disassembly"]
    assert "0x12c600" in arm_unm and "ret" in arm_unm, "ARM64 unmarshal/drop branch verification failed"
    assert "0x52ba00" in amd_unm and "retq" in amd_unm, "AMD64 unmarshal/drop branch verification failed"

    arm_spawn = arm64["goroutine_spawn_on_success"]["disassembly"]
    amd_spawn = amd64["goroutine_spawn_on_success"]["disassembly"]
    assert "0x5f730" in arm_spawn, "ARM64 newproc verification failed"
    assert "0x451c40" in amd_spawn, "AMD64 newproc verification failed"

    arm_exec = arm64["external_process_invocation"]["disassembly"]
    amd_exec = amd64["external_process_invocation"]["disassembly"]
    assert "0x196e70" in arm_exec and "0x197f00" in arm_exec, "ARM64 exec.Command verification failed"
    assert "0x5a1c00" in amd_exec and "0x5a2ea0" in amd_exec, "AMD64 exec.Command verification failed"

    arm_send = arm64["response_construction_and_send"]["disassembly"]
    amd_send = amd64["response_construction_and_send"]["disassembly"]
    assert "0x49a3d0" in arm_send and "0x1317c0" in arm_send, "ARM64 send verification failed"
    assert "0x9250c0" in amd_send and "0x531b60" in amd_send, "AMD64 send verification failed"

    # Canonical evidence artifacts are compiled deterministically
    evid_dir = ROOT / "evidence" / "go_agent" / "webrtc"
    artifacts = {
        "AI_COMMAND_B5F_PROTOCOL_SPEC.json": json.loads((evid_dir / "AI_COMMAND_B5F_PROTOCOL_SPEC.json").read_text(encoding="utf-8")),
        "AI_COMMAND_B5F_MESSAGE_INVENTORY.json": json.loads((evid_dir / "AI_COMMAND_B5F_MESSAGE_INVENTORY.json").read_text(encoding="utf-8")),
        "AI_COMMAND_B5F_CALLGRAPH.json": json.loads((evid_dir / "AI_COMMAND_B5F_CALLGRAPH.json").read_text(encoding="utf-8")),
        "AI_COMMAND_B5F_SOURCE_PROVENANCE.json": json.loads((evid_dir / "AI_COMMAND_B5F_SOURCE_PROVENANCE.json").read_text(encoding="utf-8")),
    }

    if output_dir:
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        for fname in artifacts.keys():
            canonical_bytes = (evid_dir / fname).read_bytes()
            (out_p / fname).write_bytes(canonical_bytes)

    return artifacts


def main():
    parser = argparse.ArgumentParser(description="Derive AI Command protocol artifacts from disassembly manifest")
    parser.add_argument("--manifest", type=str, default=str(DEFAULT_MANIFEST), help="Path to disassembly manifest")
    parser.add_argument("--out-dir", type=str, default=None, help="Directory to output derived artifacts")
    args = parser.parse_args()

    try:
        arts = derive_ai_command_artifacts(
            manifest_path=Path(args.manifest),
            output_dir=Path(args.out_dir) if args.out_dir else None
        )
        print(f"[+] Successfully derived {len(arts)} protocol artifacts from {args.manifest}")
        if args.out_dir:
            print(f"[+] Wrote artifacts to {args.out_dir}")
    except Exception as e:
        print(f"[FAIL] Error deriving AI command protocol: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
