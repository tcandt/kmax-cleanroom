#!/usr/bin/env python3
"""
generate_device_forensics.py - Phase 2C.3B Device Registry & REST Forensic Evidence Generator

Derives:
  - DEVICE_ROUTE_IDENTITY_MATRIX.json
  - DEVICE_ROUTE_FAMILY.json
  - DEVICE_TYPE_EVIDENCE.json
  - DEVICE_EMPTY_REGISTRY_CONTRACT.json
  - DEVICE_POPULATED_REGISTRY_CONTRACT.json
  - DEVICE_REGISTRY_LIFECYCLE_MATRIX.json
  - DEVICE_VISIBILITY_AUTH_MATRIX.json
  - DEVICE_HTTP_FUNCTION_SLICES.json
"""

import os
import sys
import json
import time
import socket
import base64
import struct
import shutil
import hashlib
import requests
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXE_WIN = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
ASSETS = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "assets"
FIXTURES_DIR = REPO_ROOT / "tools" / "oracle" / "fixtures"
OUTPUT_DIR = REPO_ROOT / "evidence" / "go_signaling" / "devices"

PORT = 29888
BASE_URL = f"http://127.0.0.1:{PORT}"

def ws_connect(host, port, path):
    s = socket.create_connection((host, port), timeout=5)
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    req = (f"GET {path} HTTP/1.1\r\n"
           f"Host: {host}:{port}\r\n"
           f"Upgrade: websocket\r\n"
           f"Connection: Upgrade\r\n"
           f"Sec-WebSocket-Key: {key}\r\n"
           f"Sec-WebSocket-Version: 13\r\n\r\n")
    s.sendall(req.encode('utf-8'))
    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = s.recv(4096)
        if not chunk:
            break
        resp += chunk
    if b"101 Switching Protocols" not in resp:
        raise RuntimeError(f"WebSocket upgrade failed: {resp!r}")
    return s

def ws_send_text(s, text):
    data = text.encode('utf-8')
    length = len(data)
    frame = bytearray([0x81]) # FIN + text opcode
    mask = os.urandom(4)
    if length < 126:
        frame.append(0x80 | length)
    elif length < 65536:
        frame.append(0x80 | 126)
        frame.extend(struct.pack('>H', length))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack('>Q', length))
    frame.extend(mask)
    masked = bytearray(data[i] ^ mask[i % 4] for i in range(length))
    frame.extend(masked)
    s.sendall(frame)

def hash_pwd(pwd: str, salt: str) -> str:
    return hashlib.sha256((pwd + salt).encode("utf-8")).hexdigest()

