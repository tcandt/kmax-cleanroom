#!/usr/bin/env python3
"""
tools/forensics/camera/dump_camera_strings.py
Dumps all camera-related string literals directly from the ARM64 and AMD64 cloudphone-agent binaries.
Toolchain: Built-in Python 3; no external runtime dependencies.
"""
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ARM64_BINARY = os.path.join(REPO_ROOT, "cloudphone-v0.3.6 (1)", "android", "cloudphone-agent")
AMD64_BINARY = os.path.join(REPO_ROOT, "cloudphone-v0.3.6 (1)", "agentd", "cloudphone-agent-amd64")

# ARM64 VA = FileOffset + 0x10000 for text/rodata in loadable segment
ARM64_OFFSETS = [
    (0x69cdb6, 5, "0x6acdb6", "width"),
    (0x69ddfb, 6, "0x6addfb", "height"),
    (0x6a39ed, 10, "0x6b39ed", "frame_rate"),
    (0x6cddac, 54, "0x6dddac", "[Camera] DataChannel open. Connecting to Camera HAL..."),
    (0x6c863a, 46, "0x6d863a", "[Camera] Handshake settings sent successfully."),
    (0x6cc579, 51, "0x6dc579", "[Camera] ERROR: failed to connect to Camera HAL: %v"),
    (0x6cc5ac, 51, "0x6dc5ac", "[Camera] Failed to send handshake configuration: %v"),
    (0x6bf9fa, 36, "0x6cf9fa", "[Camera] Dialing Camera HAL at %s..."),
    (0x6bb6cd, 32, "0x6cb6cd", "[Camera] DataChannel '%s' opened"),
    (0x6d0ea3, 59, "0x6e0ea3", "[Camera] DataChannel closed. Stopping Camera HAL session..."),
    (0x6ca3a4, 48, "0x6da3a4", "[Camera] ERROR: failed to decode JPEG to YUV: %v"),
    (0x6c6bd0, 44, "0x6d6bd0", "[Camera] ERROR: failed to send YUV frame: %v"),
    (0x6ba6ee, 31, "0x6ca6ee", "[Camera] Received HAL event: %s"),
    (0x6beac7, 35, "0x6ceac7", "VIRTUAL_DEVICE_START_CAMERA_SESSION"),
    (0x6bdb19, 34, "0x6cdb19", "VIRTUAL_DEVICE_STOP_CAMERA_SESSION"),
    (0x6b7482, 28, "0x6c7482", "VIRTUAL_DEVICE_CAPTURE_IMAGE"),
    (0x69c7fd, 4, "0x6ac7fd", "stop"),
    (0x69cd4d, 5, "0x6acd4d", "start"),
    (0x6ade01 - 0x10000, 6, "0x6ade01", "action"),
    (0x6cbc7d, 50, "0x6dbc7d", "[Camera] Android closed camera! Stopping stream..."),
    (0x6cbc4b, 50, "0x6dbc4b", "[Camera] Android opened camera! Starting stream..."),
    (0x6d42d6 - 0x10000, 41, "0x6d42d6", "[Camera] Android requested JPEG snapshot!"),
    (0x6da374 - 0x10000, 48, "0x6da374", "[Camera] Failed to send JPEG snapshot to HAL: %v"),
    (0x6d8858, 91, "0x6e8858", "[Agent] Camera HAL is not available, but camera support is FORCED enabled via -force-camera"),
    (0x6d22c4, 62, "0x6e22c4", "[Agent] Camera HAL is available at %s (camera support enabled)"),
    (0x6e9132 - 0x10000, 99, "0x6e9132", "[Agent] Camera HAL is not available at %s (camera support disabled). Use -force-camera to override.")
]

def dump_strings():
    if not os.path.exists(ARM64_BINARY):
        print(f"ERROR: binary not found: {ARM64_BINARY}", file=sys.stderr)
        sys.exit(1)

    print(f"Dumping {len(ARM64_OFFSETS)} forensic string literals from {ARM64_BINARY}...")
    results = {}
    with open(ARM64_BINARY, "rb") as f:
        for off, length, va, expected in ARM64_OFFSETS:
            f.seek(off)
            raw = f.read(length)
            decoded = raw.decode("utf-8", errors="replace")
            assert decoded == expected, f"Mismatch at {va}: expected {expected!r}, got {decoded!r}"
            results[va] = decoded
            print(f"  [{va}] {decoded}")
    print("All string assertions verified successfully.")
    return results

if __name__ == "__main__":
    dump_strings()
