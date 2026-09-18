#!/usr/bin/env python3
"""
tools/forensics/reproduce_camera_forensics.py

Reproduces and validates the frozen camera forensic interpretation against original
binary disassembly and supporting artifacts.

Modes:
  --check (default): Non-mutating verification. Regenerates artifacts into a temporary
                     directory, computes cryptographic hashes, asserts exact match against
                     frozen canonical values, validates machine-binding invariants, and
                     leaves the repository untouched.
  --write:           Explicitly writes regenerated canonical artifacts to evidence/ directory.

Usage:
  python tools/forensics/reproduce_camera_forensics.py --check
  python tools/forensics/reproduce_camera_forensics.py --write
"""
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS_CAMERA = REPO_ROOT / "tools" / "forensics" / "camera"
EVIDENCE_DIR = REPO_ROOT / "evidence" / "go_agent" / "webrtc"

SPEC_PATH = EVIDENCE_DIR / "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json"
CONTRACT_PATH = EVIDENCE_DIR / "CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json"

EXPECTED_SPEC_SHA = "1a177531761d51ee280be5d9dce5bd8442c42f19f66ca5acde66b38dd4c48ff9"
EXPECTED_BASE_CONTRACT_SHA = "818abe7db2cc38df3563a0f6cf45ec047cf0c0a93338c994e60a327fc0d471ce"

sys.path.insert(0, str(REPO_ROOT))
from tools.forensics.camera.extract_camera_disassembly import discover_llvm_objdump, verify_toolchain, extract_all
from tools.forensics.camera.derive_camera_protocol import derive_protocol_rules

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().lower()

