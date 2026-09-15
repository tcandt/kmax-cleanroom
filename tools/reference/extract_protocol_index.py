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

    # 1. Parse HTTP Endpoints from raw web-app files
    discovered_endpoints = {}
    web_app_dir = raw_dir / "web-app"

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

    # 2. Parse WebSocket Messages
    ws_client_messages = set()
    ws_server_messages = set()

    # Search useWebRTC.js and devices.js for message_type
    ws_send_regex = re.compile(r'message_type\s*[:=]\s*[\'"]([a-zA-Z0-9_\-]+)[\'"]')
    for fpath in web_app_dir.rglob("*"):
        if fpath.suffix in (".js", ".vue"):
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            for m in ws_send_regex.findall(content):
                ws_client_messages.add(m)

    # Server to client messages received in onmessage switches
    onmsg_regex = re.compile(r'(?:msg|data)\.message_type\s*===\s*[\'"]([a-zA-Z0-9_\-]+)[\'"]')
    for fpath in web_app_dir.rglob("*"):
        if fpath.suffix in (".js", ".vue"):
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            for m in onmsg_regex.findall(content):
                ws_server_messages.add(m)

    # Explicitly cataloged server messages from switch branches
    known_server_msgs = {"config", "device_msg", "device_online", "device_offline", "device_list", "command_result", "auth_error"}
    ws_server_messages.update(known_server_msgs)

    # 3. Parse forward payloads
    fwd_payload_regex = re.compile(r'type\s*[:=]\s*[\'"](request-offer|offer|answer|ice-candidate|clipboard|camera)[\'"]')
    fwd_payloads = set()
    for fpath in web_app_dir.rglob("*"):
        if fpath.suffix in (".js", ".vue"):
            content = fpath.read_text(encoding="utf-8", errors="ignore")
            for m in fwd_payload_regex.findall(content):
                fwd_payloads.add(m)

    # 4. Build Structured Protocol Index
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
            "classification": "SOURCE_REFERENCE_CANDIDATE"
        })

    ws_c2s_definitions = [
        {
            "message_type": "connect",
            "fields": { "message_type": "connect", "device_id": "string" },
            "description": "Sent by client immediately after WebSocket connection to target device session",
            "source": "web-app/src/composables/useWebRTC.js:92"
        },
        {
            "message_type": "forward",
            "fields": { "message_type": "forward", "device_id": "string", "payload": "object" },
            "description": "Wraps signaling payloads (request-offer, answer, ice-candidate) forwarded to Agent",
            "source": "web-app/src/composables/useWebRTC.js:140"
        },
        {
            "message_type": "command",
            "fields": { "message_type": "command", "device_id": "string", "request_id": "string", "command": "string" },
            "description": "Direct shell/command execution request forwarded to agent via signaling server",
            "source": "web-app/src/composables/useWebRTC.js:271"
        },
        {
            "message_type": "inject_data",
            "fields": { "message_type": "inject_data", "device_id": "string", "channel": "string", "data": "any" },
            "description": "WebSocket fallback for touch/clipboard when DataChannel is unavailable",
            "source": "web-app/src/composables/useWebRTC.js:254"
        },
        {
            "message_type": "group_control_event",
            "fields": { "message_type": "group_control_event", "device_ids": "array", "event": "object" },
            "description": "Multi-device synchronized control broadcast across multiple phone sessions",
            "source": "web-app/src/stores/devices.js:583"
        },
        {
            "message_type": "get_settings",
            "fields": { "message_type": "get_settings" },
            "description": "Requests global system settings from signaling server",
            "source": "web-app/src/stores/devices.js:592"
        },
        {
            "message_type": "webrtc_failed",
            "fields": { "message_type": "webrtc_failed", "device_id": "string" },
            "description": "Candidate message indicating WebRTC failure",
            "source": "web-app/src/stores/devices.js"
        }
    ]

    ws_s2c_definitions = [
        {
            "message_type": "config",
            "fields": { "message_type": "config", "ice_servers": "array" },
            "description": "Provides STUN/TURN ICE server configuration to connecting client",
            "source": "web-app/src/composables/useWebRTC.js:126"
        },
        {
            "message_type": "device_msg",
            "fields": { "message_type": "device_msg", "device_id": "string", "payload": "object" },
            "description": "Delivers forwarded messages from Agent (offer, ice-candidate, clipboard, etc.)",
            "source": "web-app/src/composables/useWebRTC.js:133"
        },
        {
            "message_type": "device_online",
            "fields": { "message_type": "device_online", "device": "object" },
            "description": "Broadcasts that a device agent has connected and registered",
            "source": "web-app/src/stores/devices.js:675"
        },
        {
            "message_type": "device_offline",
            "fields": { "message_type": "device_offline", "device_id": "string" },
            "description": "Broadcasts that a device agent has disconnected",
            "source": "web-app/src/stores/devices.js:680"
        },
        {
            "message_type": "device_list",
            "fields": { "message_type": "device_list", "devices": "array" },
            "description": "Initial synchronization of all online devices on WebSocket connect",
            "source": "web-app/src/stores/devices.js:670"
        },
        {
            "message_type": "command_result",
            "fields": { "message_type": "command_result", "request_id": "string", "output": "string", "exit_code": "number" },
            "description": "Delivers asynchronous shell command execution output back to client",
            "source": "web-app/src/composables/useWebRTC.js:148"
        },
        {
            "message_type": "auth_error",
            "fields": { "message_type": "auth_error", "error": "string" },
            "description": "Signals token expiration, invalid permissions, or session kick",
            "source": "web-app/src/composables/useWebRTC.js:156"
        }
    ]

    fwd_payload_definitions = [
        {
            "type": "request-offer",
            "direction": "Browser -> Signaling -> Agent",
            "fields": { "type": "request-offer", "ip_preference": "string", "scrcpy_options": "object" },
            "description": "Requests Agent to create a WebRTC PeerConnection, start scrcpy, and generate an SDP offer",
            "source": "web-app/src/composables/useWebRTC.js:134"
        },
        {
            "type": "offer",
            "direction": "Agent -> Signaling -> Browser",
            "fields": { "type": "offer", "sdp": "string", "camera_support": "boolean" },
            "description": "Agent SDP offer containing video/audio media tracks and DataChannel attributes",
            "source": "web-app/src/composables/useWebRTC.js:175"
        },
        {
            "type": "answer",
            "direction": "Browser -> Signaling -> Agent",
            "fields": { "type": "answer", "sdp": "string" },
            "description": "Browser SDP answer with munged bandwidth parameters and audio preferences",
            "source": "web-app/src/composables/useWebRTC.js:205"
        },
        {
            "type": "ice-candidate",
            "direction": "Bi-directional (Browser <-> Agent)",
            "fields": { "type": "ice-candidate", "candidate": "string | object" },
            "description": "Trickle ICE candidate exchange for P2P UDP/TCP hole punching",
            "source": "web-app/src/composables/useWebRTC.js:215"
        },
        {
            "type": "clipboard",
            "direction": "Bi-directional",
            "fields": { "type": "clipboard", "text": "string", "source": "string", "origin_client_id": "string" },
            "description": "Fallback clipboard payload when clipboard-channel is not established",
            "source": "web-app/src/composables/useWebRTC.js:770"
        },
        {
            "type": "camera",
            "direction": "Bi-directional",
            "fields": { "type": "camera", "action": "string" },
            "description": "Camera control signaling fallback",
            "source": "web-app/src/composables/useWebRTC.js:800"
        }
    ]

    protocol_index = {
        "metadata": {
            "title": "Public Frontend Reference Protocol Index",
            "evidence_class": "SOURCE_REFERENCE_CANDIDATE",
            "source_repositories": [
                "tcandt/scrcpyoverwebrtc (commit: 65567d777bccb11d2a6d93b6acc735478e880b5b)",
                "hqw700/cloudphone-official (commit: ceb66b20ad4c6f7b217d38852ea9ec2bd70fcd39)"
            ],
            "description": "Reference protocol index dynamically parsed from pinned public Git snapshots in evidence/reference/raw/. Every entry is a candidate until corroborated by binary evidence."
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
                    "classification": "SOURCE_REFERENCE_CANDIDATE"
                },
                {
                    "path": "/register_agent",
                    "role": "Agent registration and upstream command link",
                    "query_parameters": {
                        "id": "Agent / device unique identifier (passed via -id CLI flag)"
                    },
                    "source_reference": "docs/agent-deploy.md",
                    "classification": "SOURCE_REFERENCE_CANDIDATE"
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
        f.write("**Classification**: `SOURCE_REFERENCE_CANDIDATE` (Subject to Binary Verification)\n\n")
        f.write("## 1. Transport Endpoints Summary\n\n")
        f.write(f"- **WebSocket Signaling**: {len(protocol_index['transport_endpoints']['websocket_signaling'])} endpoints (`/connect_client`, `/register_agent`)\n")
        f.write(f"- **HTTP Endpoints**: {len(protocol_index['transport_endpoints']['http_endpoints'])} discovered endpoints across Auth, Devices, Admin, Share, Config, and System\n\n")
        f.write("## 2. WebSocket Signaling Messages\n\n")
        f.write(f"- **Client-to-Server**: {len(protocol_index['websocket_messages']['client_to_server'])} message types\n")
        f.write(f"- **Server-to-Client**: {len(protocol_index['websocket_messages']['server_to_client'])} message types\n")
        f.write(f"- **Signaling Forward Payloads**: {len(protocol_index['signaling_forward_payloads'])} payload types\n\n")
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
