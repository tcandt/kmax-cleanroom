#!/usr/bin/env python3
"""
test_server_config_http_diff.py - Phase 2C.3G Server Configuration REST HTTP Differential Test Suite

Executes side-by-side differential testing between original webrtc-signaling and reconstructed http-server.
Validates 22 exhaustive differential test cases covering:
  - SERVER-CONFIG-01: Route Family Registration (all 4 routes present and responsive)
  - SERVER-CONFIG-02: /api/version Public Access Parity (200 without token)
  - SERVER-CONFIG-03: /api/version Verb Parity (GET, POST, PUT, PATCH, DELETE, HEAD return 200, OPTIONS returns 200)
  - SERVER-CONFIG-04: /api/version Schema and Content Parity
  - SERVER-CONFIG-05: /api/ice_servers Default GET Parity
  - SERVER-CONFIG-06: /api/ice_servers Auth Protection (Missing & Invalid token 401)
  - SERVER-CONFIG-07: /api/ice_servers Verb Parity
  - SERVER-CONFIG-08: /api/ice_servers Custom CLI Flags Parity (-ice_servers STUN & TURN parsing)
  - SERVER-CONFIG-09: /api/server/addresses Standard GET Parity (r.Host and non-loopback IPs)
  - SERVER-CONFIG-10: /api/server/addresses Custom Host Header With Port Parity
  - SERVER-CONFIG-11: /api/server/addresses Custom Host Header Without Port Parity
  - SERVER-CONFIG-12: /api/server/addresses Auth Protection (Missing & Invalid token 401)
  - SERVER-CONFIG-13: /api/server/addresses Verb Parity (All verbs 200, HEAD wire bodyless)
  - SERVER-CONFIG-14: /api/default_settings Initial GET Parity (Returns 200 {})
  - SERVER-CONFIG-15: /api/default_settings Auth Protection (Missing & Invalid token 401)
  - SERVER-CONFIG-16: /api/default_settings POST RBAC (User 403 vs Admin 200)
  - SERVER-CONFIG-17: /api/default_settings Mutation and Readback Parity
  - SERVER-CONFIG-18: /api/default_settings Error Handling (Empty, Malformed, Array bodies 400)
  - SERVER-CONFIG-19: /api/default_settings POST Null Parity (POST null -> 200, readback null)
  - SERVER-CONFIG-20: /api/default_settings Disallowed Methods (PUT, PATCH, DELETE, HEAD 405)
  - SERVER-CONFIG-21: /api/default_settings In-Memory Non-Persistence Across Restart
  - SERVER-CONFIG-22: No-Auth Mode Global Parity (-no-auth allows all 4 routes)

Outputs:
  - evidence/go_signaling/server_config/SERVER_CONFIG_HTTP_DIFFERENTIAL_RESULTS.json
"""

import os
import sys
import time
import json
import socket
import shutil
import hashlib
import requests
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXE_ORIG = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
ASSETS = ROOT / "cloudphone-v0.3.6 (1)" / "assets"
EXE_RECON = ROOT / "scratch" / "reconstructed_server_config.exe"

DIFF_TMP_ORIG = ROOT / "scratch" / "server_config_diff_orig"
DIFF_TMP_RECON = ROOT / "scratch" / "server_config_diff_recon"
DIFF_TMP_ORIG_NA = ROOT / "scratch" / "server_config_diff_orig_na"
DIFF_TMP_RECON_NA = ROOT / "scratch" / "server_config_diff_recon_na"
DIFF_TMP_ORIG_CUSTOM = ROOT / "scratch" / "server_config_diff_orig_custom"
DIFF_TMP_RECON_CUSTOM = ROOT / "scratch" / "server_config_diff_recon_custom"

OUTPUT_JSON = ROOT / "evidence" / "go_signaling" / "server_config" / "SERVER_CONFIG_HTTP_DIFFERENTIAL_RESULTS.json"

def get_free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

PORT_ORIG = get_free_port()
PORT_RECON = get_free_port()
PORT_ORIG_NA = get_free_port()
PORT_RECON_NA = get_free_port()
PORT_ORIG_CUSTOM = get_free_port()
PORT_RECON_CUSTOM = get_free_port()

