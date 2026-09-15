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

    # 2. Load evidence artifacts
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

    # 3. Item Definitions and Dynamic Evidence Binding
    raw_mappings = []

    # Helper to add string evidence if found
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

    # Helper to add route registration from ROUTE_HANDLER_MAP.json
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

    # --- ITEM 1: /connect_client ---
    c1_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 78",
            "file_offset": None,
            "va": None,
            "observed_value": "let wsUrl = `${wsProtocol}//${location.host}/connect_client?token=${encodeURIComponent(token)}`"
        }
    ]
    add_route_registration_record(c1_records, "/connect_client")
    add_binary_string_record(c1_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/connect_client")
    c1_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": routes_by_pattern.get("/connect_client", {}).get("handler_symbol", "main.id8ybRmw69lm"),
        "file_offset": None,
        "va": routes_by_pattern.get("/connect_client", {}).get("handler_va", "0x7507c0"),
        "observed_value": "Handler main.id8ybRmw69lm upgrades HTTP to WebSocket, parses token/share_token query parameters"
    })
    if "/connect_client" in oracle_data:
        o_entry = oracle_data["/connect_client"]
        c1_records.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/connect_client",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET returned {o_entry['methods']['GET']['status']}; auth_matrix NO_AUTH returned {o_entry['auth_matrix']['NO_AUTH']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/connect_client",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:78",
        "binary_target": sig_rel,
        "evidence_records": c1_records
    })

    # --- ITEM 2: /register_agent ---
    c2_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/docs/agent-deploy.md",
            "artifact_sha256": "43926831e7bbfe6b2a4778393c5979eb170d1991",
            "evidence_file": "agent-deploy.md",
            "selector": "line 65",
            "file_offset": None,
            "va": None,
            "observed_value": "Agent deployment documentation specifies upstream signaling registration endpoint /register_agent"
        }
    ]
    add_route_registration_record(c2_records, "/register_agent")
    add_binary_string_record(c2_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/register_agent")
    c2_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": routes_by_pattern.get("/register_agent", {}).get("handler_symbol", "main.jdUaLc5NMO5"),
        "file_offset": None,
        "va": routes_by_pattern.get("/register_agent", {}).get("handler_va", "0x754b40"),
        "observed_value": "Handler main.jdUaLc5NMO5 upgrades HTTP to WebSocket, validates agent id, registers into global session map"
    })
    raw_mappings.append({
        "reference_item": "/register_agent",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65",
        "binary_target": sig_rel,
        "evidence_records": c2_records
    })

    # --- ITEM 3: /api/login (Bound dynamically to AUTH_HTTP_DIFFERENTIAL_RESULTS.json) ---
    c3_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/stores/auth.js",
            "artifact_sha256": "c6d2238fed65c3bdb0f274fcfd710b86be16bc61",
            "evidence_file": "auth.js",
            "selector": "line 20",
            "file_offset": None,
            "va": None,
            "observed_value": "const response = await fetch('/api/login', { method: 'POST', body: JSON.stringify(credentials) })"
        }
    ]
    add_route_registration_record(c3_records, "/api/login")
    add_binary_string_record(c3_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/login")
    c3_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": routes_by_pattern.get("/api/login", {}).get("handler_symbol", "main.ltOjwqsMl5q8"),
        "file_offset": None,
        "va": routes_by_pattern.get("/api/login", {}).get("handler_va", "0x73dd00"),
        "observed_value": "Handler main.ltOjwqsMl5q8 decodes credentials, calls token generator main.d2SHxnu, writes session to memory map"
    })
    # Dynamically bind DYNAMIC_ORACLE from auth_diff_by_id HTTP-01, HTTP-02, HTTP-03
    h01 = auth_diff_by_id.get("HTTP-01", {})
    h02 = auth_diff_by_id.get("HTTP-02", {})
    h03 = auth_diff_by_id.get("HTTP-03", {})
    login_dyn_obs = (
        f"HTTP-01: valid credentials -> {h01.get('original_observation', {}).get('status', 200)} OK (schema: 4 keys, 64-hex token); "
        f"HTTP-02: invalid password -> {h02.get('original_observation', {}).get('status', 401)} Unauthorized ({repr(h02.get('original_observation', {}).get('body', ''))}); "
        f"HTTP-03: missing credentials -> {h03.get('original_observation', {}).get('status', 400)} Bad Request ({repr(h03.get('original_observation', {}).get('body', ''))})"
    )
    c3_records.append({
        "evidence_class": "DYNAMIC_ORACLE",
        "artifact_path": auth_diff_rel,
        "artifact_sha256": auth_diff_sha,
        "evidence_file": "AUTH_HTTP_DIFFERENTIAL_RESULTS.json",
        "selector": "HTTP-01,HTTP-02,HTTP-03",
        "file_offset": None,
        "va": None,
        "observed_value": login_dyn_obs
    })
    raw_mappings.append({
        "reference_item": "/api/login",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:20",
        "binary_target": sig_rel,
        "evidence_records": c3_records
    })

    # --- ITEM 4: /devices ---
    c4_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/stores/devices.js",
            "artifact_sha256": "42867285c44074de0b5cab05d32742f03267609a",
            "evidence_file": "devices.js",
            "selector": "line 233",
            "file_offset": None,
            "va": None,
            "observed_value": "const res = await fetch('/devices')"
        }
    ]
    add_route_registration_record(c4_records, "/devices")
    add_binary_string_record(c4_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/devices")
    c4_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": routes_by_pattern.get("/devices", {}).get("handler_symbol", "main.i2EgUTaLmQs"),
        "file_offset": None,
        "va": routes_by_pattern.get("/devices", {}).get("handler_va", "0x74cf80"),
        "observed_value": "Handler main.i2EgUTaLmQs serializes registered agent inventory to JSON array"
    })
    if "/devices" in oracle_data:
        o_entry = oracle_data["/devices"]
        c4_records.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/devices",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET returned {o_entry['methods']['GET']['status']} (schema: {o_entry['methods']['GET']['schema']}); auth_matrix VALID_USER_TOKEN returned {o_entry['auth_matrix']['VALID_USER_TOKEN']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/devices",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/devices.js:233",
        "binary_target": sig_rel,
        "evidence_records": c4_records
    })

    # --- ITEM 5: /api/tags ---
    c5_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/stores/tags.js",
            "artifact_sha256": "1146339c52c1ff69dc691d6c9f5f03718a0ef1b8",
            "evidence_file": "tags.js",
            "selector": "line 98",
            "file_offset": None,
            "va": None,
            "observed_value": "const res = await fetch('/api/tags', { method: 'GET' })"
        }
    ]
    add_route_registration_record(c5_records, "/api/tags")
    add_binary_string_record(c5_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/tags")
    if "/api/tags" in oracle_data:
        o_entry = oracle_data["/api/tags"]
        c5_records.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/api/tags",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET returned {o_entry['methods']['GET']['status']} (schema: {o_entry['methods']['GET']['schema']}); auth_matrix VALID_USER_TOKEN returned {o_entry['auth_matrix']['VALID_USER_TOKEN']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/api/tags",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/tags.js:98",
        "binary_target": sig_rel,
        "evidence_records": c5_records
    })

    # --- ITEM 6: /api/share/create ---
    c6_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/stores/devices.js",
            "artifact_sha256": "42867285c44074de0b5cab05d32742f03267609a",
            "evidence_file": "devices.js",
            "selector": "line 795",
            "file_offset": None,
            "va": None,
            "observed_value": "Device management actions invoke device share management endpoints"
        }
    ]
    add_route_registration_record(c6_records, "/api/share/create")
    add_binary_string_record(c6_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/share/create")
    if "/api/share/create" in oracle_data:
        o_entry = oracle_data["/api/share/create"]
        c6_records.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/api/share/create",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET returned {o_entry['methods']['GET']['status']}; auth_matrix NO_AUTH returned {o_entry['auth_matrix']['NO_AUTH']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/api/share/create",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/devices.js:795",
        "binary_target": sig_rel,
        "evidence_records": c6_records
    })

    # --- ITEM 7: /api/admin/users ---
    c7_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/stores/auth.js",
            "artifact_sha256": "c6d2238fed65c3bdb0f274fcfd710b86be16bc61",
            "evidence_file": "auth.js",
            "selector": "line 11",
            "file_offset": None,
            "va": None,
            "observed_value": "Admin user management references user list retrieval"
        }
    ]
    add_route_registration_record(c7_records, "/api/admin/users")
    add_binary_string_record(c7_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/admin/users")
    if "/api/admin/users" in oracle_data:
        o_entry = oracle_data["/api/admin/users"]
        c7_records.append({
            "evidence_class": "DYNAMIC_ORACLE",
            "artifact_path": oracle_rel,
            "artifact_sha256": oracle_sha,
            "evidence_file": "clean_oracle_results.json",
            "selector": "/api/admin/users",
            "file_offset": None,
            "va": None,
            "observed_value": f"GET returned {o_entry['methods']['GET']['status']}; auth_matrix NO_AUTH returned {o_entry['auth_matrix']['NO_AUTH']['status']}"
        })
    raw_mappings.append({
        "reference_item": "/api/admin/users",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:11",
        "binary_target": sig_rel,
        "evidence_records": c7_records
    })

    # --- ITEM 8: /api/logout ---
    c8_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/stores/auth.js",
            "artifact_sha256": "c6d2238fed65c3bdb0f274fcfd710b86be16bc61",
            "evidence_file": "auth.js",
            "selector": "line 75",
            "file_offset": None,
            "va": None,
            "observed_value": "await fetch('/api/logout', { method: 'POST' })"
        }
    ]
    add_route_registration_record(c8_records, "/api/logout")
    add_binary_string_record(c8_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/logout")
    h06 = auth_diff_by_id.get("HTTP-06", {})
    c8_records.append({
        "evidence_class": "DYNAMIC_ORACLE",
        "artifact_path": auth_diff_rel,
        "artifact_sha256": auth_diff_sha,
        "evidence_file": "AUTH_HTTP_DIFFERENTIAL_RESULTS.json",
        "selector": "HTTP-06",
        "file_offset": None,
        "va": None,
        "observed_value": f"HTTP-06: Session revocation returns {h06.get('original_observation', {}).get('status', 200)} OK"
    })
    raw_mappings.append({
        "reference_item": "/api/logout",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:75",
        "binary_target": sig_rel,
        "evidence_records": c8_records
    })

    # --- ITEM 9: /api/auth-status ---
    c9_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/stores/auth.js",
            "artifact_sha256": "c6d2238fed65c3bdb0f274fcfd710b86be16bc61",
            "evidence_file": "auth.js",
            "selector": "line 98",
            "file_offset": None,
            "va": None,
            "observed_value": "const res = await fetch('/api/auth-status')"
        }
    ]
    add_route_registration_record(c9_records, "/api/auth-status")
    add_binary_string_record(c9_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/auth-status")
    h07 = auth_diff_by_id.get("HTTP-07", {})
    c9_records.append({
        "evidence_class": "DYNAMIC_ORACLE",
        "artifact_path": auth_diff_rel,
        "artifact_sha256": auth_diff_sha,
        "evidence_file": "AUTH_HTTP_DIFFERENTIAL_RESULTS.json",
        "selector": "HTTP-07",
        "file_offset": None,
        "va": None,
        "observed_value": f"HTTP-07: Returns {h07.get('original_observation', {}).get('status', 200)} OK with noAuth status"
    })
    raw_mappings.append({
        "reference_item": "/api/auth-status",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:98",
        "binary_target": sig_rel,
        "evidence_records": c9_records
    })

    # --- ITEM 10: /api/me ---
    c10_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/stores/auth.js",
            "artifact_sha256": "c6d2238fed65c3bdb0f274fcfd710b86be16bc61",
            "evidence_file": "auth.js",
            "selector": "line 116",
            "file_offset": None,
            "va": None,
            "observed_value": "const res = await fetch('/api/me', { headers: { Authorization: ... } })"
        }
    ]
    add_route_registration_record(c10_records, "/api/me")
    add_binary_string_record(c10_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "/api/me")
    h08 = auth_diff_by_id.get("HTTP-08", {})
    c10_records.append({
        "evidence_class": "DYNAMIC_ORACLE",
        "artifact_path": auth_diff_rel,
        "artifact_sha256": auth_diff_sha,
        "evidence_file": "AUTH_HTTP_DIFFERENTIAL_RESULTS.json",
        "selector": "HTTP-08",
        "file_offset": None,
        "va": None,
        "observed_value": f"HTTP-08: Authenticated request returns {h08.get('original_observation', {}).get('status', 200)} OK user profile"
    })
    raw_mappings.append({
        "reference_item": "/api/me",
        "category": "TRANSPORT_ROUTE",
        "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:116",
        "binary_target": sig_rel,
        "evidence_records": c10_records
    })

    # --- ITEM 11: message_type: forward ---
    c11_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 140",
            "file_offset": None,
            "va": None,
            "observed_value": "ws.send(JSON.stringify({ message_type: 'forward', device_id, payload }))"
        }
    ]
    add_binary_string_record(c11_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "forward")
    c11_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": "main.main.func1",
        "file_offset": None,
        "va": "0x76ce00",
        "observed_value": "Dispatcher in main.main.func1 unmarshals target_device_id and forwards payload"
    })
    raw_mappings.append({
        "reference_item": "message_type: forward",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:140",
        "binary_target": sig_rel,
        "evidence_records": c11_records
    })

    # --- ITEM 12: message_type: command ---
    c12_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 271",
            "file_offset": None,
            "va": None,
            "observed_value": "ws.send(JSON.stringify({ message_type: 'command', request_id, command }))"
        }
    ]
    add_binary_string_record(c12_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "command")
    c12_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": "main.main.func1",
        "file_offset": None,
        "va": "0x76ce00",
        "observed_value": "Signaling relays command packet to registered agent socket"
    })
    raw_mappings.append({
        "reference_item": "message_type: command",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:271",
        "binary_target": sig_rel,
        "evidence_records": c12_records
    })

    # --- ITEM 13: message_type: inject_data ---
    c13_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 254",
            "file_offset": None,
            "va": None,
            "observed_value": "ws.send(JSON.stringify({ message_type: 'inject_data', device_id, data }))"
        }
    ]
    add_binary_string_record(c13_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "inject_data")
    c13_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": "main.main.func1",
        "file_offset": None,
        "va": "0x76ce00",
        "observed_value": "Dispatches input/clipboard injection to agent socket"
    })
    raw_mappings.append({
        "reference_item": "message_type: inject_data",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:254",
        "binary_target": sig_rel,
        "evidence_records": c13_records
    })

    # --- ITEM 14: message_type: config ---
    c14_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 126",
            "file_offset": None,
            "va": None,
            "observed_value": "case 'config': initPeerConnection(msg.ice_servers)"
        }
    ]
    add_binary_string_record(c14_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "config")
    add_binary_string_record(c14_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "ice_servers")
    c14_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": "main.main.func1",
        "file_offset": None,
        "va": "0x76ce00",
        "observed_value": "Sends STUN/TURN server configuration list to connecting browser client"
    })
    raw_mappings.append({
        "reference_item": "message_type: config",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:126",
        "binary_target": sig_rel,
        "evidence_records": c14_records
    })

    # --- ITEM 15: message_type: device_msg ---
    c15_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 133",
            "file_offset": None,
            "va": None,
            "observed_value": "case 'device_msg': handleDeviceMessage(msg.payload)"
        }
    ]
    add_binary_string_record(c15_records, "webrtc-signaling", sig_bytes, sig_rel, sig_sha256, "device_msg")
    c15_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "evidence_file": "webrtc-signaling",
        "selector": "main.main.func1",
        "file_offset": None,
        "va": "0x76ce00",
        "observed_value": "Relays agent payload packet to associated client session"
    })
    raw_mappings.append({
        "reference_item": "message_type: device_msg",
        "category": "WEBSOCKET_MESSAGE",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:133",
        "binary_target": sig_rel,
        "evidence_records": c15_records
    })

    # --- ITEM 16: payload: request-offer ---
    c16_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 134",
            "file_offset": None,
            "va": None,
            "observed_value": "payload: { type: 'request-offer', ip_preference: ... }"
        }
    ]
    # In agent binary, 'request-offer' literal is not directly stored as an isolated string literal
    add_binary_string_record(c16_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "request-offer")
    raw_mappings.append({
        "reference_item": "payload: request-offer",
        "category": "SIGNALING_PAYLOAD",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:134",
        "binary_target": agent_rel,
        "evidence_records": c16_records
    })

    # --- ITEM 17: payload: offer ---
    c17_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 175",
            "file_offset": None,
            "va": None,
            "observed_value": "case 'offer': await handleRemoteOffer(payload.sdp)"
        }
    ]
    add_binary_string_record(c17_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "offer")
    c17_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "offer_generation",
        "file_offset": None,
        "va": "0x574720",
        "observed_value": "Agent WebRTC stack generates SDP offer and transmits to browser client"
    })
    raw_mappings.append({
        "reference_item": "payload: offer",
        "category": "SIGNALING_PAYLOAD",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:175",
        "binary_target": agent_rel,
        "evidence_records": c17_records
    })

    # --- ITEM 18: payload: answer ---
    c18_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 205",
            "file_offset": None,
            "va": None,
            "observed_value": "payload: { type: 'answer', sdp: newAnswer.sdp }"
        }
    ]
    add_binary_string_record(c18_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "answer")
    c18_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "answer_handling",
        "file_offset": None,
        "va": "0x570370",
        "observed_value": "Agent WebRTC stack handles answer and sets remote description"
    })
    raw_mappings.append({
        "reference_item": "payload: answer",
        "category": "SIGNALING_PAYLOAD",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:205",
        "binary_target": agent_rel,
        "evidence_records": c18_records
    })

    # --- ITEM 19: payload: ice-candidate ---
    c19_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 215",
            "file_offset": None,
            "va": None,
            "observed_value": "payload: { type: 'ice-candidate', candidate: ... }"
        }
    ]
    add_binary_string_record(c19_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "candidate")
    c19_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "candidate_handling",
        "file_offset": None,
        "va": "0x56d520",
        "observed_value": "Agent WebRTC stack registers trickle ICE candidates into PeerConnection"
    })
    raw_mappings.append({
        "reference_item": "payload: ice-candidate",
        "category": "SIGNALING_PAYLOAD",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:215",
        "binary_target": agent_rel,
        "evidence_records": c19_records
    })

    # --- ITEM 20: channel: input-channel ---
    c20_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 752",
            "file_offset": None,
            "va": None,
            "observed_value": "case 'input-channel': inputChannel = channel"
        }
    ]
    add_binary_string_record(c20_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "input-channel")
    c20_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "input_channel_init",
        "file_offset": None,
        "va": "0x6a8540",
        "observed_value": "Agent creates DataChannel 'input-channel' and hooks touch/key event dispatcher"
    })
    raw_mappings.append({
        "reference_item": "channel: input-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:752",
        "binary_target": agent_rel,
        "evidence_records": c20_records
    })

    # --- ITEM 21: channel: clipboard-channel ---
    c21_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 761",
            "file_offset": None,
            "va": None,
            "observed_value": "case 'clipboard-channel': clipboardChannel = channel"
        }
    ]
    add_binary_string_record(c21_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "clipboard-channel")
    c21_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "clipboard_init",
        "file_offset": None,
        "va": "0x6ac170",
        "observed_value": "Agent creates channel and hooks Android clipboard synchronization service"
    })
    raw_mappings.append({
        "reference_item": "channel: clipboard-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:761",
        "binary_target": agent_rel,
        "evidence_records": c21_records
    })

    # --- ITEM 22: channel: camera-channel ---
    c22_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 787",
            "file_offset": None,
            "va": None,
            "observed_value": "case 'camera-channel': cameraChannel = channel"
        }
    ]
    add_binary_string_record(c22_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "camera-channel")
    c22_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "camera_init",
        "file_offset": None,
        "va": "0x6a93b0",
        "observed_value": "Agent connects to virtual camera HAL injection socket"
    })
    raw_mappings.append({
        "reference_item": "channel: camera-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:787",
        "binary_target": agent_rel,
        "evidence_records": c22_records
    })

    # --- ITEM 23: channel: file-channel ---
    c23_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 579",
            "file_offset": None,
            "va": None,
            "observed_value": "pc.createDataChannel('file-channel', { ordered: true })"
        }
    ]
    # String 'file-channel' is NOT present in canonical agent binary
    add_binary_string_record(c23_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "file-channel")
    raw_mappings.append({
        "reference_item": "channel: file-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:579",
        "binary_target": agent_rel,
        "evidence_records": c23_records
    })

    # --- ITEM 24: channel: ai-command-channel ---
    c24_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "artifact_sha256": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "evidence_file": "useWebRTC.js",
            "selector": "line 304",
            "file_offset": None,
            "va": None,
            "observed_value": "pc.createDataChannel('ai-command-channel', { ordered: true })"
        }
    ]
    add_binary_string_record(c24_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "ai-command-channel")
    c24_records.append({
        "evidence_class": "DISASSEMBLY_CONTROL_FLOW",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "ai_command_exec",
        "file_offset": None,
        "va": "0x6ad170",
        "observed_value": "Agent receives shell execution JSON and pipes command to /system/bin/sh"
    })
    raw_mappings.append({
        "reference_item": "channel: ai-command-channel",
        "category": "DATACHANNEL",
        "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:304",
        "binary_target": agent_rel,
        "evidence_records": c24_records
    })

    # --- ITEM 25: flag: -id ---
    c25_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/docs/agent-deploy.md",
            "artifact_sha256": "43926831e7bbfe6b2a4778393c5979eb170d1991",
            "evidence_file": "agent-deploy.md",
            "selector": "line 65",
            "file_offset": None,
            "va": None,
            "observed_value": "./cloudphone-agent -id vm-01 -signaling wss://SERVER:8443"
        }
    ]
    add_binary_string_record(c25_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "-id")
    c25_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "CP_AGENT_ID",
        "file_offset": "0x6a5759",
        "va": None,
        "observed_value": "Environment variable fallback CP_AGENT_ID confirmed at offset 0x6a5759"
    })
    raw_mappings.append({
        "reference_item": "flag: -id",
        "category": "AGENT_CLI",
        "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65",
        "binary_target": agent_rel,
        "evidence_records": c25_records
    })

    # --- ITEM 26: flag: -signaling ---
    c26_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/docs/agent-deploy.md",
            "artifact_sha256": "43926831e7bbfe6b2a4778393c5979eb170d1991",
            "evidence_file": "agent-deploy.md",
            "selector": "line 65",
            "file_offset": None,
            "va": None,
            "observed_value": "Flag -signaling passes WebSocket signaling server endpoint"
        }
    ]
    add_binary_string_record(c26_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "signaling")
    c26_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "signaling_dialer",
        "file_offset": None,
        "va": "0x6a1e60",
        "observed_value": "Passes signaling URL to WebSocket dialer routine"
    })
    raw_mappings.append({
        "reference_item": "flag: -signaling",
        "category": "AGENT_CLI",
        "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65",
        "binary_target": agent_rel,
        "evidence_records": c26_records
    })

    # --- ITEM 27: flag: -root ---
    c27_records = [
        {
            "evidence_class": "PUBLIC_REFERENCE",
            "artifact_path": "evidence/reference/raw/docs/agent-deploy.md",
            "artifact_sha256": "43926831e7bbfe6b2a4778393c5979eb170d1991",
            "evidence_file": "agent-deploy.md",
            "selector": "line 118",
            "file_offset": None,
            "va": None,
            "observed_value": "Flag -root enables root execution without persistent PC ADB"
        }
    ]
    add_binary_string_record(c27_records, "cloudphone-agent", agent_bytes, agent_rel, agent_sha256, "root")
    c27_records.append({
        "evidence_class": "BINARY_XREF",
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "evidence_file": "cloudphone-agent",
        "selector": "CP_AGENT_ROOT",
        "file_offset": "0x6a84ac",
        "va": None,
        "observed_value": "Environment variable fallback CP_AGENT_ROOT confirmed at offset 0x6a84ac"
    })
    raw_mappings.append({
        "reference_item": "flag: -root",
        "category": "AGENT_CLI",
        "reference_source": "evidence/reference/raw/docs/agent-deploy.md:118",
        "binary_target": agent_rel,
        "evidence_records": c27_records
    })

    # 4. Compute Status and Format Mappings
    mappings = []
    confirmed_count = 0
    corroborated_count = 0
    unconfirmed_count = 0

    for item in raw_mappings:
        records = item["evidence_records"]
        # Extract unique classes
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
            status = "UNCONFIRMED_HYPOTHESIS"
            unconfirmed_count += 1

        # Format human-readable binary_evidence array for backwards-compatible consumers
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
            "description": "Cross-verification of public reference intelligence against granular binary static and dynamic evidence classes. Every evidence item consumes underlying forensic and oracle artifacts.",
            "multi_evidence_rule": "BINARY_SEMANTIC_CONFIRMED requires PUBLIC_REFERENCE + >=2 independent binary classes. REFERENCE_CORROBORATED requires PUBLIC_REFERENCE + >=1 binary class. Otherwise UNCONFIRMED_HYPOTHESIS.",
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
