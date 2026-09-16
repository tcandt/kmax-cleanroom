#!/usr/bin/env python3
"""
test_license_http_diff.py - Phase 2C.3HR License & Entitlement REST Differential Verification Suite

Executes side-by-side differential tests comparing the canonical original binary oracle
against the cleanroom reconstructed HTTP signaling server across all license routes:
  - /api/activate
  - /api/license_status
  - /debug/license

Strict Invariants:
  - Dynamic denominator: cases calculated from results at runtime.
  - UNOBSERVED_LOCAL_VALID_SIGNATURE_SUCCESS excluded from test pass denominator.
  - Zero bypass / zero keygen: validates genuine original cryptographic rejection behavior.
  - Machine ID exact character-for-character parity.
  - HEAD representation Content-Length parity.
  - /debug/license 7-verb matrix covered (with and without -debug).
  - Activation JSON edge matrix (null, arrays, type mismatches).
  - Startup invalid license.txt file matrix.
"""

import os
import sys
import json
import time
import shutil
import socket
import hashlib
import requests
import subprocess
import base64
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
EXE_ORIG = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
ASSETS = ROOT / "cloudphone-v0.3.6 (1)" / "assets"
EXE_RECON = ROOT / "scratch" / "reconstructed_license.exe"

DIFF_TMP_ORIG = ROOT / "scratch" / "license_diff_orig"
DIFF_TMP_RECON = ROOT / "scratch" / "license_diff_recon"
DIFF_TMP_ORIG_NA = ROOT / "scratch" / "license_diff_orig_na"
DIFF_TMP_RECON_NA = ROOT / "scratch" / "license_diff_recon_na"
DIFF_TMP_ORIG_NODEBUG = ROOT / "scratch" / "license_diff_orig_nodebug"
DIFF_TMP_RECON_NODEBUG = ROOT / "scratch" / "license_diff_recon_nodebug"

OUTPUT_JSON = ROOT / "evidence" / "go_signaling" / "license" / "LICENSE_HTTP_DIFFERENTIAL_RESULTS.json"

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
PORT_ORIG_NODEBUG = get_free_port()
PORT_RECON_NODEBUG = get_free_port()

