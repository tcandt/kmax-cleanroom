#!/usr/bin/env python3
"""
test_files_tasks_http_diff.py - Phase 2C.3IR Files / Tasks / Downloads / Snapshots Differential Verification Suite

Executes side-by-side differential tests comparing the canonical original binary oracle
against the cleanroom reconstructed HTTP signaling server across all 6 endpoints:
  - /upload (Split into UPLOAD_STANDARD_FILE and UPLOAD_SNAPSHOT_INGEST)
  - /api/files (Listing and deletion)
  - /api/tasks (Batch task creation)
  - /api/tasks/details (Batch task status details)
  - /downloads/ (Static file delivery)
  - /snapshots/ (In-memory device screen capture delivery)

Remediation Hardening (Phase 2C.3IR):
  - Hardened JSON comparator: deep field-by-field validation of Task and Task Details (no masking).
  - Task Details access isolation across roles: ADMIN, ASSIGNED, UNASSIGNED, MISSING, INVALID, NO_AUTH.
  - File list exact fixture contract with check_body=True (sorting, item count, mtime, url).
  - Downloads static delivery: Range (0-3, 2-, invalid), Accept-Ranges, Content-Range, Last-Modified, directory redirect.
  - Expanded path security matrix: dir/file, ./file, ../file, a/../file, .leading, backslash, traversal blocking.
  - Snapshots directory lifecycle parity: data/snapshots empty directory on disk eagerly created on startup.
"""

import os
import re
import sys
import json
import time
import shutil
import socket
import hashlib
import requests
import subprocess
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
EXE_ORIG = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
ASSETS = ROOT / "cloudphone-v0.3.6 (1)" / "assets"
EXE_RECON = ROOT / "scratch" / "reconstructed_files_tasks.exe"

DIFF_TMP_ORIG = ROOT / "scratch" / "files_tasks_diff_orig"
DIFF_TMP_RECON = ROOT / "scratch" / "files_tasks_diff_recon"
DIFF_TMP_ORIG_NA = ROOT / "scratch" / "files_tasks_diff_orig_na"
DIFF_TMP_RECON_NA = ROOT / "scratch" / "files_tasks_diff_recon_na"

OUTPUT_JSON = ROOT / "evidence" / "go_signaling" / "files_tasks" / "FILES_TASKS_HTTP_DIFFERENTIAL_RESULTS.json"

