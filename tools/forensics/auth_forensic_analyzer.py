import os
import sys
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.forensics.pclntab_parser import get_repo_root

ELF_PATH = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
FN_MAP_PATH = REPO_ROOT / "evidence" / "go_signaling" / "FUNCTION_MAP.json"
CG_PATH = REPO_ROOT / "evidence" / "go_signaling" / "CALLGRAPH.json"
ROLES_PATH = REPO_ROOT / "evidence" / "go_signaling" / "ROLE_MAPPING.json"
ROUTES_PATH = REPO_ROOT / "evidence" / "go_signaling" / "ROUTE_HANDLER_MAP.json"

def main():
    print("=== Analyzing Auth Subsystem in webrtc-signaling ===")
    fn_map = json.loads(FN_MAP_PATH.read_text("utf-8"))
    cg = json.loads(CG_PATH.read_text("utf-8"))
    routes = json.loads(ROUTES_PATH.read_text("utf-8"))

    # Map VA to function info
    fn_by_va = {f["va"]: f for f in fn_map}
    fn_by_name = {f["symbol_name"]: f for f in fn_map}

    # Read ELF to extract code
    with open(ELF_PATH, "rb") as f:
        elf_bytes = f.read()

    # We need to map VA to file offset
    # In Linux AMD64 ELF: text segment usually loaded at 0x400000 with 0 offset or similar
    # Let's inspect ELF program headers
    import struct
    e_phoff, = struct.unpack_from("<Q", elf_bytes, 32)
    e_phentsize, e_phnum = struct.unpack_from("<HH", elf_bytes, 54)

    ph_list = []
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsize
        p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack_from("<IIQQQQQQ", elf_bytes, off)
        if p_type == 1: # PT_LOAD
            ph_list.append((p_vaddr, p_vaddr + p_memsz, p_offset, p_filesz))

    def va_to_offset(va):
        for vstart, vend, off, fsz in ph_list:
            if vstart <= va < vend:
                return off + (va - vstart)
        return None

    cs = Cs(CS_ARCH_X86, CS_MODE_64)
    cs.detail = True

    # Identify routes of interest
    auth_routes = [
        "/api/login",
        "/api/logout",
        "/api/auth-status",
        "/api/me",
        "/api/admin/users/kick",
        "/api/register"
    ]

    target_vas = {}
    for r in routes["routes"]:
        if r["pattern"] in auth_routes:
            target_vas[r["handler_va"]] = (r["pattern"], r["handler_symbol"])

    print(f"Target Route Handlers: {target_vas}")

    # Explore handlers and their callees recursively (depth 2)
    explored = {}
    queue = list(target_vas.keys())

    all_auth_vas = set(target_vas.keys())
    for tva in target_vas:
        callees = cg.get(tva, [])
        for cname in callees:
            cfn = fn_by_name.get(cname)
            if cfn:
                all_auth_vas.add(cfn["va"])
                for cname2 in cg.get(cfn["va"], []):
                    cfn2 = fn_by_name.get(cname2)
                    if cfn2:
                        all_auth_vas.add(cfn2["va"])

    print(f"Total candidate auth functions: {len(all_auth_vas)}")

    funcs_to_inspect = [
        "0x739060", "0x739240", "0x739320", "0x73b080",
        "0x73dd00", "0x73ec40", "0x73f100", "0x73fdc0", "0x7409a0", "0x747880"
    ]

    for va_str in funcs_to_inspect:
        fn = fn_by_va.get(va_str)
        if not fn:
            continue
        va = int(va_str, 16)
        size = fn["size_bytes"]
        off = va_to_offset(va)
        if off is None:
            continue

        code = elf_bytes[off : off + size]
        disasm = list(cs.disasm(code, va))

        calls = []
        for insn in disasm:
            if insn.mnemonic == "call":
                try:
                    target = int(insn.op_str, 16)
                    target_va = f"0x{target:x}"
                    callee_fn = fn_by_va.get(target_va)
                    callee_name = callee_fn["symbol_name"] if callee_fn else "UNKNOWN"
                    calls.append(f"{callee_name} ({target_va})")
                except:
                    calls.append(insn.op_str)

        print(f"\n==================================================")
        print(f"Function: {fn['symbol_name']} ({va_str}) - Size: {size} bytes")
        if va_str in target_vas:
            print(f"ROUTE: {target_vas[va_str][0]}")
        print("Calls:")
        for c in list(dict.fromkeys(calls)):
            print(f"  -> {c}")

if __name__ == "__main__":
    main()
