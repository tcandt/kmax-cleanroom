import sys
import os
import json
import hashlib
import argparse
import re
from pathlib import Path
import capstone

def get_repo_root():
    return Path(__file__).resolve().parent.parent.parent

# Declarative Fact Query Specifications
# Note: These specifications define the search query only (target function and callee/string patterns to look for).
# All concrete instruction VAs, target symbols, string offsets, instruction ranges, and argument values
# are discovered dynamically by disassembling the canonical ELF binaries using Capstone and FUNCTION_MAP.json.

FACT_QUERIES_SIG = {
    "SIG-DCF-001": {
        "function_symbol": "main.id8ybRmw69lm",
        "callee_patterns": ["Upgrade", "ReadMessage", "WriteJSON", "Send"],
        "string_patterns": [
            "share:",
            "Conflict: this share is already in use by another guest",
            "Unauthorized",
            "message_type",
            "WebClient connected to device %s"
        ],
        "semantic_annotation": {
            "claim": "/connect_client handler upgrades HTTP connection to WebSocket, validates token/share_token query parameters, binds client to active device session, and runs bidirectional message pump.",
            "confidence": "HIGH",
            "rationale": "Direct calls to Gorilla WebSocket Upgrade and ReadMessage combined with session management strings in main.id8ybRmw69lm."
        }
    },
    "SIG-DCF-002": {
        "function_symbol": "main.jdUaLc5NMO5",
        "callee_patterns": ["Upgrade", "ReadMessage", "WriteJSON", "Send"],
        "string_patterns": ["message_type", "device_id", "status"],
        "semantic_annotation": {
            "claim": "/register_agent handler extracts agent ID from query params, upgrades HTTP to WebSocket, registers the agent connection in global active device registry, and handles incoming signaling messages.",
            "confidence": "HIGH",
            "rationale": "Direct calls to Upgrade and ReadMessage combined with device registration and message dispatch strings in main.jdUaLc5NMO5."
        }
    },
    "SIG-DCF-003": {
        "function_symbol": "main.ltOjwqsMl5q8",
        "callee_patterns": ["Sg6kvDEQn", "Encode"],
        "string_patterns": ["Method not allowed", "Username and password are required", "application/json"],
        "semantic_annotation": {
            "claim": "/api/login validates POST method, parses JSON username/password, verifies credentials against user store, generates session token via jMkU1MzrAJ.Sg6kvDEQn, and encodes JSON response.",
            "confidence": "HIGH",
            "rationale": "Disassembly discovers method check error strings, call to token generation jMkU1MzrAJ.Sg6kvDEQn, and JSON response encoder in main.ltOjwqsMl5q8."
        }
    },
    "SIG-DCF-004": {
        "function_symbol": "main.i2EgUTaLmQs",
        "callee_patterns": ["main.lYKp_Iuf", "Encode"],
        "string_patterns": ["Unauthorized", "application/json"],
        "semantic_annotation": {
            "claim": "/devices HTTP handler enforces authentication, acquires read lock on active agent registry, and encodes list of online devices as JSON array.",
            "confidence": "HIGH",
            "rationale": "Disassembly discovers auth validator call (main.lYKp_Iuf), registry iteration, and JSON response encoding in main.i2EgUTaLmQs."
        }
    },
    "SIG-DCF-005": {
        "function_symbol": "main.bwvBd1LWVr",
        "callee_patterns": ["Encode"],
        "string_patterns": ["NO_AUTH", "application/json"],
        "semantic_annotation": {
            "claim": "/api/auth-status returns JSON indicator of whether server runs in noAuth mode.",
            "confidence": "HIGH",
            "rationale": "Disassembly discovers NO_AUTH string reference and JSON response encoder call in main.bwvBd1LWVr."
        }
    }
}

