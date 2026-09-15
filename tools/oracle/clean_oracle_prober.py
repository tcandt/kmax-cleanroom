import os
import sys
import subprocess
import time
import requests
import json
import shutil
import hashlib
from pathlib import Path

# Add repo root to sys.path portably
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root

ROOT = get_repo_root()
EXE_WIN = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
EXE_LINUX = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
ASSETS = ROOT / "cloudphone-v0.3.6 (1)" / "assets"

FIXTURES_DIR = ROOT / "tools" / "oracle" / "fixtures"
OUTPUT_JSON = ROOT / "raw_extraction" / "go_signaling" / "clean_oracle_results.json"

PORT = 28448
BASE_URL = f"http://127.0.0.1:{PORT}"

PROBE_ROUTES = [
    # Registered routes in main.main
    "/api/tags",
    "/api/shortcuts",
    "/api/auth-status",
    "/api/activate",
    "/api/license_status",
    "/debug/license",
    "/api/login",
    "/api/register",
    "/api/me",
    "/api/user/ai-config",
    "/api/admin/users",
    "/api/admin/users/rename",
    "/api/admin/assign",
    "/api/admin/users/create",
    "/api/admin/users/delete",
    "/api/admin/users/update_note",
    "/api/admin/users/update",
    "/api/admin/users/reset_password",
    "/api/admin/users/kick",
    "/api/share/create",
    "/api/share/list",
    "/api/share/revoke",
    "/api/share/extend",
    "/api/share/update",
    "/api/share/info",
    "/api/share/redeem_card",
    "/api/server/addresses",
    "/register_device",
    "/register_agent",
    "/connect_client",
    "/devices",
    "/api/devices/",
    "/api/devices",
    "/upload",
    "/api/files",
    "/api/tasks",
    "/api/tasks/details",
    "/api/default_settings",
    "/api/ice_servers",
    "/api/version",
    "/snapshots/",
    "/",
    # Static String Candidates (not registered in main.main)
    "/api/turn",
    "/api/devices/list",
    "/api/admin/users/register_device",
    "/downloads",
    "/debug/pprof",
    "/debug/pprof/cmdline",
    "/debug/pprof/profile",
    "/debug/pprof/symbol",
    "/debug/pprof/trace",
    # Strictly LAST
    "/api/logout"
]

STATIC_REGISTERED_SET = {
    "/api/tags", "/api/shortcuts", "/api/auth-status", "/api/activate", "/api/license_status",
    "/debug/license", "/api/login", "/api/register", "/api/me", "/api/user/ai-config",
    "/api/logout", "/api/admin/users", "/api/admin/users/rename", "/api/admin/assign",
    "/api/admin/users/create", "/api/admin/users/delete", "/api/admin/users/update_note",
    "/api/admin/users/update", "/api/admin/users/reset_password", "/api/admin/users/kick",
    "/api/share/create", "/api/share/list", "/api/share/revoke", "/api/share/extend",
    "/api/share/update", "/api/share/info", "/api/share/redeem_card", "/api/server/addresses",
    "/register_device", "/register_agent", "/connect_client", "/devices", "/api/devices/",
    "/upload", "/api/files", "/api/tasks", "/api/tasks/details", "/api/default_settings",
    "/api/ice_servers", "/api/version", "/snapshots/", "/"
}

def get_fresh_token(username, password):
    try:
        r = requests.post(f"{BASE_URL}/api/login", json={"username": username, "password": password}, timeout=2)
        if r.status_code == 200:
            return r.json().get("token")
    except Exception as e:
        print(f"[-] Login error for {username}: {e}")
    return None

def infer_schema(r):
    ct = r.headers.get("Content-Type", "")
    if "application/json" in ct:
        try:
            val = r.json()
            if isinstance(val, dict):
                return "json_object"
            elif isinstance(val, list):
                return "json_array"
            return "json_primitive"
        except:
            return "malformed_json"
    elif "text/html" in ct:
        return "text_html"
    elif "text/plain" in ct:
        return "text_plain"
    elif len(r.content) == 0:
        return "empty"
    return "binary_or_other"

