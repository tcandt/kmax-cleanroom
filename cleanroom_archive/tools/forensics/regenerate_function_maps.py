import os
import sys
import json
import struct
import re
import bisect
from pathlib import Path
from collections import defaultdict

# Add repo root to sys.path portably
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root, parse_elf_sections, parse_pclntab

ROOT = get_repo_root()
SIGNALING_LINUX = ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
AGENT_ARM64 = ROOT / "cloudphone-v0.3.6 (1)" / "android" / "cloudphone-agent"

EV_SIG = ROOT / "evidence" / "go_signaling"
EV_AGENT = ROOT / "evidence" / "go_agent"

def extract_strings_and_calls_x86_64(data, text_sec, rodata_sec, functions):
    text_data = data[text_sec["offset"] : text_sec["offset"] + text_sec["size"]]
    text_base_va = text_sec["addr"]
    rodata_base_va = rodata_sec["addr"]
    rodata_end_va = rodata_base_va + rodata_sec["size"]

    func_vas = [f["va_int"] for f in functions]
    func_by_va = {f["va_int"]: f for f in functions}

    def get_func(va):
        idx = bisect.bisect_right(func_vas, va) - 1
        if 0 <= idx < len(functions):
            f = functions[idx]
            if f["va_int"] <= va < f["va_int"] + f["size"]:
                return f
        return None

    func_strings = defaultdict(list)
    func_calls = defaultdict(list)

    # 1. Direct Near CALL: E8 disp32
    for m in re.finditer(rb'\xe8', text_data):
        off = m.start()
        if off + 5 <= len(text_data):
            disp = struct.unpack_from("<i", text_data, off + 1)[0]
            target_va = text_base_va + off + 5 + disp
            if target_va in func_by_va:
                caller = get_func(text_base_va + off)
                callee = func_by_va[target_va]
                if caller and callee and caller["va_int"] != callee["va_int"]:
                    callee_name = callee["name"]
                    if callee_name not in func_calls[caller["va_str"]]:
                        func_calls[caller["va_str"]].append(callee_name)

    # 2. RIP-relative LEA: 48 8d [05/0d/15/1d/25/2d/35/3d] disp32
    for m in re.finditer(rb'\x48\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]', text_data):
        off = m.start()
        if off + 7 <= len(text_data):
            disp = struct.unpack_from("<i", text_data, off + 3)[0]
            target_va = text_base_va + off + 7 + disp
            if rodata_base_va <= target_va < rodata_end_va:
                caller = get_func(text_base_va + off)
                if not caller:
                    continue

                str_off = rodata_sec["offset"] + (target_va - rodata_base_va)
                s_val = None
                if off + 12 <= len(text_data):
                    next_op = text_data[off + 7]
                    if 0xb8 <= next_op <= 0xbf:
                        str_len = struct.unpack_from("<I", text_data, off + 8)[0]
                        if 1 <= str_len <= 128 and str_off + str_len <= len(data):
                            raw = data[str_off : str_off + str_len]
                            try:
                                cand = raw.decode("utf-8")
                                if cand.isprintable() and len(cand.strip()) >= 3:
                                    s_val = cand
                            except UnicodeDecodeError:
                                pass

                if not s_val:
                    raw = data[str_off : str_off + 80]
                    clean = []
                    for b in raw:
                        if 32 <= b <= 126:
                            clean.append(chr(b))
                        else:
                            break
                    cand = "".join(clean)
                    if len(cand) >= 4 and any(k in cand for k in ["/api", "ws", "user", "pass", "token", "device", "admin", "json", "http"]):
                        s_val = cand[:60]

                if s_val and s_val not in func_strings[caller["va_str"]]:
                    func_strings[caller["va_str"]].append(s_val)

    return func_strings, func_calls

def extract_strings_and_calls_arm64(data, text_sec, rodata_sec, functions):
    text_data = data[text_sec["offset"] : text_sec["offset"] + text_sec["size"]]
    text_base_va = text_sec["addr"]
    rodata_base_va = rodata_sec["addr"]
    rodata_end_va = rodata_base_va + rodata_sec["size"]

    func_vas = [f["va_int"] for f in functions]
    func_by_va = {f["va_int"]: f for f in functions}

    def get_func(va):
        idx = bisect.bisect_right(func_vas, va) - 1
        if 0 <= idx < len(functions):
            f = functions[idx]
            if f["va_int"] <= va < f["va_int"] + f["size"]:
                return f
        return None

    func_strings = defaultdict(list)
    func_calls = defaultdict(list)

    num_insns = len(text_data) // 4
    for i in range(num_insns):
        insn_off = i * 4
        insn = struct.unpack_from("<I", text_data, insn_off)[0]
        pc = text_base_va + insn_off

        # 1. BL imm26
        if (insn & 0xFC000000) == 0x94000000:
            imm26 = insn & 0x03FFFFFF
            if imm26 & 0x02000000:
                imm26 -= 0x04000000
            target_va = pc + (imm26 * 4)
            if target_va in func_by_va:
                caller = get_func(pc)
                callee = func_by_va[target_va]
                if caller and callee and caller["va_int"] != callee["va_int"]:
                    callee_name = callee["name"]
                    if callee_name not in func_calls[caller["va_str"]]:
                        func_calls[caller["va_str"]].append(callee_name)

        # 2. ADRP + ADD
        if (insn & 0x9F000000) == 0x90000000:
            rd = insn & 0x1F
            immlo = (insn >> 29) & 0x3
            immhi = (insn >> 5) & 0x7FFFF
            imm = (immhi << 2) | immlo
            if imm & 0x100000:
                imm -= 0x200000
            page_addr = (pc & ~0xFFF) + (imm << 12)

            if insn_off + 4 < len(text_data):
                next_insn = struct.unpack_from("<I", text_data, insn_off + 4)[0]
                if (next_insn & 0xFF800000) == 0x91000000:
                    rn = (next_insn >> 5) & 0x1F
                    if rn == rd:
                        imm12 = (next_insn >> 10) & 0xFFF
                        target_va = page_addr + imm12
                        if rodata_base_va <= target_va < rodata_end_va:
                            caller = get_func(pc)
                            if caller:
                                str_off = rodata_sec["offset"] + (target_va - rodata_base_va)
                                raw = data[str_off : str_off + 80]
                                clean = []
                                for b in raw:
                                    if 32 <= b <= 126:
                                        clean.append(chr(b))
                                    else:
                                        break
                                cand = "".join(clean)
                                if len(cand) >= 4 and any(k in cand for k in ["scrcpy", "video", "audio", "webrtc", "token", "signaling", "agent", "uds", "control"]):
                                    if cand[:60] not in func_strings[caller["va_str"]]:
                                        func_strings[caller["va_str"]].append(cand[:60])

    return func_strings, func_calls

