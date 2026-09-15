import sys
import os
import json
import hashlib
import tempfile
import difflib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.reference.extract_protocol_index import extract_protocol_index, generate_protocol_index
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
    print("PHASE 2R.2 REFERENCE EVIDENCE REPRODUCIBILITY CHECK")
    print("==================================================")

    evidence_dir = REPO_ROOT / "evidence" / "reference"
    results = {}

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        print(f"[*] Regenerating reference artifacts into temp directory: {tmp_dir}")

        # 1. Execute evidence extractors targeting temp directory
        extract_protocol_index(tmp_path)
        extract_datachannels(tmp_path)
        extract_signaling_state_machine(tmp_path)
        extract_agent_cli(tmp_path)
        build_reference_crossmap(tmp_path)

        # 2. Check SOURCE_EXTRACTION_REPRODUCIBLE
        # Target files: REFERENCE_PROTOCOL_INDEX.json, DATACHANNEL_REFERENCE_MATRIX.json, CLIENT_SIGNALING_STATE_MACHINE.json
        source_files = [
            "REFERENCE_PROTOCOL_INDEX.json",
            "DATACHANNEL_REFERENCE_MATRIX.json",
            "CLIENT_SIGNALING_STATE_MACHINE.json"
        ]
        source_pass = True
        for sf in source_files:
            committed_file = evidence_dir / sf
            generated_file = tmp_path / sf
            if not committed_file.exists() or not generated_file.exists():
                source_pass = False
                break
            comm_text = committed_file.read_text(encoding="utf-8")
            gen_text = generated_file.read_text(encoding="utf-8")
            if comm_text != gen_text:
                source_pass = False
                print(f"[FAIL] Discrepancy in source extraction artifact {sf}")
                diff = list(difflib.unified_diff(comm_text.splitlines(), gen_text.splitlines(), n=3))
                for line in diff[:15]:
                    print("  " + line)
                break
        results["SOURCE_EXTRACTION_REPRODUCIBLE"] = source_pass
        print(f"[{'PASS' if source_pass else 'FAIL'}] SOURCE_EXTRACTION_REPRODUCIBLE: {source_pass}")

        # 3. Check BINARY_EVIDENCE_REPRODUCIBLE
        # Target file: AGENT_CLI_REFERENCE_MATRIX.json
        cli_comm = (evidence_dir / "AGENT_CLI_REFERENCE_MATRIX.json").read_text(encoding="utf-8")
        cli_gen = (tmp_path / "AGENT_CLI_REFERENCE_MATRIX.json").read_text(encoding="utf-8")
        binary_pass = (cli_comm == cli_gen)
        if not binary_pass:
            print(f"[FAIL] Discrepancy in AGENT_CLI_REFERENCE_MATRIX.json")
        results["BINARY_EVIDENCE_REPRODUCIBLE"] = binary_pass
        print(f"[{'PASS' if binary_pass else 'FAIL'}] BINARY_EVIDENCE_REPRODUCIBLE: {binary_pass}")

        # 4. Check ANNOTATION_STABLE
        # Verify REFERENCE_ANNOTATIONS.json against pinned raw files
        ann_path = evidence_dir / "REFERENCE_ANNOTATIONS.json"
        ann_pass = True
        if not ann_path.exists():
            ann_pass = False
        else:
            with open(ann_path, "r", encoding="utf-8") as f:
                ann_data = json.load(f)
            annotations = ann_data.get("annotations", [])
            for ann in annotations:
                src_rel = ann["source_file"]
                src_full = evidence_dir / "raw" / src_rel
                if not src_full.exists():
                    ann_pass = False
                    print(f"[FAIL] Annotation source missing: {src_full}")
                    break
                lines = src_full.read_text(encoding="utf-8", errors="ignore").splitlines()
                l_start = ann["line_start"] - 1
                l_end = ann["line_end"]
                slice_text = "\n".join(lines[l_start:l_end])
                slice_hash = hashlib.sha256(slice_text.encode("utf-8")).hexdigest()
                if slice_hash != ann["observed_text_hash"]:
                    ann_pass = False
                    print(f"[FAIL] Annotation hash mismatch for {ann['annotation_id']}: {slice_hash[:12]} != {ann['observed_text_hash'][:12]}")
                    break
        results["ANNOTATION_STABLE"] = ann_pass
        print(f"[{'PASS' if ann_pass else 'FAIL'}] ANNOTATION_STABLE: {ann_pass}")

        # 5. Check CROSSMAP_REPRODUCIBLE
        # Target file: REFERENCE_TO_BINARY_CROSSMAP.json
        cm_comm = (evidence_dir / "REFERENCE_TO_BINARY_CROSSMAP.json").read_text(encoding="utf-8")
        cm_gen = (tmp_path / "REFERENCE_TO_BINARY_CROSSMAP.json").read_text(encoding="utf-8")
        cm_pass = (cm_comm == cm_gen)
        if not cm_pass:
            print(f"[FAIL] Discrepancy in REFERENCE_TO_BINARY_CROSSMAP.json")
            diff = list(difflib.unified_diff(cm_comm.splitlines(), cm_gen.splitlines(), n=3))
            for line in diff[:20]:
                print("  " + line)
        results["CROSSMAP_REPRODUCIBLE"] = cm_pass
        print(f"[{'PASS' if cm_pass else 'FAIL'}] CROSSMAP_REPRODUCIBLE: {cm_pass}")

    all_matched = all(results.values())
    print("==================================================")
    print(f"REPRODUCIBILITY VERDICT: {'PASS' if all_matched else 'FAIL'}")
    print("==================================================")
    return all_matched

if __name__ == "__main__":
    passed = verify_reproducibility()
    sys.exit(0 if passed else 1)