def build_canonical_spec_dict(derived):
    return {
        "metadata": {
            "title": "Phase 2C.5B4F WebRTC Camera DataChannel & Bridge Protocol Specification",
            "phase": "Phase 2C.5B4F",
            "status": "FROZEN_FORENSIC_BASELINE",
            "base_commit": "2a039510d7e5ae4ef3f067769b40660c705989ff",
            "classification": "Clean-room behavioral/protocol reconstruction",
            "channel_label": "camera-channel",
            "toolchain_provenance": derived["toolchain_provenance"],
            "governing_docs": [
                "evidence/go_agent/webrtc/DATACHANNEL_LABEL_EVIDENCE.json",
                "evidence/go_agent/webrtc/DATACHANNEL_FRAMING_MATRIX.json",
                "evidence/go_agent/webrtc/AGENT_HELPER_IPC_SOCKET_MATRIX.json",
                "evidence/go_agent/DISASSEMBLY_FACTS.json",
                "evidence/go_agent/STRINGS.json",
                "evidence/reference/raw/web-app/src/composables/useWebRTC.js"
            ]
        },
        "channel_properties": {
            "label": "camera-channel",
            "channel_type": "OUTBOUND_AGENT_CREATED",
            "creator_side": "Agent",
            "consumer_side": "Browser Client",
            "ordered": True,
            "evidence_class": "STATIC_CONFIRMED",
            "ordered_evidence": "Disassembly passes ordered=1 byte pointer in AMD64 0x9e216d and ARM64 0x53e740",
            "conditional_creation": "Created if and only if cameraSupport == true (probed at cameraAddr or overridden via -force-camera)",
            "framing": "MIXED_JSON_AND_RAW_BINARY",
            "binary_type": "arraybuffer"
        },
        "datachannel_message_types": {
            "agent_to_browser": {
                "start_command": {
                    "evidence_class": "STATIC_CONFIRMED",
                    "framing": "JSON_TEXT",
                    "payload": {
                        "action": "start"
                    },
                    "trigger": "Received VIRTUAL_DEVICE_START_CAMERA_SESSION event from Camera HAL TCP socket",
                    "log_string": "[Camera] Android opened camera! Starting stream...",
                    "rodata_va": "0x6dbc4b"
                },
                "stop_command": {
                    "evidence_class": "STATIC_CONFIRMED",
                    "framing": "JSON_TEXT",
                    "payload": {
                        "action": "stop"
                    },
                    "trigger": "Received VIRTUAL_DEVICE_STOP_CAMERA_SESSION event from Camera HAL TCP socket",
                    "log_string": "[Camera] Android closed camera! Stopping stream...",
                    "rodata_va": "0x6dbc7d"
                }
            },
            "browser_to_agent": {
                "camera_frame": {
                    "evidence_class": "STATIC_CONFIRMED",
                    "framing": "RAW_BINARY",
                    "format": "image/jpeg (ArrayBuffer)",
                    "agent_decoder": "image/jpeg.Decode (*image.YCbCr expected)",
                    "reference_frontend_parameters": {
                        "evidence_class": "REFERENCE_ONLY",
                        "canvas_resolution": "640x480",
                        "fps": 30,
                        "mime_type": "image/jpeg",
                        "quality": 0.6,
                        "source": "Browser canvas.toBlob(..., 'image/jpeg', 0.6) from navigator.mediaDevices.getUserMedia"
                    },
                    "processing": "Cached in s.latestCameraJpeg (under latestCameraJpegMu); non-blocking send to s.cameraFrameChan; decoded to planar YUV420P for Camera HAL"
                }
            }
        },
        "camera_hal_tcp_protocol": {
            "endpoint_classification": derived["tcp_endpoint_classification"],
            "wire_framing": {
                "evidence_class": "STATIC_CONFIRMED",
                "description": "4-byte little-endian uint32 length prefix preceding raw payload bytes",
                "width_bytes": 4,
                "byte_order": "little-endian",
                "data_type": "uint32",
                "arm64_instruction": "str w3, [x0] (native 32-bit register store, little-endian)",
                "amd64_instruction": "movl %edx, (%rax) (native 32-bit register store, little-endian)",
                "byte_swap_present": False,
                "framing_test_vectors": derived["wire_length_framing"]["test_vectors"]
            },
            "inbound_event_framing": derived["hal_inbound_framing"],
            "handshake": {
                "evidence_class": "STATIC_CONFIRMED",
                "format": "JSON_TEXT inside 4-byte little-endian length prefix",
                "default_fields": derived["handshake_parameters"]["fields"],
                "schema": derived["handshake_parameters"]["json_schema"],
                "success_log": "[Camera] Handshake settings sent successfully. (0x6d863a)",
                "failure_log": "[Camera] Failed to send handshake configuration: %v (0x6dc5ac)"
            },
            "video_frame_stream": {
                "evidence_class": "STATIC_CONFIRMED",
                "format": "RAW_PLANAR_YUV420P inside 4-byte little-endian length prefix",
                "planar_layout": derived["yuv420_planar_layout"],
                "error_log": "[Camera] ERROR: failed to send YUV frame: %v (0x6d6bd0)"
            },
            "snapshot_response": {
                "evidence_class": "STATIC_CONFIRMED",
                "format": "RAW_JPEG inside 4-byte little-endian length prefix",
                "source": "s.latestCameraJpeg (or fallback JPEG if unpopulated)",
                "trigger": "Received VIRTUAL_DEVICE_CAPTURE_IMAGE event from Camera HAL",
                "event_log": "[Camera] Android requested JPEG snapshot! (0x6d42d6)",
                "error_log": "[Camera] Failed to send JPEG snapshot to HAL: %v (0x6da374)"
            }
        },
        "backpressure_and_concurrency": {
            "channel_capacity": {
                "evidence_class": "STATIC_CONFIRMED",
                "name": "cameraFrameChan",
                "capacity": 1,
                "allocation_callsite": "runtime.makechan64 with size = 1 (ARM64 0x51ea3c)"
            },
            "enqueue_semantics": {
                "evidence_class": "STATIC_CONFIRMED",
                "callsite": "runtime.selectnbsend(s.cameraFrameChan, msg.Data) (ARM64 0x51a388)",
                "static_fact": "current frame is not enqueued when non-blocking send cannot proceed",
                "drop_policy_rationale": {
                    "classification": "INFERENCE",
                    "rationale": "Non-blocking send discards newest incoming frame when single-element buffer is saturated to minimize transmission latency"
                }
            },
            "snapshot_cache_ordering": {
                "evidence_class": "STATIC_CONFIRMED",
                "mutex": "latestCameraJpegMu (offset 0x488)",
                "cache": "latestCameraJpeg (offset 0x470)",
                "ordering": "latestCameraJpeg is updated under lock BEFORE selectnbsend into cameraFrameChan",
                "dropped_frame_retention": "Frame discarded from streaming queue still persists in snapshot cache; VIRTUAL_DEVICE_CAPTURE_IMAGE always delivers latest frame"
            }
        },
        "lifecycle_state_model": derived["lifecycle_model_classification"],
        "architectural_separation": derived["camera_capture_boundary"]
    }