def regenerate_binary_function_map(target_name, filepath, ev_dir, is_signaling=True):
    print(f"[*] Regenerating function map for {target_name} ({filepath})...")
    with open(filepath, "rb") as f:
        data = f.read()

    secs = parse_elf_sections(data)
    pcln_data = data[secs[".gopclntab"]["offset"] : secs[".gopclntab"]["offset"] + secs[".gopclntab"]["size"]]
    parsed_pcln = parse_pclntab(pcln_data)

    text_sec = secs[".text"]
    rodata_sec = secs[".rodata"]
    text_base_va = text_sec["addr"]
    text_off = text_sec["offset"]

    raw_funcs = parsed_pcln["functions"]
    raw_funcs.sort(key=lambda x: x["va"])

    functions = []
    for i, fn in enumerate(raw_funcs):
        va_int = fn["va"]
        file_offset = text_off + (va_int - text_base_va)
        functions.append({
            "index": i,
            "va_str": hex(va_int),
            "va_int": va_int,
            "file_offset_str": hex(file_offset),
            "size": fn["size"],
            "name": fn["name"]
        })

    if is_signaling:
        func_strings, func_calls = extract_strings_and_calls_x86_64(data, text_sec, rodata_sec, functions)
    else:
        func_strings, func_calls = extract_strings_and_calls_arm64(data, text_sec, rodata_sec, functions)

    func_map = []
    for fn in functions:
        va_str = fn["va_str"]
        sym = fn["name"]
        xrefs = func_strings.get(va_str, [])
        callees = func_calls.get(va_str, [])

        is_garbled = bool(re.search(r'\b[A-Za-z0-9_]{6,12}\b', sym) and not sym.startswith(("runtime.", "internal/", "sync.", "math.", "reflect.", "syscall.", "net/", "os.", "time.", "encoding/json", "crypto/")))

        func_map.append({
            "index": fn["index"],
            "va": va_str,
            "file_offset": fn["file_offset_str"],
            "size_bytes": fn["size"],
            "symbol_name": sym,
            "is_garbled": is_garbled,
            "referenced_strings": xrefs[:10],
            "callees": callees[:10]
        })

    ev_dir.mkdir(parents=True, exist_ok=True)

    with open(ev_dir / "FUNCTION_MAP.json", "w", encoding="utf-8") as f:
        json.dump(func_map, f, indent=2, ensure_ascii=False)

    with open(ev_dir / "CALLGRAPH.json", "w", encoding="utf-8") as f:
        json.dump(func_calls, f, indent=2, ensure_ascii=False)

    with open(ev_dir / "FUNCTION_MAP.md", "w", encoding="utf-8") as f:
        f.write(f"# Function Map: {target_name}\n\n")
        f.write(f"- **Total Functions Recovered**: {len(func_map)}\n")
        f.write(f"- **Total Functions with Direct Call Edges**: {len(func_calls)}\n")
        f.write(f"- **Total Functions with String Xrefs**: {len(func_strings)}\n\n")
        f.write("| Index | VA | Size | Symbol Name |\n")
        f.write("|---|---|---|---|\n")
        for fn in func_map[:300]:
            f.write(f"| {fn['index']} | `{fn['va']}` | {fn['size_bytes']} | `{fn['symbol_name']}` |\n")
        if len(func_map) > 300:
            f.write(f"\n*... and {len(func_map) - 300} additional functions documented in FUNCTION_MAP.json*\n")

    print(f"[+] Successfully wrote FUNCTION_MAP.json, FUNCTION_MAP.md, CALLGRAPH.json to {ev_dir}")

def main():
    regenerate_binary_function_map("WebRTC Signaling Server", SIGNALING_LINUX, EV_SIG, is_signaling=True)
    regenerate_binary_function_map("CloudPhone Agent Daemon", AGENT_ARM64, EV_AGENT, is_signaling=False)

if __name__ == "__main__":
    main()
