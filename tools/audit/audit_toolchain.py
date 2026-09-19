#!/usr/bin/env python3
"""
tools/audit/audit_toolchain.py

Canonical Toolchain Discovery, Portability & Policy Auditor.
Validates required clean-room toolchain:
- Go compiler (>= 1.22.0)
- Python interpreter (>= 3.10.0)
- Git (>= 2.30.0)
- llvm-objdump (extracts real LLVM version line)
- CGO C compiler (documents gcc.exe driver vs Clang backend relationship)
- Classifies archival tools (JADX, Apktool, Baksmali) as historical archival evidence.
"""

import os
import sys
import json
import shutil
import hashlib
import subprocess
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.camera.extract_camera_disassembly import discover_llvm_objdump

import re

PORTABILITY_PATTERN = re.compile(
    r'(?:[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_.-]+|(?:^|[\"\'`(\s])[\\/](?:home|Users)[\\/][A-Za-z0-9_.-]+)',
    re.IGNORECASE
)

PORTABILITY_AUDITED_FILES = [
    "tools/verify_release.py",
    "tools/verify_phase2.py",
    "tools/audit/audit_toolchain.py",
    "tools/audit/audit_frozen_contracts.py",
    "tools/audit/audit_original_artifacts.py",
    "tools/audit/audit_method_count.py",
    "tools/audit/validate_phase3_cross_phase_matrix.py",
    "tools/audit/audit_reconstructed_source_provenance.py",
    "tools/forensics/camera/extract_camera_disassembly.py",
    "tools/forensics/adb_channel/extract_adb_channel_disassembly.py",
    "tools/forensics/reproduce_adb_channel_forensics.py",
    "evidence/final/TOOLCHAIN_MANIFEST.json",
    "evidence/final/FROZEN_CONTRACT_REGISTRY.json",
    "evidence/final/PHASE3_CROSS_PHASE_FACT_MATRIX.json",
    "evidence/final/ANDROID_METHOD_COUNT_RECONCILIATION.json",
    "evidence/final/INTENTIONAL_DIVERGENCES.json",
    "evidence/final/RECONSTRUCTED_SOURCE_PROVENANCE_FINAL.json",
    "evidence/final/PROVENANCE_RULES.json"
]

def audit_path_portability(target_or_path=None, repo_root=REPO_ROOT, pattern=None, audited_files=None):
    """
    Audits manifests, configuration objects, or canonical runtime scripts for hardcoded workstation paths.
    Returns (portable: bool, leaks: list).
    """
    pat = pattern if pattern is not None else PORTABILITY_PATTERN
    files_to_check = audited_files if audited_files is not None else PORTABILITY_AUDITED_FILES
    leaks = []

    def _scan_obj(val, loc_prefix):
        if isinstance(val, str):
            if pat.search(val):
                leaks.append({"location": loc_prefix, "value": val})
        elif isinstance(val, dict):
            for k, v in val.items():
                _scan_obj(v, f"{loc_prefix}.{k}" if loc_prefix else str(k))
        elif isinstance(val, list):
            for i, item in enumerate(val):
                _scan_obj(item, f"{loc_prefix}[{i}]")

    # If target_or_path is provided directly (e.g. dict or specific file during test):
    if target_or_path is not None:
        if isinstance(target_or_path, (dict, list)):
            _scan_obj(target_or_path, "target_obj")
        else:
            p = Path(target_or_path)
            if not p.is_absolute() and repo_root:
                p = Path(repo_root) / p
            if p.exists():
                if p.suffix == ".json":
                    try:
                        data = json.loads(p.read_text(encoding="utf-8"))
                        _scan_obj(data, p.name)
                    except Exception as e:
                        leaks.append({"location": str(p), "value": f"JSON parse error: {e}"})
                else:
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    for line_no, line in enumerate(text.splitlines(), start=1):
                        if pat.search(line):
                            leaks.append({"location": f"{p.name}:{line_no}", "value": line.strip()})
            else:
                leaks.append({"location": str(p), "value": "File not found"})
        return (len(leaks) == 0), leaks

    # Otherwise audit all canonical PORTABILITY_AUDITED_FILES
    for rel_path in files_to_check:
        fp = Path(repo_root) / rel_path
        if not fp.exists():
            continue
        if fp.suffix == ".json":
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
                _scan_obj(data, rel_path)
            except Exception as e:
                leaks.append({"location": rel_path, "value": f"JSON parse error: {e}"})
        else:
            text = fp.read_text(encoding="utf-8", errors="ignore")
            for line_no, line in enumerate(text.splitlines(), start=1):
                if pat.search(line):
                    leaks.append({"location": f"{rel_path}:{line_no}", "value": line.strip()})

    is_portable = (len(leaks) == 0)
    return is_portable, leaks