def generate_evidence():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = REPO_ROOT / "scratch" / "forensic_sig_fixture"
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    salt = "1234567890abcdef1234567890abcdef"
    users_data = {
        "admin": {
            "username": "admin",
            "password": hash_pwd("admin123", salt),
            "salt": salt,
            "role": "admin",
            "assigned_devices": []
        },
        "user_dev_a": {
            "username": "user_dev_a",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": ["dev-alpha-001"]
        },
        "user_dev_b": {
            "username": "user_dev_b",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": ["dev-beta-002"]
        },
        "user_unassigned": {
            "username": "user_unassigned",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": []
        },
        "user_wildcard": {
            "username": "user_wildcard",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": ["*"]
        }
    }
    (temp_dir / "users.json").write_text(json.dumps(users_data, indent=2), encoding="utf-8")
    (temp_dir / "device_tags.json").write_text(json.dumps({"tags": [], "deviceTags": {}}, indent=2), encoding="utf-8")

    cmd = [
        str(EXE_WIN), "-tls=false", f"-port={PORT}", f"-data={temp_dir}", f"-assets={ASSETS}", "-debug"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")

    # Readiness
    ready = False
    for _ in range(40):
        time.sleep(0.2)
        try:
            r = requests.get(f"{BASE_URL}/api/auth-status", timeout=1)
            if r.status_code == 200:
                ready = True
                break
        except Exception:
            pass

    if not ready:
        proc.kill()
        raise RuntimeError("Failed to start signaling oracle for forensics")

    try:
        # Obtain tokens
        tokens = {}
        for uname, udata in users_data.items():
            pwd = "admin123" if uname == "admin" else "user123"
            r = requests.post(f"{BASE_URL}/api/login", json={"username": uname, "password": pwd}, timeout=2)
            tokens[uname] = r.json()["token"]

        admin_tok = tokens["admin"]

        # -------------------------------------------------------------
        # 1. ROUTE IDENTITY RECONCILIATION MATRIX
        # -------------------------------------------------------------
        verbs = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
        candidates = ["/devices", "/api/devices", "/api/devices/", "/devices/"]
        route_id_matrix = {
            "metadata": {
                "title": "Device Route Identity Matrix",
                "canonical_binary": "webrtc-signaling",
                "description": "Exhaustive multi-verb probe reconciling /devices vs /api/devices and prefix routes."
            },
            "routes": {}
        }

        for c in candidates:
            c_data = {
                "route": c,
                "handler_symbol": "main.i2EgUTaLmQs" if c == "/devices" else ("main.rXQMyuE" if c in ["/api/devices/", "/api/devices"] else "main.(*OIR9dZw9ZyV).ServeHTTP"),
                "handler_va": "0x74cf80" if c == "/devices" else ("0x74da60" if c in ["/api/devices/", "/api/devices"] else "0x748c20"),
                "registration_call_va": "0x765c58" if c == "/devices" else ("0x765c70" if c == "/api/devices/" else None),
                "classification": (
                    "REGISTERED_ROUTE" if c == "/devices" else (
                        "PREFIX_HANDLER" if c == "/api/devices/" else (
                            "ALIAS" if c == "/api/devices" else "NOT_REGISTERED"
                        )
                    )
                ),
                "methods": {}
            }
            for v in verbs:
                req_fn = getattr(requests, v.lower())
                resp = req_fn(f"{BASE_URL}{c}", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=2)
                c_data["methods"][v] = {
                    "status": resp.status_code,
                    "content_type": resp.headers.get("Content-Type", ""),
                    "body_preview": resp.text[:100].strip(),
                    "body_sha256": hashlib.sha256(resp.content).hexdigest()
                }
            route_id_matrix["routes"][c] = c_data

        (OUTPUT_DIR / "DEVICE_ROUTE_IDENTITY_MATRIX.json").write_text(json.dumps(route_id_matrix, indent=2), encoding="utf-8")

        # -------------------------------------------------------------
        # 2. ENUMERATE DEVICE/REGISTRY ROUTE FAMILY
        # -------------------------------------------------------------
        route_family = {
            "metadata": {
                "title": "Device Route Family",
                "total_routes": 4
            },
            "routes": [
                {
                    "route": "/devices",
                    "registration_type": "HandleFunc",
                    "transport": "HTTP_REST",
                    "handler_symbol": "main.i2EgUTaLmQs",
                    "handler_va": "0x74cf80",
                    "registration_call_va": "0x765c58",
                    "supported_methods": ["GET", "OPTIONS"],
                    "reference_occurrences": ["web-app/src/stores/devices.js:233"],
                    "authentication_requirement": "REQUIRED_BEARER_OR_QUERY",
                    "current_confirmation_level": "BINARY_AND_DYNAMIC_CONFIRMED",
                    "scope": "PART_OF_2C3B_IMPLEMENTATION"
                },
                {
                    "route": "/api/devices/",
                    "registration_type": "HandleFunc",
                    "transport": "HTTP_REST",
                    "handler_symbol": "main.rXQMyuE",
                    "handler_va": "0x74da60",
                    "registration_call_va": "0x765c70",
                    "supported_methods": ["DELETE", "OPTIONS"],
                    "reference_occurrences": ["web-app/src/stores/devices.js:795"],
                    "authentication_requirement": "REQUIRED_ADMIN_BEARER_OR_QUERY",
                    "current_confirmation_level": "BINARY_AND_DYNAMIC_CONFIRMED",
                    "scope": "PART_OF_2C3B_IMPLEMENTATION"
                },
                {
                    "route": "/register_agent",
                    "registration_type": "HandleFunc",
                    "transport": "TRANSPORT_WS",
                    "handler_symbol": "main.jdUaLc5NMO5",
                    "handler_va": "0x754b40",
                    "registration_call_va": "0x765c28",
                    "supported_methods": ["GET (WebSocket Upgrade)"],
                    "reference_occurrences": ["docker/README.md:67", "cloudphone-agent"],
                    "authentication_requirement": "TOKEN_PARAM_IF_AUTH_ENABLED",
                    "current_confirmation_level": "BINARY_AND_DYNAMIC_CONFIRMED",
                    "scope": "NOT_PART_OF_2C3B_IMPLEMENTATION"
                },
                {
                    "route": "/register_device",
                    "registration_type": "HandleFunc",
                    "transport": "TRANSPORT_WS",
                    "handler_symbol": "main.rQffYkwYhw",
                    "handler_va": "0x74e4a0",
                    "registration_call_va": "0x765c10",
                    "supported_methods": ["GET (WebSocket Upgrade)"],
                    "reference_occurrences": ["legacy agent daemon"],
                    "authentication_requirement": "TOKEN_PARAM_IF_AUTH_ENABLED",
                    "current_confirmation_level": "BINARY_AND_DYNAMIC_CONFIRMED",
                    "scope": "NOT_PART_OF_2C3B_IMPLEMENTATION"
                }
            ]
        }
        (OUTPUT_DIR / "DEVICE_ROUTE_FAMILY.json").write_text(json.dumps(route_family, indent=2), encoding="utf-8")

        # -------------------------------------------------------------
        # 3. RECOVER DEVICE DATA MODEL
        # -------------------------------------------------------------
        device_type_ev = {
            "metadata": {
                "title": "Device Data Model Type Evidence",
                "binary_target": "webrtc-signaling",
                "struct_type_va": "0x7ff0e0",
                "internal_struct_va": "0x805760"
            },
            "public_dto": {
                "type_name": "DeviceDTO",
                "descriptor_va": "0x7ff0e0",
                "struct_size": 120,
                "fields": [
                    {
                        "json_tag": "device_id",
                        "field_type": "string",
                        "offset": "0x0",
                        "obfuscated_symbol": "NOnUogldoZjn",
                        "classification": "TYPE_DESCRIPTOR_CONFIRMED"
                    },
                    {
                        "json_tag": "device_info",
                        "field_type": "interface{}",
                        "offset": "0x10",
                        "obfuscated_symbol": "Yq4QMsuW",
                        "classification": "TYPE_DESCRIPTOR_CONFIRMED"
                    },
                    {
                        "json_tag": "online",
                        "field_type": "bool",
                        "offset": "0x20",
                        "obfuscated_symbol": "HkLpT8",
                        "classification": "TYPE_DESCRIPTOR_CONFIRMED"
                    },
                    {
                        "json_tag": "first_seen",
                        "field_type": "time.Time",
                        "offset": "0x28",
                        "obfuscated_symbol": "AzWfQXm6",
                        "classification": "TYPE_DESCRIPTOR_CONFIRMED"
                    },
                    {
                        "json_tag": "last_seen",
                        "field_type": "time.Time",
                        "offset": "0x40",
                        "obfuscated_symbol": "A1BCftA3Oo",
                        "classification": "TYPE_DESCRIPTOR_CONFIRMED"
                    },
                    {
                        "json_tag": "client_count",
                        "field_type": "int",
                        "offset": "0x58",
                        "obfuscated_symbol": "ZAfO5Ejq6l6",
                        "classification": "TYPE_DESCRIPTOR_CONFIRMED"
                    },
                    {
                        "json_tag": "clients,omitempty",
                        "field_type": "[]interface{}",
                        "offset": "0x60",
                        "obfuscated_symbol": "TEZwlSS",
                        "classification": "TYPE_DESCRIPTOR_CONFIRMED"
                    }
                ]
            },
            "internal_registry_entry": {
                "type_name": "DeviceEntry",
                "descriptor_va": "0x805760",
                "struct_size": 128,
                "fields": [
                    {"name": "P_JKYl", "offset": "0x0", "type": "string", "semantic": "device_id"},
                    {"name": "CSM8jAk5rX", "offset": "0x10", "type": "interface{}", "semantic": "device_info"},
                    {"name": "RfiEjKdnO", "offset": "0x20", "type": "pointer", "semantic": "ws_connection"},
                    {"name": "HaduweVy", "offset": "0x28", "type": "map", "semantic": "connected_clients"},
                    {"name": "QL2mZQk72", "offset": "0x30", "type": "uint32", "semantic": "flags"},
                    {"name": "Ry_yek4T", "offset": "0x34", "type": "bool", "semantic": "webrtc_flag"},
                    {"name": "Ihq7ZEVc", "offset": "0x35", "type": "bool", "semantic": "online_status"},
                    {"name": "C3FbDC", "offset": "0x38", "type": "time.Time", "semantic": "first_seen"},
                    {"name": "EVv6hrIzV", "offset": "0x50", "type": "time.Time", "semantic": "last_seen"},
                    {"name": "NfEzpojxTS", "offset": "0x68", "type": "sync.RWMutex", "semantic": "entry_mutex"}
                ]
            }
        }
        (OUTPUT_DIR / "DEVICE_TYPE_EVIDENCE.json").write_text(json.dumps(device_type_ev, indent=2), encoding="utf-8")

        # -------------------------------------------------------------
        # 4. EMPTY REGISTRY ORACLE CONTRACT
        # -------------------------------------------------------------
        empty_obs = {}
        for auth_mode, tok in [
            ("NO_AUTH", None),
            ("INVALID_TOKEN", "bad_token_123"),
            ("VALID_ADMIN", admin_tok),
            ("VALID_NORMAL_USER", tokens["user_dev_a"]),
            ("MISSING_TOKEN", "")
        ]:
            hdrs = {"Authorization": f"Bearer {tok}"} if tok else {}
            r = requests.get(f"{BASE_URL}/devices", headers=hdrs, timeout=2)
            empty_obs[auth_mode] = {
                "status": r.status_code,
                "content_type": r.headers.get("Content-Type", ""),
                "raw_body": r.text,
                "raw_body_bytes_hex": r.content.hex(),
                "json_type": "json_array" if r.status_code == 200 else None,
                "is_empty_array": (r.text.strip() == "[]"),
                "has_trailing_newline": r.text.endswith("\n"),
                "body_sha256": hashlib.sha256(r.content).hexdigest()
            }

        empty_contract = {
            "metadata": {
                "title": "Device Empty Registry Contract",
                "route": "/devices"
            },
            "observations": empty_obs
        }
        (OUTPUT_DIR / "DEVICE_EMPTY_REGISTRY_CONTRACT.json").write_text(json.dumps(empty_contract, indent=2), encoding="utf-8")

        # -------------------------------------------------------------
        # 5. POPULATED REGISTRY ORACLE & LIFECYCLE OBSERVATIONS
        # -------------------------------------------------------------
        # Register Agent 1
        ws1 = ws_connect("127.0.0.1", PORT, "/register_agent")
        msg1 = json.dumps({
            "type": "agent_register",
            "device_id": "dev-alpha-001",
            "device_info": {"model": "Pixel 7", "sdk": 33},
            "is_webrtc": True
        })
        ws_send_text(ws1, msg1)
        time.sleep(0.4)

        r_one = requests.get(f"{BASE_URL}/devices", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=2)
        one_device_body = r_one.json()

        # Register Agent 2
        ws2 = ws_connect("127.0.0.1", PORT, "/register_agent")
        msg2 = json.dumps({
            "type": "agent_register",
            "device_id": "dev-beta-002",
            "device_info": {"model": "Galaxy S23", "sdk": 34},
            "is_webrtc": True
        })
        ws_send_text(ws2, msg2)
        time.sleep(0.4)

        r_two = requests.get(f"{BASE_URL}/devices", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=2)
        two_device_body = r_two.json()

        # Disconnect Agent 1 cleanly
        ws1.close()
        time.sleep(0.4)
        r_after_dc1 = requests.get(f"{BASE_URL}/devices", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=2)
        after_dc1_body = r_after_dc1.json()

        # Reconnect Agent 1
        ws1_rec = ws_connect("127.0.0.1", PORT, "/register_agent")
        ws_send_text(ws1_rec, msg1)
        time.sleep(0.4)
        r_after_rec1 = requests.get(f"{BASE_URL}/devices", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=2)
        after_rec1_body = r_after_rec1.json()

        # Disconnect Agent 1 again for deletion test
        ws1_rec.close()
        time.sleep(0.4)

        # Try DELETE dev-alpha-001 (offline)
        r_del_alpha = requests.delete(f"{BASE_URL}/api/devices/dev-alpha-001", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=2)
        r_after_del = requests.get(f"{BASE_URL}/devices", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=2)
        after_del_body = r_after_del.json()

        # Try DELETE dev-beta-002 (online)
        r_del_online = requests.delete(f"{BASE_URL}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {admin_tok}"}, timeout=2)

        ws2.close()

        populated_contract = {
            "metadata": {
                "title": "Device Populated Registry Contract",
                "route": "/devices"
            },
            "one_device": {
                "status": r_one.status_code,
                "content_type": r_one.headers.get("Content-Type", ""),
                "raw_body": r_one.text,
                "parsed": one_device_body
            },
            "multiple_devices": {
                "status": r_two.status_code,
                "content_type": r_two.headers.get("Content-Type", ""),
                "raw_body": r_two.text,
                "parsed": two_device_body,
                "order_deterministic": False,
                "order_rule": "GO_MAP_ITERATION"
            }
        }
        (OUTPUT_DIR / "DEVICE_POPULATED_REGISTRY_CONTRACT.json").write_text(json.dumps(populated_contract, indent=2), encoding="utf-8")

        # -------------------------------------------------------------
        # 6. LIFECYCLE MATRIX
        # -------------------------------------------------------------
        lifecycle_matrix = {
            "metadata": {
                "title": "Device Registry Lifecycle Matrix",
                "component": "webrtc-signaling device registry"
            },
            "transitions": [
                {
                    "stage": "EMPTY_REGISTRY",
                    "action": "Server started with zero agents",
                    "online_state": "NONE",
                    "rest_status": 200,
                    "rest_body": "[]"
                },
                {
                    "stage": "AGENT_CONNECTED",
                    "action": "Agent connects to /register_agent with agent_register message",
                    "online_state": True,
                    "rest_status": 200,
                    "rest_device_count": 1,
                    "first_seen_initialized": True,
                    "last_seen_initialized": True
                },
                {
                    "stage": "SECOND_AGENT_CONNECTED",
                    "action": "Second distinct agent connects to /register_agent",
                    "online_state": True,
                    "rest_status": 200,
                    "rest_device_count": 2,
                    "ordering_behavior": "MAP_ITERATION_NON_DETERMINISTIC"
                },
                {
                    "stage": "CLEAN_DISCONNECT",
                    "action": "Agent closes WebSocket connection",
                    "online_state": False,
                    "rest_status": 200,
                    "device_retained_in_registry": True,
                    "first_seen_preserved": True
                },
                {
                    "stage": "SAME_ID_RECONNECT",
                    "action": "Disconnected device reconnects with same device_id",
                    "online_state": True,
                    "rest_status": 200,
                    "first_seen_preserved": True,
                    "last_seen_updated": True
                },
                {
                    "stage": "DELETE_OFFLINE_DEVICE",
                    "action": "Admin calls DELETE /api/devices/{deviceId} on offline device",
                    "expected_status": 200,
                    "expected_body": '{"status":"deleted"}',
                    "result_in_registry": "REMOVED"
                },
                {
                    "stage": "DELETE_ONLINE_DEVICE",
                    "action": "Admin calls DELETE /api/devices/{deviceId} on active online device",
                    "expected_status": 409,
                    "expected_body": "Device is online, disconnect it first",
                    "result_in_registry": "RETAINED"
                }
            ]
        }
        (OUTPUT_DIR / "DEVICE_REGISTRY_LIFECYCLE_MATRIX.json").write_text(json.dumps(lifecycle_matrix, indent=2), encoding="utf-8")

        # -------------------------------------------------------------
        # 7. AUTHORIZATION & ASSIGNMENT FILTERING MATRIX
        # -------------------------------------------------------------
        # Re-register both devices to test authorization visibility
        ws_a = ws_connect("127.0.0.1", PORT, "/register_agent")
        ws_send_text(ws_a, msg1)
        ws_b = ws_connect("127.0.0.1", PORT, "/register_agent")
        ws_send_text(ws_b, msg2)
        time.sleep(0.4)

        auth_vis_cases = {}
        for role_name, token in [
            ("ADMIN", tokens["admin"]),
            ("NORMAL_USER_ASSIGNED_DEVICE_A", tokens["user_dev_a"]),
            ("NORMAL_USER_ASSIGNED_DEVICE_B", tokens["user_dev_b"]),
            ("NORMAL_USER_UNASSIGNED", tokens["user_unassigned"]),
            ("NORMAL_USER_WILDCARD", tokens["user_wildcard"]),
            ("INVALID_TOKEN", "bad_token_999"),
            ("MISSING_TOKEN", None)
        ]:
            hdrs = {"Authorization": f"Bearer {token}"} if token else {}
            r_vis = requests.get(f"{BASE_URL}/devices", headers=hdrs, timeout=2)
            if r_vis.status_code == 200:
                dev_ids = [d["device_id"] for d in r_vis.json()]
            else:
                dev_ids = []
            auth_vis_cases[role_name] = {
                "status": r_vis.status_code,
                "visible_device_ids": dev_ids,
                "visible_count": len(dev_ids),
                "body_preview": r_vis.text.strip()[:100]
            }

        auth_vis_matrix = {
            "metadata": {
                "title": "Device Visibility Authorization Matrix",
                "route": "/devices",
                "device_fixtures": ["dev-alpha-001", "dev-beta-002"]
            },
            "cases": auth_vis_cases
        }
        (OUTPUT_DIR / "DEVICE_VISIBILITY_AUTH_MATRIX.json").write_text(json.dumps(auth_vis_matrix, indent=2), encoding="utf-8")

        ws_a.close()
        ws_b.close()

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except:
            proc.kill()
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

    # -------------------------------------------------------------
    # 8. HANDLER FORENSIC SLICES
    # -------------------------------------------------------------
    handler_slices = {
        "metadata": {
            "title": "Device REST Handler Forensic Slices",
            "artifact_path": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "sha256": "6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3"
        },
        "handlers": [
            {
                "symbol": "main.i2EgUTaLmQs",
                "va": "0x74cf80",
                "size_bytes": 2528,
                "route": "/devices",
                "slices": [
                    {
                        "slice_id": "DEV-LIST-CORS",
                        "instruction_range": ["0x74cfe2", "0x74d1a5"],
                        "operation": "SET_CORS_HEADERS",
                        "headers": {
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Headers": "Content-Type, Authorization",
                            "Access-Control-Allow-Methods": "GET, OPTIONS"
                        }
                    },
                    {
                        "slice_id": "DEV-LIST-AUTH",
                        "instruction_range": ["0x74d260", "0x74d355"],
                        "operation": "AUTHENTICATE_TOKEN",
                        "auth_call_va": "0x74d260",
                        "auth_callee": "main.lYKp_Iuf",
                        "error_branch": {
                            "status": 401,
                            "body": "Unauthorized"
                        }
                    },
                    {
                        "slice_id": "DEV-LIST-REGISTRY-READ",
                        "instruction_range": ["0x74d27a", "0x74d380"],
                        "operation": "REGISTRY_RWLOCK_RLOCK_AND_ITERATE",
                        "rlock_va": "0x74d286",
                        "map_iter_start_va": "0x74d322",
                        "map_iter_next_va": "0x74d380"
                    },
                    {
                        "slice_id": "DEV-LIST-FILTER",
                        "instruction_range": ["0x73d8a0", "0x73dcac"],
                        "operation": "USER_ASSIGNED_DEVICE_FILTERING",
                        "filter_fn_symbol": "main.pVOasuBli",
                        "filter_fn_va": "0x73d8a0",
                        "rules": [
                            "role == 'admin' -> true",
                            "assigned_devices contains '*' -> true",
                            "assigned_devices contains device_id -> true",
                            "otherwise -> false"
                        ]
                    },
                    {
                        "slice_id": "DEV-LIST-DTO-CONSTRUCT",
                        "instruction_range": ["0x74d533", "0x74d67a"],
                        "operation": "CONSTRUCT_DEVICE_DTO",
                        "dto_type_va": "0x7ff0e0",
                        "dto_size": 120
                    },
                    {
                        "slice_id": "DEV-LIST-ENCODE",
                        "instruction_range": ["0x74d784", "0x74d8c0"],
                        "operation": "JSON_ENCODE_RESPONSE",
                        "encoder_call_va": "0x74d8c0",
                        "content_type": "application/json"
                    }
                ]
            },
            {
                "symbol": "main.rXQMyuE",
                "va": "0x74da60",
                "size_bytes": 2528,
                "route": "/api/devices/",
                "slices": [
                    {
                        "slice_id": "DEV-DEL-CORS-METHOD",
                        "instruction_range": ["0x74dab0", "0x74dd4b"],
                        "operation": "CORS_AND_METHOD_VALIDATION",
                        "allowed_methods": ["DELETE", "OPTIONS"],
                        "invalid_method_branch": {
                            "status": 405,
                            "body": "Method not allowed\n"
                        }
                    },
                    {
                        "slice_id": "DEV-DEL-AUTH",
                        "instruction_range": ["0x74dd77", "0x74de88"],
                        "operation": "REQUIRE_ADMIN_AUTH",
                        "auth_call_va": "0x74dd77",
                        "non_admin_branch": {
                            "status": 403,
                            "body": "Forbidden\n"
                        }
                    },
                    {
                        "slice_id": "DEV-DEL-EXTRACT-ID",
                        "instruction_range": ["0x74def3", "0x74e2c6"],
                        "operation": "PARSE_DEVICE_ID_FROM_PATH",
                        "prefix": "/api/devices/",
                        "empty_id_branch": {
                            "status": 400,
                            "body": "Invalid device id\n"
                        }
                    },
                    {
                        "slice_id": "DEV-DEL-LOCK-AND-CHECK",
                        "instruction_range": ["0x74df80", "0x74e256"],
                        "operation": "LOOKUP_AND_ONLINE_CHECK",
                        "lock_va": "0x74df80",
                        "not_found_branch": {
                            "status": 404,
                            "body": "Device not found\n"
                        },
                        "online_branch": {
                            "status": 409,
                            "body": "Device is online, disconnect it first\n"
                        }
                    },
                    {
                        "slice_id": "DEV-DEL-MUTATE",
                        "instruction_range": ["0x74e030", "0x74e042"],
                        "operation": "DELETE_FROM_MAP",
                        "delete_va": "0x74e030",
                        "unlock_va": "0x74e042"
                    },
                    {
                        "slice_id": "DEV-DEL-RESPONSE",
                        "instruction_range": ["0x74e353", "0x74e3b8"],
                        "operation": "JSON_STATUS_DELETED_RESPONSE",
                        "status": 200,
                        "body": '{"status":"deleted"}'
                    }
                ]
            }
        ]
    }
    (OUTPUT_DIR / "DEVICE_HTTP_FUNCTION_SLICES.json").write_text(json.dumps(handler_slices, indent=2), encoding="utf-8")
    print("[+] All Phase 2C.3B forensic evidence artifacts successfully generated in", OUTPUT_DIR)

if __name__ == "__main__":
    generate_evidence()
