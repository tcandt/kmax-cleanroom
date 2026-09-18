import os
import sys
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root

ROOT = get_repo_root()

def verify_consistency():
    print("==================================================")
    print("VERIFYING AUTH MAPPING CONSISTENCY ACROSS ARTIFACTS")
    print("==================================================")

    corr_path = ROOT / "evidence" / "go_signaling" / "auth" / "AUTH_CROSS_BUILD_CORRELATION.json"
    linux_path = ROOT / "evidence" / "go_signaling" / "auth" / "linux_amd64" / "AUTH_FUNCTION_MAP.json"
    win_path = ROOT / "evidence" / "go_signaling" / "auth" / "windows_amd64" / "AUTH_FUNCTION_MAP.json"

    if not corr_path.exists() or not linux_path.exists() or not win_path.exists():
        print("[FAIL] Missing canonical auth correlation or per-artifact maps")
        return False

    with open(corr_path, "r", encoding="utf-8") as f:
        correlation = json.load(f)
    with open(linux_path, "r", encoding="utf-8") as f:
        linux_map = {e["semantic_role"]: e for e in json.load(f)}
    with open(win_path, "r", encoding="utf-8") as f:
        win_map = {e["semantic_role"]: e for e in json.load(f)}

    # 1. Verify 1:1 cross-build correlation integrity
    for c in correlation:
        role = c["semantic_role"]
        if role not in linux_map:
            print(f"[FAIL] Role {role} missing from linux_amd64 map")
            return False
        if role not in win_map:
            print(f"[FAIL] Role {role} missing from windows_amd64 map")
            return False
        l_entry = linux_map[role]
        w_entry = win_map[role]
        if c["linux_amd64"]["symbol"] != l_entry["binary_symbol"] or c["linux_amd64"]["va"] != l_entry["VA"]:
            print(f"[FAIL] Correlation mismatch for Linux {role}")
            return False
        if c["windows_amd64"]["symbol"] != w_entry["binary_symbol"] or c["windows_amd64"]["va"] != w_entry["VA"]:
            print(f"[FAIL] Correlation mismatch for Windows {role}")
            return False

    print(f"[PASS] Cross-build correlation has 100% agreement across all {len(correlation)} roles")

    # 2. Check Go source headers against Linux canonical map
    recon_dir = ROOT / "reconstructed_source" / "webrtc-signaling"
    linux_sym_to_va = {e["binary_symbol"]: e["VA"].lower() for e in linux_map.values()}
    win_sym_to_va = {e["binary_symbol"]: e["VA"].lower() for e in win_map.values()}

    go_files = list((recon_dir / "pkg" / "session").glob("*.go")) + list((recon_dir / "pkg" / "auth").glob("*.go"))
    header_checks = 0

    for gf in go_files:
        content = gf.read_text(encoding="utf-8")
        # Pattern 1: // Binary Symbol: main.xyz \n // VA: 0x123
        matches1 = re.findall(r'// Binary Symbol:\s*([^\s\n]+)[\r\n]+// VA:\s*(0x[0-9a-fA-F]+)', content)
        # Pattern 2: - main.xyz (VA: 0x123, ...
        matches2 = re.findall(r'-\s*(main\.[^\s(]+)\s*\(VA:\s*(0x[0-9a-fA-F]+)', content)
        all_matches = matches1 + matches2
        for sym, va in all_matches:
            va_clean = va.lower()
            if sym in linux_sym_to_va:
                expected_va = linux_sym_to_va[sym]
                if va_clean != expected_va:
                    print(f"[FAIL] {gf.name}: Symbol {sym} declared VA {va_clean} != canonical Linux {expected_va}")
                    return False
                header_checks += 1
            elif sym in win_sym_to_va:
                print(f"[FAIL] {gf.name}: Symbol {sym} declared Windows symbol in Linux-targeted source")
                return False

    print(f"[PASS] Audited {header_checks} source header references against Linux map with 0 discrepancies")

    # 3. Check reports/07 consistency
    report07_path = ROOT / "reports" / "07_PHASE2C2_AUTH_FORENSICS.md"
    if not report07_path.exists():
        print("[FAIL] reports/07_PHASE2C2_AUTH_FORENSICS.md does not exist")
        return False

    r07_content = report07_path.read_text(encoding="utf-8")
    for c in correlation:
        role = c["semantic_role"]
        l_sym = c["linux_amd64"]["symbol"]
        l_va = c["linux_amd64"]["va"].lower()
        w_sym = c["windows_amd64"]["symbol"]
        w_va = c["windows_amd64"]["va"].lower()

        # Check role exists
        if role not in r07_content:
            print(f"[FAIL] Report 07 missing role {role}")
            return False
        # Check Linux pairing
        if l_sym not in r07_content or l_va not in r07_content.lower():
            print(f"[FAIL] Report 07 missing Linux symbol/VA for {role}: {l_sym} ({l_va})")
            return False
        # Check Windows pairing
        if w_sym not in r07_content or w_va not in r07_content.lower():
            print(f"[FAIL] Report 07 missing Windows symbol/VA for {role}: {w_sym} ({w_va})")
            return False

        # Check for cross-architecture contamination
        bad_l_win = rf'{re.escape(l_sym)}\s*\([^)]*0x140'
        if re.search(bad_l_win, r07_content):
            print(f"[FAIL] Report 07 erroneously pairs Linux symbol {l_sym} with Windows VA 0x140...")
            return False
        bad_w_lin = rf'{re.escape(w_sym)}\s*\([^)]*0x73'
        if re.search(bad_w_lin, r07_content):
            print(f"[FAIL] Report 07 erroneously pairs Windows symbol {w_sym} with Linux VA 0x73...")
            return False

    print("[PASS] Report 07 architecture-qualified symbols and cross-correlation verified")

    # 4. Check walkthrough.md consistency (check both repo copy and artifact if present)
    walkthrough_paths = [ROOT / "walkthrough.md"]
    if "WALKTHROUGH_OVERRIDE" in os.environ:
        art_wt = Path(os.environ["WALKTHROUGH_OVERRIDE"])
        if art_wt.exists():
            walkthrough_paths.append(art_wt)

    for wt_path in walkthrough_paths:
        wt_content = wt_path.read_text(encoding="utf-8")
        for c in correlation:
            role = c["semantic_role"]
            l_sym = c["linux_amd64"]["symbol"]
            l_va = c["linux_amd64"]["va"].lower()
            w_sym = c["windows_amd64"]["symbol"]
            w_va = c["windows_amd64"]["va"].lower()

            if role not in wt_content:
                print(f"[FAIL] {wt_path.name} missing role {role}")
                return False
            if l_sym not in wt_content or l_va not in wt_content.lower():
                print(f"[FAIL] {wt_path.name} missing Linux symbol/VA for {role}: {l_sym} ({l_va})")
                return False
            if w_sym not in wt_content or w_va not in wt_content.lower():
                print(f"[FAIL] {wt_path.name} missing Windows symbol/VA for {role}: {w_sym} ({w_va})")
                return False

            # Check no cross contamination
            bad_l_win = rf'{re.escape(l_sym)}\s*\([^)]*0x140'
            if re.search(bad_l_win, wt_content):
                print(f"[FAIL] {wt_path.name} pairs Linux symbol {l_sym} with Windows VA 0x140...")
                return False

        # Ensure old un-normalized erroneous VAs are NOT in walkthrough
        bad_old_vas = ["0x739180", "0x7397e0", "0x7395e0", "0x737ca0", "0x739980", "0x739aa0", "0x737920", "0x739ce0"]
        for bva in bad_old_vas:
            if bva in wt_content:
                print(f"[FAIL] {wt_path.name} still contains deprecated un-normalized VA: {bva}")
                return False

        # Ensure no misleading 100% side-by-side wording
        if "ALL 12 TESTS PASS (100% PARITY)" in wt_content:
            print(f"[FAIL] {wt_path.name} contains overclaiming wording 'ALL 12 TESTS PASS (100% PARITY)'")
            return False

        print(f"[PASS] {wt_path.name} function table and parity wording verified")

    print("==================================================")
    print("ALL AUTH MAPPING CONSISTENCY CHECKS PASSED")
    print("==================================================")
    return True

if __name__ == "__main__":
    ok = verify_consistency()
    sys.exit(0 if ok else 1)
