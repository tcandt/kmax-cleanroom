#!/usr/bin/env python3
"""
tools/audit/validate_phase3_cross_phase_matrix.py

Deep semantic validator for evidence/final/PHASE3_CROSS_PHASE_FACT_MATRIX.json.
Validates all authoritative fields against frozen canonical contracts and errata.
Fails closed on any fact inversion, incorrect endpoint, unauthorized framing,
or missing channel.
"""

import os
import sys
import json
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def validate_matrix(matrix_path=None, repo_root=REPO_ROOT):
    if matrix_path is None:
        matrix_path = repo_root / "evidence" / "final" / "PHASE3_CROSS_PHASE_FACT_MATRIX.json"
    else:
        matrix_path = Path(matrix_path)

    if not matrix_path.exists():
        print(f"[FAIL] Matrix file not found: {matrix_path}")
        return False

    try:
        data = json.loads(matrix_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[FAIL] Invalid JSON in matrix: {e}")
        return False

    channels = data.get("datachannel_reconciliation_summary", {})
    if len(channels) != 6:
        print(f"[FAIL] Expected 6 DataChannels, found {len(channels)}")
        return False

    required_channels = [
        "input-channel",
        "clipboard-channel",
        "file-channel",
        "camera-channel",
        "ai-command-channel",
        "adb-channel"
    ]

    for rc in required_channels:
        if rc not in channels:
            print(f"[FAIL] Missing required channel in matrix: {rc}")
            return False

    # 1. Validate input-channel
    inp = channels["input-channel"]
    if inp.get("creator") != "Agent":
        print(f"[FAIL] input-channel creator must be Agent, got {inp.get('creator')}")
        return False
    if inp.get("remote_peer") != "Browser Client":
        print(f"[FAIL] input-channel remote_peer must be Browser Client")
        return False
    if inp.get("request_framing") != "JSON_TEXT":
        print(f"[FAIL] input-channel request_framing must be JSON_TEXT")
        return False
    if inp.get("response_framing") != "NONE":
        print(f"[FAIL] input-channel response_framing must be NONE")
        return False
    if "@uds_sys_t_" not in inp.get("downstream", ""):
        print(f"[FAIL] input-channel downstream must target @uds_sys_t_")
        return False

    # 2. Validate clipboard-channel
    clip = channels["clipboard-channel"]
    if clip.get("creator") != "Agent":
        print(f"[FAIL] clipboard-channel creator must be Agent, got {clip.get('creator')}")
        return False
    if clip.get("request_framing") != "JSON_TEXT" or clip.get("response_framing") != "JSON_TEXT":
        print(f"[FAIL] clipboard-channel framing must be bidirectional JSON_TEXT")
        return False

    # 3. Validate file-channel
    fc = channels["file-channel"]
    if fc.get("creator") != "Browser Client":
        print(f"[FAIL] file-channel creator must be Browser Client, got {fc.get('creator')}")
        return False
    if fc.get("consumer") != "Agent":
        print(f"[FAIL] file-channel consumer must be Agent, got {fc.get('consumer')}")
        return False
    if fc.get("ordered_evidence_class") != "REFERENCE_INTEROPERABILITY":
        print(f"[FAIL] file-channel ordered_evidence_class must be REFERENCE_INTEROPERABILITY")
        return False
    if fc.get("response_framing") != "NOT_RECOVERED":
        print(f"[FAIL] file-channel response_framing must be NOT_RECOVERED, got {fc.get('response_framing')}")
        return False
    if fc.get("response_evidence") != "NO_CANONICAL_EGRESS_EVIDENCE":
        print(f"[FAIL] file-channel response_evidence must be NO_CANONICAL_EGRESS_EVIDENCE")
        return False

    # 4. Validate camera-channel
    cam = channels["camera-channel"]
    if cam.get("creator") != "Agent":
        print(f"[FAIL] camera-channel creator must be Agent, got {cam.get('creator')}")
        return False
    if cam.get("consumer") != "Browser Client":
        print(f"[FAIL] camera-channel consumer must be Browser Client, got {cam.get('consumer')}")
        return False
    if cam.get("request_framing") != "JSON_TEXT":
        print(f"[FAIL] camera-channel agent-to-browser framing must be JSON_TEXT")
        return False
    if cam.get("response_framing") != "RAW_BINARY":
        print(f"[FAIL] camera-channel browser-to-agent framing must be RAW_BINARY")
        return False
    if "127.0.0.1:9001" not in cam.get("downstream", ""):
        print(f"[FAIL] camera-channel downstream must target 127.0.0.1:9001")
        return False
    if "8089" in cam.get("downstream", "") or "8089" in cam.get("reconciliation_notes", ""):
        print(f"[FAIL] camera-channel contains deprecated/erroneous port 8089")
        return False
    if "4-byte little-endian" not in cam.get("downstream_protocol_framing", ""):
        print(f"[FAIL] camera-channel downstream_protocol_framing must specify 4-byte LE prefix")
        return False

    # 5. Validate ai-command-channel
    ai = channels["ai-command-channel"]
    if ai.get("creator") != "Browser Client":
        print(f"[FAIL] ai-command-channel creator must be Browser Client, got {ai.get('creator')}")
        return False
    if ai.get("consumer") != "Agent":
        print(f"[FAIL] ai-command-channel consumer must be Agent, got {ai.get('consumer')}")
        return False
    if ai.get("request_framing") != "JSON_TEXT":
        print(f"[FAIL] ai-command-channel request_framing must be JSON_TEXT")
        return False
    if ai.get("response_framing") != "BINARY_JSON_BYTES":
        print(f"[FAIL] ai-command-channel response_framing must be BINARY_JSON_BYTES")
        return False
    if "AI-B5F-10" not in ai.get("deferred_boundary", ""):
        print(f"[FAIL] ai-command-channel deferred_boundary must reference AI-B5F-10")
        return False

    # 6. Validate adb-channel
    adb = channels["adb-channel"]
    if adb.get("creator") != "Browser Client":
        print(f"[FAIL] adb-channel creator must be Browser Client, got {adb.get('creator')}")
        return False
    if adb.get("consumer") != "Agent":
        print(f"[FAIL] adb-channel consumer must be Agent, got {adb.get('consumer')}")
        return False
    if adb.get("ordered_evidence_class") != "REFERENCE_INTEROPERABILITY":
        print(f"[FAIL] adb-channel ordered_evidence_class must be REFERENCE_INTEROPERABILITY")
        return False
    if adb.get("deferred_boundary") != "ADB-B6F-11":
        print(f"[FAIL] adb-channel deferred_boundary must be ADB-B6F-11, got {adb.get('deferred_boundary')}")
        return False
    if "ADB-B6F-08" not in adb.get("downstream", ""):
        print(f"[FAIL] adb-channel downstream must reference absence finding ADB-B6F-08")
        return False

    # 7. Subsystem records
    subsystems = data.get("subsystem_reconciliation_records", [])
    if len(subsystems) < 10:
        print(f"[FAIL] Expected at least 10 subsystem reconciliation records, found {len(subsystems)}")
        return False

    print(f"[PASS] Cross-Phase Fact Matrix deep semantic validation PASSED ({len(channels)} channels, {len(subsystems)} subsystems)")
    return True

def main():
    parser = argparse.ArgumentParser(description="Validate Phase 3 Cross-Phase Fact Matrix")
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Path to repository root")
    parser.add_argument("--matrix-file", default=None, help="Explicit matrix file path")
    parser.add_argument("--check", action="store_true", help="Verification mode")
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    success = validate_matrix(matrix_path=args.matrix_file, repo_root=repo_root)
    if not success:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
