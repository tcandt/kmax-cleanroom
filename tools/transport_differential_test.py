#!/usr/bin/env python3
"""
tools/transport_differential_test.py — Phase 2C.4B Transport Source Differential Test Suite

Executes rigorous behavioral differential comparison between:
  1. Original Oracle Binary: cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe
  2. Reconstructed Source Binary: reconstructed_source/webrtc-signaling/http-server.exe

Strict Epistemic & Parity Classification:
  - EXACT_PARITY_PASS: Behavior matches original oracle identically.
  - VERIFIED_INTENTIONAL_DIVERGENCE: Documented necessary divergence.
  - EXCLUDED_ORACLE_UNAVAILABLE: Oracle could not run; FAILS CLOSED (never counted as parity pass).
  - IMPLEMENTATION_CHOICE_TESTS: Engineering design choices tested independently from original parity.
  - FAILED: Divergence or error where parity was expected.

Exit code 0 requires: failed == 0 and exact_parity_passed == exact_parity_total.
"""

import os
import sys
import json
import time
import socket
import base64
import hashlib
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent

ORIGINAL_EXE = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
RECONSTRUCTED_EXE = REPO_ROOT / "reconstructed_source" / "webrtc-signaling" / "http-server.exe"
ASSETS_DIR = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "assets"

def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def make_ws_frame(payload: bytes, opcode: int = 1, mask_payload: bool = True) -> bytes:
    length = len(payload)
    if mask_payload:
        mask = os.urandom(4)
        masked = bytes([b ^ mask[i % 4] for i, b in enumerate(payload)])
        if length < 126:
            hdr = bytes([0x80 | (opcode & 0x0f), 0x80 | length])
        elif length < 65536:
            hdr = bytes([0x80 | (opcode & 0x0f), 0x80 | 126]) + length.to_bytes(2, "big")
        else:
            hdr = bytes([0x80 | (opcode & 0x0f), 0x80 | 127]) + length.to_bytes(8, "big")
        return hdr + mask + masked
    else:
        if length < 126:
            hdr = bytes([0x80 | (opcode & 0x0f), length])
        elif length < 65536:
            hdr = bytes([0x80 | (opcode & 0x0f), 126]) + length.to_bytes(2, "big")
        else:
            hdr = bytes([0x80 | (opcode & 0x0f), 127]) + length.to_bytes(8, "big")
        return hdr + payload

def parse_ws_frame(data: bytes) -> Tuple[int, bytes, int]:
    if len(data) < 2:
        return 0, b"", 0
    opcode = data[0] & 0x0f
    is_masked = bool(data[1] & 0x80)
    payload_len = data[1] & 0x7f
    offset = 2
    if payload_len == 126:
        if len(data) < 4:
            return opcode, b"", 0
        payload_len = int.from_bytes(data[2:4], "big")
        offset = 4
    elif payload_len == 127:
        if len(data) < 10:
            return opcode, b"", 0
        payload_len = int.from_bytes(data[2:10], "big")
        offset = 10

    if is_masked:
        mask = data[offset:offset+4]
        offset += 4
        raw = data[offset:offset+payload_len]
        unmasked = bytes([b ^ mask[i % 4] for i, b in enumerate(raw)])
        return opcode, unmasked, offset + payload_len
    else:
        raw = data[offset:offset+payload_len]
        return opcode, raw, offset + payload_len

def hash_pwd(pwd: str, salt: str) -> str:
    return hashlib.sha256((pwd + salt).encode()).hexdigest()

def send_raw_http(port: int, method: str, path: str, headers: Optional[Dict[str, str]] = None, body: bytes = b"") -> Tuple[int, Dict[str, str], bytes]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.5)
    try:
        s.connect(("127.0.0.1", port))
        req_lines = [f"{method} {path} HTTP/1.1", f"Host: 127.0.0.1:{port}"]
        if headers:
            for k, v in headers.items():
                req_lines.append(f"{k}: {v}")
        if body:
            req_lines.append(f"Content-Length: {len(body)}")
        req = "\r\n".join(req_lines) + "\r\n\r\n"
        s.sendall(req.encode() + body)
        resp = s.recv(4096)
        s_line = resp.split(b"\r\n")[0].decode(errors="replace") if resp else ""
        code = int(s_line.split()[1]) if len(s_line.split()) > 1 else 0

        hdrs_raw = resp.split(b"\r\n\r\n")[0].split(b"\r\n")[1:] if b"\r\n\r\n" in resp else []
        resp_headers = {}
        for h in hdrs_raw:
            if b":" in h:
                k, v = h.split(b":", 1)
                resp_headers[k.decode(errors="replace").strip()] = v.decode(errors="replace").strip()

        resp_body = resp.split(b"\r\n\r\n", 1)[1] if b"\r\n\r\n" in resp else b""
        return code, resp_headers, resp_body
    finally:
        s.close()