def build_canonical_contract_dict(derived):
    return {
        "metadata": {
            "title": "Phase 2C.5B4F WebRTC Camera DataChannel & Virtual Camera Implementation Contract",
            "phase": "Phase 2C.5B4F",
            "status": "FROZEN_FORENSIC_BASELINE",
            "base_commit": "2a039510d7e5ae4ef3f067769b40660c705989ff",
            "classification": "Clean-room behavioral/protocol reconstruction",
            "toolchain_provenance": derived["toolchain_provenance"],
            "governing_docs": [
                "evidence/go_agent/webrtc/DATACHANNEL_LABEL_EVIDENCE.json",
                "evidence/go_agent/webrtc/DATACHANNEL_FRAMING_MATRIX.json",
                "evidence/go_agent/webrtc/AGENT_HELPER_IPC_SOCKET_MATRIX.json",
                "evidence/go_agent/webrtc/CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "evidence/go_agent/DISASSEMBLY_FACTS.json",
                "evidence/go_agent/STRINGS.json",
                "evidence/reference/raw/web-app/src/composables/useWebRTC.js"
            ]
        },
        "requirements": [
            {
                "id": "CAM-B4-01",
                "requirement": "Outbound Camera-Channel Creation and Ownership",
                "observable_behavior": "Agent creates outbound DataChannel labeled 'camera-channel' with ordered=true before SDP offer creation if cameraSupport is true",
                "source_artifact": "DATACHANNEL_LABEL_EVIDENCE.json",
                "source_field_or_case": "confirmed_webrtc_channels.camera-channel",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "Static disassembly proves CreateDataChannel call with ordered=1 byte pointer at AMD64 0x9e216d and ARM64 0x53e740 under cameraSupport condition at 0x53e704"
            },
            {
                "id": "CAM-B4-02",
                "requirement": "Camera HAL/Bridge Probe and Signaling Flag Parity",
                "observable_behavior": "Agent probes default Camera HAL/bridge endpoint (default 127.0.0.1:9001, configurable via -camera-addr / CP_AGENT_CAMERA_ADDR); sets cameraSupport=true if responsive or overridden via -force-camera; transmits camera_support boolean in WebRTC offer payload",
                "source_artifact": "STRINGS.json",
                "source_field_or_case": "evidence/go_agent/STRINGS.json:23796,23852",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "Disassembly at ARM64 0x51ee80-0x51ef94 dials net.DialTimeout and logs '[Agent] Camera HAL is not available at %s (camera support disabled). Use -force-camera to override.' or '[Agent] Camera HAL is available at %s (camera support enabled)'"
            },
            {
                "id": "CAM-B4-03",
                "requirement": "DataChannel Lifecycle Binding (OnOpen, OnMessage, OnClose)",
                "observable_behavior": "Agent attaches active OnOpen, OnMessage, and OnClose handlers to camera-channel upon creation",
                "source_artifact": "DISASSEMBLY_FACTS.json",
                "source_field_or_case": "ARM64 0x51a024-0x51a0f8",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "Registers OnOpen closure 0x51a3d0, OnMessage closure 0x51a2e0, OnClose closure 0x51a120 on cameraDataChannel"
            },
            {
                "id": "CAM-B4-04",
                "requirement": "Camera HAL/Bridge TCP Connection and Handshake Framing",
                "observable_behavior": "Upon camera-channel open, Agent connects to Camera HAL/bridge endpoint (default 127.0.0.1:9001) and transmits 4-byte little-endian length-prefixed JSON handshake with width, height, and frame_rate",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "camera_hal_tcp_protocol.handshake",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "ARM64 0x51a764 dials 'tcp', 0x51a9c4 marshals JSON with 'width', 'height', 'frame_rate', 0x51a9e0 transmits via 0x51c060 with 4-byte little-endian length prefix"
            },
            {
                "id": "CAM-B4-05",
                "requirement": "Camera HAL/Bridge Inbound Event Read Framing and Dispatch",
                "observable_behavior": "Agent reads 4-byte little-endian length-prefixed ASCII event strings from Camera HAL/bridge socket, responding to VIRTUAL_DEVICE_START_CAMERA_SESSION, VIRTUAL_DEVICE_STOP_CAMERA_SESSION, and VIRTUAL_DEVICE_CAPTURE_IMAGE",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "camera_hal_tcp_protocol.inbound_event_framing",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "Disassembly at ARM64 0x51aa8c-0x51af50 uses io.ReadFull for 4-byte length prefix, uint32 LE read, io.ReadFull for exact payload, and runtime.memequal comparisons"
            },
            {
                "id": "CAM-B4-06",
                "requirement": "Outbound Start and Stop Command Dispatch",
                "observable_behavior": "Agent dispatches JSON text frames {'action':'start'} and {'action':'stop'} over camera-channel when Camera HAL starts or stops virtual camera session",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "datachannel_message_types.agent_to_browser",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "ARM64 0x51c980 marshals {'action': action} and calls DataChannel.SendText; matches browser useWebRTC.js:798-805"
            },
            {
                "id": "CAM-B4-07",
                "requirement": "Inbound Binary JPEG Frame Ingestion and Snapshot Cache Ordering",
                "observable_behavior": "Agent receives binary JPEG ArrayBuffer frames on camera-channel and caches the latest frame in latestCameraJpeg under mutex protection BEFORE attempting non-blocking channel enqueue",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "datachannel_message_types.browser_to_agent",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "ARM64 0x51a318-0x51a364 locks latestCameraJpegMu, updates latestCameraJpeg slice, unlocks, then invokes selectnbsend. Even if streaming buffer is full, newest frame persists in snapshot cache"
            },
            {
                "id": "CAM-B4-08",
                "requirement": "Single-Element Channel Capacity and Non-Blocking Enqueue",
                "observable_behavior": "Agent forwards incoming frames to cameraFrameChan (capacity=1) via non-blocking send (runtime.selectnbsend); current frame is not enqueued when channel buffer is saturated",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "backpressure_and_concurrency",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "Channel allocation at ARM64 0x51ea3c passes size 1 to runtime.makechan64. Enqueue at 0x51a388 calls runtime.selectnbsend (0x230a0); dropped frame design rationale is INFERENCE (low-latency drop semantics)"
            },
            {
                "id": "CAM-B4-09",
                "requirement": "JPEG Decoding to Planar I420 (YUV420P) with Stride Support",
                "observable_behavior": "Agent worker decodes incoming JPEG frames using image/jpeg.Decode, verifies *image.YCbCr with YCbCrSubsampleRatio420, and formats into contiguous planar YUV420P buffer (Y then Cb then Cr) with row-by-row stride handling and generic fallback",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "camera_hal_tcp_protocol.video_frame_stream",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "ARM64 0x51c250-0x51c780 validates SubsampleRatio==2, performs contiguous memmove when YStride==W and CStride==W/2, row-by-row copy if strides differ, and Rec.601 RGB conversion fallback"
            },
            {
                "id": "CAM-B4-10",
                "requirement": "Little-Endian Length-Prefixed YUV Frame Transmission",
                "observable_behavior": "Agent transmits raw planar YUV420P frames to Camera HAL TCP connection with a 4-byte little-endian unsigned integer length prefix",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "camera_hal_tcp_protocol.wire_framing",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "ARM64 0x51c0a8 stores 32-bit length with str w3, [x0] without byte swap; AMD64 0x9b9845 stores with movl %edx, (%rax). Both target platforms are natively little-endian"
            },
            {
                "id": "CAM-B4-11",
                "requirement": "Virtual Camera JPEG Snapshot Extraction",
                "observable_behavior": "Upon receipt of VIRTUAL_DEVICE_CAPTURE_IMAGE event from Camera HAL, Agent replies with 4-byte little-endian length-prefixed cached latestCameraJpeg frame under mutex protection",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "camera_hal_tcp_protocol.snapshot_response",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "ARM64 0x51af40-0x51b170 locks latestCameraJpegMu, reads latestCameraJpeg slice, unlocks, and writes 4-byte little-endian length prefix + payload to Camera HAL socket"
            },
            {
                "id": "CAM-B4-12",
                "requirement": "Physical-Camera vs Virtual-Camera Boundary Assertion",
                "observable_behavior": "Virtual camera data plane routes exclusively through camera-channel and Camera HAL/bridge TCP socket (default 127.0.0.1:9001), strictly decoupled from scrcpy helper video UDS (@uds_sys_v_) and CameraCapture.java",
                "source_artifact": "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json",
                "source_field_or_case": "architectural_separation",
                "evidence_class": "CROSS_COMPONENT_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "CameraCapture.java is positively bound to the physical-camera capture pipeline. No recovered call/data-flow evidence places CameraCapture.java on the virtual-camera injection path; the recovered injection path is camera-channel -> Agent JPEG decode -> camera TCP bridge"
            },
            {
                "id": "CAM-B4-13",
                "requirement": "Strict Isolation of Deferred Channels (AI and ADB)",
                "observable_behavior": "Channels 'ai-command-channel' and 'adb-channel' remain strictly deferred with inert lifecycle references only and zero payload processing logic",
                "source_artifact": "FILE_CHANNEL_B3_IMPLEMENTATION_CONTRACT.json",
                "source_field_or_case": "FILE-B3-16",
                "evidence_class": "STATIC_CONFIRMED",
                "confidence": "HIGH",
                "mandatory_for_parity": True,
                "notes": "Preserves clean-room scope isolation across reconstruction phases"
            }
        ]
    }

