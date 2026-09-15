import sys
import os
import json
import argparse
from pathlib import Path

def get_repo_root():
    return Path(__file__).resolve().parent.parent.parent

VALID_EVIDENCE_CLASSES = {
    "PUBLIC_REFERENCE",
    "BINARY_STRING",
    "BINARY_XREF",
    "PCLNTAB_SYMBOL",
    "ROUTE_REGISTRATION",
    "DISASSEMBLY_CONTROL_FLOW",
    "TYPE_DESCRIPTOR",
    "DYNAMIC_ORACLE",
    "NETWORK_CAPTURE"
}

def build_reference_crossmap(output_dir=None):
    repo_root = get_repo_root()
    if output_dir is None:
        target_dir = repo_root / "evidence" / "reference"
    else:
        target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    mappings_data = [
        {
            "reference_item": "/connect_client",
            "category": "TRANSPORT_ROUTE",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:78",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "ROUTE_REGISTRATION: HandleFunc('/connect_client', closure_va: 0x848500)",
                "DISASSEMBLY_CONTROL_FLOW: Upgrades HTTP to WebSocket, parses token/share_token parameters",
                "DYNAMIC_ORACLE: Dynamic prober returns 400 Bad Request on missing handshake parameters"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "ROUTE_REGISTRATION",
                "DISASSEMBLY_CONTROL_FLOW",
                "DYNAMIC_ORACLE"
            ]
        },
        {
            "reference_item": "/register_agent",
            "category": "TRANSPORT_ROUTE",
            "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "ROUTE_REGISTRATION: HandleFunc('/register_agent', closure_va: 0x848540)",
                "DISASSEMBLY_CONTROL_FLOW: Upgrades HTTP to WebSocket, validates agent id, registers into global in-memory session map"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "ROUTE_REGISTRATION",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "/api/login",
            "category": "TRANSPORT_ROUTE",
            "reference_source": "evidence/reference/raw/web-app/src/stores/auth.js:25",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "ROUTE_REGISTRATION: HandleFunc('/api/login', closure_va: 0x8484e0)",
                "DYNAMIC_ORACLE: POST with valid credentials returns 200 OK with session token; invalid returns 400",
                "DISASSEMBLY_CONTROL_FLOW: main.ltOjwqsMl5q8 parses credentials and invokes session token generator"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "ROUTE_REGISTRATION",
                "DYNAMIC_ORACLE",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "/api/devices",
            "category": "TRANSPORT_ROUTE",
            "reference_source": "evidence/reference/raw/web-app/src/stores/devices.js:45",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "ROUTE_REGISTRATION: HandleFunc('/api/devices', closure_va: 0x848520)",
                "DYNAMIC_ORACLE: GET with valid session returns device inventory array",
                "DISASSEMBLY_CONTROL_FLOW: Serializes registered agent list to JSON"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "ROUTE_REGISTRATION",
                "DYNAMIC_ORACLE",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "/api/tags",
            "category": "TRANSPORT_ROUTE",
            "reference_source": "evidence/reference/raw/web-app/src/stores/tags.js:65",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "ROUTE_REGISTRATION: HandleFunc('/api/tags', closure_va: 0x848560)",
                "DYNAMIC_ORACLE: Returns device_tags JSON array from persistence store"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "ROUTE_REGISTRATION",
                "DYNAMIC_ORACLE"
            ]
        },
        {
            "reference_item": "/api/share/create",
            "category": "TRANSPORT_ROUTE",
            "reference_source": "evidence/reference/raw/web-app/src/stores/devices.js:750",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "ROUTE_REGISTRATION: HandleFunc('/api/share/create', closure_va: 0x848580)",
                "DYNAMIC_ORACLE: Creates temporary share token entry in persistence store"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "ROUTE_REGISTRATION",
                "DYNAMIC_ORACLE"
            ]
        },
        {
            "reference_item": "/api/admin/users",
            "category": "TRANSPORT_ROUTE",
            "reference_source": "evidence/reference/raw/web-app/src/views/DeviceClient.vue",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "ROUTE_REGISTRATION: HandleFunc('/api/admin/users', closure_va: 0x8485a0)",
                "DYNAMIC_ORACLE: Authenticated admin request lists user accounts"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "ROUTE_REGISTRATION",
                "DYNAMIC_ORACLE"
            ]
        },
        {
            "reference_item": "message_type: forward",
            "category": "WEBSOCKET_MESSAGE",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:140",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'forward' in signaling .rodata",
                "DISASSEMBLY_CONTROL_FLOW: Dispatcher in main.main.func1 unmarshals target_device_id and forwards payload"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "message_type: command",
            "category": "WEBSOCKET_MESSAGE",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:271",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling & android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Strings 'command' and 'request_id' in signaling and agent .rodata",
                "DISASSEMBLY_CONTROL_FLOW: Signaling relays command packet to registered agent socket"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "message_type: inject_data",
            "category": "WEBSOCKET_MESSAGE",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:254",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'inject_data' in signaling .rodata",
                "DISASSEMBLY_CONTROL_FLOW: Dispatches input/clipboard injection to agent socket"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "message_type: config",
            "category": "WEBSOCKET_MESSAGE",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:126",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'config' and 'ice_servers' in signaling .rodata",
                "DISASSEMBLY_CONTROL_FLOW: Sends STUN/TURN server list to connecting browser client"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "message_type: device_msg",
            "category": "WEBSOCKET_MESSAGE",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:133",
            "binary_target": "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'device_msg' in signaling .rodata",
                "DISASSEMBLY_CONTROL_FLOW: Relays agent payload to associated client session"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "payload: request-offer",
            "category": "SIGNALING_PAYLOAD",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:134",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'request-offer' present in agent .rodata",
                "BINARY_XREF: Triggers Agent WebRTC stack to initialize PeerConnection and generate SDP offer"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "payload: offer",
            "category": "SIGNALING_PAYLOAD",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:175",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'offer' and 'sdp' present in agent .rodata",
                "BINARY_XREF: Agent formats SDP offer and transmits back through signaling"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "payload: answer",
            "category": "SIGNALING_PAYLOAD",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:205",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'answer' present in agent .rodata",
                "BINARY_XREF: Agent calls setRemoteDescription with browser answer"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "payload: ice-candidate",
            "category": "SIGNALING_PAYLOAD",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:215",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'candidate' and 'candidateType' in agent .rodata",
                "BINARY_XREF: Agent registers trickle ICE candidate into PeerConnection"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "channel: input-channel",
            "category": "DATACHANNEL",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:752",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'input-channel' in agent .rodata at offset 0x75a593",
                "BINARY_XREF: Agent calls CreateDataChannel('input-channel') and attaches touch dispatcher"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "channel: clipboard-channel",
            "category": "DATACHANNEL",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:761",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'clipboard-channel' in agent .rodata",
                "BINARY_XREF: Agent creates channel and hooks Android clipboard service"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "channel: camera-channel",
            "category": "DATACHANNEL",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:787",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'camera-channel' in agent .rodata",
                "BINARY_XREF: Agent connects to virtual camera HAL injection socket"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "channel: file-channel",
            "category": "DATACHANNEL",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:579",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'file-channel' in agent .rodata"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING"
            ]
        },
        {
            "reference_item": "channel: ai-command-channel",
            "category": "DATACHANNEL",
            "reference_source": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:304",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: Literal string 'ai-command-channel' in agent .rodata",
                "DISASSEMBLY_CONTROL_FLOW: Agent listens for shell execution JSON and pipes to /system/bin/sh"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "DISASSEMBLY_CONTROL_FLOW"
            ]
        },
        {
            "reference_item": "flag: -id",
            "category": "AGENT_CLI",
            "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: String '-id' in agent .rodata",
                "BINARY_XREF: CP_AGENT_ID environment variable fallback confirmed in adjacent .rodata"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "flag: -signaling",
            "category": "AGENT_CLI",
            "reference_source": "evidence/reference/raw/docs/agent-deploy.md:65",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: String '-signaling' in agent .rodata",
                "BINARY_XREF: Passes signaling URL to WebSocket dialer"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        },
        {
            "reference_item": "flag: -root",
            "category": "AGENT_CLI",
            "reference_source": "evidence/reference/raw/docs/agent-deploy.md:118",
            "binary_target": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
            "binary_evidence": [
                "BINARY_STRING: String '-root' in agent .rodata",
                "BINARY_XREF: CP_AGENT_ROOT environment variable fallback confirmed"
            ],
            "evidence_classes": [
                "PUBLIC_REFERENCE",
                "BINARY_STRING",
                "BINARY_XREF"
            ]
        }
    ]

    # Process statuses according to strong multi-evidence gate
    mappings = []
    confirmed_count = 0
    corroborated_count = 0

    for m in mappings_data:
        ev_classes = m.get("evidence_classes", [])
        for c in ev_classes:
            if c not in VALID_EVIDENCE_CLASSES:
                raise ValueError(f"Invalid evidence class: {c}")
        
        has_ref = "PUBLIC_REFERENCE" in ev_classes
        binary_classes = [c for c in ev_classes if c != "PUBLIC_REFERENCE"]

        if has_ref and len(binary_classes) >= 2:
            status = "BINARY_SEMANTIC_CONFIRMED"
            confirmed_count += 1
        elif has_ref and len(binary_classes) >= 1:
            status = "REFERENCE_CORROBORATED"
            corroborated_count += 1
        else:
            status = "UNCONFIRMED_HYPOTHESIS"

        entry = dict(m)
        entry["status"] = status
        mappings.append(entry)

    crossmap = {
        "metadata": {
            "title": "Reference to Binary Granular Multi-Evidence Crossmap",
            "description": "Cross-verification of public reference intelligence against granular binary static and dynamic evidence classes",
            "multi_evidence_rule": "BINARY_SEMANTIC_CONFIRMED requires PUBLIC_REFERENCE + >=2 independent binary classes. REFERENCE_CORROBORATED requires PUBLIC_REFERENCE + >=1 binary class.",
            "total_items": len(mappings),
            "binary_semantic_confirmed_items": confirmed_count,
            "reference_corroborated_items": corroborated_count,
            "unconfirmed_items": len(mappings) - confirmed_count - corroborated_count
        },
        "mappings": mappings
    }

    out_file = target_dir / "REFERENCE_TO_BINARY_CROSSMAP.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(crossmap, f, indent=2)

    print(f"[+] Successfully generated {out_file} ({confirmed_count} semantic confirmed, {corroborated_count} corroborated)")
    return crossmap

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Reference to Binary Crossmap with granular evidence classes")
    parser.add_argument("--output-dir", help="Target output directory")
    args = parser.parse_args()
    build_reference_crossmap(args.output_dir)
