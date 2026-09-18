#!/usr/bin/env python3
"""
tools/forensics/camera/extract_camera_disassembly.py

Extracts verbatim disassembly snippets from ARM64 and AMD64 cloudphone-agent binaries
using the documented toolchain disassembler.

TOOLCHAIN METADATA:
  Executable Basename: llvm-objdump.exe
  Version: 22.1.8
  SHA256: 2225c03acd46d4dd9aee94ae2f431e42d305b9145a885462c1e5d1998983d64d
  Origin / Install Method: WinGet MartinStorsjo.LLVM-MinGW.UCRT (20260616-ucrt-x86_64)
  Target Architectures: aarch64 (little endian), x86-64 (little endian)
"""
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ARM64_BINARY = os.path.join(REPO_ROOT, "cloudphone-v0.3.6 (1)", "android", "cloudphone-agent")
AMD64_BINARY = os.path.join(REPO_ROOT, "cloudphone-v0.3.6 (1)", "agentd", "cloudphone-agent-amd64")

LLVM_OBJDUMP_PATH = r"C:\Users\TINH-NGUYEN\AppData\Local\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20260616-ucrt-x86_64\bin\llvm-objdump.exe"
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

def run_disassembly(binary_path, start_addr, stop_addr):
    cmd = [
        LLVM_OBJDUMP_PATH,
        "-d",
        f"--start-address=0x{start_addr:x}",
        f"--stop-address=0x{stop_addr:x}",
        binary_path
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return proc.stdout

def extract_all():
    print(f"Extracting disassembly with {TOOLCHAIN_METADATA['disassembler']} (v{TOOLCHAIN_METADATA['version']})...")
    output = {
        "toolchain": TOOLCHAIN_METADATA,
        "arm64_snippets": {},
        "amd64_snippets": {}
    }

    for key, spec in ARM64_SNIPPETS.items():
        disas = run_disassembly(ARM64_BINARY, spec["start"], spec["stop"])
        output["arm64_snippets"][key] = {
            "description": spec["description"],
            "start_vma": f"0x{spec['start']:x}",
            "stop_vma": f"0x{spec['stop']:x}",
            "disassembly": disas
        }
        print(f"  [ARM64] Extracted {key} (0x{spec['start']:x} - 0x{spec['stop']:x})")

    for key, spec in AMD64_SNIPPETS.items():
        disas = run_disassembly(AMD64_BINARY, spec["start"], spec["stop"])
        output["amd64_snippets"][key] = {
            "description": spec["description"],
            "start_vma": f"0x{spec['start']:x}",
            "stop_vma": f"0x{spec['stop']:x}",
            "disassembly": disas
        }
        print(f"  [AMD64] Extracted {key} (0x{spec['start']:x} - 0x{spec['stop']:x})")

    out_file = os.path.join(REPO_ROOT, "tools", "forensics", "camera", "camera_disassembly_manifest.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"Saved disassembly manifest to {out_file}")
    return output

if __name__ == "__main__":
    extract_all()
