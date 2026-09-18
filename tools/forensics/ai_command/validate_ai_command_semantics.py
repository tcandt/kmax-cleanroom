#!/usr/bin/env python3
"""
tools/forensics/ai_command/validate_ai_command_semantics.py
Phase 2C.5B5FR Shared Semantic Validator for AI-Command Forensic Artifacts.

Validates actual artifact documents (JSON dictionaries or files) against authoritative
protocol, contract, and clean-room safety invariants.

Reused by:
- reproduce_ai_command_forensics.py (--check pipeline)
- test_ai_command_forensics_negative.py (mutation testing on tempfile copies)
- verify_phase2.py (Section 25 master verifier)
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union


def validate_ai_command_semantics(
    spec: Union[Dict[str, Any], str, Path],
    contract: Union[Dict[str, Any], str, Path],
    inventory: Optional[Union[Dict[str, Any], str, Path]] = None,
    callgraph: Optional[Union[Dict[str, Any], str, Path]] = None,
    provenance: Optional[Union[Dict[str, Any], str, Path]] = None
) -> Dict[str, Any]:
    """
    Validates forensic artifacts against required invariants.
    Raises ValueError or AssertionError if any invariant is violated.
    """
    # Load JSON if file paths are given
    def _load(obj):
        if isinstance(obj, (str, Path)):
            p = Path(obj)
            return json.loads(p.read_text(encoding="utf-8"))
        return obj

    spec_data = _load(spec)
    contract_data = _load(contract)
    inv_data = _load(inventory) if inventory is not None else None
    cg_data = _load(callgraph) if callgraph is not None else None
    prov_data = _load(provenance) if provenance is not None else None

    # 1. Channel Label Invariant
    lbl_spec = spec_data.get("channel_properties", {}).get("label")
    lbl_contract = contract_data.get("metadata", {}).get("channel_label")
    if lbl_spec != "ai-command-channel":
        raise ValueError(f"Channel label in protocol spec must be 'ai-command-channel', got '{lbl_spec}'")
    if lbl_contract != "ai-command-channel":
        raise ValueError(f"Channel label in contract must be 'ai-command-channel', got '{lbl_contract}'")

    # 2. Ownership / Directionality Invariant
    ch_props = spec_data.get("channel_properties", {})
    if ch_props.get("channel_type") != "INBOUND_CLIENT_CREATED":
        raise ValueError(f"Channel type must be 'INBOUND_CLIENT_CREATED', got '{ch_props.get('channel_type')}'")
    if ch_props.get("creator_side") != "Browser Client":
        raise ValueError(f"Creator side must be 'Browser Client', got '{ch_props.get('creator_side')}'")
    if ch_props.get("consumer_side") != "Agent":
        raise ValueError(f"Consumer side must be 'Agent', got '{ch_props.get('consumer_side')}'")

    # 3. Request Directional Framing
    df = spec_data.get("directional_framing", {})
    req_framing = df.get("browser_to_agent_request", {}).get("framing_type")
    if req_framing != "JSON_TEXT":
        raise ValueError(f"Browser to Agent request framing must be 'JSON_TEXT', got '{req_framing}'")

    # 4. Response Directional Framing
    resp_framing = df.get("agent_to_browser_response", {}).get("framing_type")
    if resp_framing != "BINARY_JSON_BYTES":
        raise ValueError(f"Agent to Browser response framing must be 'BINARY_JSON_BYTES', got '{resp_framing}'")
    send_method = df.get("agent_to_browser_response", {}).get("agent_send_method", "")
    if "SendText" in send_method:
        raise ValueError("Agent response send method must NOT use SendText; it must use (*DataChannel).Send ([]byte)")
    if "(*DataChannel).Send" not in send_method:
        raise ValueError("Agent response send method must explicitly reference (*DataChannel).Send")

    # 5. Ordered Property Classification
    ord_class = ch_props.get("ordered", {}).get("evidence_class")
    if ord_class != "REFERENCE_ONLY":
        raise ValueError(
            f"Inbound ordered property must be classified as 'REFERENCE_ONLY' from browser creation, got '{ord_class}'"
        )

    # 6. Request Schema & Field Classification (Known Fields, Not Required Non-Empty)
    req_schema = spec_data.get("message_schemas", {}).get("request", {})
    req_fields = req_schema.get("fields", [])
    if len(req_fields) != 2:
        raise ValueError(f"Request schema must define exactly 2 fields, got {len(req_fields)}")
    f_names = {f.get("json_tag"): f for f in req_fields}
    if "request_id" not in f_names or "command" not in f_names:
        raise ValueError("Request schema missing 'request_id' or 'command' JSON tags")
    for tag, f in f_names.items():
        if f.get("classification") != "KNOWN_FIELD":
            raise ValueError(
                f"Request field '{tag}' classification must be 'KNOWN_FIELD', got '{f.get('classification')}'"
            )

    orig_val = req_schema.get("field_validation_semantics", {}).get("original_binary_validation", "")
    if not orig_val.startswith("NONE"):
        raise ValueError(f"Original binary validation must be 'NONE', got '{orig_val}'")

    # 7. Malformed JSON Semantics
    malformed = req_schema.get("malformed_json_semantics", {})
    if malformed.get("behavior") != "LOG_AND_DROP":
        raise ValueError(f"Malformed JSON behavior must be 'LOG_AND_DROP', got '{malformed.get('behavior')}'")
    if malformed.get("response_sent") is not False:
        raise ValueError("Malformed JSON response_sent must be False")

    # 8. Response Schema & Request ID Correlation
    resp_schema = spec_data.get("message_schemas", {}).get("response", {})
    resp_fields = {f.get("json_key"): f for f in resp_schema.get("fields", [])}
    for required_key in ("request_id", "exit_code", "stdout", "stderr"):
        if required_key not in resp_fields:
            raise ValueError(f"Response schema missing required key '{required_key}'")

    req_id_origin = resp_fields["request_id"].get("value_origin", "")
    if "echo" not in req_id_origin.lower() or "request.requestid" not in req_id_origin.lower():
        raise ValueError(f"Response request_id origin must confirm direct echo, got '{req_id_origin}'")

    # 9. Concurrency Model
    conc = spec_data.get("concurrency_model", {})
    if conc.get("model") != "GOROUTINE_PER_ACCEPTED_REQUEST":
        raise ValueError(f"Concurrency model must be 'GOROUTINE_PER_ACCEPTED_REQUEST', got '{conc.get('model')}'")
    if conc.get("evidence_class") != "STATIC_CONFIRMED":
        raise ValueError(f"Concurrency evidence class must be 'STATIC_CONFIRMED', got '{conc.get('evidence_class')}'")

    # 10. Execution Boundary Classification
    exec_b = spec_data.get("execution_boundary", {})
    if exec_b.get("classification") != "DEFERRED_EXECUTION_BOUNDARY":
        raise ValueError(
            f"Execution boundary classification must be 'DEFERRED_EXECUTION_BOUNDARY', got '{exec_b.get('classification')}'"
        )
    if exec_b.get("category") != "EXTERNAL_PROCESS_CANDIDATE":
        raise ValueError(
            f"Execution boundary category must be 'EXTERNAL_PROCESS_CANDIDATE', got '{exec_b.get('category')}'"
        )
    clean_room_rule = exec_b.get("clean_room_safety_restriction", {}).get("rule", "")
    if "NOT implement" not in clean_room_rule or "os/exec" not in clean_room_rule:
        raise ValueError("Clean-room safety restriction rule must strictly forbid os/exec and command execution")

    # 11. Contract Requirements Validation
    c_reqs = {r["id"]: r for r in contract_data.get("requirements", [])}
    required_cids = ["AI-B5F-01", "AI-B5F-04", "AI-B5F-06", "AI-B5F-09", "AI-B5F-10", "AI-B5F-12", "AI-B5F-13", "AI-B5F-14", "AI-B5F-15"]
    for cid in required_cids:
        if cid not in c_reqs:
            raise ValueError(f"Contract missing requirement '{cid}'")

    # Validate specific contract requirements
    r10 = c_reqs["AI-B5F-10"]
    if r10.get("evidence_class") != "MANDATORY_SAFETY_GUARD":
        raise ValueError(f"AI-B5F-10 evidence class must be 'MANDATORY_SAFETY_GUARD', got '{r10.get('evidence_class')}'")

    r12 = c_reqs["AI-B5F-12"]
    if r12.get("evidence_class") != "STATIC_CONFIRMED":
        raise ValueError(f"AI-B5F-12 request ID echo evidence class must be 'STATIC_CONFIRMED', got '{r12.get('evidence_class')}'")

    r15 = c_reqs["AI-B5F-15"]
    if "strictly inert" not in r15.get("observable_behavior", ""):
        raise ValueError("AI-B5F-15 observable behavior must require channel to remain strictly inert")

    # 12. Optional Inventory and Callgraph validation
    if inv_data is not None:
        inv_messages = {m.get("message_id"): m for m in inv_data.get("messages", [])}
        if "MSG_AI_CMD_REQ" not in inv_messages or "MSG_AI_CMD_RESP" not in inv_messages:
            raise ValueError("Message inventory missing MSG_AI_CMD_REQ or MSG_AI_CMD_RESP")

    if cg_data is not None:
        nodes = cg_data.get("nodes", {})
        required_nodes = {"INBOUND_DISPATCH", "LABEL_MATCH", "ONMESSAGE_REGISTRATION", "ONMESSAGE_HANDLER", "WORKER_GOROUTINE"}
        if not required_nodes.issubset(set(nodes.keys())):
            raise ValueError(f"Callgraph missing required nodes: {required_nodes - set(nodes.keys())}")

    # 13. Source Provenance Artifact Validation (Item 11 & 12)
    prov_checked = 0
    if prov_data is not None:
        binaries = prov_data.get("binaries", {})
        if "arm64" not in binaries or "amd64" not in binaries:
            raise ValueError("Source provenance missing arm64 or amd64 binary metadata")
        for arch in ("arm64", "amd64"):
            b_info = binaries[arch]
            if not b_info.get("sha256") or not b_info.get("path"):
                raise ValueError(f"Source provenance binary '{arch}' missing sha256 or path")

        facts = prov_data.get("facts", [])
        if len(facts) < 12:
            raise ValueError(f"Source provenance must define at least 12 facts, got {len(facts)}")

        facts_by_id = {f.get("fact_id"): f for f in facts}

        # Check all STATIC_CONFIRMED facts have both ARM64 and AMD64 evidence
        for f in facts:
            if f.get("classification") == "STATIC_CONFIRMED":
                fid = f.get("fact_id")
                arm_ev = f.get("arm64_evidence")
                amd_ev = f.get("amd64_evidence")
                if not isinstance(arm_ev, dict) or not isinstance(amd_ev, dict):
                    raise ValueError(f"Fact '{fid}' ({f.get('description')}) classified STATIC_CONFIRMED must include both arm64_evidence and amd64_evidence dicts")

        # Specific Invariant Checks:
        # A. Response Send callsites exist
        f_send = facts_by_id.get("FACT-AI-11")
        if not f_send or "0x49a3d0" not in f_send.get("arm64_evidence", {}).get("send_call", "") or "0x9250c0" not in f_send.get("amd64_evidence", {}).get("send_call", ""):
            raise ValueError("Source provenance FACT-AI-11 missing (*DataChannel).Send callsites (ARM64: 0x49a3d0, AMD64: 0x9250c0)")
        if f_send.get("arm64_evidence", {}).get("framing") != "BINARY_JSON_BYTES":
            raise ValueError("Source provenance FACT-AI-11 framing must be BINARY_JSON_BYTES")

        # B. json.Marshal callsites exist
        f_marshal = facts_by_id.get("FACT-AI-09")
        if not f_marshal or "0x1317c0" not in f_marshal.get("arm64_evidence", {}).get("marshal_call", "") or "0x531b60" not in f_marshal.get("amd64_evidence", {}).get("marshal_call", ""):
            raise ValueError("Source provenance FACT-AI-09 missing json.Marshal callsites (ARM64: 0x1317c0, AMD64: 0x531b60)")

        # C. runtime.newproc callsites exist
        f_newproc = facts_by_id.get("FACT-AI-07")
        if not f_newproc or "0x5f730" not in f_newproc.get("arm64_evidence", {}).get("spawn_site", "") or "0x451c40" not in f_newproc.get("amd64_evidence", {}).get("spawn_site", ""):
            raise ValueError("Source provenance FACT-AI-07 missing runtime.newproc callsites (ARM64: 0x5f730, AMD64: 0x451c40)")

        # D. Request schema source/type evidence exists
        f_req = facts_by_id.get("FACT-AI-04")
        if not f_req or f_req.get("arm64_evidence", {}).get("type_descriptor_va") != "0x60e660" or f_req.get("amd64_evidence", {}).get("type_descriptor_va") != "0xab0be0":
            raise ValueError("Source provenance FACT-AI-04 missing request type descriptor VAs (ARM64: 0x60e660, AMD64: 0xab0be0)")

        # E. Request-ID echo provenance exists
        f_echo = facts_by_id.get("FACT-AI-10")
        if not f_echo or "request_id" not in f_echo.get("arm64_evidence", {}).get("dataflow", "") or "request_id" not in f_echo.get("amd64_evidence", {}).get("dataflow", ""):
            raise ValueError("Source provenance FACT-AI-10 missing request-id dataflow echo confirmation")

        # F. External process boundary provenance exists
        f_exec = facts_by_id.get("FACT-AI-08")
        if not f_exec or f_exec.get("clean_room_scope") != "DEFERRED_EXECUTION_BOUNDARY. Zero process execution code permitted in clean-room agent.":
            raise ValueError("Source provenance FACT-AI-08 missing clean_room_scope DEFERRED_EXECUTION_BOUNDARY invariant")
        if "0x196e70" not in f_exec.get("arm64_evidence", {}).get("exec_cmd_call", "") or "0x5a1c00" not in f_exec.get("amd64_evidence", {}).get("exec_cmd_call", ""):
            raise ValueError("Source provenance FACT-AI-08 missing exec.Command callsite evidence")

        prov_checked = len(facts)

    return {
        "status": "VALID",
        "channel_label": lbl_spec,
        "request_framing": req_framing,
        "response_framing": resp_framing,
        "ordered_class": ord_class,
        "fields_validated": len(req_fields) + len(resp_fields),
        "concurrency_model": conc.get("model"),
        "execution_boundary": exec_b.get("classification"),
        "contract_requirements_checked": len(required_cids),
        "provenance_facts_checked": prov_checked
    }


if __name__ == "__main__":
    import sys
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
    EVID = ROOT_DIR / "evidence" / "go_agent" / "webrtc"
    try:
        res = validate_ai_command_semantics(
            spec=EVID / "AI_COMMAND_B5F_PROTOCOL_SPEC.json",
            contract=EVID / "AI_COMMAND_B5F_IMPLEMENTATION_CONTRACT.json",
            inventory=EVID / "AI_COMMAND_B5F_MESSAGE_INVENTORY.json",
            callgraph=EVID / "AI_COMMAND_B5F_CALLGRAPH.json",
            provenance=EVID / "AI_COMMAND_B5F_SOURCE_PROVENANCE.json"
        )
        print(f"[+] validate_ai_command_semantics: PASS ({res})")
    except Exception as e:
        print(f"[FAIL] validate_ai_command_semantics: {e}", file=sys.stderr)
        sys.exit(1)
