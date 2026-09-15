import os
import sys
import json
import shutil
import hashlib
from pathlib import Path

# Portable repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root

ROOT = get_repo_root()

def canonical_json_hash(filepath: Path) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    norm = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()

def reproduce_all():
    print("==================================================")
    print("PHASE 2 REPRODUCIBILITY AUDIT")
    print("==================================================")

    temp_dir = ROOT / "tmp" / "reproduce_phase2_workspace"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    ev_sig_temp = temp_dir / "go_signaling"
    ev_agent_temp = temp_dir / "go_agent"
    ev_sig_temp.mkdir(parents=True)
    ev_agent_temp.mkdir(parents=True)

    committed_sig = ROOT / "evidence" / "go_signaling"
    committed_agent = ROOT / "evidence" / "go_agent"

    # 1. Regenerate Function Maps and Callgraphs
    print("[1/4] Regenerating FUNCTION_MAP and CALLGRAPH into isolated workspace...")
    from tools.forensics.regenerate_function_maps import regenerate_binary_function_map, SIGNALING_LINUX, AGENT_ARM64
    regenerate_binary_function_map("WebRTC Signaling Server", SIGNALING_LINUX, ev_sig_temp, is_signaling=True)
    regenerate_binary_function_map("CloudPhone Agent Daemon", AGENT_ARM64, ev_agent_temp, is_signaling=False)

    # 2. Regenerate Route Handler Map
    print("[2/4] Regenerating ROUTE_HANDLER_MAP into isolated workspace...")
    from tools.forensics.extract_route_handlers import extract_routes
    # Temporarily redirect output
    import tools.forensics.extract_route_handlers as erh
    orig_json = erh.OUTPUT_JSON
    orig_md = erh.OUTPUT_MD
    erh.OUTPUT_JSON = ev_sig_temp / "ROUTE_HANDLER_MAP.json"
    erh.OUTPUT_MD = ev_sig_temp / "ROUTE_HANDLER_MAP.md"
    try:
        erh.extract_routes()
    finally:
        erh.OUTPUT_JSON = orig_json
        erh.OUTPUT_MD = orig_md

    # 3. Regenerate Role Mappings
    print("[3/4] Regenerating ROLE_MAPPING into isolated workspace...")
    import tools.forensics.regenerate_role_mappings as rrm
    orig_ev_sig = rrm.EV_SIG
    orig_ev_agent = rrm.EV_AGENT
    rrm.EV_SIG = ev_sig_temp
    rrm.EV_AGENT = ev_agent_temp
    try:
        rrm.process_role_mapping(
            "WebRTC Signaling Server",
            ev_sig_temp / "FUNCTION_MAP.json",
            ev_sig_temp / "CALLGRAPH.json",
            ev_sig_temp,
            is_signaling=True
        )
        rrm.process_role_mapping(
            "CloudPhone Agent Daemon",
            ev_agent_temp / "FUNCTION_MAP.json",
            ev_agent_temp / "CALLGRAPH.json",
            ev_agent_temp,
            is_signaling=False
        )
    finally:
        rrm.EV_SIG = orig_ev_sig
        rrm.EV_AGENT = orig_ev_agent

    # 4. Regenerate Type Field Evidence
    print("[4/4] Regenerating TYPE_FIELD_EVIDENCE into isolated workspace...")
    import tools.forensics.extract_type_field_evidence as etfe
    orig_tfe_json = etfe.OUTPUT_JSON
    orig_tfe_md = etfe.OUTPUT_MD
    etfe.OUTPUT_JSON = ev_sig_temp / "TYPE_FIELD_EVIDENCE.json"
    etfe.OUTPUT_MD = ev_sig_temp / "TYPE_FIELD_EVIDENCE.md"
    try:
        etfe.extract_type_field_evidence()
    finally:
        etfe.OUTPUT_JSON = orig_tfe_json
        etfe.OUTPUT_MD = orig_tfe_md

    # 5. Compare Canonical Hashes
    print("\n[+] Comparing Regenerated Evidence Against Committed Evidence...")
    targets = [
        ("Signaling FUNCTION_MAP.json", committed_sig / "FUNCTION_MAP.json", ev_sig_temp / "FUNCTION_MAP.json"),
        ("Signaling CALLGRAPH.json", committed_sig / "CALLGRAPH.json", ev_sig_temp / "CALLGRAPH.json"),
        ("Signaling ROUTE_HANDLER_MAP.json", committed_sig / "ROUTE_HANDLER_MAP.json", ev_sig_temp / "ROUTE_HANDLER_MAP.json"),
        ("Signaling ROLE_MAPPING.json", committed_sig / "ROLE_MAPPING.json", ev_sig_temp / "ROLE_MAPPING.json"),
        ("Signaling TYPE_FIELD_EVIDENCE.json", committed_sig / "TYPE_FIELD_EVIDENCE.json", ev_sig_temp / "TYPE_FIELD_EVIDENCE.json"),
        ("Agent FUNCTION_MAP.json", committed_agent / "FUNCTION_MAP.json", ev_agent_temp / "FUNCTION_MAP.json"),
        ("Agent CALLGRAPH.json", committed_agent / "CALLGRAPH.json", ev_agent_temp / "CALLGRAPH.json"),
        ("Agent ROLE_MAPPING.json", committed_agent / "ROLE_MAPPING.json", ev_agent_temp / "ROLE_MAPPING.json")
    ]

    all_matched = True
    for name, comm_p, regen_p in targets:
        if not comm_p.exists():
            print(f"[FAIL] {name:<35} Committed file missing: {comm_p}")
            all_matched = False
            continue
        if not regen_p.exists():
            print(f"[FAIL] {name:<35} Regenerated file missing: {regen_p}")
            all_matched = False
            continue

        h_comm = canonical_json_hash(comm_p)
        h_regen = canonical_json_hash(regen_p)
        if h_comm == h_regen:
            print(f"[PASS] {name:<35} Canonical hash match: {h_comm[:12]}")
        else:
            print(f"[FAIL] {name:<35} Hash mismatch: {h_comm[:12]} != {h_regen[:12]}")
            all_matched = False

    print("==================================================")
    status_str = "STATIC_FORENSIC_REPRODUCIBLE (PASS)" if all_matched else "REPRODUCIBILITY_FAILED"
    print(f"OVERALL REPRODUCIBILITY VERDICT: {status_str}")
    print("==================================================")

    # Cleanup temp dir
    try:
        shutil.rmtree(temp_dir)
    except:
        pass

    return all_matched

if __name__ == "__main__":
    ok = reproduce_all()
    sys.exit(0 if ok else 1)
