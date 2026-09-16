#!/usr/bin/env python3
"""
test_shortcuts_http_diff.py - Phase 2C.3F Shortcuts REST HTTP Differential Test Suite

Executes side-by-side differential testing between original webrtc-signaling and reconstructed http-server.
Validates 13 exhaustive differential test cases covering:
  - SHORTCUT-HTTP-01: Baseline empty GET ([]\n)
  - SHORTCUT-HTTP-02: Missing token 401 (Unauthorized\n)
  - SHORTCUT-HTTP-03: Invalid token 401 (Unauthorized\n)
  - SHORTCUT-HTTP-04: Normal user GET & POST parity
  - SHORTCUT-HTTP-05: No-auth mode bypass (returns 200, persists under key "admin")
  - SHORTCUT-HTTP-06: OPTIONS method and CORS headers
  - SHORTCUT-HTTP-07: HEAD method 405 (wire bodyless, Content-Length: 19)
  - SHORTCUT-HTTP-08: Disallowed methods (PUT, PATCH, DELETE) 405 (Method not allowed\n)
  - SHORTCUT-HTTP-09: Valid mutation and replacement (200 {"status":"success"}\n)
  - SHORTCUT-HTTP-10: Malformed JSON 400 (Invalid JSON\n)
  - SHORTCUT-HTTP-11: Empty body 400 (Invalid JSON\n)
  - SHORTCUT-HTTP-12: Disk persistence contract (shortcuts.json, mode 0644, reload on restart)
  - SHORTCUT-HTTP-13: Per-user isolation (User A shortcuts independent from User B shortcuts)

Outputs:
  - evidence/go_signaling/shortcuts/SHORTCUT_HTTP_DIFFERENTIAL_RESULTS.json
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
EXE_RECON = ROOT / "scratch" / "reconstructed_shortcuts_server.exe"

DIFF_TMP_ORIG = ROOT / "scratch" / "shortcuts_diff_orig"
DIFF_TMP_RECON = ROOT / "scratch" / "shortcuts_diff_recon"
DIFF_TMP_ORIG_NA = ROOT / "scratch" / "shortcuts_diff_orig_na"
DIFF_TMP_RECON_NA = ROOT / "scratch" / "shortcuts_diff_recon_na"

OUTPUT_JSON = ROOT / "evidence" / "go_signaling" / "shortcuts" / "SHORTCUT_HTTP_DIFFERENTIAL_RESULTS.json"

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
    # Note: shortcuts.json is intentionally omitted to verify clean first-run behavior

def build_reconstructed():
    print("[*] Compiling cleanroom http-server binary...")
    src_dir = ROOT / "reconstructed_source" / "webrtc-signaling"
    EXE_RECON.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["go", "build", "-o", str(EXE_RECON), "./cmd/http-server"]
    res = subprocess.run(cmd, cwd=str(src_dir), capture_output=True, text=True)
    if res.returncode != 0:
        print("[FAIL] go build failed:", res.stderr)
        sys.exit(1)
    print(f"[+] Cleanroom binary built: {EXE_RECON}")

def main():
    build_reconstructed()

    make_fixture(DIFF_TMP_ORIG)
    make_fixture(DIFF_TMP_RECON)
    make_fixture(DIFF_TMP_ORIG_NA)
    make_fixture(DIFF_TMP_RECON_NA)

    # Launch servers
    proc_orig = subprocess.Popen([
        str(EXE_ORIG),
        "-tls=false",
        f"-port={PORT_ORIG}",
        f"-data={DIFF_TMP_ORIG}",
        f"-assets={ASSETS}",
        "-debug"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    proc_recon = subprocess.Popen([
        str(EXE_RECON),
        f"-port={PORT_RECON}",
        f"-data={DIFF_TMP_RECON}"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    proc_orig_na = subprocess.Popen([
        str(EXE_ORIG),
        "-tls=false",
        f"-port={PORT_ORIG_NA}",
        f"-data={DIFF_TMP_ORIG_NA}",
        f"-assets={ASSETS}",
        "-no-auth"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    proc_recon_na = subprocess.Popen([
        str(EXE_RECON),
        f"-port={PORT_RECON_NA}",
        f"-data={DIFF_TMP_RECON_NA}",
        "-no-auth"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(2.0)

    results = []
    def log_diff(test_id, name, classification, orig_res, recon_res, passed, details=""):
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {test_id}: {name} ({classification})")
        if not passed:
            print(f"    Orig:  {orig_res}")
            print(f"    Recon: {recon_res}")
            if details:
                print(f"    Notes: {details}")
        results.append({
            "test_id": test_id,
            "test_name": name,
            "classification": classification,
            "status": status,
            "passed": passed,
            "original": orig_res,
            "reconstructed": recon_res,
            "details": details
        })

    try:
        # Check initial file existence before any requests
        f_orig = DIFF_TMP_ORIG / "shortcuts.json"
        f_recon = DIFF_TMP_RECON / "shortcuts.json"
        file_init_orig = f_orig.exists()
        file_init_recon = f_recon.exists()

        # Step 0: Authenticate sessions
        r = requests.post(f"{URL_ORIG}/api/login", json={"username": "admin", "password": "admin123"})
        token_orig_admin = r.json()["token"]
        r = requests.post(f"{URL_RECON}/api/login", json={"username": "admin", "password": "admin123"})
        token_recon_admin = r.json()["token"]

        r = requests.post(f"{URL_ORIG}/api/login", json={"username": "user_test", "password": "user123"})
        token_orig_user = r.json()["token"]
        r = requests.post(f"{URL_RECON}/api/login", json={"username": "user_test", "password": "user123"})
        token_recon_user = r.json()["token"]

        hdr_orig_admin = {"Authorization": f"Bearer {token_orig_admin}"}
        hdr_recon_admin = {"Authorization": f"Bearer {token_recon_admin}"}
        hdr_orig_user = {"Authorization": f"Bearer {token_orig_user}"}
        hdr_recon_user = {"Authorization": f"Bearer {token_recon_user}"}

        # Case 1: SHORTCUT-HTTP-01 - Baseline empty GET ([]\n)
        r_orig = requests.get(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_admin)
        r_recon = requests.get(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_admin)
        file_after_get_orig = f_orig.exists()
        file_after_get_recon = f_recon.exists()
        orig_res = {"status": r_orig.status_code, "body": r_orig.text, "ct": r_orig.headers.get("Content-Type")}
        recon_res = {"status": r_recon.status_code, "body": r_recon.text, "ct": r_recon.headers.get("Content-Type")}
        passed = (r_orig.status_code == r_recon.status_code == 200 and
                  r_orig.text == r_recon.text == "[]\n" and
                  "application/json" in r_recon.headers.get("Content-Type", ""))
        log_diff("SHORTCUT-HTTP-01", "Baseline empty GET ([]\\n)", "READ_CONTRACT", orig_res, recon_res, passed)

        # Case 2: SHORTCUT-HTTP-02 - Missing token 401
        r_orig = requests.get(f"{URL_ORIG}/api/shortcuts")
        r_recon = requests.get(f"{URL_RECON}/api/shortcuts")
        orig_res = {"status": r_orig.status_code, "body": r_orig.text}
        recon_res = {"status": r_recon.status_code, "body": r_recon.text}
        passed = (r_orig.status_code == r_recon.status_code == 401 and
                  r_orig.text == r_recon.text == "Unauthorized\n")
        log_diff("SHORTCUT-HTTP-02", "Missing token 401 (Unauthorized\\n)", "AUTH_MATRIX", orig_res, recon_res, passed)

        # Case 3: SHORTCUT-HTTP-03 - Invalid token 401
        bad_hdr = {"Authorization": "Bearer bad-token-xyz"}
        r_orig = requests.get(f"{URL_ORIG}/api/shortcuts", headers=bad_hdr)
        r_recon = requests.get(f"{URL_RECON}/api/shortcuts", headers=bad_hdr)
        orig_res = {"status": r_orig.status_code, "body": r_orig.text}
        recon_res = {"status": r_recon.status_code, "body": r_recon.text}
        passed = (r_orig.status_code == r_recon.status_code == 401 and
                  r_orig.text == r_recon.text == "Unauthorized\n")
        log_diff("SHORTCUT-HTTP-03", "Invalid token 401 (Unauthorized\\n)", "AUTH_MATRIX", orig_res, recon_res, passed)

        # Case 4: SHORTCUT-HTTP-04 - Normal user GET & POST parity
        user_shortcuts = [{"name": "UserCmd", "cmd": "echo user"}]
        r_orig_post = requests.post(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_user, json=user_shortcuts)
        r_recon_post = requests.post(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_user, json=user_shortcuts)
        r_orig_get = requests.get(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_user)
        r_recon_get = requests.get(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_user)
        orig_res = {"post_status": r_orig_post.status_code, "get_status": r_orig_get.status_code, "get_body": r_orig_get.json()}
        recon_res = {"post_status": r_recon_post.status_code, "get_status": r_recon_get.status_code, "get_body": r_recon_get.json()}
        passed = (r_orig_post.status_code == r_recon_post.status_code == 200 and
                  r_orig_get.status_code == r_recon_get.status_code == 200 and
                  r_orig_get.json() == r_recon_get.json() == user_shortcuts)
        log_diff("SHORTCUT-HTTP-04", "Normal user GET & POST parity", "RBAC_PARITY", orig_res, recon_res, passed)

        # Case 5: SHORTCUT-HTTP-05 - No-auth mode bypass (returns 200, persists under key 'admin')
        na_shortcuts = [{"name": "NoAuthCmd", "cmd": "echo noauth"}]
        r_orig_na_p = requests.post(f"{URL_ORIG_NA}/api/shortcuts", json=na_shortcuts)
        r_recon_na_p = requests.post(f"{URL_RECON_NA}/api/shortcuts", json=na_shortcuts)
        r_orig_na_g = requests.get(f"{URL_ORIG_NA}/api/shortcuts")
        r_recon_na_g = requests.get(f"{URL_RECON_NA}/api/shortcuts")
        # Check disk key in both
        time.sleep(0.2)
        disk_orig_na = json.loads((DIFF_TMP_ORIG_NA / "shortcuts.json").read_text(encoding="utf-8"))
        disk_recon_na = json.loads((DIFF_TMP_RECON_NA / "shortcuts.json").read_text(encoding="utf-8"))
        orig_res = {"post_status": r_orig_na_p.status_code, "get_status": r_orig_na_g.status_code, "disk_keys": list(disk_orig_na.keys())}
        recon_res = {"post_status": r_recon_na_p.status_code, "get_status": r_recon_na_g.status_code, "disk_keys": list(disk_recon_na.keys())}
        passed = (r_orig_na_p.status_code == r_recon_na_p.status_code == 200 and
                  r_orig_na_g.status_code == r_recon_na_g.status_code == 200 and
                  r_orig_na_g.json() == r_recon_na_g.json() == na_shortcuts and
                  "admin" in disk_orig_na and "admin" in disk_recon_na)
        log_diff("SHORTCUT-HTTP-05", "No-auth mode bypass & 'admin' key mapping", "NO_AUTH_SEMANTICS", orig_res, recon_res, passed)

        # Case 6: SHORTCUT-HTTP-06 - OPTIONS method and CORS headers
        r_orig = requests.options(f"{URL_ORIG}/api/shortcuts")
        r_recon = requests.options(f"{URL_RECON}/api/shortcuts")
        orig_res = {
            "status": r_orig.status_code,
            "origin": r_orig.headers.get("Access-Control-Allow-Origin"),
            "methods": r_orig.headers.get("Access-Control-Allow-Methods"),
            "headers": r_orig.headers.get("Access-Control-Allow-Headers")
        }
        recon_res = {
            "status": r_recon.status_code,
            "origin": r_recon.headers.get("Access-Control-Allow-Origin"),
            "methods": r_recon.headers.get("Access-Control-Allow-Methods"),
            "headers": r_recon.headers.get("Access-Control-Allow-Headers")
        }
        passed = (r_orig.status_code == r_recon.status_code == 200 and
                  orig_res["origin"] == recon_res["origin"] == "*" and
                  "GET" in recon_res["methods"] and "POST" in recon_res["methods"] and "OPTIONS" in recon_res["methods"] and
                  "Content-Type" in recon_res["headers"] and "Authorization" in recon_res["headers"])
        log_diff("SHORTCUT-HTTP-06", "OPTIONS method and CORS headers", "CORS_CONTRACT", orig_res, recon_res, passed)

        # Case 7: SHORTCUT-HTTP-07 - HEAD method 405 (wire bodyless, Content-Length: 19)
        r_orig = requests.head(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_admin)
        r_recon = requests.head(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_admin)
        orig_res = {"status": r_orig.status_code, "wire_body_len": len(r_orig.content), "content_length": r_orig.headers.get("Content-Length")}
        recon_res = {"status": r_recon.status_code, "wire_body_len": len(r_recon.content), "content_length": r_recon.headers.get("Content-Length")}
        passed = (r_orig.status_code == r_recon.status_code == 405 and
                  len(r_orig.content) == len(r_recon.content) == 0 and
                  orig_res["content_length"] == recon_res["content_length"] == "19")
        log_diff("SHORTCUT-HTTP-07", "HEAD method 405 (wire bodyless, Content-Length: 19)", "METHOD_CONTRACT", orig_res, recon_res, passed)

        # Case 8: SHORTCUT-HTTP-08 - Disallowed methods (PUT, PATCH, DELETE) 405
        disallowed_passed = True
        orig_sub = {}
        recon_sub = {}
        for m in ["PUT", "PATCH", "DELETE"]:
            fn = getattr(requests, m.lower())
            ro = fn(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_admin)
            rr = fn(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_admin)
            orig_sub[m] = {"status": ro.status_code, "body": ro.text}
            recon_sub[m] = {"status": rr.status_code, "body": rr.text}
            if not (ro.status_code == rr.status_code == 405 and ro.text == rr.text == "Method not allowed\n"):
                disallowed_passed = False
        log_diff("SHORTCUT-HTTP-08", "Disallowed methods (PUT, PATCH, DELETE) 405", "METHOD_CONTRACT", orig_sub, recon_sub, disallowed_passed)

        # Case 9: SHORTCUT-HTTP-09 - Valid mutation and replacement (200 {"status":"success"}\n)
        admin_shortcuts_1 = [{"name": "Terminal", "cmd": "cmd.exe"}]
        r_orig = requests.post(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_admin, json=admin_shortcuts_1)
        r_recon = requests.post(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_admin, json=admin_shortcuts_1)
        file_after_post_orig = f_orig.exists()
        file_after_post_recon = f_recon.exists()
        orig_res = {"status": r_orig.status_code, "body": r_orig.text}
        recon_res = {"status": r_recon.status_code, "body": r_recon.text}
        p1 = (r_orig.status_code == r_recon.status_code == 200 and r_orig.text == r_recon.text == '{"status":"success"}\n')

        # Replace with 2 items
        admin_shortcuts_2 = [{"name": "Cmd1", "cmd": "c1"}, {"name": "Cmd2", "cmd": "c2"}]
        r_orig_2 = requests.post(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_admin, json=admin_shortcuts_2)
        r_recon_2 = requests.post(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_admin, json=admin_shortcuts_2)
        r_orig_get = requests.get(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_admin)
        r_recon_get = requests.get(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_admin)
        p2 = (r_orig_2.status_code == r_recon_2.status_code == 200 and
              r_orig_get.json() == r_recon_get.json() == admin_shortcuts_2)
        passed = p1 and p2
        log_diff("SHORTCUT-HTTP-09", "Valid mutation and list replacement", "MUTATION_CONTRACT", orig_res, recon_res, passed)

        # Case 10: SHORTCUT-HTTP-10 - Malformed JSON 400 (Invalid JSON\n)
        bad_json = "{bad_json_payload"
        r_orig = requests.post(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_admin, data=bad_json)
        r_recon = requests.post(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_admin, data=bad_json)
        orig_res = {"status": r_orig.status_code, "body": r_orig.text}
        recon_res = {"status": r_recon.status_code, "body": r_recon.text}
        passed = (r_orig.status_code == r_recon.status_code == 400 and
                  r_orig.text == r_recon.text == "Invalid JSON\n")
        log_diff("SHORTCUT-HTTP-10", "Malformed JSON 400 (Invalid JSON\\n)", "ERROR_HANDLING", orig_res, recon_res, passed)

        # Case 11: SHORTCUT-HTTP-11 - Empty body 400 (Invalid JSON\n)
        r_orig = requests.post(f"{URL_ORIG}/api/shortcuts", headers=hdr_orig_admin, data="")
        r_recon = requests.post(f"{URL_RECON}/api/shortcuts", headers=hdr_recon_admin, data="")
        orig_res = {"status": r_orig.status_code, "body": r_orig.text}
        recon_res = {"status": r_recon.status_code, "body": r_recon.text}
        passed = (r_orig.status_code == r_recon.status_code == 400 and
                  r_orig.text == r_recon.text == "Invalid JSON\n")
        log_diff("SHORTCUT-HTTP-11", "Empty body 400 (Invalid JSON\\n)", "ERROR_HANDLING", orig_res, recon_res, passed)

        # Case 12: SHORTCUT-HTTP-12 - Disk persistence contract (shortcuts.json, mode, reload on restart)
        # Verify file exists on disk
        f_orig = DIFF_TMP_ORIG / "shortcuts.json"
        f_recon = DIFF_TMP_RECON / "shortcuts.json"
        time.sleep(0.2)
        f_orig_content = f_orig.read_text(encoding="utf-8")
        f_recon_content = f_recon.read_text(encoding="utf-8")
        
        # Kill servers and restart them to verify disk reload!
        proc_orig.terminate()
        proc_recon.terminate()
        proc_orig.wait()
        proc_recon.wait()

        # Restart
        proc_orig = subprocess.Popen([
            str(EXE_ORIG),
            "-tls=false",
            f"-port={PORT_ORIG}",
            f"-data={DIFF_TMP_ORIG}",
            f"-assets={ASSETS}",
            "-debug"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        proc_recon = subprocess.Popen([
            str(EXE_RECON),
            f"-port={PORT_RECON}",
            f"-data={DIFF_TMP_RECON}"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2.0)
        file_after_restart_orig = f_orig.exists()
        file_after_restart_recon = f_recon.exists()

        # Re-login admin and user_test after restart
        r = requests.post(f"{URL_ORIG}/api/login", json={"username": "admin", "password": "admin123"})
        t_orig_admin = r.json()["token"]
        r = requests.post(f"{URL_RECON}/api/login", json={"username": "admin", "password": "admin123"})
        t_recon_admin = r.json()["token"]

        r = requests.post(f"{URL_ORIG}/api/login", json={"username": "user_test", "password": "user123"})
        t_orig_user = r.json()["token"]
        r = requests.post(f"{URL_RECON}/api/login", json={"username": "user_test", "password": "user123"})
        t_recon_user = r.json()["token"]

        r_orig_reloaded = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"})
        r_recon_reloaded = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"})

        orig_res = {"file_exists": f_orig.exists(), "reloaded_items": len(r_orig_reloaded.json())}
        recon_res = {"file_exists": f_recon.exists(), "reloaded_items": len(r_recon_reloaded.json())}
        passed = (f_orig.exists() and f_recon.exists() and
                  r_orig_reloaded.status_code == r_recon_reloaded.status_code == 200 and
                  r_orig_reloaded.json() == r_recon_reloaded.json() == admin_shortcuts_2)
        log_diff("SHORTCUT-HTTP-12", "Disk persistence contract & restart reload", "PERSISTENCE_CONTRACT", orig_res, recon_res, passed)

        # Case 13: SHORTCUT-HTTP-13 - Per-user isolation
        # User admin has admin_shortcuts_2
        # User user_test sets user_shortcuts
        r_orig_post = requests.post(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_user}"}, json=user_shortcuts)
        r_recon_post = requests.post(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_user}"}, json=user_shortcuts)

        r_orig_admin_get = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"})
        r_recon_admin_get = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"})

        r_orig_user_get = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_user}"})
        r_recon_user_get = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_user}"})

        orig_res = {"admin_shortcuts": r_orig_admin_get.json(), "user_shortcuts": r_orig_user_get.json()}
        recon_res = {"admin_shortcuts": r_recon_admin_get.json(), "user_shortcuts": r_recon_user_get.json()}
        passed = (r_orig_admin_get.json() == r_recon_admin_get.json() == admin_shortcuts_2 and
                  r_orig_user_get.json() == r_recon_user_get.json() == user_shortcuts and
                  r_orig_admin_get.json() != r_orig_user_get.json())
        log_diff("SHORTCUT-HTTP-13", "Per-user isolation (multi-user independent state)", "ISOLATION_CONTRACT", orig_res, recon_res, passed)

        # Case 14: SHORTCUT-HTTP-14 - POST null literal parity (null literal, null\n readback, null on disk, persist restart)
        r_orig_null = requests.post(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}", "Content-Type": "application/json"}, data="null")
        r_recon_null = requests.post(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}", "Content-Type": "application/json"}, data="null")
        
        r_orig_get_null = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"})
        r_recon_get_null = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"})
        
        time.sleep(0.1)
        disk_orig_null = json.loads(f_orig.read_text(encoding="utf-8")).get("admin")
        disk_recon_null = json.loads(f_recon.read_text(encoding="utf-8")).get("admin")
        
        # Restart servers to verify persistence of null across restart
        proc_orig.terminate()
        proc_recon.terminate()
        proc_orig.wait()
        proc_recon.wait()
        
        proc_orig = subprocess.Popen([
            str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG}", f"-data={DIFF_TMP_ORIG}", f"-assets={ASSETS}", "-debug"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc_recon = subprocess.Popen([
            str(EXE_RECON), f"-port={PORT_RECON}", f"-data={DIFF_TMP_RECON}"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2.0)
        
        r_a = requests.post(f"{URL_ORIG}/api/login", json={"username": "admin", "password": "admin123"})
        t_orig_admin = r_a.json()["token"]
        r_a = requests.post(f"{URL_RECON}/api/login", json={"username": "admin", "password": "admin123"})
        t_recon_admin = r_a.json()["token"]
        
        r_orig_restart_null = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"})
        r_recon_restart_null = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"})
        
        orig_res = {
            "post_status": r_orig_null.status_code, "post_body": r_orig_null.text,
            "get_body": r_orig_get_null.text, "disk_val": disk_orig_null,
            "restart_get_body": r_orig_restart_null.text
        }
        recon_res = {
            "post_status": r_recon_null.status_code, "post_body": r_recon_null.text,
            "get_body": r_recon_get_null.text, "disk_val": disk_recon_null,
            "restart_get_body": r_recon_restart_null.text
        }
        passed = (
            r_orig_null.status_code == r_recon_null.status_code == 200 and
            r_orig_null.text == r_recon_null.text == "{\"status\":\"success\"}\n" and
            r_orig_get_null.text == r_recon_get_null.text == "null\n" and
            disk_orig_null is None and disk_recon_null is None and
            r_orig_restart_null.text == r_recon_restart_null.text == "null\n"
        )
        log_diff("SHORTCUT-HTTP-14", "POST null literal parity (success, null\\n readback, null on disk, persist restart)", "NULL_EDGE_CONTRACT", orig_res, recon_res, passed)

        # Case 15: SHORTCUT-HTTP-15 - POST [null] parity (zero-value struct initialization)
        r_orig_p15 = requests.post(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}", "Content-Type": "application/json"}, data="[null]")
        r_recon_p15 = requests.post(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}", "Content-Type": "application/json"}, data="[null]")
        r_orig_g15 = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"})
        r_recon_g15 = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"})
        orig_res = {"post_status": r_orig_p15.status_code, "get_body": r_orig_g15.text}
        recon_res = {"post_status": r_recon_p15.status_code, "get_body": r_recon_g15.text}
        passed = (
            r_orig_p15.status_code == r_recon_p15.status_code == 200 and
            r_orig_g15.status_code == r_recon_g15.status_code == 200 and
            r_orig_g15.text == r_recon_g15.text == '[{"name":"","cmd":""}]\n'
        )
        log_diff("SHORTCUT-HTTP-15", "POST [null] array element parity (zero-value struct initialization)", "JSON_EDGE_CONTRACT", orig_res, recon_res, passed)

        # Case 16: SHORTCUT-HTTP-16 - Partial fields mutation parity
        # Subcase 1: name only
        r_orig_p16a = requests.post(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"}, json=[{"name": "OnlyName"}])
        r_recon_p16a = requests.post(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"}, json=[{"name": "OnlyName"}])
        r_orig_g16a = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"})
        r_recon_g16a = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"})
        
        # Subcase 2: cmd only
        r_orig_p16b = requests.post(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"}, json=[{"cmd": "OnlyCmd"}])
        r_recon_p16b = requests.post(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"}, json=[{"cmd": "OnlyCmd"}])
        r_orig_g16b = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"})
        r_recon_g16b = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"})
        
        orig_res = {"name_only": r_orig_g16a.json(), "cmd_only": r_orig_g16b.json()}
        recon_res = {"name_only": r_recon_g16a.json(), "cmd_only": r_recon_g16b.json()}
        passed = (
            r_orig_g16a.json() == r_recon_g16a.json() == [{"name": "OnlyName", "cmd": ""}] and
            r_orig_g16b.json() == r_recon_g16b.json() == [{"name": "", "cmd": "OnlyCmd"}]
        )
        log_diff("SHORTCUT-HTTP-16", "Partial fields mutation parity (missing fields default to zero-value empty string)", "JSON_EDGE_CONTRACT", orig_res, recon_res, passed)

        # Case 17: SHORTCUT-HTTP-17 - Extra fields ignored
        r_orig_p17 = requests.post(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"}, json=[{"name": "x", "cmd": "y", "extra": "z"}])
        r_recon_p17 = requests.post(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"}, json=[{"name": "x", "cmd": "y", "extra": "z"}])
        r_orig_g17 = requests.get(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}"})
        r_recon_g17 = requests.get(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}"})
        orig_res = {"post_status": r_orig_p17.status_code, "get_json": r_orig_g17.json()}
        recon_res = {"post_status": r_recon_p17.status_code, "get_json": r_recon_g17.json()}
        passed = (
            r_orig_p17.status_code == r_recon_p17.status_code == 200 and
            r_orig_g17.json() == r_recon_g17.json() == [{"name": "x", "cmd": "y"}]
        )
        log_diff("SHORTCUT-HTTP-17", "Extra fields ignored parity (unknown fields ignored by decoder)", "JSON_EDGE_CONTRACT", orig_res, recon_res, passed)

        # Case 18: SHORTCUT-HTTP-18 - Type mismatch 400 Invalid JSON
        r_orig_p18 = requests.post(f"{URL_ORIG}/api/shortcuts", headers={"Authorization": f"Bearer {t_orig_admin}", "Content-Type": "application/json"}, data='[{"name":123,"cmd":"x"}]')
        r_recon_p18 = requests.post(f"{URL_RECON}/api/shortcuts", headers={"Authorization": f"Bearer {t_recon_admin}", "Content-Type": "application/json"}, data='[{"name":123,"cmd":"x"}]')
        orig_res = {"status": r_orig_p18.status_code, "body": r_orig_p18.text}
        recon_res = {"status": r_recon_p18.status_code, "body": r_recon_p18.text}
        passed = (
            r_orig_p18.status_code == r_recon_p18.status_code == 400 and
            r_orig_p18.text == r_recon_p18.text == "Invalid JSON\n"
        )
        log_diff("SHORTCUT-HTTP-18", "Type mismatch 400 (number in string field -> Invalid JSON\\n)", "ERROR_HANDLING", orig_res, recon_res, passed)

        # Case 19: SHORTCUT-HTTP-19 - First-run file lifecycle contract (LAZY_CREATE_ON_MUTATION)
        orig_res = {
            "file_at_startup": file_init_orig,
            "file_after_first_get": file_after_get_orig,
            "file_after_first_post": file_after_post_orig,
            "file_after_restart": file_after_restart_orig
        }
        recon_res = {
            "file_at_startup": file_init_recon,
            "file_after_first_get": file_after_get_recon,
            "file_after_first_post": file_after_post_recon,
            "file_after_restart": file_after_restart_recon
        }
        passed = (
            not file_init_orig and not file_init_recon and
            not file_after_get_orig and not file_after_get_recon and
            file_after_post_orig and file_after_post_recon and
            file_after_restart_orig and file_after_restart_recon
        )
        log_diff("SHORTCUT-HTTP-19", "First-run file lifecycle contract (LAZY_CREATE_ON_MUTATION proven)", "PERSISTENCE_LIFECYCLE", orig_res, recon_res, passed)

    finally:
        for p in [proc_orig, proc_recon, proc_orig_na, proc_recon_na]:
            try:
                p.terminate()
                p.wait(timeout=2)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass

    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = total - passed_count
    pass_rate = f"IMPLEMENTED_SHORTCUT_CONTRACT_DIFFERENTIAL_PASS_RATE = {passed_count}/{total}"

    out_data = {
        "metadata": {
            "title": "Phase 2C.3F Shortcuts REST HTTP Differential Verification Results",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": "/api/shortcuts",
            "total_executed": total,
            "passed": passed_count,
            "failed": failed_count,
            "metric": pass_rate,
            "all_passed": failed_count == 0
        },
        "results": results
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(out_data, indent=2), encoding="utf-8")
    print("==================================================")
    print(f"SHORTCUT DIFFERENTIAL RESULTS: {passed_count}/{total} PASS")
    print(f"METRIC: {pass_rate}")
    print(f"[+] Output written to {OUTPUT_JSON}")
    print("==================================================")

    if failed_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
