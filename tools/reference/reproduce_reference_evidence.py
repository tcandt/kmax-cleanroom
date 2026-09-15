import sys
import os
import json
import tempfile
import difflib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.reference.extract_protocol_index import generate_protocol_index
from tools.reference.extract_datachannels import extract_datachannels
from tools.reference.extract_signaling_state_machine import extract_signaling_state_machine
from tools.reference.extract_agent_cli import extract_agent_cli
from tools.reference.build_reference_crossmap import build_reference_crossmap

TARGET_FILES = [
    "REFERENCE_PROTOCOL_INDEX.json",
    "DATACHANNEL_REFERENCE_MATRIX.json",
    "CLIENT_SIGNALING_STATE_MACHINE.json",
    "AGENT_CLI_REFERENCE_MATRIX.json",
    "REFERENCE_TO_BINARY_CROSSMAP.json"
]

def canonical_json_dump(obj):
    return json.dumps(obj, indent=2, sort_keys=False)

def verify_reproducibility():
    print("==================================================")
    print("PHASE 2R.1 REFERENCE EVIDENCE REPRODUCIBILITY CHECK")
    print("==================================================")

    evidence_dir = REPO_ROOT / "evidence" / "reference"
    all_matched = True

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        print(f"[*] Regenerating reference artifacts into temp directory: {tmp_dir}")

        # Run all generators targeting temp directory
        generate_protocol_index(tmp_path)
        extract_datachannels(tmp_path)
        extract_signaling_state_machine(tmp_path)
        extract_agent_cli(tmp_path)
        build_reference_crossmap(tmp_path)

        for filename in TARGET_FILES:
            committed_file = evidence_dir / filename
            generated_file = tmp_path / filename

            if not committed_file.exists():
                print(f"[FAIL] Committed file missing: {committed_file}")
                all_matched = False
                continue

            if not generated_file.exists():
                print(f"[FAIL] Generator failed to produce: {filename}")
                all_matched = False
                continue

            with open(committed_file, "r", encoding="utf-8") as f:
                committed_data = json.load(f)
            with open(generated_file, "r", encoding="utf-8") as f:
                generated_data = json.load(f)

            committed_str = canonical_json_dump(committed_data)
            generated_str = canonical_json_dump(generated_data)

            if committed_str == generated_str:
                print(f"[PASS] {filename:<40} (Bit/Key Exact Match)")
            else:
                diff = list(difflib.unified_diff(
                    committed_str.splitlines(),
                    generated_str.splitlines(),
                    fromfile="committed",
                    tofile="generated",
                    n=3
                ))
                print(f"[FAIL] Discrepancy found in {filename}:")
                for line in diff[:20]:
                    print("  " + line)
                all_matched = False

    print("==================================================")
    print(f"REPRODUCIBILITY VERDICT: {'PASS' if all_matched else 'FAIL'}")
    print("==================================================")
    return all_matched

if __name__ == "__main__":
    passed = verify_reproducibility()
    sys.exit(0 if passed else 1)