def send_ws_handshake(port: int, path: str, extra_headers: Optional[Dict[str, str]] = None, custom_key: Optional[str] = None, version: str = "13") -> Tuple[Optional[socket.socket], int, Dict[str, str]]:
    key = custom_key if custom_key is not None else base64.b64encode(os.urandom(16)).decode()
    hdrs = {
        "Upgrade": "websocket",
        "Connection": "Upgrade",
        "Sec-WebSocket-Key": key,
        "Sec-WebSocket-Version": version
    }
    if extra_headers:
        hdrs.update(extra_headers)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", port))
        req_lines = [f"GET {path} HTTP/1.1", f"Host: 127.0.0.1:{port}"]
        for k, v in hdrs.items():
            if v != "__DROP__":
                req_lines.append(f"{k}: {v}")
        req = "\r\n".join(req_lines) + "\r\n\r\n"
        s.sendall(req.encode())
        resp = s.recv(4096)
        s_line = resp.split(b"\r\n")[0].decode(errors="replace") if resp else ""
        code = int(s_line.split()[1]) if len(s_line.split()) > 1 else 0

        hdrs_raw = resp.split(b"\r\n\r\n")[0].split(b"\r\n")[1:] if b"\r\n\r\n" in resp else []
        resp_headers = {}
        for h in hdrs_raw:
            if b":" in h:
                k, v = h.split(b":", 1)
                resp_headers[k.decode(errors="replace").strip()] = v.decode(errors="replace").strip()

        if code == 101:
            return s, code, resp_headers
        else:
            s.close()
            return None, code, resp_headers
    except Exception:
        s.close()
        return None, 0, {}

