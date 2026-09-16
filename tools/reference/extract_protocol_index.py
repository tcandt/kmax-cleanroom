import sys
import os
import re
import json
import argparse
from pathlib import Path

def get_repo_root():
    return Path(__file__).resolve().parent.parent.parent

def extract_protocol_index(output_dir=None):
    repo_root = get_repo_root()
    raw_dir = repo_root / "evidence" / "reference" / "raw"
    if output_dir is None:
        target_dir = repo_root / "evidence" / "reference"
    else:
        target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # 1. PURE MACHINE EXTRACTION (AST / Regex over raw source files)
    # =========================================================================
    web_app_dir = raw_dir / "web-app"

    # A. Machine extraction of HTTP endpoints
    discovered_endpoints = {}
    endpoint_regex = re.compile(r'[\'"`](/(?:api|connect_client|register_agent)[^\'"`\s?#]*)')
    
    for fpath in web_app_dir.rglob("*"):
        if fpath.suffix in (".js", ".vue"):
            rel_path = fpath.relative_to(raw_dir).as_posix()
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(content.splitlines(), 1):
                matches = endpoint_regex.findall(line)
                for m in matches:
                    clean_m = m.split("${")[0].rstrip("/")
                    if not clean_m:
                        clean_m = "/"
                    if clean_m not in discovered_endpoints:
                        discovered_endpoints[clean_m] = []
                    discovered_endpoints[clean_m].append({
                        "file": rel_path,
                        "line": line_no
                    })

    machine_endpoints = [
        {
            "endpoint": ep,
            "occurrences_count": len(occs),
            "occurrences": occs,
            "classification": "MACHINE_OBSERVED"
        }
        for ep, occs in sorted(discovered_endpoints.items())
    ]

    # B. Machine extraction of WebSocket Client-to-Server Message Types
    ws_send_regex = re.compile(r'message_type\s*[:=]\s*[\'"]([a-zA-Z0-9_\-]+)[\'"]')
    client_msg_occurrences = {}
    for fpath in web_app_dir.rglob("*"):
        if fpath.suffix in (".js", ".vue"):
            rel_path = fpath.relative_to(raw_dir).as_posix()
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(content.splitlines(), 1):
                for m in ws_send_regex.findall(line):
                    if m not in client_msg_occurrences:
                        client_msg_occurrences[m] = []
                    client_msg_occurrences[m].append({
                        "file": rel_path,
                        "line": line_no
                    })

    machine_client_msgs = [
        {
            "message_type": m,
            "occurrences_count": len(occs),
            "occurrences": occs,
            "classification": "MACHINE_OBSERVED"
        }
        for m, occs in sorted(client_msg_occurrences.items())
    ]

    # C. Machine extraction of WebSocket Server-to-Client Message Types
    onmsg_regex = re.compile(r'(?:msg|data)\.message_type\s*===\s*[\'"]([a-zA-Z0-9_\-]+)[\'"]')
    server_msg_occurrences = {}
    for fpath in web_app_dir.rglob("*"):
        if fpath.suffix in (".js", ".vue"):
            rel_path = fpath.relative_to(raw_dir).as_posix()
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(content.splitlines(), 1):
                for m in onmsg_regex.findall(line):
                    if m not in server_msg_occurrences:
                        server_msg_occurrences[m] = []
                    server_msg_occurrences[m].append({
                        "file": rel_path,
                        "line": line_no
                    })

    machine_server_msgs = [
        {
            "message_type": m,
            "occurrences_count": len(occs),
            "occurrences": occs,
            "classification": "MACHINE_OBSERVED"
        }
        for m, occs in sorted(server_msg_occurrences.items())
    ]

    # D. Machine extraction of Forward Payload Types
    fwd_payload_regex = re.compile(r'type\s*[:=]\s*[\'"](request-offer|offer|answer|ice-candidate|clipboard|camera)[\'"]')
    fwd_payload_occurrences = {}
    for fpath in web_app_dir.rglob("*"):
        if fpath.suffix in (".js", ".vue"):
            rel_path = fpath.relative_to(raw_dir).as_posix()
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(content.splitlines(), 1):
                for m in fwd_payload_regex.findall(line):
                    if m not in fwd_payload_occurrences:
                        fwd_payload_occurrences[m] = []
                    fwd_payload_occurrences[m].append({
                        "file": rel_path,
                        "line": line_no
                    })

    machine_fwd_payloads = [
        {
            "payload_type": m,
            "occurrences_count": len(occs),
            "occurrences": occs,
            "classification": "MACHINE_OBSERVED"
        }
        for m, occs in sorted(fwd_payload_occurrences.items())
    ]

    # =========================================================================
    # 2. ANNOTATION TEMPLATES & PRESENTATION CATALOG (Explicitly Separated)
    # =========================================================================
    # These roles and definitions are semantic interpretations or documentation
    # templates. They are classified as ANNOTATION_TEMPLATE and excluded from
    # forensic binary confirmation counts.

    known_endpoint_roles = {
        "/api/login": ("POST", "Authentication: credentials login and session token issuance"),
        "/api/logout": ("ANY", "Authentication: session revocation"),
        "/api/auth-status": ("ANY", "Authentication: check whether noAuth mode is active"),
        "/api/me": ("ANY", "Authentication: retrieve authenticated user profile"),
        "/api/devices": ("GET", "Device: list active and registered devices"),
        "/api/devices/": ("GET/POST/DELETE", "Device: manage specific device by ID"),
        "/api/tags": ("GET/POST/PUT/DELETE", "Tags: manage device categories and label associations"),
        "/api/admin/users": ("GET", "Admin: list user accounts"),
        "/api/admin/users/create": ("POST", "Admin: create new user account"),
        "/api/admin/users/update": ("POST", "Admin: update account properties / expiration"),
        "/api/admin/users/delete": ("POST", "Admin: remove user account"),
        "/api/admin/users/reset_password": ("POST", "Admin: reset user password"),
        "/api/admin/users/rename": ("POST", "Admin: rename user account"),
        "/api/admin/users/update_note": ("POST", "Admin: update user note field"),
        "/api/admin/users/kick": ("POST", "Admin: kick active user sessions"),
        "/api/admin/assign": ("POST", "Admin: assign device permissions to user"),
        "/api/share/create": ("POST", "Share: create temporary sharing link for device"),
        "/api/share/list": ("GET", "Share: list active share tokens"),
        "/api/share/revoke": ("POST", "Share: revoke share token"),
        "/api/share/extend": ("POST", "Share: extend share token lifetime"),
        "/api/share/update": ("POST", "Share: update share token properties"),
        "/api/share/info": ("GET", "Share: fetch metadata for shared device"),
        "/api/share/redeem_card": ("POST", "Share: redeem card code for device access"),
        "/api/default_settings": ("GET/POST", "Config: global default settings (bitrate, fps, etc.)"),
        "/api/ice_servers": ("GET/POST", "Config: STUN/TURN server list"),
        "/api/server/addresses": ("GET", "Config: query external server IPs"),
        "/api/shortcuts": ("GET/POST", "Config: keyboard shortcut mappings"),
        "/api/version": ("GET", "System: signaling server version"),
        "/api/license_status": ("GET", "System: query license status"),
        "/api/activate": ("POST", "System: apply license key"),
        "/api/files": ("GET/DELETE", "Files: file management listing and deletion"),
        "/api/tasks": ("GET/POST", "Tasks: batch task execution"),
        "/api/tasks/details": ("GET", "Tasks: query task execution status"),
        "/api/user/ai-config": ("GET/POST", "User: AI assistant integration settings"),
        "/upload": ("POST", "Upload: file/APK upload endpoint"),
        "/downloads/": ("GET", "Static: agent executable / APK downloads"),
        "/snapshots/": ("GET", "Static: device screenshot thumbnail serving")
    }

    http_endpoints_list = []
    for path, (method, role) in sorted(known_endpoint_roles.items()):
        occurrences = discovered_endpoints.get(path.rstrip("/"), [])
        first_ref = occurrences[0]["file"] if occurrences else "docs/web-development.md"
        http_endpoints_list.append({
            "path": path,
            "method": method,
            "role": role,
            "source_evidence": first_ref,
            "occurrences_in_source": len(occurrences),
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        })

    ws_c2s_definitions = [
        {
            "message_type": "connect",
            "fields": { "message_type": "connect", "device_id": "string" },
            "description": "Sent by client immediately after WebSocket connection to target device session",
            "source": "web-app/src/composables/useWebRTC.js:92",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "forward",
            "fields": { "message_type": "forward", "device_id": "string", "payload": "object" },
            "description": "Wraps signaling payloads (request-offer, answer, ice-candidate) forwarded to Agent",
            "source": "web-app/src/composables/useWebRTC.js:140",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "command",
            "fields": { "message_type": "command", "device_id": "string", "request_id": "string", "command": "string" },
            "description": "Direct shell/command execution request forwarded to agent via signaling server",
            "source": "web-app/src/composables/useWebRTC.js:271",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "inject_data",
            "fields": { "message_type": "inject_data", "device_id": "string", "channel": "string", "data": "any" },
            "description": "WebSocket fallback for touch/clipboard when DataChannel is unavailable",
            "source": "web-app/src/composables/useWebRTC.js:254",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "group_control_event",
            "fields": { "message_type": "group_control_event", "device_ids": "array", "event": "object" },
            "description": "Multi-device synchronized control broadcast across multiple phone sessions",
            "source": "web-app/src/stores/devices.js:583",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "get_settings",
            "fields": { "message_type": "get_settings" },
            "description": "Requests global system settings from signaling server",
            "source": "web-app/src/stores/devices.js:592",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "webrtc_failed",
            "fields": { "message_type": "webrtc_failed", "device_id": "string" },
            "description": "Candidate message indicating WebRTC failure",
            "source": "web-app/src/stores/devices.js",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        }
    ]

    ws_s2c_definitions = [
        {
            "message_type": "config",
            "fields": { "message_type": "config", "ice_servers": "array" },
            "description": "Provides STUN/TURN ICE server configuration to connecting client",
            "source": "web-app/src/composables/useWebRTC.js:126",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "device_msg",
            "fields": { "message_type": "device_msg", "device_id": "string", "payload": "object" },
            "description": "Delivers forwarded messages from Agent (offer, ice-candidate, clipboard, etc.)",
            "source": "web-app/src/composables/useWebRTC.js:133",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "device_online",
            "fields": { "message_type": "device_online", "device": "object" },
            "description": "Broadcasts that a device agent has connected and registered",
            "source": "web-app/src/stores/devices.js:675",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "device_offline",
            "fields": { "message_type": "device_offline", "device_id": "string" },
            "description": "Broadcasts that a device agent has disconnected",
            "source": "web-app/src/stores/devices.js:680",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "device_list",
            "fields": { "message_type": "device_list", "devices": "array" },
            "description": "Initial synchronization of all online devices on WebSocket connect",
            "source": "web-app/src/stores/devices.js:670",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "command_result",
            "fields": { "message_type": "command_result", "request_id": "string", "output": "string", "exit_code": "number" },
            "description": "Delivers asynchronous shell command execution output back to client",
            "source": "web-app/src/composables/useWebRTC.js:148",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "message_type": "auth_error",
            "fields": { "message_type": "auth_error", "error": "string" },
            "description": "Signals token expiration, invalid permissions, or session kick",
            "source": "web-app/src/composables/useWebRTC.js:156",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        }
    ]

    fwd_payload_definitions = [
        {
            "type": "request-offer",
            "direction": "Browser -> Signaling -> Agent",
            "fields": { "type": "request-offer", "ip_preference": "string", "scrcpy_options": "object" },
            "description": "Requests Agent to create a WebRTC PeerConnection, start scrcpy, and generate an SDP offer",
            "source": "web-app/src/composables/useWebRTC.js:134",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "type": "offer",
            "direction": "Agent -> Signaling -> Browser",
            "fields": { "type": "offer", "sdp": "string", "camera_support": "boolean" },
            "description": "Agent SDP offer containing video/audio media tracks and DataChannel attributes",
            "source": "web-app/src/composables/useWebRTC.js:175",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "type": "answer",
            "direction": "Browser -> Signaling -> Agent",
            "fields": { "type": "answer", "sdp": "string" },
            "description": "Browser SDP answer with munged bandwidth parameters and audio preferences",
            "source": "web-app/src/composables/useWebRTC.js:205",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "type": "ice-candidate",
            "direction": "Bi-directional (Browser <-> Agent)",
            "fields": { "type": "ice-candidate", "candidate": "string | object" },
            "description": "Trickle ICE candidate exchange for P2P UDP/TCP hole punching",
            "source": "web-app/src/composables/useWebRTC.js:215",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "type": "clipboard",
            "direction": "Bi-directional",
            "fields": { "type": "clipboard", "text": "string", "source": "string", "origin_client_id": "string" },
            "description": "Fallback clipboard payload when clipboard-channel is not established",
            "source": "web-app/src/composables/useWebRTC.js:770",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        },
        {
            "type": "camera",
            "direction": "Bi-directional",
            "fields": { "type": "camera", "action": "string" },
            "description": "Camera control signaling fallback",
            "source": "web-app/src/composables/useWebRTC.js:800",
            "classification": "ANNOTATION_TEMPLATE",
            "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
        }
    ]

    protocol_index = {
        "metadata": {
            "title": "Public Frontend Reference Protocol Index",
            "evidence_class": "REFERENCE_DERIVED",
            "source_repositories": [
                "tcandt/scrcpyoverwebrtc (commit: 65567d777bccb11d2a6d93b6acc735478e880b5b)",
                "hqw700/cloudphone-official (commit: ceb66b20ad4c6f7b217d38852ea9ec2bd70fcd39)"
            ],
            "description": "Reference protocol index separating pure machine extractions (MACHINE_OBSERVED) from human design annotations (ANNOTATION_TEMPLATE)."
        },
        "machine_extracted": {
            "http_endpoints": machine_endpoints,
            "websocket_client_messages": machine_client_msgs,
            "websocket_server_messages": machine_server_msgs,
            "forward_payloads": machine_fwd_payloads
        },
        "annotated_catalog": {
            "description": "Human/design annotations explicitly excluded from forensic confirmation counts.",
            "http_endpoints": http_endpoints_list,
            "websocket_client_messages": ws_c2s_definitions,
            "websocket_server_messages": ws_s2c_definitions,
            "forward_payloads": fwd_payload_definitions
        },
        "transport_endpoints": {
            "websocket_signaling": [
                {
                    "path": "/connect_client",
                    "role": "Browser client signaling connection",
                    "query_parameters": {
                        "token": "Session auth token (optional if share_token is used)",
                        "share_token": "Share link authorization token (optional)",
                        "share_pwd": "Share link password (optional, if protected)"
                    },
                    "source_reference": "web-app/src/composables/useWebRTC.js:78-83, web-app/src/stores/devices.js:669",
                    "classification": "ANNOTATION_TEMPLATE",
                    "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
                },
                {
                    "path": "/register_agent",
                    "role": "Agent registration and upstream command link",
                    "query_parameters": {
                        "id": "Agent / device unique identifier (passed via -id CLI flag)"
                    },
                    "source_reference": "docs/agent-deploy.md",
                    "classification": "ANNOTATION_TEMPLATE",
                    "forensic_status": "EXCLUDED_FROM_CONFIRMATION_COUNTS"
                }
            ],
            "http_endpoints": http_endpoints_list
        },
        "websocket_messages": {
            "client_to_server": ws_c2s_definitions,
            "server_to_client": ws_s2c_definitions
        },
        "signaling_forward_payloads": fwd_payload_definitions,
        "demo_mock_routes": [
            { "path": "/api/demo/devices", "mock_source": "demoEngine.js", "classification": "MOCK_ONLY_SYNTHETIC" },
            { "path": "/api/demo/login", "mock_source": "demoEngine.js", "classification": "MOCK_ONLY_SYNTHETIC" },
            { "path": "/api/demo/stream", "mock_source": "demoEngine.js", "classification": "MOCK_ONLY_SYNTHETIC" }
        ]
    }

    json_path = target_dir / "REFERENCE_PROTOCOL_INDEX.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(protocol_index, f, indent=2)

    md_path = target_dir / "REFERENCE_PROTOCOL_INDEX.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Public Reference Protocol Index & Candidate Hypotheses\n\n")
        f.write("**Status**: GENERATED FROM IMMUTABLE LOCAL SNAPSHOTS (`evidence/reference/raw/`)\n")
        f.write("**Separation**: `MACHINE_OBSERVED` vs `ANNOTATION_TEMPLATE`\n\n")
        f.write("## 1. Machine Extractions Summary\n\n")
        f.write(f"- **Machine Observed Endpoints**: {len(machine_endpoints)} distinct endpoint literals\n")
        f.write(f"- **Machine Client WS Message Types**: {len(machine_client_msgs)} extracted types\n")
        f.write(f"- **Machine Server WS Message Types**: {len(machine_server_msgs)} extracted types\n")
        f.write(f"- **Machine Forward Payloads**: {len(machine_fwd_payloads)} extracted payload types\n\n")
        f.write("## 2. Annotation Templates (Excluded From Forensic Confirmation Counts)\n\n")
        f.write(f"- **Annotated Endpoints**: {len(http_endpoints_list)} cataloged routes\n")
        f.write(f"- **Annotated Client-to-Server WS**: {len(ws_c2s_definitions)} cataloged definitions\n")
        f.write(f"- **Annotated Server-to-Client WS**: {len(ws_s2c_definitions)} cataloged definitions\n")
        f.write(f"- **Annotated Forward Payloads**: {len(fwd_payload_definitions)} cataloged definitions\n\n")
        f.write("## 3. Strict Demo Mode Isolation\n\n")
        f.write(f"- Identified {len(protocol_index['demo_mock_routes'])} synthetic demo mock routes isolated from real production paths.\n")

    print(f"[+] Successfully generated {json_path} and {md_path}")
    return protocol_index

generate_protocol_index = extract_protocol_index

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract protocol index from reference raw snapshot")
    parser.add_argument("--output-dir", help="Target output directory")
    args = parser.parse_args()
    extract_protocol_index(args.output_dir)