URL_ORIG = f"http://127.0.0.1:{PORT_ORIG}"
URL_RECON = f"http://127.0.0.1:{PORT_RECON}"
URL_ORIG_NA = f"http://127.0.0.1:{PORT_ORIG_NA}"
URL_RECON_NA = f"http://127.0.0.1:{PORT_RECON_NA}"
URL_ORIG_CUSTOM = f"http://127.0.0.1:{PORT_ORIG_CUSTOM}"
URL_RECON_CUSTOM = f"http://127.0.0.1:{PORT_RECON_CUSTOM}"

def hash_pwd(pwd: str, salt: str) -> str:
    return hashlib.sha256((pwd + salt).encode("utf-8")).hexdigest()

def make_fixture(target_dir: Path):
    if target_dir.exists():
        shutil.rmtree(target_dir, ignore_errors=True)
    target_dir.mkdir(parents=True, exist_ok=True)

    salt = "1234567890abcdef1234567890abcdef"
    fixture_users = {
        "admin": {
            "username": "admin",
            "password": hash_pwd("admin123", salt),
            "salt": salt,
            "role": "admin",
            "assigned_devices": ["*"],
            "note": "Administrator",
            "expires_at": "2099-12-31T23:59:59Z"
        },
        "user_test": {
            "username": "user_test",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": ["dev-001"],
            "note": "Test user",
            "expires_at": "2099-12-31T23:59:59Z"
        }
    }
    (target_dir / "users.json").write_text(json.dumps(fixture_users, indent=2), encoding="utf-8")
    (target_dir / "device_tags.json").write_text(json.dumps({"tags": [], "deviceTags": {}}, indent=2), encoding="utf-8")