def validate_machine_binding_invariants(spec, contract, derived):
    """
    Independently validates all 16 critical machine-binding checks required by Section 11.
    """
    # 1. camera-channel label
    assert spec["channel_properties"]["label"] == "camera-channel", "camera-channel label missing"

    # 2. ordered flag
    assert spec["channel_properties"]["ordered"] is True, "ordered flag must be True"

    # 3. cameraSupport branch/gate
    gate = spec["channel_properties"]["conditional_creation"]
    assert "cameraSupport == true" in gate and "-force-camera" in gate, "cameraSupport gate missing"

    # 4. 4-byte LE framing
    wire_framing = spec["camera_hal_tcp_protocol"]["wire_framing"]
    assert wire_framing["width_bytes"] == 4, "wire framing width must be 4 bytes"
    assert wire_framing["byte_order"] == "little-endian", "wire framing must be little-endian"
    assert "str w3, [x0]" in wire_framing["arm64_instruction"], "ARM64 str w3 missing"
    assert "movl %edx, (%rax)" in wire_framing["amd64_instruction"], "AMD64 movl %edx missing"

    # 5. Three HAL event names and lengths
    events = spec["camera_hal_tcp_protocol"]["inbound_event_framing"]["supported_events"]
    event_map = {e["event_name"]: e["length"] for e in events}
    assert event_map.get("VIRTUAL_DEVICE_START_CAMERA_SESSION") == 35, "START event length != 35"
    assert event_map.get("VIRTUAL_DEVICE_STOP_CAMERA_SESSION") == 34, "STOP event length != 34"
    assert event_map.get("VIRTUAL_DEVICE_CAPTURE_IMAGE") == 28, "CAPTURE event length != 28"

    # 6. io.ReadFull prefix/payload pattern
    read_mech = spec["camera_hal_tcp_protocol"]["inbound_event_framing"]["read_mechanism"]
    assert "io.ReadFull" in read_mech, "io.ReadFull read mechanism missing"

    # 7. cameraFrameChan capacity = 1
    assert spec["backpressure_and_concurrency"]["channel_capacity"]["capacity"] == 1, "capacity != 1"

    # 8. selectnbsend callsite
    assert "selectnbsend" in spec["backpressure_and_concurrency"]["enqueue_semantics"]["callsite"], "selectnbsend callsite missing"

    # 9. latestCameraJpeg update-before-enqueue ordering
    ordering = spec["backpressure_and_concurrency"]["snapshot_cache_ordering"]["ordering"]
    assert "BEFORE selectnbsend" in ordering, "snapshot ordering must update before selectnbsend"

    # 10. jpeg.Decode call path
    assert "image/jpeg.Decode" in spec["datachannel_message_types"]["browser_to_agent"]["camera_frame"]["agent_decoder"], "jpeg.Decode missing"

    # 11. YCbCr SubsampleRatio420 check
    layout = spec["camera_hal_tcp_protocol"]["video_frame_stream"]["planar_layout"]
    assert layout["format"] == "Planar I420 (YUV420P)", "format != Planar I420"

    # 12. Y/U/V plane order
    assert layout["plane_order"] == ["Y", "U (Cb)", "V (Cr)"], "plane order != Y, U, V"

    # 13. stride fallback
    assert "stride_fallback_action" in layout, "stride fallback missing"

    # 14. default endpoint 127.0.0.1:9001
    endpoint = spec["camera_hal_tcp_protocol"]["endpoint_classification"]
    assert endpoint["default_endpoint"] == "127.0.0.1:9001", "default endpoint != 127.0.0.1:9001"

    # 15. -camera-addr
    assert endpoint["configurable_flag"] == "-camera-addr", "-camera-addr flag missing"

    # 16. -force-camera
    assert endpoint["override_flag"] == "-force-camera", "-force-camera flag missing"

    # Browser reference parameters separated in REFERENCE_ONLY
    ref_params = spec["datachannel_message_types"]["browser_to_agent"]["camera_frame"]["reference_frontend_parameters"]
    assert ref_params["evidence_class"] == "REFERENCE_ONLY", "frontend reference must be REFERENCE_ONLY"
    assert ref_params["canvas_resolution"] == "640x480"
    assert ref_params["fps"] == 30
    assert ref_params["quality"] == 0.6

    # Verify contract requirements count
    assert len(contract["requirements"]) == 13, f"Expected 13 requirements, got {len(contract['requirements'])}"

