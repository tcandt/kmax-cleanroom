import sys
import os
import json
import argparse
from pathlib import Path

def get_repo_root():
    return Path(__file__).resolve().parent.parent.parent

def extract_signaling_state_machine(output_dir=None):
    repo_root = get_repo_root()
    if output_dir is None:
        target_dir = repo_root / "evidence" / "reference"
    else:
        target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    sm = {
        "metadata": {
            "title": "Client WebRTC Signaling State Machine Reference",
            "evidence_class": "SOURCE_REFERENCE_CANDIDATE",
            "source_repository": "tcandt/scrcpyoverwebrtc (commit: 65567d777bccb11d2a6d93b6acc735478e880b5b)",
            "source_file": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
            "description": "Deterministic state transitions of browser WebUI during WebRTC connection setup, media negotiation, and control streaming. Timeouts and fallbacks reflect strictly observed source properties."
        },
        "states": [
            "DISCONNECTED",
            "CONNECTING_WS",
            "WS_CONNECTED_SIGNALING",
            "WAITING_OFFER",
            "RECEIVING_OFFER",
            "CREATING_ANSWER",
            "SENDING_ANSWER_TRICKLE_ICE",
            "CONNECTED_P2P",
            "ERROR"
        ],
        "transitions": [
            {
                "transition_id": "T01_CONNECT",
                "from_state": "DISCONNECTED",
                "to_state": "CONNECTING_WS",
                "trigger": "User invokes connect(shareToken, sharePwd)",
                "outbound_message": "WebSocket HTTP Upgrade GET /connect_client?token=<auth_token>",
                "expected_inbound_response": "101 Switching Protocols (WebSocket Handshake Success)",
                "timeout_ms": None,
                "timeout_evidence": "NOT_OBSERVED",
                "fallback": None,
                "fallback_evidence": "NOT_OBSERVED",
                "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:65-88"
            },
            {
                "transition_id": "T02_WS_OPEN",
                "from_state": "CONNECTING_WS",
                "to_state": "WS_CONNECTED_SIGNALING",
                "trigger": "ws.onopen event fired",
                "outbound_message": {
                    "message_type": "connect",
                    "device_id": "<target_device_id>"
                },
                "expected_inbound_response": {
                    "message_type": "config",
                    "ice_servers": "array of STUN/TURN definitions"
                },
                "timeout_ms": None,
                "timeout_evidence": "NOT_OBSERVED",
                "fallback": None,
                "fallback_evidence": "NOT_OBSERVED",
                "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:89-95"
            },
            {
                "transition_id": "T03_CONFIG_RECEIVED",
                "from_state": "WS_CONNECTED_SIGNALING",
                "to_state": "WAITING_OFFER",
                "trigger": "Received message_type: 'config'",
                "outbound_message": {
                    "message_type": "forward",
                    "device_id": "<target_device_id>",
                    "payload": {
                        "type": "request-offer",
                        "ip_preference": "auto | ipv4 | ipv6",
                        "scrcpy_options": "{...}"
                    }
                },
                "expected_inbound_response": {
                    "message_type": "device_msg",
                    "payload": {
                        "type": "offer",
                        "sdp": "v=0...",
                        "camera_support": True
                    }
                },
                "timeout_ms": None,
                "timeout_evidence": "NOT_OBSERVED",
                "fallback": None,
                "fallback_evidence": "NOT_OBSERVED",
                "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:126-141"
            },
            {
                "transition_id": "T04_OFFER_RECEIVED",
                "from_state": "WAITING_OFFER",
                "to_state": "CREATING_ANSWER",
                "trigger": "Received message_type: 'device_msg' with payload.type == 'offer'",
                "outbound_message": "None (internal RTCPeerConnection creation and SDP munging)",
                "expected_inbound_response": "pc.createAnswer() promise resolution",
                "timeout_ms": None,
                "timeout_evidence": "NOT_OBSERVED",
                "fallback": "Transition to ERROR on SDP error exception",
                "fallback_evidence": "REFERENCE_OBSERVED",
                "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:175-200"
            },
            {
                "transition_id": "T05_SEND_ANSWER",
                "from_state": "CREATING_ANSWER",
                "to_state": "SENDING_ANSWER_TRICKLE_ICE",
                "trigger": "pc.setLocalDescription(newAnswer) resolves",
                "outbound_message": {
                    "message_type": "forward",
                    "device_id": "<target_device_id>",
                    "payload": {
                        "type": "answer",
                        "sdp": "<munged_sdp_with_bitrate_settings>"
                    }
                },
                "expected_inbound_response": "Trickle ICE candidate exchange: device_msg with payload.type == 'ice-candidate'",
                "timeout_ms": None,
                "timeout_evidence": "NOT_OBSERVED",
                "fallback": None,
                "fallback_evidence": "NOT_OBSERVED",
                "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:201-213"
            },
            {
                "transition_id": "T06_ICE_EXCHANGE",
                "from_state": "SENDING_ANSWER_TRICKLE_ICE",
                "to_state": "CONNECTED_P2P",
                "trigger": "pc.connectionState === 'connected' and pc.ontrack fired",
                "outbound_message": {
                    "message_type": "forward",
                    "device_id": "<target_device_id>",
                    "payload": {
                        "type": "ice-candidate",
                        "candidate": "<local_ice_candidate>"
                    }
                },
                "expected_inbound_response": "Agent opens DataChannels (input-channel, clipboard-channel)",
                "timeout_ms": None,
                "timeout_evidence": "NOT_OBSERVED",
                "fallback": "Sends message_type: 'webrtc_failed' if connection fails (no automatic protocol switch observed in frontend)",
                "fallback_evidence": "REFERENCE_OBSERVED",
                "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:215-227, 725-748"
            },
            {
                "transition_id": "T07_COMMAND_EXECUTION",
                "from_state": "CONNECTED_P2P",
                "to_state": "CONNECTED_P2P",
                "trigger": "User or AI dispatches shell command via executeCommandP2P()",
                "outbound_message": "ai-command-channel: JSON {'request_id': reqId, 'command': cmd} (Fallback: WS message_type: 'command')",
                "expected_inbound_response": "ai-command-channel: JSON {'request_id': reqId, 'output': '...', 'exit_code': 0}",
                "timeout_ms": 15000,
                "timeout_evidence": "REFERENCE_OBSERVED",
                "fallback": "aiCommandPromises timer fires at 15000ms; rejects promise with timeout error",
                "fallback_evidence": "REFERENCE_OBSERVED",
                "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:339-369"
            },
            {
                "transition_id": "T08_TERMINATION",
                "from_state": "ANY",
                "to_state": "DISCONNECTED",
                "trigger": "User clicks Disconnect or window unloads",
                "outbound_message": "ws.close() and pc.close()",
                "expected_inbound_response": "Cleanup of active streams, channels, and event listeners",
                "timeout_ms": None,
                "timeout_evidence": "NOT_OBSERVED",
                "fallback": None,
                "fallback_evidence": "NOT_OBSERVED",
                "source_reference": "evidence/reference/raw/web-app/src/composables/useWebRTC.js:740-748"
            }
        ]
    }

    out_file = target_dir / "CLIENT_SIGNALING_STATE_MACHINE.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(sm, f, indent=2)

    print(f"[+] Successfully generated {out_file}")
    return sm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract signaling state machine from reference frontend")
    parser.add_argument("--output-dir", help="Target output directory")
    args = parser.parse_args()
    extract_signaling_state_machine(args.output_dir)
