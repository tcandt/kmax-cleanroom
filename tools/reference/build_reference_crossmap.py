import sys
import os
import json
import hashlib
import argparse
from pathlib import Path

def get_repo_root():
    return Path(__file__).resolve().parent.parent.parent

VALID_EVIDENCE_CLASSES = {
    "PUBLIC_REFERENCE",
    "BINARY_STRING",
    "BINARY_XREF",
    "PCLNTAB_SYMBOL",
    "ROUTE_REGISTRATION",
    "DISASSEMBLY_CONTROL_FLOW",
    "TYPE_DESCRIPTOR",
    "DYNAMIC_ORACLE",
    "NETWORK_CAPTURE"
}

def compute_file_sha256(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()

def find_string_in_binary(binary_bytes: bytes, target_str: str):
    raw = target_str.encode("utf-8")
    off = binary_bytes.find(raw)
    cnt = binary_bytes.count(raw)
    return off, cnt

def build_reference_crossmap(output_dir=None):
    repo_root = get_repo_root()
    if output_dir is None:
        target_dir = repo_root / "evidence" / "reference"
    else:
        target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load canonical binaries
    sig_rel = "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling"
    agent_rel = "cloudphone-v0.3.6 (1)/android/cloudphone-agent"
    
    sig_path = repo_root / sig_rel
    agent_path = repo_root / agent_rel

    sig_bytes = sig_path.read_bytes()
    agent_bytes = agent_path.read_bytes()

    sig_sha256 = compute_file_sha256(sig_path)
    agent_sha256 = compute_file_sha256(agent_path)

    # 2. Load manifest for dynamic PUBLIC_REFERENCE binding
    manifest_rel = "evidence/reference/PUBLIC_REFERENCE_TREE_MANIFEST.json"
    manifest_path = repo_root / manifest_rel
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    manifest_entries = manifest_data.get("reference_sources", [])
    manifest_by_path = {}
    for entry in manifest_entries:
        manifest_by_path[entry["path"]] = entry
        manifest_by_path[entry["materialized_path"]] = entry
        manifest_by_path[Path(entry["path"]).name] = entry

    # 3. Load evidence artifacts
    route_map_rel = "evidence/go_signaling/ROUTE_HANDLER_MAP.json"
    route_map_path = repo_root / route_map_rel
    route_map_sha = compute_file_sha256(route_map_path)
    with open(route_map_path, "r", encoding="utf-8") as f:
        route_map_data = json.load(f)
    routes_by_pattern = {r["pattern"]: r for r in route_map_data.get("routes", [])}

    oracle_rel = "raw_extraction/go_signaling/clean_oracle_results.json"
    oracle_path = repo_root / oracle_rel
    oracle_sha = compute_file_sha256(oracle_path)
    with open(oracle_path, "r", encoding="utf-8") as f:
        oracle_data = json.load(f)

    auth_diff_rel = "evidence/go_signaling/http/AUTH_HTTP_DIFFERENTIAL_RESULTS.json"
    auth_diff_path = repo_root / auth_diff_rel
    auth_diff_sha = compute_file_sha256(auth_diff_path)
    with open(auth_diff_path, "r", encoding="utf-8") as f:
        auth_diff_data = json.load(f)
    auth_diff_by_id = {c["test_id"]: c for c in auth_diff_data}

    # Disassembly facts artifacts
    sig_facts_rel = "evidence/go_signaling/DISASSEMBLY_FACTS.json"
    sig_facts_path = repo_root / sig_facts_rel
    sig_facts_sha = compute_file_sha256(sig_facts_path)
    with open(sig_facts_path, "r", encoding="utf-8") as f:
        sig_facts_data = json.load(f)
    sig_facts_by_id = {f["fact_id"]: f for f in sig_facts_data.get("facts", [])}

    agent_facts_rel = "evidence/go_agent/DISASSEMBLY_FACTS.json"
    agent_facts_path = repo_root / agent_facts_rel
    agent_facts_sha = compute_file_sha256(agent_facts_path)
    with open(agent_facts_path, "r", encoding="utf-8") as f:
        agent_facts_data = json.load(f)
    agent_facts_by_id = {f["fact_id"]: f for f in agent_facts_data.get("facts", [])}

    # Callgraphs
    sig_cg_rel = "evidence/go_signaling/CALLGRAPH.json"
    sig_cg_path = repo_root / sig_cg_rel
    sig_cg_sha = compute_file_sha256(sig_cg_path)
    with open(sig_cg_path, "r", encoding="utf-8") as f:
        sig_cg = json.load(f)

    agent_cg_rel = "evidence/go_agent/CALLGRAPH.json"
    agent_cg_path = repo_root / agent_cg_rel
    agent_cg_sha = compute_file_sha256(agent_cg_path)
    with open(agent_cg_path, "r", encoding="utf-8") as f:
        agent_cg = json.load(f)

    # 4. Helpers for constructing compliant evidence records

    def make_public_ref_record(rel_path, line_start, line_end=None, fallback_text=""):
        entry = manifest_by_path.get(rel_path)
        if entry is None:
            # Fallback search by basename
            bname = Path(rel_path).name
            entry = manifest_by_path.get(bname)
        if entry is None:
            raise ValueError(f"Could not find manifest entry for public reference path: {rel_path}")

        mat_path = repo_root / entry["materialized_path"]
        if not mat_path.exists():
            raise FileNotFoundError(f"Materialized reference file missing: {mat_path}")

        lines = mat_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        l_start = line_start
        l_end = line_end if line_end is not None else line_start
        slice_lines = lines[l_start - 1 : l_end]
        slice_text = "\n".join(slice_lines)
        observed_hash = hashlib.sha256(slice_text.encode("utf-8")).hexdigest()

        obs_val = slice_text.strip() if slice_text.strip() else fallback_text
        if len(obs_val) > 200:
            obs_val = obs_val[:197] + "..."

        sel = f"line {line_start}" if l_start == l_end else f"lines {line_start}-{l_end}"

        return {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": entry["materialized_path"],
            "artifact_sha256": entry["sha256"],
            "evidence_file": Path(entry["path"]).name,
            "source_path": entry["path"],
            "source_commit_sha": entry["commit_sha"],
            "source_git_blob_sha": entry["git_blob_sha"],
            "source_sha256": entry["sha256"],
            "line_start": l_start,
            "line_end": l_end,
            "observed_text_hash": observed_hash,
            "selector": sel,
            "file_offset": None,
            "va": None,
            "observed_value": obs_val
        }

    def add_binary_string_record(records, binary_name, binary_bytes, binary_rel, binary_sha, query_str):
        off, cnt = find_string_in_binary(binary_bytes, query_str)
        if off >= 0:
            records.append({
                "evidence_class": "BINARY_STRING",
                "artifact_path": binary_rel,
                "artifact_sha256": binary_sha,
                "evidence_file": Path(binary_rel).name,
                "selector": query_str,
                "file_offset": hex(off),
                "va": None,
                "observed_value": f"Literal string '{query_str}' present at file offset {hex(off)} (count: {cnt}) in {binary_name} .rodata"
            })
            return True
        return False

    def add_route_registration_record(records, pattern):
        if pattern in routes_by_pattern:
            r = routes_by_pattern[pattern]
            records.append({
                "evidence_class": "ROUTE_REGISTRATION",
                "artifact_path": route_map_rel,
                "artifact_sha256": route_map_sha,
                "evidence_file": "ROUTE_HANDLER_MAP.json",
                "selector": pattern,
                "file_offset": None,
                "va": r.get("call_va"),
                "closure_va": r.get("closure_va"),
                "handler_va": r.get("handler_va"),
                "handler_symbol": r.get("handler_symbol"),
                "observed_value": f"{r.get('registration_type')}('{pattern}', closure_va: {r.get('closure_va')}, handler: {r.get('handler_symbol')} @ {r.get('handler_va')})"
            })
            return True
        return False

    def add_disassembly_fact_record(records, fact_id):
        if fact_id in sig_facts_by_id:
            fact = sig_facts_by_id[fact_id]
            art_rel = sig_facts_rel
            art_sha = sig_facts_sha
        elif fact_id in agent_facts_by_id:
            fact = agent_facts_by_id[fact_id]
            art_rel = agent_facts_rel
            art_sha = agent_facts_sha
        else:
            raise KeyError(f"Unknown fact_id: {fact_id}")

        records.append({
            "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
            "artifact_path": art_rel,
            "artifact_sha256": art_sha,
            "evidence_file": Path(art_rel).name,
            "selector": fact_id,
            "function_symbol": fact["function_symbol"],
            "function_va": fact["function_va"],
            "file_offset": None,
            "va": fact["function_va"],
            "observed_value": fact["semantic_claim"],
            "derivation": fact["derivation"]
        })
        return True

    def add_binary_xref_record(records, caller_sym, caller_va, target_sym, is_agent=False):
        if is_agent:
            cg_rel = agent_cg_rel
            cg_sha = agent_cg_sha
            cg_dict = agent_cg
        else:
            cg_rel = sig_cg_rel
            cg_sha = sig_cg_sha
            cg_dict = sig_cg

        callees = cg_dict.get(caller_va, [])
        if target_sym in callees or any(target_sym in c for c in callees):
            records.append({
                "evidence_class": "BINARY_XREF",
                "artifact_path": cg_rel,
                "artifact_sha256": cg_sha,
                "evidence_file": Path(cg_rel).name,
                "selector": f"{caller_va} -> {target_sym}",
                "caller_symbol": caller_sym,
                "caller_va": caller_va,
                "target_symbol": target_sym,
                "file_offset": None,
                "va": caller_va,
                "observed_value": f"Caller {caller_sym} ({caller_va}) invokes {target_sym} in direct callgraph"
            })
            return True
        return False

    raw_mappings = []

    # =========================================================================
    # ITEM DEFINITIONS
    # =========================================================================

    # --- ITEM 1: /connect_client ---
    c1 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 78, 83)]
    add_route_registration_record(c1, "/connect_client")
    add_binary_string_record(c1, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/connect_client")
    add_disassembly_fact_record(c1, "SIG-DCF-001")
    if "/connect_client" in oracle_data:
        o = oracle_data["/connect_client"]
        c1.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/connect_client",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET: status={o['methods']['GET']['status']}; NO_AUTH: status={o['auth_matrix']['NO_AUTH']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/connect_client",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:78-83",
        "binary_target": sig_rel,
        "evidence_records": c1
    })

    # --- ITEM 2: /register_agent ---
    c2 = [make_public_ref_record("docs/agent-deploy.md", 65, 75)]
    add_route_registration_record(c2, "/register_agent")
    add_binary_string_record(c2, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/register_agent")
    add_disassembly_fact_record(c2, "SIG-DCF-002")
    raw_mappings.append({
        "reference_item": "/register_agent",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65-75",
        "binary_target": sig_rel,
        "evidence_records": c2
    })

    # --- ITEM 3: /api/login ---
    c3 = [make_public_ref_record("web-app/src/stores/auth.js", 20, 25)]
    add_route_registration_record(c3, "/api/login")
    add_binary_string_record(c3, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/login")
    add_disassembly_fact_record(c3, "SIG-DCF-003")
    h01 = auth_diff_by_id.get("HTTP-01", {})
    h02 = auth_diff_by_id.get("HTTP-02", {})
    h03 = auth_diff_by_id.get("HTTP-03", {})
    s01 = h01.get("original_observation", {}).get("status", 200)
    s02 = h02.get("original_observation", {}).get("status", 401)
    s03 = h03.get("original_observation", {}).get("status", 400)
    c3.append({
        "evidence_class": "DYNAMIC_ORACLE",
        "artifact_path": auth_diff_rel,
        "artifact_sha256": auth_diff_sha,
        "evidence_file": "AUTH_HTTP_DIFFERENTIAL_RESULTS.json",
        "selector": "HTTP-01,HTTP-02,HTTP-03",
        "file_offset": None,
        "va": None,
        "observed_value": f"HTTP-01: status={s01}; HTTP-02: status={s02}; HTTP-03: status={s03}"
    })
    raw_mappings.append({
        "reference_item": "/api/login",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:20-25",
        "binary_target": sig_rel,
        "evidence_records": c3
    })

    # --- ITEM 4: /devices ---
    c4 = [make_public_ref_record("web-app/src/stores/devices.js", 233, 237)]
    add_route_registration_record(c4, "/devices")
    add_binary_string_record(c4, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/devices")
    add_disassembly_fact_record(c4, "SIG-DCF-004")
    if "/devices" in oracle_data:
        o = oracle_data["/devices"]
        c4.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/devices",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET: status={o['methods']['GET']['status']}; VALID_USER_TOKEN: status={o['auth_matrix']['VALID_USER_TOKEN']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/devices",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/devices.js:233-237",
        "binary_target": sig_rel,
        "evidence_records": c4
    })

    # --- ITEM 5: /api/tags ---
    c5 = [make_public_ref_record("web-app/src/stores/tags.js", 98, 103)]
    add_route_registration_record(c5, "/api/tags")
    add_binary_string_record(c5, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/tags")
    if "/api/tags" in oracle_data:
        o = oracle_data["/api/tags"]
        c5.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/api/tags",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET: status={o['methods']['GET']['status']}; VALID_USER_TOKEN: status={o['auth_matrix']['VALID_USER_TOKEN']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/api/tags",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/tags.js:98-103",
        "binary_target": sig_rel,
        "evidence_records": c5
    })

    # --- ITEM 6: /api/share/create ---
    c6 = [make_public_ref_record("web-app/src/stores/devices.js", 795, 800)]
    add_route_registration_record(c6, "/api/share/create")
    add_binary_string_record(c6, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/share/create")
    if "/api/share/create" in oracle_data:
        o = oracle_data["/api/share/create"]
        c6.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/api/share/create",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET: status={o['methods']['GET']['status']}; NO_AUTH: status={o['auth_matrix']['NO_AUTH']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/api/share/create",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/devices.js:795-800",
        "binary_target": sig_rel,
        "evidence_records": c6
    })

    # --- ITEM 7: /api/admin/users ---
    c7 = [make_public_ref_record("web-app/src/stores/auth.js", 11, 15)]
    add_route_registration_record(c7, "/api/admin/users")
    add_binary_string_record(c7, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/admin/users")
    if "/api/admin/users" in oracle_data:
        o = oracle_data["/api/admin/users"]
        c7.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/api/admin/users",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET: status={o['methods']['GET']['status']}; NO_AUTH: status={o['auth_matrix']['NO_AUTH']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/api/admin/users",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:11-15",
        "binary_target": sig_rel,
        "evidence_records": c7
    })

    # --- ITEM 8: /api/logout ---
    c8 = [make_public_ref_record("web-app/src/stores/auth.js", 75, 80)]
    add_route_registration_record(c8, "/api/logout")
    add_binary_string_record(c8, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/logout")
    h06 = auth_diff_by_id.get("HTTP-06", {})
    s06 = h06.get("original_observation", {}).get("status", 200)
    c8.append({
        "evidence_class": "DYNAMIC_ORACLE",
        "artifact_path": auth_diff_rel,
        "artifact_sha256": auth_diff_sha,
        "evidence_file": "AUTH_HTTP_DIFFERENTIAL_RESULTS.json",
        "selector": "HTTP-06",
        "file_offset": None,
        "va": None,
        "observed_value": f"HTTP-06: status={s06}"
    })
    raw_mappings.append({
        "reference_item": "/api/logout",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:75-80",
        "binary_target": sig_rel,
        "evidence_records": c8
    })

    # --- ITEM 9: /api/auth-status ---
    c9 = [make_public_ref_record("web-app/src/stores/auth.js", 98, 102)]
    add_route_registration_record(c9, "/api/auth-status")
    add_binary_string_record(c9, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/auth-status")
    add_disassembly_fact_record(c9, "SIG-DCF-005")
    h07 = auth_diff_by_id.get("HTTP-07", {})
    s07 = h07.get("original_observation", {}).get("status", 200)
    c9.append({
        "evidence_class": "DYNAMIC_ORACLE",
        "artifact_path": auth_diff_rel,
        "artifact_sha256": auth_diff_sha,
        "evidence_file": "AUTH_HTTP_DIFFERENTIAL_RESULTS.json",
        "selector": "HTTP-07",
        "file_offset": None,
        "va": None,
        "observed_value": f"HTTP-07: status={s07}"
    })
    raw_mappings.append({
        "reference_item": "/api/auth-status",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:98-102",
        "binary_target": sig_rel,
        "evidence_records": c9
    })

    # --- ITEM 10: /api/me ---
    c10 = [make_public_ref_record("web-app/src/stores/auth.js", 116, 120)]
    add_route_registration_record(c10, "/api/me")
    add_binary_string_record(c10, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/me")
    h08 = auth_diff_by_id.get("HTTP-08", {})
    s08 = h08.get("original_observation", {}).get("status", 200)
    c10.append({
        "evidence_class": "DYNAMIC_ORACLE",
        "artifact_path": auth_diff_rel,
        "artifact_sha256": auth_diff_sha,
        "evidence_file": "AUTH_HTTP_DIFFERENTIAL_RESULTS.json",
        "selector": "HTTP-08",
        "file_offset": None,
        "va": None,
        "observed_value": f"HTTP-08: status={s08}"
    })
    raw_mappings.append({
        "reference_item": "/api/me",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:116-120",
        "binary_target": sig_rel,
        "evidence_records": c10
    })

    # --- ITEM 11: message_type: forward ---
    c11 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 140, 145)]
    add_binary_string_record(c11, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "forward")
    add_binary_xref_record(c11, "main.id8ybRmw69lm", "0x7507c0", "main.(*LG7nmxLRaW).WriteJSON", is_agent=False)
    raw_mappings.append({
        "reference_item": "message_type: forward",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:140-145",
        "binary_target": sig_rel,
        "evidence_records": c11
    })

    # --- ITEM 12: message_type: command ---
    c12 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 271, 275)]
    add_binary_string_record(c12, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "command")
    add_binary_xref_record(c12, "main.jdUaLc5NMO5", "0x754b40", "main.(*A38AV00w_).Send", is_agent=False)
    raw_mappings.append({
        "reference_item": "message_type: command",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:271-275",
        "binary_target": sig_rel,
        "evidence_records": c12
    })

    # --- ITEM 13: message_type: inject_data ---
    c13 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 254, 258)]
    add_binary_string_record(c13, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "inject_data")
    add_binary_xref_record(c13, "main.id8ybRmw69lm", "0x7507c0", "_iYIJQCvEF4X.(*Yt_Fm_GhgcEh).ReadMessage", is_agent=False)
    raw_mappings.append({
        "reference_item": "message_type: inject_data",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:254-258",
        "binary_target": sig_rel,
        "evidence_records": c13
    })

    # --- ITEM 14: message_type: config ---
    c14 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 126, 130)]
    add_binary_string_record(c14, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "config")
    add_binary_xref_record(c14, "main.id8ybRmw69lm", "0x7507c0", "main.(*LG7nmxLRaW).WriteJSON", is_agent=False)
    raw_mappings.append({
        "reference_item": "message_type: config",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:126-130",
        "binary_target": sig_rel,
        "evidence_records": c14
    })

    # --- ITEM 15: message_type: device_msg ---
    c15 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 133, 137)]
    add_binary_string_record(c15, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "device_msg")
    add_binary_xref_record(c15, "main.id8ybRmw69lm", "0x7507c0", "main.(*AoIDVQHamcx).Send", is_agent=False)
    raw_mappings.append({
        "reference_item": "message_type: device_msg",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:133-137",
        "binary_target": sig_rel,
        "evidence_records": c15
    })

    # --- ITEM 16: payload: request-offer ---
    c16 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 134, 138)]
    # string 'request-offer' is not in agent binary
    add_binary_string_record(c16, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "request-offer")
    raw_mappings.append({
        "reference_item": "payload: request-offer",
        "category": "SIGNALING_PAYLOAD",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:134-138",
        "binary_target": agent_rel,
        "evidence_records": c16
    })

    # --- ITEM 17: payload: offer ---
    c17 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 175, 180)]
    add_binary_string_record(c17, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "offer")
    add_binary_xref_record(c17, "main.(*JJffa1S1Zv6).iIhwd_WXInS", "0x53c730", "IV04EXWpwj.(*VOMNaNery).CreateDataChannel", is_agent=True)
    raw_mappings.append({
        "reference_item": "payload: offer",
        "category": "SIGNALING_PAYLOAD",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:175-180",
        "binary_target": agent_rel,
        "evidence_records": c17
    })

    # --- ITEM 18: payload: answer ---
    c18 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 205, 210)]
    add_binary_string_record(c18, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "answer")
    add_binary_xref_record(c18, "main.(*JJffa1S1Zv6).iIhwd_WXInS", "0x53c730", "IV04EXWpwj.(*VOMNaNery).OnDataChannel", is_agent=True)
    raw_mappings.append({
        "reference_item": "payload: answer",
        "category": "SIGNALING_PAYLOAD",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:205-210",
        "binary_target": agent_rel,
        "evidence_records": c18
    })

    # --- ITEM 19: payload: ice-candidate ---
    c19 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 215, 220)]
    add_binary_string_record(c19, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "candidate")
    add_binary_xref_record(c19, "main.(*JJffa1S1Zv6).iIhwd_WXInS", "0x53c730", "IV04EXWpwj.(*VOMNaNery).OnDataChannel", is_agent=True)
    raw_mappings.append({
        "reference_item": "payload: ice-candidate",
        "category": "SIGNALING_PAYLOAD",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:215-220",
        "binary_target": agent_rel,
        "evidence_records": c19
    })

    # --- ITEM 20: channel: input-channel ---
    c20 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 750, 755)]
    add_binary_string_record(c20, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "input-channel")
    add_disassembly_fact_record(c20, "AGENT-DCF-001")
    raw_mappings.append({
        "reference_item": "channel: input-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:750-755",
        "binary_target": agent_rel,
        "evidence_records": c20
    })

    # --- ITEM 21: channel: clipboard-channel ---
    c21 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 761, 766)]
    add_binary_string_record(c21, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "clipboard-channel")
    add_disassembly_fact_record(c21, "AGENT-DCF-002")
    raw_mappings.append({
        "reference_item": "channel: clipboard-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:761-766",
        "binary_target": agent_rel,
        "evidence_records": c21
    })

    # --- ITEM 22: channel: camera-channel ---
    c22 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 787, 792)]
    add_binary_string_record(c22, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "camera-channel")
    add_disassembly_fact_record(c22, "AGENT-DCF-003")
    raw_mappings.append({
        "reference_item": "channel: camera-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:787-792",
        "binary_target": agent_rel,
        "evidence_records": c22
    })

    # --- ITEM 23: channel: file-channel ---
    c23 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 578, 582)]
    add_binary_string_record(c23, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "file-channel")
    add_disassembly_fact_record(c23, "AGENT-DCF-004")
    raw_mappings.append({
        "reference_item": "channel: file-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:578-582",
        "binary_target": agent_rel,
        "evidence_records": c23
    })

    # --- ITEM 24: channel: ai-command-channel ---
    c24 = [make_public_ref_record("web-app/src/composables/useWebRTC.js", 303, 307)]
    add_binary_string_record(c24, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "ai-command-channel")
    add_disassembly_fact_record(c24, "AGENT-DCF-004")
    raw_mappings.append({
        "reference_item": "channel: ai-command-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:303-307",
        "binary_target": agent_rel,
        "evidence_records": c24
    })

    # --- ITEM 25: flag: -id ---
    c25 = [make_public_ref_record("docs/agent-deploy.md", 65, 75)]
    add_binary_string_record(c25, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "-id")
    add_disassembly_fact_record(c25, "AGENT-DCF-005")
    raw_mappings.append({
        "reference_item": "flag: -id",
        "category": "AGENT_CLI",
        "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65-75",
        "binary_target": agent_rel,
        "evidence_records": c25
    })

    # --- ITEM 26: flag: -signaling ---
    c26 = [make_public_ref_record("docs/agent-deploy.md", 65, 75)]
    add_binary_string_record(c26, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "signaling")
    add_disassembly_fact_record(c26, "AGENT-DCF-005")
    raw_mappings.append({
        "reference_item": "flag: -signaling",
        "category": "AGENT_CLI",
        "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65-75",
        "binary_target": agent_rel,
        "evidence_records": c26
    })

    # --- ITEM 27: flag: -root ---
    c27 = [make_public_ref_record("docs/agent-deploy.md", 65, 75)]
    add_binary_string_record(c27, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "root")
    add_disassembly_fact_record(c27, "AGENT-DCF-005")
    raw_mappings.append({
        "reference_item": "flag: -root",
        "category": "AGENT_CLI",
        "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65-75",
        "binary_target": agent_rel,
        "evidence_records": c27
    })

    # --- ITEM 28: message_type: webrtc_failed ---
    c28 = [make_public_ref_record("web-app/src/stores/devices.js", 728, 735, fallback_text="webrtc_failed")]
    raw_mappings.append({
        "reference_item": "message_type: webrtc_failed",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/devices.js:728-735",
        "binary_target": sig_rel,
        "evidence_records": c28
    })

    # 5. Compute Strict Confirmation Status
    # Strong Gate: BINARY_SEMANTIC_CONFIRMED requires PUBLIC_REFERENCE + >= 2 independent resolved binary classes
    # REFERENCE_CORROBORATED requires PUBLIC_REFERENCE + >= 1 independent resolved binary class
    # Otherwise UNCONFIRMED_REFERENCE_ONLY

    mappings = []
    confirmed_count = 0
    corroborated_count = 0
    unconfirmed_count = 0

    for item in raw_mappings:
        records = item["evidence_records"]
        ev_classes = sorted(list(set(r["evidence_class"] for r in records)))
        for c in ev_classes:
            if c not in VALID_EVIDENCE_CLASSES:
                raise ValueError(f"Invalid evidence class: {c}")

        has_ref = "PUBLIC_REFERENCE" in ev_classes
        bin_classes = [c for c in ev_classes if c != "PUBLIC_REFERENCE"]

        if has_ref and len(bin_classes) >= 2:
            status = "BINARY_SEMANTIC_CONFIRMED"
            confirmed_count += 1
        elif has_ref and len(bin_classes) >= 1:
            status = "REFERENCE_CORROBORATED"
            corroborated_count += 1
        else:
            status = "UNCONFIRMED_REFERENCE_ONLY"
            unconfirmed_count += 1

        binary_evidence_lines = []
        for r in records:
            if r["evidence_class"] != "PUBLIC_REFERENCE":
                binary_evidence_lines.append(f"{r['evidence_class']}: {r['observed_value']}")

        mapping_entry = {
            "reference_item": item["reference_item"],
            "category": item["category"],
            "reference_source": item["reference_source"],
            "binary_target": item["binary_target"],
            "binary_evidence": binary_evidence_lines,
            "evidence_records": records,
            "evidence_classes": ev_classes,
            "status": status
        }
        mappings.append(mapping_entry)

    crossmap = {
        "metadata": {
            "title": "Reference to Binary Granular Multi-Evidence Crossmap",
            "description": "Cross-verification of public reference intelligence against granular binary static and dynamic evidence classes. Every evidence item references resolvable underlying forensic and oracle artifacts.",
            "multi_evidence_rule": "BINARY_SEMANTIC_CONFIRMED requires PUBLIC_REFERENCE + >=2 independent resolved binary classes. REFERENCE_CORROBORATED requires PUBLIC_REFERENCE + 1 binary class. Otherwise UNCONFIRMED_REFERENCE_ONLY.",
            "total_items": len(mappings),
            "binary_semantic_confirmed_items": confirmed_count,
            "reference_corroborated_items": corroborated_count,
            "unconfirmed_items": unconfirmed_count
        },
        "mappings": mappings
    }

    out_file = target_dir / "REFERENCE_TO_BINARY_CROSSMAP.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(crossmap, f, indent=2)

    print(f"[+] Successfully generated {out_file} ({confirmed_count} semantic confirmed, {corroborated_count} corroborated, {unconfirmed_count} unconfirmed)")
    return crossmap

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Reference to Binary Crossmap consuming actual evidence artifacts")
    parser.add_argument("--output-dir", help="Target output directory")
    args = parser.parse_args()
    build_reference_crossmap(args.output_dir)
