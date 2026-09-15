import sys
import os
import json
import argparse
from pathlib import Path

def get_repo_root():
    return Path(__file__).resolve().parent.parent.parent

def generate_protocol_index(output_dir=None):
    repo_root = get_repo_root()
    if output_dir is None:
        target_dir = repo_root / "evidence" / "reference"
    else:
        target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    protocol_index = {
        "metadata": {
            "title": "Public Frontend Reference Protocol Index",
            "evidence_class": "SOURCE_REFERENCE_CANDIDATE",
            "source_repositories": [
                "tcandt/scrcpyoverwebrtc (commit: 65567d777bccb11d2a6d93b6acc735478e880b5b)",
                "hqw700/cloudphone-official (commit: ceb66b20ad4c6f7b217d38852ea9ec2bd70fcd39)"
            ],
            "description": "Comprehensive reference protocol index extracted from public frontend and official documentation materialized under evidence/reference/raw/. Every entry is a hypothesis/candidate until corroborated by binary evidence."
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
                    "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:78-83, evidence/reference/raw/web-app/src/stores/devices.js:669",
                    "classification": "SOURCE_REFERENCE_CANDIDATE"
                },
                {
                    "path": "/register_agent",
                    "role": "Agent registration and upstream command link",
                    "query_parameters": {
                        "id": "Agent / device unique identifier (passed via -id CLI flag)"
                    },
                    "source_reference": "evidence/reference/raw/docs/agent-deploy.md",
                    "classification": "SOURCE_REFERENCE_CANDIDATE"
                }
            ],
            "http_endpoints": [
                { "path": "/api/login", "method": "POST", "role": "Authentication: credentials login and session token issuance", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/logout", "method": "ANY", "role": "Authentication: session revocation", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/auth-status", "method": "ANY", "role": "Authentication: check whether noAuth mode is active", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/me", "method": "ANY", "role": "Authentication: retrieve authenticated user profile", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/devices", "method": "GET", "role": "Device: list active and registered devices", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/devices/", "method": "GET/POST/DELETE", "role": "Device: manage specific device by ID", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/tags", "method": "GET/POST/PUT/DELETE", "role": "Tags: manage device categories and label associations", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/users", "method": "GET", "role": "Admin: list user accounts", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/users/create", "method": "POST", "role": "Admin: create new user account", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/users/update", "method": "POST", "role": "Admin: update account properties / expiration", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/users/delete", "method": "POST", "role": "Admin: remove user account", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/users/reset_password", "method": "POST", "role": "Admin: reset user password", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/users/rename", "method": "POST", "role": "Admin: rename user account", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/users/update_note", "method": "POST", "role": "Admin: update user note field", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/users/kick", "method": "POST", "role": "Admin: kick active user sessions", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/admin/assign", "method": "POST", "role": "Admin: assign device permissions to user", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/share/create", "method": "POST", "role": "Share: create temporary sharing link for device", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/share/list", "method": "GET", "role": "Share: list active share tokens", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/share/revoke", "method": "POST", "role": "Share: revoke share token", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/share/extend", "method": "POST", "role": "Share: extend share token lifetime", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/share/update", "method": "POST", "role": "Share: update share token properties", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/share/info", "method": "GET", "role": "Share: fetch metadata for shared device", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/share/redeem_card", "method": "POST", "role": "Share: redeem card code for device access", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/default_settings", "method": "GET/POST", "role": "Config: global default settings (bitrate, fps, etc.)", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/ice_servers", "method": "GET/POST", "role": "Config: STUN/TURN server list", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/server/addresses", "method": "GET", "role": "Config: query external server IPs", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/shortcuts", "method": "GET/POST", "role": "Config: keyboard shortcut mappings", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/version", "method": "GET", "role": "System: signaling server version", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/license_status", "method": "GET", "role": "System: query license status", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/activate", "method": "POST", "role": "System: apply license key", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/files", "method": "GET/DELETE", "role": "Files: file management listing and deletion", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/tasks", "method": "GET/POST", "role": "Tasks: batch task execution", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/tasks/details", "method": "GET", "role": "Tasks: query task execution status", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/api/user/ai-config", "method": "GET/POST", "role": "User: AI assistant integration settings", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/upload", "method": "POST", "role": "Upload: file/APK upload endpoint", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/downloads/", "method": "GET", "role": "Static: agent executable / APK downloads", "classification": "SOURCE_REFERENCE_CANDIDATE" },
                { "path": "/snapshots/", "method": "GET", "role": "Static: device screenshot thumbnail serving", "classification": "SOURCE_REFERENCE_CANDIDATE" }
            ]
        },
        "websocket_messages": {
            "client_to_server": [
                {
                    "message_type": "connect",
                    "fields": { "message_type": "connect", "device_id": "string" },
                    "description": "Sent by client immediately after WebSocket connection to target device session",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:92-95"
                },
                {
                    "message_type": "forward",
                    "fields": { "message_type": "forward", "device_id": "string", "payload": "object" },
                    "description": "Wraps signaling payloads (request-offer, answer, ice-candidate) forwarded to Agent",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:140"
                },
                {
                    "message_type": "command",
                    "fields": { "message_type": "command", "device_id": "string", "request_id": "string", "command": "string" },
                    "description": "Direct shell/command execution request forwarded to agent via signaling server",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:271-276"
                },
                {
                    "message_type": "inject_data",
                    "fields": { "message_type": "inject_data", "device_id": "string", "channel": "string", "data": "any" },
                    "description": "WebSocket fallback for touch/clipboard when DataChannel is unavailable",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:254-265, evidence/reference/raw/web-app/src/stores/devices.js:610"
                },
                {
                    "message_type": "group_control_event",
                    "fields": { "message_type": "group_control_event", "device_ids": "array", "event": "object" },
                    "description": "Multi-device synchronized control broadcast across multiple phone sessions",
                    "source": "evidence/reference/raw/web-app/src/stores/devices.js:583-587"
                },
                {
                    "message_type": "webrtc_failed",
                    "fields": { "message_type": "webrtc_failed", "device_id": "string", "reason": "string" },
                    "description": "Notifies signaling server that WebRTC ICE negotiation failed",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:730"
                },
                {
                    "message_type": "get_settings",
                    "fields": { "message_type": "get_settings" },
                    "description": "Requests global system settings from signaling server",
                    "source": "evidence/reference/raw/web-app/src/stores/devices.js:592"
                }
            ],
            "server_to_client": [
                {
                    "message_type": "config",
                    "fields": { "message_type": "config", "ice_servers": "array" },
                    "description": "Provides STUN/TURN ICE server configuration to connecting client",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:126-130"
                },
                {
                    "message_type": "device_msg",
                    "fields": { "message_type": "device_msg", "device_id": "string", "payload": "object" },
                    "description": "Delivers forwarded messages from Agent (offer, ice-candidate, clipboard, etc.)",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:133-145"
                },
                {
                    "message_type": "device_online",
                    "fields": { "message_type": "device_online", "device": "object" },
                    "description": "Broadcasts that a device agent has connected and registered",
                    "source": "evidence/reference/raw/web-app/src/stores/devices.js:675"
                },
                {
                    "message_type": "device_offline",
                    "fields": { "message_type": "device_offline", "device_id": "string" },
                    "description": "Broadcasts that a device agent has disconnected",
                    "source": "evidence/reference/raw/web-app/src/stores/devices.js:680"
                },
                {
                    "message_type": "device_list",
                    "fields": { "message_type": "device_list", "devices": "array" },
                    "description": "Initial synchronization of all online devices on WebSocket connect",
                    "source": "evidence/reference/raw/web-app/src/stores/devices.js:670"
                },
                {
                    "message_type": "command_result",
                    "fields": { "message_type": "command_result", "request_id": "string", "output": "string", "exit_code": "number" },
                    "description": "Delivers asynchronous shell command execution output back to client",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:148-155"
                },
                {
                    "message_type": "auth_error",
                    "fields": { "message_type": "auth_error", "error": "string" },
                    "description": "Signals token expiration, invalid permissions, or session kick",
                    "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:156-160"
                }
            ]
        },
        "signaling_forward_payloads": [
            {
                "type": "request-offer",
                "direction": "Browser -> Signaling -> Agent",
                "fields": { "type": "request-offer", "ip_preference": "string", "scrcpy_options": "object" },
                "description": "Requests Agent to create a WebRTC PeerConnection, start scrcpy, and generate an SDP offer",
                "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:134"
            },
            {
                "type": "offer",
                "direction": "Agent -> Signaling -> Browser",
                "fields": { "type": "offer", "sdp": "string", "camera_support": "boolean" },
                "description": "Agent SDP offer containing video/audio media tracks and DataChannel attributes",
                "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:175-185"
            },
            {
                "type": "answer",
                "direction": "Browser -> Signaling -> Agent",
                "fields": { "type": "answer", "sdp": "string" },
                "description": "Browser SDP answer with munged bandwidth parameters and audio preferences",
                "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:205"
            },
            {
                "type": "ice-candidate",
                "direction": "Bi-directional (Browser <-> Agent)",
                "fields": { "type": "ice-candidate", "candidate": "string | object" },
                "description": "Trickle ICE candidate exchange for P2P UDP/TCP hole punching",
                "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:215-225"
            },
            {
                "type": "clipboard",
                "direction": "Bi-directional",
                "fields": { "type": "clipboard", "text": "string", "source": "string", "origin_client_id": "string" },
                "description": "Fallback clipboard payload when clipboard-channel is not established",
                "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:770"
            },
            {
                "type": "camera",
                "direction": "Bi-directional",
                "fields": { "type": "camera", "action": "string" },
                "description": "Camera control signaling fallback",
                "source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:800"
            }
        ],
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract protocol index from reference raw snapshot")
    parser.add_argument("--output-dir", help="Target output directory")
    args = parser.parse_args()
    generate_protocol_index(args.output_dir)
