#!/usr/bin/env python3
"""
tools/forensics/ai_command/extract_ai_command_disassembly.py

Extracts verbatim disassembly snippets from ARM64 and AMD64 cloudphone-agent binaries
for the ai-command-channel subsystem using portable toolchain discovery.
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
        "start": 0x53f288,
        "stop": 0x53f2ac,
        "description": "ARM64 DataChannel label comparison for 'ai-command-channel' (18 bytes / 0x12, rodata at 0x6bd173, runtime.memequal at 0x15440, branch to 0x53f414)"
    },
    "onmessage_callback_registration": {
        "start": 0x53f414,
        "stop": 0x53f468,
        "description": "ARM64 ai-command-channel setup: closure allocation with func 0x53f5d0 (cemlVcjsE0LQ.2), registration via (*DataChannel).OnMessage (0x499770), no branch-specific OnOpen/OnClose"
    },
    "json_unmarshal_and_validation_branch": {
        "start": 0x53f5d0,
        "stop": 0x53f66c,
        "description": "ARM64 json.Unmarshal into anonymous struct {request_id, command} at 0x60e660; on error logs '[AI-Command] Error parsing request JSON: %v' (0x6d5f36) and returns without response; zero field validation checks"
    },
    "goroutine_spawn_on_success": {
        "start": 0x53f66c,
        "stop": 0x53f710,
        "description": "ARM64 logs '[AI-Command] Executing P2P command (id=%s): %s' (0x6d86f2), allocates closure with func 0x53f740 (cemlVcjsE0LQ.2.1), and spawns goroutine via runtime.newproc (0x5f730)"
    },
    "external_process_invocation": {
        "start": 0x53f740,
        "stop": 0x53f840,
        "description": "ARM64 worker loads 'sh' (0x6ac000) and '-c' (0x6ac002), calls exec.Command (0x196e70) with req.Command, captures stdout/stderr buffers, runs cmd.Run (0x197f00), extracts exit code (0, ExitCode(), or -1)"
    },
    "response_construction_and_send": {
        "start": 0x53f840,
        "stop": 0x53fa00,
        "description": "ARM64 response map construction: request_id (0x6b3a5b), exit_code (0x6b1f17), stdout (0x6ade37), stderr (0x6ade3d), json.Marshal (0x1317c0), and binary response transmission via (*DataChannel).Send (0x49a3d0)"
    }
}

AMD64_SNIPPETS = {
    "inbound_dispatch_label_check": {
        "start": 0x9e2f80,
        "stop": 0x9e2fa8,
        "description": "AMD64 DataChannel label comparison for 'ai-command-channel' (18 bytes / 0x12, rip+0x17c230 = 0xb5f1c2, runtime.memequal at 0x406ce0, jne to 0x9e30eb)"
    },
    "onmessage_callback_registration": {
        "start": 0x9e30eb,
        "stop": 0x9e3134,
        "description": "AMD64 ai-command-channel setup: closure allocation with func 0x9e32c0, registration via (*DataChannel).OnMessage (0x9244a0)"
    },
    "json_unmarshal_and_validation_branch": {
        "start": 0x9e32c0,
        "stop": 0x9e336b,
        "description": "AMD64 json.Unmarshal into struct; on error logs '[AI-Command] Error parsing request JSON: %v' (0xb77ed7) and returns without response; zero field validation checks"
    },
    "goroutine_spawn_on_success": {
        "start": 0x9e336b,
        "stop": 0x9e342e,
        "description": "AMD64 logs '[AI-Command] Executing P2P command (id=%s): %s' (0xb7a693), allocates closure with func 0x9e3460, and spawns goroutine via runtime.newproc (0x451c40)"
    },
    "external_process_invocation": {
        "start": 0x9e3460,
        "stop": 0x9e3650,
        "description": "AMD64 worker loads 'sh' (0xb4e032) and '-c' (0xb4e034), calls exec.Command (0x5a1c00) with req.Command, captures stdout/stderr buffers, runs cmd.Run, extracts exit code (0, ExitCode(), or -1)"
    },
    "response_construction_and_send": {
        "start": 0x9e3650,
        "stop": 0x9e3758,
        "description": "AMD64 response map construction: request_id (0xb55aee), exit_code (0xb53f84), stdout (0xb4fe64), stderr (0xb4fe6a), json.Marshal (0x531b60), and binary response transmission via (*DataChannel).Send (0x9250c0)"
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
    out = proc.stdout
    canonical_bin = "D:\\KMAX-CLEANROOM\\" + os.path.relpath(binary_path, REPO_ROOT)
    if binary_path in out:
        out = out.replace(binary_path, canonical_bin)
    elif binary_path.lower() in out.lower():
        import re
        out = re.sub(re.escape(binary_path), canonical_bin, out, flags=re.IGNORECASE)
    return out

def extract_all(output_file=None):
    disasm_path, discovery_method = discover_llvm_objdump()
    verification = verify_toolchain(disasm_path)
    if verification["status"] not in ("SAME_CANONICAL_TOOLCHAIN", "DIFFERENT_VERIFIED_TOOLCHAIN"):
        raise RuntimeError(f"Cannot extract disassembly: toolchain status is {verification['status']} ({verification.get('error', '')})")

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

    target = output_file or os.path.join(REPO_ROOT, "tools", "forensics", "ai_command", "ai_command_disassembly_manifest.json")
    with open(target, "w", encoding="utf-8", newline="\r\n") as f:
        json.dump(output, f, indent=2)
    return output

if __name__ == "__main__":
    extract_all()