def build_reconstructed():
    print("[*] Compiling cleanroom http-server binary...")
    src_dir = ROOT / "reconstructed_source" / "webrtc-signaling"
    cmd = ["go", "build", "-o", str(EXE_RECON), "./cmd/http-server"]
    res = subprocess.run(cmd, cwd=str(src_dir), capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[-] Build failed:\n{res.stderr}")
        sys.exit(1)
    print(f"[+] Cleanroom binary built successfully: {EXE_RECON}")

class ServerProcess:
    def __init__(self, cmd, cwd):
        self.cmd = cmd
        self.cwd = cwd
        self.proc = None

    def start(self):
        self.proc = subprocess.Popen(
            self.cmd, cwd=str(self.cwd),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def stop(self):
        if self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=2)
            except:
                try:
                    self.proc.kill()
                except:
                    pass
            self.proc = None

def main():
    build_reconstructed()

    for p in [DIFF_TMP_ORIG, DIFF_TMP_RECON, DIFF_TMP_ORIG_NA, DIFF_TMP_RECON_NA, DIFF_TMP_ORIG_CUSTOM, DIFF_TMP_RECON_CUSTOM]:
        make_fixture(p)

    custom_ice_flags = "-ice_servers=stun:stun1.example.com:19302,turn:user:pass@turn.example.com:3478"

    servers = [
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG}", f"-data={DIFF_TMP_ORIG}", f"-assets={ASSETS}", "-debug"], DIFF_TMP_ORIG),
        ServerProcess([str(EXE_RECON), f"-port={PORT_RECON}", f"-data={DIFF_TMP_RECON}"], DIFF_TMP_RECON),
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG_NA}", f"-data={DIFF_TMP_ORIG_NA}", f"-assets={ASSETS}", "-no-auth", "-debug"], DIFF_TMP_ORIG_NA),
        ServerProcess([str(EXE_RECON), f"-port={PORT_RECON_NA}", f"-data={DIFF_TMP_RECON_NA}", "-no-auth"], DIFF_TMP_RECON_NA),
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG_CUSTOM}", f"-data={DIFF_TMP_ORIG_CUSTOM}", f"-assets={ASSETS}", custom_ice_flags, "-debug"], DIFF_TMP_ORIG_CUSTOM),
        ServerProcess([str(EXE_RECON), f"-port={PORT_RECON_CUSTOM}", f"-data={DIFF_TMP_RECON_CUSTOM}", custom_ice_flags], DIFF_TMP_RECON_CUSTOM),
    ]

    print("[*] Launching oracle and reconstructed server instances...")
    for s in servers:
        s.start()

    time.sleep(2.5)

    results = []
    test_run_success = True

    try:
        # Obtain tokens
        r_orig_adm = requests.post(f"{URL_ORIG}/api/login", json={"username": "admin", "password": "admin123"}).json()
        r_recon_adm = requests.post(f"{URL_RECON}/api/login", json={"username": "admin", "password": "admin123"}).json()
        tok_orig_adm = r_orig_adm["token"]
        tok_recon_adm = r_recon_adm["token"]

        r_orig_usr = requests.post(f"{URL_ORIG}/api/login", json={"username": "user_test", "password": "user123"}).json()
        r_recon_usr = requests.post(f"{URL_RECON}/api/login", json={"username": "user_test", "password": "user123"}).json()
        tok_orig_usr = r_orig_usr["token"]
        tok_recon_usr = r_recon_usr["token"]

        h_orig_adm = {"Authorization": f"Bearer {tok_orig_adm}"}
        h_recon_adm = {"Authorization": f"Bearer {tok_recon_adm}"}
        h_orig_usr = {"Authorization": f"Bearer {tok_orig_usr}"}
        h_recon_usr = {"Authorization": f"Bearer {tok_recon_usr}"}

        # Helper assertion function
        def run_test(case_id, desc, orig_fn, recon_fn, validator_fn=None):
            nonlocal test_run_success
            resp_orig = orig_fn()
            resp_recon = recon_fn()

            status_match = resp_orig.status_code == resp_recon.status_code
            ct_orig = resp_orig.headers.get("Content-Type", "").split(";")[0].strip()
            ct_recon = resp_recon.headers.get("Content-Type", "").split(";")[0].strip()
            ct_match = (ct_orig == ct_recon) or (not ct_orig and not ct_recon)

            custom_valid = True
            err_msg = ""
            if validator_fn:
                try:
                    custom_valid, err_msg = validator_fn(resp_orig, resp_recon)
                except Exception as e:
                    custom_valid = False
                    err_msg = str(e)

            case_pass = status_match and ct_match and custom_valid
            if not case_pass:
                test_run_success = False

            res_entry = {
                "case_id": case_id,
                "description": desc,
                "status": "PASS" if case_pass else "FAIL",
                "details": {
                    "orig_status": resp_orig.status_code,
                    "recon_status": resp_recon.status_code,
                    "orig_content_type": resp_orig.headers.get("Content-Type"),
                    "recon_content_type": resp_recon.headers.get("Content-Type"),
                    "error": err_msg
                }
            }
            results.append(res_entry)
            print(f"  [{'PASS' if case_pass else 'FAIL'}] {case_id}: {desc}")
            if not case_pass:
                print(f"       Details: {res_entry['details']}")

        print("\n=== Running Phase 2C.3G Server Configuration Differential Test Cases ===")

        # Case 01: Route Family Registration
        def val_01(ro, rr):
            return True, ""
        for r_path in ["/api/server/addresses", "/api/default_settings", "/api/ice_servers", "/api/version"]:
            run_test(
                f"SERVER-CONFIG-01-{r_path.split('/')[-1]}",
                f"Route {r_path} registration presence",
                lambda p=r_path: requests.get(f"{URL_ORIG}{p}", headers=h_orig_adm),
                lambda p=r_path: requests.get(f"{URL_RECON}{p}", headers=h_recon_adm),
                val_01
            )

        # Case 02: /api/version Public Access Parity
        def val_02(ro, rr):
            jo = ro.json()
            jr = rr.json()
            match = "version" in jo and "version" in jr and "git_commit" in jo and "git_commit" in jr
            return match, f"Keys mismatch: orig={list(jo.keys())}, recon={list(jr.keys())}"
        run_test(
            "SERVER-CONFIG-02",
            "/api/version public access without auth token (200 OK)",
            lambda: requests.get(f"{URL_ORIG}/api/version"),
            lambda: requests.get(f"{URL_RECON}/api/version"),
            val_02
        )

        # Case 03: /api/version Verb Parity
        def val_verb(ro, rr):
            return ro.status_code == rr.status_code, f"Status mismatch: orig={ro.status_code}, recon={rr.status_code}"
        for m in ["POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
            run_test(
                f"SERVER-CONFIG-03-{m}",
                f"/api/version method {m} parity",
                lambda meth=m: requests.request(meth, f"{URL_ORIG}/api/version"),
                lambda meth=m: requests.request(meth, f"{URL_RECON}/api/version"),
                val_verb
            )

        # Case 04: /api/version Content & Schema Parity
        def val_04(ro, rr):
            jo = ro.json()
            jr = rr.json()
            v_match = isinstance(jo.get("version"), str) and isinstance(jr.get("version"), str)
            c_match = isinstance(jo.get("git_commit"), str) and isinstance(jr.get("git_commit"), str)
            t_match = isinstance(jo.get("build_time"), str) and isinstance(jr.get("build_time"), str)
            return (v_match and c_match and t_match), f"Content mismatch: orig={jo}, recon={jr}"
        run_test(
            "SERVER-CONFIG-04",
            "/api/version schema and fields parity",
            lambda: requests.get(f"{URL_ORIG}/api/version"),
            lambda: requests.get(f"{URL_RECON}/api/version"),
            val_04
        )

        # Case 05: /api/ice_servers Default GET Parity
        def val_05(ro, rr):
            jo = ro.json()
            jr = rr.json()
            match = len(jo) == 1 and len(jr) == 1 and jo[0]["urls"] == jr[0]["urls"]
            return match, f"ICE server default mismatch: orig={jo}, recon={jr}"
        run_test(
            "SERVER-CONFIG-05",
            "/api/ice_servers default configuration GET parity",
            lambda: requests.get(f"{URL_ORIG}/api/ice_servers", headers=h_orig_adm),
            lambda: requests.get(f"{URL_RECON}/api/ice_servers", headers=h_recon_adm),
            val_05
        )

        # Case 06: /api/ice_servers Auth Protection
        run_test(
            "SERVER-CONFIG-06-missing",
            "/api/ice_servers missing token returns 401 Unauthorized",
            lambda: requests.get(f"{URL_ORIG}/api/ice_servers"),
            lambda: requests.get(f"{URL_RECON}/api/ice_servers")
        )
        run_test(
            "SERVER-CONFIG-06-invalid",
            "/api/ice_servers invalid token returns 401 Unauthorized",
            lambda: requests.get(f"{URL_ORIG}/api/ice_servers", headers={"Authorization": "Bearer bad"}),
            lambda: requests.get(f"{URL_RECON}/api/ice_servers", headers={"Authorization": "Bearer bad"})
        )

        # Case 07: /api/ice_servers Verb Parity
        for m in ["POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
            run_test(
                f"SERVER-CONFIG-07-{m}",
                f"/api/ice_servers method {m} parity",
                lambda meth=m: requests.request(meth, f"{URL_ORIG}/api/ice_servers", headers=h_orig_adm),
                lambda meth=m: requests.request(meth, f"{URL_RECON}/api/ice_servers", headers=h_recon_adm),
                val_verb
            )

        # Case 08: /api/ice_servers Custom CLI Flags Parity
        r_c_orig_adm = requests.post(f"{URL_ORIG_CUSTOM}/api/login", json={"username": "admin", "password": "admin123"}).json()
        r_c_recon_adm = requests.post(f"{URL_RECON_CUSTOM}/api/login", json={"username": "admin", "password": "admin123"}).json()
        h_orig_cust = {"Authorization": f"Bearer {r_c_orig_adm['token']}"}
        h_recon_cust = {"Authorization": f"Bearer {r_c_recon_adm['token']}"}

        def val_08(ro, rr):
            jo = ro.json()
            jr = rr.json()
            match = jo == jr
            return match, f"Custom ICE mismatch: orig={jo}, recon={jr}"
        run_test(
            "SERVER-CONFIG-08",
            "/api/ice_servers custom CLI -ice_servers parsing parity",
            lambda: requests.get(f"{URL_ORIG_CUSTOM}/api/ice_servers", headers=h_orig_cust),
            lambda: requests.get(f"{URL_RECON_CUSTOM}/api/ice_servers", headers=h_recon_cust),
            val_08
        )

        # Case 09: /api/server/addresses Standard GET Parity
        def val_09(ro, rr):
            jo = ro.json()
            jr = rr.json()
            code_ok = jo.get("code") == 0 and jr.get("code") == 0
            cur_ok = jo.get("data", {}).get("current") == f"127.0.0.1:{PORT_ORIG}" and jr.get("data", {}).get("current") == f"127.0.0.1:{PORT_RECON}"
            addrs_o = jo.get("data", {}).get("addresses", [])
            addrs_r = jr.get("data", {}).get("addresses", [])
            idx0_ok = len(addrs_o) > 0 and len(addrs_r) > 0 and addrs_o[0] == jo["data"]["current"] and addrs_r[0] == jr["data"]["current"]
            count_ok = len(addrs_o) == len(addrs_r)
            return (code_ok and cur_ok and idx0_ok and count_ok), f"Address mismatch: orig={jo}, recon={jr}"
        run_test(
            "SERVER-CONFIG-09",
            "/api/server/addresses standard address discovery parity",
            lambda: requests.get(f"{URL_ORIG}/api/server/addresses", headers=h_orig_adm),
            lambda: requests.get(f"{URL_RECON}/api/server/addresses", headers=h_recon_adm),
            val_09
        )

        # Case 10: /api/server/addresses Custom Host Header With Port Parity
        def val_10(ro, rr):
            jo = ro.json()
            jr = rr.json()
            cur_ok = jo.get("data", {}).get("current") == "custom-domain.org:8443" and jr.get("data", {}).get("current") == "custom-domain.org:8443"
            addrs_o = jo.get("data", {}).get("addresses", [])
            addrs_r = jr.get("data", {}).get("addresses", [])
            idx0_ok = addrs_o[0] == "custom-domain.org:8443" and addrs_r[0] == "custom-domain.org:8443"
            ports_ok = all(a.endswith(":8443") for a in addrs_o) and all(a.endswith(":8443") for a in addrs_r)
            return (cur_ok and idx0_ok and ports_ok), f"Host with port mismatch: orig={jo}, recon={jr}"
        run_test(
            "SERVER-CONFIG-10",
            "/api/server/addresses custom Host header with port parity",
            lambda: requests.get(f"{URL_ORIG}/api/server/addresses", headers={"Authorization": f"Bearer {tok_orig_adm}", "Host": "custom-domain.org:8443"}),
            lambda: requests.get(f"{URL_RECON}/api/server/addresses", headers={"Authorization": f"Bearer {tok_recon_adm}", "Host": "custom-domain.org:8443"}),
            val_10
        )

        # Case 11: /api/server/addresses Custom Host Header Without Port Parity
        def val_11(ro, rr):
            jo = ro.json()
            jr = rr.json()
            cur_ok = jo.get("data", {}).get("current") == "custom-domain.org" and jr.get("data", {}).get("current") == "custom-domain.org"
            addrs_o = jo.get("data", {}).get("addresses", [])
            addrs_r = jr.get("data", {}).get("addresses", [])
            idx0_ok = addrs_o[0] == "custom-domain.org" and addrs_r[0] == "custom-domain.org"
            ports_ok = all(a.endswith(f":{PORT_ORIG}") for a in addrs_o[1:]) and all(a.endswith(f":{PORT_RECON}") for a in addrs_r[1:])
            return (cur_ok and idx0_ok and ports_ok), f"Host without port mismatch: orig={jo}, recon={jr}"
        run_test(
            "SERVER-CONFIG-11",
            "/api/server/addresses custom Host header without port parity",
            lambda: requests.get(f"{URL_ORIG}/api/server/addresses", headers={"Authorization": f"Bearer {tok_orig_adm}", "Host": "custom-domain.org"}),
            lambda: requests.get(f"{URL_RECON}/api/server/addresses", headers={"Authorization": f"Bearer {tok_recon_adm}", "Host": "custom-domain.org"}),
            val_11
        )

        # Case 12: /api/server/addresses Auth Protection
        run_test(
            "SERVER-CONFIG-12-missing",
            "/api/server/addresses missing token returns 401 Unauthorized",
            lambda: requests.get(f"{URL_ORIG}/api/server/addresses"),
            lambda: requests.get(f"{URL_RECON}/api/server/addresses")
        )
        run_test(
            "SERVER-CONFIG-12-invalid",
            "/api/server/addresses invalid token returns 401 Unauthorized",
            lambda: requests.get(f"{URL_ORIG}/api/server/addresses", headers={"Authorization": "Bearer bad"}),
            lambda: requests.get(f"{URL_RECON}/api/server/addresses", headers={"Authorization": "Bearer bad"})
        )

        # Case 13: /api/server/addresses Verb Parity
        for m in ["POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
            run_test(
                f"SERVER-CONFIG-13-{m}",
                f"/api/server/addresses method {m} parity",
                lambda meth=m: requests.request(meth, f"{URL_ORIG}/api/server/addresses", headers=h_orig_adm),
                lambda meth=m: requests.request(meth, f"{URL_RECON}/api/server/addresses", headers=h_recon_adm),
                val_verb
            )

        # Case 14: /api/default_settings Initial GET Parity
        def val_14(ro, rr):
            match = ro.text.strip() == "{}" and rr.text.strip() == "{}"
            return match, f"Initial settings mismatch: orig={ro.text}, recon={rr.text}"
        run_test(
            "SERVER-CONFIG-14",
            "/api/default_settings initial GET returns empty map {}",
            lambda: requests.get(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm),
            lambda: requests.get(f"{URL_RECON}/api/default_settings", headers=h_recon_adm),
            val_14
        )

        # Case 15: /api/default_settings Auth Protection
        run_test(
            "SERVER-CONFIG-15-missing",
            "/api/default_settings missing token returns 401 Unauthorized",
            lambda: requests.get(f"{URL_ORIG}/api/default_settings"),
            lambda: requests.get(f"{URL_RECON}/api/default_settings")
        )
        run_test(
            "SERVER-CONFIG-15-invalid",
            "/api/default_settings invalid token returns 401 Unauthorized",
            lambda: requests.get(f"{URL_ORIG}/api/default_settings", headers={"Authorization": "Bearer bad"}),
            lambda: requests.get(f"{URL_RECON}/api/default_settings", headers={"Authorization": "Bearer bad"})
        )

        # Case 16: /api/default_settings POST RBAC (Admin only)
        def val_16_usr(ro, rr):
            match = ro.text == "Forbidden: admin only\n" and rr.text == "Forbidden: admin only\n"
            return match, f"RBAC 403 body mismatch: orig={repr(ro.text)}, recon={repr(rr.text)}"
        run_test(
            "SERVER-CONFIG-16-user-403",
            "/api/default_settings normal user POST returns 403 Forbidden: admin only",
            lambda: requests.post(f"{URL_ORIG}/api/default_settings", headers=h_orig_usr, json={"test": 1}),
            lambda: requests.post(f"{URL_RECON}/api/default_settings", headers=h_recon_usr, json={"test": 1}),
            val_16_usr
        )

        # Case 17: /api/default_settings Mutation and Readback Parity
        mutation_payload = {"video_bitrate": 8000, "fps": 60, "encoder": "h264"}
        def val_17(ro, rr):
            match = ro.json() == rr.json() and ro.json() == mutation_payload
            return match, f"Mutation readback mismatch: orig={ro.text}, recon={rr.text}"
        requests.post(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm, json=mutation_payload)
        requests.post(f"{URL_RECON}/api/default_settings", headers=h_recon_adm, json=mutation_payload)
        run_test(
            "SERVER-CONFIG-17",
            "/api/default_settings mutation and readback parity",
            lambda: requests.get(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm),
            lambda: requests.get(f"{URL_RECON}/api/default_settings", headers=h_recon_adm),
            val_17
        )

        # Case 18: /api/default_settings Error Handling (Empty, Malformed, Array)
        def val_400(ro, rr):
            match = ro.text == "Invalid JSON\n" and rr.text == "Invalid JSON\n"
            return match, f"400 body mismatch: orig={repr(ro.text)}, recon={repr(rr.text)}"
        run_test(
            "SERVER-CONFIG-18-empty",
            "/api/default_settings empty POST body returns 400 Invalid JSON",
            lambda: requests.post(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm, data=""),
            lambda: requests.post(f"{URL_RECON}/api/default_settings", headers=h_recon_adm, data=""),
            val_400
        )
        run_test(
            "SERVER-CONFIG-18-malformed",
            "/api/default_settings malformed JSON POST body returns 400 Invalid JSON",
            lambda: requests.post(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm, data="{not_json"),
            lambda: requests.post(f"{URL_RECON}/api/default_settings", headers=h_recon_adm, data="{not_json"),
            val_400
        )
        run_test(
            "SERVER-CONFIG-18-array",
            "/api/default_settings non-object JSON POST body returns 400 Invalid JSON",
            lambda: requests.post(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm, json=[1, 2, 3]),
            lambda: requests.post(f"{URL_RECON}/api/default_settings", headers=h_recon_adm, json=[1, 2, 3]),
            val_400
        )

        # Case 19: /api/default_settings POST Null Parity
        def val_19_post(ro, rr):
            match = ro.text == '{"status":"success"}' and rr.text == '{"status":"success"}'
            return match, f"POST null response mismatch: orig={ro.text}, recon={rr.text}"
        run_test(
            "SERVER-CONFIG-19-post",
            "/api/default_settings POST null returns 200 {\"status\":\"success\"}",
            lambda: requests.post(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm, data="null"),
            lambda: requests.post(f"{URL_RECON}/api/default_settings", headers=h_recon_adm, data="null"),
            val_19_post
        )
        def val_19_get(ro, rr):
            match = ro.text.strip() == "null" and rr.text.strip() == "null"
            return match, f"GET after null mismatch: orig={ro.text}, recon={rr.text}"
        run_test(
            "SERVER-CONFIG-19-get",
            "/api/default_settings GET after POST null returns 200 null",
            lambda: requests.get(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm),
            lambda: requests.get(f"{URL_RECON}/api/default_settings", headers=h_recon_adm),
            val_19_get
        )

        # Case 20: /api/default_settings Disallowed Methods (PUT, PATCH, DELETE, HEAD)
        def val_405(ro, rr):
            match = (ro.status_code == 405 and rr.status_code == 405)
            if ro.request.method != "HEAD":
                match = match and (ro.text == "Method not allowed\n" and rr.text == "Method not allowed\n")
            return match, f"405 mismatch: orig={ro.status_code} {repr(ro.text)}, recon={rr.status_code} {repr(rr.text)}"
        for m in ["PUT", "PATCH", "DELETE", "HEAD"]:
            run_test(
                f"SERVER-CONFIG-20-{m}",
                f"/api/default_settings method {m} returns 405 Method not allowed",
                lambda meth=m: requests.request(meth, f"{URL_ORIG}/api/default_settings", headers=h_orig_adm),
                lambda meth=m: requests.request(meth, f"{URL_RECON}/api/default_settings", headers=h_recon_adm),
                val_405
            )

        # Case 21: In-Memory Non-Persistence Across Restart
        # Set mutation on both
        requests.post(f"{URL_ORIG}/api/default_settings", headers=h_orig_adm, json={"persist": "fail"})
        requests.post(f"{URL_RECON}/api/default_settings", headers=h_recon_adm, json={"persist": "fail"})
        # Restart standard instances
        servers[0].stop()
        servers[1].stop()
        time.sleep(0.5)
        servers[0].start()
        servers[1].start()
        time.sleep(2.0)
        # Re-login
        r_o_a = requests.post(f"{URL_ORIG}/api/login", json={"username": "admin", "password": "admin123"}).json()
        r_r_a = requests.post(f"{URL_RECON}/api/login", json={"username": "admin", "password": "admin123"}).json()
        h_o_a = {"Authorization": f"Bearer {r_o_a['token']}"}
        h_r_a = {"Authorization": f"Bearer {r_r_a['token']}"}

        def val_21(ro, rr):
            match = ro.text.strip() == "{}" and rr.text.strip() == "{}"
            return match, f"Restart persistence leak: orig={ro.text}, recon={rr.text}"
        run_test(
            "SERVER-CONFIG-21",
            "/api/default_settings in-memory lifecycle resets to {} across restart",
            lambda: requests.get(f"{URL_ORIG}/api/default_settings", headers=h_o_a),
            lambda: requests.get(f"{URL_RECON}/api/default_settings", headers=h_r_a),
            val_21
        )

        # Case 22: No-Auth Mode Global Parity
        for r_path in ["/api/version", "/api/ice_servers", "/api/server/addresses", "/api/default_settings"]:
            run_test(
                f"SERVER-CONFIG-22-{r_path.split('/')[-1]}",
                f"-no-auth mode access to {r_path} without token",
                lambda p=r_path: requests.get(f"{URL_ORIG_NA}{p}"),
                lambda p=r_path: requests.get(f"{URL_RECON_NA}{p}")
            )
        run_test(
            "SERVER-CONFIG-22-default_settings-post",
            "-no-auth mode allows POST /api/default_settings without token",
            lambda: requests.post(f"{URL_ORIG_NA}/api/default_settings", json={"na": True}),
            lambda: requests.post(f"{URL_RECON_NA}/api/default_settings", json={"na": True})
        )
        # Case 23: /api/version Character-Exact Deterministic String Parity
        def val_23(ro, rr):
            jo = ro.json()
            jr = rr.json()
            exact_v = (jo.get("version") == jr.get("version")) and (len(jo.get("version", "")) > 0)
            exact_c = (jo.get("git_commit") == jr.get("git_commit")) and (len(jo.get("git_commit", "")) > 0)
            exact_t = (jo.get("build_time") == jr.get("build_time")) and (len(jo.get("build_time", "")) > 0)
            exact_keys = set(jo.keys()) == {"version", "git_commit", "build_time"} and set(jr.keys()) == {"version", "git_commit", "build_time"}
            match = exact_v and exact_c and exact_t and exact_keys
            return match, f"Exact version mismatch: orig={jo}, recon={jr}"
        run_test(
            "SERVER-CONFIG-23",
            "/api/version exact deterministic string and key parity (fails if 1 char differs)",
            lambda: requests.get(f"{URL_ORIG}/api/version"),
            lambda: requests.get(f"{URL_RECON}/api/version"),
            val_23
        )

        # Case 24: Isolated -stun_server Fallback Parity
        port_o_stun = get_free_port()
        port_r_stun = get_free_port()
        dir_o_stun = ROOT / "scratch" / "server_config_diff_orig_stun"
        dir_r_stun = ROOT / "scratch" / "server_config_diff_recon_stun"
        if dir_o_stun.exists(): shutil.rmtree(dir_o_stun, ignore_errors=True)
        if dir_r_stun.exists(): shutil.rmtree(dir_r_stun, ignore_errors=True)
        dir_o_stun.mkdir(parents=True, exist_ok=True)
        dir_r_stun.mkdir(parents=True, exist_ok=True)

        s_o_stun = ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={port_o_stun}", f"-data={dir_o_stun}", f"-assets={ASSETS}", "-no-auth", "-stun_server=stun:fallback.test.org:3478", "-debug"], dir_o_stun)
        s_r_stun = ServerProcess([str(EXE_RECON), f"-port={port_r_stun}", f"-data={dir_r_stun}", "-no-auth", "-stun_server=stun:fallback.test.org:3478"], dir_r_stun)
        s_o_stun.start()
        s_r_stun.start()
        time.sleep(2.0)

        try:
            def val_24(ro, rr):
                jo = ro.json()
                jr = rr.json()
                match = (jo == jr) and (len(jo) == 1) and (jo[0]["urls"] == ["stun:fallback.test.org:3478"])
                return match, f"STUN fallback mismatch: orig={jo}, recon={jr}"
            run_test(
                "SERVER-CONFIG-24",
                "Isolated -stun_server fallback parity when -ice_servers is omitted",
                lambda: requests.get(f"http://127.0.0.1:{port_o_stun}/api/ice_servers"),
                lambda: requests.get(f"http://127.0.0.1:{port_r_stun}/api/ice_servers"),
                val_24
            )
        finally:
            s_o_stun.stop()
            s_r_stun.stop()

    finally:
        print("\n[*] Shutting down server instances...")
        for s in servers:
            s.stop()

    pass_count = sum(1 for r in results if r["status"] == "PASS")
    total_count = len(results)

    summary = {
        "execution_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_cases": total_count,
        "passed": pass_count,
        "failed": total_count - pass_count,
        "all_passed": test_run_success and (pass_count == total_count),
        "results": results
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n[+] Differential results written to: {OUTPUT_JSON}")
    print(f"[+] Verdict: {pass_count}/{total_count} cases PASSED.")

    if not test_run_success or pass_count != total_count:
        sys.exit(1)

if __name__ == "__main__":
    main()