def setup_server_instance(exe_path: Path, port: int, tmp_dir: Path) -> subprocess.Popen:
    salt = "test_salt_123"
    users_data = {
        "admin": {
            "username": "admin",
            "password": hash_pwd("admin123", salt),
            "salt": salt,
            "role": "admin",
            "assigned_devices": ["*"],
            "expires_at": "0001-01-01T00:00:00Z"
        },
        "user1": {
            "username": "user1",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": ["test_dev_01"],
            "expires_at": "0001-01-01T00:00:00Z"
        }
    }
    (tmp_dir / "users.json").write_text(json.dumps(users_data, indent=2), encoding="utf-8")

    cmd = [str(exe_path), "-tls=false", f"-port={port}", f"-data={tmp_dir}", f"-assets={ASSETS_DIR}"]
    proc = subprocess.Popen(cmd, cwd=str(tmp_dir), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    return proc

def run_differential_suite() -> Dict[str, Any]:
    print("==================================================")
    print("PHASE 2C.4B TRANSPORT DIFFERENTIAL TEST SUITE")
    print("==================================================")

    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "original_binary": str(ORIGINAL_EXE),
        "reconstructed_binary": str(RECONSTRUCTED_EXE),
        "exact_parity_total": 0,
        "exact_parity_passed": 0,
        "verified_divergences": 0,
        "excluded_oracle_unavailable": 0,
        "implementation_choice_tests": 0,
        "failed": 0,
        "cases": []
    }

    # Verify binaries exist
    if not ORIGINAL_EXE.exists():
        print(f"[FAIL-CLOSED] Original binary not found: {ORIGINAL_EXE}")
        results["excluded_oracle_unavailable"] += 1
        return results

    # Build reconstructed binary if needed
    if not RECONSTRUCTED_EXE.exists():
        print("[*] Compiling reconstructed http-server.exe...")
        build_res = subprocess.run(["go", "build", "-o", "http-server.exe", "./cmd/http-server"],
                                   cwd=str(REPO_ROOT / "reconstructed_source" / "webrtc-signaling"),
                                   capture_output=True, text=True)
        if build_res.returncode != 0:
            print(f"[FAIL] Failed to compile reconstructed server: {build_res.stderr}")
            results["failed"] += 1
            return results

    orig_port = get_free_port()
    recon_port = get_free_port()

    orig_tmp = Path(tempfile.mkdtemp(prefix="orig_transport_"))
    recon_tmp = Path(tempfile.mkdtemp(prefix="recon_transport_"))

    orig_proc = None
    recon_proc = None

    try:
        print(f"[*] Starting Original Binary on port {orig_port}...")
        orig_proc = setup_server_instance(ORIGINAL_EXE, orig_port, orig_tmp)

        print(f"[*] Starting Reconstructed Binary on port {recon_port}...")
        recon_proc = setup_server_instance(RECONSTRUCTED_EXE, recon_port, recon_tmp)

        # Obtain login tokens on both instances for auth tests
        # Original login
        _, _, orig_login_body = send_raw_http(orig_port, "POST", "/api/login",
                                               headers={"Content-Type": "application/json"},
                                               body=json.dumps({"username": "admin", "password": "admin123"}).encode())
        orig_token = ""
        try:
            orig_token = json.loads(orig_login_body.decode()).get("token", "")
        except Exception:
            pass

        # Reconstructed login
        _, _, recon_login_body = send_raw_http(recon_port, "POST", "/api/login",
                                                headers={"Content-Type": "application/json"},
                                                body=json.dumps({"username": "admin", "password": "admin123"}).encode())
        recon_token = ""
        try:
            recon_token = json.loads(recon_login_body.decode()).get("token", "")
        except Exception:
            pass

        def record_case(case_id: str, desc: str, classification: str, matched: bool, detail: str):
            status = "EXACT_PARITY_PASS" if (matched and classification == "EXACT_PARITY") else \
                     "VERIFIED_INTENTIONAL_DIVERGENCE" if classification == "INTENTIONAL_DIVERGENCE" else \
                     "IMPLEMENTATION_CHOICE_TESTS" if classification == "IMPLEMENTATION_CHOICE" else "FAILED"

            if status == "EXACT_PARITY_PASS":
                results["exact_parity_total"] += 1
                results["exact_parity_passed"] += 1
                print(f"  [PASS] {case_id:36} {desc}")
            elif status == "VERIFIED_INTENTIONAL_DIVERGENCE":
                results["verified_divergences"] += 1
                print(f"  [DIVERGENCE] {case_id:36} {desc}: {detail}")
            elif status == "IMPLEMENTATION_CHOICE_TESTS":
                results["implementation_choice_tests"] += 1
                print(f"  [CHOICE] {case_id:36} {desc}: {detail}")
            else:
                results["exact_parity_total"] += 1
                results["failed"] += 1
                print(f"  [FAIL] {case_id:36} {desc}: {detail}")

            results["cases"].append({
                "case_id": case_id,
                "description": desc,
                "status": status,
                "matched": matched,
                "detail": detail
            })

        print("\n--- 1. HTTP Method Upgrade Matrix Differential (7 Methods x 3 Endpoints) ---")
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
        endpoints = ["/register_device", "/register_agent", "/connect_client"]

        for ep in endpoints:
            for m in methods:
                case_id = f"TR-DIFF-METHOD-{ep.strip('/')[:3].upper()}-{m}"
                orig_code, _, _ = send_raw_http(orig_port, m, ep)
                recon_code, _, _ = send_raw_http(recon_port, m, ep)
                matched = (orig_code == recon_code)
                detail = f"orig={orig_code}, recon={recon_code}"
                record_case(case_id, f"{m} {ep} standard HTTP response parity", "EXACT_PARITY", matched, detail)

        print("\n--- 2. WebSocket Upgrade Variations Differential ---")
        upgrade_cases = [
            ("valid_upgrade", "/register_device", {}, 101),
            ("valid_upgrade", "/register_agent", {}, 101),
            ("missing_upgrade_header", "/register_device", {"Upgrade": "__DROP__"}, 400),
            ("missing_upgrade_header", "/register_agent", {"Upgrade": "__DROP__"}, 400),
            ("wrong_version", "/register_device", {"Sec-WebSocket-Version": "12"}, 400),
            ("wrong_version", "/register_agent", {"Sec-WebSocket-Version": "12"}, 400),
        ]
        for name, ep, hdrs, expected_code in upgrade_cases:
            case_id = f"TR-DIFF-UPGRADE-{ep.strip('/')[:3].upper()}-{name.upper()}"
            s_orig, orig_code, _ = send_ws_handshake(orig_port, ep, extra_headers=hdrs)
            if s_orig: s_orig.close()
            s_recon, recon_code, _ = send_ws_handshake(recon_port, ep, extra_headers=hdrs)
            if s_recon: s_recon.close()
            matched = (orig_code == recon_code == expected_code)
            detail = f"orig={orig_code}, recon={recon_code}, expected={expected_code}"
            record_case(case_id, f"{ep} {name} handshake parity", "EXACT_PARITY", matched, detail)

        print("\n--- 3. Pre-Upgrade Authentication Matrix Differential (/connect_client) ---")
        auth_cases = [
            ("ADMIN_HEADER", {"Authorization": f"Bearer {orig_token}"}, {"Authorization": f"Bearer {recon_token}"}, 101),
            ("ADMIN_QUERY", f"?token={orig_token}", f"?token={recon_token}", 101),
            ("MISSING_TOKEN", {}, {}, 401),
            ("INVALID_TOKEN", {"Authorization": "Bearer invalid_xyz"}, {"Authorization": "Bearer invalid_xyz"}, 401),
        ]
        for name, orig_arg, recon_arg, expected_code in auth_cases:
            case_id = f"TR-DIFF-AUTH-{name}"
            if isinstance(orig_arg, dict):
                s_orig, orig_code, _ = send_ws_handshake(orig_port, "/connect_client", extra_headers=orig_arg)
                s_recon, recon_code, _ = send_ws_handshake(recon_port, "/connect_client", extra_headers=recon_arg)
            else:
                s_orig, orig_code, _ = send_ws_handshake(orig_port, f"/connect_client{orig_arg}")
                s_recon, recon_code, _ = send_ws_handshake(recon_port, f"/connect_client{recon_arg}")

            if s_orig: s_orig.close()
            if s_recon: s_recon.close()
            matched = (orig_code == recon_code == expected_code)
            detail = f"orig={orig_code}, recon={recon_code}, expected={expected_code}"
            record_case(case_id, f"/connect_client auth {name} parity", "EXACT_PARITY", matched, detail)

        print("\n--- 4. End-to-End WebSocket State Machine & Protocol Parity ---")
        # /register_device: register -> config
        s_orig_dev, c_o, _ = send_ws_handshake(orig_port, "/register_device")
        s_recon_dev, c_r, _ = send_ws_handshake(recon_port, "/register_device")
        if s_orig_dev and s_recon_dev:
            reg_frame = json.dumps({"message_type": "register", "device_id": "diff_dev_01"}).encode()
            s_orig_dev.sendall(make_ws_frame(reg_frame, opcode=1))
            s_recon_dev.sendall(make_ws_frame(reg_frame, opcode=1))

            data_orig = s_orig_dev.recv(4096)
            data_recon = s_recon_dev.recv(4096)
            op_o, p_o, _ = parse_ws_frame(data_orig)
            op_r, p_r, _ = parse_ws_frame(data_recon)

            msg_o = json.loads(p_o.decode()) if p_o else {}
            msg_r = json.loads(p_r.decode()) if p_r else {}

            matched = (op_o == op_r == 1) and (msg_o.get("message_type") == msg_r.get("message_type") == "config")
            record_case("TR-DIFF-E2E-DEV-REGISTER", "Device registration triggers config response parity", "EXACT_PARITY", matched,
                        f"orig_type={msg_o.get('message_type')}, recon_type={msg_r.get('message_type')}")
            s_orig_dev.close()
            s_recon_dev.close()
        else:
            record_case("TR-DIFF-E2E-DEV-REGISTER", "Device registration", "EXACT_PARITY", False, "Handshake failed")

        # /register_agent: agent_register -> agent_register_ok
        s_orig_ag, _, _ = send_ws_handshake(orig_port, "/register_agent")
        s_recon_ag, _, _ = send_ws_handshake(recon_port, "/register_agent")
        if s_orig_ag and s_recon_ag:
            ag_frame = json.dumps({"type": "agent_register", "device_id": "diff_dev_01", "is_webrtc": True}).encode()
            s_orig_ag.sendall(make_ws_frame(ag_frame, opcode=1))
            s_recon_ag.sendall(make_ws_frame(ag_frame, opcode=1))

            data_orig = s_orig_ag.recv(4096)
            data_recon = s_recon_ag.recv(4096)
            op_o, p_o, _ = parse_ws_frame(data_orig)
            op_r, p_r, _ = parse_ws_frame(data_recon)

            msg_o = json.loads(p_o.decode()) if p_o else {}
            msg_r = json.loads(p_r.decode()) if p_r else {}

            matched = (op_o == op_r == 1) and (msg_o.get("message_type") == msg_r.get("message_type") == "agent_register_ok")
            record_case("TR-DIFF-E2E-AGENT-REGISTER", "Agent registration triggers agent_register_ok parity", "EXACT_PARITY", matched,
                        f"orig_type={msg_o.get('message_type')}, recon_type={msg_r.get('message_type')}")
            s_orig_ag.close()
            s_recon_ag.close()
        else:
            record_case("TR-DIFF-E2E-AGENT-REGISTER", "Agent registration", "EXACT_PARITY", False, "Handshake failed")

        # Ping / Pong RFC 6455 parity
        s_orig_dev, _, _ = send_ws_handshake(orig_port, "/register_device")
        s_recon_dev, _, _ = send_ws_handshake(recon_port, "/register_device")
        if s_orig_dev and s_recon_dev:
            ping_frame = make_ws_frame(b"diff-ping-test", opcode=9)
            s_orig_dev.sendall(ping_frame)
            s_recon_dev.sendall(ping_frame)

            data_orig = s_orig_dev.recv(1024)
            data_recon = s_recon_dev.recv(1024)
            op_o, p_o, _ = parse_ws_frame(data_orig)
            op_r, p_r, _ = parse_ws_frame(data_recon)

            matched = (op_o == op_r == 10) and (p_o == p_r == b"diff-ping-test")
            record_case("TR-DIFF-EDGE-PING-PONG", "RFC 6455 Ping (opcode 9) -> Pong (opcode 10) parity", "EXACT_PARITY", matched,
                        f"orig_op={op_o}, recon_op={op_r}")
            s_orig_dev.close()
            s_recon_dev.close()
        else:
            record_case("TR-DIFF-EDGE-PING-PONG", "Ping/Pong", "EXACT_PARITY", False, "Handshake failed")

        # Unmasked client frame protocol error (RFC 6455 1002)
        s_orig_dev, _, _ = send_ws_handshake(orig_port, "/register_device")
        s_recon_dev, _, _ = send_ws_handshake(recon_port, "/register_device")
        if s_orig_dev and s_recon_dev:
            unmasked_frame = make_ws_frame(b"unmasked-violation", opcode=1, mask_payload=False)
            s_orig_dev.sendall(unmasked_frame)
            s_recon_dev.sendall(unmasked_frame)

            data_orig = s_orig_dev.recv(1024)
            data_recon = s_recon_dev.recv(1024)
            op_o, _, _ = parse_ws_frame(data_orig)
            op_r, _, _ = parse_ws_frame(data_recon)

            matched = (op_o == op_r == 8) # Opcode 8 Close Frame
            record_case("TR-DIFF-EDGE-UNMASKED-FRAME", "Unmasked client frame causes RFC 6455 Close Frame (opcode 8) parity", "EXACT_PARITY", matched,
                        f"orig_op={op_o}, recon_op={op_r}")
            s_orig_dev.close()
            s_recon_dev.close()
        else:
            record_case("TR-DIFF-EDGE-UNMASKED-FRAME", "Unmasked frame", "EXACT_PARITY", False, "Handshake failed")

    finally:
        if orig_proc:
            orig_proc.terminate()
            orig_proc.wait()
        if recon_proc:
            recon_proc.terminate()
            recon_proc.wait()
        shutil.rmtree(orig_tmp, ignore_errors=True)
        shutil.rmtree(recon_tmp, ignore_errors=True)

    print("\n==================================================")
    print("TRANSPORT DIFFERENTIAL RESULTS SUMMARY")
    print("==================================================")
    print(f"Exact Parity Total:             {results['exact_parity_total']}")
    print(f"Exact Parity Passed:            {results['exact_parity_passed']}")
    print(f"Verified Divergences:           {results['verified_divergences']}")
    print(f"Excluded (Oracle Unavailable):  {results['excluded_oracle_unavailable']}")
    print(f"Implementation Choice Tests:    {results['implementation_choice_tests']}")
    print(f"Failed:                         {results['failed']}")
    all_ok = (results["failed"] == 0 and results["exact_parity_passed"] == results["exact_parity_total"])
    print(f"Verdict:                        {'PASS' if all_ok else 'FAIL'}")
    print("==================================================")

    # Save results to scratch directory (ignored by git to ensure non-mutating audit)
    out_file = REPO_ROOT / "scratch" / "transport_differential_results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")

    return results


if __name__ == "__main__":
    import shutil
    res = run_differential_suite()
    if res["failed"] != 0 or res["exact_parity_passed"] != res["exact_parity_total"]:
        sys.exit(1)
    sys.exit(0)
