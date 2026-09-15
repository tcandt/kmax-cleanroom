import os
import sys
import json
import time
import shutil
import hashlib
import subprocess
import requests
from pathlib import Path

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root

ROOT = get_repo_root()
EXE_ORIG = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
ASSETS = ROOT / "cloudphone-v0.3.6 (1)" / "assets"
TMP_DIR = ROOT / "tmp" / "auth_oracle_run"

def make_user_fixture(data_dir: Path, users: dict):
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "users.json").write_text(json.dumps(users, indent=2), encoding="utf-8")
    (data_dir / "device_tags.json").write_text(json.dumps({"tags": [], "deviceTags": {}}, indent=2), encoding="utf-8")

def run_server(data_dir: Path, port: int):
    cmd = [
        str(EXE_ORIG), "-tls=false", f"-port={port}", f"-data={data_dir}", f"-assets={ASSETS}", "-debug"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    time.sleep(1.8)
    return proc

def stop_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except:
        proc.kill()

def main():
    print("==================================================")
    print("PHASE 2C.2 AUTHENTICATION & SESSION ORACLE PROBER")
    print("==================================================")

    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True)

    salt_admin = "salt1234567890123456789012345678"
    pwd_admin = hashlib.sha256(("admin123" + salt_admin).encode()).hexdigest()

    salt_user = "usersalt123456789012345678901234"
    pwd_user = hashlib.sha256(("userpass" + salt_user).encode()).hexdigest()

    baseline_users = {
        "admin": {
            "username": "admin",
            "password": pwd_admin,
            "salt": salt_admin,
            "role": "admin",
            "assigned_devices": ["*"],
            "note": "",
            "forbid_bitrate": False,
            "forbid_fps": False,
            "forbid_resolution": False,
            "forbid_audio": False,
            "expires_at": "0001-01-01T00:00:00Z"
        },
        "testuser": {
            "username": "testuser",
            "password": pwd_user,
            "salt": salt_user,
            "role": "user",
            "assigned_devices": ["dev1"],
            "note": "regular test user",
            "forbid_bitrate": True,
            "forbid_fps": True,
            "forbid_resolution": False,
            "forbid_audio": False,
            "expires_at": "0001-01-01T00:00:00Z"
        },
        "expired_user": {
            "username": "expired_user",
            "password": pwd_user,
            "salt": salt_user,
            "role": "user",
            "assigned_devices": [],
            "note": "expired user account",
            "forbid_bitrate": False,
            "forbid_fps": False,
            "forbid_resolution": False,
            "forbid_audio": False,
            "expires_at": "2020-01-01T00:00:00Z"
        },
        "future_user": {
            "username": "future_user",
            "password": pwd_user,
            "salt": salt_user,
            "role": "user",
            "assigned_devices": [],
            "note": "future expiry account",
            "forbid_bitrate": False,
            "forbid_fps": False,
            "forbid_resolution": False,
            "forbid_audio": False,
            "expires_at": "2099-01-01T00:00:00Z"
        }
    }

    results = {}

    # ----------------------------------------------------
    # TEST MATRIX 1: Login Cases (2C.2D)
    # ----------------------------------------------------
    print("\n--- 1. Testing Login Payload Matrix ---")
    data_dir1 = TMP_DIR / "login_matrix"
    make_user_fixture(data_dir1, baseline_users)
    port1 = 29601
    p1 = run_server(data_dir1, port1)
    base_url1 = f"http://127.0.0.1:{port1}"

    login_cases = [
        ("VALID_ADMIN", {"username": "admin", "password": "admin123"}),
        ("VALID_REGULAR_USER", {"username": "testuser", "password": "userpass"}),
        ("INVALID_PASSWORD", {"username": "admin", "password": "wrongpassword"}),
        ("UNKNOWN_USER", {"username": "nonexistent", "password": "anypassword"}),
        ("EMPTY_USERNAME", {"username": "", "password": "admin123"}),
        ("EMPTY_PASSWORD", {"username": "admin", "password": ""}),
        ("MISSING_USERNAME", {"password": "admin123"}),
        ("MISSING_PASSWORD", {"username": "admin"}),
        ("PAST_EXPIRES_AT", {"username": "expired_user", "password": "userpass"}),
        ("FUTURE_EXPIRES_AT", {"username": "future_user", "password": "userpass"}),
    ]

    login_results = {}
    for case_name, payload in login_cases:
        r = requests.post(f"{base_url1}/api/login", json=payload, timeout=2)
        login_results[case_name] = {
            "status_code": r.status_code,
            "content_type": r.headers.get("Content-Type", ""),
            "body_raw": r.text,
            "is_json": "application/json" in r.headers.get("Content-Type", ""),
            "json_data": r.json() if "application/json" in r.headers.get("Content-Type", "") else None
        }
        print(f"  [{case_name}] Status: {r.status_code}, Body: {r.text[:80]}")

    # Test malformed JSON and wrong Content-Type
    r_malformed = requests.post(f"{base_url1}/api/login", data="{ malformed json", headers={"Content-Type": "application/json"}, timeout=2)
    login_results["MALFORMED_JSON"] = {"status_code": r_malformed.status_code, "body": r_malformed.text}
    print(f"  [MALFORMED_JSON] Status: {r_malformed.status_code}, Body: {r_malformed.text[:80]}")

    r_wrong_ct = requests.post(f"{base_url1}/api/login", data="username=admin&password=admin123", headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=2)
    login_results["WRONG_CONTENT_TYPE"] = {"status_code": r_wrong_ct.status_code, "body": r_wrong_ct.text}
    print(f"  [WRONG_CONTENT_TYPE] Status: {r_wrong_ct.status_code}, Body: {r_wrong_ct.text[:80]}")

    results["login_matrix"] = login_results

    # ----------------------------------------------------
    # TEST MATRIX 2: Token Structural Analysis (2C.2C)
    # ----------------------------------------------------
    print("\n--- 2. Collecting Multiple Login Tokens for Structural Analysis ---")
    tokens = []
    for i in range(10):
        r = requests.post(f"{base_url1}/api/login", json={"username": "admin", "password": "admin123"}, timeout=2)
        tok = r.json().get("token")
        tokens.append(tok)

    token_analysis = {
        "samples": tokens,
        "lengths": [len(t) for t in tokens],
        "all_len_64": all(len(t) == 64 for t in tokens),
        "is_hex": all(all(c in "0123456789abcdef" for c in t) for t in tokens),
        "is_unique": len(set(tokens)) == len(tokens),
    }
    print(f"  Token samples collected: {len(tokens)}")
    print(f"  All length 64: {token_analysis['all_len_64']}")
    print(f"  All lowercase hex: {token_analysis['is_hex']}")
    print(f"  All unique: {token_analysis['is_unique']}")
    results["token_analysis"] = token_analysis

    # ----------------------------------------------------
    # TEST MATRIX 3: Session State Machine & Lifecycle (2C.2E)
    # ----------------------------------------------------
    print("\n--- 3. Testing Session State Machine Transitions ---")
    r_log = requests.post(f"{base_url1}/api/login", json={"username": "admin", "password": "admin123"}, timeout=2)
    active_tok = r_log.json().get("token")

    # A: Auth status with valid token
    r_auth_stat = requests.get(f"{base_url1}/api/auth-status", headers={"Authorization": f"Bearer {active_tok}"}, timeout=2)
    # B: Me with valid token
    r_me_valid = requests.get(f"{base_url1}/api/me", headers={"Authorization": f"Bearer {active_tok}"}, timeout=2)
    # C: Me with query param token
    r_me_query = requests.get(f"{base_url1}/api/me?token={active_tok}", timeout=2)
    # D: Me with invalid token
    r_me_inv = requests.get(f"{base_url1}/api/me", headers={"Authorization": "Bearer deadbeef1234567890deadbeef1234567890deadbeef1234567890deadbeef1234"}, timeout=2)
    # E: Me with no token
    r_me_noauth = requests.get(f"{base_url1}/api/me", timeout=2)

    # F: Logout
    r_logout = requests.post(f"{base_url1}/api/logout", headers={"Authorization": f"Bearer {active_tok}"}, timeout=2)
    # G: Me AFTER logout
    r_me_after_logout = requests.get(f"{base_url1}/api/me", headers={"Authorization": f"Bearer {active_tok}"}, timeout=2)

    state_transitions = {
        "auth_status_status": r_auth_stat.status_code,
        "auth_status_body": r_auth_stat.json() if r_auth_stat.status_code == 200 else r_auth_stat.text,
        "me_valid_status": r_me_valid.status_code,
        "me_valid_body": r_me_valid.json() if r_me_valid.status_code == 200 else r_me_valid.text,
        "me_query_status": r_me_query.status_code,
        "me_query_body": r_me_query.json() if r_me_query.status_code == 200 else r_me_query.text,
        "me_invalid_status": r_me_inv.status_code,
        "me_invalid_body": r_me_inv.text,
        "me_noauth_status": r_me_noauth.status_code,
        "me_noauth_body": r_me_noauth.text,
        "logout_status": r_logout.status_code,
        "logout_body": r_logout.json() if r_logout.status_code == 200 else r_logout.text,
        "me_after_logout_status": r_me_after_logout.status_code,
        "me_after_logout_body": r_me_after_logout.text,
    }
    print(f"  /api/me with valid Bearer: Status {r_me_valid.status_code}, User: {r_me_valid.json().get('username') if r_me_valid.status_code == 200 else ''}")
    print(f"  /api/me with ?token= param: Status {r_me_query.status_code}")
    print(f"  /api/me with invalid token: Status {r_me_inv.status_code}, Body: {r_me_inv.text}")
    print(f"  /api/me without auth: Status {r_me_noauth.status_code}, Body: {r_me_noauth.text}")
    print(f"  /api/logout: Status {r_logout.status_code}, Body: {r_logout.text}")
    print(f"  /api/me after logout: Status {r_me_after_logout.status_code}, Body: {r_me_after_logout.text}")
    results["session_state_machine"] = state_transitions

    # ----------------------------------------------------
    # TEST MATRIX 4: Multiple Concurrent Sessions (2C.2F)
    # ----------------------------------------------------
    print("\n--- 4. Testing Multiple Concurrent Sessions ---")
    r_loginA = requests.post(f"{base_url1}/api/login", json={"username": "admin", "password": "admin123"}, timeout=2)
    tokA = r_loginA.json().get("token")
    r_loginB = requests.post(f"{base_url1}/api/login", json={"username": "admin", "password": "admin123"}, timeout=2)
    tokB = r_loginB.json().get("token")

    # Check both tokens valid
    r_meA = requests.get(f"{base_url1}/api/me", headers={"Authorization": f"Bearer {tokA}"}, timeout=2)
    r_meB = requests.get(f"{base_url1}/api/me", headers={"Authorization": f"Bearer {tokB}"}, timeout=2)

    # Logout Token A
    requests.post(f"{base_url1}/api/logout", headers={"Authorization": f"Bearer {tokA}"}, timeout=2)
    r_meA_after = requests.get(f"{base_url1}/api/me", headers={"Authorization": f"Bearer {tokA}"}, timeout=2)
    r_meB_after = requests.get(f"{base_url1}/api/me", headers={"Authorization": f"Bearer {tokB}"}, timeout=2)

    concurrent_res = {
        "tokenA_valid_initially": r_meA.status_code == 200,
        "tokenB_valid_initially": r_meB.status_code == 200,
        "tokenA_invalid_after_logoutA": r_meA_after.status_code != 200,
        "tokenB_still_valid_after_logoutA": r_meB_after.status_code == 200
    }
    print(f"  Token A & B valid simultaneously: {concurrent_res['tokenA_valid_initially'] and concurrent_res['tokenB_valid_initially']}")
    print(f"  Token B unaffected by Token A logout: {concurrent_res['tokenB_still_valid_after_logoutA']}")
    results["concurrent_sessions"] = concurrent_res

    # Stop server 1
    stop_server(p1)

    # ----------------------------------------------------
    # TEST MATRIX 5: Process Restart Behavior (2C.2G)
    # ----------------------------------------------------
    print("\n--- 5. Testing Process Restart Persistence ---")
    data_dir2 = TMP_DIR / "restart_test"
    make_user_fixture(data_dir2, baseline_users)
    port2 = 29602
    p2 = run_server(data_dir2, port2)
    base_url2 = f"http://127.0.0.1:{port2}"

    # Login and verify
    r_restart_login = requests.post(f"{base_url2}/api/login", json={"username": "admin", "password": "admin123"}, timeout=2)
    restart_tok = r_restart_login.json().get("token")
    r_check_before = requests.get(f"{base_url2}/api/me", headers={"Authorization": f"Bearer {restart_tok}"}, timeout=2)
    valid_before_restart = (r_check_before.status_code == 200)

    # Stop process
    stop_server(p2)
    time.sleep(1)

    # Check filesystem: are there any session persistence files created?
    files_in_data = [p.name for p in data_dir2.iterdir()]

    # Restart process on same data dir
    p2_restarted = run_server(data_dir2, port2)
    r_check_after = requests.get(f"{base_url2}/api/me", headers={"Authorization": f"Bearer {restart_tok}"}, timeout=2)
    valid_after_restart = (r_check_after.status_code == 200)

    stop_server(p2_restarted)

    restart_res = {
        "valid_before_restart": valid_before_restart,
        "valid_after_restart": valid_after_restart,
        "persistence_classification": "SESSION_PERSISTENT_ACROSS_RESTART" if valid_after_restart else "SESSION_MEMORY_ONLY",
        "data_directory_files": files_in_data
    }
    print(f"  Valid before restart: {valid_before_restart}")
    print(f"  Valid after restart: {valid_after_restart}")
    print(f"  Classification: {restart_res['persistence_classification']}")
    results["restart_behavior"] = restart_res

    # ----------------------------------------------------
    # TEST MATRIX 6: Role Dynamics (2C.2J)
    # ----------------------------------------------------
    print("\n--- 6. Testing Role Dynamics & Profile Response ---")
    data_dir3 = TMP_DIR / "role_test"
    make_user_fixture(data_dir3, baseline_users)
    port3 = 29603
    p3 = run_server(data_dir3, port3)
    base_url3 = f"http://127.0.0.1:{port3}"

    r_admin = requests.post(f"{base_url3}/api/login", json={"username": "admin", "password": "admin123"}, timeout=2)
    admin_data = r_admin.json()
    r_user = requests.post(f"{base_url3}/api/login", json={"username": "testuser", "password": "userpass"}, timeout=2)
    user_data = r_user.json()

    r_me_admin = requests.get(f"{base_url3}/api/me", headers={"Authorization": f"Bearer {admin_data['token']}"}, timeout=2).json()
    r_me_user = requests.get(f"{base_url3}/api/me", headers={"Authorization": f"Bearer {user_data['token']}"}, timeout=2).json()

    role_res = {
        "login_admin_response_keys": sorted(admin_data.keys()),
        "login_admin_role": admin_data.get("role"),
        "login_user_role": user_data.get("role"),
        "me_admin_keys": sorted(r_me_admin.keys()),
        "me_admin_role": r_me_admin.get("role"),
        "me_user_role": r_me_user.get("role")
    }
    print(f"  Login response keys: {role_res['login_admin_response_keys']}")
    print(f"  /api/me response keys: {role_res['me_admin_keys']}")
    print(f"  Admin role: {role_res['login_admin_role']}, User role: {role_res['login_user_role']}")
    results["role_semantics"] = role_res

    stop_server(p3)

    # Save complete oracle results
    out_path = ROOT / "evidence" / "go_signaling" / "auth" / "DYNAMIC_AUTH_ORACLE_RESULTS.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n[+] Successfully saved {out_path}")

    # Cleanup temp dir
    try:
        shutil.rmtree(TMP_DIR)
    except:
        pass

if __name__ == "__main__":
    main()
