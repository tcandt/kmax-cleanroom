import sys
import os
import json
import hashlib
import tempfile
import difflib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.reference.extract_protocol_index import extract_protocol_index
from tools.reference.extract_datachannels import extract_datachannels
from tools.reference.extract_signaling_state_machine import extract_signaling_state_machine
from tools.reference.extract_agent_cli import extract_agent_cli
from tools.reference.generate_disassembly_facts import generate_disassembly_facts
from tools.reference.build_reference_crossmap import build_reference_crossmap

def compute_git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("utf-8")
    return hashlib.sha1(header + content).hexdigest()

def verify_reproducibility():
    print("==================================================")
    print("PHASE 2R.3 REFERENCE EVIDENCE REPRODUCIBILITY CHECK")
    print("==================================================")

    evidence_dir = REPO_ROOT / "evidence" / "reference"
    results = {}

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        print(f"[*] Regenerating reference artifacts into temp directory: {tmp_dir}")

        # 1. PUBLIC_GIT_INPUT_REPRODUCIBLE
        manifest_path = evidence_dir / "PUBLIC_REFERENCE_TREE_MANIFEST.json"
        git_input_pass = True
        git_detail = ""
        if not manifest_path.exists():
            git_input_pass = False
            git_detail = "PUBLIC_REFERENCE_TREE_MANIFEST.json missing"
        else:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            for entry in manifest.get("reference_sources", []):
                fp = REPO_ROOT / entry["materialized_path"]
                if not fp.exists():
                    git_input_pass = False
                    git_detail = f"Missing file {entry['materialized_path']}"
                    break
                data = fp.read_bytes()
                f_sha = hashlib.sha256(data).hexdigest()
                g_sha = compute_git_blob_sha(data)
                if f_sha != entry["sha256"]:
                    git_input_pass = False
                    git_detail = f"SHA256 mismatch for {entry['path']}: {f_sha[:10]} != {entry['sha256'][:10]}"
                    break
                if g_sha != entry["git_blob_sha"]:
                    git_input_pass = False
                    git_detail = f"Git blob SHA mismatch for {entry['path']}: {g_sha[:10]} != {entry['git_blob_sha'][:10]}"
                    break
        results["PUBLIC_GIT_INPUT_REPRODUCIBLE"] = git_input_pass
        print(f"[{'PASS' if git_input_pass else 'FAIL'}] PUBLIC_GIT_INPUT_REPRODUCIBLE: {git_detail if git_detail else 'All pinned git blobs and file hashes match'}")

        # 2. Execute evidence extractors targeting temp directory
        extract_protocol_index(tmp_path)
        extract_datachannels(tmp_path)
        extract_signaling_state_machine(tmp_path)
        extract_agent_cli(tmp_path)
        generate_disassembly_facts(tmp_path)
        build_reference_crossmap(tmp_path)

        # 3. SOURCE_MACHINE_EXTRACTION_REPRODUCIBLE
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
        results["SOURCE_MACHINE_EXTRACTION_REPRODUCIBLE"] = source_pass
        print(f"[{'PASS' if source_pass else 'FAIL'}] SOURCE_MACHINE_EXTRACTION_REPRODUCIBLE: {source_pass}")

        # 4. ANNOTATION_BINDINGS_VALID
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
        results["ANNOTATION_BINDINGS_VALID"] = ann_pass
        print(f"[{'PASS' if ann_pass else 'FAIL'}] ANNOTATION_BINDINGS_VALID: {ann_pass}")

        # 5. CLI_BINARY_EXTRACTION_REPRODUCIBLE
        cli_matrix_comm = (evidence_dir / "AGENT_CLI_REFERENCE_MATRIX.json").read_text(encoding="utf-8")
        cli_matrix_gen = (tmp_path / "AGENT_CLI_REFERENCE_MATRIX.json").read_text(encoding="utf-8")
        cli_ev_comm = (REPO_ROOT / "evidence/go_agent/cli/CLI_FLAG_REGISTRATION_EVIDENCE.json").read_text(encoding="utf-8")
        cli_ev_gen = (tmp_path / "cli/CLI_FLAG_REGISTRATION_EVIDENCE.json").read_text(encoding="utf-8")

        cli_binary_pass = (cli_matrix_comm == cli_matrix_gen and cli_ev_comm == cli_ev_gen)
        if not cli_binary_pass:
            if cli_matrix_comm != cli_matrix_gen:
                print(f"[FAIL] Discrepancy in AGENT_CLI_REFERENCE_MATRIX.json")
            if cli_ev_comm != cli_ev_gen:
                print(f"[FAIL] Discrepancy in CLI_FLAG_REGISTRATION_EVIDENCE.json")
        results["CLI_BINARY_EXTRACTION_REPRODUCIBLE"] = cli_binary_pass
        print(f"[{'PASS' if cli_binary_pass else 'FAIL'}] CLI_BINARY_EXTRACTION_REPRODUCIBLE: {cli_binary_pass}")

        # 6. DISASSEMBLY_FACTS_REPRODUCIBLE
        sig_facts_comm = (REPO_ROOT / "evidence/go_signaling/DISASSEMBLY_FACTS.json").read_text(encoding="utf-8")
        sig_facts_gen = (tmp_path / "go_signaling/DISASSEMBLY_FACTS.json").read_text(encoding="utf-8")
        agent_facts_comm = (REPO_ROOT / "evidence/go_agent/DISASSEMBLY_FACTS.json").read_text(encoding="utf-8")
        agent_facts_gen = (tmp_path / "go_agent/DISASSEMBLY_FACTS.json").read_text(encoding="utf-8")

        disasm_facts_pass = (sig_facts_comm == sig_facts_gen and agent_facts_comm == agent_facts_gen)
        if not disasm_facts_pass:
            print("[FAIL] Discrepancy in DISASSEMBLY_FACTS.json")
        results["DISASSEMBLY_FACTS_REPRODUCIBLE"] = disasm_facts_pass
        print(f"[{'PASS' if disasm_facts_pass else 'FAIL'}] DISASSEMBLY_FACTS_REPRODUCIBLE: {disasm_facts_pass}")

        # 7. CROSSMAP_EVIDENCE_RESOLUTION_PASS
        cm_comm = (evidence_dir / "REFERENCE_TO_BINARY_CROSSMAP.json").read_text(encoding="utf-8")
        cm_gen = (tmp_path / "REFERENCE_TO_BINARY_CROSSMAP.json").read_text(encoding="utf-8")
        crossmap_match = (cm_comm == cm_gen)
        
        # Verify resolution of every record in committed crossmap
        cm_data = json.loads(cm_comm)
        all_resolved = True
        for m in cm_data.get("mappings", []):
            for rec in m.get("evidence_records", []):
                art_p = REPO_ROOT / rec["artifact_path"]
                if not art_p.exists():
                    all_resolved = False
                    break
        crossmap_resolution_pass = crossmap_match and all_resolved
        results["CROSSMAP_EVIDENCE_RESOLUTION_PASS"] = crossmap_resolution_pass
        print(f"[{'PASS' if crossmap_resolution_pass else 'FAIL'}] CROSSMAP_EVIDENCE_RESOLUTION_PASS: {crossmap_resolution_pass}")

    all_matched = all(results.values())
    print("==================================================")
    print(f"REPRODUCIBILITY VERDICT: {'PASS' if all_matched else 'FAIL'}")
    print("==================================================")
    return all_matched

if __name__ == "__main__":
    passed = verify_reproducibility()
    sys.exit(0 if passed else 1)