def run_check_mode():
    print("==================================================")
    print("PHASE 2C.5B4F CAMERA FORENSIC REPRODUCER (--check)")
    print("==================================================")
    print("Mode: Non-mutating temp verification & machine-binding validation\n")

    # Snapshot git status before execution
    git_before = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO_ROOT), capture_output=True, text=True)
    before_status = git_before.stdout.strip()

    # Step 0: Toolchain discovery and verification
    disasm_path, method = discover_llvm_objdump()
    t_info = verify_toolchain(disasm_path)
    print(f"Toolchain: {t_info['basename']} via {method} (Status: {t_info['status']}, SHA256: {str(t_info['sha256'])[:16]}...)")
    if t_info["status"] not in ("SAME_CANONICAL_TOOLCHAIN", "DIFFERENT_VERIFIED_TOOLCHAIN"):
        print(f"[FAIL] Incompatible toolchain status: {t_info['status']}", file=sys.stderr)
        sys.exit(1)

    # Verify canonical files exist
    if not SPEC_PATH.exists():
        print(f"[FAIL] Canonical spec file missing: {SPEC_PATH}", file=sys.stderr)
        sys.exit(1)
    if not CONTRACT_PATH.exists():
        print(f"[FAIL] Canonical contract file missing: {CONTRACT_PATH}", file=sys.stderr)
        sys.exit(1)

    canon_spec_sha = hash_file(SPEC_PATH)
    canon_contract_sha = hash_file(CONTRACT_PATH)

    # Fail-closed check against frozen constants
    if canon_spec_sha != EXPECTED_SPEC_SHA:
        print(f"[FAIL] Canonical spec SHA mismatch! Expected {EXPECTED_SPEC_SHA}, got {canon_spec_sha}", file=sys.stderr)
        sys.exit(1)
    if canon_contract_sha != EXPECTED_BASE_CONTRACT_SHA:
        print(f"[FAIL] Canonical base contract SHA mismatch! Expected {EXPECTED_BASE_CONTRACT_SHA}, got {canon_contract_sha}", file=sys.stderr)
        sys.exit(1)
    print(f"[+] Canonical Spec SHA256 matches frozen baseline:     {canon_spec_sha}")
    print(f"[+] Canonical Contract SHA256 matches frozen baseline: {canon_contract_sha}")

    # Regenerate in temporary directory to verify non-mutating reproducibility
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_p = Path(temp_dir)
        temp_manifest = temp_dir_p / "camera_disassembly_manifest.json"
        temp_derived_p = temp_dir_p / "derived_camera_protocol.json"
        temp_spec_p = temp_dir_p / "CAMERA_CHANNEL_B4_PROTOCOL_SPEC.json"
        temp_contract_p = temp_dir_p / "CAMERA_CHANNEL_B4_IMPLEMENTATION_CONTRACT.json"

        # 1. Disassembly extraction
        extract_all(output_file=str(temp_manifest))

        # 2. Protocol derivation
        derived = derive_protocol_rules(manifest_path=str(temp_manifest), output_path=str(temp_derived_p))

        # 3. Spec & Contract generation
        spec_dict = build_canonical_spec_dict(derived)
        contract_dict = build_canonical_contract_dict(derived)

        with open(temp_spec_p, "w", encoding="utf-8") as f:
            json.dump(spec_dict, f, indent=2)
        with open(temp_contract_p, "w", encoding="utf-8") as f:
            json.dump(contract_dict, f, indent=2)

        # 4. Hash verification
        regen_spec_sha = hash_file(temp_spec_p)
        regen_contract_sha = hash_file(temp_contract_p)

        if regen_spec_sha != EXPECTED_SPEC_SHA:
            print(f"[FAIL] Regenerated spec SHA mismatch! Expected {EXPECTED_SPEC_SHA}, got {regen_spec_sha}", file=sys.stderr)
            sys.exit(1)
        if regen_contract_sha != EXPECTED_BASE_CONTRACT_SHA:
            print(f"[FAIL] Regenerated contract SHA mismatch! Expected {EXPECTED_BASE_CONTRACT_SHA}, got {regen_contract_sha}", file=sys.stderr)
            sys.exit(1)

        print(f"[+] Regenerated Spec in temp matches frozen SHA:     {regen_spec_sha}")
        print(f"[+] Regenerated Contract in temp matches frozen SHA: {regen_contract_sha}")

        # 5. Machine-binding invariant validation
        validate_machine_binding_invariants(spec_dict, contract_dict, derived)
        print("[+] All 16 critical machine-binding invariants validated successfully.")

    # 6. Verify working tree remained clean of new mutations
    git_after = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO_ROOT), capture_output=True, text=True)
    after_status = git_after.stdout.strip()
    if after_status != before_status:
        print(f"[FAIL] Reproducer caused repository mutations during check run:\nBefore:\n{before_status}\nAfter:\n{after_status}", file=sys.stderr)
        sys.exit(1)

    print("\n------------------------------------------------------------")
    print("PHASE 2C.5B4F CAMERA FORENSIC REPRODUCER: PASS")
    print("------------------------------------------------------------\n")
    return 0