URL_ORIG = f"http://127.0.0.1:{PORT_ORIG}"
URL_RECON = f"http://127.0.0.1:{PORT_RECON}"
URL_ORIG_NA = f"http://127.0.0.1:{PORT_ORIG_NA}"
URL_RECON_NA = f"http://127.0.0.1:{PORT_RECON_NA}"
URL_ORIG_NODEBUG = f"http://127.0.0.1:{PORT_ORIG_NODEBUG}"
URL_RECON_NODEBUG = f"http://127.0.0.1:{PORT_RECON_NODEBUG}"

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

    for p in [DIFF_TMP_ORIG, DIFF_TMP_RECON, DIFF_TMP_ORIG_NA, DIFF_TMP_RECON_NA, DIFF_TMP_ORIG_NODEBUG, DIFF_TMP_RECON_NODEBUG]:
        make_fixture(p)

    servers = [
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG}", f"-data={DIFF_TMP_ORIG}", f"-assets={ASSETS}", "-debug"], DIFF_TMP_ORIG),
        ServerProcess([str(EXE_RECON), f"-port={PORT_RECON}", f"-data={DIFF_TMP_RECON}", "-debug"], DIFF_TMP_RECON),
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG_NA}", f"-data={DIFF_TMP_ORIG_NA}", f"-assets={ASSETS}", "-no-auth", "-debug"], DIFF_TMP_ORIG_NA),
        ServerProcess([str(EXE_RECON), f"-port={PORT_RECON_NA}", f"-data={DIFF_TMP_RECON_NA}", "-no-auth", "-debug"], DIFF_TMP_RECON_NA),
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG_NODEBUG}", f"-data={DIFF_TMP_ORIG_NODEBUG}", f"-assets={ASSETS}"], DIFF_TMP_ORIG_NODEBUG),
        ServerProcess([str(EXE_RECON), f"-port={PORT_RECON_NODEBUG}", f"-data={DIFF_TMP_RECON_NODEBUG}"], DIFF_TMP_RECON_NODEBUG)
    ]

    results = []
    test_run_success = True

    try:
        print("[*] Launching oracle and reconstructed server instances...")
        for s in servers:
            s.start()
        time.sleep(3.0)

        # Helper to login
        def login(url, user, pwd):
            r = requests.post(f"{url}/api/login", json={"username": user, "password": pwd})
            return r.json().get("token")

        tok_o_adm = login(URL_ORIG, "admin", "admin123")
        tok_r_adm = login(URL_RECON, "admin", "admin123")
        tok_o_usr = login(URL_ORIG, "user_test", "user123")
        tok_r_usr = login(URL_RECON, "user_test", "user123")

        h_o_adm = {"Authorization": f"Bearer {tok_o_adm}"}
        h_r_adm = {"Authorization": f"Bearer {tok_r_adm}"}
        h_o_usr = {"Authorization": f"Bearer {tok_o_usr}"}
        h_r_usr = {"Authorization": f"Bearer {tok_r_usr}"}

        print("\n=== Running Phase 2C.3HR License & Entitlement Differential Test Cases ===")

        def run_test(case_id, desc, orig_fn, recon_fn, validator=None):
            nonlocal test_run_success
            try:
                ro = orig_fn()
                rr = recon_fn()

                status_match = (ro.status_code == rr.status_code)
                ctype_match = (ro.headers.get("Content-Type") == rr.headers.get("Content-Type"))
                
                custom_pass = True
                diag = ""
                if validator:
                    custom_pass, diag = validator(ro, rr)

                passed = status_match and ctype_match and custom_pass
                if not passed:
                    test_run_success = False
                    print(f"  [FAIL] {case_id}: {desc}")
                    print(f"         Status: orig={ro.status_code}, recon={rr.status_code}")
                    print(f"         CType:  orig={ro.headers.get('Content-Type')}, recon={rr.headers.get('Content-Type')}")
                    print(f"         Body Orig:  {ro.text[:100]}")
                    print(f"         Body Recon: {rr.text[:100]}")
                    if diag:
                        print(f"         Diag:   {diag}")
                else:
                    print(f"  [PASS] {case_id}: {desc}")

                results.append({
                    "case_id": case_id,
                    "description": desc,
                    "status": "PASS" if passed else "FAIL",
                    "orig_status": ro.status_code,
                    "recon_status": rr.status_code,
                    "orig_content_type": ro.headers.get("Content-Type"),
                    "recon_content_type": rr.headers.get("Content-Type"),
                    "details": "" if passed else diag
                })
            except Exception as e:
                test_run_success = False
                print(f"  [ERROR] {case_id}: {desc} -> {e}")
                results.append({
                    "case_id": case_id,
                    "description": desc,
                    "status": "ERROR",
                    "error": str(e)
                })

        # Base validator for 13-field license status
        def val_01(ro, rr):
            jo = ro.json()
            jr = rr.json()
            if set(jo.keys()) != set(jr.keys()):
                return False, f"Key set mismatch: orig={set(jo.keys())}, recon={set(jr.keys())}"
            if len(jo) != 13:
                return False, f"Expected 13 fields, got {len(jo)}"
            
            fields_to_match = ["activated", "current_devices", "customer", "error_msg",
                               "expires_at", "license_expired", "license_source",
                               "max_devices", "post_promo_max_devices", "promo", "status"]
            for f in fields_to_match:
                if jo[f] != jr[f]:
                    return False, f"Field '{f}' mismatch: orig={jo[f]}, recon={jr[f]}"
            
            # Exact Machine ID comparison
            if jo["machine_id"] != jr["machine_id"]:
                return False, f"Machine ID mismatch: orig={jo['machine_id']}, recon={jr['machine_id']}"

            # Days remaining comparison
            if abs(jo["days_remaining"] - jr["days_remaining"]) > 1:
                return False, f"Days remaining divergence: orig={jo['days_remaining']}, recon={jr['days_remaining']}"

            return True, ""

        # =========================================================================
        # 1. HISTORICAL TEST CASES (LICENSE-HTTP-01 to LICENSE-HTTP-19)
        # =========================================================================

        # Case 01: License Status Baseline Parity (13 fields, built-in promo values)
        run_test(
            "LICENSE-HTTP-01",
            "/api/license_status baseline unactivated entitlement parity (13 keys, built-in promo)",
            lambda: requests.get(f"{URL_ORIG}/api/license_status", headers=h_o_adm),
            lambda: requests.get(f"{URL_RECON}/api/license_status", headers=h_r_adm),
            val_01
        )

        # Case 02: /debug/license Baseline Parity when -debug is enabled
        run_test(
            "LICENSE-HTTP-02",
            "/debug/license status baseline parity when -debug is enabled (200 OK)",
            lambda: requests.get(f"{URL_ORIG}/debug/license"),
            lambda: requests.get(f"{URL_RECON}/debug/license"),
            val_01
        )

        # Case 03: /debug/license Parity when -debug is disabled (404 Not found)
        def val_03(ro, rr):
            return (ro.text == rr.text and ro.text == "Not found\n"), f"Body mismatch: orig={repr(ro.text)}, recon={repr(rr.text)}"

        run_test(
            "LICENSE-HTTP-03",
            "/debug/license returns 404 Not found when -debug flag is omitted",
            lambda: requests.get(f"{URL_ORIG_NODEBUG}/debug/license"),
            lambda: requests.get(f"{URL_RECON_NODEBUG}/debug/license"),
            val_03
        )

        # Case 04: Missing Token on /api/license_status (Public 200 OK)
        run_test(
            "LICENSE-HTTP-04",
            "/api/license_status public access without auth token (200 OK)",
            lambda: requests.get(f"{URL_ORIG}/api/license_status"),
            lambda: requests.get(f"{URL_RECON}/api/license_status"),
            val_01
        )

        # Case 05: Invalid Token on /api/license_status (Public 200 OK)
        run_test(
            "LICENSE-HTTP-05",
            "/api/license_status public access with invalid Bearer token (200 OK)",
            lambda: requests.get(f"{URL_ORIG}/api/license_status", headers={"Authorization": "Bearer badtoken"}),
            lambda: requests.get(f"{URL_RECON}/api/license_status", headers={"Authorization": "Bearer badtoken"}),
            val_01
        )

        # Case 06: Normal User Access on /api/license_status (200 OK)
        run_test(
            "LICENSE-HTTP-06",
            "/api/license_status normal user access parity (200 OK)",
            lambda: requests.get(f"{URL_ORIG}/api/license_status", headers=h_o_usr),
            lambda: requests.get(f"{URL_RECON}/api/license_status", headers=h_r_usr),
            val_01
        )

        # Case 07: No-Auth Mode Access on /api/license_status (200 OK)
        run_test(
            "LICENSE-HTTP-07",
            "/api/license_status -no-auth mode access parity (200 OK)",
            lambda: requests.get(f"{URL_ORIG_NA}/api/license_status"),
            lambda: requests.get(f"{URL_RECON_NA}/api/license_status"),
            val_01
        )

        # Case 08: OPTIONS Preflight Parity on /api/license_status
        def val_08(ro, rr):
            m_orig = ro.headers.get("Access-Control-Allow-Methods", "")
            m_recon = rr.headers.get("Access-Control-Allow-Methods", "")
            h_orig = ro.headers.get("Access-Control-Allow-Headers", "")
            h_recon = rr.headers.get("Access-Control-Allow-Headers", "")
            o_orig = ro.headers.get("Access-Control-Allow-Origin", "")
            o_recon = rr.headers.get("Access-Control-Allow-Origin", "")
            match = (m_orig == m_recon == "GET, OPTIONS") and (h_orig == h_recon) and (o_orig == o_recon == "*")
            return match, f"CORS headers mismatch: orig=({m_orig}, {h_orig}), recon=({m_recon}, {h_recon})"

        run_test(
            "LICENSE-HTTP-08",
            "/api/license_status OPTIONS CORS preflight headers parity",
            lambda: requests.options(f"{URL_ORIG}/api/license_status"),
            lambda: requests.options(f"{URL_RECON}/api/license_status"),
            val_08
        )

        # Case 09: HEAD Request Semantics on /api/license_status
        def val_09(ro, rr):
            clen_match = (ro.headers.get("Content-Length") == rr.headers.get("Content-Length"))
            body_match = (len(ro.content) == len(rr.content) == 0)
            return (clen_match and body_match), f"HEAD mismatch: clen=({ro.headers.get('Content-Length')},{rr.headers.get('Content-Length')}), body=({len(ro.content)},{len(rr.content)})"

        run_test(
            "LICENSE-HTTP-09",
            "/api/license_status HEAD request parity (200 OK, empty wire body, Content-Length preserved)",
            lambda: requests.head(f"{URL_ORIG}/api/license_status"),
            lambda: requests.head(f"{URL_RECON}/api/license_status"),
            val_09
        )

        # Case 10: Permissive Verbs on /api/license_status (POST, PUT, PATCH, DELETE)
        for m in ["POST", "PUT", "PATCH", "DELETE"]:
            run_test(
                f"LICENSE-HTTP-10-{m}",
                f"/api/license_status permissive verb {m} parity (200 OK)",
                lambda m=m: requests.request(m, f"{URL_ORIG}/api/license_status"),
                lambda m=m: requests.request(m, f"{URL_RECON}/api/license_status"),
                val_01
            )

        # Case 11: Method Rejection on /api/activate (GET, PUT, PATCH, DELETE, HEAD)
        def make_val_11(method):
            def val_11(ro, rr):
                m_orig = ro.headers.get("Access-Control-Allow-Methods", "")
                m_recon = rr.headers.get("Access-Control-Allow-Methods", "")
                if method == "HEAD":
                    body_match = (len(ro.content) == len(rr.content) == 0)
                else:
                    body_match = (ro.text == rr.text == "Method not allowed\n")
                return (m_orig == m_recon == "POST, OPTIONS") and body_match, f"405 mismatch: orig={repr(ro.text)}, recon={repr(rr.text)}"
            return val_11

        for m in ["GET", "PUT", "PATCH", "DELETE", "HEAD"]:
            run_test(
                f"LICENSE-HTTP-11-{m}",
                f"/api/activate method {m} rejection parity (405 Method not allowed)",
                lambda m=m: requests.request(m, f"{URL_ORIG}/api/activate"),
                lambda m=m: requests.request(m, f"{URL_RECON}/api/activate"),
                make_val_11(m)
            )

        # Case 12: OPTIONS Preflight Parity on /api/activate
        def val_12(ro, rr):
            m_orig = ro.headers.get("Access-Control-Allow-Methods", "")
            m_recon = rr.headers.get("Access-Control-Allow-Methods", "")
            return (m_orig == m_recon == "POST, OPTIONS"), f"CORS methods mismatch: orig={m_orig}, recon={m_recon}"

        run_test(
            "LICENSE-HTTP-12",
            "/api/activate OPTIONS CORS preflight headers parity",
            lambda: requests.options(f"{URL_ORIG}/api/activate"),
            lambda: requests.options(f"{URL_RECON}/api/activate"),
            val_12
        )

        # Case 13: Empty Activation Body Rejection (400 Invalid JSON payload)
        def val_13(ro, rr):
            return (ro.text == rr.text == "Invalid JSON payload\n"), f"Body mismatch: orig={repr(ro.text)}, recon={repr(rr.text)}"

        run_test(
            "LICENSE-HTTP-13",
            "/api/activate empty POST body rejection parity (400 Invalid JSON payload)",
            lambda: requests.post(f"{URL_ORIG}/api/activate", data=""),
            lambda: requests.post(f"{URL_RECON}/api/activate", data=""),
            val_13
        )

        # Case 14: Malformed JSON Rejection (400 Invalid JSON payload)
        run_test(
            "LICENSE-HTTP-14",
            "/api/activate malformed JSON body rejection parity (400 Invalid JSON payload)",
            lambda: requests.post(f"{URL_ORIG}/api/activate", data="{bad", headers={"Content-Type": "application/json"}),
            lambda: requests.post(f"{URL_RECON}/api/activate", data="{bad", headers={"Content-Type": "application/json"}),
            val_13
        )

        # Case 15: Empty JSON Object Rejection (400 {"error":"授权码格式错误"})
        def val_15(ro, rr):
            jo = ro.json()
            jr = rr.json()
            return (jo == jr == {"error": "授权码格式错误"}), f"Error JSON mismatch: orig={jo}, recon={jr}"

        run_test(
            "LICENSE-HTTP-15",
            "/api/activate empty JSON object rejection parity (400 授权码格式错误)",
            lambda: requests.post(f"{URL_ORIG}/api/activate", json={}),
            lambda: requests.post(f"{URL_RECON}/api/activate", json={}),
            val_15
        )

        # Case 16: Empty License Field Rejection (400 {"error":"授权码格式错误"})
        run_test(
            "LICENSE-HTTP-16",
            "/api/activate empty license string rejection parity (400 授权码格式错误)",
            lambda: requests.post(f"{URL_ORIG}/api/activate", json={"license": ""}),
            lambda: requests.post(f"{URL_RECON}/api/activate", json={"license": ""}),
            val_15
        )

        # Case 17: Invalid Synthetic License Key Rejection (400 {"error":"授权码格式错误"})
        run_test(
            "LICENSE-HTTP-17",
            "/api/activate invalid synthetic license key rejection parity (400 授权码格式错误)",
            lambda: requests.post(f"{URL_ORIG}/api/activate", json={"license": "INVALID-SYNTHETIC-KEY-12345"}),
            lambda: requests.post(f"{URL_RECON}/api/activate", json={"license": "INVALID-SYNTHETIC-KEY-12345"}),
            val_15
        )

        # Case 18: State Idempotency After Failed Activation
        def val_18(ro, rr):
            jo = ro.json()
            jr = rr.json()
            unact = (jo["activated"] is False and jr["activated"] is False)
            source_built = (jo["license_source"] == jr["license_source"] == "built-in")
            lic_txt_o = (DIFF_TMP_ORIG / "license.txt").exists()
            lic_txt_r = (DIFF_TMP_RECON / "license.txt").exists()
            no_file = (not lic_txt_o and not lic_txt_r)
            return (unact and source_built and no_file), f"State leaked: jo={jo}, jr={jr}, file_o={lic_txt_o}, file_r={lic_txt_r}"

        run_test(
            "LICENSE-HTTP-18",
            "/api/activate state idempotency after failed activation (no disk mutation, built-in mode retained)",
            lambda: requests.get(f"{URL_ORIG}/api/license_status"),
            lambda: requests.get(f"{URL_RECON}/api/license_status"),
            val_18
        )

        # Case 19: Public Unauthenticated Access to /api/activate
        run_test(
            "LICENSE-HTTP-19",
            "/api/activate validates payload without requiring auth token (does not return 401)",
            lambda: requests.post(f"{URL_ORIG}/api/activate", json={"license": "TEST"}),
            lambda: requests.post(f"{URL_RECON}/api/activate", json={"license": "TEST"}),
            val_15
        )

        # =========================================================================
        # 2. PHASE 2C.3HR NEW CONTRACT CASES (EXACT PARITY & EDGE SUITES)
        # =========================================================================

        # Case G: Machine ID Exact Character-for-Character Parity
        def val_mid(ro, rr):
            mid_o = ro.json().get("machine_id", "")
            mid_r = rr.json().get("machine_id", "")
            match = (mid_o == mid_r == "8AD9-A7EF-87FB-E780")
            return match, f"Machine ID mismatch: orig={mid_o}, recon={mid_r}, expected=8AD9-A7EF-87FB-E780"

        run_test(
            "LICENSE-HTTP-MACHINE-ID-EXACT",
            "/api/license_status exact character-for-character machine_id parity (8AD9-A7EF-87FB-E780)",
            lambda: requests.get(f"{URL_ORIG}/api/license_status"),
            lambda: requests.get(f"{URL_RECON}/api/license_status"),
            val_mid
        )

        # Case I.1: HEAD /api/license_status exact representation header parity
        def val_head_status(ro, rr):
            clen_o = ro.headers.get("Content-Length")
            clen_r = rr.headers.get("Content-Length")
            body_len_o = len(ro.content)
            body_len_r = len(rr.content)
            match = (clen_o == clen_r == "277") and (body_len_o == body_len_r == 0)
            return match, f"HEAD /api/license_status header mismatch: clen=({clen_o},{clen_r}), body_len=({body_len_o},{body_len_r})"

        run_test(
            "LICENSE-HTTP-HEAD-CLEN-STATUS",
            "/api/license_status HEAD retains Content-Length=277 with zero body bytes",
            lambda: requests.head(f"{URL_ORIG}/api/license_status"),
            lambda: requests.head(f"{URL_RECON}/api/license_status"),
            val_head_status
        )

        # Case I.2: HEAD /debug/license exact representation header parity
        def val_head_debug(ro, rr):
            clen_o = ro.headers.get("Content-Length")
            clen_r = rr.headers.get("Content-Length")
            body_len_o = len(ro.content)
            body_len_r = len(rr.content)
            match = (clen_o == clen_r == "277") and (body_len_o == body_len_r == 0)
            return match, f"HEAD /debug/license header mismatch: clen=({clen_o},{clen_r}), body_len=({body_len_o},{body_len_r})"

        run_test(
            "LICENSE-HTTP-HEAD-CLEN-DEBUG",
            "/debug/license HEAD retains Content-Length=277 with zero body bytes",
            lambda: requests.head(f"{URL_ORIG}/debug/license"),
            lambda: requests.head(f"{URL_RECON}/debug/license"),
            val_head_debug
        )

        # Case J.1: /debug/license Permissive Verbs with -debug enabled
        def val_debug_verb(ro, rr):
            status_match = (ro.status_code == rr.status_code == 200)
            cors_absent = (ro.headers.get("Access-Control-Allow-Origin") is None and rr.headers.get("Access-Control-Allow-Origin") is None)
            clen_match = (ro.headers.get("Content-Length") == rr.headers.get("Content-Length") == "277")
            data_match = (ro.json() == rr.json())
            return (status_match and cors_absent and clen_match and data_match), f"Debug verb mismatch: status=({ro.status_code},{rr.status_code}), cors=({ro.headers.get('Access-Control-Allow-Origin')},{rr.headers.get('Access-Control-Allow-Origin')})"

        for v in ["POST", "PUT", "PATCH", "DELETE", "OPTIONS"]:
            run_test(
                f"LICENSE-HTTP-DEBUG-VERB-{v}",
                f"/debug/license permissive verb {v} parity with -debug (200 OK, no CORS, Content-Length: 277)",
                lambda v=v: requests.request(v, f"{URL_ORIG}/debug/license"),
                lambda v=v: requests.request(v, f"{URL_RECON}/debug/license"),
                val_debug_verb
            )

        # Case J.2: /debug/license 7 Verbs when -debug is disabled (all 404 Not found)
        def val_debug_nodebug(ro, rr):
            status_match = (ro.status_code == rr.status_code == 404)
            ctype_match = (ro.headers.get("Content-Type") == rr.headers.get("Content-Type") == "text/plain; charset=utf-8")
            body_match = (ro.text == rr.text)
            return (status_match and ctype_match and body_match), f"404 mismatch: orig=({ro.status_code},{repr(ro.text)}), recon=({rr.status_code},{repr(rr.text)})"

        for v in ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]:
            run_test(
                f"LICENSE-HTTP-DEBUG-NODEBUG-{v}",
                f"/debug/license verb {v} rejection without -debug flag (404 Not found)",
                lambda v=v: requests.request(v, f"{URL_ORIG_NODEBUG}/debug/license"),
                lambda v=v: requests.request(v, f"{URL_RECON_NODEBUG}/debug/license"),
                val_debug_nodebug
            )

        # Case K: Activation JSON Edge Cases (10 cases)
        edge_cases = [
            ("EDGE-NULL", "null", 400, "application/json", {"error": "授权码格式错误"}),
            ("EDGE-ARRAY", "[]", 400, "text/plain; charset=utf-8", "Invalid JSON payload\n"),
            ("EDGE-STRING", '"string"', 400, "text/plain; charset=utf-8", "Invalid JSON payload\n"),
            ("EDGE-LIC-NULL", '{"license":null}', 400, "application/json", {"error": "授权码格式错误"}),
            ("EDGE-LIC-INT", '{"license":123}', 400, "text/plain; charset=utf-8", "Invalid JSON payload\n"),
            ("EDGE-LIC-BOOL", '{"license":false}', 400, "text/plain; charset=utf-8", "Invalid JSON payload\n"),
            ("EDGE-LIC-ARRAY", '{"license":[]}', 400, "text/plain; charset=utf-8", "Invalid JSON payload\n"),
            ("EDGE-LIC-OBJ", '{"license":{}}', 400, "text/plain; charset=utf-8", "Invalid JSON payload\n"),
            ("EDGE-EMPTY-EXTRA", '{"license":"","extra":1}', 400, "application/json", {"error": "授权码格式错误"}),
            ("EDGE-INVALID-EXTRA", '{"license":"INVALID","extra":1}', 400, "application/json", {"error": "授权码格式错误"})
        ]

        def make_val_edge(expected_body):
            def val_edge(ro, rr):
                if isinstance(expected_body, dict):
                    return (ro.json() == rr.json() == expected_body), f"Edge JSON mismatch: orig={ro.json()}, recon={rr.json()}"
                else:
                    return (ro.text == rr.text == expected_body), f"Edge text mismatch: orig={repr(ro.text)}, recon={repr(rr.text)}"
            return val_edge

        for eid, payload, exp_code, exp_ctype, exp_body in edge_cases:
            run_test(
                f"LICENSE-HTTP-ACT-{eid}",
                f"/api/activate JSON edge case {eid} payload: {payload}",
                lambda payload=payload: requests.post(f"{URL_ORIG}/api/activate", data=payload, headers={"Content-Type": "application/json"}),
                lambda payload=payload: requests.post(f"{URL_RECON}/api/activate", data=payload, headers={"Content-Type": "application/json"}),
                make_val_edge(exp_body)
            )

        # Case B: Cryptographic Rejection Error Strings Parity (4 cases)
        crypto_rejections = [
            ("CRYPTO-NO-DOT", "INVALIDNODOTKEY", "授权码格式错误"),
            ("CRYPTO-BAD-BASE64", "!!!notbase64.123456", "非法的 Base64 编码"),
            ("CRYPTO-BAD-HEX", base64.b64encode(b'{}').decode() + ".not_hex_chars", "数字签名格式无效"),
            (
                "CRYPTO-BAD-SIG",
                base64.b64encode(b'{"machine_id":"8AD9-A7EF-87FB-E780"}').decode() + "." + "00"*64,
                "授权数字签名校验失败，可能已被篡改"
            )
        ]

        def make_val_crypto(expected_err):
            def val_crypto(ro, rr):
                jo = ro.json()
                jr = rr.json()
                return (jo == jr == {"error": expected_err}), f"Crypto error mismatch: orig={jo}, recon={jr}, want={expected_err}"
            return val_crypto

        for cid, key, exp_err in crypto_rejections:
            run_test(
                f"LICENSE-HTTP-{cid}",
                f"/api/activate cryptographic pipeline error parity: {exp_err}",
                lambda key=key: requests.post(f"{URL_ORIG}/api/activate", json={"license": key}),
                lambda key=key: requests.post(f"{URL_RECON}/api/activate", json={"license": key}),
                make_val_crypto(exp_err)
            )

        # Case F: Startup File Matrix Differential Verification (6 cases)
        startup_cases = [
            ("STARTUP-01-NO-FILE", None),
            ("STARTUP-02-EMPTY", ""),
            ("STARTUP-03-WHITESPACE", "   \n\t  \n"),
            ("STARTUP-04-INVALID-TEXT", "this-is-not-a-valid-license"),
            ("STARTUP-05-MALFORMED-B64", "notbase64.123456"),
            ("STARTUP-06-BAD-SIGNATURE", base64.b64encode(b'{"machine_id":"8AD9-A7EF-87FB-E780"}').decode() + "." + "00"*64)
        ]

        matrix_path = ROOT / "evidence" / "go_signaling" / "license" / "LICENSE_STARTUP_FILE_MATRIX.json"
        assert matrix_path.exists(), "LICENSE_STARTUP_FILE_MATRIX.json must exist"
        sm_data = json.loads(matrix_path.read_text(encoding="utf-8"))["cases"]

        def run_live_startup_recon(content):
            t_recon = ROOT / "scratch" / "test_startup_recon_tmp"
            if t_recon.exists():
                shutil.rmtree(t_recon, ignore_errors=True)
            t_recon.mkdir(parents=True, exist_ok=True)
            (t_recon / "users.json").write_text("{}", encoding="utf-8")
            (t_recon / "device_tags.json").write_text(json.dumps({"tags":[],"deviceTags":{}}), encoding="utf-8")
            if content is not None:
                (t_recon / "license.txt").write_text(content, encoding="utf-8")
            p = get_free_port()
            proc = subprocess.Popen([str(EXE_RECON), f"-port={p}", f"-data={t_recon}", "-debug"],
                                    cwd=str(t_recon), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1.0)
            try:
                res = requests.get(f"http://127.0.0.1:{p}/api/license_status")
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except:
                    proc.kill()
            return res

        class OracleMockResponse:
            def __init__(self, c):
                self.status_code = c["license_status_http_code"]
                self.headers = {"Content-Type": "application/json"}
                self._c = c
            def json(self):
                return {
                    "license_source": self._c["license_source"],
                    "status": self._c["status"],
                    "activated": self._c["activated"],
                    "error_msg": self._c["error_msg"]
                }

        for idx, (sid, lic_content) in enumerate(startup_cases):
            expected_case = sm_data[idx]
            def val_startup(ro, rr):
                jo = ro.json()
                jr = rr.json()
                match = (
                    rr.status_code == 200 and
                    jr.get("license_source") == jo.get("license_source") == "built-in" and
                    jr.get("status") == jo.get("status") == "valid" and
                    jr.get("activated") == jo.get("activated") is False and
                    jr.get("error_msg") == jo.get("error_msg") == ""
                )
                return match, f"Startup mismatch: recon={jr}, orig={jo}"

            run_test(
                f"LICENSE-HTTP-{sid}",
                f"Startup license.txt handling: {expected_case['name']} falls back to built-in promo",
                lambda c=expected_case: OracleMockResponse(c),
                lambda content=lic_content: run_live_startup_recon(content),
                val_startup
            )

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
        "excluded_unknowns": ["UNOBSERVED_LOCAL_VALID_SIGNATURE_SUCCESS"],
        "results": results
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[+] Differential results written to: {OUTPUT_JSON}")
    print(f"[+] Verdict: {pass_count}/{total_count} cases PASSED.")

    if not test_run_success or pass_count != total_count:
        sys.exit(1)

if __name__ == "__main__":
    main()
