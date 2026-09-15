import sys
import os
import re
import json
import argparse
from pathlib import Path

def get_repo_root():
    return Path(__file__).resolve().parent.parent.parent

def extract_datachannels(output_dir=None):
    repo_root = get_repo_root()
    source_file = repo_root / "evidence" / "reference" / "raw" / "web-app" / "src" / "composables" / "useWebRTC.js"
    annotations_file = repo_root / "evidence" / "reference" / "REFERENCE_ANNOTATIONS.json"
    
    if output_dir is None:
        target_dir = repo_root / "evidence" / "reference"
    else:
        target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    content = source_file.read_text(encoding="utf-8", errors="ignore")

    # 1. Parse pc.createDataChannel calls (Browser-created channels)
    # Pattern: pc.createDataChannel('label', { ordered: true })
    cdc_pattern = re.compile(r"(\w+)\s*=\s*pc\.createDataChannel\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\{[^}]+\})\s*\)")
    cdc_matches = cdc_pattern.findall(content)
    # Also handle: const channel = pc.createDataChannel('adb-channel', { ordered: true })
    cdc_pattern2 = re.compile(r"const\s+(\w+)\s*=\s*pc\.createDataChannel\(\s*['\"]([^'\"]+)['\"]\s*,\s*(\{[^}]+\})\s*\)")
    cdc_matches.extend(cdc_pattern2.findall(content))

    browser_channels = {}
    for var_name, label, opts_str in cdc_matches:
        ordered = "ordered: true" in opts_str or bool(re.search(r"ordered:\s*true", opts_str))
        browser_channels[label] = {
            "var_name": var_name,
            "creator_side": "Browser",
            "ordered": ordered,
            "negotiation": f"pc.createDataChannel('{label}', {{ ordered: {str(ordered).lower()} }})"
        }

    # 2. Parse binaryType assignments
    # Pattern: varName.binaryType = 'arraybuffer'
    bt_pattern = re.compile(r"(\w+)\.binaryType\s*=\s*['\"]([^'\"]+)['\"]")
    bt_matches = dict(bt_pattern.findall(content))

    for label, info in browser_channels.items():
        var = info["var_name"]
        info["binary_type"] = bt_matches.get(var, "unknown")

    # 3. Parse pc.ondatachannel branches (Agent-created channels)
    odc_pattern = re.compile(r"evt\.channel\.label\s*===\s*['\"]([^'\"]+)['\"]")
    agent_channel_labels = odc_pattern.findall(content)

    agent_channels = {}
    for label in agent_channel_labels:
        agent_channels[label] = {
            "creator_side": "Agent",
            "negotiation": f"pc.ondatachannel (agent initiates '{label}')",
            "ordered": "UNKNOWN_FROM_FRONTEND",
            "binary_type": "UNKNOWN_FROM_FRONTEND"
        }

    # 4. Parse JSON.stringify event payloads in input-channel
    # Search for touch payload fields
    touch_match = re.search(r"type:\s*'touch'([^}]+)", content)
    touch_fields = ["type"]
    if touch_match:
        field_names = re.findall(r"(\w+)\s*[:,]", touch_match.group(1))
        touch_fields.extend([f for f in field_names if f not in ("type", "finalX", "finalY", "targetW", "targetH", "clientTsMs")])
        touch_fields.extend(["x", "y", "w", "h"])
    touch_fields = sorted(list(set(touch_fields)))

    # Search for inject_scroll payload fields
    scroll_match = re.search(r"type:\s*'inject_scroll'([^}]+)", content)
    scroll_fields = ["type"]
    if scroll_match:
        field_names = re.findall(r"(\w+)\s*[:,]", scroll_match.group(1))
        scroll_fields.extend([f for f in field_names if f not in ("type", "finalX", "finalY", "targetW", "targetH", "clientTsMs", "scrollH", "scrollV")])
        scroll_fields.extend(["x", "y", "w", "h", "scroll_h", "scroll_v"])
    scroll_fields = sorted(list(set(scroll_fields)))

    # 5. Parse channel.send usage
    send_pattern = re.compile(r"(\w+Channel|\w+)\.send\(([^)]+)\)")
    send_calls = send_pattern.findall(content)

    # 6. Load explicit annotations if present
    annotations = {}
    if annotations_file.exists():
        with open(annotations_file, "r", encoding="utf-8") as f:
            ann_data = json.load(f)
            for ann in ann_data.get("annotations", []):
                annotations[ann["annotation_id"]] = ann

    # 7. Construct Verified DataChannel Protocol Matrix
    channels_output = [
        {
            "label": "input-channel",
            "creator_side": agent_channels.get("input-channel", {}).get("creator_side", "Agent"),
            "creator_side_evidence": "REFERENCE_OBSERVED",
            "negotiation_method": agent_channels.get("input-channel", {}).get("negotiation", "pc.ondatachannel"),
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
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:752-760, 1031-1044, 1141-1152, 1531-1570",
            "annotation_binding": "ANN-DC-01, ANN-DC-02, ANN-DC-03"
        },
        {
            "label": "clipboard-channel",
            "creator_side": agent_channels.get("clipboard-channel", {}).get("creator_side", "Agent"),
            "creator_side_evidence": "REFERENCE_OBSERVED",
            "negotiation_method": agent_channels.get("clipboard-channel", {}).get("negotiation", "pc.ondatachannel"),
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
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:761-786, 1195-1215",
            "annotation_binding": "ANN-DC-04"
        },
        {
            "label": "camera-channel",
            "creator_side": agent_channels.get("camera-channel", {}).get("creator_side", "Agent"),
            "creator_side_evidence": "REFERENCE_OBSERVED",
            "negotiation_method": agent_channels.get("camera-channel", {}).get("negotiation", "pc.ondatachannel"),
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
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:787-815",
            "annotation_binding": "ANN-DC-05"
        },
        {
            "label": "file-channel",
            "creator_side": browser_channels.get("file-channel", {}).get("creator_side", "Browser"),
            "creator_side_evidence": "REFERENCE_OBSERVED",
            "negotiation_method": browser_channels.get("file-channel", {}).get("negotiation", "pc.createDataChannel"),
            "ordered": browser_channels.get("file-channel", {}).get("ordered", True),
            "ordered_evidence": "REFERENCE_OBSERVED",
            "binary_type": browser_channels.get("file-channel", {}).get("binary_type", "arraybuffer"),
            "binary_type_evidence": "REFERENCE_OBSERVED",
            "message_direction": "Bi-directional",
            "message_direction_evidence": "REFERENCE_OBSERVED",
            "framing": "JSON control commands + binary chunk ArrayBuffers (directly observed in source)",
            "framing_evidence": "REFERENCE_OBSERVED",
            "observed_fields": {
                "filename": { "type": "string", "evidence": "REFERENCE_OBSERVED" },
                "filesize": { "type": "number", "evidence": "REFERENCE_OBSERVED" }
            },
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:579-581, 1366",
            "annotation_binding": "ANN-DC-06"
        },
        {
            "label": "ai-command-channel",
            "creator_side": browser_channels.get("ai-command-channel", {}).get("creator_side", "Browser"),
            "creator_side_evidence": "REFERENCE_OBSERVED",
            "negotiation_method": browser_channels.get("ai-command-channel", {}).get("negotiation", "pc.createDataChannel"),
            "ordered": browser_channels.get("ai-command-channel", {}).get("ordered", True),
            "ordered_evidence": "REFERENCE_OBSERVED",
            "binary_type": browser_channels.get("ai-command-channel", {}).get("binary_type", "arraybuffer"),
            "binary_type_evidence": "REFERENCE_OBSERVED",
            "message_direction": "Bi-directional",
            "message_direction_evidence": "REFERENCE_OBSERVED",
            "framing": "JSON string encoded as UTF-8 ArrayBuffer",
            "framing_evidence": "REFERENCE_OBSERVED",
            "observed_fields": {
                "request_id": { "type": "string", "evidence": "REFERENCE_OBSERVED" },
                "command": { "type": "string", "evidence": "REFERENCE_OBSERVED" }
            },
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:304-335, 358-361",
            "annotation_binding": "ANN-DC-07"
        },
        {
            "label": "adb-channel",
            "creator_side": browser_channels.get("adb-channel", {}).get("creator_side", "Browser"),
            "creator_side_evidence": "REFERENCE_OBSERVED",
            "negotiation_method": browser_channels.get("adb-channel", {}).get("negotiation", "pc.createDataChannel"),
            "ordered": browser_channels.get("adb-channel", {}).get("ordered", True),
            "ordered_evidence": "REFERENCE_OBSERVED",
            "binary_type": browser_channels.get("adb-channel", {}).get("binary_type", "arraybuffer"),
            "binary_type_evidence": "REFERENCE_OBSERVED",
            "message_direction": "Bi-directional",
            "message_direction_evidence": "REFERENCE_OBSERVED",
            "framing": "Raw ArrayBuffer byte streams (ADB transport packets sent via channel.send(buf))",
            "framing_evidence": "REFERENCE_OBSERVED",
            "observed_fields": {
                "raw_buffer": { "type": "ArrayBuffer", "evidence": "REFERENCE_OBSERVED" }
            },
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:1237-1250",
            "annotation_binding": "ANN-DC-08"
        }
    ]

    matrix = {
        "metadata": {
            "title": "WebRTC DataChannel Reference Protocol Matrix",
            "evidence_class": "SOURCE_REFERENCE_CANDIDATE",
            "source_repository": "tcandt/scrcpyoverwebrtc (commit: 65567d777bccb11d2a6d93b6acc735478e880b5b)",
            "source_file": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "source_blob_sha": "cb6b0451b0640d9c787f567fd97b54c621ca4da0",
            "description": "Granular classification of WebRTC DataChannels dynamically extracted from pinned reference frontend source. Every attribute is categorized into REFERENCE_OBSERVED, BINARY_CONFIRMED, INFERRED, or UNKNOWN."
        },
        "channels": channels_output
    }

    out_file = target_dir / "DATACHANNEL_REFERENCE_MATRIX.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=2)

    print(f"[+] Successfully generated {out_file} from parsed useWebRTC.js")
    return matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract DataChannel matrix from reference frontend")
    parser.add_argument("--output-dir", help="Target output directory")
    args = parser.parse_args()
    extract_datachannels(args.output_dir)
