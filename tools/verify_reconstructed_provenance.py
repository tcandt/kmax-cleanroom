import os
import sys
import re
from pathlib import Path
from collections import defaultdict

# Portable repo root resolution
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root

ROOT = get_repo_root()
SOURCE_DIRS = [
    ROOT / "reconstructed_source" / "webrtc-signaling" / "pkg" / "types",
    ROOT / "reconstructed_source" / "webrtc-signaling" / "pkg" / "storage",
    ROOT / "reconstructed_source" / "webrtc-signaling" / "cmd" / "storage-tool"
]

VALID_CLASSIFICATIONS = {
    "DIRECT_TYPE_RECOVERY",
    "RECONSTRUCTED_FROM_BINARY",
    "RECONSTRUCTED_FROM_BEHAVIOR",
    "GENERATED_ADAPTER",
    "GENERATED_TEST_INTERFACE",
    "GENERATED_BUILD_FUNCTION"
}

def audit_reconstructed_provenance():
    print("==================================================")
    print("AUDITING RECONSTRUCTED SOURCE FUNCTION PROVENANCE")
    print("==================================================")

    total_functions = 0
    classification_counts = defaultdict(int)
    missing_provenance = []
    audited_functions = []

    func_decl_re = re.compile(r'^\s*func\s+(?:\((?:[^)]+)\)\s+)?([A-Za-z0-9_]+)\s*\(')

    for sdir in SOURCE_DIRS:
        if not sdir.exists():
            continue
        for root_dir, _, files in os.walk(sdir):
            for fname in files:
                if not fname.endswith(".go") or fname.endswith("_test.go"):
                    continue
                fpath = Path(root_dir) / fname
                rel_path = fpath.relative_to(ROOT)

                with open(fpath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    m = func_decl_re.match(line)
                    if m:
                        func_name = m.group(1)
                        total_functions += 1

                        # Search preceding lines (up to 20 lines back) for CLEANROOM-PROVENANCE block
                        search_start = max(0, i - 20)
                        comment_block = []
                        for j in range(i - 1, search_start - 1, -1):
                            stripped = lines[j].strip()
                            if stripped.startswith("//"):
                                comment_block.insert(0, stripped)
                            elif stripped == "":
                                continue
                            else:
                                break

                        has_provenance = False
                        classification = None
                        for c_line in comment_block:
                            if "CLEANROOM-PROVENANCE:" in c_line:
                                has_provenance = True
                            if "Classification:" in c_line:
                                parts = c_line.split("Classification:", 1)
                                if len(parts) > 1:
                                    c_name = parts[1].strip()
                                    if c_name in VALID_CLASSIFICATIONS:
                                        classification = c_name

                        if has_provenance and classification:
                            classification_counts[classification] += 1
                            audited_functions.append({
                                "file": str(rel_path),
                                "line": i + 1,
                                "function": func_name,
                                "classification": classification
                            })
                        else:
                            missing_provenance.append({
                                "file": str(rel_path),
                                "line": i + 1,
                                "function": func_name,
                                "has_header": has_provenance,
                                "found_class": classification
                            })

    print(f"Total Declared Functions Audited: {total_functions}")
    print("\nProvenance Classification Breakdown:")
    for c in sorted(VALID_CLASSIFICATIONS):
        print(f"  - {c:30} : {classification_counts[c]}")

    if missing_provenance:
        print(f"\n[FAIL] Found {len(missing_provenance)} functions with missing or invalid CLEANROOM-PROVENANCE blocks:")
        for mp in missing_provenance:
            print(f"  - {mp['file']}:{mp['line']} in func '{mp['function']}' (header={mp['has_header']}, class={mp['found_class']})")
        return False, total_functions, classification_counts

    print(f"\n[PASS] All {total_functions} functions have valid, explicit CLEANROOM-PROVENANCE blocks.")
    return True, total_functions, classification_counts

if __name__ == "__main__":
    passed, total, counts = audit_reconstructed_provenance()
    if not passed:
        sys.exit(1)
    sys.exit(0)
