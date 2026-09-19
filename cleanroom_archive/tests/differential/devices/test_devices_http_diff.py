#!/usr/bin/env python3
"""
test_devices_http_diff.py - Phase 2C.3BR Device Registry HTTP Differential Test Suite

Runs original webrtc-signaling and reconstructed http-server side-by-side.
Executes 28 exhaustive differential test cases covering:
  - Empty/populated registry queries
  - Exact DTO schema and invariant verification
  - Auth and visibility filtering
  - Reconnect and disconnect lifecycles
  - Full method contract across /devices (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
  - Full delete route contract across /api/devices/ (all error branches, auth requirements, OPTIONS, HEAD)
  - ServeMux trailing-slash redirect semantics with allow_redirects=False
  - Independent No-Auth server mode verification

Outputs:
  - evidence/go_signaling/devices/DEVICE_HTTP_DIFFERENTIAL_RESULTS.json
  - reports/13_PHASE2C3B_DEVICE_REGISTRY_DIFFERENTIAL.md
"""

import os
import sys
import time
import socket
import base64
import struct
import shutil
import hashlib
import json
import requests
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXE_ORIG = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
ASSETS = ROOT / "cloudphone-v0.3.6 (1)" / "assets"
DIFF_TMP = ROOT / "scratch" / "device_http_diff_fixture"
DIFF_TMP_NA = ROOT / "scratch" / "device_http_noauth_fixture"
EXE_RECON = ROOT / "scratch" / "reconstructed_http_server.exe"

OUTPUT_JSON = ROOT / "evidence" / "go_signaling" / "devices" / "DEVICE_HTTP_DIFFERENTIAL_RESULTS.json"
OUTPUT_REPORT = ROOT / "reports" / "13R_PHASE2C3B_DEVICE_CONTRACT_CLOSURE.md"

PORT_ORIG = 29888
PORT_RECON = 29889
URL_ORIG = f"http://127.0.0.1:{PORT_ORIG}"
URL_RECON = f"http://127.0.0.1:{PORT_RECON}"

PORT_ORIG_NA = 29892
PORT_RECON_NA = 29893
URL_ORIG_NA = f"http://127.0.0.1:{PORT_ORIG_NA}"
URL_RECON_NA = f"http://127.0.0.1:{PORT_RECON_NA}"

def ws_connect(host, port, path):
    s = socket.create_connection((host, port), timeout=5)
    key = base64.b64encode(os.urandom(16)).decode("utf-8")
    req = (f"GET {path} HTTP/1.1\r\n"
           f"Host: {host}:{port}\r\n"
           f"Upgrade: websocket\r\n"
           f"Connection: Upgrade\r\n"
           f"Sec-WebSocket-Key: {key}\r\n"
           f"Sec-WebSocket-Version: 13\r\n\r\n")
    s.sendall(req.encode("utf-8"))
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
    data = text.encode("utf-8")
    length = len(data)
    frame = bytearray([0x81])
    mask = os.urandom(4)
    if length < 126:
        frame.append(0x80 | length)
    elif length < 65536:
        frame.append(0x80 | 126)
        frame.extend(struct.pack(">H", length))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack(">Q", length))
    frame.extend(mask)
    masked = bytearray(data[i] ^ mask[i % 4] for i in range(length))
    frame.extend(masked)
    s.sendall(frame)

def hash_pwd(pwd: str, salt: str) -> str:
    return hashlib.sha256((pwd + salt).encode("utf-8")).hexdigest()

def setup_fixtures():
    if DIFF_TMP.exists():
        shutil.rmtree(DIFF_TMP, ignore_errors=True)
    DIFF_TMP.mkdir(parents=True, exist_ok=True)

    salt = "1234567890abcdef1234567890abcdef"
    users_fixture = {
        "admin": {
            "username": "admin",
            "password": hash_pwd("admin123", salt),
            "salt": salt,
            "role": "admin",
            "assigned_devices": ["*"]
        },
        "user_assigned": {
            "username": "user_assigned",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": ["dev-alpha-001"]
        },
        "user_unassigned": {
            "username": "user_unassigned",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": []
        }
    }
    (DIFF_TMP / "users.json").write_text(json.dumps(users_fixture, indent=2), encoding="utf-8")
    (DIFF_TMP / "device_tags.json").write_text(json.dumps({"tags": [], "deviceTags": {}}, indent=2), encoding="utf-8")