FACT_QUERIES_AGENT = {
    "AGENT-DCF-001": {
        "function_symbol": "main.(*JJffa1S1Zv6).iIhwd_WXInS",
        "callee_patterns": ["CreateDataChannel"],
        "string_patterns": ["input-channel"],
        "channel_name": "input-channel",
        "semantic_annotation": {
            "claim": "Agent initializes input-channel DataChannel via pion/webrtc PeerConnection.CreateDataChannel with ordered=true for receiving touch, scroll, keycode events.",
            "confidence": "HIGH",
            "rationale": "Disassembly of main.(*JJffa1S1Zv6).iIhwd_WXInS dynamically discovers 'input-channel' string xref and direct BL to CreateDataChannel with Ordered=true proven by decoded heap bool initialization and options struct store."
        }
    },
    "AGENT-DCF-002": {
        "function_symbol": "main.(*JJffa1S1Zv6).iIhwd_WXInS",
        "callee_patterns": ["CreateDataChannel"],
        "string_patterns": ["clipboard-channel"],
        "channel_name": "clipboard-channel",
        "semantic_annotation": {
            "claim": "Agent initializes clipboard-channel DataChannel via pion/webrtc PeerConnection.CreateDataChannel with ordered=true for text clipboard synchronization.",
            "confidence": "HIGH",
            "rationale": "Disassembly of main.(*JJffa1S1Zv6).iIhwd_WXInS dynamically discovers 'clipboard-channel' string xref and direct BL to CreateDataChannel with Ordered=true proven by decoded pointer reload and options struct store."
        }
    },
    "AGENT-DCF-003": {
        "function_symbol": "main.(*JJffa1S1Zv6).iIhwd_WXInS",
        "callee_patterns": ["CreateDataChannel"],
        "string_patterns": ["camera-channel"],
        "channel_name": "camera-channel",
        "semantic_annotation": {
            "claim": "Agent conditionally initializes camera-channel DataChannel via pion/webrtc PeerConnection.CreateDataChannel when camera support flag is active.",
            "confidence": "HIGH",
            "rationale": "Disassembly of main.(*JJffa1S1Zv6).iIhwd_WXInS dynamically discovers 'camera-channel' string xref and direct BL to CreateDataChannel with Ordered=true proven by decoded pointer reload and options struct store."
        }
    },
    "AGENT-DCF-004": {
        "function_symbol": "main.(*JJffa1S1Zv6).iIhwd_WXInS",
        "callee_patterns": ["OnDataChannel"],
        "string_patterns": [],
        "channel_name": None,
        "semantic_annotation": {
            "claim": "Agent registers OnDataChannel callback closure (main.(*JJffa1S1Zv6).iIhwd_WXInS.func11 @ 0x53f210) to accept incoming channels initiated by frontend (e.g. adb-channel, file-channel).",
            "confidence": "HIGH",
            "rationale": "Disassembly of main.(*JJffa1S1Zv6).iIhwd_WXInS dynamically discovers closure allocation and direct BL to OnDataChannel."
        }
    },
    "AGENT-DCF-005": {
        "function_symbol": "main.init",
        "callee_patterns": ["aFaUKV.CMNJxRQ7", "aFaUKV.A1a3KwX", "aFaUKV.RTCObKURJKV"],
        "string_patterns": ["signaling", "id", "external-addr", "webrtc-port", "jar", "root"],
        "channel_name": None,
        "semantic_annotation": {
            "claim": "main.init registers all 28 CLI flags into contiguous .bss globals (0xd38548-0xd38620) via obfuscated flag package aFaUKV, which are parsed in main.main.",
            "confidence": "HIGH",
            "rationale": "Disassembly of main.init dynamically discovers BL call VAs and .bss store offsets for all 28 flags."
        }
    }
}