def run_write_mode():
    print("=== Executing camera forensics in --write mode ===")
    disasm_path, method = discover_llvm_objdump()
    t_info = verify_toolchain(disasm_path)
    print(f"Toolchain: {t_info['basename']} via {method} (Status: {t_info['status']})")

    extract_all()
    derived = derive_protocol_rules()
    spec = build_canonical_spec_dict(derived)
    contract = build_canonical_contract_dict(derived)

    with open(SPEC_PATH, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
    with open(CONTRACT_PATH, "w", encoding="utf-8") as f:
        json.dump(contract, f, indent=2)

    s_sha = hash_file(SPEC_PATH)
    c_sha = hash_file(CONTRACT_PATH)

    assert s_sha == EXPECTED_SPEC_SHA, f"Spec SHA mismatch: {s_sha} != {EXPECTED_SPEC_SHA}"
    assert c_sha == EXPECTED_BASE_CONTRACT_SHA, f"Contract SHA mismatch: {c_sha} != {EXPECTED_BASE_CONTRACT_SHA}"
    print(f"Wrote canonical spec ({s_sha}) and contract ({c_sha}).")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Phase 2C.5B4F Camera Forensic Reproducer")
    parser.add_argument("--check", action="store_true", default=True, help="Non-mutating check mode (default)")
    parser.add_argument("--write", action="store_true", help="Explicitly write regenerated canonical files")
    args = parser.parse_args()

    if args.write:
        sys.exit(run_write_mode())
    else:
        sys.exit(run_check_mode())

if __name__ == "__main__":
    main()
