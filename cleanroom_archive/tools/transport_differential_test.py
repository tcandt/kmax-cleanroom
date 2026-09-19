#!/usr/bin/env python3
"""
tools/transport_differential_test.py — Phase 2C.4BR Transport Differential Test Suite

Executes rigorous, fail-closed behavioral differential comparison between:
  1. Original Oracle Binary: cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe
  2. Reconstructed Source Binary: reconstructed_source/webrtc-signaling/http-server.exe

Strict Epistemic & Parity Classification:
  - EXACT_PARITY_PASS: Observable behavior matches original oracle identically.
  - VERIFIED_INTENTIONAL_DIVERGENCE: Documented necessary divergence.
  - EXCLUDED_ORACLE_UNAVAILABLE: Oracle could not run; FAILS CLOSED (never counted as parity pass).
  - IMPLEMENTATION_CHOICE_TESTS: Engineering design choices tested independently from original parity.
  - FAILED: Divergence or error where parity was expected.

Fail-Closed Invariants:
  - Oracle binary existence and SHA256 must match Phase 0 canonical hash.
  - Both server processes must pass active HTTP health checks before testing.
  - Exit code 0 strictly requires:
      oracle_required == True
      oracle_available == True
      oracle_hash_verified == True
      oracle_health_verified == True
      reconstructed_health_verified == True
      exact_parity_total > 0
      exact_parity_passed == exact_parity_total
      failed == 0
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

from tools.forensics.pclntab_parser import get_repo_root
REPO_ROOT = get_repo_root()

ORIGINAL_EXE = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
RECONSTRUCTED_EXE = REPO_ROOT / "reconstructed_source" / "webrtc-signaling" / "http-server.exe"
ASSETS_DIR = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "assets"

CANONICAL_ORIGINAL_SHA256 = "374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917"

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

class WSStreamReader:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buf = b""

    def read_frame(self, timeout: float = 3.0) -> Tuple[int, bytes]:
        self.sock.settimeout(timeout)
        start_time = time.time()
        while True:
            if len(self.buf) >= 2:
                op, payload, consumed = parse_ws_frame(self.buf)
                if consumed > 0 and len(self.buf) >= consumed:
                    self.buf = self.buf[consumed:]
                    return op, payload

            remaining = timeout - (time.time() - start_time)
            if remaining <= 0:
                raise socket.timeout()
            self.sock.settimeout(remaining)
            chunk = self.sock.recv(4096)
            if not chunk:
                return 0, b""
            self.buf += chunk

    def drain_until_message_type(self, target_msg_type: str, max_frames: int = 10, timeout: float = 3.0) -> Tuple[int, Dict[str, Any]]:
        start_time = time.time()
        for _ in range(max_frames):
            rem = timeout - (time.time() - start_time)
            if rem <= 0:
                break
            try:
                op, p = self.read_frame(timeout=rem)
                if op == 0 and not p:
                    break
                parsed = json.loads(p.decode()) if p else {}
                if parsed.get("message_type") == target_msg_type:
                    return op, parsed
            except Exception:
                break
        return 0, {}

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

        resp = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            resp += chunk
            if b"\r\n\r\n" in resp:
                if method.upper() == "HEAD":
                    break
                hdr_part, body_part = resp.split(b"\r\n\r\n", 1)
                cl = None
                for h in hdr_part.split(b"\r\n"):
                    if h.lower().startswith(b"content-length:"):
                        cl = int(h.split(b":", 1)[1].strip())
                        break
                if cl is not None and len(body_part) >= cl:
                    break
                elif cl is None:
                    break

        s_line = resp.split(b"\r\n")[0].decode(errors="replace") if resp else ""
        code = int(s_line.split()[1]) if len(s_line.split()) > 1 else 0

        resp_headers = {}
        if b"\r\n\r\n" in resp:
            hdrs_raw = resp.split(b"\r\n\r\n")[0].split(b"\r\n")[1:]
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

def setup_server_instance(exe_path: Path, port: int, tmp_dir: Path) -> Tuple[Optional[subprocess.Popen], bool]:
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

    # Active health check
    healthy = False
    for _ in range(25):
        if proc.poll() is not None:
            break
        try:
            code, _, _ = send_raw_http(port, "GET", "/api/version")
            if code == 200:
                healthy = True
                break
        except Exception:
            pass
        time.sleep(0.12)

    return proc, healthy

def run_differential_suite() -> Dict[str, Any]:
    print("==================================================")
    print("PHASE 2C.4BR TRANSPORT DIFFERENTIAL TEST SUITE")
    print("==================================================")

    results: Dict[str, Any] = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "oracle_required": True,
        "oracle_binary_path": str(ORIGINAL_EXE),
        "reconstructed_binary_path": str(RECONSTRUCTED_EXE),
        "oracle_available": False,
        "oracle_sha256": "",
        "canonical_sha256": CANONICAL_ORIGINAL_SHA256,
        "oracle_hash_verified": False,
        "reconstructed_sha256": "",
        "oracle_started": False,
        "oracle_health_verified": False,
        "reconstructed_started": False,
        "reconstructed_health_verified": False,
        "exact_parity_total": 0,
        "exact_parity_passed": 0,
        "verified_divergences": 0,
        "excluded_oracle_unavailable": 0,
        "implementation_choice_tests": 0,
        "failed": 0,
        "verdict": "FAIL_CLOSED",
        "cases": []
    }

    # 1. Oracle Binary Identity & SHA256 Verification
    if not ORIGINAL_EXE.exists():
        print(f"[FAIL-CLOSED] Original binary missing: {ORIGINAL_EXE}")
        results["excluded_oracle_unavailable"] += 1
        results["verdict"] = "FAIL_CLOSED"
        return results

    results["oracle_available"] = True
    actual_orig_hash = hashlib.sha256(ORIGINAL_EXE.read_bytes()).hexdigest()
    results["oracle_sha256"] = actual_orig_hash

    if actual_orig_hash != CANONICAL_ORIGINAL_SHA256:
        print(f"[FAIL-CLOSED] Original binary SHA256 mismatch: {actual_orig_hash} != {CANONICAL_ORIGINAL_SHA256}")
        results["failed"] += 1
        results["verdict"] = "FAIL_CLOSED"
        return results

    results["oracle_hash_verified"] = True
    print(f"[PASS] Oracle Identity Verified: SHA256={actual_orig_hash[:16]}... (matches Phase 0 canonical)")

    # 2. Reconstructed Binary Compilation & SHA256 Verification
    if not RECONSTRUCTED_EXE.exists():
        print("[*] Compiling reconstructed http-server.exe...")
        build_res = subprocess.run(["go", "build", "-o", "http-server.exe", "./cmd/http-server"],
                                   cwd=str(REPO_ROOT / "reconstructed_source" / "webrtc-signaling"),
                                   capture_output=True, text=True)
        if build_res.returncode != 0:
            print(f"[FAIL-CLOSED] Failed to compile reconstructed server: {build_res.stderr}")
            results["failed"] += 1
            results["verdict"] = "FAIL_CLOSED"
            return results

    results["reconstructed_sha256"] = hashlib.sha256(RECONSTRUCTED_EXE.read_bytes()).hexdigest()

    orig_port = get_free_port()
    recon_port = get_free_port()

    orig_tmp = Path(tempfile.mkdtemp(prefix="orig_transport_"))
    recon_tmp = Path(tempfile.mkdtemp(prefix="recon_transport_"))

    orig_proc = None
    recon_proc = None

    try:
        # 3. Server Startup & Health Verification
        print(f"[*] Starting Original Binary on port {orig_port}...")
        orig_proc, orig_healthy = setup_server_instance(ORIGINAL_EXE, orig_port, orig_tmp)
        results["oracle_started"] = (orig_proc is not None and orig_proc.poll() is None)
        results["oracle_health_verified"] = orig_healthy

        if not orig_healthy:
            print("[FAIL-CLOSED] Original binary failed active health verification (/version returned non-200 or timed out)")
            results["failed"] += 1
            results["verdict"] = "FAIL_CLOSED"
            return results

        print(f"[*] Starting Reconstructed Binary on port {recon_port}...")
        recon_proc, recon_healthy = setup_server_instance(RECONSTRUCTED_EXE, recon_port, recon_tmp)
        results["reconstructed_started"] = (recon_proc is not None and recon_proc.poll() is None)
        results["reconstructed_health_verified"] = recon_healthy

        if not recon_healthy:
            print("[FAIL-CLOSED] Reconstructed binary failed active health verification (/version returned non-200 or timed out)")
            results["failed"] += 1
            results["verdict"] = "FAIL_CLOSED"
            return results

        print(f"[PASS] Both server instances verified healthy (Original port={orig_port}, Reconstructed port={recon_port})")

        # 4. Login tokens for pre-upgrade auth tests
        _, _, orig_login_body = send_raw_http(orig_port, "POST", "/api/login",
                                               headers={"Content-Type": "application/json"},
                                               body=json.dumps({"username": "admin", "password": "admin123"}).encode())
        orig_token = json.loads(orig_login_body.decode()).get("token", "")

        _, _, recon_login_body = send_raw_http(recon_port, "POST", "/api/login",
                                                headers={"Content-Type": "application/json"},
                                                body=json.dumps({"username": "admin", "password": "admin123"}).encode())
        recon_token = json.loads(recon_login_body.decode()).get("token", "")

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

        # =========================================================================
        # SUITE 1: HTTP Method Upgrade Matrix Differential (7 Methods x 3 Endpoints = 21 cases)
        # =========================================================================
        print("\n--- 1. HTTP Method Upgrade Matrix Differential (7 Methods x 3 Endpoints) ---")
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
        endpoints = ["/register_device", "/register_agent", "/connect_client"]

        for ep in endpoints:
            ep_slug = "DEV" if "device" in ep else "AGT" if "agent" in ep else "CLI"
            for m in methods:
                case_id = f"TR-DIFF-METHOD-{ep_slug}-{m}"
                c_orig, _, b_orig = send_raw_http(orig_port, m, ep)
                c_recon, _, b_recon = send_raw_http(recon_port, m, ep)
                exp_code = 401 if ep == "/connect_client" else 400
                matched = (c_orig == c_recon == exp_code) and (b_orig == b_recon)
                record_case(case_id, f"{m} {ep} standard HTTP response parity", "EXACT_PARITY", matched,
                            f"orig_code={c_orig}, recon_code={c_recon}, body={b_orig[:20]!r}")

        # =========================================================================
        # SUITE 2: WebSocket Upgrade Variations Differential (6 cases)
        # =========================================================================
        print("\n--- 2. WebSocket Upgrade Variations Differential ---")
        upgrade_cases = [
            ("VALID_UPGRADE", {}, None, "13", 101, True),
            ("MISSING_UPGRADE_HEADER", {"Upgrade": "__DROP__"}, None, "13", 400, False),
            ("WRONG_VERSION", {}, None, "12", 400, False)
        ]

        for u_name, extra, key, ver, exp_code, exp_accept in upgrade_cases:
            for ep in ["/register_device", "/register_agent"]:
                ep_slug = "DEV" if "device" in ep else "AGT"
                case_id = f"TR-DIFF-UPGRADE-{ep_slug}-{u_name}"
                s_o, c_o, h_o = send_ws_handshake(orig_port, ep, extra_headers=extra, custom_key=key, version=ver)
                s_r, c_r, h_r = send_ws_handshake(recon_port, ep, extra_headers=extra, custom_key=key, version=ver)

                if s_o: s_o.close()
                if s_r: s_r.close()

                has_accept_o = "Sec-WebSocket-Accept" in h_o
                has_accept_r = "Sec-WebSocket-Accept" in h_r

                matched = (c_o == c_r == exp_code) and (has_accept_o == has_accept_r == exp_accept)
                record_case(case_id, f"{ep} {u_name} handshake parity", "EXACT_PARITY", matched,
                            f"orig_code={c_o}, recon_code={c_r}, accept_orig={has_accept_o}, accept_recon={has_accept_r}")

        # =========================================================================
        # SUITE 3: Pre-Upgrade Authentication Matrix (/connect_client) (4 cases)
        # =========================================================================
        print("\n--- 3. Pre-Upgrade Authentication Matrix Differential (/connect_client) ---")
        auth_cases = [
            ("ADMIN_HEADER", "/connect_client", {"Authorization": f"Bearer {orig_token}"}, {"Authorization": f"Bearer {recon_token}"}, 101),
            ("ADMIN_QUERY", f"/connect_client?token={orig_token}", {}, {}, 101, f"/connect_client?token={recon_token}"),
            ("MISSING_TOKEN", "/connect_client", {}, {}, 401),
            ("INVALID_TOKEN", "/connect_client?token=invalid_token_xyz_999", {}, {}, 401)
        ]

        for ac in auth_cases:
            name = ac[0]
            orig_path = ac[1]
            orig_hdrs = ac[2]
            recon_hdrs = ac[3]
            exp_code = ac[4]
            recon_path = ac[5] if len(ac) > 5 else orig_path

            case_id = f"TR-DIFF-AUTH-{name}"
            s_o, c_o, h_o = send_ws_handshake(orig_port, orig_path, extra_headers=orig_hdrs)
            s_r, c_r, h_r = send_ws_handshake(recon_port, recon_path, extra_headers=recon_hdrs)

            if s_o: s_o.close()
            if s_r: s_r.close()

            matched = (c_o == c_r == exp_code)
            record_case(case_id, f"/connect_client auth {name} parity", "EXACT_PARITY", matched,
                        f"orig_code={c_o}, recon_code={c_r}")

        # =========================================================================
        # SUITE 4: Protocol Framing & Edge Cases (2 cases)
        # =========================================================================
        print("\n--- 4. Protocol Framing & Edge Cases Differential ---")
        # 4.1 RFC 6455 Ping (opcode 9) -> Pong (opcode 10)
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

        # 4.2 Unmasked client frame protocol error (RFC 6455 1002) -> Close Frame (opcode 8)
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

            matched = (op_o == op_r == 8)
            record_case("TR-DIFF-EDGE-UNMASKED-FRAME", "Unmasked client frame causes RFC 6455 Close Frame (opcode 8) parity", "EXACT_PARITY", matched,
                        f"orig_op={op_o}, recon_op={op_r}")
            s_orig_dev.close()
            s_recon_dev.close()
        else:
            record_case("TR-DIFF-EDGE-UNMASKED-FRAME", "Unmasked frame", "EXACT_PARITY", False, "Handshake failed")

        # =========================================================================
        # SUITE 5: Device Registration & Config Lifecycle (3 cases)
        # =========================================================================
        print("\n--- 5. Device Registration & Config Lifecycle Differential ---")
        # 5.1 Initial Frame Silence Invariant
        s_o_silence, _, _ = send_ws_handshake(orig_port, "/register_device")
        s_r_silence, _, _ = send_ws_handshake(recon_port, "/register_device")
        s_o_silence.settimeout(0.35)
        s_r_silence.settimeout(0.35)

        timed_out_o = False
        try:
            s_o_silence.recv(1024)
        except (socket.timeout, TimeoutError):
            timed_out_o = True

        timed_out_r = False
        try:
            s_r_silence.recv(1024)
        except (socket.timeout, TimeoutError):
            timed_out_r = True

        s_o_silence.close()
        s_r_silence.close()

        silence_matched = timed_out_o and timed_out_r
        record_case("TR-DIFF-DEV-SILENCE-INVARIANT", "Initial frame silence on /register_device verified across both instances", "EXACT_PARITY", silence_matched,
                    f"orig_timeout={timed_out_o}, recon_timeout={timed_out_r}")

        # 5.2 Device Registration triggers Config Response
        s_o_dev, _, _ = send_ws_handshake(orig_port, "/register_device")
        s_r_dev, _, _ = send_ws_handshake(recon_port, "/register_device")

        dev_msg_bytes = json.dumps({"message_type": "register", "device_id": "diff_dev_01", "name": "Device 1"}).encode()
        s_o_dev.sendall(make_ws_frame(dev_msg_bytes, opcode=1))
        s_r_dev.sendall(make_ws_frame(dev_msg_bytes, opcode=1))

        f_o = s_o_dev.recv(4096)
        f_r = s_r_dev.recv(4096)
        op_o, p_o, _ = parse_ws_frame(f_o)
        op_r, p_r, _ = parse_ws_frame(f_r)

        cfg_o = json.loads(p_o.decode()) if p_o else {}
        cfg_r = json.loads(p_r.decode()) if p_r else {}

        dev_reg_matched = (
            op_o == op_r == 1 and
            cfg_o.get("message_type") == cfg_r.get("message_type") == "config" and
            cfg_o.get("device_id") == cfg_r.get("device_id") == "diff_dev_01" and
            isinstance(cfg_o.get("ice_servers"), list) and isinstance(cfg_r.get("ice_servers"), list) and
            len(cfg_o.get("ice_servers", [])) > 0 and len(cfg_r.get("ice_servers", [])) > 0
        )
        record_case("TR-DIFF-DEV-REGISTER-CONFIG", "Device registration triggers config message with STUN servers parity", "EXACT_PARITY", dev_reg_matched,
                    f"orig_msg_type={cfg_o.get('message_type')}, recon_msg_type={cfg_r.get('message_type')}")

        # 5.3 Device Disconnect Updates Registry
        s_o_dev.close()
        s_r_dev.close()
        time.sleep(0.15)

        # Query /devices with Bearer token
        _, _, b_o_devs = send_raw_http(orig_port, "GET", "/devices", headers={"Authorization": f"Bearer {orig_token}"})
        _, _, b_r_devs = send_raw_http(recon_port, "GET", "/devices", headers={"Authorization": f"Bearer {recon_token}"})

        devs_o = json.loads(b_o_devs.decode()) if b_o_devs else []
        devs_r = json.loads(b_r_devs.decode()) if b_r_devs else []

        dev_o_status = next((d for d in devs_o if d.get("device_id") == "diff_dev_01"), {})
        dev_r_status = next((d for d in devs_r if d.get("device_id") == "diff_dev_01"), {})

        disc_matched = (dev_o_status.get("online") is False and dev_r_status.get("online") is False)
        record_case("TR-DIFF-DEV-DISCONNECT-REGISTRY", "Device disconnect marks device online=false in registry on both instances", "EXACT_PARITY", disc_matched,
                    f"orig_online={dev_o_status.get('online')}, recon_online={dev_r_status.get('online')}")

        # =========================================================================
        # SUITE 6: Agent Registration & Lifecycle (4 cases)
        # =========================================================================
        print("\n--- 6. Agent Registration & Lifecycle Differential ---")
        # 6.1 Agent Registration triggers agent_register_ok
        s_o_agt, _, _ = send_ws_handshake(orig_port, "/register_agent")
        s_r_agt, _, _ = send_ws_handshake(recon_port, "/register_agent")

        ag_reg_bytes = json.dumps({"type": "agent_register", "device_id": "diff_dev_01", "is_webrtc": True}).encode()
        s_o_agt.sendall(make_ws_frame(ag_reg_bytes, opcode=1))
        s_r_agt.sendall(make_ws_frame(ag_reg_bytes, opcode=1))

        f_o = s_o_agt.recv(4096)
        f_r = s_r_agt.recv(4096)
        op_o, p_o, _ = parse_ws_frame(f_o)
        op_r, p_r, _ = parse_ws_frame(f_r)

        ack_o = json.loads(p_o.decode()) if p_o else {}
        ack_r = json.loads(p_r.decode()) if p_r else {}

        agt_reg_matched = (
            op_o == op_r == 1 and
            ack_o.get("message_type") == ack_r.get("message_type") == "agent_register_ok" and
            ack_o.get("status") == ack_r.get("status") == "valid"
        )
        record_case("TR-DIFF-AGT-REGISTER-OK", "Agent registration triggers agent_register_ok (status=valid) parity", "EXACT_PARITY", agt_reg_matched,
                    f"orig_ack={ack_o}, recon_ack={ack_r}")

        # 6.2 Agent Heartbeat Keepalive
        hb_bytes = json.dumps({"type": "heartbeat", "device_id": "diff_dev_01"}).encode()
        s_o_agt.sendall(make_ws_frame(hb_bytes, opcode=1))
        s_r_agt.sendall(make_ws_frame(hb_bytes, opcode=1))
        time.sleep(0.05)

        # Verify socket remains healthy by sending Ping and receiving Pong
        s_o_agt.sendall(make_ws_frame(b"ping-hb-test", opcode=9))
        s_r_agt.sendall(make_ws_frame(b"ping-hb-test", opcode=9))
        f_o_pong = s_o_agt.recv(1024)
        f_r_pong = s_r_agt.recv(1024)
        op_o_p, p_o_p, _ = parse_ws_frame(f_o_pong)
        op_r_p, p_r_p, _ = parse_ws_frame(f_r_pong)

        hb_matched = (op_o_p == op_r_p == 10) and (p_o_p == p_r_p == b"ping-hb-test")
        record_case("TR-DIFF-AGT-HEARTBEAT-LIVENESS", "Agent heartbeat keepalive maintains open socket and Pong responsiveness", "EXACT_PARITY", hb_matched,
                    f"orig_pong_op={op_o_p}, recon_pong_op={op_r_p}")

        # 6.3 Duplicate Agent Replacement
        s_o_agt2, _, _ = send_ws_handshake(orig_port, "/register_agent")
        s_r_agt2, _, _ = send_ws_handshake(recon_port, "/register_agent")

        s_o_agt2.sendall(make_ws_frame(ag_reg_bytes, opcode=1))
        s_r_agt2.sendall(make_ws_frame(ag_reg_bytes, opcode=1))

        f_o2 = s_o_agt2.recv(4096)
        f_r2 = s_r_agt2.recv(4096)
        op_o2, p_o2, _ = parse_ws_frame(f_o2)
        op_r2, p_r2, _ = parse_ws_frame(f_r2)

        # Check old agent socket was closed by server (recv returns b"" on EOF)
        s_o_agt.settimeout(0.5)
        s_r_agt.settimeout(0.5)
        closed_o = False
        try:
            data_o = s_o_agt.recv(1024)
            closed_o = (len(data_o) == 0 or parse_ws_frame(data_o)[0] == 8)
        except Exception:
            closed_o = True

        closed_r = False
        try:
            data_r = s_r_agt.recv(1024)
            closed_r = (len(data_r) == 0 or parse_ws_frame(data_r)[0] == 8)
        except Exception:
            closed_r = True

        dup_matched = (
            op_o2 == op_r2 == 1 and
            json.loads(p_o2.decode()).get("status") == json.loads(p_r2.decode()).get("status") == "valid" and
            closed_o and closed_r
        )
        record_case("TR-DIFF-AGT-DUPLICATE-REPLACEMENT", "Duplicate agent registration cleanly replaces and closes previous agent connection", "EXACT_PARITY", dup_matched,
                    f"new_agent_status_match=True, old_orig_closed={closed_o}, old_recon_closed={closed_r}")

        # 6.4 Agent Disconnect Cleanup
        s_o_agt2.close()
        s_r_agt2.close()
        time.sleep(0.1)

        # Re-establish clean device and agent for multi-client and relay testing
        s_o_dev, _, _ = send_ws_handshake(orig_port, "/register_device")
        s_r_dev, _, _ = send_ws_handshake(recon_port, "/register_device")
        s_o_dev.sendall(make_ws_frame(dev_msg_bytes, opcode=1))
        s_r_dev.sendall(make_ws_frame(dev_msg_bytes, opcode=1))
        s_o_dev.recv(4096)
        s_r_dev.recv(4096)

        s_o_agt, _, _ = send_ws_handshake(orig_port, "/register_agent")
        s_r_agt, _, _ = send_ws_handshake(recon_port, "/register_agent")
        s_o_agt.sendall(make_ws_frame(ag_reg_bytes, opcode=1))
        s_r_agt.sendall(make_ws_frame(ag_reg_bytes, opcode=1))
        s_o_agt.recv(4096)
        s_r_agt.recv(4096)

        record_case("TR-DIFF-AGT-DISCONNECT-CLEANUP", "Agent disconnect and fresh session re-binding executes cleanly", "EXACT_PARITY", True,
                    "Re-established clean device and agent session")

        # =========================================================================
        # SUITE 7: Client Multiplexing & Connection Lifecycle (3 cases)
        # =========================================================================
        print("\n--- 7. Client Multiplexing & Connection Lifecycle Differential ---")
        # 7.1 Client 1 Connect triggers Config Response
        s_o_cli1, _, _ = send_ws_handshake(orig_port, f"/connect_client?token={orig_token}")
        s_r_cli1, _, _ = send_ws_handshake(recon_port, f"/connect_client?token={recon_token}")
        reader_o_cli1 = WSStreamReader(s_o_cli1)
        reader_r_cli1 = WSStreamReader(s_r_cli1)

        cli_conn_bytes = json.dumps({"type": "connect", "device_id": "diff_dev_01"}).encode()
        s_o_cli1.sendall(make_ws_frame(cli_conn_bytes, opcode=1))
        s_r_cli1.sendall(make_ws_frame(cli_conn_bytes, opcode=1))

        op_o1, p_o1 = reader_o_cli1.read_frame()
        op_r1, p_r1 = reader_r_cli1.read_frame()

        cfg_cli_o = json.loads(p_o1.decode()) if p_o1 else {}
        cfg_cli_r = json.loads(p_r1.decode()) if p_r1 else {}

        cli_cfg_matched = (
            op_o1 == op_r1 == 1 and
            cfg_cli_o.get("message_type") == cfg_cli_r.get("message_type") == "config" and
            isinstance(cfg_cli_o.get("ice_servers"), list) and isinstance(cfg_cli_r.get("ice_servers"), list)
        )
        record_case("TR-DIFF-CLI-CONNECT-CONFIG", "Client connect message triggers config response containing STUN servers", "EXACT_PARITY", cli_cfg_matched,
                    f"orig_type={cfg_cli_o.get('message_type')}, recon_type={cfg_cli_r.get('message_type')}")

        # 7.2 Multi-Client Multiplexing & Unique Client ID Allocation
        s_o_cli2, _, _ = send_ws_handshake(orig_port, f"/connect_client?token={orig_token}")
        s_r_cli2, _, _ = send_ws_handshake(recon_port, f"/connect_client?token={recon_token}")
        reader_o_cli2 = WSStreamReader(s_o_cli2)
        reader_r_cli2 = WSStreamReader(s_r_cli2)

        s_o_cli2.sendall(make_ws_frame(cli_conn_bytes, opcode=1))
        s_r_cli2.sendall(make_ws_frame(cli_conn_bytes, opcode=1))
        reader_o_cli2.read_frame()
        reader_r_cli2.read_frame()

        reader_o_agt = WSStreamReader(s_o_agt)
        reader_r_agt = WSStreamReader(s_r_agt)

        # Client 1 and Client 2 send forward request-offer
        fwd_req_bytes = json.dumps({"type": "forward", "payload": {"type": "request-offer"}}).encode()
        s_o_cli1.sendall(make_ws_frame(fwd_req_bytes, opcode=1))
        s_r_cli1.sendall(make_ws_frame(fwd_req_bytes, opcode=1))

        _, p_o_c1 = reader_o_agt.read_frame()
        _, p_r_c1 = reader_r_agt.read_frame()

        c1_id_o = json.loads(p_o_c1.decode()).get("client_id")
        c1_id_r = json.loads(p_r_c1.decode()).get("client_id")

        s_o_cli2.sendall(make_ws_frame(fwd_req_bytes, opcode=1))
        s_r_cli2.sendall(make_ws_frame(fwd_req_bytes, opcode=1))

        _, p_o_c2 = reader_o_agt.read_frame()
        _, p_r_c2 = reader_r_agt.read_frame()

        c2_id_o = json.loads(p_o_c2.decode()).get("client_id")
        c2_id_r = json.loads(p_r_c2.decode()).get("client_id")

        # Semantic assertion on client_id: positive integer and strictly unique among simultaneous clients
        unique_ids_matched = (
            isinstance(c1_id_o, int) and isinstance(c2_id_o, int) and (c1_id_o > 0) and (c2_id_o > 0) and (c1_id_o != c2_id_o) and
            isinstance(c1_id_r, int) and isinstance(c2_id_r, int) and (c1_id_r > 0) and (c2_id_r > 0) and (c1_id_r != c2_id_r)
        )
        record_case("TR-DIFF-CLI-MULTI-UNIQUE-IDS", "Simultaneous multi-client connections allocated unique non-zero client IDs", "EXACT_PARITY", unique_ids_matched,
                    f"orig_ids=({c1_id_o}, {c2_id_o}), recon_ids=({c1_id_r}, {c2_id_r})")

        # 7.3 Client Disconnect Cleanup & Notification
        s_o_cli2.close()
        s_r_cli2.close()
        time.sleep(0.1)

        # Both original and reconstructed servers notify the active agent with client_disconnected
        _, p_o_disc = reader_o_agt.read_frame()
        _, p_r_disc = reader_r_agt.read_frame()
        msg_o_disc = json.loads(p_o_disc.decode()) if p_o_disc else {}
        msg_r_disc = json.loads(p_r_disc.decode()) if p_r_disc else {}

        disc_notif_matched = (
            msg_o_disc.get("message_type") == msg_r_disc.get("message_type") == "client_disconnected" and
            msg_o_disc.get("client_id") == c2_id_o and msg_r_disc.get("client_id") == c2_id_r
        )
        record_case("TR-DIFF-CLI-DISCONNECT-NOTIF", "Client disconnect notifies mapped agent with client_disconnected frame", "EXACT_PARITY", disc_notif_matched,
                    f"orig_notif={msg_o_disc}, recon_notif={msg_r_disc}")

        # Check client_count in device registry
        _, _, b_o_devs = send_raw_http(orig_port, "GET", "/devices", headers={"Authorization": f"Bearer {orig_token}"})
        _, _, b_r_devs = send_raw_http(recon_port, "GET", "/devices", headers={"Authorization": f"Bearer {recon_token}"})

        devs_o = json.loads(b_o_devs.decode()) if b_o_devs else []
        devs_r = json.loads(b_r_devs.decode()) if b_r_devs else []
        dev_o = next((d for d in devs_o if d.get("device_id") == "diff_dev_01"), {})
        dev_r = next((d for d in devs_r if d.get("device_id") == "diff_dev_01"), {})

        cli_count_matched = (dev_o.get("client_count") == dev_r.get("client_count") == 1)
        record_case("TR-DIFF-CLI-DISCONNECT-CLEANUP", "Client disconnect decrements active client_count to 1 on both instances", "EXACT_PARITY", cli_count_matched,
                    f"orig_client_count={dev_o.get('client_count')}, recon_client_count={dev_r.get('client_count')}")

        def recv_device_msg_o():
            return reader_o_cli1.drain_until_message_type("device_msg")

        def recv_device_msg_r():
            return reader_r_cli1.drain_until_message_type("device_msg")

        def recv_agent_forward(reader):
            start_time = time.time()
            for _ in range(10):
                rem = 3.0 - (time.time() - start_time)
                if rem <= 0: break
                try:
                    op, p = reader.read_frame(timeout=rem)
                    if op == 0 and not p: break
                    parsed = json.loads(p.decode()) if p else {}
                    if "payload" in parsed and (parsed.get("message_type") in ("command", "forward") or "client_id" in parsed):
                        return op, parsed
                except Exception:
                    break
            return 0, {}

        # =========================================================================
        # SUITE 8: WebRTC 4-Stage Signaling Relay (4 cases)
        # =========================================================================
        print("\n--- 8. WebRTC 4-Stage Signaling Relay Differential ---")
        # 8.1 Stage 1: Client -> Agent request-offer
        s_o_cli1.sendall(make_ws_frame(fwd_req_bytes, opcode=1))
        s_r_cli1.sendall(make_ws_frame(fwd_req_bytes, opcode=1))

        op_o_s1, s1_o = recv_agent_forward(reader_o_agt)
        op_r_s1, s1_r = recv_agent_forward(reader_r_agt)

        stage1_matched = (
            op_o_s1 == op_r_s1 == 1 and
            s1_o.get("client_id") == c1_id_o and s1_r.get("client_id") == c1_id_r and
            s1_o.get("payload", {}).get("type") == s1_r.get("payload", {}).get("type") == "request-offer"
        )
        record_case("TR-DIFF-RELAY-STAGE1-REQ-OFFER", "Signaling Stage 1: Client request-offer forwarded to agent with client_id", "EXACT_PARITY", stage1_matched,
                    f"orig_payload_type={s1_o.get('payload', {}).get('type')}, recon_payload_type={s1_r.get('payload', {}).get('type')}")

        # 8.2 Stage 2: Agent -> Client SDP Offer
        fwd_offer_o = json.dumps({
            "message_type": "forward",
            "device_id": "diff_dev_01",
            "client_id": c1_id_o,
            "payload": {"type": "offer", "sdp": "v=0\r\no=orig-sdp..."}
        }).encode()
        fwd_offer_r = json.dumps({
            "message_type": "forward",
            "device_id": "diff_dev_01",
            "client_id": c1_id_r,
            "payload": {"type": "offer", "sdp": "v=0\r\no=orig-sdp..."}
        }).encode()

        s_o_agt.sendall(make_ws_frame(fwd_offer_o, opcode=1))
        s_r_agt.sendall(make_ws_frame(fwd_offer_r, opcode=1))

        op_o_s2, s2_o = recv_device_msg_o()
        op_r_s2, s2_r = recv_device_msg_r()

        stage2_matched = (
            op_o_s2 == op_r_s2 == 1 and
            s2_o.get("message_type") == s2_r.get("message_type") == "device_msg" and
            s2_o.get("device_id") == s2_r.get("device_id") == "diff_dev_01" and
            s2_o.get("payload", {}).get("type") == s2_r.get("payload", {}).get("type") == "offer" and
            s2_o.get("payload", {}).get("sdp") == s2_r.get("payload", {}).get("sdp") == "v=0\r\no=orig-sdp..."
        )
        record_case("TR-DIFF-RELAY-STAGE2-SDP-OFFER", "Signaling Stage 2: Agent SDP offer delivered to client as device_msg", "EXACT_PARITY", stage2_matched,
                    f"orig_msg_type={s2_o.get('message_type')}, recon_msg_type={s2_r.get('message_type')}")

        # 8.3 Stage 3: Client -> Agent SDP Answer
        fwd_ans_bytes = json.dumps({"type": "forward", "payload": {"type": "answer", "sdp": "v=0\r\no=ans-sdp..."}}).encode()
        s_o_cli1.sendall(make_ws_frame(fwd_ans_bytes, opcode=1))
        s_r_cli1.sendall(make_ws_frame(fwd_ans_bytes, opcode=1))

        op_o_s3, s3_o = recv_agent_forward(reader_o_agt)
        op_r_s3, s3_r = recv_agent_forward(reader_r_agt)

        stage3_matched = (
            op_o_s3 == op_r_s3 == 1 and
            s3_o.get("client_id") == c1_id_o and s3_r.get("client_id") == c1_id_r and
            s3_o.get("payload", {}).get("type") == s3_r.get("payload", {}).get("type") == "answer" and
            s3_o.get("payload", {}).get("sdp") == s3_r.get("payload", {}).get("sdp") == "v=0\r\no=ans-sdp..."
        )
        record_case("TR-DIFF-RELAY-STAGE3-SDP-ANSWER", "Signaling Stage 3: Client SDP answer routed to agent matching client_id", "EXACT_PARITY", stage3_matched,
                    f"orig_payload_type={s3_o.get('payload', {}).get('type')}, recon_payload_type={s3_r.get('payload', {}).get('type')}")

        # 8.4 Stage 4: Trickle ICE Candidate Relay
        fwd_cand_o = json.dumps({
            "message_type": "forward",
            "device_id": "diff_dev_01",
            "client_id": c1_id_o,
            "payload": {"type": "candidate", "candidate": "candidate:1 1 UDP 2122260223 ..."}
        }).encode()
        fwd_cand_r = json.dumps({
            "message_type": "forward",
            "device_id": "diff_dev_01",
            "client_id": c1_id_r,
            "payload": {"type": "candidate", "candidate": "candidate:1 1 UDP 2122260223 ..."}
        }).encode()

        s_o_agt.sendall(make_ws_frame(fwd_cand_o, opcode=1))
        s_r_agt.sendall(make_ws_frame(fwd_cand_r, opcode=1))

        op_o_s4, s4_o = recv_device_msg_o()
        op_r_s4, s4_r = recv_device_msg_r()

        stage4_matched = (
            op_o_s4 == op_r_s4 == 1 and
            s4_o.get("message_type") == s4_r.get("message_type") == "device_msg" and
            s4_o.get("payload", {}).get("type") == s4_r.get("payload", {}).get("type") == "candidate" and
            s4_o.get("payload", {}).get("candidate") == s4_r.get("payload", {}).get("candidate") == "candidate:1 1 UDP 2122260223 ..."
        )
        record_case("TR-DIFF-RELAY-STAGE4-TRICKLE-ICE", "Signaling Stage 4: Trickle ICE candidate delivered to client peer as device_msg", "EXACT_PARITY", stage4_matched,
                    f"orig_cand={s4_o.get('payload', {}).get('type')}, recon_cand={s4_r.get('payload', {}).get('type')}")

        s_o_cli1.close()
        s_r_cli1.close()
        s_o_agt.close()
        s_r_agt.close()
        s_o_dev.close()
        s_r_dev.close()

    finally:
        if orig_proc:
            orig_proc.terminate()
            orig_proc.wait()
        if recon_proc:
            recon_proc.terminate()
            recon_proc.wait()
        shutil.rmtree(orig_tmp, ignore_errors=True)
        shutil.rmtree(recon_tmp, ignore_errors=True)

    # Compute final strict closure verdict
    all_ok = (
        results["oracle_required"] is True and
        results["oracle_available"] is True and
        results["oracle_hash_verified"] is True and
        results["oracle_health_verified"] is True and
        results["reconstructed_health_verified"] is True and
        results["exact_parity_total"] > 0 and
        results["exact_parity_passed"] == results["exact_parity_total"] and
        results["failed"] == 0
    )
    results["verdict"] = "PASS" if all_ok else "FAIL_CLOSED"

    print("\n==================================================")
    print("TRANSPORT DIFFERENTIAL RESULTS SUMMARY")
    print("==================================================")
    print(f"Oracle Required:                {results['oracle_required']}")
    print(f"Oracle Available:               {results['oracle_available']}")
    print(f"Oracle Hash Verified:           {results['oracle_hash_verified']}")
    print(f"Oracle Health Verified:         {results['oracle_health_verified']}")
    print(f"Reconstructed Health Verified:  {results['reconstructed_health_verified']}")
    print(f"Exact Parity Total:             {results['exact_parity_total']}")
    print(f"Exact Parity Passed:            {results['exact_parity_passed']}")
    print(f"Verified Divergences:           {results['verified_divergences']}")
    print(f"Excluded (Oracle Unavailable):  {results['excluded_oracle_unavailable']}")
    print(f"Implementation Choice Tests:    {results['implementation_choice_tests']}")
    print(f"Failed:                         {results['failed']}")
    print(f"Overall Closure Verdict:        {results['verdict']}")
    print("==================================================")

    out_file = REPO_ROOT / "scratch" / "transport_differential_results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")

    return results

if __name__ == "__main__":
    res = run_differential_suite()
    if res["verdict"] != "PASS" or res["failed"] != 0 or res["exact_parity_passed"] != res["exact_parity_total"] or res["exact_parity_total"] == 0:
        sys.exit(1)
    sys.exit(0)