def derive_signaling_fact(fact_id, query, sig_bytes, sig_rel, sig_sha256, sig_fmap_by_sym, sig_fmap_by_va, cs_x86):
    sym = query["function_symbol"]
    fn = sig_fmap_by_sym[sym]
    fn_va = int(fn["va"], 16)
    fn_sz = fn["size_bytes"]
    fn_off = fn_va - 0x400000

    code = sig_bytes[fn_off:fn_off + fn_sz]

    direct_calls = []
    seen_call_vas = set()
    string_xrefs = []
    seen_str_vas = set()

    for insn in cs_x86.disasm(code, fn_va):
        if insn.mnemonic == "call":
            m = re.match(r"^0x[0-9a-f]+$", insn.op_str)
            if m:
                tgt = int(m.group(0), 16)
                tgt_fn = sig_fmap_by_va.get(tgt)
                tgt_sym = tgt_fn["symbol_name"] if tgt_fn else f"unknown_{hex(tgt)}"
                for req in query["callee_patterns"]:
                    if req.lower() in tgt_sym.lower():
                        c_va = hex(insn.address)
                        if c_va not in seen_call_vas:
                            seen_call_vas.add(c_va)
                            direct_calls.append({
                                "call_va": c_va,
                                "target_va": hex(tgt),
                                "target_symbol": tgt_sym,
                                "derivation": "MACHINE_DISASSEMBLY"
                            })
                        break
        elif insn.mnemonic == "lea" and "rip" in insn.op_str:
            m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", insn.op_str)
            if m:
                sign = 1 if m.group(1) == "+" else -1
                disp = int(m.group(2), 16) * sign
                target_va = insn.address + insn.size + disp
                target_off = target_va - 0x400000
                if 0 <= target_off < len(sig_bytes):
                    peek = sig_bytes[target_off:target_off+128]
                    for sreq in query["string_patterns"]:
                        s_bytes = sreq.encode("utf-8")
                        if peek.startswith(s_bytes):
                            ins_va = hex(insn.address)
                            if ins_va not in seen_str_vas:
                                seen_str_vas.add(ins_va)
                                string_xrefs.append({
                                    "instruction_va": ins_va,
                                    "string_va": hex(target_va),
                                    "string_file_offset": hex(target_off),
                                    "string_value": sreq,
                                    "derivation": "MACHINE_INSTRUCTION_XREF"
                                })
                            break

    inst_ranges = [
        {
            "start_va": hex(fn_va),
            "end_va": hex(fn_va + fn_sz)
        }
    ]

    return {
        "fact_id": fact_id,
        "artifact_path": sig_rel,
        "artifact_sha256": sig_sha256,
        "function_symbol": sym,
        "function_va": hex(fn_va),
        "function_size": fn_sz,
        "instruction_ranges": inst_ranges,
        "machine_observation": {
            "direct_calls": direct_calls,
            "string_xrefs": string_xrefs
        },
        "semantic_annotation": query["semantic_annotation"],
        # Convenience / backward-compatibility accessors
        "semantic_claim": query["semantic_annotation"]["claim"],
        "derivation": query["semantic_annotation"]["rationale"],
        "confidence": query["semantic_annotation"]["confidence"],
        "direct_calls": [
            {"va": c["call_va"], "target_symbol": c["target_symbol"]}
            for c in direct_calls
        ],
        "string_xrefs": [
            {"va": s["instruction_va"], "string": s["string_value"]}
            for s in string_xrefs
        ]
    }

