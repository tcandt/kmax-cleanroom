#!/usr/bin/env python3
"""
tools/forensics/adb_channel/validate_adb_channel_semantics.py

Validates semantic consistency, forensic invariants, and safety boundaries
across Phase 2C.5B6F adb-channel artifacts.
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any, Union

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
EVID_DIR = REPO_ROOT / "evidence" / "go_agent" / "webrtc"


def _load(obj_or_path: Union[str, Path, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(obj_or_path, (str, Path)):
        return json.loads(Path(obj_or_path).read_text(encoding="utf-8"))
    return obj_or_path


def validate_adb_channel_semantics(
    spec: Union[str, Path, Dict[str, Any]] = None,
    topology: Union[str, Path, Dict[str, Any]] = None,
    framing: Union[str, Path, Dict[str, Any]] = None,
    callgraph: Union[str, Path, Dict[str, Any]] = None,
    provenance: Union[str, Path, Dict[str, Any]] = None,
    contract: Union[str, Path, Dict[str, Any]] = None,
    errata: Union[str, Path, Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Executes comprehensive semantic validation across all Phase 2C.5B6F artifacts.
    Raises ValueError on any invariant violation (fail-closed).
    """
    spec_d = _load(spec or (EVID_DIR / "ADB_CHANNEL_B6F_PROTOCOL_SPEC.json"))
    top_d = _load(topology or (EVID_DIR / "ADB_CHANNEL_B6F_TOPOLOGY.json"))
    frame_d = _load(framing or (EVID_DIR / "ADB_CHANNEL_B6F_MESSAGE_FRAMING.json"))
    cg_d = _load(callgraph or (EVID_DIR / "ADB_CHANNEL_B6F_CALLGRAPH.json"))
    prov_d = _load(provenance or (EVID_DIR / "ADB_CHANNEL_B6F_SOURCE_PROVENANCE.json"))
    contract_d = _load(contract or (EVID_DIR / "ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json"))
    err_d = _load(errata or (EVID_DIR / "ADB_CHANNEL_B6F_CONTRACT_ERRATA.json")) if (errata or (EVID_DIR / "ADB_CHANNEL_B6F_CONTRACT_ERRATA.json").exists()) else None

    # 1. Channel Label Invariant
    channel_label = spec_d.get("channel_identity", {}).get("label")
    if channel_label != "adb-channel":
        raise ValueError(f"Channel label must be 'adb-channel', got '{channel_label}'")
    if top_d.get("channel_label") != "adb-channel":
        raise ValueError(f"Topology channel label must be 'adb-channel', got '{top_d.get('channel_label')}'")
    if frame_d.get("channel_label") != "adb-channel":
        raise ValueError(f"Framing channel label must be 'adb-channel', got '{frame_d.get('channel_label')}'")

    # 2. Channel Ownership Invariant
    creator = spec_d.get("channel_identity", {}).get("creator_side")
    consumer = spec_d.get("channel_identity", {}).get("consumer_side")
    if creator != "Browser Client":
        raise ValueError(f"Creator side must be 'Browser Client', got '{creator}'")
    if consumer != "Agent":
        raise ValueError(f"Consumer side must be 'Agent', got '{consumer}'")

    # 3. Inbound Ordered Property Classification Invariant
    ordered_info = spec_d.get("channel_identity", {}).get("ordered_property", {})
    if ordered_info.get("classification") != "REFERENCE_ONLY":
        raise ValueError(f"Inbound ordered property must be 'REFERENCE_ONLY', got '{ordered_info.get('classification')}'")

    # 4. Directional Framing Invariant
    dir_framing = spec_d.get("directional_framing", {})
    req_modes = dir_framing.get("browser_to_agent_request", {}).get("supported_modes", [])
    resp_api = dir_framing.get("agent_to_browser_response", {}).get("api", "")
    if not any("ADB_PACKET_MODE" in m for m in req_modes) or not any("BARE_RAW_PTY_MODE" in m for m in req_modes):
        raise ValueError(f"Request framing must support both ADB_PACKET_MODE and BARE_RAW_PTY_MODE: {req_modes}")
    if "SendText" in resp_api:
        raise ValueError("Agent response API must NOT use SendText; it must use (*DataChannel).Send (binary)")
    if "(*DataChannel).Send" not in resp_api:
        raise ValueError(f"Agent response API must use (*DataChannel).Send, got '{resp_api}'")

    # 5. Session-Sticky Mode Lifecycle Invariant
    lifecycle = spec_d.get("session_mode_lifecycle", {})
    if not lifecycle.get("is_session_sticky"):
        raise ValueError("Session mode lifecycle must be marked 'is_session_sticky: true'")
    if lifecycle.get("header_length_threshold") != 24:
        raise ValueError(f"Header length threshold must be 24, got {lifecycle.get('header_length_threshold')}")
    if lifecycle.get("cnxn_command_magic") != "0x4e584e43":
        raise ValueError(f"CNXN command magic must be '0x4e584e43', got '{lifecycle.get('cnxn_command_magic')}'")

    # 6. ADB Packet Header Layout Invariant
    packet_proto = spec_d.get("adb_packet_protocol", {})
    if packet_proto.get("header_bytes") != 24:
        raise ValueError(f"Packet header length must be 24 bytes, got {packet_proto.get('header_bytes')}")
    fields = packet_proto.get("fields", [])
    if len(fields) != 6:
        raise ValueError(f"Packet header must define exactly 6 fields, got {len(fields)}")
    expected_offsets = [0, 4, 8, 12, 16, 20]
    for idx, f in enumerate(fields):
        if f.get("offset") != expected_offsets[idx]:
            raise ValueError(f"Field {idx} expected offset {expected_offsets[idx]}, got {f.get('offset')}")
        if f.get("width") != 4:
            raise ValueError(f"Field {idx} width must be 4 bytes, got {f.get('width')}")
        if f.get("endian") != "LITTLE_ENDIAN":
            raise ValueError(f"Field {idx} endian must be 'LITTLE_ENDIAN', got {f.get('endian')}")

    # 7. Commands Supported in State Machine
    cmds = packet_proto.get("commands", {})
    req_cmds = {"CNXN", "OPEN", "WRTE", "CLSE", "OKAY"}
    if not req_cmds.issubset(set(cmds.keys())):
        raise ValueError(f"Packet commands missing required entries: {req_cmds - set(cmds.keys())}")
    if cmds["CNXN"]["constant"] != "0x4e584e43":
        raise ValueError("CNXN command constant must be 0x4e584e43")
    if cmds["OPEN"]["constant"] != "0x4e45504f":
        raise ValueError("OPEN command constant must be 0x4e45504f")
    if cmds["WRTE"]["constant"] != "0x45545257":
        raise ValueError("WRTE command constant must be 0x45545257")
    if cmds["CLSE"]["constant"] != "0x45534c43":
        raise ValueError("CLSE command constant must be 0x45534c43")
    if cmds["OKAY"]["constant"] != "0x59414b4f":
        raise ValueError("OKAY command constant must be 0x59414b4f")

    # 8. Downstream Topology & Absence of External 127.0.0.1:5555 TCP Bridge
    downstream = top_d.get("downstream_topology", {})
    top_cls = downstream.get("classification")
    if top_cls != "IN_PROCESS_PTY_SHELL_BOUNDARY":
        raise ValueError(f"Downstream classification must be 'IN_PROCESS_PTY_SHELL_BOUNDARY', got '{top_cls}'")
    ext_tcp = downstream.get("external_tcp_bridge", {})
    if ext_tcp.get("status") != "ABSENT_UNREACHABLE":
        raise ValueError(f"External TCP bridge status must be 'ABSENT_UNREACHABLE', got '{ext_tcp.get('status')}'")
    if ext_tcp.get("reachable_net_dial_calls") != 0:
        raise ValueError(f"Reachable net.Dial calls must be 0, got {ext_tcp.get('reachable_net_dial_calls')}")
    if ext_tcp.get("string_occurrences") != 0:
        raise ValueError(f"127.0.0.1:5555 string occurrences must be 0, got {ext_tcp.get('string_occurrences')}")

    # 9. Clean-Room Scope Guard
    cr_scope = downstream.get("clean_room_scope", "")
    if "DEFERRED_ADB_BRIDGE_BOUNDARY" not in cr_scope:
        raise ValueError(f"Clean room scope must specify DEFERRED_ADB_BRIDGE_BOUNDARY, got '{cr_scope}'")

    # 10. Callgraph Terminal Boundary
    arm_cg = cg_d.get("nodes", {}).get("ARM64", {})
    amd_cg = cg_d.get("nodes", {}).get("AMD64", {})
    if arm_cg.get("terminal_boundary") != "DEFERRED_ADB_BRIDGE_BOUNDARY":
        raise ValueError(f"ARM64 callgraph terminal boundary must be DEFERRED_ADB_BRIDGE_BOUNDARY, got {arm_cg.get('terminal_boundary')}")
    if amd_cg.get("terminal_boundary") != "DEFERRED_ADB_BRIDGE_BOUNDARY":
        raise ValueError(f"AMD64 callgraph terminal boundary must be DEFERRED_ADB_BRIDGE_BOUNDARY, got {amd_cg.get('terminal_boundary')}")

    # 11. Source Provenance Invariant
    facts_list = prov_d.get("facts", [])
    if len(facts_list) < 8:
        raise ValueError(f"Source provenance must define at least 8 facts, got {len(facts_list)}")
    facts_by_id = {f.get("fact_id"): f for f in facts_list}

    # Verify FACT-ADB-01 (Label & dispatch)
    f1 = facts_by_id.get("FACT-ADB-01")
    if not f1 or "0x53f2ac" not in f1.get("arm64_evidence", {}).get("va", "") or "0x9e2fad" not in f1.get("amd64_evidence", {}).get("va", ""):
        raise ValueError("Source provenance FACT-ADB-01 missing required dispatch sites (ARM64 0x53f2ac, AMD64 0x9e2fad)")

    # Verify FACT-ADB-06 (Response Send)
    f6 = facts_by_id.get("FACT-ADB-06")
    if not f6 or "0x49a3d0" not in f6.get("arm64_evidence", {}).get("call", "") or "0x9250c0" not in f6.get("amd64_evidence", {}).get("call", ""):
        raise ValueError("Source provenance FACT-ADB-06 missing (*DataChannel).Send callsites (ARM64 0x49a3d0, AMD64 0x9250c0)")

    # Verify FACT-ADB-07 (Absence of external TCP bridge)
    f7 = facts_by_id.get("FACT-ADB-07")
    if not f7 or f7.get("arm64_evidence", {}).get("reachable_net_dial") != 0 or f7.get("amd64_evidence", {}).get("reachable_net_dial") != 0:
        raise ValueError("Source provenance FACT-ADB-07 must confirm 0 reachable net.Dial calls across architectures")

    # 12. Contract Taxonomy Invariant
    tc = contract_d.get("metadata", {}).get("taxonomy_counts", {})
    if tc.get("original_static_evidence") != 8:
        raise ValueError(f"Contract taxonomy original_static_evidence must be 8, got {tc.get('original_static_evidence')}")
    if tc.get("reference_interoperability") != 1:
        raise ValueError(f"Contract taxonomy reference_interoperability must be 1, got {tc.get('reference_interoperability')}")
    if tc.get("reference_background") != 1:
        raise ValueError(f"Contract taxonomy reference_background must be 1, got {tc.get('reference_background')}")
    if tc.get("safe_scope_guard") != 1:
        raise ValueError(f"Contract taxonomy safe_scope_guard must be 1, got {tc.get('safe_scope_guard')}")
    if tc.get("deferred_execution_boundary") != 1:
        raise ValueError(f"Contract taxonomy deferred_execution_boundary must be 1, got {tc.get('deferred_execution_boundary')}")
    if tc.get("audit_provenance_guard") != 1:
        raise ValueError(f"Contract taxonomy audit_provenance_guard must be 1, got {tc.get('audit_provenance_guard')}")
    if tc.get("unknown") != 0:
        raise ValueError(f"Contract taxonomy unknown must be 0, got {tc.get('unknown')}")

    reqs = contract_d.get("requirements", [])
    if len(reqs) != 13:
        raise ValueError(f"Contract must define exactly 13 requirements, got {len(reqs)}")

    # 13. Errata Verification (if present)
    if err_d:
        corrs = err_d.get("corrections", [])
        corr_ids = {c.get("contract_id") for c in corrs}
        if "ADB-B6F-ERRATA-01" not in corr_ids or "ADB-B6F-ERRATA-02" not in corr_ids:
            raise ValueError("Formal errata missing required corrections ADB-B6F-ERRATA-01 or ADB-B6F-ERRATA-02")

    return {
        "status": "VALID",
        "channel_label": channel_label,
        "creator_side": creator,
        "consumer_side": consumer,
        "dual_modes_validated": ["ADB_PACKET_MODE", "BARE_RAW_PTY_MODE"],
        "commands_validated": list(cmds.keys()),
        "downstream_classification": top_cls,
        "external_tcp_dial_count": 0,
        "provenance_facts_validated": len(facts_list),
        "contract_requirements_validated": len(reqs)
    }


def main():
    res = validate_adb_channel_semantics()
    print("Shared Semantic Validator (Phase 2C.5B6F): PASS")
    print(f"  Channel: {res['channel_label']} ({res['creator_side']} -> {res['consumer_side']})")
    print(f"  Modes: {res['dual_modes_validated']}")
    print(f"  Commands: {res['commands_validated']}")
    print(f"  Downstream: {res['downstream_classification']} (net.Dial: {res['external_tcp_dial_count']})")
    print(f"  Provenance Facts: {res['provenance_facts_validated']}")
    print(f"  Contract Requirements: {res['contract_requirements_validated']}")


if __name__ == "__main__":
    main()
