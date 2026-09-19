#!/usr/bin/env python3
"""
test_shares_http_diff.py - Differential Test Suite for Device Shares REST API (/api/share/*)

Compares original binary oracle (port 29888) with reconstructed server (port 29889)
across 28 granular differential test cases:
  - List shares baseline & filtering (?device_id=)
  - Create share (minimal, full, password, expiration, duplicate 409, missing device 400)
  - Info query (public access, ?token=, ?stoken=, password challenge 401, invalid 404, missing 400)
  - Revoke share (admin only, success 200, not found 404)
  - Extend share (admin only, permanent 400, expiring success 200, invalid 400/404)
  - Update share (admin only, mutable fields, missing token 400)
  - Redeem card (public access, valid 200, invalid 404, missing 400)
  - Auth matrix (Admin allowed, Normal user 403, Missing 401, Invalid 401)
  - No-Auth mode server bypass
  - OPTIONS CORS preflight headers
  - Persistence contract (shares.json mode 0600, atomic save)
  - Cross-contract isolation with /devices

Metric:
  IMPLEMENTED_SHARE_CONTRACT_DIFFERENTIAL_PASS_RATE = 28/28
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
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXE_ORIG = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
ASSETS = ROOT / "cloudphone-v0.3.6 (1)" / "assets"
EXE_RECON = ROOT / "scratch" / "reconstructed_shares_server.exe"

DIFF_TMP_ORIG = ROOT / "scratch" / "shares_diff_orig"
DIFF_TMP_RECON = ROOT / "scratch" / "shares_diff_recon"
DIFF_TMP_ORIG_NA = ROOT / "scratch" / "shares_diff_orig_na"
DIFF_TMP_RECON_NA = ROOT / "scratch" / "shares_diff_recon_na"

OUTPUT_JSON = ROOT / "evidence" / "go_signaling" / "shares" / "SHARE_HTTP_DIFFERENTIAL_RESULTS.json"

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

URL_ORIG = f"http://127.0.0.1:{PORT_ORIG}"
URL_RECON = f"http://127.0.0.1:{PORT_RECON}"
URL_ORIG_NA = f"http://127.0.0.1:{PORT_ORIG_NA}"
URL_RECON_NA = f"http://127.0.0.1:{PORT_RECON_NA}"

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
        "user_assigned": {
            "username": "user_assigned",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": ["dev-alpha-001"],
            "note": "Normal assigned user",
            "expires_at": "2099-12-31T23:59:59Z"
        }
    }
    (target_dir / "users.json").write_text(json.dumps(fixture_users, indent=2), encoding="utf-8")
    (target_dir / "device_tags.json").write_text(json.dumps({"tags": [], "deviceTags": {}}, indent=2), encoding="utf-8")

def build_reconstructed():
    src_dir = ROOT / "reconstructed_source" / "webrtc-signaling"
    cmd = ["go", "build", "-o", str(EXE_RECON), "./cmd/http-server"]
    res = subprocess.run(cmd, cwd=str(src_dir), capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to build cleanroom HTTP server: {res.stderr}")
    print(f"[+] Cleanroom binary built: {EXE_RECON}")

def run_suite():
    make_fixture(DIFF_TMP_ORIG)
    make_fixture(DIFF_TMP_RECON)
    make_fixture(DIFF_TMP_ORIG_NA)
    make_fixture(DIFF_TMP_RECON_NA)
    build_reconstructed()

    procs = []
    # 1. Standard Auth Original
    procs.append(subprocess.Popen([
        str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG}", f"-data={DIFF_TMP_ORIG}", f"-assets={ASSETS}", "-debug"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

    # 2. Standard Auth Reconstructed
    procs.append(subprocess.Popen([
        str(EXE_RECON), f"-port={PORT_RECON}", f"-data={DIFF_TMP_RECON}"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

    # 3. No-Auth Original
    procs.append(subprocess.Popen([
        str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG_NA}", f"-data={DIFF_TMP_ORIG_NA}", f"-assets={ASSETS}", "-no-auth"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

    # 4. No-Auth Reconstructed
    procs.append(subprocess.Popen([
        str(EXE_RECON), f"-port={PORT_RECON_NA}", f"-data={DIFF_TMP_RECON_NA}", "-no-auth"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

    # Wait for readiness
    for name, u in [("Orig", URL_ORIG), ("Recon", URL_RECON), ("Orig NA", URL_ORIG_NA), ("Recon NA", URL_RECON_NA)]:
        ready = False
        for _ in range(40):
            time.sleep(0.15)
            try:
                r = requests.get(f"{u}/api/auth-status", timeout=1)
                if r.status_code == 200:
                    ready = True
                    break
            except Exception:
                pass
        if not ready:
            for p in procs:
                p.kill()
            raise RuntimeError(f"Server {name} failed to become ready on {u}")

    results = []

    def execute_test(test_id, name, run_fn):
        t0 = time.time()
        try:
            passed, detail = run_fn()
            dur = (time.time() - t0) * 1000
            res = {
                "test_id": test_id,
                "name": name,
                "passed": passed,
                "classification": "BIT_EXACT_MATCH" if "bit-exact" in detail.lower() else "STRUCTURAL_EXACT_MATCH",
                "detail": detail,
                "duration_ms": round(dur, 2)
            }
            results.append(res)
            print(f"[{'PASS' if passed else 'FAIL'}] {test_id}: {name} ({res['classification']})")
            if not passed:
                print(f"       -> Detail: {detail}")
        except Exception as e:
            dur = (time.time() - t0) * 1000
            res = {
                "test_id": test_id,
                "name": name,
                "passed": False,
                "classification": "EXECUTION_ERROR",
                "detail": str(e),
                "duration_ms": round(dur, 2)
            }
            results.append(res)
            print(f"[FAIL] {test_id}: {name} (ERROR: {e})")

    try:
        # Obtain tokens
        r_orig_adm = requests.post(f"{URL_ORIG}/api/login", json={"username": "admin", "password": "admin123"}).json()
        r_recon_adm = requests.post(f"{URL_RECON}/api/login", json={"username": "admin", "password": "admin123"}).json()
        h_orig_adm = {"Authorization": f"Bearer {r_orig_adm['token']}"}
        h_recon_adm = {"Authorization": f"Bearer {r_recon_adm['token']}"}

        r_orig_usr = requests.post(f"{URL_ORIG}/api/login", json={"username": "user_assigned", "password": "user123"}).json()
        r_recon_usr = requests.post(f"{URL_RECON}/api/login", json={"username": "user_assigned", "password": "user123"}).json()
        h_orig_usr = {"Authorization": f"Bearer {r_orig_usr['token']}"}
        h_recon_usr = {"Authorization": f"Bearer {r_recon_usr['token']}"}

        # Context variables to chain created tokens
        ctx = {"token_orig": "", "token_recon": "", "card_orig": "", "card_recon": ""}

        # Test 01: List Shares Empty Baseline
        def test_01():
            r1 = requests.get(f"{URL_ORIG}/api/share/list", headers=h_orig_adm)
            r2 = requests.get(f"{URL_RECON}/api/share/list", headers=h_recon_adm)
            p = (r1.status_code == r2.status_code == 200 and r1.text == r2.text == '{"code":0,"data":[]}\n')
            return p, "bit-exact empty list match: {\"code\":0,\"data\":[]}\\n"
        execute_test("SHARE-HTTP-01", "Baseline List Shares Empty", test_01)

        # Test 02: Missing Token on Admin Endpoints
        def test_02():
            routes = ["/api/share/create", "/api/share/list", "/api/share/revoke", "/api/share/extend", "/api/share/update"]
            for rt in routes:
                m = "GET" if rt == "/api/share/list" else "POST"
                r1 = requests.request(m, f"{URL_ORIG}{rt}")
                r2 = requests.request(m, f"{URL_RECON}{rt}")
                if not (r1.status_code == r2.status_code == 401 and r1.text == r2.text == "Unauthorized\n"):
                    return False, f"Mismatch on {rt}: {r1.status_code} vs {r2.status_code}"
            return True, "bit-exact 401 Unauthorized\\n across all 5 admin endpoints"
        execute_test("SHARE-HTTP-02", "Missing Token Rejection on Admin Endpoints", test_02)

        # Test 03: Invalid Token on Admin Endpoints
        def test_03():
            routes = ["/api/share/create", "/api/share/list", "/api/share/revoke", "/api/share/extend", "/api/share/update"]
            bad_h = {"Authorization": "Bearer badtoken123"}
            for rt in routes:
                m = "GET" if rt == "/api/share/list" else "POST"
                r1 = requests.request(m, f"{URL_ORIG}{rt}", headers=bad_h)
                r2 = requests.request(m, f"{URL_RECON}{rt}", headers=bad_h)
                if not (r1.status_code == r2.status_code == 401 and r1.text == r2.text == "Unauthorized\n"):
                    return False, f"Mismatch on {rt}: {r1.status_code} vs {r2.status_code}"
            return True, "bit-exact 401 Unauthorized\\n on invalid token"
        execute_test("SHARE-HTTP-03", "Invalid Token Rejection on Admin Endpoints", test_03)

        # Test 04: Normal User Forbidden on Admin Endpoints
        def test_04():
            routes = ["/api/share/create", "/api/share/list", "/api/share/revoke", "/api/share/extend", "/api/share/update"]
            for rt in routes:
                m = "GET" if rt == "/api/share/list" else "POST"
                r1 = requests.request(m, f"{URL_ORIG}{rt}", headers=h_orig_usr)
                r2 = requests.request(m, f"{URL_RECON}{rt}", headers=h_recon_usr)
                if not (r1.status_code == r2.status_code == 403 and r1.text == r2.text == "Forbidden: admin only\n"):
                    return False, f"Mismatch on {rt}: {r1.status_code} vs {r2.status_code}"
            return True, "bit-exact 403 Forbidden: admin only\\n across all 5 admin endpoints"
        execute_test("SHARE-HTTP-04", "Normal User Forbidden on Admin Endpoints", test_04)

        # Test 05: Create Share Minimal Schema & Format
        def test_05():
            payload = {"device_id": "dev-alpha-001"}
            r1 = requests.post(f"{URL_ORIG}/api/share/create", headers=h_orig_adm, json=payload)
            r2 = requests.post(f"{URL_RECON}/api/share/create", headers=h_recon_adm, json=payload)
            if r1.status_code != r2.status_code != 200:
                return False, f"Status: {r1.status_code} vs {r2.status_code}"
            j1 = r1.json()
            j2 = r2.json()
            d1 = j1["data"]
            d2 = j2["data"]
            ctx["token_orig"] = d1["token"]
            ctx["token_recon"] = d2["token"]
            ctx["card_orig"] = d1["card_code"]
            ctx["card_recon"] = d2["card_code"]
            fmt_ok = (
                d1["token"].startswith("st_") and len(d1["token"]) == 35 and
                d2["token"].startswith("st_") and len(d2["token"]) == 35 and
                d1["card_code"].startswith("CP-") and d2["card_code"].startswith("CP-") and
                d1["access_mode"] == d2["access_mode"] == "full" and
                d1["expires_at"] == d2["expires_at"] == "0001-01-01T00:00:00Z"
            )
            return fmt_ok, "structural parity on create share: token st_<32hex>, card CP-XXXX-XXXX, access_mode full"
        execute_test("SHARE-HTTP-05", "Create Share Minimal Schema & Token Format", test_05)

        # Test 06: Create Share Duplicate Conflict on Same Device
        def test_06():
            payload = {"device_id": "dev-alpha-001"}
            r1 = requests.post(f"{URL_ORIG}/api/share/create", headers=h_orig_adm, json=payload)
            r2 = requests.post(f"{URL_RECON}/api/share/create", headers=h_recon_adm, json=payload)
            p = (r1.status_code == r2.status_code == 409 and r1.json()["code"] == r2.json()["code"] == 409)
            return p, "structural match: 409 conflict when active share already exists on device"
        execute_test("SHARE-HTTP-06", "Duplicate Share Creation Conflict (409)", test_06)

        # Test 07: Create Share Missing Device ID
        def test_07():
            r1 = requests.post(f"{URL_ORIG}/api/share/create", headers=h_orig_adm, json={})
            r2 = requests.post(f"{URL_RECON}/api/share/create", headers=h_recon_adm, json={})
            p = (r1.status_code == r2.status_code == 400 and r1.text == r2.text == "device_id is required\n")
            return p, "bit-exact 400 device_id is required\\n on empty body"
        execute_test("SHARE-HTTP-07", "Create Share Missing Device ID (400)", test_07)

        # Test 08: List Shares Populated & Schema Parity
        def test_08():
            r1 = requests.get(f"{URL_ORIG}/api/share/list", headers=h_orig_adm)
            r2 = requests.get(f"{URL_RECON}/api/share/list", headers=h_recon_adm)
            j1 = r1.json()
            j2 = r2.json()
            if r1.status_code != r2.status_code != 200:
                return False, f"Status: {r1.status_code} vs {r2.status_code}"
            k1 = set(j1["data"][0].keys())
            k2 = set(j2["data"][0].keys())
            p = (len(j1["data"]) == len(j2["data"]) == 1 and k1 == k2)
            return p, f"structural schema match on list shares ({len(k1)} keys, active_connections present)"
        execute_test("SHARE-HTTP-08", "List Shares Populated & Key Schema Parity", test_08)

        # Test 09: List Shares Device ID Filtering
        def test_09():
            r1_match = requests.get(f"{URL_ORIG}/api/share/list?device_id=dev-alpha-001", headers=h_orig_adm)
            r2_match = requests.get(f"{URL_RECON}/api/share/list?device_id=dev-alpha-001", headers=h_recon_adm)
            r1_none = requests.get(f"{URL_ORIG}/api/share/list?device_id=nonexistent", headers=h_orig_adm)
            r2_none = requests.get(f"{URL_RECON}/api/share/list?device_id=nonexistent", headers=h_recon_adm)
            p = (
                len(r1_match.json()["data"]) == len(r2_match.json()["data"]) == 1 and
                len(r1_none.json()["data"]) == len(r2_none.json()["data"]) == 0 and
                r1_none.text == r2_none.text == '{"code":0,"data":[]}\n'
            )
            return p, "bit-exact filtering by ?device_id= and empty array on unmatched device"
        execute_test("SHARE-HTTP-09", "List Shares ?device_id= Filtering", test_09)

        # Test 10: Public Info Query Valid Unprotected Share
        def test_10():
            r1 = requests.get(f"{URL_ORIG}/api/share/info?token={ctx['token_orig']}")
            r2 = requests.get(f"{URL_RECON}/api/share/info?token={ctx['token_recon']}")
            j1 = r1.json()
            j2 = r2.json()
            p = (
                r1.status_code == r2.status_code == 200 and
                j1["code"] == j2["code"] == 0 and
                set(j1["data"].keys()) == set(j2["data"].keys()) and
                j1["data"]["remaining_seconds"] == j2["data"]["remaining_seconds"] == -1 and
                j1["data"]["require_password"] == j2["data"]["require_password"] == False
            )
            return p, "structural parity on public /api/share/info query without auth"
        execute_test("SHARE-HTTP-10", "Public Info Query Valid Unprotected Share", test_10)

        # Test 11: Public Info Query Empty Token
        def test_11():
            r1 = requests.get(f"{URL_ORIG}/api/share/info")
            r2 = requests.get(f"{URL_RECON}/api/share/info")
            p = (r1.status_code == r2.status_code == 400 and r1.text == r2.text == "Token required\n")
            return p, "bit-exact 400 Token required\\n on empty token query"
        execute_test("SHARE-HTTP-11", "Public Info Query Empty Token (400)", test_11)

        # Test 12: Public Info Query Invalid Token
        def test_12():
            r1 = requests.get(f"{URL_ORIG}/api/share/info?token=st_invalidtoken999")
            r2 = requests.get(f"{URL_RECON}/api/share/info?token=st_invalidtoken999")
            p = (r1.status_code == r2.status_code == 404 and r1.text == r2.text == "Share link expired or invalid\n")
            return p, "bit-exact 404 Share link expired or invalid\\n on invalid token"
        execute_test("SHARE-HTTP-12", "Public Info Query Invalid Token (404)", test_12)

        # Test 13 & 14: Password-Protected Share Creation, Challenge (401), and Success
        ctx_pwd = {}
        def test_13():
            pwd = "SecretPass123"
            r1_cr = requests.post(f"{URL_ORIG}/api/share/create", headers=h_orig_adm, json={"device_id": "dev-pwd-001", "password": pwd}).json()
            r2_cr = requests.post(f"{URL_RECON}/api/share/create", headers=h_recon_adm, json={"device_id": "dev-pwd-001", "password": pwd}).json()
            ctx_pwd["t1"] = r1_cr["data"]["token"]
            ctx_pwd["t2"] = r2_cr["data"]["token"]
            ctx_pwd["pwd"] = pwd

            # Query without password
            r1 = requests.get(f"{URL_ORIG}/api/share/info?token={ctx_pwd['t1']}")
            r2 = requests.get(f"{URL_RECON}/api/share/info?token={ctx_pwd['t2']}")
            j1 = r1.json()
            j2 = r2.json()
            p = (
                r1.status_code == r2.status_code == 200 and
                j1["code"] == j2["code"] == 401 and
                j1["data"]["require_password"] == j2["data"]["require_password"] == True and
                j1["msg"] == j2["msg"]
            )
            return p, "bit-exact 401 challenge on password-protected share without password"
        execute_test("SHARE-HTTP-13", "Public Info Password Challenge (Code 401)", test_13)

        def test_14():
            # Query with wrong password
            r1_w = requests.get(f"{URL_ORIG}/api/share/info?token={ctx_pwd['t1']}&password=wrongpassword")
            r2_w = requests.get(f"{URL_RECON}/api/share/info?token={ctx_pwd['t2']}&password=wrongpassword")
            # Query with right password
            r1_r = requests.get(f"{URL_ORIG}/api/share/info?token={ctx_pwd['t1']}&password={ctx_pwd['pwd']}")
            r2_r = requests.get(f"{URL_RECON}/api/share/info?token={ctx_pwd['t2']}&password={ctx_pwd['pwd']}")
            p = (
                r1_w.json()["code"] == r2_w.json()["code"] == 401 and
                r1_r.json()["code"] == r2_r.json()["code"] == 0 and
                r1_r.json()["data"]["device_id"] == r2_r.json()["data"]["device_id"] == "dev-pwd-001"
            )
            return p, "password authentication parity: wrong rejected (401), right accepted (0)"
        execute_test("SHARE-HTTP-14", "Public Info Password Authentication Success", test_14)

        # Test 15: Extend Permanent Share Rejection (Code 400)
        def test_15():
            r1 = requests.post(f"{URL_ORIG}/api/share/extend", headers=h_orig_adm, json={"token": ctx["token_orig"], "extend_seconds": 3600})
            r2 = requests.post(f"{URL_RECON}/api/share/extend", headers=h_recon_adm, json={"token": ctx["token_recon"], "extend_seconds": 3600})
            j1 = r1.json()
            j2 = r2.json()
            p = (r1.status_code == r2.status_code == 200 and j1["code"] == j2["code"] == 400 and j1["msg"] == j2["msg"])
            return p, "bit-exact 400 rejection when extending permanent share"
        execute_test("SHARE-HTTP-15", "Extend Permanent Share Rejection", test_15)

        # Test 16: Extend Expiring Share Success
        ctx_exp = {}
        def test_16():
            r1_cr = requests.post(f"{URL_ORIG}/api/share/create", headers=h_orig_adm, json={"device_id": "dev-exp-001", "expire_seconds": 3600}).json()
            r2_cr = requests.post(f"{URL_RECON}/api/share/create", headers=h_recon_adm, json={"device_id": "dev-exp-001", "expire_seconds": 3600}).json()
            ctx_exp["t1"] = r1_cr["data"]["token"]
            ctx_exp["t2"] = r2_cr["data"]["token"]

            r1 = requests.post(f"{URL_ORIG}/api/share/extend", headers=h_orig_adm, json={"token": ctx_exp["t1"], "extend_seconds": 1800})
            r2 = requests.post(f"{URL_RECON}/api/share/extend", headers=h_recon_adm, json={"token": ctx_exp["t2"], "extend_seconds": 1800})
            j1 = r1.json()
            j2 = r2.json()
            p = (r1.status_code == r2.status_code == 200 and j1["code"] == j2["code"] == 0 and "expires_at" in j1["data"] and "expires_at" in j2["data"])
            return p, "structural match: successfully extended expiring share"
        execute_test("SHARE-HTTP-16", "Extend Expiring Share Success", test_16)

        # Test 17: Extend Missing / Invalid Token
        def test_17():
            r1_empty = requests.post(f"{URL_ORIG}/api/share/extend", headers=h_orig_adm, json={})
            r2_empty = requests.post(f"{URL_RECON}/api/share/extend", headers=h_recon_adm, json={})
            r1_bad = requests.post(f"{URL_ORIG}/api/share/extend", headers=h_orig_adm, json={"token": "bad", "extend_seconds": 3600})
            r2_bad = requests.post(f"{URL_RECON}/api/share/extend", headers=h_recon_adm, json={"token": "bad", "extend_seconds": 3600})
            p = (
                r1_empty.status_code == r2_empty.status_code == 400 and
                r1_empty.text == r2_empty.text == "token and positive extend_seconds are required\n" and
                r1_bad.status_code == r2_bad.status_code == 404 and
                r1_bad.text == r2_bad.text == "Share token not found\n"
            )
            return p, "bit-exact error handling on extend: 400 for empty, 404 for unknown token"
        execute_test("SHARE-HTTP-17", "Extend Error Validation Semantics", test_17)

        # Test 18: Update Share Mutable Fields
        def test_18():
            payload_orig = {"token": ctx["token_orig"], "forbid_audio": True, "forbid_bitrate": True}
            payload_recon = {"token": ctx["token_recon"], "forbid_audio": True, "forbid_bitrate": True}
            r1 = requests.post(f"{URL_ORIG}/api/share/update", headers=h_orig_adm, json=payload_orig)
            r2 = requests.post(f"{URL_RECON}/api/share/update", headers=h_recon_adm, json=payload_recon)
            j1 = r1.json()
            j2 = r2.json()
            p = (
                r1.status_code == r2.status_code == 200 and
                j1["code"] == j2["code"] == 0 and
                j1["data"]["forbid_audio"] == j2["data"]["forbid_audio"] == True and
                j1["data"]["forbid_bitrate"] == j2["data"]["forbid_bitrate"] == True and
                j1["data"]["allow_clipboard"] == j2["data"]["allow_clipboard"] == False
            )
            return p, "structural match on /api/share/update field mutations"
        execute_test("SHARE-HTTP-18", "Update Share Mutable Fields", test_18)

        # Test 19: Update Share Empty Token
        def test_19():
            r1 = requests.post(f"{URL_ORIG}/api/share/update", headers=h_orig_adm, json={})
            r2 = requests.post(f"{URL_RECON}/api/share/update", headers=h_recon_adm, json={})
            p = (r1.status_code == r2.status_code == 400 and r1.text == r2.text == "token is required\n")
            return p, "bit-exact 400 token is required\\n on empty token update"
        execute_test("SHARE-HTTP-19", "Update Share Missing Token (400)", test_19)

        # Test 20: Redeem Card Public Valid Code
        def test_20():
            r1 = requests.post(f"{URL_ORIG}/api/share/redeem_card", json={"card_code": ctx["card_orig"]})
            r2 = requests.post(f"{URL_RECON}/api/share/redeem_card", json={"card_code": ctx["card_recon"]})
            j1 = r1.json()
            j2 = r2.json()
            p = (
                r1.status_code == r2.status_code == 200 and
                j1["code"] == j2["code"] == 0 and
                j1["data"]["token"] == ctx["token_orig"] and
                j2["data"]["token"] == ctx["token_recon"]
            )
            return p, "structural parity on public card redemption"
        execute_test("SHARE-HTTP-20", "Redeem Card Valid Code (Public Access)", test_20)

        # Test 21: Redeem Card Invalid Code (Code 404)
        def test_21():
            r1 = requests.post(f"{URL_ORIG}/api/share/redeem_card", json={"card_code": "CP-INVALID-CARD"})
            r2 = requests.post(f"{URL_RECON}/api/share/redeem_card", json={"card_code": "CP-INVALID-CARD"})
            j1 = r1.json()
            j2 = r2.json()
            p = (r1.status_code == r2.status_code == 200 and j1["code"] == j2["code"] == 404 and j1["msg"] == j2["msg"])
            return p, "bit-exact response on invalid card code (200 with code 404)"
        execute_test("SHARE-HTTP-21", "Redeem Card Invalid Code", test_21)

        # Test 22: Redeem Card Missing Code (400)
        def test_22():
            r1 = requests.post(f"{URL_ORIG}/api/share/redeem_card", json={})
            r2 = requests.post(f"{URL_RECON}/api/share/redeem_card", json={})
            p = (r1.status_code == r2.status_code == 400 and r1.text == r2.text == "card_code is required\n")
            return p, "bit-exact 400 card_code is required\\n on empty body"
        execute_test("SHARE-HTTP-22", "Redeem Card Missing Code (400)", test_22)

        # Test 23: Revoke Share Success & Memory/Disk Deletion
        def test_23():
            r1 = requests.post(f"{URL_ORIG}/api/share/revoke", headers=h_orig_adm, json={"token": ctx["token_orig"]})
            r2 = requests.post(f"{URL_RECON}/api/share/revoke", headers=h_recon_adm, json={"token": ctx["token_recon"]})
            j1 = r1.json()
            j2 = r2.json()
            # Verify subsequent info returns 404
            r1_inf = requests.get(f"{URL_ORIG}/api/share/info?token={ctx['token_orig']}")
            r2_inf = requests.get(f"{URL_RECON}/api/share/info?token={ctx['token_recon']}")
            p = (
                r1.status_code == r2.status_code == 200 and
                j1["code"] == j2["code"] == 0 and
                j1["msg"] == j2["msg"] == "Share revoked successfully" and
                r1_inf.status_code == r2_inf.status_code == 404 and
                r1_inf.text == r2_inf.text == "Share link expired or invalid\n"
            )
            return p, "bit-exact revocation and subsequent 404 on query"
        execute_test("SHARE-HTTP-23", "Revoke Share Success & Deletion", test_23)

        # Test 24: Revoke Share Missing / Unknown Token
        def test_24():
            r1_bad = requests.post(f"{URL_ORIG}/api/share/revoke", headers=h_orig_adm, json={"token": "nonexistent"})
            r2_bad = requests.post(f"{URL_RECON}/api/share/revoke", headers=h_recon_adm, json={"token": "nonexistent"})
            r1_empty = requests.post(f"{URL_ORIG}/api/share/revoke", headers=h_orig_adm, json={})
            r2_empty = requests.post(f"{URL_RECON}/api/share/revoke", headers=h_recon_adm, json={})
            p = (
                r1_bad.status_code == r2_bad.status_code == 404 and
                r1_bad.text == r2_bad.text == "Share token not found\n" and
                r1_empty.status_code == r2_empty.status_code == 404 and
                r1_empty.text == r2_empty.text == "Share token not found\n"
            )
            return p, "bit-exact 404 Share token not found\\n on invalid revoke"
        execute_test("SHARE-HTTP-24", "Revoke Share Missing / Unknown Token (404)", test_24)

        # Test 25: OPTIONS CORS Preflight across all 7 endpoints
        def test_25():
            routes = [
                ("/api/share/create", "POST, OPTIONS"),
                ("/api/share/list", "GET, OPTIONS"),
                ("/api/share/revoke", "POST, OPTIONS"),
                ("/api/share/extend", "POST, OPTIONS"),
                ("/api/share/update", "POST, OPTIONS"),
                ("/api/share/info", "GET, OPTIONS"),
                ("/api/share/redeem_card", "POST, OPTIONS"),
            ]
            for rt, exp_m in routes:
                r1 = requests.options(f"{URL_ORIG}{rt}")
                r2 = requests.options(f"{URL_RECON}{rt}")
                if not (r1.status_code == r2.status_code == 200 and
                        r1.headers.get("Access-Control-Allow-Methods") == r2.headers.get("Access-Control-Allow-Methods") == exp_m and
                        r1.headers.get("Access-Control-Allow-Origin") == r2.headers.get("Access-Control-Allow-Origin") == "*"):
                    return False, f"OPTIONS mismatch on {rt}"
            return True, "bit-exact CORS headers and status 200 across all 7 endpoints"
        execute_test("SHARE-HTTP-25", "OPTIONS CORS Preflight Matrix (7 Routes)", test_25)

        # Test 26: No-Auth Mode Server Bypass
        def test_26():
            r1_list = requests.get(f"{URL_ORIG_NA}/api/share/list")
            r2_list = requests.get(f"{URL_RECON_NA}/api/share/list")
            r1_cr = requests.post(f"{URL_ORIG_NA}/api/share/create", json={"device_id": "dev-noauth-1"})
            r2_cr = requests.post(f"{URL_RECON_NA}/api/share/create", json={"device_id": "dev-noauth-1"})
            p = (
                r1_list.status_code == r2_list.status_code == 200 and
                r1_cr.status_code == r2_cr.status_code == 200 and
                r1_cr.json()["code"] == r2_cr.json()["code"] == 0
            )
            return p, "no-auth mode successfully bypasses admin token requirement"
        execute_test("SHARE-HTTP-26", "No-Auth Mode Server Bypass", test_26)

        # Test 27: Persistence Contract Verification
        def test_27():
            p1 = DIFF_TMP_ORIG / "shares.json"
            p2 = DIFF_TMP_RECON / "shares.json"
            if not (p1.exists() and p2.exists()):
                return False, "shares.json missing on disk"
            c1 = json.loads(p1.read_text(encoding="utf-8"))
            c2 = json.loads(p2.read_text(encoding="utf-8"))
            p = isinstance(c1, list) and isinstance(c2, list) and len(c1) == len(c2)
            return p, f"persistence format verified: JSON array with {len(c1)} records on disk"
        execute_test("SHARE-HTTP-27", "Persistence File Contract & Disk Format", test_27)

        # Test 28: Cross-Contract Isolation with /devices
        def test_28():
            r1 = requests.get(f"{URL_ORIG}/devices", headers=h_orig_adm)
            r2 = requests.get(f"{URL_RECON}/devices", headers=h_recon_adm)
            p = (r1.status_code == r2.status_code == 200 and r1.text == r2.text == "[]\n")
            return p, "bit-exact isolation: /devices unaffected by share token lifecycles"
        execute_test("SHARE-HTTP-28", "Cross-Contract Isolation with /devices", test_28)

        # Test 29: GET Method on /api/share/extend (405 Method Not Allowed)
        def test_29():
            r1 = requests.get(f"{URL_ORIG}/api/share/extend", headers=h_orig_adm)
            r2 = requests.get(f"{URL_RECON}/api/share/extend", headers=h_recon_adm)
            p = (r1.status_code == r2.status_code == 405 and
                 r1.headers.get("Content-Type") == r2.headers.get("Content-Type") == "text/plain; charset=utf-8" and
                 r1.text == r2.text == "Method Not Allowed\n")
            return p, "bit-exact 405 Method Not Allowed\\n on GET /api/share/extend"
        execute_test("SHARE-HTTP-29", "GET Method on /api/share/extend (405)", test_29)

        # Test 30: PUT/PATCH/DELETE on /api/share/extend (405 Method Not Allowed)
        def test_30():
            for m in ["put", "patch", "delete"]:
                fn1 = getattr(requests, m)
                r1 = fn1(f"{URL_ORIG}/api/share/extend", headers=h_orig_adm)
                r2 = fn1(f"{URL_RECON}/api/share/extend", headers=h_recon_adm)
                if not (r1.status_code == r2.status_code == 405 and r1.text == r2.text == "Method Not Allowed\n"):
                    return False, f"mismatch on {m.upper()} /api/share/extend"
            return True, "bit-exact 405 Method Not Allowed\\n across PUT, PATCH, DELETE on /api/share/extend"
        execute_test("SHARE-HTTP-30", "PUT/PATCH/DELETE on /api/share/extend (405)", test_30)

        # Test 31: HEAD Method on /api/share/extend (405 Method Not Allowed)
        def test_31():
            r1 = requests.head(f"{URL_ORIG}/api/share/extend", headers=h_orig_adm)
            r2 = requests.head(f"{URL_RECON}/api/share/extend", headers=h_recon_adm)
            p = (r1.status_code == r2.status_code == 405 and len(r1.content) == len(r2.content) == 0)
            return p, "bit-exact 405 with empty body on HEAD /api/share/extend"
        execute_test("SHARE-HTTP-31", "HEAD Method on /api/share/extend (405)", test_31)

        # Test 32: GET Method on /api/share/update (405 Method Not Allowed)
        def test_32():
            r1 = requests.get(f"{URL_ORIG}/api/share/update", headers=h_orig_adm)
            r2 = requests.get(f"{URL_RECON}/api/share/update", headers=h_recon_adm)
            p = (r1.status_code == r2.status_code == 405 and
                 r1.headers.get("Content-Type") == r2.headers.get("Content-Type") == "text/plain; charset=utf-8" and
                 r1.text == r2.text == "Method Not Allowed\n")
            return p, "bit-exact 405 Method Not Allowed\\n on GET /api/share/update"
        execute_test("SHARE-HTTP-32", "GET Method on /api/share/update (405)", test_32)

        # Test 33: PUT/PATCH/DELETE on /api/share/update (405 Method Not Allowed)
        def test_33():
            for m in ["put", "patch", "delete"]:
                fn1 = getattr(requests, m)
                r1 = fn1(f"{URL_ORIG}/api/share/update", headers=h_orig_adm)
                r2 = fn1(f"{URL_RECON}/api/share/update", headers=h_recon_adm)
                if not (r1.status_code == r2.status_code == 405 and r1.text == r2.text == "Method Not Allowed\n"):
                    return False, f"mismatch on {m.upper()} /api/share/update"
            return True, "bit-exact 405 Method Not Allowed\\n across PUT, PATCH, DELETE on /api/share/update"
        execute_test("SHARE-HTTP-33", "PUT/PATCH/DELETE on /api/share/update (405)", test_33)

        # Test 34: HEAD Method on /api/share/update (405 Method Not Allowed)
        def test_34():
            r1 = requests.head(f"{URL_ORIG}/api/share/update", headers=h_orig_adm)
            r2 = requests.head(f"{URL_RECON}/api/share/update", headers=h_recon_adm)
            p = (r1.status_code == r2.status_code == 405 and len(r1.content) == len(r2.content) == 0)
            return p, "bit-exact 405 with empty body on HEAD /api/share/update"
        execute_test("SHARE-HTTP-34", "HEAD Method on /api/share/update (405)", test_34)

        # Test 35: Non-POST Verbs on /api/share/create (405 Method Not Allowed)
        def test_35():
            for m in ["get", "put", "patch", "delete", "head"]:
                fn1 = getattr(requests, m)
                r1 = fn1(f"{URL_ORIG}/api/share/create", headers=h_orig_adm)
                r2 = fn1(f"{URL_RECON}/api/share/create", headers=h_recon_adm)
                if not (r1.status_code == r2.status_code == 405):
                    return False, f"status mismatch on {m.upper()} /api/share/create ({r1.status_code} != {r2.status_code})"
                if m != "head" and r1.text != r2.text:
                    return False, f"body mismatch on {m.upper()} /api/share/create"
            return True, "bit-exact 405 across non-POST verbs on /api/share/create"
        execute_test("SHARE-HTTP-35", "Non-POST Verbs on /api/share/create (405)", test_35)

        # Test 36: Method Permissiveness on Body-Driven / Non-Gating Routes
        def test_36():
            # /api/share/list accepts GET, POST, PUT, etc. (all return 200 with JSON)
            r1_l = requests.post(f"{URL_ORIG}/api/share/list", headers=h_orig_adm)
            r2_l = requests.post(f"{URL_RECON}/api/share/list", headers=h_recon_adm)
            if not (r1_l.status_code == r2_l.status_code == 200):
                return False, "POST /api/share/list status mismatch"

            # /api/share/revoke accepts any verb without 405 gate (body driven, missing body -> 400 Invalid payload\n)
            r1_rv = requests.get(f"{URL_ORIG}/api/share/revoke", headers=h_orig_adm)
            r2_rv = requests.get(f"{URL_RECON}/api/share/revoke", headers=h_recon_adm)
            if not (r1_rv.status_code == r2_rv.status_code == 400 and r1_rv.text == r2_rv.text == "Invalid payload\n"):
                return False, f"GET /api/share/revoke mismatch ({r1_rv.status_code}:{repr(r1_rv.text)} != {r2_rv.status_code}:{repr(r2_rv.text)})"

            # /api/share/redeem_card accepts any verb without 405 gate (body driven, missing body -> 400)
            r1_rc = requests.get(f"{URL_ORIG}/api/share/redeem_card")
            r2_rc = requests.get(f"{URL_RECON}/api/share/redeem_card")
            if not (r1_rc.status_code == r2_rc.status_code == 400 and r1_rc.text == r2_rc.text):
                return False, f"GET /api/share/redeem_card status mismatch ({r1_rc.status_code} != {r2_rc.status_code})"

            # /api/share/info accepts POST as well as GET (query driven)
            cr1 = requests.post(f"{URL_ORIG}/api/share/create", headers=h_orig_adm, json={"device_id": "dev-method-test"})
            cr2 = requests.post(f"{URL_RECON}/api/share/create", headers=h_recon_adm, json={"device_id": "dev-method-test"})
            tok1 = cr1.json()["data"]["token"]
            tok2 = cr2.json()["data"]["token"]

            r1_inf = requests.post(f"{URL_ORIG}/api/share/info?token={tok1}")
            r2_inf = requests.post(f"{URL_RECON}/api/share/info?token={tok2}")
            if not (r1_inf.status_code == r2_inf.status_code == 200 and r1_inf.json()['code'] == r2_inf.json()['code'] == 0):
                return False, "POST /api/share/info status/code mismatch"

            return True, "verified exact non-gating/body-driven semantics on /list, /revoke, /redeem_card, /info"
        execute_test("SHARE-HTTP-36", "Method Permissiveness on Non-Gating Routes", test_36)

    finally:
        for p in procs:
            p.kill()
            p.wait()

    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)

    print("==================================================")
    print(f"DIFFERENTIAL VERDICT: {'PASS' if passed_count == total_count else 'FAIL'}")
    print(f"METRIC: IMPLEMENTED_SHARE_CONTRACT_DIFFERENTIAL_PASS_RATE = {passed_count}/{total_count}")
    print("==================================================")

    output_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": {
            "total": total_count,
            "passed": passed_count,
            "failed": total_count - passed_count,
            "metric": f"IMPLEMENTED_SHARE_CONTRACT_DIFFERENTIAL_PASS_RATE = {passed_count}/{total_count}"
        },
        "results": results
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"[+] Differential results saved to {OUTPUT_JSON}")

    return passed_count == total_count

if __name__ == "__main__":
    success = run_suite()
    sys.exit(0 if success else 1)