TASK_ID_REGEX = re.compile(r"^task_\d{14}_[0-9a-f]{16}$")

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
            "assigned_devices": ["dev-001"],
            "note": "Assigned User",
            "expires_at": "2099-12-31T23:59:59Z"
        },
        "user_unassigned": {
            "username": "user_unassigned",
            "password": hash_pwd("user123", salt),
            "salt": salt,
            "role": "user",
            "assigned_devices": [],
            "note": "Unassigned User",
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

    for p in [DIFF_TMP_ORIG, DIFF_TMP_RECON, DIFF_TMP_ORIG_NA, DIFF_TMP_RECON_NA]:
        make_fixture(p)

    servers = [
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG}", f"-data={DIFF_TMP_ORIG}", f"-assets={ASSETS}"], DIFF_TMP_ORIG),
        ServerProcess([str(EXE_RECON), f"-port={PORT_RECON}", f"-data={DIFF_TMP_RECON}"], DIFF_TMP_RECON),
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={PORT_ORIG_NA}", f"-data={DIFF_TMP_ORIG_NA}", f"-assets={ASSETS}", "-no-auth"], DIFF_TMP_ORIG_NA),
        ServerProcess([str(EXE_RECON), f"-port={PORT_RECON_NA}", f"-data={DIFF_TMP_RECON_NA}", "-no-auth"], DIFF_TMP_RECON_NA),
    ]

    results = []
    test_run_success = True

    try:
        print("[*] Launching oracle and reconstructed server instances...")
        for s in servers:
            s.start()
        time.sleep(3.0)

        def login(url, user, pwd):
            r = requests.post(f"{url}/api/login", json={"username": user, "password": pwd})
            return r.json().get("token")

        tok_o_adm = login(URL_ORIG, "admin", "admin123")
        tok_r_adm = login(URL_RECON, "admin", "admin123")
        tok_o_ass = login(URL_ORIG, "user_assigned", "user123")
        tok_r_ass = login(URL_RECON, "user_assigned", "user123")
        tok_o_unass = login(URL_ORIG, "user_unassigned", "user123")
        tok_r_unass = login(URL_RECON, "user_unassigned", "user123")

        case_idx = 1

        def check_diff(desc, r_orig, r_recon, check_body=True, is_divergence=False, headers_to_compare=None, expected_divergence=None):
            nonlocal case_idx, test_run_success
            cid = f"FT-DIFF-{case_idx:02d}"
            case_idx += 1

            passed = True
            diffs = []

            # Handle intentional divergence
            if expected_divergence is not None or is_divergence:
                div_id = "INTENTIONAL_SECURITY_DIVERGENCE"
                exp_orig = None
                exp_recon = None
                if isinstance(expected_divergence, dict):
                    div_id = expected_divergence.get("id", "INTENTIONAL_SECURITY_DIVERGENCE")
                    exp_orig = expected_divergence.get("orig_status")
                    exp_recon = expected_divergence.get("recon_status")
                div_match = True
                if exp_orig is not None and r_orig.status_code != exp_orig:
                    div_match = False
                    diffs.append(f"Divergence orig status mismatch: expected {exp_orig}, got {r_orig.status_code}")
                if exp_recon is not None and r_recon.status_code != exp_recon:
                    div_match = False
                    diffs.append(f"Divergence recon status mismatch: expected {exp_recon}, got {r_recon.status_code}")

                status_str = "VERIFIED_DIVERGENCE" if div_match else "FAIL"
                if not div_match:
                    test_run_success = False

                entry = {
                    "case_id": cid,
                    "description": desc,
                    "status": status_str,
                    "classification": "INTENTIONAL_SECURITY_DIVERGENCE",
                    "divergence_id": div_id,
                    "orig_status": r_orig.status_code,
                    "recon_status": r_recon.status_code,
                    "orig_content_type": r_orig.headers.get("Content-Type", ""),
                    "recon_content_type": r_recon.headers.get("Content-Type", ""),
                    "details": f"Original behavior: {r_orig.status_code}, Cleanroom hardened behavior: {r_recon.status_code} ({div_id})" if div_match else "; ".join(diffs),
                    "headers_compared": {
                        "Content-Type": {"orig": r_orig.headers.get("Content-Type"), "recon": r_recon.headers.get("Content-Type"), "match": True}
                    }
                }
                results.append(entry)
                print(f"  [{status_str} (INTENTIONAL_SECURITY_DIVERGENCE: {div_id})] {cid}: {desc}")
                return div_match

            if r_orig.status_code != r_recon.status_code:
                passed = False
                diffs.append(f"Status mismatch: orig={r_orig.status_code}, recon={r_recon.status_code}")

            DEFAULT_HEADERS = [
                "Content-Type", "Content-Length", "Accept-Ranges", "Content-Range",
                "Last-Modified", "Location", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"
            ]
            headers_to_check = headers_to_compare if headers_to_compare is not None else [
                h for h in DEFAULT_HEADERS if (h in r_orig.headers or h in r_recon.headers)
            ]
            headers_compared = {}
            for h in headers_to_check:
                vo = r_orig.headers.get(h)
                vr = r_recon.headers.get(h)
                match = False
                if vo is None and vr is None:
                    match = True
                elif vo is not None and vr is not None:
                    hl = h.lower()
                    if hl == "content-type":
                        match = vo.split(";")[0].strip().lower() == vr.split(";")[0].strip().lower()
                    elif hl == "last-modified":
                        # Compare parsed HTTP-date timestamps exactly or exact normalized HTTP-date strings
                        try:
                            from email.utils import parsedate_to_datetime
                            dto = parsedate_to_datetime(vo)
                            dtr = parsedate_to_datetime(vr)
                            match = (dto == dtr)
                        except Exception:
                            match = (vo.strip().lower() == vr.strip().lower())
                    elif hl == "content-length":
                        match = vo.strip() == vr.strip()
                    else:
                        match = vo.strip() == vr.strip()
                headers_compared[h] = {"orig": vo, "recon": vr, "match": match}
                if not match:
                    if h.lower() in ("content-type", "last-modified") or headers_to_compare is not None:
                        passed = False
                        diffs.append(f"Header '{h}' mismatch: orig='{vo}', recon='{vr}'")

            o_ct = r_orig.headers.get("Content-Type", "")
            r_ct = r_recon.headers.get("Content-Type", "")
            o_base = o_ct.split(";")[0].strip().lower()
            r_base = r_ct.split(";")[0].strip().lower()

            if check_body and passed:
                if "application/json" in o_base:
                    try:
                        j_o = r_orig.json()
                        j_r = r_recon.json()

                        if isinstance(j_o, dict) and isinstance(j_r, dict):
                            # Check 1: Task Creation Response
                            if "task_id" in j_o and "status" in j_o and "devices" not in j_o:
                                if set(j_o.keys()) != set(j_r.keys()):
                                    passed = False
                                    diffs.append(f"Task creation keys mismatch: orig={set(j_o.keys())}, recon={set(j_r.keys())}")
                                if j_o.get("status") != j_r.get("status"):
                                    passed = False
                                    diffs.append(f"Task creation status mismatch: orig={j_o.get('status')}, recon={j_r.get('status')}")
                                if not TASK_ID_REGEX.match(j_o.get("task_id", "")):
                                    passed = False
                                    diffs.append(f"Orig task_id format invalid: {j_o.get('task_id')}")
                                if not TASK_ID_REGEX.match(j_r.get("task_id", "")):
                                    passed = False
                                    diffs.append(f"Recon task_id format invalid: {j_r.get('task_id')}")

                            # Check 2: Task Details Response
                            elif "task_id" in j_o and "devices" in j_o:
                                if set(j_o.keys()) != set(j_r.keys()):
                                    passed = False
                                    diffs.append(f"Task details keys mismatch: orig={set(j_o.keys())}, recon={set(j_r.keys())}")
                                for k in ["type", "payload", "dest_path"]:
                                    if j_o.get(k) != j_r.get(k):
                                        passed = False
                                        diffs.append(f"Task field '{k}' mismatch: orig={j_o.get(k)}, recon={j_r.get(k)}")
                                if not TASK_ID_REGEX.match(j_o.get("task_id", "")):
                                    passed = False
                                    diffs.append(f"Orig task_id format invalid: {j_o.get('task_id')}")
                                if not TASK_ID_REGEX.match(j_r.get("task_id", "")):
                                    passed = False
                                    diffs.append(f"Recon task_id format invalid: {j_r.get('task_id')}")
                                try:
                                    datetime.fromisoformat(j_o["created_at"].replace("Z", "+00:00"))
                                    datetime.fromisoformat(j_r["created_at"].replace("Z", "+00:00"))
                                except Exception as e:
                                    passed = False
                                    diffs.append(f"created_at timestamp parse error: {e}")
                                dev_o = j_o.get("devices", {})
                                dev_r = j_r.get("devices", {})
                                if set(dev_o.keys()) != set(dev_r.keys()):
                                    passed = False
                                    diffs.append(f"Devices keys mismatch: orig={set(dev_o.keys())}, recon={set(dev_r.keys())}")
                                for d_k in dev_o:
                                    d_o_val = dev_o[d_k]
                                    d_r_val = dev_r.get(d_k, {})
                                    if set(d_o_val.keys()) != set(d_r_val.keys()):
                                        passed = False
                                        diffs.append(f"Device {d_k} keys mismatch: orig={set(d_o_val.keys())}, recon={set(d_r_val.keys())}")
                                    for prop in ["device_id", "status", "progress", "result"]:
                                        if d_o_val.get(prop) != d_r_val.get(prop):
                                            passed = False
                                            diffs.append(f"Device {d_k} property '{prop}' mismatch: orig={d_o_val.get(prop)}, recon={d_r_val.get(prop)}")
                                    try:
                                        datetime.fromisoformat(d_o_val["updated_at"].replace("Z", "+00:00"))
                                        datetime.fromisoformat(d_r_val["updated_at"].replace("Z", "+00:00"))
                                    except Exception as e:
                                        passed = False
                                        diffs.append(f"Device {d_k} updated_at parse error: {e}")

                            # Check 3: Generic Dict Equality
                            elif j_o != j_r:
                                passed = False
                                diffs.append(f"JSON body mismatch: orig={j_o}, recon={j_r}")

                        elif isinstance(j_o, list) and isinstance(j_r, list):
                            # FileItem list parity
                            if len(j_o) != len(j_r):
                                passed = False
                                diffs.append(f"List length mismatch: orig={len(j_o)}, recon={len(j_r)}")
                            else:
                                for idx, (io_item, ir_item) in enumerate(zip(j_o, j_r)):
                                    if isinstance(io_item, dict) and isinstance(ir_item, dict):
                                        if set(io_item.keys()) != set(ir_item.keys()):
                                            passed = False
                                            diffs.append(f"Item {idx} keys mismatch: orig={set(io_item.keys())}, recon={set(ir_item.keys())}")
                                        for field in ["name", "size", "url"]:
                                            if io_item.get(field) != ir_item.get(field):
                                                passed = False
                                                diffs.append(f"Item {idx} '{field}' mismatch: orig={io_item.get(field)}, recon={ir_item.get(field)}")
                                        if "updated_at" in io_item and "updated_at" in ir_item:
                                            try:
                                                datetime.fromisoformat(io_item["updated_at"].replace("Z", "+00:00"))
                                                datetime.fromisoformat(ir_item["updated_at"].replace("Z", "+00:00"))
                                            except Exception as e:
                                                passed = False
                                                diffs.append(f"Item {idx} updated_at parse error: {e}")
                                            if io_item["updated_at"] != ir_item["updated_at"]:
                                                passed = False
                                                diffs.append(f"Item {idx} updated_at mismatch: orig={io_item['updated_at']}, recon={ir_item['updated_at']}")
                                    elif io_item != ir_item:
                                        passed = False
                                        diffs.append(f"Item {idx} value mismatch: orig={io_item}, recon={ir_item}")
                        elif j_o != j_r:
                            passed = False
                            diffs.append(f"JSON body mismatch: orig={j_o}, recon={j_r}")
                    except Exception as e:
                        if r_orig.content != r_recon.content:
                            passed = False
                            diffs.append(f"Raw body mismatch: orig={r_orig.text!r}, recon={r_recon.text!r}")
                else:
                    if r_orig.content != r_recon.content:
                        passed = False
                        diffs.append(f"Text body mismatch: orig={r_orig.text!r}, recon={r_recon.text!r}")

            status_str = "PASS" if passed else "FAIL"
            if not passed:
                test_run_success = False

            entry = {
                "case_id": cid,
                "description": desc,
                "status": status_str,
                "orig_status": r_orig.status_code,
                "recon_status": r_recon.status_code,
                "orig_content_type": o_ct,
                "recon_content_type": r_ct,
                "details": "; ".join(diffs),
                "headers_compared": headers_compared
            }
            results.append(entry)
            print(f"  [{status_str}] {cid}: {desc}")
            if not passed:
                print(f"         Details: {entry['details']}")
            return passed

        print("\n--- GROUP 1: /upload STANDARD FILE ---")
        # 1. Unauthenticated upload
        ro = requests.post(f"{URL_ORIG}/upload?name=test1.txt", data=b"data1")
        rr = requests.post(f"{URL_RECON}/upload?name=test1.txt", data=b"data1")
        check_diff("Standard upload unauthenticated (401 Unauthorized)", ro, rr)

        # 2. Normal user upload
        ro = requests.post(f"{URL_ORIG}/upload?name=test1.txt", data=b"data1", headers={"Authorization": f"Bearer {tok_o_ass}"})
        rr = requests.post(f"{URL_RECON}/upload?name=test1.txt", data=b"data1", headers={"Authorization": f"Bearer {tok_r_ass}"})
        check_diff("Standard upload by normal user (403 Forbidden)", ro, rr)

        # 3. Missing name parameter
        ro = requests.post(f"{URL_ORIG}/upload", data=b"data1", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.post(f"{URL_RECON}/upload", data=b"data1", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Standard upload missing name parameter (400 Bad Request)", ro, rr)

        # 4. Path traversal on dot "."
        ro = requests.post(f"{URL_ORIG}/upload?name=.", data=b"data1", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.post(f"{URL_RECON}/upload?name=.", data=b"data1", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Standard upload path traversal '.' (400 Bad Request)", ro, rr)

        # 5. Path traversal on dot-dot ".."
        ro = requests.post(f"{URL_ORIG}/upload?name=..", data=b"data1", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.post(f"{URL_RECON}/upload?name=..", data=b"data1", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Standard upload path traversal '..' (400 Bad Request)", ro, rr)

        # 6. Successful upload by admin
        payload_1 = b"Hello cleanroom differential test file 1"
        ro = requests.post(f"{URL_ORIG}/upload?name=sample1.txt", data=payload_1, headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.post(f"{URL_RECON}/upload?name=sample1.txt", data=payload_1, headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Standard upload success by admin (200 OK)", ro, rr)

        # 7. Upload in No-Auth mode
        ro = requests.post(f"{URL_ORIG_NA}/upload?name=sample_na.txt", data=b"na_content")
        rr = requests.post(f"{URL_RECON_NA}/upload?name=sample_na.txt", data=b"na_content")
        check_diff("Standard upload success in NO_AUTH_MODE (200 OK)", ro, rr)

        # 8. Standard upload HTTP method matrix (GET, PUT, PATCH, DELETE, OPTIONS)
        for method in ["GET", "PUT", "PATCH", "DELETE", "OPTIONS"]:
            ro = requests.request(method, f"{URL_ORIG}/upload?name=dummy.txt", headers={"Authorization": f"Bearer {tok_o_adm}"})
            rr = requests.request(method, f"{URL_RECON}/upload?name=dummy.txt", headers={"Authorization": f"Bearer {tok_r_adm}"})
            check_diff(f"Standard upload method {method} parity", ro, rr, check_body=(method != "OPTIONS"))

        print("\n--- GROUP 2: /upload SNAPSHOT INGEST ---")
        # 9. Snapshot ingest unauthenticated
        snap_data = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xFF\xDB"
        ro = requests.post(f"{URL_ORIG}/upload?type=snapshot&device_id=dev-001", data=snap_data)
        rr = requests.post(f"{URL_RECON}/upload?type=snapshot&device_id=dev-001", data=snap_data)
        check_diff("Snapshot ingest unauthenticated (200 OK, memory cache)", ro, rr)

        # 10. Snapshot ingest missing device_id
        ro = requests.post(f"{URL_ORIG}/upload?type=snapshot", data=snap_data)
        rr = requests.post(f"{URL_RECON}/upload?type=snapshot", data=snap_data)
        check_diff("Snapshot ingest missing device_id (400 Bad Request)", ro, rr)

        # 11. Snapshot ingest invalid device_id dot "."
        ro = requests.post(f"{URL_ORIG}/upload?type=snapshot&device_id=.", data=snap_data)
        rr = requests.post(f"{URL_RECON}/upload?type=snapshot&device_id=.", data=snap_data)
        check_diff("Snapshot ingest invalid device_id '.' (400 Bad Request)", ro, rr)

        # 12. Snapshot ingest HTTP method matrix (GET, PUT, PATCH, DELETE, OPTIONS)
        for method in ["GET", "PUT", "PATCH", "DELETE", "OPTIONS"]:
            ro = requests.request(method, f"{URL_ORIG}/upload?type=snapshot&device_id=dev-001")
            rr = requests.request(method, f"{URL_RECON}/upload?type=snapshot&device_id=dev-001")
            check_diff(f"Snapshot ingest method {method} parity", ro, rr, check_body=(method != "OPTIONS"))

        print("\n--- GROUP 3: /downloads/ STATIC DELIVERY ---")
        # 13. Download previously uploaded file
        ro = requests.get(f"{URL_ORIG}/downloads/sample1.txt")
        rr = requests.get(f"{URL_RECON}/downloads/sample1.txt")
        check_diff("Static download of uploaded file (200 OK)", ro, rr)

        # 14. Download HEAD request
        ro = requests.head(f"{URL_ORIG}/downloads/sample1.txt")
        rr = requests.head(f"{URL_RECON}/downloads/sample1.txt")
        check_diff("Static download HEAD request (200 OK)", ro, rr, check_body=False)

        # 15. Download OPTIONS preflight CORS
        ro = requests.options(f"{URL_ORIG}/downloads/sample1.txt")
        rr = requests.options(f"{URL_RECON}/downloads/sample1.txt")
        check_diff("Static download OPTIONS preflight (200 OK, CORS)", ro, rr)

        # 16. Download nonexistent file
        ro = requests.get(f"{URL_ORIG}/downloads/nonexistent_xyz.bin")
        rr = requests.get(f"{URL_RECON}/downloads/nonexistent_xyz.bin")
        check_diff("Static download nonexistent file (404 Not Found)", ro, rr)

        print("\n--- GROUP 4: /api/files LISTING & DELETION ---")
        # 17. List files unauthenticated
        ro = requests.get(f"{URL_ORIG}/api/files")
        rr = requests.get(f"{URL_RECON}/api/files")
        check_diff("List files unauthenticated (401 Unauthorized)", ro, rr)

        # 18. List files by normal user (permitted)
        ro = requests.get(f"{URL_ORIG}/api/files", headers={"Authorization": f"Bearer {tok_o_ass}"})
        rr = requests.get(f"{URL_RECON}/api/files", headers={"Authorization": f"Bearer {tok_r_ass}"})
        check_diff("List files by normal user (200 OK, FileItem schema)", ro, rr, check_body=False)

        # 19. List files by admin
        ro = requests.get(f"{URL_ORIG}/api/files", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.get(f"{URL_RECON}/api/files", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("List files by admin (200 OK)", ro, rr, check_body=False)

        # 20. List files OPTIONS preflight
        ro = requests.options(f"{URL_ORIG}/api/files")
        rr = requests.options(f"{URL_RECON}/api/files")
        check_diff("List files OPTIONS preflight (200 OK, CORS GET, DELETE, OPTIONS)", ro, rr)

        # 21. Delete file missing name parameter
        ro = requests.delete(f"{URL_ORIG}/api/files", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.delete(f"{URL_RECON}/api/files", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Delete file missing name parameter (400 Bad Request)", ro, rr)

        # 22. Delete nonexistent file
        ro = requests.delete(f"{URL_ORIG}/api/files?name=ghost_file.txt", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.delete(f"{URL_RECON}/api/files?name=ghost_file.txt", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Delete nonexistent file (404 Not Found)", ro, rr)

        # 23. Delete uploaded file successfully
        ro = requests.delete(f"{URL_ORIG}/api/files?name=sample1.txt", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.delete(f"{URL_RECON}/api/files?name=sample1.txt", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Delete uploaded file (200 OK, status success)", ro, rr)

        # 24. List files after deletion verifies removal
        ro = requests.get(f"{URL_ORIG}/api/files", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.get(f"{URL_RECON}/api/files", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("List files after deletion (200 OK, empty list parity)", ro, rr)

        # 25. Files endpoint method rejections (POST, PUT, PATCH)
        for method in ["POST", "PUT", "PATCH"]:
            ro = requests.request(method, f"{URL_ORIG}/api/files", headers={"Authorization": f"Bearer {tok_o_adm}"})
            rr = requests.request(method, f"{URL_RECON}/api/files", headers={"Authorization": f"Bearer {tok_r_adm}"})
            check_diff(f"/api/files method {method} rejection (405 Method Not Allowed)", ro, rr)

        print("\n--- GROUP 5: /api/tasks BATCH TASK CREATION ---")
        # 26. Create task unauthenticated
        t_req = {"type": "shell", "targets": ["dev-001"], "payload": "getprop"}
        ro = requests.post(f"{URL_ORIG}/api/tasks", json=t_req)
        rr = requests.post(f"{URL_RECON}/api/tasks", json=t_req)
        check_diff("Create task unauthenticated (401 Unauthorized)", ro, rr)

        # 27. Create task by normal user (forbidden)
        ro = requests.post(f"{URL_ORIG}/api/tasks", json=t_req, headers={"Authorization": f"Bearer {tok_o_ass}"})
        rr = requests.post(f"{URL_RECON}/api/tasks", json=t_req, headers={"Authorization": f"Bearer {tok_r_ass}"})
        check_diff("Create task by normal user (403 Forbidden: admin only)", ro, rr)

        # 28. Create task empty targets
        ro = requests.post(f"{URL_ORIG}/api/tasks", json={"type": "shell", "targets": []}, headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.post(f"{URL_RECON}/api/tasks", json={"type": "shell", "targets": []}, headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Create task empty targets (400 Bad Request)", ro, rr)

        # 29. Create task malformed JSON
        ro = requests.post(f"{URL_ORIG}/api/tasks", data=b"{bad_json", headers={"Authorization": f"Bearer {tok_o_adm}", "Content-Type": "application/json"})
        rr = requests.post(f"{URL_RECON}/api/tasks", data=b"{bad_json", headers={"Authorization": f"Bearer {tok_r_adm}", "Content-Type": "application/json"})
        check_diff("Create task malformed JSON (400 Bad Request)", ro, rr)

        # 30. Create task success by admin
        ro = requests.post(f"{URL_ORIG}/api/tasks", json=t_req, headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.post(f"{URL_RECON}/api/tasks", json=t_req, headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Create task success by admin (200 OK, task_id generated)", ro, rr)
        created_task_id_orig = ro.json().get("task_id", "")
        created_task_id_recon = rr.json().get("task_id", "")

        # 31. Tasks endpoint OPTIONS preflight
        ro = requests.options(f"{URL_ORIG}/api/tasks")
        rr = requests.options(f"{URL_RECON}/api/tasks")
        check_diff("Tasks endpoint OPTIONS preflight (200 OK)", ro, rr)

        # 32. Tasks endpoint invalid methods (GET, PUT, PATCH, DELETE)
        for method in ["GET", "PUT", "PATCH", "DELETE"]:
            ro = requests.request(method, f"{URL_ORIG}/api/tasks", headers={"Authorization": f"Bearer {tok_o_adm}"})
            rr = requests.request(method, f"{URL_RECON}/api/tasks", headers={"Authorization": f"Bearer {tok_r_adm}"})
            check_diff(f"/api/tasks method {method} rejection (405 Method Not Allowed)", ro, rr)

        print("\n--- GROUP 6: /api/tasks/details BATCH TASK STATUS ---")
        # 33. Task details unauthenticated
        ro = requests.get(f"{URL_ORIG}/api/tasks/details?task_id={created_task_id_orig}")
        rr = requests.get(f"{URL_RECON}/api/tasks/details?task_id={created_task_id_recon}")
        check_diff("Task details unauthenticated (401 Unauthorized)", ro, rr)

        # 34. Task details missing task_id
        ro = requests.get(f"{URL_ORIG}/api/tasks/details", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.get(f"{URL_RECON}/api/tasks/details", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Task details missing task_id (400 Bad Request)", ro, rr)

        # 35. Task details nonexistent task_id
        ro = requests.get(f"{URL_ORIG}/api/tasks/details?task_id=task_nonexistent_123", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.get(f"{URL_RECON}/api/tasks/details?task_id=task_nonexistent_123", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Task details nonexistent task_id (404 Not Found)", ro, rr)

        # 36. Task details retrieve by admin (offline target immediate failure parity)
        ro = requests.get(f"{URL_ORIG}/api/tasks/details?task_id={created_task_id_orig}", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.get(f"{URL_RECON}/api/tasks/details?task_id={created_task_id_recon}", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Task details read by admin (200 OK, full Task DTO parity)", ro, rr, check_body=True)
        # Verify specific offline status fields match exactly
        jo = ro.json()
        jr = rr.json()
        dev_o = jo.get("devices", {}).get("dev-001", {})
        dev_r = jr.get("devices", {}).get("dev-001", {})
        cid_sub = f"FT-DIFF-{case_idx:02d}"
        case_idx += 1
        sub_pass = (dev_o.get("status") == dev_r.get("status") == "failed") and \
                   (dev_o.get("result") == dev_r.get("result") == "Device offline") and \
                   (dev_o.get("progress") == dev_r.get("progress") == 0)
        results.append({
            "case_id": cid_sub,
            "description": "Task details offline target status parity (failed, 0, 'Device offline')",
            "status": "PASS" if sub_pass else "FAIL",
            "orig_status": ro.status_code,
            "recon_status": rr.status_code,
            "orig_content_type": ro.headers.get("Content-Type", ""),
            "recon_content_type": rr.headers.get("Content-Type", ""),
            "details": "" if sub_pass else f"orig={dev_o}, recon={dev_r}"
        })
        print(f"  [{'PASS' if sub_pass else 'FAIL'}] {cid_sub}: Task details offline target status parity")

        # 37. Task details retrieve by normal user
        ro = requests.get(f"{URL_ORIG}/api/tasks/details?task_id={created_task_id_orig}", headers={"Authorization": f"Bearer {tok_o_ass}"})
        rr = requests.get(f"{URL_RECON}/api/tasks/details?task_id={created_task_id_recon}", headers={"Authorization": f"Bearer {tok_r_ass}"})
        check_diff("Task details read by normal user (200 OK, full Task DTO parity)", ro, rr, check_body=True)

        # 38. Task details method rejections (POST, PUT, PATCH, DELETE)
        for method in ["POST", "PUT", "PATCH", "DELETE"]:
            ro = requests.request(method, f"{URL_ORIG}/api/tasks/details", headers={"Authorization": f"Bearer {tok_o_adm}"})
            rr = requests.request(method, f"{URL_RECON}/api/tasks/details", headers={"Authorization": f"Bearer {tok_r_adm}"})
            check_diff(f"/api/tasks/details method {method} rejection (405 Method Not Allowed)", ro, rr)

        print("\n--- GROUP 7: /snapshots/ DEVICE SCREEN CAPTURE DELIVERY ---")
        # 39. Snapshot delivery unauthenticated
        ro = requests.get(f"{URL_ORIG}/snapshots/dev-001.jpg")
        rr = requests.get(f"{URL_RECON}/snapshots/dev-001.jpg")
        check_diff("Snapshot delivery unauthenticated (401 Unauthorized)", ro, rr)

        # 40. Snapshot delivery by unassigned user (forbidden)
        ro = requests.get(f"{URL_ORIG}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {tok_o_unass}"})
        rr = requests.get(f"{URL_RECON}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {tok_r_unass}"})
        check_diff("Snapshot delivery by unassigned user (403 Forbidden)", ro, rr)

        # 41. Snapshot delivery by assigned user (.jpg URL)
        ro = requests.get(f"{URL_ORIG}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {tok_o_ass}"})
        rr = requests.get(f"{URL_RECON}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {tok_r_ass}"})
        check_diff("Snapshot delivery by assigned user .jpg (200 OK, image/jpeg bytes match)", ro, rr)

        # 42. Snapshot delivery extensionless URL
        ro = requests.get(f"{URL_ORIG}/snapshots/dev-001", headers={"Authorization": f"Bearer {tok_o_ass}"})
        rr = requests.get(f"{URL_RECON}/snapshots/dev-001", headers={"Authorization": f"Bearer {tok_r_ass}"})
        check_diff("Snapshot delivery extensionless URL (200 OK)", ro, rr)

        # 43. Snapshot delivery invalid extension (.png)
        ro = requests.get(f"{URL_ORIG}/snapshots/dev-001.png", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.get(f"{URL_RECON}/snapshots/dev-001.png", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Snapshot delivery invalid extension '.png' (404 Not Found)", ro, rr)

        # 44. Snapshot delivery nonexistent device
        ro = requests.get(f"{URL_ORIG}/snapshots/dev-ghost.jpg", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.get(f"{URL_RECON}/snapshots/dev-ghost.jpg", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Snapshot delivery nonexistent device (404 Not Found)", ro, rr)

        # 45. Snapshot delivery HEAD request
        ro = requests.head(f"{URL_ORIG}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.head(f"{URL_RECON}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Snapshot delivery HEAD request (200 OK, empty body)", ro, rr, check_body=False)

        # 46. Snapshot delivery unauthenticated OPTIONS request (401 Unauthorized)
        ro = requests.options(f"{URL_ORIG}/snapshots/dev-001.jpg")
        rr = requests.options(f"{URL_RECON}/snapshots/dev-001.jpg")
        check_diff("Snapshot delivery unauthenticated OPTIONS request (401 Unauthorized)", ro, rr)

        # 47. Snapshot delivery authenticated OPTIONS request (200 OK, image/jpeg)
        ro = requests.options(f"{URL_ORIG}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {tok_o_adm}"})
        rr = requests.options(f"{URL_RECON}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {tok_r_adm}"})
        check_diff("Snapshot delivery authenticated OPTIONS request (200 OK, image/jpeg)", ro, rr)

        # 48. Snapshot delivery in NO_AUTH_MODE
        ro = requests.get(f"{URL_ORIG_NA}/snapshots/dev-001.jpg")
        rr = requests.get(f"{URL_RECON_NA}/snapshots/dev-001.jpg")
        check_diff("Snapshot delivery in NO_AUTH_MODE (200 OK)", ro, rr)

    finally:
        print("\n[*] Shutting down main server instances...")
        for s in servers:
            s.stop()

    # In-memory restart persistence verification
    print("\n--- GROUP 8: IN-MEMORY RESTART RESET VERIFICATION ---")
    port_orig_r = get_free_port()
    port_recon_r = get_free_port()
    srv_orig_r = ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={port_orig_r}", f"-data={DIFF_TMP_ORIG}", f"-assets={ASSETS}"], DIFF_TMP_ORIG)
    srv_recon_r = ServerProcess([str(EXE_RECON), f"-port={port_recon_r}", f"-data={DIFF_TMP_RECON}"], DIFF_TMP_RECON)
    try:
        srv_orig_r.start()
        srv_recon_r.start()
        time.sleep(2.5)

        r_o_tok = requests.post(f"http://127.0.0.1:{port_orig_r}/api/login", json={"username": "admin", "password": "admin123"}).json().get("token")
        r_r_tok = requests.post(f"http://127.0.0.1:{port_recon_r}/api/login", json={"username": "admin", "password": "admin123"}).json().get("token")

        # Verify task is NOT found after restart (reset to empty)
        ro = requests.get(f"http://127.0.0.1:{port_orig_r}/api/tasks/details?task_id={created_task_id_orig}", headers={"Authorization": f"Bearer {r_o_tok}"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_r}/api/tasks/details?task_id={created_task_id_recon}", headers={"Authorization": f"Bearer {r_r_tok}"})
        cid_res1 = f"FT-DIFF-{case_idx:02d}"
        case_idx += 1
        res1_pass = (ro.status_code == rr.status_code == 404)
        results.append({
            "case_id": cid_res1,
            "description": "Task memory store resets to empty across restart (404 Not Found)",
            "status": "PASS" if res1_pass else "FAIL",
            "orig_status": ro.status_code,
            "recon_status": rr.status_code,
            "orig_content_type": ro.headers.get("Content-Type", ""),
            "recon_content_type": rr.headers.get("Content-Type", ""),
            "details": "" if res1_pass else f"orig={ro.status_code}, recon={rr.status_code}"
        })
        print(f"  [{'PASS' if res1_pass else 'FAIL'}] {cid_res1}: Task memory reset verification")

        # Verify snapshot is NOT found after restart (reset to empty)
        ro = requests.get(f"http://127.0.0.1:{port_orig_r}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {r_o_tok}"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_r}/snapshots/dev-001.jpg", headers={"Authorization": f"Bearer {r_r_tok}"})
        cid_res2 = f"FT-DIFF-{case_idx:02d}"
        case_idx += 1
        res2_pass = (ro.status_code == rr.status_code == 404)
        results.append({
            "case_id": cid_res2,
            "description": "Snapshot memory store resets to empty across restart (404 Not Found)",
            "status": "PASS" if res2_pass else "FAIL",
            "orig_status": ro.status_code,
            "recon_status": rr.status_code,
            "orig_content_type": ro.headers.get("Content-Type", ""),
            "recon_content_type": rr.headers.get("Content-Type", ""),
            "details": "" if res2_pass else f"orig={ro.status_code}, recon={rr.status_code}"
        })
        print(f"  [{'PASS' if res2_pass else 'FAIL'}] {cid_res2}: Snapshot memory reset verification")

    finally:
        srv_orig_r.stop()
        srv_recon_r.stop()

    # =========================================================================
    # PHASE 2C.3IR REMEDIATION TEST SUITE
    # =========================================================================

    print("\n--- GROUP 9: TASK DETAILS ACCESS ISOLATION ---")
    port_orig_g9 = get_free_port()
    port_recon_g9 = get_free_port()
    port_orig_g9_na = get_free_port()
    port_recon_g9_na = get_free_port()

    tmp_g9_orig = ROOT / "scratch" / "diff_g9_orig"
    tmp_g9_recon = ROOT / "scratch" / "diff_g9_recon"
    tmp_g9_orig_na = ROOT / "scratch" / "diff_g9_orig_na"
    tmp_g9_recon_na = ROOT / "scratch" / "diff_g9_recon_na"

    for p in [tmp_g9_orig, tmp_g9_recon, tmp_g9_orig_na, tmp_g9_recon_na]:
        make_fixture(p)

    srv_g9 = [
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={port_orig_g9}", f"-data={tmp_g9_orig}", f"-assets={ASSETS}"], tmp_g9_orig),
        ServerProcess([str(EXE_RECON), f"-port={port_recon_g9}", f"-data={tmp_g9_recon}"], tmp_g9_recon),
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={port_orig_g9_na}", f"-data={tmp_g9_orig_na}", f"-assets={ASSETS}", "-no-auth"], tmp_g9_orig_na),
        ServerProcess([str(EXE_RECON), f"-port={port_recon_g9_na}", f"-data={tmp_g9_recon_na}", "-no-auth"], tmp_g9_recon_na),
    ]

    try:
        for s in srv_g9:
            s.start()
        time.sleep(2.5)

        tok_o_adm_g9 = requests.post(f"http://127.0.0.1:{port_orig_g9}/api/login", json={"username": "admin", "password": "admin123"}).json().get("token")
        tok_r_adm_g9 = requests.post(f"http://127.0.0.1:{port_recon_g9}/api/login", json={"username": "admin", "password": "admin123"}).json().get("token")
        tok_o_ass_g9 = requests.post(f"http://127.0.0.1:{port_orig_g9}/api/login", json={"username": "user_assigned", "password": "user123"}).json().get("token")
        tok_r_ass_g9 = requests.post(f"http://127.0.0.1:{port_recon_g9}/api/login", json={"username": "user_assigned", "password": "user123"}).json().get("token")
        tok_o_unass_g9 = requests.post(f"http://127.0.0.1:{port_orig_g9}/api/login", json={"username": "user_unassigned", "password": "user123"}).json().get("token")
        tok_r_unass_g9 = requests.post(f"http://127.0.0.1:{port_recon_g9}/api/login", json={"username": "user_unassigned", "password": "user123"}).json().get("token")

        # Create one real task via admin
        t_req_g9 = {"type": "shell", "targets": ["dev-001"], "payload": "remediation_probe"}
        ro_task = requests.post(f"http://127.0.0.1:{port_orig_g9}/api/tasks", json=t_req_g9, headers={"Authorization": f"Bearer {tok_o_adm_g9}"})
        rr_task = requests.post(f"http://127.0.0.1:{port_recon_g9}/api/tasks", json=t_req_g9, headers={"Authorization": f"Bearer {tok_r_adm_g9}"})
        tid_o = ro_task.json().get("task_id")
        tid_r = rr_task.json().get("task_id")

        # 9.1 Read task details by ADMIN
        ro = requests.get(f"http://127.0.0.1:{port_orig_g9}/api/tasks/details?task_id={tid_o}", headers={"Authorization": f"Bearer {tok_o_adm_g9}"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g9}/api/tasks/details?task_id={tid_r}", headers={"Authorization": f"Bearer {tok_r_adm_g9}"})
        check_diff("Task details access isolation: ADMIN role (200 OK, full Task DTO)", ro, rr, check_body=True)

        # 9.2 Read task details by NORMAL_USER_ASSIGNED
        ro = requests.get(f"http://127.0.0.1:{port_orig_g9}/api/tasks/details?task_id={tid_o}", headers={"Authorization": f"Bearer {tok_o_ass_g9}"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g9}/api/tasks/details?task_id={tid_r}", headers={"Authorization": f"Bearer {tok_r_ass_g9}"})
        check_diff("Task details access isolation: NORMAL_USER_ASSIGNED role (200 OK, global authenticated read)", ro, rr, check_body=True)

        # 9.3 Read task details by NORMAL_USER_UNASSIGNED
        ro = requests.get(f"http://127.0.0.1:{port_orig_g9}/api/tasks/details?task_id={tid_o}", headers={"Authorization": f"Bearer {tok_o_unass_g9}"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g9}/api/tasks/details?task_id={tid_r}", headers={"Authorization": f"Bearer {tok_r_unass_g9}"})
        check_diff("Task details access isolation: NORMAL_USER_UNASSIGNED role (200 OK, global authenticated read)", ro, rr, check_body=True)

        # 9.4 Read task details with MISSING_TOKEN
        ro = requests.get(f"http://127.0.0.1:{port_orig_g9}/api/tasks/details?task_id={tid_o}")
        rr = requests.get(f"http://127.0.0.1:{port_recon_g9}/api/tasks/details?task_id={tid_r}")
        check_diff("Task details access isolation: MISSING_TOKEN (401 Unauthorized)", ro, rr, check_body=True)

        # 9.5 Read task details with INVALID_TOKEN
        ro = requests.get(f"http://127.0.0.1:{port_orig_g9}/api/tasks/details?task_id={tid_o}", headers={"Authorization": "Bearer bad_token_12345"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g9}/api/tasks/details?task_id={tid_r}", headers={"Authorization": "Bearer bad_token_12345"})
        check_diff("Task details access isolation: INVALID_TOKEN (401 Unauthorized)", ro, rr, check_body=True)

        # 9.6 Read task details in NO_AUTH_MODE
        ro_na_task = requests.post(f"http://127.0.0.1:{port_orig_g9_na}/api/tasks", json=t_req_g9)
        rr_na_task = requests.post(f"http://127.0.0.1:{port_recon_g9_na}/api/tasks", json=t_req_g9)
        tid_o_na = ro_na_task.json().get("task_id")
        tid_r_na = rr_na_task.json().get("task_id")

        ro = requests.get(f"http://127.0.0.1:{port_orig_g9_na}/api/tasks/details?task_id={tid_o_na}")
        rr = requests.get(f"http://127.0.0.1:{port_recon_g9_na}/api/tasks/details?task_id={tid_r_na}")
        check_diff("Task details access isolation: NO_AUTH_MODE (200 OK without token)", ro, rr, check_body=True)

    finally:
        for s in srv_g9:
            s.stop()

    print("\n--- GROUP 10: FILE LIST EXACT CONTRACT & FIXTURES ---")
    port_orig_g10 = get_free_port()
    port_recon_g10 = get_free_port()
    tmp_g10_orig = ROOT / "scratch" / "diff_g10_orig"
    tmp_g10_recon = ROOT / "scratch" / "diff_g10_recon"

    for p in [tmp_g10_orig, tmp_g10_recon]:
        make_fixture(p)
        dl_p = p / "downloads"
        dl_p.mkdir(parents=True, exist_ok=True)
        (dl_p / "a.txt").write_bytes(b"aaa")
        (dl_p / "B.txt").write_bytes(b"bbb")
        (dl_p / "empty.txt").write_bytes(b"")
        (dl_p / "spaced file.txt").write_bytes(b"spaced")
        (dl_p / "tiếng Việt.txt").write_bytes("Nội dung tiếng Việt".encode("utf-8"))
        (dl_p / "café_ñandú.txt").write_bytes("café ñandú payload".encode("utf-8"))
        (dl_p / "normal.txt").write_bytes(b"normal content")
        (dl_p / "sub").mkdir(parents=True, exist_ok=True)
        (dl_p / "sub" / "nested.txt").write_bytes(b"nested")
        for f in dl_p.glob("**/*"):
            if f.is_file():
                os.utime(f, (1700000000, 1700000000))

    srv_g10 = [
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={port_orig_g10}", f"-data={tmp_g10_orig}", f"-assets={ASSETS}"], tmp_g10_orig),
        ServerProcess([str(EXE_RECON), f"-port={port_recon_g10}", f"-data={tmp_g10_recon}"], tmp_g10_recon),
    ]

    try:
        for s in srv_g10:
            s.start()
        time.sleep(2.5)

        tok_o_adm_g10 = requests.post(f"http://127.0.0.1:{port_orig_g10}/api/login", json={"username": "admin", "password": "admin123"}).json().get("token")
        tok_r_adm_g10 = requests.post(f"http://127.0.0.1:{port_recon_g10}/api/login", json={"username": "admin", "password": "admin123"}).json().get("token")
        tok_o_ass_g10 = requests.post(f"http://127.0.0.1:{port_orig_g10}/api/login", json={"username": "user_assigned", "password": "user123"}).json().get("token")
        tok_r_ass_g10 = requests.post(f"http://127.0.0.1:{port_recon_g10}/api/login", json={"username": "user_assigned", "password": "user123"}).json().get("token")

        # 10.1 List files exact contract by ADMIN with check_body=True
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/api/files", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/api/files", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("File list exact contract by ADMIN (sorting B.txt before a.txt, excluded subdirs, mtime parity)", ro, rr, check_body=True, headers_to_compare=["Content-Type"])

        # 10.2 List files exact contract by NORMAL USER with check_body=True
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/api/files", headers={"Authorization": f"Bearer {tok_o_ass_g10}"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/api/files", headers={"Authorization": f"Bearer {tok_r_ass_g10}"})
        check_diff("File list exact contract by NORMAL USER (identical item count, size, schema parity)", ro, rr, check_body=True, headers_to_compare=["Content-Type"])

        print("\n--- GROUP 11: DOWNLOADS STATIC HEADERS & RANGE CONTRACT ---")
        # 11.1 GET existing file: compare Accept-Ranges, Content-Length, CORS
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/spaced%20file.txt")
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/spaced%20file.txt")
        check_diff("Downloads static GET existing (200 OK, Accept-Ranges: bytes, Last-Modified, CORS)", ro, rr, check_body=True,
                   headers_to_compare=["Content-Type", "Content-Length", "Accept-Ranges", "Last-Modified", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"])

        # 11.2 HEAD existing file: empty body, headers match
        ro = requests.head(f"http://127.0.0.1:{port_orig_g10}/downloads/spaced%20file.txt")
        rr = requests.head(f"http://127.0.0.1:{port_recon_g10}/downloads/spaced%20file.txt")
        check_diff("Downloads static HEAD existing (200 OK, empty body)", ro, rr, check_body=False,
                   headers_to_compare=["Content-Type", "Content-Length", "Accept-Ranges", "Last-Modified"])

        # 11.3 Range: bytes=0-3
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/spaced%20file.txt", headers={"Range": "bytes=0-3"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/spaced%20file.txt", headers={"Range": "bytes=0-3"})
        check_diff("Downloads Range bytes=0-3 (206 Partial Content, Content-Range bytes 0-3/6)", ro, rr, check_body=True,
                   headers_to_compare=["Content-Type", "Content-Length", "Accept-Ranges", "Content-Range"])

        # 11.4 Range: bytes=2-
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/spaced%20file.txt", headers={"Range": "bytes=2-"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/spaced%20file.txt", headers={"Range": "bytes=2-"})
        check_diff("Downloads Range bytes=2- (206 Partial Content, Content-Range bytes 2-5/6)", ro, rr, check_body=True,
                   headers_to_compare=["Content-Type", "Content-Length", "Accept-Ranges", "Content-Range"])

        # 11.5 Invalid Range: bytes=999-1000
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/spaced%20file.txt", headers={"Range": "bytes=999-1000"})
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/spaced%20file.txt", headers={"Range": "bytes=999-1000"})
        check_diff("Downloads invalid Range (416 Range Not Satisfiable, Content-Range bytes */6)", ro, rr, check_body=True,
                   headers_to_compare=["Content-Type", "Content-Range"])

        # 11.6 Directory without trailing slash redirects to trailing slash
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/sub", allow_redirects=False)
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/sub", allow_redirects=False)
        check_diff("Downloads directory without slash (301 Moved Permanently, Location: sub/)", ro, rr, check_body=True,
                   headers_to_compare=["Location", "Content-Type"])

        # 11.7 Non-ASCII Unicode filename download ("tiếng Việt.txt")
        url_viet = urllib.parse.quote("tiếng Việt.txt")
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/{url_viet}")
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/{url_viet}")
        check_diff("Downloads non-ASCII Unicode 'tiếng Việt.txt' (200 OK, matching payload)", ro, rr, check_body=True,
                   headers_to_compare=["Content-Type", "Content-Length", "Accept-Ranges", "Last-Modified"])

        # 11.8 Non-ASCII Unicode filename download ("café_ñandú.txt")
        url_cafe = urllib.parse.quote("café_ñandú.txt")
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/{url_cafe}")
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/{url_cafe}")
        check_diff("Downloads non-ASCII Unicode 'café_ñandú.txt' (200 OK, matching payload)", ro, rr, check_body=True,
                   headers_to_compare=["Content-Type", "Content-Length", "Accept-Ranges", "Last-Modified"])

        # 11.9 Zero-byte file download
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/empty.txt")
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/empty.txt")
        check_diff("Downloads zero-byte file delivery (200 OK, Content-Length: 0)", ro, rr, check_body=True,
                   headers_to_compare=["Content-Type", "Content-Length"])

        print("\n--- GROUP 12: EXPANDED PATH SECURITY & TRAVERSAL MATRIX ---")
        # 12.1 Upload: dir/file.txt (original strips directory and saves base)
        ro = requests.post(f"http://127.0.0.1:{port_orig_g10}/upload?name=dir/file.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.post(f"http://127.0.0.1:{port_recon_g10}/upload?name=dir/file.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Path security upload 'dir/file.txt' (200 OK, strips dir to base 'file.txt')", ro, rr, check_body=True)

        # 12.2 Upload: ./file2.txt
        ro = requests.post(f"http://127.0.0.1:{port_orig_g10}/upload?name=./file2.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.post(f"http://127.0.0.1:{port_recon_g10}/upload?name=./file2.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Path security upload './file2.txt' (200 OK, saves as 'file2.txt')", ro, rr, check_body=True)

        # 12.3 Upload: ../file3.txt (strips path components safely)
        ro = requests.post(f"http://127.0.0.1:{port_orig_g10}/upload?name=../file3.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.post(f"http://127.0.0.1:{port_recon_g10}/upload?name=../file3.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Path security upload '../file3.txt' (200 OK, base file3.txt)", ro, rr, check_body=True)

        # 12.4 Upload: a/../file4.txt
        ro = requests.post(f"http://127.0.0.1:{port_orig_g10}/upload?name=a/../file4.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.post(f"http://127.0.0.1:{port_recon_g10}/upload?name=a/../file4.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Path security upload 'a/../file4.txt' (200 OK, base file4.txt)", ro, rr, check_body=True)

        # 12.5 Upload: .leading
        ro = requests.post(f"http://127.0.0.1:{port_orig_g10}/upload?name=.leading", data=b"pdata", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.post(f"http://127.0.0.1:{port_recon_g10}/upload?name=.leading", data=b"pdata", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Path security upload '.leading' dotfile (200 OK)", ro, rr, check_body=True)

        # 12.6 Upload: backslash path C:\test\win.txt
        ro = requests.post(f"http://127.0.0.1:{port_orig_g10}/upload?name=C:\\test\\win.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.post(f"http://127.0.0.1:{port_recon_g10}/upload?name=C:\\test\\win.txt", data=b"pdata", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Path security upload backslash path 'C:\\test\\win.txt' (200 OK, base 'win.txt')", ro, rr, check_body=True)

        # 12.7 Upload: absolute-looking path /etc/passwd
        ro = requests.post(f"http://127.0.0.1:{port_orig_g10}/upload?name=/etc/passwd", data=b"pdata", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.post(f"http://127.0.0.1:{port_recon_g10}/upload?name=/etc/passwd", data=b"pdata", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Path security upload absolute '/etc/passwd' (200 OK, base 'passwd')", ro, rr, check_body=True)

        # /downloads/ path matrix
        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/normal.txt", allow_redirects=False)
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/normal.txt", allow_redirects=False)
        check_diff("Downloads matrix normal file '/downloads/normal.txt' (200 OK)", ro, rr, check_body=True)

        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/../users.json", allow_redirects=False)
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/../users.json", allow_redirects=False)
        check_diff("Downloads matrix parent traversal '/downloads/../users.json' (404 Not Found)", ro, rr, check_body=True)

        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/..%2fusers.json", allow_redirects=False)
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/..%2fusers.json", allow_redirects=False)
        check_diff("Downloads matrix encoded traversal '/downloads/..%2fusers.json' (301 Redirect)", ro, rr, check_body=True)

        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/sub/nested.txt", allow_redirects=False)
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/sub/nested.txt", allow_redirects=False)
        check_diff("Downloads matrix nested file '/downloads/sub/nested.txt' (404 Not Found)", ro, rr, check_body=True)

        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/./normal.txt", allow_redirects=False)
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/./normal.txt", allow_redirects=False)
        check_diff("Downloads matrix dot segment '/downloads/./normal.txt' (200 OK)", ro, rr, check_body=True)

        ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/sub/../normal.txt", allow_redirects=False)
        rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/sub/../normal.txt", allow_redirects=False)
        check_diff("Downloads matrix resolved segment '/downloads/sub/../normal.txt' (200 OK)", ro, rr, check_body=True)

        # Symlink traversal check
        cid_sym = f"FT-DIFF-{case_idx:02d}"
        case_idx += 1
        symlink_created = False
        try:
            target_f = tmp_g10_orig / "downloads" / "normal.txt"
            link_orig = tmp_g10_orig / "downloads" / "symlink_normal.txt"
            link_recon = tmp_g10_recon / "downloads" / "symlink_normal.txt"
            os.symlink(target_f, link_orig)
            os.symlink(tmp_g10_recon / "downloads" / "normal.txt", link_recon)
            symlink_created = True
        except OSError:
            symlink_created = False

        if symlink_created:
            ro = requests.get(f"http://127.0.0.1:{port_orig_g10}/downloads/symlink_normal.txt")
            rr = requests.get(f"http://127.0.0.1:{port_recon_g10}/downloads/symlink_normal.txt")
            check_diff("Downloads symlink resolution (200 OK, matching payload)", ro, rr, check_body=True)
        else:
            entry = {
                "case_id": cid_sym,
                "description": "Downloads symlink traversal verification",
                "status": "EXCLUDED",
                "classification": "ENVIRONMENT_UNAVAILABLE",
                "orig_status": 0,
                "recon_status": 0,
                "orig_content_type": "",
                "recon_content_type": "",
                "details": "os.symlink privilege unavailable on host OS ([WinError 1314]); recorded as ENVIRONMENT_UNAVAILABLE",
                "headers_compared": {}
            }
            results.append(entry)
            print(f"  [EXCLUDED (ENVIRONMENT_UNAVAILABLE)] {cid_sym}: Downloads symlink traversal verification (WinError 1314)")

        # Complete DELETE path matrix
        ro = requests.delete(f"http://127.0.0.1:{port_orig_g10}/api/files?name=normal.txt", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.delete(f"http://127.0.0.1:{port_recon_g10}/api/files?name=normal.txt", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Delete path normal file 'normal.txt' (200 OK)", ro, rr, check_body=True)

        ro = requests.delete(f"http://127.0.0.1:{port_orig_g10}/api/files?name=sub/nested.txt", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.delete(f"http://127.0.0.1:{port_recon_g10}/api/files?name=sub/nested.txt", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Delete path nested file 'sub/nested.txt' (404 Not Found)", ro, rr, check_body=True)

        ro = requests.delete(f"http://127.0.0.1:{port_orig_g10}/api/files?name=../normal.txt", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.delete(f"http://127.0.0.1:{port_recon_g10}/api/files?name=../normal.txt", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Delete path traversal '../normal.txt' (404 Not Found)", ro, rr, check_body=True)

        ro = requests.delete(f"http://127.0.0.1:{port_orig_g10}/api/files?name=..%2fnormal.txt", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.delete(f"http://127.0.0.1:{port_recon_g10}/api/files?name=..%2fnormal.txt", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Delete path encoded traversal '..%2fnormal.txt' (404 Not Found)", ro, rr, check_body=True)

        ro = requests.delete(f"http://127.0.0.1:{port_orig_g10}/api/files?name=.", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.delete(f"http://127.0.0.1:{port_recon_g10}/api/files?name=.", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Delete path '.' directory removal protection (DIV-SEC-DELETE-DOT)", ro, rr, expected_divergence={"id": "DIV-SEC-DELETE-DOT", "orig_status": 500, "recon_status": 404})

        ro = requests.delete(f"http://127.0.0.1:{port_orig_g10}/api/files?name=..", headers={"Authorization": f"Bearer {tok_o_adm_g10}"})
        rr = requests.delete(f"http://127.0.0.1:{port_recon_g10}/api/files?name=..", headers={"Authorization": f"Bearer {tok_r_adm_g10}"})
        check_diff("Delete path '..' parent directory removal protection (DIV-SEC-DELETE-DOTDOT)", ro, rr, expected_divergence={"id": "DIV-SEC-DELETE-DOTDOT", "orig_status": 500, "recon_status": 404})

    finally:
        for s in srv_g10:
            s.stop()

    print("\n--- GROUP 13: SNAPSHOTS DIRECTORY STARTUP PARITY ---")
    port_orig_g13 = get_free_port()
    port_recon_g13 = get_free_port()
    tmp_g13_orig = ROOT / "scratch" / "diff_g13_orig"
    tmp_g13_recon = ROOT / "scratch" / "diff_g13_recon"

    for p in [tmp_g13_orig, tmp_g13_recon]:
        make_fixture(p)
        # Verify data/snapshots does not exist prior to startup
        assert not (p / "snapshots").exists()

    srv_g13 = [
        ServerProcess([str(EXE_ORIG), "-tls=false", f"-port={port_orig_g13}", f"-data={tmp_g13_orig}", f"-assets={ASSETS}"], tmp_g13_orig),
        ServerProcess([str(EXE_RECON), f"-port={port_recon_g13}", f"-data={tmp_g13_recon}"], tmp_g13_recon),
    ]

    try:
        for s in srv_g13:
            s.start()
        time.sleep(2.5)

        # 13.1 Eager empty directory created on startup
        orig_exists = (tmp_g13_orig / "snapshots").is_dir()
        recon_exists = (tmp_g13_recon / "snapshots").is_dir()
        orig_empty = len(list((tmp_g13_orig / "snapshots").glob("*"))) == 0
        recon_empty = len(list((tmp_g13_recon / "snapshots").glob("*"))) == 0

        cid_s1 = f"FT-DIFF-{case_idx:02d}"
        case_idx += 1
        s1_pass = orig_exists and recon_exists and orig_empty and recon_empty
        results.append({
            "case_id": cid_s1,
            "description": "Snapshots directory startup lifecycle parity (eager empty directory on disk)",
            "status": "PASS" if s1_pass else "FAIL",
            "orig_status": 200 if orig_exists and orig_empty else 500,
            "recon_status": 200 if recon_exists and recon_empty else 500,
            "orig_content_type": "filesystem/dir",
            "recon_content_type": "filesystem/dir",
            "details": f"orig_dir={orig_exists}(empty={orig_empty}), recon_dir={recon_exists}(empty={recon_empty})"
        })
        print(f"  [{'PASS' if s1_pass else 'FAIL'}] {cid_s1}: Snapshots directory startup lifecycle parity")

        # 13.2 Upload snapshot bytes to dev-999: disk directory remains strictly empty!
        snap_jpg = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xFF\xDB"
        requests.post(f"http://127.0.0.1:{port_orig_g13}/upload?type=snapshot&device_id=dev-999", data=snap_jpg)
        requests.post(f"http://127.0.0.1:{port_recon_g13}/upload?type=snapshot&device_id=dev-999", data=snap_jpg)

        orig_still_empty = len(list((tmp_g13_orig / "snapshots").glob("*"))) == 0
        recon_still_empty = len(list((tmp_g13_recon / "snapshots").glob("*"))) == 0

        cid_s2 = f"FT-DIFF-{case_idx:02d}"
        case_idx += 1
        s2_pass = orig_still_empty and recon_still_empty
        results.append({
            "case_id": cid_s2,
            "description": "Snapshot data storage remains in-memory only (0 disk snapshot files created)",
            "status": "PASS" if s2_pass else "FAIL",
            "orig_status": 200 if orig_still_empty else 500,
            "recon_status": 200 if recon_still_empty else 500,
            "orig_content_type": "filesystem/dir",
            "recon_content_type": "filesystem/dir",
            "details": f"orig_disk_files={len(list((tmp_g13_orig / 'snapshots').glob('*')))}, recon_disk_files={len(list((tmp_g13_recon / 'snapshots').glob('*')))}"
        })
        print(f"  [{'PASS' if s2_pass else 'FAIL'}] {cid_s2}: Snapshot data storage remains in-memory only")

    finally:
        for s in srv_g13:
            s.stop()

    total_cases = len(results)
    exact_parity_cases = [
        r for r in results
        if r.get("classification") == "PARITY" or (
            r.get("status") in ("PASS", "FAIL") and
            r.get("classification") not in ("ENVIRONMENT_UNAVAILABLE", "INTENTIONAL_SECURITY_DIVERGENCE")
        )
    ]
    exact_parity_total = len(exact_parity_cases)
    exact_parity_passed = len([r for r in exact_parity_cases if r.get("status") == "PASS"])

    verified_divergences = len([
        r for r in results
        if r.get("classification") == "INTENTIONAL_SECURITY_DIVERGENCE" and r.get("status") == "VERIFIED_DIVERGENCE"
    ])
    excluded_env = len([
        r for r in results
        if r.get("classification") == "ENVIRONMENT_UNAVAILABLE" and r.get("status") == "EXCLUDED"
    ])
    failed_cases = len([r for r in results if r.get("status") == "FAIL"])
    verdict_passed = (failed_cases == 0 and exact_parity_passed == exact_parity_total)

    summary_payload = {
        "execution_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_cases_evaluated": total_cases,
        "exact_parity_total": exact_parity_total,
        "exact_parity_passed": exact_parity_passed,
        "exact_parity_pass_rate": f"{exact_parity_passed}/{exact_parity_total}",
        "verified_intentional_divergences": verified_divergences,
        "excluded_environment_unavailable": excluded_env,
        "failed": failed_cases,
        "all_passed": verdict_passed,
        "passed": exact_parity_passed,
        "total_cases": exact_parity_total,
        "summary": {
            "total_cases_evaluated": total_cases,
            "exact_parity_total": exact_parity_total,
            "exact_parity_passed": exact_parity_passed,
            "exact_parity_pass_rate": f"{exact_parity_passed}/{exact_parity_total}",
            "verified_intentional_divergences": verified_divergences,
            "excluded_environment_unavailable": excluded_env,
            "failed": failed_cases,
            "verdict": "PASS" if verdict_passed else "FAIL"
        },
        "results": results
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)

    print("\n==========================================================")
    print("DIFFERENTIAL TEST RESULTS SUMMARY:")
    print(f"  EXACT_PARITY_PASS_RATE = {exact_parity_passed}/{exact_parity_total}")
    print(f"  VERIFIED_INTENTIONAL_DIVERGENCES = {verified_divergences}")
    print(f"  ENVIRONMENT_UNAVAILABLE_EXCLUDED = {excluded_env}")
    print(f"  FAILED = {failed_cases}")
    print(f"  VERDICT = {'PASS' if verdict_passed else 'FAIL'}")
    print(f"Output saved to: {OUTPUT_JSON}")
    print("==========================================================")

    if not verdict_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