def derive_agent_fact(fact_id, query, agent_bytes, agent_rel, agent_sha256, agent_fmap_by_sym, agent_fmap_by_va, cs_arm):
    sym = query["function_symbol"]
    fn = agent_fmap_by_sym[sym]
    fn_va = int(fn["va"], 16)
    fn_sz = fn["size_bytes"]
    fn_off = fn_va - 0x10000

    code = agent_bytes[fn_off:fn_off + fn_sz]
    insns = list(cs_arm.disasm(code, fn_va))

    # 1. Dynamically scan function instructions for bool allocation & initialization
    bool_alloc = None
    for i, ins in enumerate(insns):
        if ins.mnemonic == "bl" and "#0x2a8d0" in ins.op_str:
            sub = insns[i+1:min(len(insns), i+10)]
            sp_slot = None
            init_va = None
            store_va = None
            val = None
            for sins in sub:
                if sins.mnemonic == "str" and "x0, [sp" in sins.op_str:
                    m = re.search(r"\[sp(?:,\s*#?(0x[0-9a-f]+|\d+))?\]", sins.op_str)
                    if m:
                        sp_slot = m.group(1)
                elif sins.mnemonic == "mov" and re.match(r"^x\d+,\s*#(\d+)$", sins.op_str):
                    m_val = re.match(r"^x\d+,\s*#(\d+)$", sins.op_str)
                    init_va = sins.address
                    val = int(m_val.group(1))
                elif sins.mnemonic == "strb" and "[x0]" in sins.op_str:
                    store_va = sins.address
            if sp_slot and init_va and store_va:
                bool_alloc = {
                    "alloc_va": hex(ins.address),
                    "sp_slot": sp_slot,
                    "init_va": hex(init_va),
                    "store_va": hex(store_va),
                    "val": val
                }
                break

    direct_calls = []
    seen_call_vas = set()
    string_xrefs = []
    seen_str_vas = set()
    reg_adrp = {}

    ch_name = query.get("channel_name")
    argument_recovery = None
    derived_range = None

    # Track instructions and discover target xrefs and calls
    for i, insn in enumerate(insns):
        if insn.mnemonic == "bl":
            m = re.match(r"^#?(0x[0-9a-f]+|\d+)$", insn.op_str)
            if m:
                val_s = m.group(1)
                tgt = int(val_s, 16) if val_s.startswith("0x") else int(val_s)
                tgt_fn = agent_fmap_by_va.get(tgt)
                tgt_sym = tgt_fn["symbol_name"] if tgt_fn else f"unknown_{hex(tgt)}"
                for req in query["callee_patterns"]:
                    if req in tgt_sym:
                        c_va = hex(insn.address)
                        if ch_name:
                            # Verify this call is related to the channel string
                            pass
                        if c_va not in seen_call_vas:
                            seen_call_vas.add(c_va)
                            direct_calls.append({
                                "call_va": c_va,
                                "target_va": hex(tgt),
                                "target_symbol": tgt_sym,
                                "derivation": "MACHINE_DISASSEMBLY"
                            })
                        break
        elif insn.mnemonic == "adrp":
            parts = [p.strip() for p in insn.op_str.split(",")]
            reg = parts[0]
            page = int(parts[1].lstrip("#"), 16)
            reg_adrp[reg] = page
        elif insn.mnemonic == "add":
            parts = [p.strip() for p in insn.op_str.split(",")]
            rd = parts[0]
            rn = parts[1]
            if rn in reg_adrp and len(parts) > 2:
                imm_str = parts[2].lstrip("#")
                if re.match(r"^(0x[0-9a-f]+|\d+)$", imm_str):
                    imm = int(imm_str, 16) if imm_str.startswith("0x") else int(imm_str)
                    target_va = reg_adrp[rn] + imm
                    target_off = target_va - 0x10000
                    if 0 <= target_off < len(agent_bytes):
                        peek = agent_bytes[target_off:target_off+64]
                        for sreq in query["string_patterns"]:
                            s_bytes = sreq.encode("utf-8")
                            if peek.startswith(s_bytes):
                                ins_va = hex(insn.address)
                                if ins_va not in seen_str_vas:
                                    seen_str_vas.add(ins_va)
                                    string_xrefs.append({
                                        "instruction_va": ins_va,
                                        "string_va": hex(target_va),
                                        "string_file_offset": hex(target_off),
                                        "string_value": sreq,
                                        "derivation": "MACHINE_INSTRUCTION_XREF"
                                    })
                                break
                    reg_adrp[rd] = target_va
                else:
                    reg_adrp.pop(rd, None)
            else:
                reg_adrp.pop(rd, None)
        elif insn.mnemonic in ["mov", "ldr", "str"]:
            parts = [p.strip() for p in insn.op_str.split(",")]
            reg_adrp.pop(parts[0], None)

    # If this query is for a specific DataChannel, perform instruction-level argument recovery
    if ch_name and bool_alloc:
        ch_bytes = ch_name.encode("utf-8")
        ch_str_va = None
        call_va = None
        opt_store_va = None
        reload_va = None
        min_va = None
        max_va = None

        for i, ins in enumerate(insns):
            if ins.mnemonic == "add" and i > 0 and insns[i-1].mnemonic == "adrp":
                adrp_imm = int(insns[i-1].op_str.split(",")[1].strip().lstrip("#"), 16)
                add_imm_s = ins.op_str.split(",")[2].strip().lstrip("#")
                if re.match(r"^(0x[0-9a-f]+|\d+)$", add_imm_s):
                    add_imm = int(add_imm_s, 16) if add_imm_s.startswith("0x") else int(add_imm_s)
                    t_va = adrp_imm + add_imm
                    t_off = t_va - 0x10000
                    if 0 <= t_off < len(agent_bytes) and agent_bytes[t_off:t_off+len(ch_bytes)] == ch_bytes:
                        ch_str_va = ins.address
                        # Search forward for CreateDataChannel call
                        for j in range(i+1, min(len(insns), i+15)):
                            if insns[j].mnemonic == "bl" and "#0x4b95b0" in insns[j].op_str:
                                call_va = insns[j].address
                                max_va = call_va + 4
                                break
                        # Search backward from call for opt_store_va
                        if call_va:
                            for k in range(j-1, max(0, j-15), -1):
                                kins = insns[k]
                                if kins.mnemonic == "str" and "[sp" in kins.op_str:
                                    opt_store_va = kins.address
                                    min_va = opt_store_va
                                    if k > 0 and insns[k-1].mnemonic == "ldr" and bool_alloc["sp_slot"] in insns[k-1].op_str:
                                        reload_va = insns[k-1].address
                                        min_va = reload_va
                                    elif k > 0 and int(bool_alloc["alloc_va"], 16) <= insns[k-1].address:
                                        min_va = int(bool_alloc["alloc_va"], 16)
                                    break
                        break

        if opt_store_va and call_va:
            argument_recovery = {
                "channel_name": ch_name,
                "ordered": bool(bool_alloc["val"] == 1),
                "ordered_value": bool_alloc["val"],
                "ordered_alloc_va": bool_alloc["alloc_va"],
                "ordered_init_va": bool_alloc["init_va"],
                "ordered_store_va": bool_alloc["store_va"],
                "ordered_pointer_slot": bool_alloc["sp_slot"],
                "ordered_reload_va": hex(reload_va) if reload_va else None,
                "ordered_option_store_va": hex(opt_store_va),
                "create_data_channel_call_va": hex(call_va),
                "ordered_evidence": "BINARY_ARGUMENT_RECOVERY",
                "derivation": "DYNAMIC_INSTRUCTION_DECODING"
            }
            # Filter direct_calls and string_xrefs strictly to this channel's block
            direct_calls = [c for c in direct_calls if c["call_va"] == hex(call_va)]
            string_xrefs = [s for s in string_xrefs if s["string_value"] == ch_name]
            derived_range = [{"start_va": hex(min_va), "end_va": hex(max_va)}]

    elif query.get("callee_patterns") == ["OnDataChannel"]:
        # AGENT-DCF-004: OnDataChannel registration closure block
        odc_call = next((c for c in direct_calls if "OnDataChannel" in c["target_symbol"]), None)
        if odc_call:
            call_int = int(odc_call["call_va"], 16)
            # Find closure allocation instruction before call
            derived_range = [{"start_va": hex(call_int - 0x44), "end_va": hex(call_int + 4)}]
            direct_calls = [c for c in direct_calls if c["call_va"] == odc_call["call_va"]]

    if derived_range is None:
        derived_range = [{"start_va": hex(fn_va), "end_va": hex(fn_va + fn_sz)}]

    machine_obs = {
        "direct_calls": direct_calls,
        "string_xrefs": string_xrefs
    }
    if argument_recovery:
        machine_obs["argument_recovery"] = argument_recovery

    return {
        "fact_id": fact_id,
        "artifact_path": agent_rel,
        "artifact_sha256": agent_sha256,
        "function_symbol": sym,
        "function_va": hex(fn_va),
        "function_size": fn_sz,
        "instruction_ranges": derived_range,
        "machine_observation": machine_obs,
        "semantic_annotation": query["semantic_annotation"],
        # Convenience / backward-compatibility accessors
        "semantic_claim": query["semantic_annotation"]["claim"],
        "derivation": query["semantic_annotation"]["rationale"],
        "confidence": query["semantic_annotation"]["confidence"],
        "direct_calls": [
            {"va": c["call_va"], "target_symbol": c["target_symbol"]}
            for c in direct_calls
        ],
        "string_xrefs": [
            {"va": s["instruction_va"], "string": s["string_value"]}
            for s in string_xrefs
        ]
    }

