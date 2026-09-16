#!/usr/bin/env python3
"""
test_license_http_diff.py - Phase 2C.3H License & Entitlement REST Differential Verification Suite

Executes side-by-side differential tests comparing the canonical original binary oracle
against the cleanroom reconstructed HTTP signaling server across all license routes:
  - /api/activate
  - /api/license_status
  - /debug/license

Strict Invariants:
  - Dynamic denominator: cases calculated from results at runtime.
  - UNKNOWN_REMOTE_SUCCESS excluded from test pass denominator.
  - Zero bypass / zero keygen: validates genuine original rejection behavior.
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

        print("\n=== Running Phase 2C.3H License & Entitlement Differential Test Cases ===")

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

        # Case 01: License Status Baseline Parity (13 fields, built-in promo values)
        def val_01(ro, rr):
            jo = ro.json()
            jr = rr.json()
            # Assert exact key set parity
            if set(jo.keys()) != set(jr.keys()):
                return False, f"Key set mismatch: orig={set(jo.keys())}, recon={set(jr.keys())}"
            if len(jo) != 13:
                return False, f"Expected 13 fields, got {len(jo)}"
            
            # Compare stable invariant fields
            fields_to_match = ["activated", "current_devices", "customer", "error_msg",
                               "expires_at", "license_expired", "license_source",
                               "max_devices", "post_promo_max_devices", "promo", "status"]
            for f in fields_to_match:
                if jo[f] != jr[f]:
                    return False, f"Field '{f}' mismatch: orig={jo[f]}, recon={jr[f]}"
            
            # Both should have valid machine_id format (XXXX-XXXX-XXXX-XXXX)
            if len(jr["machine_id"].split("-")) != 4:
                return False, f"Invalid reconstructed machine_id format: {jr['machine_id']}"

            # Days remaining should match (both calculated relative to expires_at)
            if abs(jo["days_remaining"] - jr["days_remaining"]) > 1:
                return False, f"Days remaining divergence: orig={jo['days_remaining']}, recon={jr['days_remaining']}"

            return True, ""

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
            return (len(ro.content) == len(rr.content) == 0), f"Body not empty: orig={len(ro.content)}, recon={len(rr.content)}"

        run_test(
            "LICENSE-HTTP-09",
            "/api/license_status HEAD request parity (200 OK, empty wire body)",
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
            # Assert state remained unactivated
            unact = (jo["activated"] is False and jr["activated"] is False)
            source_built = (jo["license_source"] == jr["license_source"] == "built-in")
            # Assert license.txt was not created on either disk
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
        "excluded_unknowns": ["UNKNOWN_REMOTE_SUCCESS"],
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
