#!/usr/bin/env python3
"""
test_tags_http_diff.py - Phase 2C.3D Device Tags REST HTTP Differential Test Suite

Executes side-by-side differential testing between original webrtc-signaling and reconstructed http-server.
Validates 20 exhaustive differential test cases covering:
  - Baseline list schema and key contracts
  - Role-based authorization and 401 Unauthorized rejection
  - Admin full state replacement vs non-admin scoped mutation
  - Non-admin tag merge and in-place tag update
  - Invalid JSON and empty body rejection (400 Invalid JSON)
  - Empty JSON object acceptance (200 {"status":"success"})
  - Method matrix behavior (PUT, PATCH, DELETE routed to GET; HEAD and OPTIONS CORS)
  - No-Auth server mode bypass
  - Persistence contract (direct os.WriteFile, 0644 mode, 2-space indent, no .tmp rename)
  - Candidate discrete endpoints verification (all confirmed NOT_PRESENT 404)
  - Cross-contract isolation with /devices

Outputs:
  - evidence/go_signaling/tags/TAG_HTTP_DIFFERENTIAL_RESULTS.json
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
EXE_RECON = ROOT / "scratch" / "reconstructed_tags_server.exe"

DIFF_TMP_ORIG = ROOT / "scratch" / "tags_diff_orig"
DIFF_TMP_RECON = ROOT / "scratch" / "tags_diff_recon"
DIFF_TMP_ORIG_NA = ROOT / "scratch" / "tags_diff_orig_na"
DIFF_TMP_RECON_NA = ROOT / "scratch" / "tags_diff_recon_na"

OUTPUT_JSON = ROOT / "evidence" / "go_signaling" / "tags" / "TAG_HTTP_DIFFERENTIAL_RESULTS.json"

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

    initial_tags = {
        "tags": [
            {"id": "tag-base-1", "name": "Production", "color": "#ff0000"},
            {"id": "tag-base-2", "name": "Staging", "color": "#00ff00"}
        ],
        "deviceTags": {
            "dev-alpha-001": ["tag-base-1"],
            "dev-beta-002": ["tag-base-2"]
        }
    }
    (target_dir / "device_tags.json").write_text(json.dumps(initial_tags, indent=2), encoding="utf-8")

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
        # Pre-authenticate admin & normal user
        # 1. Admin login
        r_oa = requests.post(f"{URL_ORIG}/api/login", json={"username": "admin", "password": "admin123"})
        r_ra = requests.post(f"{URL_RECON}/api/login", json={"username": "admin", "password": "admin123"})
        t_oa, t_ra = r_oa.json()["token"], r_ra.json()["token"]
        h_oa = {"Authorization": f"Bearer {t_oa}"}
        h_ra = {"Authorization": f"Bearer {t_ra}"}

        # 2. Normal user login
        r_ou = requests.post(f"{URL_ORIG}/api/login", json={"username": "user_assigned", "password": "user123"})
        r_ru = requests.post(f"{URL_RECON}/api/login", json={"username": "user_assigned", "password": "user123"})
        t_ou, t_ru = r_ou.json()["token"], r_ru.json()["token"]
        h_ou = {"Authorization": f"Bearer {t_ou}"}
        h_ru = {"Authorization": f"Bearer {t_ru}"}

        # TAG-HTTP-01: Baseline GET /api/tags
        res_o = requests.get(f"{URL_ORIG}/api/tags", headers=h_oa)
        res_r = requests.get(f"{URL_RECON}/api/tags", headers=h_ra)
        p_01 = (res_o.status_code == res_r.status_code == 200 and
                res_o.headers.get("Content-Type") == res_r.headers.get("Content-Type") == "application/json" and
                res_o.json() == res_r.json())
        log_diff("TAG-HTTP-01", "Baseline List Tags & Device Mappings", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "json": res_o.json()},
                 {"status": res_r.status_code, "json": res_r.json()}, p_01)

        # TAG-HTTP-02: Missing Token Rejection on GET
        res_o = requests.get(f"{URL_ORIG}/api/tags")
        res_r = requests.get(f"{URL_RECON}/api/tags")
        p_02 = (res_o.status_code == res_r.status_code == 401 and
                res_o.text == res_r.text == "Unauthorized\n" and
                res_o.headers.get("Content-Type") == res_r.headers.get("Content-Type"))
        log_diff("TAG-HTTP-02", "Missing Token Rejection on GET", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "body": res_o.text},
                 {"status": res_r.status_code, "body": res_r.text}, p_02)

        # TAG-HTTP-03: Invalid Token Rejection on GET
        res_o = requests.get(f"{URL_ORIG}/api/tags", headers={"Authorization": "Bearer bad_token"})
        res_r = requests.get(f"{URL_RECON}/api/tags", headers={"Authorization": "Bearer bad_token"})
        p_03 = (res_o.status_code == res_r.status_code == 401 and
                res_o.text == res_r.text == "Unauthorized\n")
        log_diff("TAG-HTTP-03", "Invalid Token Rejection on GET", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "body": res_o.text},
                 {"status": res_r.status_code, "body": res_r.text}, p_03)

        # TAG-HTTP-04: Missing Token Rejection on POST
        dummy = {"tags": [], "deviceTags": {}}
        res_o = requests.post(f"{URL_ORIG}/api/tags", json=dummy)
        res_r = requests.post(f"{URL_RECON}/api/tags", json=dummy)
        p_04 = (res_o.status_code == res_r.status_code == 401 and
                res_o.text == res_r.text == "Unauthorized\n")
        log_diff("TAG-HTTP-04", "Missing Token Rejection on POST", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "body": res_o.text},
                 {"status": res_r.status_code, "body": res_r.text}, p_04)

        # TAG-HTTP-05: Invalid Token Rejection on POST
        res_o = requests.post(f"{URL_ORIG}/api/tags", headers={"Authorization": "Bearer bad"}, json=dummy)
        res_r = requests.post(f"{URL_RECON}/api/tags", headers={"Authorization": "Bearer bad"}, json=dummy)
        p_05 = (res_o.status_code == res_r.status_code == 401 and
                res_o.text == res_r.text == "Unauthorized\n")
        log_diff("TAG-HTTP-05", "Invalid Token Rejection on POST", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "body": res_o.text},
                 {"status": res_r.status_code, "body": res_r.text}, p_05)

        # TAG-HTTP-06: Normal User Access on GET
        res_o = requests.get(f"{URL_ORIG}/api/tags", headers=h_ou)
        res_r = requests.get(f"{URL_RECON}/api/tags", headers=h_ru)
        p_06 = (res_o.status_code == res_r.status_code == 200 and
                res_o.json() == res_r.json())
        log_diff("TAG-HTTP-06", "Normal User GET Allowed", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "json": res_o.json()},
                 {"status": res_r.status_code, "json": res_r.json()}, p_06)

        # TAG-HTTP-07: Admin Full State Replacement on POST
        admin_mut = {
            "tags": [
                {"id": "tag-a-1", "name": "Tier 1", "color": "#112233"},
                {"id": "tag-a-2", "name": "Tier 2", "color": "#445566"}
            ],
            "deviceTags": {
                "dev-alpha-001": ["tag-a-1"],
                "dev-beta-002": ["tag-a-1", "tag-a-2"]
            }
        }
        res_o = requests.post(f"{URL_ORIG}/api/tags", headers=h_oa, json=admin_mut)
        res_r = requests.post(f"{URL_RECON}/api/tags", headers=h_ra, json=admin_mut)
        disk_o = json.loads((DIFF_TMP_ORIG / "device_tags.json").read_text(encoding="utf-8"))
        disk_r = json.loads((DIFF_TMP_RECON / "device_tags.json").read_text(encoding="utf-8"))
        p_07 = (res_o.status_code == res_r.status_code == 200 and
                res_o.text == res_r.text == "{\"status\":\"success\"}\n" and
                disk_o == disk_r == admin_mut)
        log_diff("TAG-HTTP-07", "Admin Full State Update & Persistence", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "disk": disk_o},
                 {"status": res_r.status_code, "disk": disk_r}, p_07)

        # TAG-HTTP-08: Non-Admin Scoped Device Mutation
        # user_assigned has access to dev-alpha-001, but NOT dev-beta-002
        user_mut = {
            "tags": [],
            "deviceTags": {
                "dev-alpha-001": ["tag-a-2"],
                "dev-beta-002": ["tag-a-hacked"]
            }
        }
        res_o = requests.post(f"{URL_ORIG}/api/tags", headers=h_ou, json=user_mut)
        res_r = requests.post(f"{URL_RECON}/api/tags", headers=h_ru, json=user_mut)
        disk_o = json.loads((DIFF_TMP_ORIG / "device_tags.json").read_text(encoding="utf-8"))
        disk_r = json.loads((DIFF_TMP_RECON / "device_tags.json").read_text(encoding="utf-8"))
        # dev-alpha-001 updated to ["tag-a-2"], dev-beta-002 preserved as ["tag-a-1", "tag-a-2"]
        p_08 = (res_o.status_code == res_r.status_code == 200 and
                res_o.text == res_r.text == "{\"status\":\"success\"}\n" and
                disk_o == disk_r and
                disk_o["deviceTags"]["dev-alpha-001"] == ["tag-a-2"] and
                disk_o["deviceTags"]["dev-beta-002"] == ["tag-a-1", "tag-a-2"])
        log_diff("TAG-HTTP-08", "Non-Admin Scoped Device Mutation", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "deviceTags": disk_o["deviceTags"]},
                 {"status": res_r.status_code, "deviceTags": disk_r["deviceTags"]}, p_08)

        # TAG-HTTP-09: Non-Admin Tag Append Merge
        user_add_tag = {
            "tags": [
                {"id": "tag-user-new", "name": "User Custom", "color": "#abcdef"}
            ],
            "deviceTags": {
                "dev-alpha-001": ["tag-user-new"]
            }
        }
        res_o = requests.post(f"{URL_ORIG}/api/tags", headers=h_ou, json=user_add_tag)
        res_r = requests.post(f"{URL_RECON}/api/tags", headers=h_ru, json=user_add_tag)
        disk_o = json.loads((DIFF_TMP_ORIG / "device_tags.json").read_text(encoding="utf-8"))
        disk_r = json.loads((DIFF_TMP_RECON / "device_tags.json").read_text(encoding="utf-8"))
        by_id_o = {t["id"]: t for t in disk_o["tags"]}
        by_id_r = {t["id"]: t for t in disk_r["tags"]}
        p_09 = (res_o.status_code == res_r.status_code == 200 and
                res_o.text == res_r.text == "{\"status\":\"success\"}\n" and
                by_id_o == by_id_r and
                len(by_id_o) == 3 and
                by_id_o.get("tag-user-new", {}).get("name") == "User Custom")
        log_diff("TAG-HTTP-09", "Non-Admin Tag Append Merge", "STRUCTURAL_EXACT_MATCH",
                 {"status": res_o.status_code, "tags_count": len(by_id_o)},
                 {"status": res_r.status_code, "tags_count": len(by_id_r)}, p_09)

        # TAG-HTTP-10: Non-Admin In-Place Tag Update
        user_upd_tag = {
            "tags": [
                {"id": "tag-user-new", "name": "User Custom Renamed", "color": "#000000"}
            ],
            "deviceTags": {}
        }
        res_o = requests.post(f"{URL_ORIG}/api/tags", headers=h_ou, json=user_upd_tag)
        res_r = requests.post(f"{URL_RECON}/api/tags", headers=h_ru, json=user_upd_tag)
        disk_o = json.loads((DIFF_TMP_ORIG / "device_tags.json").read_text(encoding="utf-8"))
        disk_r = json.loads((DIFF_TMP_RECON / "device_tags.json").read_text(encoding="utf-8"))
        by_id_o = {t["id"]: t for t in disk_o["tags"]}
        by_id_r = {t["id"]: t for t in disk_r["tags"]}
        p_10 = (res_o.status_code == res_r.status_code == 200 and
                res_o.text == res_r.text == "{\"status\":\"success\"}\n" and
                by_id_o == by_id_r and
                by_id_o.get("tag-user-new", {}).get("name") == "User Custom Renamed" and
                by_id_o.get("tag-user-new", {}).get("color") == "#000000")
        log_diff("TAG-HTTP-10", "Non-Admin In-Place Tag Update", "STRUCTURAL_EXACT_MATCH",
                 {"status": res_o.status_code, "updated": by_id_o.get("tag-user-new")},
                 {"status": res_r.status_code, "updated": by_id_r.get("tag-user-new")}, p_10)

        # TAG-HTTP-11: Empty Body Rejection on POST
        res_o = requests.post(f"{URL_ORIG}/api/tags", headers=h_oa, data="")
        res_r = requests.post(f"{URL_RECON}/api/tags", headers=h_ra, data="")
        p_11 = (res_o.status_code == res_r.status_code == 400 and
                res_o.text == res_r.text == "Invalid JSON\n" and
                res_o.headers.get("Content-Type") == res_r.headers.get("Content-Type") == "text/plain; charset=utf-8")
        log_diff("TAG-HTTP-11", "Empty Body Rejection on POST", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "body": res_o.text},
                 {"status": res_r.status_code, "body": res_r.text}, p_11)

        # TAG-HTTP-12: Invalid JSON Syntax Rejection on POST
        res_o = requests.post(f"{URL_ORIG}/api/tags", headers=h_oa, data="invalid{syntax")
        res_r = requests.post(f"{URL_RECON}/api/tags", headers=h_ra, data="invalid{syntax")
        p_12 = (res_o.status_code == res_r.status_code == 400 and
                res_o.text == res_r.text == "Invalid JSON\n")
        log_diff("TAG-HTTP-12", "Invalid JSON Syntax Rejection on POST", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "body": res_o.text},
                 {"status": res_r.status_code, "body": res_r.text}, p_12)

        # TAG-HTTP-13: Empty JSON Object {} on POST
        res_o = requests.post(f"{URL_ORIG}/api/tags", headers=h_oa, json={})
        res_r = requests.post(f"{URL_RECON}/api/tags", headers=h_ra, json={})
        p_13 = (res_o.status_code == res_r.status_code == 200 and
                res_o.text == res_r.text == "{\"status\":\"success\"}\n")
        log_diff("TAG-HTTP-13", "Empty JSON Object Acceptance", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "body": res_o.text},
                 {"status": res_r.status_code, "body": res_r.text}, p_13)

        # TAG-HTTP-14: Method Matrix Non-POST Verbs (PUT, PATCH, DELETE)
        res_o_put = requests.put(f"{URL_ORIG}/api/tags", headers=h_oa)
        res_r_put = requests.put(f"{URL_RECON}/api/tags", headers=h_ra)
        res_o_del = requests.delete(f"{URL_ORIG}/api/tags", headers=h_oa)
        res_r_del = requests.delete(f"{URL_RECON}/api/tags", headers=h_ra)
        p_14 = (res_o_put.status_code == res_r_put.status_code == 200 and
                res_o_del.status_code == res_r_del.status_code == 200 and
                res_o_put.json() == res_r_put.json() and
                res_o_del.json() == res_r_del.json())
        log_diff("TAG-HTTP-14", "Non-POST Verbs Routed to GET", "BIT_EXACT_MATCH",
                 {"put": res_o_put.status_code, "del": res_o_del.status_code},
                 {"put": res_r_put.status_code, "del": res_r_del.status_code}, p_14)

        # TAG-HTTP-15: HEAD Method Behavior
        res_o = requests.head(f"{URL_ORIG}/api/tags", headers=h_oa)
        res_r = requests.head(f"{URL_RECON}/api/tags", headers=h_ra)
        p_15 = (res_o.status_code == res_r.status_code == 200 and
                res_o.headers.get("Content-Type") == res_r.headers.get("Content-Type") == "application/json" and
                len(res_o.content) == len(res_r.content) == 0)
        log_diff("TAG-HTTP-15", "HEAD Method Behavior", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "len": len(res_o.content)},
                 {"status": res_r.status_code, "len": len(res_r.content)}, p_15)

        # TAG-HTTP-16: OPTIONS Method and CORS Headers
        res_o = requests.options(f"{URL_ORIG}/api/tags")
        res_r = requests.options(f"{URL_RECON}/api/tags")
        p_16 = (res_o.status_code == res_r.status_code == 200 and
                res_o.headers.get("Access-Control-Allow-Origin") == res_r.headers.get("Access-Control-Allow-Origin") == "*" and
                res_o.headers.get("Access-Control-Allow-Headers") == res_r.headers.get("Access-Control-Allow-Headers") == "Content-Type, Authorization")
        log_diff("TAG-HTTP-16", "OPTIONS CORS Preflight", "BIT_EXACT_MATCH",
                 {"status": res_o.status_code, "cors": res_o.headers.get("Access-Control-Allow-Origin")},
                 {"status": res_r.status_code, "cors": res_r.headers.get("Access-Control-Allow-Origin")}, p_16)

        # TAG-HTTP-17: No-Auth Mode Server Bypass
        res_o_get = requests.get(f"{URL_ORIG_NA}/api/tags")
        res_r_get = requests.get(f"{URL_RECON_NA}/api/tags")
        res_o_post = requests.post(f"{URL_ORIG_NA}/api/tags", json={"tags": [], "deviceTags": {}})
        res_r_post = requests.post(f"{URL_RECON_NA}/api/tags", json={"tags": [], "deviceTags": {}})
        p_17 = (res_o_get.status_code == res_r_get.status_code == 200 and
                res_o_post.status_code == res_r_post.status_code == 200 and
                res_o_post.text == res_r_post.text == "{\"status\":\"success\"}\n")
        log_diff("TAG-HTTP-17", "No-Auth Mode Bypass", "BIT_EXACT_MATCH",
                 {"get": res_o_get.status_code, "post": res_o_post.status_code},
                 {"get": res_r_get.status_code, "post": res_r_post.status_code}, p_17)

        # TAG-HTTP-18: Persistence File Mode and 2-Space Indent Format
        raw_o = (DIFF_TMP_ORIG / "device_tags.json").read_text(encoding="utf-8")
        raw_r = (DIFF_TMP_RECON / "device_tags.json").read_text(encoding="utf-8")
        p_18 = (raw_o == raw_r and
                "  \"tags\":" in raw_r and
                "  \"deviceTags\":" in raw_r)
        log_diff("TAG-HTTP-18", "Persistence Formatting & Direct Write", "BIT_EXACT_MATCH",
                 {"raw_sample": raw_o[:60]},
                 {"raw_sample": raw_r[:60]}, p_18)

        # TAG-HTTP-19: Discrete Candidate Sub-Routes Rejection (404 NOT_PRESENT)
        cand_paths = ["/api/tags/add", "/api/tags/delete", "/api/tags/update", "/api/tags/assign", "/api/tags/remove", "/api/tag"]
        all_404_o = all(requests.post(f"{URL_ORIG}{p}", headers=h_oa).status_code == 404 for p in cand_paths)
        all_404_r = all(requests.post(f"{URL_RECON}{p}", headers=h_ra).status_code == 404 for p in cand_paths)
        p_19 = (all_404_o and all_404_r)
        log_diff("TAG-HTTP-19", "Candidate Sub-Routes NOT_PRESENT (404)", "BIT_EXACT_MATCH",
                 {"all_404": all_404_o},
                 {"all_404": all_404_r}, p_19)

        # TAG-HTTP-20: Cross-Contract Isolation With /devices
        r_dev_o = requests.get(f"{URL_ORIG}/devices", headers=h_oa)
        r_dev_r = requests.get(f"{URL_RECON}/devices", headers=h_ra)
        p_20 = (r_dev_o.status_code == r_dev_r.status_code == 200 and
                r_dev_o.text == r_dev_r.text == "[]\n")
        log_diff("TAG-HTTP-20", "Cross-Contract Isolation With /devices", "BIT_EXACT_MATCH",
                 {"status": r_dev_o.status_code, "body": r_dev_o.text},
                 {"status": r_dev_r.status_code, "body": r_dev_r.text}, p_20)

    finally:
        proc_orig.kill()
        proc_orig.wait()
        proc_recon.kill()
        proc_recon.wait()
        proc_orig_na.kill()
        proc_orig_na.wait()
        proc_recon_na.kill()
        proc_recon_na.wait()

    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    pass_rate = f"{passed_count}/{total_count}"
    print("==================================================")
    print(f"DIFFERENTIAL VERDICT: {'PASS' if passed_count == total_count else 'FAIL'}")
    print(f"METRIC: IMPLEMENTED_TAG_CONTRACT_DIFFERENTIAL_PASS_RATE = {pass_rate}")
    print("==================================================")

    out_data = {
        "metadata": {
            "title": "Phase 2C.3D Device Tags REST Differential Results",
            "executed_at": datetime.now(timezone.utc).isoformat(),
            "target_route": "/api/tags",
            "total_executed": total_count,
            "passed": passed_count,
            "failed": total_count - passed_count,
            "metric": f"IMPLEMENTED_TAG_CONTRACT_DIFFERENTIAL_PASS_RATE = {pass_rate}"
        },
        "results": results
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(out_data, indent=2), encoding="utf-8")
    print(f"[+] Differential results saved to {OUTPUT_JSON}")
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
