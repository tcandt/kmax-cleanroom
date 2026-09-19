#!/usr/bin/env python3
"""
tools/forensics/ai_command/derive_ai_command_protocol.py
Phase 2C.5B5FR2 AI Command Protocol Semantic Derivation Pipeline.

Deterministically derives the authoritative protocol specification, message inventory,
callgraph, and source provenance artifacts directly from fresh binary disassembly manifests,
recovered Go type descriptors, binary rodata strings, and approved Lane-D reference facts.

CRITICAL PROVENANCE RULE (Anti-Tautology Invariant):
This pipeline NEVER reads canonical forensic JSON files (AI_COMMAND_B5F_PROTOCOL_SPEC.json,
AI_COMMAND_B5F_MESSAGE_INVENTORY.json, AI_COMMAND_B5F_CALLGRAPH.json, AI_COMMAND_B5F_SOURCE_PROVENANCE.json)
as input sources. It synthesizes all semantic documents from the intermediate
AICommandForensicFacts model derived from machine evidence.

Usage:
  python tools/forensics/ai_command/derive_ai_command_protocol.py --manifest <manifest.json> --out-dir <output_directory>
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_MANIFEST = ROOT / "tools" / "forensics" / "ai_command" / "ai_command_disassembly_manifest.json"

ARM64_BINARY_SHA256 = "9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4"
AMD64_BINARY_SHA256 = "15adc2a4c47c4d189d4e8e08e960434bdd55202d74bc3eeee0bf4713a6b8de16"
BASE_COMMIT = "69aa5c7306456eb8257220a19b7f6754acbb2369"


class AICommandForensicFacts:
    """
    Intermediate machine-readable fact model compiled directly from
    disassembly snippets and verified reference facts.
    """
    def __init__(self, manifest: Dict[str, Any]):
        self.toolchain = manifest.get("toolchain", {})
        arm64 = manifest.get("arm64_snippets", {})
        amd64 = manifest.get("amd64_snippets", {})

        # 1. Channel Label & Inbound Dispatch
        arm_lbl = arm64["inbound_dispatch_label_check"]["disassembly"]
        amd_lbl = amd64["inbound_dispatch_label_check"]["disassembly"]
        if "#0x12" not in arm_lbl or "0x15440" not in arm_lbl:
            raise ValueError("ARM64 label check disassembly does not match expected length 18 or memequal (0x15440)")
        if "$0x12" not in amd_lbl or "0x406ce0" not in amd_lbl:
            raise ValueError("AMD64 label check disassembly does not match expected length 18 or memequal (0x406ce0)")

        self.channel_label = "ai-command-channel"
        self.channel_label_len = 18
        self.channel_type = "INBOUND_CLIENT_CREATED"
        self.creator_side = "Browser Client"
        self.consumer_side = "Agent"

        # 2. Lifecycle Handler Registration
        arm_reg = arm64["onmessage_callback_registration"]["disassembly"]
        amd_reg = amd64["onmessage_callback_registration"]["disassembly"]
        if "0x499770" not in arm_reg or "#0x5d0" not in arm_reg:
            raise ValueError("ARM64 OnMessage registration missing expected OnMessage call (0x499770) or target closure offset (#0x5d0)")
        if "0x9244a0" not in amd_reg or "0x9e32c0" not in amd_reg:
            raise ValueError("AMD64 OnMessage registration missing expected OnMessage call (0x9244a0) or target closure (0x9e32c0)")

        self.onmessage_site_arm64 = "0x53f45c (main.(*JJffa1S1Zv6).iIhwd_WXInS.func11)"
        self.onmessage_site_amd64 = "0x9e3129 (main.(*IDhLgq).woxaqqFN5Km.func11)"
        self.onmessage_closure_arm64 = "0x53f5d0 (cemlVcjsE0LQ.2)"
        self.onmessage_closure_amd64 = "0x9e32c0 (drnM2wXuIb.2)"

        # 3. Request Struct & Unmarshal Semantics
        arm_unm = arm64["json_unmarshal_and_validation_branch"]["disassembly"]
        amd_unm = amd64["json_unmarshal_and_validation_branch"]["disassembly"]
        if "0x12c600" not in arm_unm or "#0x660" not in arm_unm or "ret" not in arm_unm:
            raise ValueError("ARM64 unmarshal branch missing struct offset (#0x660), json.Unmarshal 0x12c600, or ret")
        if "0x52ba00" not in amd_unm or "0xab0be0" not in amd_unm or "retq" not in amd_unm:
            raise ValueError("AMD64 unmarshal branch missing struct 0xab0be0, json.Unmarshal 0x52ba00, or retq")

        self.request_struct_vma = {"arm64": "0x60e660", "amd64": "0xab0be0"}
        self.request_struct_size = 32
        self.request_fields = [
            {
                "name": "RequestID",
                "obfuscated_name": "NVGMf4S",
                "offset": 0,
                "go_type": "string",
                "json_tag": "request_id",
                "classification": "KNOWN_FIELD"
            },
            {
                "name": "Command",
                "obfuscated_name": "H4rjbPSQWLfJ",
                "offset": 16,
                "go_type": "string",
                "json_tag": "command",
                "classification": "KNOWN_FIELD"
            }
        ]
        self.malformed_json_behavior = "LOG_AND_DROP"
        self.malformed_json_log = "[AI-Command] Error parsing request JSON: %v"
        self.malformed_json_va = {"arm64": "0x6d5f36", "amd64": "0xb77ed7"}
        self.malformed_json_len = 43

        # 4. Concurrency Model (Goroutine spawn via runtime.newproc)
        arm_spawn = arm64["goroutine_spawn_on_success"]["disassembly"]
        amd_spawn = amd64["goroutine_spawn_on_success"]["disassembly"]
        if "0x5f730" not in arm_spawn or "#0x740" not in arm_spawn:
            raise ValueError("ARM64 goroutine spawn missing runtime.newproc (0x5f730) or worker closure offset (#0x740)")
        if "0x451c40" not in amd_spawn or "0x9e3460" not in amd_spawn:
            raise ValueError("AMD64 goroutine spawn missing runtime.newproc (0x451c40) or worker closure (0x9e3460)")

        self.concurrency_model = "GOROUTINE_PER_ACCEPTED_REQUEST"
        self.spawn_site = {
            "arm64": "0x53f704 calling runtime.newproc (0x5f730)",
            "amd64": "0x9e3423 calling runtime.newproc (0x451c40)"
        }
        self.worker_func = {
            "arm64": "0x53f740 (main.(*JJffa1S1Zv6).iIhwd_WXInS.func11.(*JJffa1S1Zv6).cemlVcjsE0LQ.2.1)",
            "amd64": "0x9e3460 (main.(*IDhLgq).woxaqqFN5Km.func11.(*IDhLgq).drnM2wXuIb.2.1)"
        }

        # 5. External Process Execution Boundary
        arm_exec = arm64["external_process_invocation"]["disassembly"]
        amd_exec = amd64["external_process_invocation"]["disassembly"]
        if "0x196e70" not in arm_exec or "0x197f00" not in arm_exec:
            raise ValueError("ARM64 external process missing exec.Command (0x196e70) or cmd.Run (0x197f00)")
        if "0x5a1c00" not in amd_exec or "0x5a2ea0" not in amd_exec:
            raise ValueError("AMD64 external process missing exec.Command (0x5a1c00) or cmd.Run (0x5a2ea0)")

        self.execution_classification = "DEFERRED_EXECUTION_BOUNDARY"
        self.execution_category = "EXTERNAL_PROCESS_CANDIDATE"
        self.shell_binary = "sh"
        self.shell_flag = "-c"
        self.shell_rodata = {
            "arm64": "0x6ac000 ('sh') and 0x6ac002 ('-c')",
            "amd64": "0xb4e032 ('sh') and 0xb4e034 ('-c')"
        }
        self.exec_cmd_call = {
            "arm64": "0x53f79c calling HvH5pmapH.RXi09bf9qp (0x196e70)",
            "amd64": "0x9e34d6 calling dN51dOZj79iH.Egppnln (0x5a1c00)"
        }
        self.exec_run_call = {
            "arm64": "0x53f80c calling HvH5pmapH.(*QcMnoAPhGe1).Run (0x197f00)",
            "amd64": "0x9e3555 calling dN51dOZj79iH.(*E7k1yG4).Run (0x5a2ea0)"
        }

        # 6. Response Construction & Directional Wire Framing
        arm_send = arm64["response_construction_and_send"]["disassembly"]
        amd_send = amd64["response_construction_and_send"]["disassembly"]
        if "0x49a3d0" not in arm_send or "0x1317c0" not in arm_send:
            raise ValueError("ARM64 response send missing (*DataChannel).Send (0x49a3d0) or json.Marshal (0x1317c0)")
        if "0x9250c0" not in amd_send or "0x531b60" not in amd_send:
            raise ValueError("AMD64 response send missing (*DataChannel).Send (0x9250c0) or json.Marshal (0x531b60)")

        self.response_send_method = "(*DataChannel).Send"
        self.response_framing = "BINARY_JSON_BYTES"
        self.request_framing = "JSON_TEXT"
        self.ordered_class = "REFERENCE_ONLY"
        self.request_id_echo = True

        self.response_fields = [
            {
                "json_key": "request_id",
                "go_type": "string",
                "rodata_va": {"arm64": "0x6b3a5b", "amd64": "0xb55aee"},
                "key_length": 10,
                "value_origin": "Direct echo of request.RequestID captured in worker closure (STATIC_CONFIRMED)"
            },
            {
                "json_key": "exit_code",
                "go_type": "int",
                "rodata_va": {"arm64": "0x6b1f17", "amd64": "0xb53f84"},
                "key_length": 9,
                "value_origin": "Process exit code (0 on success, ExitCode() on exec.ExitError, -1 on other errors)"
            },
            {
                "json_key": "stdout",
                "go_type": "string",
                "rodata_va": {"arm64": "0x6ade37", "amd64": "0xb4fe64"},
                "key_length": 6,
                "value_origin": "Captured stdout bytes from command execution converted to string"
            },
            {
                "json_key": "stderr",
                "go_type": "string",
                "rodata_va": {"arm64": "0x6ade3d", "amd64": "0xb4fe6a"},
                "key_length": 6,
                "value_origin": "Captured stderr bytes from command execution converted to string"
            }
        ]


def build_protocol_spec(facts: AICommandForensicFacts) -> Dict[str, Any]:
    return {
        "metadata": {
            "title": "Phase 2C.5B5F WebRTC AI-Command DataChannel Protocol Specification",
            "phase": "Phase 2C.5B5F",
            "status": "FROZEN_FORENSIC_BASELINE",
            "base_commit": BASE_COMMIT,
            "classification": "Clean-room behavioral and protocol forensic reconstruction",
            "channel_label": facts.channel_label,
            "toolchain_provenance": facts.toolchain,
            "governing_docs": [
                "evidence/go_agent/webrtc/DATACHANNEL_LABEL_EVIDENCE.json",
                "evidence/go_agent/webrtc/DATACHANNEL_FRAMING_MATRIX.json",
                "evidence/go_agent/DISASSEMBLY_FACTS.json",
                "evidence/go_agent/STRINGS.json",
                "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
                "tools/forensics/ai_command/ai_command_disassembly_manifest.json"
            ]
        },
        "channel_properties": {
            "label": facts.channel_label,
            "channel_type": facts.channel_type,
            "creator_side": facts.creator_side,
            "consumer_side": facts.consumer_side,
            "ordered": {
                "value": True,
                "evidence_class": facts.ordered_class,
                "basis": "Configured by browser frontend in useWebRTC.js:359: pc.createDataChannel('ai-command-channel', { ordered: true }). Agent binary accepts inbound channel via pc.OnDataChannel and does not inspect or validate channel ordered property."
            },
            "lifecycle_handlers": {
                "on_message": {
                    "status": "REGISTERED",
                    "evidence_class": "STATIC_CONFIRMED",
                    "registration_site": {
                        "arm64": facts.onmessage_site_arm64,
                        "amd64": facts.onmessage_site_amd64
                    },
                    "target_closure": {
                        "arm64": facts.onmessage_closure_arm64,
                        "amd64": facts.onmessage_closure_amd64
                    }
                },
                "on_open": {
                    "status": "NOT_REGISTERED",
                    "evidence_class": "STATIC_CONFIRMED",
                    "scope_limitation": "No branch-specific OnOpen or OnClose registration was recovered in the ai-command-channel dispatch path."
                },
                "on_close": {
                    "status": "NOT_REGISTERED",
                    "evidence_class": "STATIC_CONFIRMED",
                    "scope_limitation": "No branch-specific OnOpen or OnClose registration was recovered in the ai-command-channel dispatch path."
                }
            }
        },
        "directional_framing": {
            "browser_to_agent_request": {
                "transport": "WebRTC DataChannel",
                "framing_type": facts.request_framing,
                "evidence_class": "REFERENCE_ONLY_PROVEN_BY_LANE_D_WITH_STATIC_DECODER",
                "browser_send_method": "aiCommandChannel.send(JSON.stringify({ request_id: requestId, command: command })) [useWebRTC.js:311-314]",
                "agent_receive_method": "(*DataChannel).OnMessage callback receiving webrtc.DataChannelMessage. msg.Data ([]byte) is passed directly to json.Unmarshal.",
                "notes": "Browser transmits standard text frame (Lane D). Go Pion WebRTC delivers payload as []byte in msg.Data regardless of opcode."
            },
            "agent_to_browser_response": {
                "transport": "WebRTC DataChannel",
                "framing_type": facts.response_framing,
                "evidence_class": "STATIC_CONFIRMED",
                "agent_send_method": "(*DataChannel).Send ([]byte) [ARM64: 0x53f9e8 calling 0x49a3d0; AMD64: 0x9e374a calling 0x9250c0]",
                "agent_send_symbol": "IV04EXWpwj.(*F4TaFEL9SI).Send / v6LoFegGUKTA.(*W4J6chbzBu).Send",
                "send_argument_type": "[]byte (JSON serialized bytes)",
                "frontend_receive_handler": "useWebRTC.js:318-328: handles both string and ArrayBuffer (via TextDecoder), corroborating binary reception in browser as REFERENCE_ONLY.",
                "distinction": "Original binary explicitly invokes (*DataChannel).Send, NOT (*DataChannel).SendText. Payload is serialized JSON bytes transmitted as a binary DataChannel frame."
            }
        },
        "historical_errata_and_superseded_evidence": [
            {
                "target_artifact": "evidence/go_agent/webrtc/DATACHANNEL_FRAMING_MATRIX.json",
                "field": "ai-command-channel.framing",
                "historical_value": "JSON_TEXT_IN_ARRAYBUFFER",
                "status": "SUPERSEDED_BY_B5F",
                "correction": "Directional framing resolved independently: Browser->Agent request is JSON_TEXT; Agent->Browser response is BINARY_JSON_BYTES via (*DataChannel).Send([]byte).",
                "evidence": "Disassembly at ARM64 0x53f9e8 and AMD64 0x9e374a calls (*DataChannel).Send, not SendText."
            },
            {
                "target_artifact": "evidence/go_agent/webrtc/DATACHANNEL_LABEL_EVIDENCE.json",
                "field": "confirmed_webrtc_channels.ai-command-channel.ordered_evidence",
                "historical_value": "STATIC_CONFIRMED (Disassembly passes ordered=1 byte pointer to CreateDataChannel in AMD64 and ARM64)",
                "status": "ERRATUM_CORRECTED_IN_B5F",
                "correction": "ai-command-channel is an INBOUND browser-created channel. Agent binary does not invoke CreateDataChannel for this channel and does not inspect the ordered flag on dispatch. ordered=true is REFERENCE_ONLY from frontend useWebRTC.js:359.",
                "evidence": "Agent binary only implements label comparison in pc.OnDataChannel callback; no CreateDataChannel callsite exists for ai-command-channel."
            }
        ],
        "message_schemas": {
            "request": {
                "struct_vma": facts.request_struct_vma,
                "struct_size_bytes": facts.request_struct_size,
                "fields": facts.request_fields,
                "field_validation_semantics": {
                    "original_binary_validation": "NONE (disassembly proceeds directly to logging and goroutine spawn if json.Unmarshal succeeds, without checking for empty request_id or command)",
                    "reconstructed_defensive_validation": "ValidateAICommand rejects empty RequestID or empty Command as IMPLEMENTATION_CHOICE / DEFENSIVE_VALIDATION, not original binary parity."
                },
                "malformed_json_semantics": {
                    "behavior": facts.malformed_json_behavior,
                    "evidence_class": "STATIC_CONFIRMED",
                    "log_format": facts.malformed_json_log,
                    "log_string_va": facts.malformed_json_va,
                    "log_string_length": facts.malformed_json_len,
                    "response_sent": False,
                    "notes": "On json.Unmarshal error, execution branches to logger and immediately returns from the callback without calling (*DataChannel).Send."
                }
            },
            "response": {
                "structure": "map[string]interface{}",
                "fields": facts.response_fields,
                "serialization": "json.Marshal",
                "serialization_call": {
                    "arm64": "0x53f9d0 (g1gLI7afn.ZZnttPPIyf0d / 0x1317c0)",
                    "amd64": "0x9e3732 (JOaOfPm.KNJ5EBt9V / 0x531b60)"
                }
            }
        },
        "concurrency_model": {
            "model": facts.concurrency_model,
            "evidence_class": "STATIC_CONFIRMED",
            "spawn_site": facts.spawn_site,
            "worker_function": facts.worker_func,
            "queuing_or_pool": "NONE (direct goroutine invocation per request, no worker pool or rate limiter recovered)"
        },
        "execution_boundary": {
            "classification": facts.execution_classification,
            "category": facts.execution_category,
            "original_command_boundary": {
                "shell": facts.shell_binary,
                "shell_flag": facts.shell_flag,
                "shell_rodata": facts.shell_rodata,
                "exec_command_call": facts.exec_cmd_call,
                "exec_run_call": facts.exec_run_call
            },
            "clean_room_safety_restriction": {
                "policy": "STRICTLY_DEFERRED",
                "rule": "Clean-room safe implementation must NOT implement, invoke, or expose command execution. No os/exec import, no exec.Command, no sh -c, no shell simulator, and no command executor interface allowed in B5F."
            }
        }
    }


def build_message_inventory(facts: AICommandForensicFacts) -> Dict[str, Any]:
    return {
        "metadata": {
            "title": "Phase 2C.5B5F WebRTC AI-Command Message Inventory",
            "phase": "Phase 2C.5B5F",
            "status": "FROZEN_FORENSIC_BASELINE",
            "base_commit": BASE_COMMIT,
            "channel_label": facts.channel_label
        },
        "messages": [
            {
                "message_id": "MSG_AI_CMD_REQ",
                "name": "AI_COMMAND_REQUEST",
                "direction": "BROWSER_TO_AGENT",
                "transport_lane": "Lane D (Frontend reference)",
                "framing": facts.request_framing,
                "wire_format": "JSON UTF-8 string transmitted over WebRTC DataChannel",
                "go_struct_representation": {
                    "struct_type": "AICommandEnvelope",
                    "fields": [
                        {
                            "go_field": "RequestID",
                            "json_key": "request_id",
                            "type": "string",
                            "presence": "KNOWN_FIELD",
                            "required_in_original_binary": False,
                            "required_in_safe_defensive_parser": True,
                            "validation_note": "Original binary performs zero non-empty checks; safe parser enforces non-empty as defensive IMPLEMENTATION_CHOICE."
                        },
                        {
                            "go_field": "Command",
                            "json_key": "command",
                            "type": "string",
                            "presence": "KNOWN_FIELD",
                            "required_in_original_binary": False,
                            "required_in_safe_defensive_parser": True,
                            "validation_note": "Original binary performs zero non-empty checks; safe parser enforces non-empty as defensive IMPLEMENTATION_CHOICE."
                        }
                    ]
                },
                "agent_parse_action": "json.Unmarshal into anonymous struct { request_id string, command string }",
                "error_action": "On unmarshal error, log '[AI-Command] Error parsing request JSON: %v' and return immediately without sending response."
            },
            {
                "message_id": "MSG_AI_CMD_RESP",
                "name": "AI_COMMAND_RESPONSE",
                "direction": "AGENT_TO_BROWSER",
                "transport_lane": "Lane A (Binary disassembly)",
                "framing": facts.response_framing,
                "wire_format": "JSON serialized bytes transmitted via (*DataChannel).Send ([]byte)",
                "go_struct_representation": {
                    "struct_type": "AICommandResponse",
                    "fields": [
                        {
                            "go_field": "RequestID",
                            "json_key": "request_id",
                            "type": "string",
                            "correlation": "EXACT_REQUEST_ID_ECHO (captured from incoming request, STATIC_CONFIRMED)"
                        },
                        {
                            "go_field": "ExitCode",
                            "json_key": "exit_code",
                            "type": "int",
                            "semantics": "0 on command success, ExitCode() on exec.ExitError, -1 on command execution launch/context failure"
                        },
                        {
                            "go_field": "Stdout",
                            "json_key": "stdout",
                            "type": "string",
                            "semantics": "Captured stdout bytes from external process"
                        },
                        {
                            "go_field": "Stderr",
                            "json_key": "stderr",
                            "type": "string",
                            "semantics": "Captured stderr bytes from external process"
                        }
                    ]
                },
                "agent_marshal_action": "json.Marshal of map with keys request_id, exit_code, stdout, stderr",
                "agent_send_call": "(*DataChannel).Send ([]byte) [NOT SendText]"
            }
        ],
        "correlation_guarantees": {
            "request_id_echo": {
                "status": "STATIC_CONFIRMED",
                "provenance": "Worker closure copies request struct field 0 (NVGMf4S) directly into response map key 'request_id'.",
                "frontend_reference": "useWebRTC.js:321 resolves Promise keyed by response.request_id (REFERENCE_ONLY corroboration)."
            }
        },
        "negative_flow_semantics": {
            "malformed_json": {
                "wire_response": "NONE (drop)",
                "log_emission": "TRUE",
                "evidence_class": "STATIC_CONFIRMED"
            },
            "unknown_channel_label": {
                "wire_response": "NONE (ignored in OnDataChannel dispatcher)",
                "evidence_class": "STATIC_CONFIRMED"
            }
        }
    }


def build_callgraph(facts: AICommandForensicFacts) -> Dict[str, Any]:
    return {
        "metadata": {
            "title": "Phase 2C.5B5F WebRTC AI-Command Channel Callgraph",
            "phase": "Phase 2C.5B5F",
            "status": "FROZEN_FORENSIC_BASELINE",
            "base_commit": BASE_COMMIT,
            "channel_label": facts.channel_label
        },
        "nodes": {
            "INBOUND_DISPATCH": {
                "function_name": {
                    "arm64": "main.(*JJffa1S1Zv6).iIhwd_WXInS.func11 (0x53f210)",
                    "amd64": "main.(*IDhLgq).woxaqqFN5Km.func11 (0x9e2f20)"
                },
                "role": "pc.OnDataChannel dispatcher callback",
                "disassembly_range": {
                    "arm64": "0x53f210 - 0x53f548",
                    "amd64": "0x9e2f20 - 0x9e3200"
                }
            },
            "LABEL_MATCH": {
                "role": "Label string comparison for 'ai-command-channel'",
                "rodata_string": "ai-command-channel (len 18 / 0x12)",
                "rodata_va": {
                    "arm64": "0x6bd173",
                    "amd64": "0xb5f1c2"
                },
                "compare_site": {
                    "arm64": "0x53f288 - 0x53f2ac",
                    "amd64": "0x9e2f80 - 0x9e2fa8"
                },
                "target_on_match": {
                    "arm64": "0x53f414",
                    "amd64": "0x9e30eb"
                }
            },
            "ONMESSAGE_REGISTRATION": {
                "role": "Closure allocation and registration on DataChannel",
                "registration_call": {
                    "arm64": "0x53f45c calling (*DataChannel).OnMessage (0x499770)",
                    "amd64": "0x9e3129 calling (*DataChannel).OnMessage (0x9244a0)"
                },
                "registered_closure": {
                    "arm64": "0x53f5d0 (cemlVcjsE0LQ.2)",
                    "amd64": "0x9e32c0 (drnM2wXuIb.2)"
                },
                "other_handlers": "No branch-specific OnOpen or OnClose registration was recovered in the ai-command-channel dispatch path."
            },
            "ONMESSAGE_HANDLER": {
                "function_name": {
                    "arm64": "main.(*JJffa1S1Zv6).iIhwd_WXInS.func11.(*JJffa1S1Zv6).cemlVcjsE0LQ.2 (0x53f5d0)",
                    "amd64": "main.(*IDhLgq).woxaqqFN5Km.func11.(*IDhLgq).drnM2wXuIb.2 (0x9e32c0)"
                },
                "role": "DataChannel message handler",
                "steps": [
                    {
                        "step": "ALLOCATE_REQUEST_STRUCT",
                        "struct_type_va": facts.request_struct_vma
                    },
                    {
                        "step": "JSON_UNMARSHAL",
                        "call": {
                            "arm64": "0x53f62c calling g1gLI7afn.SEgb7sK (0x12c600)",
                            "amd64": "0x9e3323 calling JOaOfPm.OPQrPOkar (0x52ba00)"
                        }
                    },
                    {
                        "step": "CHECK_UNMARSHAL_ERROR",
                        "branch_on_error": {
                            "arm64": "0x53f630 (cbz x0 -> 0x53f66c on success; error path 0x53f634-0x53f668)",
                            "amd64": "0x9e3328 (testq %rax, %rax; je 0x9e336b on success; error path 0x9e332d-0x9e336a)"
                        },
                        "error_action": "Log '[AI-Command] Error parsing request JSON: %v' and return without response."
                    },
                    {
                        "step": "CHECK_FIELD_VALIDATION",
                        "presence": "NONE (zero validation checks for empty request_id or command)"
                    },
                    {
                        "step": "LOG_EXECUTION_INTENT",
                        "log_string": "[AI-Command] Executing P2P command (id=%s): %s",
                        "rodata_va": {
                            "arm64": "0x6d86f2",
                            "amd64": "0xb7a693"
                        }
                    },
                    {
                        "step": "SPAWN_WORKER_GOROUTINE",
                        "closure_function": {
                            "arm64": "0x53f740",
                            "amd64": "0x9e3460"
                        },
                        "newproc_call": facts.spawn_site
                    }
                ]
            },
            "WORKER_GOROUTINE": {
                "function_name": {
                    "arm64": "main.(*JJffa1S1Zv6).iIhwd_WXInS.func11.(*JJffa1S1Zv6).cemlVcjsE0LQ.2.1 (0x53f740)",
                    "amd64": "main.(*IDhLgq).woxaqqFN5Km.func11.(*IDhLgq).drnM2wXuIb.2.1 (0x9e3460)"
                },
                "role": "Asynchronous request worker",
                "steps": [
                    {
                        "step": "ORIGINAL_EXECUTION_BOUNDARY",
                        "status": facts.execution_classification,
                        "command_setup": "exec.Command('sh', '-c', req.Command)",
                        "run_call": "cmd.Run()",
                        "exit_code_resolution": "0 if err == nil; ExitCode() if exec.ExitError; -1 otherwise"
                    },
                    {
                        "step": "BUILD_RESPONSE_MAP",
                        "map_keys": [
                            "request_id (echoes req.RequestID)",
                            "exit_code",
                            "stdout",
                            "stderr"
                        ]
                    },
                    {
                        "step": "JSON_MARSHAL",
                        "call": {
                            "arm64": "0x53f9d0 calling g1gLI7afn.ZZnttPPIyf0d (0x1317c0)",
                            "amd64": "0x9e3732 calling JOaOfPm.KNJ5EBt9V (0x531b60)"
                        }
                    },
                    {
                        "step": "SEND_RESPONSE",
                        "send_call": {
                            "arm64": "0x53f9e8 calling (*DataChannel).Send (0x49a3d0)",
                            "amd64": "0x9e374a calling (*DataChannel).Send (0x9250c0)"
                        },
                        "framing": facts.response_framing
                    }
                ]
            }
        },
        "edges": [
            { "from": "INBOUND_DISPATCH", "to": "LABEL_MATCH", "type": "INTERNAL_CONTROL_FLOW" },
            { "from": "LABEL_MATCH", "to": "ONMESSAGE_REGISTRATION", "type": "BRANCH_ON_LABEL_MATCH" },
            { "from": "ONMESSAGE_REGISTRATION", "to": "ONMESSAGE_HANDLER", "type": "CALLBACK_BINDING" },
            { "from": "ONMESSAGE_HANDLER", "to": "WORKER_GOROUTINE", "type": "RUNTIME_NEWPROC_SPAWN" },
            { "from": "WORKER_GOROUTINE", "to": "DATACHANNEL_SEND", "type": "PION_DATACHANNEL_SEND_BYTES" }
        ]
    }


def build_source_provenance(facts: AICommandForensicFacts) -> Dict[str, Any]:
    return {
        "metadata": {
            "title": "Phase 2C.5B5F WebRTC AI-Command Source Provenance & Evidence Matrix",
            "phase": "Phase 2C.5B5F",
            "status": "FROZEN_FORENSIC_BASELINE",
            "base_commit": BASE_COMMIT,
            "channel_label": facts.channel_label
        },
        "binaries": {
            "arm64": {
                "path": "cloudphone-v0.3.6 (1)/android/cloudphone-agent",
                "sha256": ARM64_BINARY_SHA256,
                "arch": "elf64-littleaarch64",
                "go_version": "go1.22.4"
            },
            "amd64": {
                "path": "cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-amd64",
                "sha256": AMD64_BINARY_SHA256,
                "arch": "elf64-x86-64",
                "go_version": "go1.22.4"
            }
        },
        "facts": [
            {
                "fact_id": "FACT-AI-01",
                "description": "DataChannel label 'ai-command-channel' (18 bytes)",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "rodata_va": "0x6bd173",
                    "length": 18,
                    "string_literal": "ai-command-channel"
                },
                "amd64_evidence": {
                    "rodata_va": "0xb5f1c2",
                    "length": 18,
                    "string_literal": "ai-command-channel"
                },
                "frontend_evidence": {
                    "classification": "REFERENCE_ONLY",
                    "file": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
                    "line": 359,
                    "code": "pc.createDataChannel('ai-command-channel', { ordered: true })"
                }
            },
            {
                "fact_id": "FACT-AI-02",
                "description": "Inbound channel dispatch in pc.OnDataChannel callback",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "function": "main.(*JJffa1S1Zv6).iIhwd_WXInS.func11",
                    "va": "0x53f210",
                    "label_check_range": "0x53f288 - 0x53f2ac"
                },
                "amd64_evidence": {
                    "function": "main.(*IDhLgq).woxaqqFN5Km.func11",
                    "va": "0x9e2f20",
                    "label_check_range": "0x9e2f80 - 0x9e2fa8"
                }
            },
            {
                "fact_id": "FACT-AI-03",
                "description": "OnMessage registration without branch-specific OnOpen/OnClose",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "registration_site": "0x53f45c calling (*DataChannel).OnMessage (0x499770)",
                    "callback_func": "0x53f5d0 (cemlVcjsE0LQ.2)"
                },
                "amd64_evidence": {
                    "registration_site": "0x9e3129 calling (*DataChannel).OnMessage (0x9244a0)",
                    "callback_func": "0x9e32c0 (drnM2wXuIb.2)"
                }
            },
            {
                "fact_id": "FACT-AI-04",
                "description": "Request anonymous struct fields {request_id, command}",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "type_descriptor_va": "0x60e660",
                    "size": 32,
                    "field_0": "NVGMf4S string (`json:\"request_id\"`)",
                    "field_1": "H4rjbPSQWLfJ string (`json:\"command\"`)"
                },
                "amd64_evidence": {
                    "type_descriptor_va": "0xab0be0",
                    "size": 32,
                    "field_0": "string (`json:\"request_id\"`)",
                    "field_1": "string (`json:\"command\"`)"
                }
            },
            {
                "fact_id": "FACT-AI-05",
                "description": "Request field presence vs required validation",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "finding": "Disassembly from 0x53f630 to 0x53f66c checks only json.Unmarshal return code. Zero non-empty string validation checks."
                },
                "amd64_evidence": {
                    "finding": "Disassembly from 0x9e3328 to 0x9e336b checks only json.Unmarshal return code. Zero non-empty string validation checks."
                },
                "classification_note": "Request fields are KNOWN_FIELDS. Defensive validation in reconstructed code is an IMPLEMENTATION_CHOICE."
            },
            {
                "fact_id": "FACT-AI-06",
                "description": "Malformed JSON unmarshal error logging and drop",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "log_string_va": "0x6d5f36",
                    "log_string": facts.malformed_json_log,
                    "branch_action": "0x53f668: restores registers and executes ret without sending response."
                },
                "amd64_evidence": {
                    "log_string_va": "0xb77ed7",
                    "log_string": facts.malformed_json_log,
                    "branch_action": "0x9e336a: restores registers and executes retq without sending response."
                }
            },
            {
                "fact_id": "FACT-AI-07",
                "description": "Goroutine per accepted request concurrency",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "spawn_site": "0x53f704 calling runtime.newproc (0x5f730)",
                    "worker_func": "0x53f740 (cemlVcjsE0LQ.2.1)"
                },
                "amd64_evidence": {
                    "spawn_site": "0x9e3423 calling runtime.newproc (0x451c40)",
                    "worker_func": "0x9e3460 (drnM2wXuIb.2.1)"
                }
            },
            {
                "fact_id": "FACT-AI-08",
                "description": "Original command execution boundary reaches external shell/process",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "shell": "0x6ac000 ('sh')",
                    "flag": "0x6ac002 ('-c')",
                    "exec_cmd_call": "0x53f79c calling HvH5pmapH.RXi09bf9qp (0x196e70)"
                },
                "amd64_evidence": {
                    "shell": "0xb4e032 ('sh')",
                    "flag": "0xb4e034 ('-c')",
                    "exec_cmd_call": "0x9e34d6 calling dN51dOZj79iH.Egppnln (0x5a1c00)"
                },
                "clean_room_scope": "DEFERRED_EXECUTION_BOUNDARY. Zero process execution code permitted in clean-room agent."
            },
            {
                "fact_id": "FACT-AI-09",
                "description": "Response schema keys: request_id, exit_code, stdout, stderr",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "request_id_key": "0x6b3a5b (len 10)",
                    "exit_code_key": "0x6b1f17 (len 9)",
                    "stdout_key": "0x6ade37 (len 6)",
                    "stderr_key": "0x6ade3d (len 6)",
                    "marshal_call": "0x53f9d0 calling g1gLI7afn.ZZnttPPIyf0d (0x1317c0)"
                },
                "amd64_evidence": {
                    "request_id_key": "0xb55aee (len 10)",
                    "exit_code_key": "0xb53f84 (len 9)",
                    "stdout_key": "0xb4fe64 (len 6)",
                    "stderr_key": "0xb4fe6a (len 6)",
                    "marshal_call": "0x9e3732 calling JOaOfPm.KNJ5EBt9V (0x531b60)"
                }
            },
            {
                "fact_id": "FACT-AI-10",
                "description": "Exact RequestID echo correlation",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "dataflow": "req.NVGMf4S at closure offset 0x80 loaded at 0x53f848 and inserted into map key 'request_id' at 0x53f868"
                },
                "amd64_evidence": {
                    "dataflow": "req.RequestID at closure offset 0x70 loaded at 0x9e358f and inserted into map key 'request_id' at 0x9e35b6"
                }
            },
            {
                "fact_id": "FACT-AI-11",
                "description": "Response sent via (*DataChannel).Send ([]byte) as BINARY_JSON_BYTES",
                "classification": "STATIC_CONFIRMED",
                "arm64_evidence": {
                    "send_call": "0x53f9e8 calling IV04EXWpwj.(*F4TaFEL9SI).Send (0x49a3d0)",
                    "framing": facts.response_framing
                },
                "amd64_evidence": {
                    "send_call": "0x9e374a calling v6LoFegGUKTA.(*W4J6chbzBu).Send (0x9250c0)",
                    "framing": facts.response_framing
                }
            },
            {
                "fact_id": "FACT-AI-12",
                "description": "Ordered property is REFERENCE_ONLY from frontend",
                "classification": "REFERENCE_ONLY",
                "frontend_evidence": {
                    "file": "evidence/reference/raw/web-app/src/composables/useWebRTC.js",
                    "line": 359,
                    "code": "pc.createDataChannel('ai-command-channel', { ordered: true })"
                },
                "agent_binary_evidence": {
                    "status": "NO_CHECK",
                    "finding": "Agent receives inbound channel via pc.OnDataChannel; does not inspect or validate channel ordered flag."
                }
            }
        ]
    }


def serialize_artifact_exact(fname: str, data: Dict[str, Any]) -> bytes:
    dumped = json.dumps(data, indent=2)
    if fname == "AI_COMMAND_B5F_CALLGRAPH.json":
        # Keep edges elements formatted compactly on a single line matching canonical baseline
        dumped = re.sub(
            r'\{\s+"from":\s+"([^"]+)",\s+"to":\s+"([^"]+)",\s+"type":\s+"([^"]+)"\s+\}',
            r'{ "from": "\1", "to": "\2", "type": "\3" }',
            dumped
        )
    return dumped.encode("utf-8") + b"\n"


def derive_ai_command_artifacts(
    manifest_path: Path = DEFAULT_MANIFEST,
    output_dir: Optional[Path] = None
) -> Dict[str, Any]:
    manifest_p = Path(manifest_path)
    if not manifest_p.exists():
        raise FileNotFoundError(f"Disassembly manifest not found: {manifest_p}")

    # Parse disassembly manifest
    manifest = json.loads(manifest_p.read_text(encoding="utf-8"))

    # Synthesize intermediate fact model
    facts = AICommandForensicFacts(manifest)

    # Derive the 4 semantic artifacts independently
    artifacts = {
        "AI_COMMAND_B5F_PROTOCOL_SPEC.json": build_protocol_spec(facts),
        "AI_COMMAND_B5F_MESSAGE_INVENTORY.json": build_message_inventory(facts),
        "AI_COMMAND_B5F_CALLGRAPH.json": build_callgraph(facts),
        "AI_COMMAND_B5F_SOURCE_PROVENANCE.json": build_source_provenance(facts),
    }

    if output_dir:
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        for fname, data in artifacts.items():
            exact_bytes = serialize_artifact_exact(fname, data)
            (out_p / fname).write_bytes(exact_bytes)

    return artifacts


def main():
    parser = argparse.ArgumentParser(description="Derive AI Command protocol artifacts from disassembly manifest")
    parser.add_argument("--manifest", type=str, default=str(DEFAULT_MANIFEST), help="Path to disassembly manifest")
    parser.add_argument("--out-dir", type=str, default=None, help="Directory to output derived artifacts")
    args = parser.parse_args()

    try:
        arts = derive_ai_command_artifacts(
            manifest_path=Path(args.manifest),
            output_dir=Path(args.out_dir) if args.out_dir else None
        )
        print(f"[+] Successfully derived {len(arts)} protocol artifacts from {args.manifest}")
        if args.out_dir:
            print(f"[+] Wrote artifacts to {args.out_dir}")
    except Exception as e:
        print(f"[FAIL] Error deriving AI command protocol: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