def run_prober(temp_data_dir: Path):
    exe = EXE_WIN if os.name == "nt" else EXE_LINUX
    if not exe.exists():
        raise FileNotFoundError(f"Signaling binary not found: {exe}")

    temp_data_dir.mkdir(parents=True, exist_ok=True)

    def restore_fixture():
        for f in FIXTURES_DIR.glob("*.json"):
            shutil.copy2(f, temp_data_dir / f.name)

    restore_fixture()

    proc = subprocess.Popen([
        str(exe), "-tls=false", f"-port={PORT}", f"-data={temp_data_dir}", f"-assets={ASSETS}", "-debug"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    time.sleep(1.8)

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
    results = {}

    try:
        print("[*] Running Clean Dynamic Oracle Suite...")
        fixture_counter = 0

        for route in PROBE_ROUTES:
            route_results = {
                "route": route,
                "methods": {},
                "auth_matrix": {},
                "classification": "UNKNOWN_ROUTE_STATUS"
            }

            is_state_mutating = any(k in route for k in ["create", "delete", "rename", "revoke", "update", "reset", "kick", "assign"])
            test_method = "POST" if any(k in route for k in ["create", "delete", "login", "register", "activate"]) else "GET"

            # 1. Auth Matrix
            auth_cases = [
                ("NO_AUTH", None),
                ("INVALID_TOKEN", "invalid_deadbeef_token_9999"),
                ("VALID_USER_TOKEN", ("user1", "user123")),
                ("VALID_ADMIN_TOKEN", ("admin", "admin123"))
            ]

            for auth_name, creds in auth_cases:
                if is_state_mutating:
                    restore_fixture()
                    fixture_counter += 1

                headers = {}
                if creds:
                    if isinstance(creds, tuple):
                        fresh_tok = get_fresh_token(creds[0], creds[1])
                        if fresh_tok:
                            headers["Authorization"] = f"Bearer {fresh_tok}"
                    else:
                        headers["Authorization"] = f"Bearer {creds}"

                req_fn = getattr(requests, test_method.lower())
                try:
                    r = req_fn(f"{BASE_URL}{route}", headers=headers, timeout=2)
                    route_results["auth_matrix"][auth_name] = {
                        "method": test_method,
                        "status": r.status_code,
                        "body_preview": r.text[:120].strip()
                    }
                except Exception as e:
                    route_results["auth_matrix"][auth_name] = {"error": str(e)}

            # 2. Method Matrix
            any_non_404 = False
            allow_header = None

            for m in methods:
                if is_state_mutating:
                    restore_fixture()
                    fixture_counter += 1

                fresh_admin_token = get_fresh_token("admin", "admin123")
                headers = {
                    "Authorization": f"Bearer {fresh_admin_token}",
                    "Content-Type": "application/json"
                }

                req_fn = getattr(requests, m.lower())
                try:
                    r = req_fn(f"{BASE_URL}{route}", headers=headers, timeout=2)
                    body_hash = hashlib.sha256(r.content).hexdigest()
                    schema = infer_schema(r)
                    if r.status_code != 404:
                        any_non_404 = True
                    if "Allow" in r.headers:
                        allow_header = r.headers["Allow"]

                    route_results["methods"][m] = {
                        "status": r.status_code,
                        "content_type": r.headers.get("Content-Type", ""),
                        "allow": r.headers.get("Allow"),
                        "body_hash": body_hash,
                        "schema": schema,
                        "fixture_id": f"fx_{fixture_counter}"
                    }
                except Exception as e:
                    route_results["methods"][m] = {"error": str(e)}

            # 3. Route Classification
            is_static_reg = (route in STATIC_REGISTERED_SET) or (route + "/" in STATIC_REGISTERED_SET) or (route.rstrip("/") in STATIC_REGISTERED_SET)

            if is_static_reg and any_non_404:
                route_results["classification"] = "STATIC_AND_DYNAMIC_REGISTERED"
            elif is_static_reg and not any_non_404:
                route_results["classification"] = "STATIC_REGISTERED_ROUTE"
            elif not is_static_reg and not any_non_404:
                route_results["classification"] = "STATIC_STRING_CANDIDATE / NOT_RUNTIME_REGISTERED"
            elif not is_static_reg and any_non_404:
                route_results["classification"] = "DYNAMIC_REGISTERED_ROUTE"
            else:
                route_results["classification"] = "UNKNOWN_ROUTE_STATUS"

            route_results["allow_header"] = allow_header
            results[route] = route_results

        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        print(f"[+] Successfully wrote verified oracle results to {OUTPUT_JSON}")
        return results

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except:
            proc.kill()

if __name__ == "__main__":
    temp_dir = ROOT / "tmp" / "clean_oracle_run"
    run_prober(temp_dir)