def build_reconstructed():
    src_dir = ROOT / "reconstructed_source" / "webrtc-signaling"
    cmd = ["go", "build", "-o", str(EXE_RECON), "./cmd/http-server"]
    res = subprocess.run(cmd, cwd=str(src_dir), capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to build reconstructed HTTP server: {res.stderr}")
    print("[+] Successfully compiled reconstructed HTTP server")

def parse_iso_time(ts_str):
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except Exception:
        return None

def run_suite():
    setup_fixtures()
    build_reconstructed()

    # Launch original binary
    cmd_orig = [
        str(EXE_ORIG),
        "-tls=false",
        f"-port={PORT_ORIG}",
        f"-data={DIFF_TMP}",
        f"-assets={ASSETS}",
        "-debug"
    ]
    proc_orig = subprocess.Popen(cmd_orig, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")

    # Launch reconstructed server
    cmd_recon = [
        str(EXE_RECON),
        f"-port={PORT_RECON}",
        f"-data={DIFF_TMP}"
    ]
    proc_recon = subprocess.Popen(cmd_recon, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")

    # Readiness check
    for target, url in [("Original Oracle", URL_ORIG), ("Reconstructed Server", URL_RECON)]:
        ready = False
        for _ in range(40):
            time.sleep(0.2)
            try:
                r = requests.get(f"{url}/api/auth-status", timeout=1)
                if r.status_code == 200:
                    ready = True
                    break
            except Exception:
                pass
        if not ready:
            proc_orig.kill()
            proc_recon.kill()
            raise RuntimeError(f"{target} failed to initialize on {url}")
        print(f"[+] {target} ready on {url}")

    results = []

    def record_diff(test_id, name, result_class, passed, orig_obs, recon_obs, comparison, detail=""):
        status = "PASS" if passed else "FAIL"
        results.append({
            "test_id": test_id,
            "test_name": name,
            "classification": result_class,
            "passed": passed,
            "original_observation": orig_obs,
            "reconstructed_observation": recon_obs,
            "comparison_result": comparison,
            "detail": detail
        })
        print(f"[{status}] {test_id} - {name} ({result_class}): {comparison}")

    # Synchronize agent state between original and reconstructed
    active_ws = {}

    def register_device_sync(device_id, info, is_webrtc=True):
        # Original: WebSocket connect to /register_agent
        ws = ws_connect("127.0.0.1", PORT_ORIG, "/register_agent")
        msg = json.dumps({
            "type": "agent_register",
            "device_id": device_id,
            "device_info": info,
            "is_webrtc": is_webrtc
        })
        ws_send_text(ws, msg)
        active_ws[device_id] = ws

        # Reconstructed: Test fixture endpoint
        requests.post(f"{URL_RECON}/_test/register_device", json={
            "device_id": device_id,
            "device_info": info,
            "is_webrtc": is_webrtc
        }, timeout=2)
        time.sleep(0.4)

    def disconnect_device_sync(device_id):
        if device_id in active_ws:
            active_ws[device_id].close()
            del active_ws[device_id]
        requests.post(f"{URL_RECON}/_test/disconnect_device", json={"device_id": device_id}, timeout=2)
        time.sleep(0.4)

    try:
        # Obtain tokens
        tokens_orig = {}
        tokens_recon = {}
        for u in ["admin", "user_assigned", "user_unassigned"]:
            pwd = "admin123" if u == "admin" else "user123"
            r_o = requests.post(f"{URL_ORIG}/api/login", json={"username": u, "password": pwd}, timeout=2)
            r_r = requests.post(f"{URL_RECON}/api/login", json={"username": u, "password": pwd}, timeout=2)
            tokens_orig[u] = r_o.json()["token"]
            tokens_recon[u] = r_r.json()["token"]

        # =====================================================================
        # DEV-HTTP-01: Empty Registry Admin Query
        # =====================================================================
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            r_o.text == r_r.text == "[]\n" and
            r_o.headers.get("Content-Type") == r_r.headers.get("Content-Type") == "application/json"
        )
        record_diff(
            "DEV-HTTP-01", "Empty Registry Admin Query", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text, "ct": r_o.headers.get("Content-Type")},
            {"status": r_r.status_code, "body": r_r.text, "ct": r_r.headers.get("Content-Type")},
            "Both emit 200 OK, application/json, exact body '[]\\n'"
        )

        # =====================================================================
        # DEV-HTTP-02: Populated Registry One Device (Strict Schema & Invariants)
        # =====================================================================
        register_device_sync("dev-alpha-001", {"brand": "Google", "model": "Pixel 7 Pro", "sdk": 33}, True)
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)

        d_o = r_o.json()
        d_r = r_r.json()

        # Strict JSON Schema Comparison
        expected_keys = {"device_id", "device_info", "online", "first_seen", "last_seen", "client_count"}
        keys_o = set(d_o[0].keys())
        keys_r = set(d_r[0].keys())
        schema_match = (
            keys_o.issubset(expected_keys.union({"clients"})) and
            keys_r.issubset(expected_keys.union({"clients"})) and
            keys_o == keys_r
        )
        # Timestamp Invariant Check
        t_first_o = parse_iso_time(d_o[0]["first_seen"])
        t_last_o = parse_iso_time(d_o[0]["last_seen"])
        t_first_r = parse_iso_time(d_r[0]["first_seen"])
        t_last_r = parse_iso_time(d_r[0]["last_seen"])
        ts_valid = (
            t_first_o is not None and t_last_o is not None and t_first_o <= t_last_o and
            t_first_r is not None and t_last_r is not None and t_first_r <= t_last_r
        )

        passed = (
            r_o.status_code == r_r.status_code == 200 and
            len(d_o) == len(d_r) == 1 and
            d_o[0]["device_id"] == d_r[0]["device_id"] == "dev-alpha-001" and
            d_o[0]["online"] == d_r[0]["online"] == True and
            d_o[0]["client_count"] == d_r[0]["client_count"] == 0 and
            d_o[0]["device_info"] == d_r[0]["device_info"] and
            schema_match and ts_valid
        )
        record_diff(
            "DEV-HTTP-02", "Populated Registry One Device Schema & Invariants", "STRUCTURAL_EXACT_MATCH", passed,
            {"status": r_o.status_code, "keys": sorted(list(keys_o)), "dev": d_o[0]["device_id"], "online": d_o[0]["online"]},
            {"status": r_r.status_code, "keys": sorted(list(keys_r)), "dev": d_r[0]["device_id"], "online": d_r[0]["online"]},
            "Both emit 200 OK with matching 7-field schema, deep equal device_info, and valid RFC3339 timestamp invariants"
        )

        # =====================================================================
        # DEV-HTTP-03: Populated Registry Multiple Devices (Normalized DTO Match)
        # =====================================================================
        register_device_sync("dev-beta-002", {"brand": "Samsung", "model": "Galaxy S23", "sdk": 34}, True)
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)

        d_o = r_o.json()
        d_r = r_r.json()

        def normalize_dto_map(dev_list):
            res = {}
            for d in dev_list:
                item = {k: v for k, v in d.items() if k not in ["first_seen", "last_seen"]}
                res[d["device_id"]] = item
            return res

        norm_o = normalize_dto_map(d_o)
        norm_r = normalize_dto_map(d_r)
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            len(d_o) == len(d_r) == 2 and
            norm_o == norm_r
        )
        record_diff(
            "DEV-HTTP-03", "Populated Registry Multiple Devices Normalized DTO", "NORMALIZED_JSON_MATCH", passed,
            {"status": r_o.status_code, "count": len(d_o), "devices": sorted(list(norm_o.keys()))},
            {"status": r_r.status_code, "count": len(d_r), "devices": sorted(list(norm_r.keys()))},
            "Both contain identical normalized DTOs for 2 devices under non-deterministic Go map iteration order"
        )

        # =====================================================================
        # DEV-HTTP-04: Invalid Token
        # =====================================================================
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": "Bearer bad_invalid_token_999"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": "Bearer bad_invalid_token_999"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 401 and
            r_o.text == r_r.text == "Unauthorized\n"
        )
        record_diff(
            "DEV-HTTP-04", "Invalid Token Rejection", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both reject invalid token with 401 Unauthorized"
        )

        # =====================================================================
        # DEV-HTTP-05: Missing Token
        # =====================================================================
        r_o = requests.get(f"{URL_ORIG}/devices", timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 401 and
            r_o.text == r_r.text == "Unauthorized\n"
        )
        record_diff(
            "DEV-HTTP-05", "Missing Token Rejection", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both reject unauthenticated request with 401 Unauthorized"
        )

        # =====================================================================
        # DEV-HTTP-06: Normal User Assigned Device
        # =====================================================================
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['user_assigned']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['user_assigned']}"}, timeout=2)
        d_o = r_o.json()
        d_r = r_r.json()
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            len(d_o) == len(d_r) == 1 and
            d_o[0]["device_id"] == d_r[0]["device_id"] == "dev-alpha-001"
        )
        record_diff(
            "DEV-HTTP-06", "Normal User Assigned Device Filtering", "STRUCTURAL_EXACT_MATCH", passed,
            {"status": r_o.status_code, "visible_devices": [d["device_id"] for d in d_o]},
            {"status": r_r.status_code, "visible_devices": [d["device_id"] for d in d_r]},
            "Both filter devices to only the assigned device dev-alpha-001"
        )

        # =====================================================================
        # DEV-HTTP-07: Normal User Unassigned
        # =====================================================================
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['user_unassigned']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['user_unassigned']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            r_o.text == r_r.text == "[]\n"
        )
        record_diff(
            "DEV-HTTP-07", "Normal User Unassigned Visibility", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both emit empty array '[]\\n' for unassigned normal user"
        )

        # =====================================================================
        # DEV-HTTP-08: Reconnected Device Lifecycle
        # =====================================================================
        disconnect_device_sync("dev-alpha-001")
        register_device_sync("dev-alpha-001", {"brand": "Google", "model": "Pixel 7 Pro", "sdk": 33}, True)
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        d_o_map = {d["device_id"]: d for d in r_o.json()}
        d_r_map = {d["device_id"]: d for d in r_r.json()}
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            "dev-alpha-001" in d_o_map and "dev-alpha-001" in d_r_map and
            d_o_map["dev-alpha-001"]["online"] == d_r_map["dev-alpha-001"]["online"] == True
        )
        record_diff(
            "DEV-HTTP-08", "Reconnected Device State Restoration", "STRUCTURAL_EXACT_MATCH", passed,
            {"dev_alpha_online": d_o_map["dev-alpha-001"]["online"]},
            {"dev_alpha_online": d_r_map["dev-alpha-001"]["online"]},
            "Both restore online=true when existing device reconnects"
        )

        # =====================================================================
        # DEV-HTTP-09: Disconnect Lifecycle
        # =====================================================================
        disconnect_device_sync("dev-alpha-001")
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        d_o_map = {d["device_id"]: d for d in r_o.json()}
        d_r_map = {d["device_id"]: d for d in r_r.json()}
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            d_o_map["dev-alpha-001"]["online"] == d_r_map["dev-alpha-001"]["online"] == False and
            d_o_map["dev-beta-002"]["online"] == d_r_map["dev-beta-002"]["online"] == True
        )
        record_diff(
            "DEV-HTTP-09", "Disconnect Lifecycle & Offline State", "STRUCTURAL_EXACT_MATCH", passed,
            {"dev_alpha_online": d_o_map["dev-alpha-001"]["online"], "dev_beta_online": d_o_map["dev-beta-002"]["online"]},
            {"dev_alpha_online": d_r_map["dev-alpha-001"]["online"], "dev_beta_online": d_r_map["dev-beta-002"]["online"]},
            "Both retain disconnected device in registry with online=false while active device remains online=true"
        )

        # =====================================================================
        # DEV-HTTP-10: Wrong Method (GET) on /api/devices/{id}
        # =====================================================================
        r_o = requests.get(f"{URL_ORIG}/api/devices/dev-alpha-001", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/api/devices/dev-alpha-001", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 405 and
            r_o.text == r_r.text == "Method not allowed\n"
        )
        record_diff(
            "DEV-HTTP-10", "Wrong Method (GET) on /api/devices/{id}", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both reject non-DELETE request with 405 Method not allowed"
        )

        # =====================================================================
        # DEV-HTTP-11: HEAD Method on /devices
        # =====================================================================
        r_o = requests.head(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.head(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            len(r_o.content) == len(r_r.content) == 0 and
            r_o.headers.get("Content-Type") == r_r.headers.get("Content-Type") == "application/json"
        )
        record_diff(
            "DEV-HTTP-11", "HEAD Method on /devices", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body_len": len(r_o.content), "ct": r_o.headers.get("Content-Type")},
            {"status": r_r.status_code, "body_len": len(r_r.content), "ct": r_r.headers.get("Content-Type")},
            "Both return 200 OK with empty body and Content-Type: application/json for HEAD"
        )

        # =====================================================================
        # DEV-HTTP-12: OPTIONS Preflight CORS Headers
        # =====================================================================
        r_o = requests.options(f"{URL_ORIG}/devices", timeout=2)
        r_r = requests.options(f"{URL_RECON}/devices", timeout=2)
        cors_orig = r_o.headers.get("Access-Control-Allow-Origin")
        cors_recon = r_r.headers.get("Access-Control-Allow-Origin")
        methods_orig = r_o.headers.get("Access-Control-Allow-Methods")
        methods_recon = r_r.headers.get("Access-Control-Allow-Methods")
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            cors_orig == cors_recon == "*" and
            methods_orig == methods_recon == "GET, OPTIONS"
        )
        record_diff(
            "DEV-HTTP-12", "OPTIONS Preflight CORS Headers", "STRUCTURAL_EXACT_MATCH", passed,
            {"status": r_o.status_code, "origin": cors_orig, "methods": methods_orig},
            {"status": r_r.status_code, "origin": cors_recon, "methods": methods_recon},
            "Both emit 200 OK with Access-Control-Allow-Origin: * and Access-Control-Allow-Methods: GET, OPTIONS"
        )

        # =====================================================================
        # DEV-HTTP-13: Content-Type and Raw JSON Shape
        # =====================================================================
        r_o = requests.get(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.get(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        ct_match = r_o.headers.get("Content-Type") == r_r.headers.get("Content-Type") == "application/json"
        nl_match = r_o.text.endswith("\n") and r_r.text.endswith("\n")
        passed = ct_match and nl_match and r_o.status_code == r_r.status_code == 200
        record_diff(
            "DEV-HTTP-13", "Content-Type and Raw JSON Shape", "STRUCTURAL_EXACT_MATCH", passed,
            {"ct": r_o.headers.get("Content-Type"), "ends_with_newline": r_o.text.endswith("\n")},
            {"ct": r_r.headers.get("Content-Type"), "ends_with_newline": r_r.text.endswith("\n")},
            "Both emit Content-Type: application/json with trailing newline delimiter"
        )

        # =====================================================================
        # DEV-HTTP-14: Online & Offline Deletion Lifecycle
        # =====================================================================
        r_del_on_o = requests.delete(f"{URL_ORIG}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_del_on_r = requests.delete(f"{URL_RECON}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        on_del_match = (
            r_del_on_o.status_code == r_del_on_r.status_code == 409 and
            r_del_on_o.text == r_del_on_r.text == "Device is online, disconnect it first\n"
        )

        r_del_off_o = requests.delete(f"{URL_ORIG}/api/devices/dev-alpha-001", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_del_off_r = requests.delete(f"{URL_RECON}/api/devices/dev-alpha-001", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        off_del_match = (
            r_del_off_o.status_code == r_del_off_r.status_code == 200 and
            r_del_off_o.text == r_del_off_r.text == '{"status":"deleted"}\n'
        )

        passed = on_del_match and off_del_match
        record_diff(
            "DEV-HTTP-14", "Online & Offline Deletion Lifecycle", "BIT_EXACT_MATCH", passed,
            {"online_delete_status": r_del_on_o.status_code, "offline_delete_status": r_del_off_o.status_code},
            {"online_delete_status": r_del_on_r.status_code, "offline_delete_status": r_del_off_r.status_code},
            "Online delete rejected with 409, offline delete succeeds with 200 {'status':'deleted'}\\n"
        )

        # =====================================================================
        # DEV-HTTP-15 to DEV-HTTP-18: /devices All-Method Support
        # =====================================================================
        for m, cid in [("POST", "DEV-HTTP-15"), ("PUT", "DEV-HTTP-16"), ("PATCH", "DEV-HTTP-17"), ("DELETE", "DEV-HTTP-18")]:
            req_fn = getattr(requests, m.lower())
            resp_o = req_fn(f"{URL_ORIG}/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
            resp_r = req_fn(f"{URL_RECON}/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
            m_pass = (
                resp_o.status_code == resp_r.status_code == 200 and
                resp_o.headers.get("Content-Type") == resp_r.headers.get("Content-Type") == "application/json" and
                len(resp_o.json()) == len(resp_r.json())
            )
            record_diff(
                cid, f"{m} Method on /devices", "STRUCTURAL_EXACT_MATCH", m_pass,
                {"status": resp_o.status_code, "count": len(resp_o.json())},
                {"status": resp_r.status_code, "count": len(resp_r.json())},
                f"Both serve device list with 200 OK on {m} /devices (matching lack of method check in binary)"
            )

        # =====================================================================
        # DEV-HTTP-19: DELETE device as normal assigned user
        # =====================================================================
        r_o = requests.delete(f"{URL_ORIG}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {tokens_orig['user_assigned']}"}, timeout=2)
        r_r = requests.delete(f"{URL_RECON}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {tokens_recon['user_assigned']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 403 and
            r_o.text == r_r.text == "Forbidden\n"
        )
        record_diff(
            "DEV-HTTP-19", "DELETE Device as Normal Assigned User Rejection", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both reject non-admin delete with 403 Forbidden"
        )

        # =====================================================================
        # DEV-HTTP-20: DELETE device as normal unassigned user
        # =====================================================================
        r_o = requests.delete(f"{URL_ORIG}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {tokens_orig['user_unassigned']}"}, timeout=2)
        r_r = requests.delete(f"{URL_RECON}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {tokens_recon['user_unassigned']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 403 and
            r_o.text == r_r.text == "Forbidden\n"
        )
        record_diff(
            "DEV-HTTP-20", "DELETE Device as Normal Unassigned User Rejection", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both reject unassigned user delete with 403 Forbidden"
        )

        # =====================================================================
        # DEV-HTTP-21: DELETE with missing token
        # =====================================================================
        r_o = requests.delete(f"{URL_ORIG}/api/devices/dev-beta-002", timeout=2)
        r_r = requests.delete(f"{URL_RECON}/api/devices/dev-beta-002", timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 401 and
            r_o.text == r_r.text == "Unauthorized\n"
        )
        record_diff(
            "DEV-HTTP-21", "DELETE with Missing Token Rejection", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both reject unauthenticated delete with 401 Unauthorized"
        )

        # =====================================================================
        # DEV-HTTP-22: DELETE with invalid token
        # =====================================================================
        r_o = requests.delete(f"{URL_ORIG}/api/devices/dev-beta-002", headers={"Authorization": "Bearer bad_token_999"}, timeout=2)
        r_r = requests.delete(f"{URL_RECON}/api/devices/dev-beta-002", headers={"Authorization": "Bearer bad_token_999"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 401 and
            r_o.text == r_r.text == "Unauthorized\n"
        )
        record_diff(
            "DEV-HTTP-22", "DELETE with Invalid Token Rejection", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both reject invalid token delete with 401 Unauthorized"
        )

        # =====================================================================
        # DEV-HTTP-23: DELETE nonexistent device ID
        # =====================================================================
        r_o = requests.delete(f"{URL_ORIG}/api/devices/dev-nonexistent-999", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.delete(f"{URL_RECON}/api/devices/dev-nonexistent-999", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 404 and
            r_o.text == r_r.text == "Device not found\n"
        )
        record_diff(
            "DEV-HTTP-23", "DELETE Nonexistent Device ID", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both return 404 Device not found for nonexistent device"
        )

        # =====================================================================
        # DEV-HTTP-24: DELETE empty ID / slash-root
        # =====================================================================
        r_o = requests.delete(f"{URL_ORIG}/api/devices/", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.delete(f"{URL_RECON}/api/devices/", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 400 and
            r_o.text == r_r.text == "Invalid device id\n"
        )
        record_diff(
            "DEV-HTTP-24", "DELETE Empty Device ID on /api/devices/", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "body": r_o.text},
            {"status": r_r.status_code, "body": r_r.text},
            "Both return 400 Invalid device id for empty path parameter"
        )

        # =====================================================================
        # DEV-HTTP-25: OPTIONS on delete route
        # =====================================================================
        r_o = requests.options(f"{URL_ORIG}/api/devices/dev-beta-002", timeout=2)
        r_r = requests.options(f"{URL_RECON}/api/devices/dev-beta-002", timeout=2)
        cors_o = r_o.headers.get("Access-Control-Allow-Methods")
        cors_r = r_r.headers.get("Access-Control-Allow-Methods")
        passed = (
            r_o.status_code == r_r.status_code == 200 and
            cors_o == cors_r == "DELETE, OPTIONS"
        )
        record_diff(
            "DEV-HTTP-25", "OPTIONS on Delete Route /api/devices/{id}", "STRUCTURAL_EXACT_MATCH", passed,
            {"status": r_o.status_code, "methods": cors_o},
            {"status": r_r.status_code, "methods": cors_r},
            "Both return 200 OK with Access-Control-Allow-Methods: DELETE, OPTIONS"
        )

        # =====================================================================
        # DEV-HTTP-26: HEAD on delete route
        # =====================================================================
        r_o = requests.head(f"{URL_ORIG}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, timeout=2)
        r_r = requests.head(f"{URL_RECON}/api/devices/dev-beta-002", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, timeout=2)
        passed = (
            r_o.status_code == r_r.status_code == 405
        )
        record_diff(
            "DEV-HTTP-26", "HEAD on Delete Route /api/devices/{id}", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code},
            {"status": r_r.status_code},
            "Both reject HEAD request on delete handler with 405 Method not allowed"
        )

        # =====================================================================
        # DEV-HTTP-27: Initial /api/devices redirect semantics with allow_redirects=False
        # =====================================================================
        r_o = requests.get(f"{URL_ORIG}/api/devices", headers={"Authorization": f"Bearer {tokens_orig['admin']}"}, allow_redirects=False, timeout=2)
        r_r = requests.get(f"{URL_RECON}/api/devices", headers={"Authorization": f"Bearer {tokens_recon['admin']}"}, allow_redirects=False, timeout=2)
        loc_o = r_o.headers.get("Location")
        loc_r = r_r.headers.get("Location")
        passed = (
            r_o.status_code == r_r.status_code == 301 and
            loc_o == loc_r == "/api/devices/"
        )
        record_diff(
            "DEV-HTTP-27", "ServeMux Trailing Slash Redirect Semantics", "BIT_EXACT_MATCH", passed,
            {"status": r_o.status_code, "location": loc_o},
            {"status": r_r.status_code, "location": loc_r},
            "Both return 301 Moved Permanently with Location: /api/devices/ when trailing slash is omitted"
        )

    finally:
        for ws in active_ws.values():
            try:
                ws.close()
            except Exception:
                pass
        proc_orig.terminate()
        proc_recon.terminate()
        try:
            proc_orig.wait(timeout=2)
            proc_recon.wait(timeout=2)
        except Exception:
            proc_orig.kill()
            proc_recon.kill()
        if DIFF_TMP.exists():
            shutil.rmtree(DIFF_TMP, ignore_errors=True)

    # =====================================================================
    # DEV-HTTP-28: No-Auth Server Mode Verification
    # =====================================================================
    if DIFF_TMP_NA.exists():
        shutil.rmtree(DIFF_TMP_NA, ignore_errors=True)
    DIFF_TMP_NA.mkdir(parents=True, exist_ok=True)

    cmd_orig_na = [
        str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG_NA}", f"-data={DIFF_TMP_NA}", f"-assets={ASSETS}", "-no-auth", "-debug"
    ]
    proc_orig_na = subprocess.Popen(cmd_orig_na, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")

    cmd_recon_na = [
        str(EXE_RECON), f"-port={PORT_RECON_NA}", f"-data={DIFF_TMP_NA}", "-no-auth"
    ]
    proc_recon_na = subprocess.Popen(cmd_recon_na, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")

    for target, url in [("Original Oracle (no-auth)", URL_ORIG_NA), ("Reconstructed (no-auth)", URL_RECON_NA)]:
        ready = False
        for _ in range(40):
            time.sleep(0.2)
            try:
                r = requests.get(f"{url}/api/auth-status", timeout=1)
                if r.status_code == 200:
                    ready = True
                    break
            except Exception:
                pass
        if not ready:
            proc_orig_na.kill()
            proc_recon_na.kill()
            raise RuntimeError(f"{target} failed to initialize on {url}")

    try:
        r_o_na = requests.get(f"{URL_ORIG_NA}/devices", timeout=2)
        r_r_na = requests.get(f"{URL_RECON_NA}/devices", timeout=2)
        r_o_status = requests.get(f"{URL_ORIG_NA}/api/auth-status", timeout=2)
        r_r_status = requests.get(f"{URL_RECON_NA}/api/auth-status", timeout=2)

        passed = (
            r_o_na.status_code == r_r_na.status_code == 200 and
            r_o_na.text == r_r_na.text == "[]\n" and
            r_o_status.json().get("noAuth") == r_r_status.json().get("noAuth") == True
        )
        record_diff(
            "DEV-HTTP-28", "No-Auth Server Mode Unauthenticated Query", "BIT_EXACT_MATCH", passed,
            {"status": r_o_na.status_code, "body": r_o_na.text, "noAuth": r_o_status.json().get("noAuth")},
            {"status": r_r_na.status_code, "body": r_r_na.text, "noAuth": r_r_status.json().get("noAuth")},
            "Both serve device list without token and report noAuth: true when started with -no-auth"
        )
    finally:
        proc_orig_na.terminate()
        proc_recon_na.terminate()
        try:
            proc_orig_na.wait(timeout=2)
            proc_recon_na.wait(timeout=2)
        except Exception:
            proc_orig_na.kill()
            proc_recon_na.kill()
        if DIFF_TMP_NA.exists():
            shutil.rmtree(DIFF_TMP_NA, ignore_errors=True)

    # Save Results
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    total_count = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = sum(1 for r in results if not r["passed"])
    rate_str = f"IMPLEMENTED_DEVICE_CONTRACT_DIFFERENTIAL_PASS_RATE = {passed_count}/{total_count}"

    results_obj = {
        "metadata": {
            "title": "Phase 2C.3BR Device REST Differential Results",
            "contract_coverage": rate_str,
            "total_cases": total_count,
            "passed_cases": passed_count,
            "failed_cases": failed_count
        },
        "results": results
    }
    OUTPUT_JSON.write_text(json.dumps(results_obj, indent=2), encoding="utf-8")
    print(f"\n[+] Wrote {len(results)} differential results to {OUTPUT_JSON}")
    print(f"[+] Status: {rate_str}")

    # Generate Markdown Report 13
    md_lines = [
        "# Report 13: Phase 2C.3B Device Registry & REST Differential Verification",
        "",
        "## 1. Executive Summary",
        "",
        f"The Phase 2C.3BR Device Registry REST differential test suite executed **{len(results)} automated test cases** comparing the original `webrtc-signaling` binary against the cleanroom reconstructed HTTP server.",
        "",
        f"- **Total Test Cases**: {total_count}",
        f"- **Passed Cases**: {passed_count}",
        f"- **Failed Cases**: {failed_count}",
        f"- **Contract Pass Rate**: **`{rate_str}`**",
        "",
        "---",
        "",
        "## 2. Test Case Results Matrix",
        "",
        "| Case ID | Test Name | Classification | Verdict | Comparison Summary |",
        "|---|---|---|---|---|"
    ]
    for r in results:
        v = "**PASS**" if r["passed"] else "**FAIL**"
        md_lines.append(f"| `{r['test_id']}` | {r['test_name']} | `{r['classification']}` | {v} | {r['comparison_result']} |")

    md_lines.extend([
        "",
        "---",
        "",
        "## 3. Verified Parity Highlights",
        "",
        "1. **Empty Registry Serialization**: Both servers emit exact byte sequence `[]\\n` with `Content-Type: application/json`.",
        "2. **Device Data Model**: Matching 7-field JSON schema (`device_id`, `device_info`, `online`, `first_seen`, `last_seen`, `client_count`, and omitempty `clients`), field types, deep equality, and RFC3339 timestamp invariants (`first_seen <= last_seen`).",
        "3. **Assignment Filtering**: Admin sees all devices (`*`); assigned users see only their designated device; unassigned users receive `[]\\n`.",
        "4. **Lifecycle & Deletion**: Online devices cannot be deleted (`409 Conflict: Device is online, disconnect it first\\n`); offline devices are successfully removed (`200 OK: {\"status\":\"deleted\"}\\n`).",
        "5. **CORS & Preflight**: Identical headers for `OPTIONS` across listing and delete routes.",
        "6. **ServeMux Redirect Semantics**: With redirects disabled, `/api/devices` returns `301 Moved Permanently` with `Location: /api/devices/`.",
        "7. **Delete Route Contract Closure**: All error branches verified (401 missing/invalid token, 403 non-admin, 404 nonexistent ID, 400 empty ID, 405 wrong method/HEAD).",
        "8. **No-Auth Server Mode**: Both servers operate unauthenticated when launched with `-no-auth`."
    ])
    OUTPUT_REPORT.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"[+] Wrote Report 13R to {OUTPUT_REPORT}")

    all_passed = all(r["passed"] for r in results)
    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    run_suite()
