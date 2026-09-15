import sys
import os
import json
import argparse
from pathlib import Path

def get_repo_root():
    return Path(__file__).resolve().parent.parent.parent

def extract_datachannels(output_dir=None):
    repo_root = get_repo_root()
    if output_dir is None:
        target_dir = repo_root / "evidence" / "reference"
    else:
        target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    matrix = {
        "metadata": {
            "title": "WebRTC DataChannel Reference Protocol Matrix",
            "evidence_class": "SOURCE_REFERENCE_CANDIDATE",
            "source_repository": "tcandt/scrcpyoverwebrtc (commit: 65567d777bccb11d2a6d93b6acc735478e880b5b)",
            "source_file": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "description": "Granular classification of WebRTC DataChannels extracted from reference frontend. Every attribute is categorized into REFERENCE_OBSERVED, BINARY_CONFIRMED, INFERRED, or UNKNOWN."
        },
        "channels": [
            {
                "label": "input-channel",
                "creator_side": "Agent",
                "creator_side_evidence": "REFERENCE_OBSERVED",
                "negotiation_method": "pc.ondatachannel (agent initiates)",
                "ordered": "UNKNOWN_FROM_FRONTEND",
                "ordered_evidence": "UNKNOWN",
                "binary_type": "UNKNOWN_FROM_FRONTEND",
                "binary_type_evidence": "UNKNOWN",
                "message_direction": "Browser -> Agent",
                "message_direction_evidence": "REFERENCE_OBSERVED",
                "framing": "JSON string payload (JSON.stringify) dispatched via inputChannel.send(msg)",
                "framing_evidence": "REFERENCE_OBSERVED",
                "observed_events": {
                    "touch": {
                        "type": { "value": "touch", "evidence": "REFERENCE_OBSERVED" },
                        "id": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "seq": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "client_ts_ms": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "action": { "type": "number (0=DOWN, 1=UP, 2=MOVE)", "evidence": "REFERENCE_OBSERVED" },
                        "x": { "type": "number (logical coordinate)", "evidence": "REFERENCE_OBSERVED" },
                        "y": { "type": "number (logical coordinate)", "evidence": "REFERENCE_OBSERVED" },
                        "w": { "type": "number (logical target width)", "evidence": "REFERENCE_OBSERVED" },
                        "h": { "type": "number (logical target height)", "evidence": "REFERENCE_OBSERVED" }
                    },
                    "inject_scroll": {
                        "type": { "value": "inject_scroll", "evidence": "REFERENCE_OBSERVED" },
                        "seq": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "client_ts_ms": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "x": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "y": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "w": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "h": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "scroll_h": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "scroll_v": { "type": "number", "evidence": "REFERENCE_OBSERVED" }
                    },
                    "inject_text": {
                        "type": { "value": "inject_text", "evidence": "REFERENCE_OBSERVED" },
                        "text": { "type": "string", "evidence": "REFERENCE_OBSERVED" }
                    },
                    "inject_keycode": {
                        "type": { "value": "inject_keycode", "evidence": "REFERENCE_OBSERVED" },
                        "action": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "keycode": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "repeat": { "type": "number", "evidence": "REFERENCE_OBSERVED" },
                        "meta": { "type": "number", "evidence": "REFERENCE_OBSERVED" }
                    }
                },
                "binary_control_alternative": {
                    "status": "UNPROVEN_HYPOTHESIS",
                    "evidence": "INFERRED",
                    "notes": "Prior hypothesis of binary control packet framing is unobserved in reference frontend and requires agent binary verification before adoption."
                },
                "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:752-760, 1031-1044, 1141-1152, 1531-1570"
            },
            {
                "label": "clipboard-channel",
                "creator_side": "Agent",
                "creator_side_evidence": "REFERENCE_OBSERVED",
                "negotiation_method": "pc.ondatachannel (agent initiates)",
                "ordered": "UNKNOWN_FROM_FRONTEND",
                "ordered_evidence": "UNKNOWN",
                "binary_type": "UNKNOWN_FROM_FRONTEND",
                "binary_type_evidence": "UNKNOWN",
                "message_direction": "Bi-directional (Agent <-> Browser)",
                "message_direction_evidence": "REFERENCE_OBSERVED",
                "framing": "JSON string or UTF-8 ArrayBuffer representing JSON object",
                "framing_evidence": "REFERENCE_OBSERVED",
                "observed_fields": {
                    "type": { "value": "clipboard", "evidence": "REFERENCE_OBSERVED" },
                    "text": { "type": "string", "evidence": "REFERENCE_OBSERVED" },
                    "source": { "type": "string ('device' | 'web')", "evidence": "REFERENCE_OBSERVED" },
                    "origin_client_id": { "type": "string | null", "evidence": "REFERENCE_OBSERVED" }
                },
                "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:761-786, 1195-1215"
            },
            {
                "label": "camera-channel",
                "creator_side": "Agent",
                "creator_side_evidence": "REFERENCE_OBSERVED",
                "negotiation_method": "pc.ondatachannel (agent initiates)",
                "ordered": "UNKNOWN_FROM_FRONTEND",
                "ordered_evidence": "UNKNOWN",
                "binary_type": "UNKNOWN_FROM_FRONTEND",
                "binary_type_evidence": "UNKNOWN",
                "message_direction": "Bi-directional (Agent sends control commands; Browser sends video feed frames)",
                "message_direction_evidence": "REFERENCE_OBSERVED",
                "framing": "JSON control messages for handshake; binary raw video frames for streaming",
                "framing_evidence": "REFERENCE_OBSERVED",
                "observed_fields": {
                    "action": { "type": "string ('start' | 'stop')", "evidence": "REFERENCE_OBSERVED" }
                },
                "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:787-815"
            },
            {
                "label": "file-channel",
                "creator_side": "Browser",
                "creator_side_evidence": "REFERENCE_OBSERVED",
                "negotiation_method": "pc.createDataChannel('file-channel', { ordered: true })",
                "ordered": True,
                "ordered_evidence": "REFERENCE_OBSERVED",
                "binary_type": "arraybuffer",
                "binary_type_evidence": "REFERENCE_OBSERVED",
                "message_direction": "Bi-directional",
                "message_direction_evidence": "REFERENCE_OBSERVED",
                "framing": "JSON control commands + binary chunk ArrayBuffers (directly observed in source)",
                "framing_evidence": "REFERENCE_OBSERVED",
                "observed_fields": {
                    "filename": { "type": "string", "evidence": "REFERENCE_OBSERVED" },
                    "filesize": { "type": "number", "evidence": "REFERENCE_OBSERVED" }
                },
                "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:579-581, 1366"
            },
            {
                "label": "ai-command-channel",
                "creator_side": "Browser",
                "creator_side_evidence": "REFERENCE_OBSERVED",
                "negotiation_method": "pc.createDataChannel('ai-command-channel', { ordered: true })",
                "ordered": True,
                "ordered_evidence": "REFERENCE_OBSERVED",
                "binary_type": "arraybuffer",
                "binary_type_evidence": "REFERENCE_OBSERVED",
                "message_direction": "Bi-directional",
                "message_direction_evidence": "REFERENCE_OBSERVED",
                "framing": "JSON string encoded as UTF-8 ArrayBuffer",
                "framing_evidence": "REFERENCE_OBSERVED",
                "observed_fields": {
                    "request_id": { "type": "string", "evidence": "REFERENCE_OBSERVED" },
                    "command": { "type": "string", "evidence": "REFERENCE_OBSERVED" }
                },
                "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:304-335, 358-361"
            },
            {
                "label": "adb-channel",
                "creator_side": "Browser",
                "creator_side_evidence": "REFERENCE_OBSERVED",
                "negotiation_method": "pc.createDataChannel('adb-channel', { ordered: true })",
                "ordered": True,
                "ordered_evidence": "REFERENCE_OBSERVED",
                "binary_type": "arraybuffer",
                "binary_type_evidence": "REFERENCE_OBSERVED",
                "message_direction": "Bi-directional",
                "message_direction_evidence": "REFERENCE_OBSERVED",
                "framing": "Raw ArrayBuffer byte streams (ADB transport packets sent via channel.send(buf))",
                "framing_evidence": "REFERENCE_OBSERVED",
                "observed_fields": {
                    "raw_buffer": { "type": "ArrayBuffer", "evidence": "REFERENCE_OBSERVED" }
                },
                "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:1237-1250"
            }
        ]
    }

    out_file = target_dir / "DATACHANNEL_REFERENCE_MATRIX.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)

    print(f"[+] Successfully generated {out_file}")
    return matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract DataChannel matrix from reference frontend")
    parser.add_argument("--output-dir", help="Target output directory")
    args = parser.parse_args()
    extract_datachannels(args.output_dir)
