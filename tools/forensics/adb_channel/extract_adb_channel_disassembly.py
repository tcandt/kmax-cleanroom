#!/usr/bin/env python3
"""
tools/forensics/adb_channel/extract_adb_channel_disassembly.py

Extracts verbatim disassembly snippets from ARM64 and AMD64 cloudphone-agent binaries
for the adb-channel subsystem using portable toolchain discovery.
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
    "inbound_dispatch_label_check": {
        "start": 0x53f2ac,
        "stop": 0x53f300,
        "description": "ARM64 DataChannel label comparison for 'adb-channel' (11 bytes / 0xb, cmp x1, #0xb, immediate compares 'adb-chan', 'ne', 'l', branches to 0x53f300 on match)"
    },
    "onopen_and_readystate_check": {
        "start": 0x53f300,
        "stop": 0x53f414,
        "description": "ARM64 adb-channel setup: closure allocation with func 0x53f4e0 (func11.1), readyState check (0x70(dc)), if open (state==2) directly invokes 0x516020 (_kTtL83Kr), else registers (*DataChannel).OnOpen (0x498d10)"
    },
    "lifecycle_handler_registration": {
        "start": 0x516240,
        "stop": 0x516388,
        "description": "ARM64 handler setup: registers (*DataChannel).OnClose (0x499570) and registers (*DataChannel).OnMessage (0x499770) with closure func 0x5163a0 (func3); no branch-specific OnError registered"
    },
    "session_mode_discriminator_branch": {
        "start": 0x516508,
        "stop": 0x516578,
        "description": "ARM64 session-sticky mode check: evaluates is_first_packet flag, clears it, verifies length >= 24 (0x18) and first 4 bytes match 0x4e584e43 ('CNXN'); if non-matching sets is_bare_pty_mode = true and logs 'First packet is not ADB, switching to BARE raw PTY mode' (0x6e294e)"
    },
    "adb_packet_state_machine": {
        "start": 0x516f5c,
        "stop": 0x516fc0,
        "description": "ARM64 ADB packet header parser & state machine: evaluates 24-byte packet header fields, discriminates OPEN (0x4e45504f), CNXN (0x4e584e43), WRTE, and replies OKAY (0x59414b4f) / CNXN via (*DataChannel).Send (0x49a3d0)"
    },
    "downstream_pty_shell_spawner": {
        "start": 0x516590,
        "stop": 0x516800,
        "description": "ARM64 downstream execution boundary: allocates PTY master/slave via 0x519bf0 (uORj3xlV_Z / pty.Open), pipe fallback via 0x110d40 (EW11VGMk), spawns shell process (/system/bin/sh), launches goroutines via runtime.newproc (0x5f730) to pump stdout to DataChannel; zero net.Dial calls reachable"
    }
}

AMD64_SNIPPETS = {
    "inbound_dispatch_label_check": {
        "start": 0x9e2fad,
        "stop": 0x9e2fdb,
        "description": "AMD64 DataChannel label comparison for 'adb-channel' (11 bytes / 0xb, cmpq $0xb, %rbx, immediate compares 0x6e6168632d626461 'adb-chan', 0x656e 'ne', 0x6c 'l', branches to 0x9e2fdb on match)"
    },
    "onopen_and_readystate_check": {
        "start": 0x9e2fdb,
        "stop": 0x9e30eb,
        "description": "AMD64 adb-channel setup: closure allocation with func 0x9e31c0 (func11.1), readyState check (0x70(%rsi)), if open (state==2) directly invokes 0x9b2be0 (lgKKctm2YGo1), else registers (*DataChannel).OnOpen (0x923b60)"
    },
    "lifecycle_handler_registration": {
        "start": 0x9b2ef4,
        "stop": 0x9b30a0,
        "description": "AMD64 handler setup: registers (*DataChannel).OnClose (0x9242e0) with closure 0x9b5fc0, registers (*DataChannel).OnMessage (0x9244a0) with closure 0x9b30c0; no branch-specific OnError registered"
    },
    "session_mode_discriminator_branch": {
        "start": 0x9b328b,
        "stop": 0x9b3318,
        "description": "AMD64 session-sticky mode check: evaluates is_first_packet flag (%r12), clears it, verifies length >= 24 (0x18) and first 4 bytes match 0x4e584e43 ('CNXN'); if non-matching sets is_bare_pty_mode = true and logs 'First packet is not ADB, switching to BARE raw PTY mode' (0xb8487d)"
    },
    "adb_packet_state_machine": {
        "start": 0x9b3eab,
        "stop": 0x9b4054,
        "description": "AMD64 ADB packet header parser & state machine: evaluates 24-byte packet header fields (offset 0 cmd, offset 4 arg0, offset 8 arg1, offset 12 len, offset 16 crc32, offset 20 magic), discriminates WRTE (0x45545257), CLSE (0x45534c43), OPEN (0x4e45504f), CNXN (0x4e584e43), replies OKAY (0x59414b4f) / CNXN via (*DataChannel).Send (0x9250c0)"
    },
    "downstream_pty_shell_spawner": {
        "start": 0x9b3318,
        "stop": 0x9b3680,
        "description": "AMD64 downstream execution boundary: allocates PTY master/slave via 0x9b7200 (hFJbmSI3 / pty.Open), pipe fallback via 0x50dd80 (HSWRWyyeZ3), spawns shell process (/bin/sh), launches goroutines via runtime.newproc (0x451c40) to pump stdout to DataChannel; zero net.Dial calls reachable"
    }
}

def discover_llvm_objdump():
    env_p = os.environ.get("LLVM_OBJDUMP")
    if env_p and Path(env_p).exists():
        return str(Path(env_p)), "LLVM_OBJDUMP_ENV"

    which_p = shutil.which("llvm-objdump") or shutil.which("llvm-objdump.exe")
    if which_p:
        return str(Path(which_p)), "SYSTEM_PATH"

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

    local_app = os.environ.get("LOCALAPPDATA")
    if local_app:
        winget_dir = Path(local_app) / "Microsoft" / "WinGet" / "Packages"
        if winget_dir.exists():
            for cand in winget_dir.glob("*llvm*/**/llvm-objdump.exe"):
                if cand.exists():
                    return str(cand), "LOCALAPPDATA_WINGET_PACKAGES"

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

    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    actual_sha = h.hexdigest().lower()

    try:
        proc = subprocess.run([str(p), "--version"], capture_output=True, text=True, check=True)
        version_line = proc.stdout.splitlines()[0] if proc.stdout else "unknown"
    except Exception as e:
        version_line = f"error_getting_version: {e}"

    if actual_sha == DOCUMENTED_CANONICAL_SHA256:
        status = "SAME_CANONICAL_TOOLCHAIN"
    elif DOCUMENTED_VERSION_PREFIX in version_line:
        status = "DIFFERENT_VERIFIED_TOOLCHAIN"
    else:
        status = "TOOLCHAIN_MISMATCH"

    return {
        "status": status,
        "basename": basename,
        "path": str(p),
        "version": version_line,
        "sha256": actual_sha
    }

def disassemble_range(objdump_path, binary_path, start_addr, stop_addr):
    cmd = [
        objdump_path,
        "-d",
        f"--start-address={hex(start_addr)}",
        f"--stop-address={hex(stop_addr)}",
        binary_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    out = res.stdout
    canonical_bin = "D:\\KMAX-CLEANROOM\\" + os.path.relpath(binary_path, REPO_ROOT)
    if binary_path in out:
        out = out.replace(binary_path, canonical_bin)
    elif binary_path.lower() in out.lower():
        import re
        out = re.sub(re.escape(binary_path), canonical_bin, out, flags=re.IGNORECASE)
    return out

def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def extract_manifest(output_path=None):
    objdump_p, discovery_method = discover_llvm_objdump()
    tc_info = verify_toolchain(objdump_p)

    if tc_info["status"] == "TOOLCHAIN_MISMATCH":
        raise RuntimeError(f"Toolchain mismatch: {tc_info}")
    if tc_info["status"] == "TOOLCHAIN_UNAVAILABLE":
        raise RuntimeError(f"Toolchain unavailable: {tc_info}")

    arm64_sha = compute_sha256(ARM64_BINARY)
    amd64_sha = compute_sha256(AMD64_BINARY)

    manifest = {
        "toolchain": {
            "disassembler": tc_info["basename"],
            "version": tc_info["version"],
            "sha256": tc_info["sha256"],
            "discovery_method": discovery_method,
            "verification_status": tc_info["status"]
        },
        "binaries": {
            "arm64": {
                "path": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
                "sha256": arm64_sha,
                "snippets": {}
            },
            "amd64": {
                "path": "cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-amd64",
                "sha256": amd64_sha,
                "snippets": {}
            }
        }
    }

    for name, spec in ARM64_SNIPPETS.items():
        disasm_text = disassemble_range(objdump_p, ARM64_BINARY, spec["start"], spec["stop"])
        manifest["binaries"]["arm64"]["snippets"][name] = {
            "start": hex(spec["start"]),
            "stop": hex(spec["stop"]),
            "description": spec["description"],
            "disassembly": disasm_text
        }

    for name, spec in AMD64_SNIPPETS.items():
        disasm_text = disassemble_range(objdump_p, AMD64_BINARY, spec["start"], spec["stop"])
        manifest["binaries"]["amd64"]["snippets"][name] = {
            "start": hex(spec["start"]),
            "stop": hex(spec["stop"]),
            "description": spec["description"],
            "disassembly": disasm_text
        }

    if output_path:
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"Wrote disassembly manifest to {output_path}")

    return manifest

if __name__ == "__main__":
    out_file = os.path.join(REPO_ROOT, "evidence", "go_agent", "webrtc", "adb_channel_disassembly_manifest.json")
    extract_manifest(out_file)
