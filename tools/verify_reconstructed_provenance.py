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
    ROOT / "reconstructed_source" / "webrtc-signaling" / "cmd" / "storage-tool",
    ROOT / "reconstructed_source" / "webrtc-signaling" / "pkg" / "session",
    ROOT / "reconstructed_source" / "webrtc-signaling" / "pkg" / "auth",
    ROOT / "reconstructed_source" / "webrtc-signaling" / "cmd" / "auth-tool",
    ROOT / "reconstructed_source" / "webrtc-signaling" / "pkg" / "httpapi",
    ROOT / "reconstructed_source" / "webrtc-signaling" / "pkg" / "devices",
    ROOT / "reconstructed_source" / "webrtc-signaling" / "cmd" / "http-server"
]

VALID_CLASSIFICATIONS = {
    "DIRECT_TYPE_RECOVERY",
    "RECONSTRUCTED_FROM_BINARY",
    "RECONSTRUCTED_FROM_BEHAVIOR",
    "GENERATED_ADAPTER",
    "GENERATED_TEST_INTERFACE",
    "GENERATED_BUILD_FUNCTION"
}

def check_provenance_fields(classification, comment_block):
    """
    Checks that the comment block contains all required fields for its classification:
    - RECONSTRUCTED_FROM_BINARY: Binary Symbol, VA, Evidence, Confidence
    - RECONSTRUCTED_FROM_BEHAVIOR: Evidence, Confidence
    - DIRECT_TYPE_RECOVERY: Descriptor VA (or equivalent), Evidence, Confidence
    - GENERATED_ADAPTER: Original Function Mapping: NONE, (Source Behavior or Purpose)
    - GENERATED_TEST_INTERFACE: Original Function Mapping: NONE, (Source Behavior or Purpose)
    - GENERATED_BUILD_FUNCTION: Original Function Mapping: NONE, (Source Behavior or Purpose)
    """
    block_text = "\n".join(comment_block)
    missing = []

    def has_field(field_prefix):
        for line in comment_block:
            # Strip // and whitespace
            clean = line.lstrip("/").strip()
            if clean.lower().startswith(field_prefix.lower()):
                parts = clean.split(":", 1)
                if len(parts) > 1 and parts[1].strip():
                    return True
        return False

    if classification == "RECONSTRUCTED_FROM_BINARY":
        if not has_field("Binary Symbol"):
            missing.append("Binary Symbol")
        if not has_field("VA"):
            missing.append("VA")
        if not has_field("Evidence"):
            missing.append("Evidence")
        if not has_field("Confidence"):
            missing.append("Confidence")

    elif classification == "RECONSTRUCTED_FROM_BEHAVIOR":
        if not has_field("Evidence"):
            missing.append("Evidence")
        if not has_field("Confidence"):
            missing.append("Confidence")

    elif classification == "DIRECT_TYPE_RECOVERY":
        has_va = has_field("Descriptor VA") or has_field("Binary Type Descriptor VA") or has_field("VA")
        if not has_va:
            missing.append("Descriptor VA")
        if not has_field("Evidence"):
            missing.append("Evidence")
        if not has_field("Confidence"):
            missing.append("Confidence")

    elif classification in ("GENERATED_ADAPTER", "GENERATED_TEST_INTERFACE", "GENERATED_BUILD_FUNCTION"):
        has_none_map = any("original function mapping" in l.lower() and "none" in l.lower() for l in comment_block)
        if not has_none_map:
            missing.append("Original Function Mapping: NONE")
        has_behavior = has_field("Source Behavior") or has_field("Purpose")
        if not has_behavior:
            missing.append("Source Behavior or Purpose")

    return missing

def audit_reconstructed_provenance():
    print("==================================================")
    print("AUDITING RECONSTRUCTED SOURCE FUNCTION PROVENANCE")
    print("==================================================")

    total_functions = 0
    classification_counts = defaultdict(int)
    missing_headers = []
    missing_fields = []
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
                            field_errs = check_provenance_fields(classification, comment_block)
                            if field_errs:
                                missing_fields.append({
                                    "file": str(rel_path),
                                    "line": i + 1,
                                    "function": func_name,
                                    "classification": classification,
                                    "missing": field_errs
                                })
                            else:
                                audited_functions.append({
                                    "file": str(rel_path),
                                    "line": i + 1,
                                    "function": func_name,
                                    "classification": classification
                                })
                        else:
                            missing_headers.append({
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

    print(f"\nAudit Summary:")
    print(f"  - Missing Headers: {len(missing_headers)}")
    print(f"  - Missing Required Metadata Fields: {len(missing_fields)}")

    failed = False
    if missing_headers:
        failed = True
        print(f"\n[FAIL] Found {len(missing_headers)} functions with missing or invalid CLEANROOM-PROVENANCE headers:")
        for mp in missing_headers:
            print(f"  - {mp['file']}:{mp['line']} in func '{mp['function']}' (header={mp['has_header']}, class={mp['found_class']})")

    if missing_fields:
        failed = True
        print(f"\n[FAIL] Found {len(missing_fields)} functions missing required provenance metadata fields:")
        for mf in missing_fields:
            print(f"  - {mf['file']}:{mf['line']} in func '{mf['function']}' [{mf['classification']}]: missing {mf['missing']}")

    if failed:
        return False, total_functions, classification_counts, len(missing_headers), len(missing_fields)

    print(f"\n[PASS] All {total_functions} functions have valid CLEANROOM-PROVENANCE headers and 100% required metadata fields present.")
    return True, total_functions, classification_counts, 0, 0

if __name__ == "__main__":
    passed, total, counts, m_hdr, m_fld = audit_reconstructed_provenance()
    if not passed:
        sys.exit(1)
    sys.exit(0)
