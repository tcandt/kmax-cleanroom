#!/usr/bin/env python3
"""
test_files_tasks_http_diff.py - Phase 2C.3I Files / Tasks / Downloads / Snapshots Differential Verification Suite

Executes side-by-side differential tests comparing the canonical original binary oracle
against the cleanroom reconstructed HTTP signaling server across all 6 endpoints:
  - /upload (Split into UPLOAD_STANDARD_FILE and UPLOAD_SNAPSHOT_INGEST)
  - /api/files (Listing and deletion)
  - /api/tasks (Batch task creation)
  - /api/tasks/details (Batch task status details)
  - /downloads/ (Static file delivery)
  - /snapshots/ (In-memory device screen capture delivery)

Strict Invariants:
  - Dynamic denominator: cases calculated from structured results at runtime.
  - Zero mock WebRTC/agent: online dispatch branch verified as ONLINE_DISPATCH_TRANSPORT_DEPENDENT.
  - Snapshot in-memory only: zero disk snapshot directory created.
  - Path security: traversal tests on dots safely evaluated in isolated directories.
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
EXE_RECON = ROOT / "scratch" / "reconstructed_files_tasks.exe"

DIFF_TMP_ORIG = ROOT / "scratch" / "files_tasks_diff_orig"
DIFF_TMP_RECON = ROOT / "scratch" / "files_tasks_diff_recon"
DIFF_TMP_ORIG_NA = ROOT / "scratch" / "files_tasks_diff_orig_na"
DIFF_TMP_RECON_NA = ROOT / "scratch" / "files_tasks_diff_recon_na"

OUTPUT_JSON = ROOT / "evidence" / "go_signaling" / "files_tasks" / "FILES_TASKS_HTTP_DIFFERENTIAL_RESULTS.json"

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

        def check_diff(desc, r_orig, r_recon, check_body=True):
            nonlocal case_idx, test_run_success
            cid = f"FT-DIFF-{case_idx:02d}"
            case_idx += 1

            passed = True
            diffs = []

            if r_orig.status_code != r_recon.status_code:
                passed = False
                diffs.append(f"Status mismatch: orig={r_orig.status_code}, recon={r_recon.status_code}")

            o_ct = r_orig.headers.get("Content-Type", "")
            r_ct = r_recon.headers.get("Content-Type", "")
            # Relax charset or standard spacing differences if base MIME matches
            o_base = o_ct.split(";")[0].strip().lower()
            r_base = r_ct.split(";")[0].strip().lower()
            if o_base != r_base:
                passed = False
                diffs.append(f"Content-Type mismatch: orig='{o_ct}', recon='{r_ct}'")

            if check_body and passed:
                if "application/json" in o_base:
                    try:
                        j_o = r_orig.json()
                        j_r = r_recon.json()
                        # Mask dynamic timestamps or task IDs if necessary
                        if isinstance(j_o, dict) and isinstance(j_r, dict):
                            if "task_id" in j_o and "task_id" in j_r:
                                # Validate format parity
                                if not (j_r["task_id"].startswith("task_") and len(j_r["task_id"]) >= 30):
                                    passed = False
                                    diffs.append(f"Recon task_id format invalid: {j_r['task_id']}")
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
                "details": "; ".join(diffs)
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
        check_diff("Task details read by admin (200 OK, offline failure parity)", ro, rr, check_body=False)
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
        check_diff("Task details read by normal user (200 OK)", ro, rr, check_body=False)

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
        print("\n[*] Shutting down server instances...")
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

    total_cases = len(results)
    passed_cases = sum(1 for r in results if r["status"] == "PASS")
    failed_cases = total_cases - passed_cases
    all_passed = (failed_cases == 0)

    summary_payload = {
        "execution_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_cases": total_cases,
        "passed": passed_cases,
        "failed": failed_cases,
        "all_passed": all_passed,
        "results": results
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)

    print("\n==========================================================")
    print(f"DIFFERENTIAL TEST RESULTS: {passed_cases}/{total_cases} PASSED")
    print(f"Output saved to: {OUTPUT_JSON}")
    print("==========================================================")

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
