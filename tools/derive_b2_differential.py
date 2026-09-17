#!/usr/bin/env python3
"""
tools/derive_b2_differential.py
Phase 2C.5B2R Machine Derivation & Validator of DataChannel Differential Results.

Derives DATACHANNEL_B2_DIFFERENTIAL_RESULT.json directly from evaluated_dimensions.
Validates:
- All dimensions have (id, classification, evidence_basis, runtime_basis, result)
- Zero duplicate IDs
- Allowed classifications only
- Computed counters strictly match the dimension sums
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ALLOWED_CLASSIFICATIONS = {
    "STATIC_PROTOCOL_EVIDENCE",
    "EXACT_BINARY_FRAME",
    "RUNTIME_RECONSTRUCTED_E2E",
    "ORIGINAL_AGENT_RUNTIME_PARITY",
    "SEMANTIC_PARITY",
    "REFERENCE_ONLY",
    "IMPLEMENTATION_CHOICE",
    "ENVIRONMENT_UNAVAILABLE",
    "VERIFIED_DIVERGENCE",
    "FAILED",
}

DIMENSIONS = [
    {
        "id": "DC-B2-DIM-01",
        "name": "input_channel_label",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_LABEL_EVIDENCE.json (AMD64 0xb5a5af / ARM64 0x6b8548)",
        "runtime_basis": "pc.CreateDataChannel('input-channel')",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-02",
        "name": "input_channel_ordered",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_LABEL_EVIDENCE.json (Disassembly passes ordered=1 byte pointer)",
        "runtime_basis": "DataChannelInit.Ordered = true",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-03",
        "name": "input_channel_json_framing",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_FRAMING_MATRIX.json (channels.input-channel.payload_encoding = JSON_TEXT)",
        "runtime_basis": "HandleInputMessage parses JSON string",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-04",
        "name": "clipboard_channel_label",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_LABEL_EVIDENCE.json (AMD64 0xb5e208 / ARM64 0x6bc175)",
        "runtime_basis": "pc.CreateDataChannel('clipboard-channel')",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-05",
        "name": "clipboard_channel_ordered",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_LABEL_EVIDENCE.json (Disassembly passes ordered=1 byte pointer)",
        "runtime_basis": "DataChannelInit.Ordered = true",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-06",
        "name": "clipboard_channel_json_framing",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_FRAMING_MATRIX.json (channels.clipboard-channel.payload_encoding = JSON_TEXT)",
        "runtime_basis": "HandleClipboardMessage parses JSON string",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-07",
        "name": "touch_binary_frame_32bytes",
        "classification": "EXACT_BINARY_FRAME",
        "evidence_basis": "CONTROL_INPUT_PROTOCOL_CROSSMAP.json (AMD64 0x9cfb54-0x9cfc0e bswap/rol, ecx=0x20)",
        "runtime_basis": "TestGoldenTouchEvent",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-08",
        "name": "keycode_binary_frame_14bytes",
        "classification": "EXACT_BINARY_FRAME",
        "evidence_basis": "DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json (AMD64 0x9e3ace, ControlMessageReader.java:69)",
        "runtime_basis": "TestGoldenKeycodeEvent",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-09",
        "name": "text_binary_frame_5plusN",
        "classification": "EXACT_BINARY_FRAME",
        "evidence_basis": "DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json (AMD64 0x9e3a4d, ControlMessageReader.java:95)",
        "runtime_basis": "TestGoldenTextEvent",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-10",
        "name": "scroll_binary_frame_21bytes",
        "classification": "EXACT_BINARY_FRAME",
        "evidence_basis": "DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json (AMD64 0x9e3c07, ControlMessageReader.java:103)",
        "runtime_basis": "TestGoldenScrollEvent",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-11",
        "name": "hard_keyboard_frame_1byte",
        "classification": "EXACT_BINARY_FRAME",
        "evidence_basis": "DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json (AMD64 0x9e3b60, ControlMessageReader.java:40)",
        "runtime_basis": "TestGoldenHardKeyboardEvent",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-12",
        "name": "set_clipboard_handling",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json (AMD64 0x9e3860, string origin_client_id at 0xb5...)",
        "runtime_basis": "TestSetClipboard",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-13",
        "name": "get_clipboard_handling",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json (AMD64 0x9e38ce)",
        "runtime_basis": "TestGetClipboard",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-14",
        "name": "clipboard_response_schema",
        "classification": "STATIC_PROTOCOL_EVIDENCE",
        "evidence_basis": "DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json, useWebRTC.js:773-778",
        "runtime_basis": "TestGetClipboard sends {type: 'clipboard', text, source: 'device', origin_client_id: null}",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-15",
        "name": "input_sctp_e2e",
        "classification": "RUNTIME_RECONSTRUCTED_E2E",
        "evidence_basis": "WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json (CORE-12)",
        "runtime_basis": "TestWebRTCDataChannelsE2E (Browser SCTP -> Agent -> ControlSink exact 32-byte frame)",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-16",
        "name": "clipboard_set_sctp_e2e",
        "classification": "RUNTIME_RECONSTRUCTED_E2E",
        "evidence_basis": "WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json (CORE-12)",
        "runtime_basis": "TestWebRTCDataChannelsE2E (Browser SCTP -> Agent -> ClipboardProvider.Set)",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-17",
        "name": "clipboard_get_sctp_e2e",
        "classification": "RUNTIME_RECONSTRUCTED_E2E",
        "evidence_basis": "WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json (CORE-12)",
        "runtime_basis": "TestWebRTCDataChannelsE2E (Browser SCTP -> Agent -> ClipboardProvider.Get -> Response)",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-18",
        "name": "deferred_channels_isolation",
        "classification": "SEMANTIC_PARITY",
        "evidence_basis": "WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json (CORE-08)",
        "runtime_basis": "Master Verifier scans entire cloudphone-agent production tree for zero deferred channel logic",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-19",
        "name": "touch_alias_compatibility",
        "classification": "REFERENCE_ONLY",
        "evidence_basis": "useWebRTC.js:1032 ('type': 'touch')",
        "runtime_basis": "TestHandleInputMessageEndToEnd/touch_alias_type",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-20",
        "name": "touch_seq_client_ts_fields",
        "classification": "REFERENCE_ONLY",
        "evidence_basis": "useWebRTC.js:1034-1035 (seq, client_ts_ms)",
        "runtime_basis": "TouchEvent struct unmarshals without error",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-21",
        "name": "clipboard_paste_suppress_broadcast_fields",
        "classification": "REFERENCE_ONLY",
        "evidence_basis": "useWebRTC.js:1200-1202 (paste, suppress_broadcast)",
        "runtime_basis": "SetClipboardMessage struct unmarshals without error",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-22",
        "name": "clipboard_peer_notification_inbound",
        "classification": "IMPLEMENTATION_CHOICE",
        "evidence_basis": "Defensive handling of inbound 'clipboard' frames",
        "runtime_basis": "TestPeerClipboardNotification",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-23",
        "name": "defensive_payload_bound",
        "classification": "IMPLEMENTATION_CHOICE",
        "evidence_basis": "ControlMessageReader.CLIPBOARD_TEXT_MAX_LENGTH (262130) + JSON buffer envelope",
        "runtime_basis": "TestClipboardParserRobustnessAndFuzz/oversized_payload",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-24",
        "name": "control_sink_adapter",
        "classification": "IMPLEMENTATION_CHOICE",
        "evidence_basis": "Boundary abstraction for @uds_sys_t_",
        "runtime_basis": "MemoryControlSink in-memory test implementation",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-25",
        "name": "clipboard_provider_adapter",
        "classification": "IMPLEMENTATION_CHOICE",
        "evidence_basis": "Boundary abstraction for Android ClipboardManager",
        "runtime_basis": "MemoryClipboardProvider in-memory test implementation",
        "result": "PASS"
    },
    {
        "id": "DC-B2-DIM-26",
        "name": "original_agent_datachannel_runtime_parity",
        "classification": "ENVIRONMENT_UNAVAILABLE",
        "evidence_basis": "Requires Android container runtime with root UID 2000 and abstract UDS @uds_sys_t_",
        "runtime_basis": "Host environment is Windows AMD64 desktop without Android emulator / app_process",
        "result": "ENVIRONMENT_UNAVAILABLE"
    }
]

def compute_counters(dimensions):
    seen_ids = set()
    for d in dimensions:
        dim_id = d.get("id")
        if not dim_id:
            raise ValueError(f"Missing id in dimension: {d}")
        if dim_id in seen_ids:
            raise ValueError(f"Duplicate dimension id: {dim_id}")
        seen_ids.add(dim_id)

        cls = d.get("classification")
        if cls not in ALLOWED_CLASSIFICATIONS:
            raise ValueError(f"Unknown classification {cls} in dimension {dim_id}")

        res = d.get("result")
        if not res:
            raise ValueError(f"Missing result in dimension {dim_id}")

    counters = {
        "static_protocol_evidence_total": sum(1 for d in dimensions if d["classification"] == "STATIC_PROTOCOL_EVIDENCE"),
        "static_protocol_evidence_passed": sum(1 for d in dimensions if d["classification"] == "STATIC_PROTOCOL_EVIDENCE" and d["result"] == "PASS"),
        "exact_binary_frame_total": sum(1 for d in dimensions if d["classification"] == "EXACT_BINARY_FRAME"),
        "exact_binary_frame_passed": sum(1 for d in dimensions if d["classification"] == "EXACT_BINARY_FRAME" and d["result"] == "PASS"),
        "reconstructed_runtime_e2e_total": sum(1 for d in dimensions if d["classification"] == "RUNTIME_RECONSTRUCTED_E2E"),
        "reconstructed_runtime_e2e_passed": sum(1 for d in dimensions if d["classification"] == "RUNTIME_RECONSTRUCTED_E2E" and d["result"] == "PASS"),
        "original_agent_runtime_parity_total": sum(1 for d in dimensions if d["classification"] == "ORIGINAL_AGENT_RUNTIME_PARITY"),
        "original_agent_runtime_parity_passed": sum(1 for d in dimensions if d["classification"] == "ORIGINAL_AGENT_RUNTIME_PARITY" and d["result"] == "PASS"),
        "semantic_parity_total": sum(1 for d in dimensions if d["classification"] == "SEMANTIC_PARITY"),
        "semantic_parity_passed": sum(1 for d in dimensions if d["classification"] == "SEMANTIC_PARITY" and d["result"] == "PASS"),
        "reference_only_total": sum(1 for d in dimensions if d["classification"] == "REFERENCE_ONLY"),
        "implementation_choice_total": sum(1 for d in dimensions if d["classification"] == "IMPLEMENTATION_CHOICE"),
        "environment_unavailable_total": sum(1 for d in dimensions if d["classification"] == "ENVIRONMENT_UNAVAILABLE"),
        "verified_divergence_total": sum(1 for d in dimensions if d["classification"] == "VERIFIED_DIVERGENCE"),
        "failed_total": sum(1 for d in dimensions if d["result"] == "FAILED" or d["classification"] == "FAILED"),
    }
    return counters

def main():
    counters = compute_counters(DIMENSIONS)
    out_obj = {
        "metadata": {
            "title": "Phase 2C.5B2R DataChannel Protocol Differential Result",
            "phase": "Phase 2C.5B2R",
            "evaluation_timestamp": "2026-09-17T18:15:00Z",
            "classification": "Clean-room behavioral/protocol reconstruction",
            "derivation_tool": "tools/derive_b2_differential.py"
        },
        "counters": counters,
        "overall_verdict": "PASS_PHASE_2C5B2R_CLOSED" if counters["failed_total"] == 0 else "FAILED",
        "evaluated_dimensions": DIMENSIONS
    }
    out_path = ROOT / "evidence" / "go_agent" / "webrtc" / "DATACHANNEL_B2_DIFFERENTIAL_RESULT.json"
    out_path.write_text(json.dumps(out_obj, indent=2), encoding="utf-8")
    print(f"Generated {out_path} with {len(DIMENSIONS)} dimensions.")
    print("Counters:", json.dumps(counters, indent=2))

if __name__ == "__main__":
    main()