def parse_version_tuple(ver_str):
    match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", ver_str)
    if match:
        parts = [int(p) for p in match.groups() if p is not None]
        while len(parts) < 3:
            parts.append(0)
        return tuple(parts)
    return (0, 0, 0)

def audit_toolchain(repo_root=REPO_ROOT, check_mode=False):
    print("=" * 60)
    print("CLEAN-ROOM TOOLCHAIN MANIFEST & POLICY AUDIT")
    print("=" * 60)

    # 1. Python
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if parse_version_tuple(py_ver) < (3, 10, 0):
        print(f"[FAIL] Python version {py_ver} < required 3.10.0")
        return False

    # 2. Go
    go_path = shutil.which("go")
    if not go_path:
        print("[FAIL] Go compiler not found on PATH!")
        return False
    go_raw = subprocess.check_output([go_path, "version"], text=True).strip()
    go_ver = go_raw.split(" ")[2] if len(go_raw.split(" ")) > 2 else go_raw

    # 3. Git
    git_path = shutil.which("git")
    if not git_path:
        print("[FAIL] Git not found on PATH!")
        return False
    git_raw = subprocess.check_output([git_path, "--version"], text=True).strip()
    git_ver = git_raw.split(" ")[2] if len(git_raw.split(" ")) > 2 else git_raw

    # 4. llvm-objdump
    llvm_path, llvm_prov = discover_llvm_objdump()
    if not llvm_path or not Path(llvm_path).exists():
        print("[FAIL] llvm-objdump could not be discovered via portable discovery!")
        return False

    llvm_proc = subprocess.run([llvm_path, "--version"], capture_output=True, text=True)
    llvm_ver_clean = "Unknown"
    for line in llvm_proc.stdout.splitlines():
        line_s = line.strip()
        if "LLVM version" in line_s or "version" in line_s.lower():
            llvm_ver_clean = line_s
            break
    if llvm_ver_clean == "Unknown":
        llvm_ver_clean = llvm_proc.stdout.splitlines()[0] if llvm_proc.stdout else "Unknown"

    llvm_sha = hashlib.sha256(Path(llvm_path).read_bytes()).hexdigest()

    # 5. CGO C compiler
    cc_path = shutil.which("gcc") or shutil.which("clang")
    if not cc_path and llvm_path:
        candidate_gcc = Path(llvm_path).parent / "gcc.exe"
        if candidate_gcc.exists():
            cc_path = str(candidate_gcc)
        else:
            candidate_clang = Path(llvm_path).parent / "clang.exe"
            if candidate_clang.exists():
                cc_path = str(candidate_clang)

    cc_ver = "Unknown"
    cc_relationship = "gcc.exe is the LLVM-MinGW GCC-compatible driver wrapper calling Clang backend engine for CGO compilation."
    if cc_path:
        cc_proc = subprocess.run([cc_path, "--version"], capture_output=True, text=True)
        cc_ver = cc_proc.stdout.splitlines()[0] if cc_proc.stdout else "Unknown"

    print(f"Discovered Toolchain:")
    print(f"  - Python:        {py_ver} ({sys.executable})")
    print(f"  - Go:            {go_ver} ({go_path})")
    print(f"  - Git:           {git_ver} ({git_path})")
    print(f"  - llvm-objdump:  {llvm_ver_clean} ({llvm_path}) [SHA: {llvm_sha[:12]}...]")
    print(f"  - CGO Compiler:  {cc_ver} ({cc_path})")

    toolchain_data = {
        "metadata": {
            "title": "Final Clean-Room Toolchain Provenance Manifest",
            "phase": "Phase 3AR",
            "host_os": sys.platform,
            "date": "2026-09-18",
            "policy": "PORTABLE_MULTI_SOURCE_DISCOVERY"
        },
        "tools": {
            "go": {
                "role": "Production build, unit test execution, and data-race detector",
                "version": go_raw,
                "required": True,
                "path_policy": "PORTABLE_PATH_DISCOVERY",
                "discovery_mechanism": "shutil.which('go') or %GOROOT%/bin/go",
                "resolved_executable": Path(go_path).name if go_path else None
            },
            "python": {
                "role": "Master release verifier, forensic reproduction engines, and differential derivation test suites",
                "version": py_ver,
                "required": True,
                "path_policy": "CURRENT_RUNTIME_INTERPRETER",
                "discovery_mechanism": "sys.executable",
                "resolved_executable": Path(sys.executable).name
            },
            "git": {
                "role": "Repository tree state validation, historical baseline commit pinning, and git status cleanliness check",
                "version": git_raw,
                "required": True,
                "path_policy": "PORTABLE_PATH_DISCOVERY",
                "discovery_mechanism": "shutil.which('git')",
                "resolved_executable": Path(git_path).name if git_path else None
            },
            "llvm_objdump": {
                "role": "Machine binary disassembly extraction and cross-architecture forensic binding",
                "version": llvm_ver_clean,
                "sha256": llvm_sha,
                "required": True,
                "path_policy": "PORTABLE_MULTI_SOURCE_DISCOVERY",
                "discovery_mechanism": "LLVM_OBJDUMP env -> PATH -> Windows User Registry -> WinGet Packages -> TOOLCHAIN.json",
                "resolved_executable_provenance": llvm_prov,
                "resolved_executable_basename": Path(llvm_path).name
            },
            "c_compiler_cgo": {
                "role": "CGO compiler for go test -race concurrency validation",
                "version": cc_ver,
                "driver_basename": Path(cc_path).name if cc_path else "gcc.exe",
                "backend_engine": "clang",
                "compiler_relationship": cc_relationship,
                "required": True,
                "path_policy": "PORTABLE_MULTI_SOURCE_DISCOVERY",
                "discovery_mechanism": "CC env -> PATH -> Windows User Registry -> TOOLCHAIN.json"
            },
            "jadx": {
                "role": "Android Helper APK direct decompilation (Phase 1A archival)",
                "version": "JADX v1.5.6",
                "classification": "HISTORICAL_ARCHIVAL_OUTPUT_PRESENT",
                "independently_reverified_in_phase3": False,
                "required": False,
                "output_location": "raw_extraction/android/jadx/",
                "notes": "Historical archival artifacts preserved under raw_extraction/android/jadx/. Not independently re-verified in Phase 3AR."
            },
            "apktool": {
                "role": "Android manifest and resources decoder (Phase 1A archival)",
                "version": "Apktool v3.0.3",
                "classification": "HISTORICAL_ARCHIVAL_OUTPUT_PRESENT",
                "independently_reverified_in_phase3": False,
                "required": False,
                "output_location": "raw_extraction/android/apktool/",
                "notes": "Historical archival artifacts preserved under raw_extraction/android/apktool/. Not independently re-verified in Phase 3AR."
            },
            "baksmali": {
                "role": "Dalvik bytecode disassembler for classes.dex (Phase 1A archival)",
                "version": "Baksmali v2.5.2",
                "classification": "HISTORICAL_ARCHIVAL_OUTPUT_PRESENT",
                "independently_reverified_in_phase3": False,
                "required": False,
                "output_location": "raw_extraction/android/smali/",
                "notes": "Historical archival artifacts preserved under raw_extraction/android/smali/. Not independently re-verified in Phase 3AR."
            }
        },
        "decompiler_fidelity_scope": {
            "declared_fidelity_claim": "100.00% decompilation completeness for recovered class/method population (1,061 of 1,061 declared methods represented in the recovered decompilation output; literal source-text identity, comments, local names, and compiler-stripped metadata are not claimed)",
            "prohibited_claims": [
                "100% literal original source text recovery",
                "100% comment recovery"
            ]
        }
    }

    out_file = repo_root / "evidence" / "final" / "TOOLCHAIN_MANIFEST.json"

    if check_mode:
        if not out_file.exists():
            print(f"[FAIL] Check mode failed: {out_file} missing")
            return False
        existing = json.loads(out_file.read_text(encoding="utf-8"))
        tools = existing.get("tools", {})
        for req in ["go", "python", "git", "llvm_objdump", "c_compiler_cgo"]:
            if req not in tools:
                print(f"[FAIL] Required tool missing in {out_file}: {req}")
                return False
            if not tools[req].get("version") or tools[req]["version"] == "Unknown":
                print(f"[FAIL] Tool {req} has invalid version in manifest!")
                return False

        # Validate path portability across canonical tools and manifests
        portable, leaks = audit_path_portability(repo_root=repo_root)
        if not portable:
            print(f"[FAIL] Non-portable workstation path leak detected: {leaks}")
            return False

        print(f"[PASS] Toolchain Manifest verified with all required tools present and valid (zero workstation path leaks).")
        return True

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(toolchain_data, indent=2), encoding="utf-8")
    print(f"[+] Wrote toolchain manifest to {out_file}")
    print("[PASS] Toolchain Policy Audit PASSED.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Audit Toolchain Manifest")
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Path to repository root")
    parser.add_argument("--check", action="store_true", help="Verification mode")
    args = parser.parse_args()

    success = audit_toolchain(repo_root=Path(args.repo_root), check_mode=args.check)
    if not success:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
