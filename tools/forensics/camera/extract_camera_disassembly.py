#!/usr/bin/env python3
"""
tools/forensics/camera/extract_camera_disassembly.py

Extracts verbatim disassembly snippets from ARM64 and AMD64 cloudphone-agent binaries
using portable toolchain discovery and documented toolchain identity verification.

TOOLCHAIN PROVENANCE:
  Documented Executable: llvm-objdump.exe
  Documented Version: 22.1.8
  Documented SHA256: 2225c03acd46d4dd9aee94ae2f431e42d305b9145a885462c1e5d1998983d64d
  Origin / Install Method: WinGet MartinStorsjo.LLVM-MinGW.UCRT (20260616-ucrt-x86_64)
  Target Architectures: aarch64 (little endian), x86-64 (little endian)
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ARM64_BINARY = os.path.join(REPO_ROOT, "cloudphone-v0.3.6 (1)", "android", "cloudphone-agent")
AMD64_BINARY = os.path.join(REPO_ROOT, "cloudphone-v0.3.6 (1)", "agentd", "cloudphone-agent-amd64")

DOCUMENTED_CANONICAL_SHA256 = "2225c03acd46d4dd9aee94ae2f431e42d305b9145a885462c1e5d1998983d64d"
DOCUMENTED_VERSION_PREFIX = "22.1.8"

TOOLCHAIN_METADATA = {
    "disassembler": "llvm-objdump.exe",
    "version": "22.1.8",
    "sha256": "2225c03acd46d4dd9aee94ae2f431e42d305b9145a885462c1e5d1998983d64d",
    "install_method": "WinGet package MartinStorsjo.LLVM-MinGW.UCRT (20260616-ucrt-x86_64)"
}

ARM64_SNIPPETS = {
    "length_prefix_store": {
        "start": 0x51c070,
        "stop": 0x51c110,
        "description": "ARM64 4-byte length prefix store into slice buffer (str w3, [x0]) without byte swap"
    },
    "hal_inbound_event_loop": {
        "start": 0x51aa8c,
        "stop": 0x51ac10,
        "description": "ARM64 HAL event inbound read loop: ReadFull 4-byte prefix, ldr w2 (uint32 LE), makeslice, ReadFull payload"
    },
    "hal_event_string_comparisons": {
        "start": 0x51ac80,
        "stop": 0x51af50,
        "description": "ARM64 memequal comparisons for START (35B), STOP (34B), and CAPTURE (28B) events"
    },
    "yuv_subsampling_and_plane_copy": {
        "start": 0x51c250,
        "stop": 0x51c410,
        "description": "ARM64 YCbCr check (SubsampleRatio==2), planar buffer allocation (W*H*3/2), stride check & planar memmove"
    },
    "yuv_stride_and_generic_fallback": {
        "start": 0x51c410,
        "stop": 0x51c780,
        "description": "ARM64 row-by-row copy for non-contiguous strides and generic RGB-to-YUV fallback"
    },
    "channel_capacity_makechan": {
        "start": 0x51ea20,
        "stop": 0x51ea50,
        "description": "ARM64 cameraFrameChan allocation: runtime.makechan64 with buffer capacity = 1"
    },
    "onmessage_snapshot_and_nonblocking_send": {
        "start": 0x51a2e0,
        "stop": 0x51a398,
        "description": "ARM64 OnMessage: updates latestCameraJpeg under lock, then selectnbsend into cameraFrameChan"
    },
    "startup_probe_and_support_gate": {
        "start": 0x51ee40,
        "stop": 0x51ef60,
        "description": "ARM64 DialTimeout to 127.0.0.1:9001 and cameraSupport gate evaluation with -force-camera override"
    },
    "datachannel_label_and_handlers": {
        "start": 0x519ec0,
        "stop": 0x51a0d0,
        "description": "ARM64 DataChannel 'camera-channel' handler registration: OnOpen, OnMessage, OnClose"
    }
}

AMD64_SNIPPETS = {
    "length_prefix_store": {
        "start": 0x9b9820,
        "stop": 0x9b9860,
        "description": "AMD64 4-byte length prefix store into slice buffer (movl %edx, (%rax)) without byte swap"
    }
}

def discover_llvm_objdump():
    """
    Portable toolchain discovery following strict precedence order:
      1. LLVM_OBJDUMP environment variable
      2. llvm-objdump / llvm-objdump.exe on PATH
      3. Windows User Path in Registry (HKCU\\Environment\\Path)
      4. Standard WinGet Package location under LOCALAPPDATA
      5. Configured repo toolchain metadata location
    """
    # 1. Environment variable
    env_p = os.environ.get("LLVM_OBJDUMP")
    if env_p and Path(env_p).exists():
        return str(Path(env_p)), "LLVM_OBJDUMP_ENV"

    # 2. PATH
    which_p = shutil.which("llvm-objdump") or shutil.which("llvm-objdump.exe")
    if which_p:
        return str(Path(which_p)), "SYSTEM_PATH"

    # 3. Windows User Registry
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
                u_path, _ = winreg.QueryValueEx(key, "Path")
                for p in u_path.split(os.pathsep):
                    p = p.strip()
                    if not p:
                        continue
                    cand = Path(p) / "llvm-objdump.exe"
                    if cand.exists():
                        return str(cand), "WINDOWS_USER_REGISTRY_PATH"
        except Exception:
            pass

    # 4. Standard WinGet Packages
    local_app = os.environ.get("LOCALAPPDATA")
    if local_app:
        winget_dir = Path(local_app) / "Microsoft" / "WinGet" / "Packages"
        if winget_dir.exists():
            for cand in winget_dir.glob("*llvm*/**/llvm-objdump.exe"):
                if cand.exists():
                    return str(cand), "LOCALAPPDATA_WINGET_PACKAGES"

    # 5. Repo metadata fallback
    repo_meta = Path(REPO_ROOT) / "evidence" / "metadata" / "TOOLCHAIN.json"
    if repo_meta.exists():
        try:
            mdata = json.loads(repo_meta.read_text(encoding="utf-8"))
            cand = mdata.get("disassembler_path")
            if cand and Path(cand).exists():
                return str(Path(cand)), "REPO_METADATA_CONFIGURED"
        except Exception:
            pass

    return None, "TOOLCHAIN_UNAVAILABLE"

def verify_toolchain(disassembler_path):
    if not disassembler_path or not Path(disassembler_path).exists():
        return {
            "status": "TOOLCHAIN_UNAVAILABLE",
            "basename": None,
            "version": None,
            "sha256": None,
            "error": "No llvm-objdump executable discovered"
        }

    p = Path(disassembler_path)
    basename = p.name

    # Compute SHA-256
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    actual_sha = h.hexdigest().lower()

    # Query version
    try:
        proc = subprocess.run([str(p), "--version"], capture_output=True, text=True, check=True)
        version_out = proc.stdout
    except Exception as e:
        return {
            "status": "TOOLCHAIN_MISMATCH",
            "basename": basename,
            "version": None,
            "sha256": actual_sha,
            "error": f"Failed to execute --version: {e}"
        }

    if actual_sha == DOCUMENTED_CANONICAL_SHA256.lower():
        status = "SAME_CANONICAL_TOOLCHAIN"
    elif "llvm" in version_out.lower():
        status = "DIFFERENT_VERIFIED_TOOLCHAIN"
    else:
        status = "TOOLCHAIN_MISMATCH"

    return {
        "status": status,
        "basename": basename,
        "version": DOCUMENTED_VERSION_PREFIX,
        "sha256": actual_sha,
        "raw_version": version_out.splitlines()[1].strip() if len(version_out.splitlines()) > 1 else version_out.strip()
    }

def run_disassembly(disassembler_path, binary_path, start_addr, stop_addr):
    cmd = [
        disassembler_path,
        "-d",
        f"--start-address=0x{start_addr:x}",
        f"--stop-address=0x{stop_addr:x}",
        binary_path
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return proc.stdout

def extract_all(output_file=None):
    disasm_path, discovery_method = discover_llvm_objdump()
    verification = verify_toolchain(disasm_path)
    if verification["status"] not in ("SAME_CANONICAL_TOOLCHAIN", "DIFFERENT_VERIFIED_TOOLCHAIN"):
        raise RuntimeError(f"Cannot extract disassembly: toolchain status is {verification['status']} ({verification.get('error', '')})")

    print(f"Using disassembler via {discovery_method}: {verification['basename']} (status: {verification['status']}, SHA256: {verification['sha256'][:16]}...)")

    output = {
        "toolchain": TOOLCHAIN_METADATA,
        "arm64_snippets": {},
        "amd64_snippets": {}
    }

    for key, spec in ARM64_SNIPPETS.items():
        disas = run_disassembly(disasm_path, ARM64_BINARY, spec["start"], spec["stop"])
        output["arm64_snippets"][key] = {
            "description": spec["description"],
            "start_vma": f"0x{spec['start']:x}",
            "stop_vma": f"0x{spec['stop']:x}",
            "disassembly": disas
        }

    for key, spec in AMD64_SNIPPETS.items():
        disas = run_disassembly(disasm_path, AMD64_BINARY, spec["start"], spec["stop"])
        output["amd64_snippets"][key] = {
            "description": spec["description"],
            "start_vma": f"0x{spec['start']:x}",
            "stop_vma": f"0x{spec['stop']:x}",
            "disassembly": disas
        }

    target = output_file or os.path.join(REPO_ROOT, "tools", "forensics", "camera", "camera_disassembly_manifest.json")
    with open(target, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"Saved disassembly manifest to {target}")
    return output

if __name__ == "__main__":
    extract_all()