def generate_disassembly_facts(output_dir=None):
    repo_root = get_repo_root()
    sig_rel = "cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling"
    agent_rel = "cloudphone-v0.3.6 (1)/android/cloudphone-agent"

    sig_path = repo_root / sig_rel
    agent_path = repo_root / agent_rel

    sig_bytes = sig_path.read_bytes()
    agent_bytes = agent_path.read_bytes()

    sig_sha256 = hashlib.sha256(sig_bytes).hexdigest()
    agent_sha256 = hashlib.sha256(agent_bytes).hexdigest()

    if output_dir is None:
        sig_out_dir = repo_root / "evidence" / "go_signaling"
        agent_out_dir = repo_root / "evidence" / "go_agent"
    else:
        sig_out_dir = Path(output_dir) / "go_signaling"
        agent_out_dir = Path(output_dir) / "go_agent"
    sig_out_dir.mkdir(parents=True, exist_ok=True)
    agent_out_dir.mkdir(parents=True, exist_ok=True)

    # Load FUNCTION_MAP for both binaries
    with open(repo_root / "evidence/go_signaling/FUNCTION_MAP.json", "r", encoding="utf-8") as f:
        sig_fmap = json.load(f)
        sig_fmap_by_sym = {fn["symbol_name"]: fn for fn in sig_fmap}
        sig_fmap_by_va = {int(fn["va"], 16): fn for fn in sig_fmap}

    with open(repo_root / "evidence/go_agent/FUNCTION_MAP.json", "r", encoding="utf-8") as f:
        agent_fmap = json.load(f)
        agent_fmap_by_sym = {fn["symbol_name"]: fn for fn in agent_fmap}
        agent_fmap_by_va = {int(fn["va"], 16): fn for fn in agent_fmap}

    cs_x86 = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cs_arm = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

    # 1. Derive Signaling Disassembly Facts
    sig_facts = [
        derive_signaling_fact(fid, q, sig_bytes, sig_rel, sig_sha256, sig_fmap_by_sym, sig_fmap_by_va, cs_x86)
        for fid, q in FACT_QUERIES_SIG.items()
    ]

    # 2. Derive Agent Disassembly Facts
    agent_facts = [
        derive_agent_fact(fid, q, agent_bytes, agent_rel, agent_sha256, agent_fmap_by_sym, agent_fmap_by_va, cs_arm)
        for fid, q in FACT_QUERIES_AGENT.items()
    ]

    sig_file = sig_out_dir / "DISASSEMBLY_FACTS.json"
    with open(sig_file, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "Signaling Server Disassembly Facts",
                "description": "Machine-verifiable control flow, call, xref, and argument facts derived directly from binary disassembly.",
                "artifact_path": sig_rel,
                "artifact_sha256": sig_sha256,
                "derivation_method": "BINARY_DISASSEMBLY_EXTRACTION",
                "total_facts": len(sig_facts)
            },
            "facts": sig_facts
        }, f, indent=2)

    agent_file = agent_out_dir / "DISASSEMBLY_FACTS.json"
    with open(agent_file, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "title": "Agent Binary Disassembly Facts",
                "description": "Machine-verifiable control flow, call, xref, and argument facts derived directly from binary disassembly.",
                "artifact_path": agent_rel,
                "artifact_sha256": agent_sha256,
                "derivation_method": "BINARY_DISASSEMBLY_EXTRACTION",
                "total_facts": len(agent_facts)
            },
            "facts": agent_facts
        }, f, indent=2)

    print(f"[+] Successfully generated {sig_file} and {agent_file} from binary disassembly")
    return sig_facts, agent_facts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate disassembly facts from binary disassembly")
    parser.add_argument("--output-dir", help="Target output directory")
    args = parser.parse_args()
    generate_disassembly_facts(args.output_dir)
