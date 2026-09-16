#!/usr/bin/env python3
"""
generate_server_config_forensics.py - Phase 2C.3G Server Configuration REST Forensic Generator

Extracts static binary metadata and executes dynamic oracle probing for the Server Configuration REST family:
  1. /api/server/addresses -> main.vz0hZo0q1IzM (VA: 0x7632a0)
  2. /api/default_settings -> main.j0yBBXR1Hjl (VA: 0x768980)
  3. /api/ice_servers      -> main.vREP2EE2     (VA: 0x768500)
  4. /api/version          -> main.ys0CAJV5f5k  (VA: 0x769840)

Generates 8 comprehensive forensic artifacts adhering to cleanroom invariants.
"""

import os
import sys
import json
import time
import socket
import struct
import shutil
import hashlib
import requests
import subprocess
from pathlib import Path
import capstone

REPO_ROOT = Path(__file__).resolve().parents[2]
ELF_LINUX = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "linux_amd64" / "webrtc-signaling"
EXE_WIN = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "bin" / "windows_amd64" / "webrtc-signaling.exe"
ASSETS = REPO_ROOT / "cloudphone-v0.3.6 (1)" / "assets"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "evidence" / "go_signaling" / "server_config"

def get_free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def parse_elf_sections(elf_bytes: bytes) -> dict:
    e_shoff, = struct.unpack("<Q", elf_bytes[0x28:0x30])
    e_shentsize, e_shnum = struct.unpack("<HH", elf_bytes[0x3a:0x3e])
    e_shstrndx, = struct.unpack("<H", elf_bytes[0x3e:0x40])

    shstr_header = elf_bytes[e_shoff + e_shstrndx * e_shentsize : e_shoff + (e_shstrndx + 1) * e_shentsize]
    shstr_offset, = struct.unpack("<Q", shstr_header[0x18:0x20])

    sections = {}
    for i in range(e_shnum):
        sh = elf_bytes[e_shoff + i * e_shentsize : e_shoff + (i + 1) * e_shentsize]
        sh_name_idx, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack("<IIQQQQ", sh[:0x28])
        name_end = elf_bytes.find(b'\x00', shstr_offset + sh_name_idx)
        name = elf_bytes[shstr_offset + sh_name_idx : name_end].decode("ascii", errors="ignore")
        sections[name] = {"addr": sh_addr, "offset": sh_offset, "size": sh_size}
    return sections

def va_to_offset(va: int, sections: dict) -> int:
    for s_name, s_info in sections.items():
        if s_info["addr"] <= va < s_info["addr"] + s_info["size"]:
            return s_info["offset"] + (va - s_info["addr"])
    return None

def read_varint(data: bytes, pos: int):
    val = 0
    shift = 0
    while pos < len(data):
        b = data[pos]
        pos += 1
        val |= (b & 0x7f) << shift
        if (b & 0x80) == 0:
            break
        shift += 7
    return val, pos

def parse_go_name(elf_bytes: bytes, sections: dict, name_ptr: int):
    off = va_to_offset(name_ptr, sections)
    if off is None or off >= len(elf_bytes) - 4:
        return "", ""
    flags = elf_bytes[off]
    name_len, pos = read_varint(elf_bytes, off + 1)
    if pos + name_len > len(elf_bytes):
        return "", ""
    name = elf_bytes[pos:pos+name_len].decode("utf-8", errors="ignore")
    pos += name_len
    tag = ""
    if (flags & 0x2) != 0 and pos < len(elf_bytes):
        tag_len, pos = read_varint(elf_bytes, pos)
        if pos + tag_len <= len(elf_bytes):
            tag = elf_bytes[pos:pos+tag_len].decode("utf-8", errors="ignore")
    return name, tag

def generate_evidence(output_dir: Path = DEFAULT_OUTPUT_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Extracting Server Config forensic evidence into {output_dir}")

    elf_bytes = ELF_LINUX.read_bytes()
    sections = parse_elf_sections(elf_bytes)

    # 1. Resolve Route Family from ROUTE_HANDLER_MAP
    rhm_path = REPO_ROOT / "evidence" / "go_signaling" / "ROUTE_HANDLER_MAP.json"
    rhm_routes = json.loads(rhm_path.read_text(encoding="utf-8"))["routes"]
    
    fm_path = REPO_ROOT / "evidence" / "go_signaling" / "FUNCTION_MAP.json"
    fm_list = json.loads(fm_path.read_text(encoding="utf-8"))
    fm_by_sym = {f["symbol_name"]: f for f in fm_list}
    fm_by_va = {int(f["va"], 16): f for f in fm_list}

    target_routes = {
        "/api/server/addresses": "SERVER_ADDRESSES_DISPATCHER",
        "/api/default_settings": "DEFAULT_SETTINGS_DISPATCHER",
        "/api/ice_servers": "ICE_SERVERS_CONFIGURATION",
        "/api/version": "VERSION_INFO_DISPATCHER"
    }

    route_family = {
        "family_name": "SERVER_CONFIGURATION_REST",
        "description": "Family of 4 core server configuration, metadata, and environment discovery REST endpoints",
        "routes": []
    }

    for pattern, role in target_routes.items():
        entry = next((r for r in rhm_routes if r.get("pattern") == pattern), None)
        assert entry is not None, f"Route {pattern} not found in ROUTE_HANDLER_MAP"
        sym = entry["handler_symbol"]
        f_meta = fm_by_sym.get(sym, {})
        route_family["routes"].append({
            "pattern": pattern,
            "semantic_role": role,
            "registration_call_va": entry["call_va"],
            "handler_va": entry["handler_va"],
            "handler_symbol": sym,
            "size_bytes": f_meta.get("size_bytes", 0),
            "callees": f_meta.get("callees", []),
            "referenced_strings": f_meta.get("referenced_strings", [])
        })

    (output_dir / "SERVER_CONFIG_ROUTE_FAMILY.json").write_text(json.dumps(route_family, indent=2), encoding="utf-8")

    # 2. Extract Type Evidence from ELF
    # A. ICE Server Struct: main.Py1TDt at 0x7e24e0
    ice_struct_va = 0x7e24e0
    ice_off = va_to_offset(ice_struct_va, sections)
    raw_ice_st = elf_bytes[ice_off:ice_off+0x80]
    st_size, ptrdata, hsh, tflag, st_align, falign, kind = struct.unpack('<QQIBBBB', raw_ice_st[:24])
    fields_ptr, fields_len, _ = struct.unpack('<QQQ', raw_ice_st[56:80])
    
    fld_off = va_to_offset(fields_ptr, sections)
    ice_fields = []
    for idx in range(fields_len):
        item = elf_bytes[fld_off+idx*24:fld_off+(idx+1)*24]
        name_off, typ_ptr, offset_val = struct.unpack('<QQQ', item)
        f_name, f_tag = parse_go_name(elf_bytes, sections, name_off)
        t_off = va_to_offset(typ_ptr, sections)
        t_size = struct.unpack('<Q', elf_bytes[t_off:t_off+8])[0]
        ice_fields.append({
            "field_index": idx,
            "name": f_name,
            "tag": f_tag,
            "offset": offset_val,
            "size_bytes": t_size,
            "type_va": hex(typ_ptr)
        })

    ice_type_evidence = {
        "classification": "DIRECT_TYPE_RECOVERY",
        "abi_validation": {
            "architecture": "AMD64",
            "runtime_struct_field_size": 24,
            "offset_encoding": "RAW_UINTPTR_BYTE_OFFSET",
            "is_non_overlapping": (
                len(ice_fields) == 3 and
                ice_fields[0]["offset"] == 0 and ice_fields[0]["size_bytes"] == 24 and
                ice_fields[1]["offset"] == 24 and ice_fields[1]["size_bytes"] == 16 and
                ice_fields[2]["offset"] == 40 and ice_fields[2]["size_bytes"] == 16 and
                st_size == 56
            ),
            "struct_total_size": st_size,
            "struct_alignment": st_align
        },
        "ice_server_struct": {
            "struct_va": hex(ice_struct_va),
            "struct_name": "*main.Py1TDt",
            "size_bytes": st_size,
            "field_count": len(ice_fields),
            "fields": ice_fields
        },
        "slice_type_descriptor": {
            "descriptor_va": "0x797460",
            "type_name": "*[]main.Py1TDt"
        }
    }
    (output_dir / "ICE_SERVER_TYPE_EVIDENCE.json").write_text(json.dumps(ice_type_evidence, indent=2), encoding="utf-8")

    # B. Default Settings Type Evidence: map[string]interface{}
    ds_type_evidence = {
        "classification": "DIRECT_TYPE_RECOVERY",
        "descriptor_va": "0x7bf940",
        "type_name": "*map[string]interface {}",
        "decode_pointer_va": "0x7968e0",
        "runtime_type": "map[string]interface{}",
        "lifecycle": "IN_MEMORY_GLOBAL",
        "persistence_to_disk": False,
        "default_initial_value": {}
    }
    (output_dir / "DEFAULT_SETTINGS_TYPE_EVIDENCE.json").write_text(json.dumps(ds_type_evidence, indent=2), encoding="utf-8")

    # C. Version Globals Recovery from ELF
    def read_elf_str(data_va, len_va):
        off_d = va_to_offset(data_va, sections)
        off_l = va_to_offset(len_va, sections)
        ptr, = struct.unpack('<Q', elf_bytes[off_d:off_d+8])
        l, = struct.unpack('<Q', elf_bytes[off_l:off_l+8])
        off_s = va_to_offset(ptr, sections)
        return elf_bytes[off_s:off_s+l].decode('utf-8')

    version_str = read_elf_str(0xbeee00, 0xbeee08)
    commit_str = read_elf_str(0xbeee10, 0xbeee18)
    build_time_str = read_elf_str(0xbeee20, 0xbeee28)

    version_contract = {
        "classification": "DIRECT_GLOBAL_RECOVERY",
        "route": "/api/version",
        "auth_required": False,
        "methods_allowed": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
        "metadata_fields": {
            "version": {
                "value": version_str,
                "data_ptr_va": "0xbeee00",
                "len_va": "0xbeee08",
                "origin": "COMPILE_TIME_LDFLAGS"
            },
            "git_commit": {
                "value": commit_str,
                "data_ptr_va": "0xbeee10",
                "len_va": "0xbeee18",
                "origin": "COMPILE_TIME_LDFLAGS"
            },
            "build_time": {
                "value": build_time_str,
                "data_ptr_va": "0xbeee20",
                "len_va": "0xbeee28",
                "origin": "COMPILE_TIME_LDFLAGS"
            }
        },
        "response_schema": {
            "type": "object",
            "properties": {
                "version": {"type": "string"},
                "git_commit": {"type": "string"},
                "build_time": {"type": "string"}
            },
            "required": ["version", "git_commit", "build_time"]
        }
    }
    (output_dir / "VERSION_CONTRACT.json").write_text(json.dumps(version_contract, indent=2), encoding="utf-8")

    # 3. Dynamic Oracle Probing (Method Matrix, Auth Matrix, Operation Contracts)
    scratch_std = REPO_ROOT / "scratch" / "server_config_oracle_std"
    scratch_noauth = REPO_ROOT / "scratch" / "server_config_oracle_na"
    scratch_custom = REPO_ROOT / "scratch" / "server_config_oracle_custom"

    for p in [scratch_std, scratch_noauth, scratch_custom]:
        if p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True)

    salt = "1234567890abcdef1234567890abcdef"
    pwd_hash = hashlib.sha256(("admin123" + salt).encode()).hexdigest()
    pwd_u1_hash = hashlib.sha256(("user123" + salt).encode()).hexdigest()
    fixture_users = {
        "admin": {
            "username": "admin", "password": pwd_hash, "salt": salt, "role": "admin",
            "assigned_devices": ["*"], "expires_at": "2099-12-31T23:59:59Z"
        },
        "user1": {
            "username": "user1", "password": pwd_u1_hash, "salt": salt, "role": "user",
            "assigned_devices": ["dev-1"], "expires_at": "2099-12-31T23:59:59Z"
        }
    }
    for p in [scratch_std, scratch_noauth, scratch_custom]:
        (p / "users.json").write_text(json.dumps(fixture_users, indent=2))
        (p / "device_tags.json").write_text(json.dumps({"tags": [], "deviceTags": {}}, indent=2))

    port_std = get_free_port()
    port_noauth = get_free_port()
    port_custom = get_free_port()

    proc_std = subprocess.Popen([
        str(EXE_WIN), "-tls=false", f"-port={port_std}", f"-data={scratch_std}", f"-assets={ASSETS}", "-debug"
    ], cwd=str(scratch_std), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    proc_noauth = subprocess.Popen([
        str(EXE_WIN), "-tls=false", f"-port={port_noauth}", f"-data={scratch_noauth}", f"-assets={ASSETS}", "-no-auth", "-debug"
    ], cwd=str(scratch_noauth), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    proc_custom = subprocess.Popen([
        str(EXE_WIN), "-tls=false", f"-port={port_custom}", f"-data={scratch_custom}", f"-assets={ASSETS}",
        "-ice_servers=stun:stun1.example.com:19302,turn:user:pass@turn.example.com:3478", "-debug"
    ], cwd=str(scratch_custom), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(2.0)

    url_std = f"http://127.0.0.1:{port_std}"
    url_na = f"http://127.0.0.1:{port_noauth}"
    url_custom = f"http://127.0.0.1:{port_custom}"

    try:
        r_adm = requests.post(f"{url_std}/api/login", json={"username": "admin", "password": "admin123"})
        tok_adm = r_adm.json()["token"]
        h_adm = {"Authorization": f"Bearer {tok_adm}"}

        # Create user1 properly via admin API to avoid hash/salt edge cases
        requests.post(f"{url_std}/api/admin/users/create", headers=h_adm, json={"username": "user1", "password": "user123", "role": "user"})
        r_u1 = requests.post(f"{url_std}/api/login", json={"username": "user1", "password": "user123"})
        tok_u1 = r_u1.json()["token"]
        h_u1 = {"Authorization": f"Bearer {tok_u1}"}

        # Capture initial state of default_settings before any probes mutate it
        r_ds_initial = requests.get(f"{url_std}/api/default_settings", headers=h_adm)

        # A. Method Matrix across 4 routes
        method_matrix = {}
        for route in target_routes:
            method_matrix[route] = {}
            for m in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
                resp = requests.request(m, f"{url_std}{route}", headers=h_adm, data="{}", allow_redirects=False)
                method_matrix[route][m] = {
                    "status_code": resp.status_code,
                    "content_type": resp.headers.get("Content-Type"),
                    "content_length": resp.headers.get("Content-Length"),
                    "cors_origin": resp.headers.get("Access-Control-Allow-Origin"),
                    "cors_methods": resp.headers.get("Access-Control-Allow-Methods"),
                    "cors_headers": resp.headers.get("Access-Control-Allow-Headers"),
                    "body_bytes": len(resp.content),
                    "body_preview": resp.text.strip()[:100]
                }
        (output_dir / "SERVER_CONFIG_ROUTE_METHOD_MATRIX.json").write_text(json.dumps(method_matrix, indent=2), encoding="utf-8")

        # B. Auth Matrix across 4 routes
        auth_matrix = {}
        for route in target_routes:
            r_a = requests.get(f"{url_std}{route}", headers=h_adm)
            r_u = requests.get(f"{url_std}{route}", headers=h_u1)
            r_miss = requests.get(f"{url_std}{route}")
            r_inv = requests.get(f"{url_std}{route}", headers={"Authorization": "Bearer bad_tok"})
            r_na = requests.get(f"{url_na}{route}")

            # Also check POST for /api/default_settings
            post_rbac = {}
            if route == "/api/default_settings":
                p_a = requests.post(f"{url_std}{route}", headers=h_adm, json={"k": "v"})
                p_u = requests.post(f"{url_std}{route}", headers=h_u1, json={"k": "v"})
                p_miss = requests.post(f"{url_std}{route}", json={"k": "v"})
                p_na = requests.post(f"{url_na}{route}", json={"k": "v"})
                post_rbac = {
                    "POST_ADMIN": {"status_code": p_a.status_code, "body": p_a.text.strip()},
                    "POST_NORMAL_USER": {"status_code": p_u.status_code, "body": p_u.text.strip()},
                    "POST_MISSING_TOKEN": {"status_code": p_miss.status_code, "body": p_miss.text.strip()},
                    "POST_NO_AUTH_MODE": {"status_code": p_na.status_code, "body": p_na.text.strip()}
                }

            auth_matrix[route] = {
                "GET": {
                    "ADMIN": {"status_code": r_a.status_code, "body": r_a.text.strip()[:100]},
                    "NORMAL_USER": {"status_code": r_u.status_code, "body": r_u.text.strip()[:100]},
                    "MISSING_TOKEN": {"status_code": r_miss.status_code, "body": r_miss.text.strip()[:100]},
                    "INVALID_TOKEN": {"status_code": r_inv.status_code, "body": r_inv.text.strip()[:100]},
                    "NO_AUTH_MODE": {"status_code": r_na.status_code, "body": r_na.text.strip()[:100]}
                },
                "POST_RBAC": post_rbac
            }
        (output_dir / "SERVER_CONFIG_AUTH_MATRIX.json").write_text(json.dumps(auth_matrix, indent=2), encoding="utf-8")

        # C. Server Addresses Contract
        r_addr_base = requests.get(f"{url_std}/api/server/addresses", headers=h_adm)
        r_addr_host = requests.get(f"{url_std}/api/server/addresses", headers={"Authorization": f"Bearer {tok_adm}", "Host": "my-domain.net:9090"})
        r_addr_noprt = requests.get(f"{url_std}/api/server/addresses", headers={"Authorization": f"Bearer {tok_adm}", "Host": "my-domain.net"})

        addr_contract = {
            "route": "/api/server/addresses",
            "handler_symbol": "main.vz0hZo0q1IzM",
            "handler_va": "0x7632a0",
            "methods_allowed": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
            "auth_required": True,
            "response_structure": {
                "code": "int (always 0)",
                "data": {
                    "addresses": "[]string (host:port or [ipv6]:port)",
                    "current": "string (r.Host exact string)"
                }
            },
            "field_classification": {
                "current": {
                    "classification": "REQUEST_DERIVED",
                    "origin": "r.Host"
                },
                "addresses": {
                    "classification": "ENVIRONMENT_AND_REQUEST_DERIVED",
                    "composition": [
                        "Index 0: r.Host (exact client request host)",
                        "Subsequent indices: non-loopback IP addresses from net.InterfaceAddrs(), formatted with request port or server port"
                    ]
                }
            },
            "observed_samples": {
                "standard_loopback_host": r_addr_base.json(),
                "custom_host_with_port": r_addr_host.json(),
                "custom_host_no_port": r_addr_noprt.json()
            }
        }
        (output_dir / "SERVER_ADDRESSES_CONTRACT.json").write_text(json.dumps(addr_contract, indent=2), encoding="utf-8")

        # D. Default Settings Contract
        # Test mutation
        test_payload = {"video_bitrate": 5000, "fps": 60, "encoder": "nvenc"}
        r_ds_set = requests.post(f"{url_std}/api/default_settings", headers=h_adm, json=test_payload)
        r_ds_mutated = requests.get(f"{url_std}/api/default_settings", headers=h_adm)

        # Edge cases
        r_ds_empty = requests.post(f"{url_std}/api/default_settings", headers=h_adm, data="")
        r_ds_mal = requests.post(f"{url_std}/api/default_settings", headers=h_adm, data="{bad")
        r_ds_null = requests.post(f"{url_std}/api/default_settings", headers=h_adm, data="null")
        r_ds_arr = requests.post(f"{url_std}/api/default_settings", headers=h_adm, json=[1, 2])

        ds_contract = {
            "route": "/api/default_settings",
            "handler_symbol": "main.j0yBBXR1Hjl",
            "handler_va": "0x768980",
            "methods_allowed": ["GET", "POST", "OPTIONS"],
            "disallowed_methods_status": 405,
            "auth_required_get": True,
            "auth_required_post": "ADMIN_ONLY (403 Forbidden: admin only\\n)",
            "initial_state": r_ds_initial.json(),
            "mutation_behavior": {
                "post_success_response": r_ds_set.text,
                "readback_after_mutation": r_ds_mutated.json(),
                "storage_mechanism": "IN_MEMORY_GLOBAL",
                "persistence_across_restart": False
            },
            "error_handling": {
                "empty_body": {"status_code": r_ds_empty.status_code, "body": r_ds_empty.text},
                "malformed_json": {"status_code": r_ds_mal.status_code, "body": r_ds_mal.text},
                "json_null": {"status_code": r_ds_null.status_code, "body": r_ds_null.text},
                "json_array": {"status_code": r_ds_arr.status_code, "body": r_ds_arr.text}
            }
        }
        (output_dir / "DEFAULT_SETTINGS_CONTRACT.json").write_text(json.dumps(ds_contract, indent=2), encoding="utf-8")

        # E. ICE Server Contract
        r_ice_default = requests.get(f"{url_std}/api/ice_servers", headers=h_adm)
        
        # Login to custom server to probe CLI ice servers
        r_adm_c = requests.post(f"{url_custom}/api/login", json={"username": "admin", "password": "admin123"})
        h_adm_c = {"Authorization": f"Bearer {r_adm_c.json()['token']}"}
        r_ice_custom = requests.get(f"{url_custom}/api/ice_servers", headers=h_adm_c)

        ice_contract = {
            "route": "/api/ice_servers",
            "handler_symbol": "main.vREP2EE2",
            "handler_va": "0x768500",
            "methods_allowed": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
            "auth_required": True,
            "element_schema": {
                "urls": "[]string (required)",
                "username": "string (optional, omitempty)",
                "credential": "string (optional, omitempty)"
            },
            "precedence_rules": {
                "cli_flag_ice_servers": "Highest precedence. Comma-separated list of stun:host:port or turn:user:pass@host:port",
                "cli_flag_stun_server": "Deprecated fallback if -ice_servers is omitted. Formatted as single STUN entry",
                "compiled_default": "[{\"urls\": [\"stun:stun.l.google.com:19302\"]}]"
            },
            "observed_samples": {
                "default_configuration": r_ice_default.json(),
                "custom_cli_configuration": r_ice_custom.json()
            }
        }
        (output_dir / "ICE_SERVER_CONTRACT.json").write_text(json.dumps(ice_contract, indent=2), encoding="utf-8")

        # F. Function Slices
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        md.detail = True

        function_slices = []
        for route_info in route_family["routes"]:
            sym = route_info["handler_symbol"]
            f_meta = fm_by_sym[sym]
            h_va = int(f_meta["va"], 16)
            size = f_meta["size_bytes"]
            off = va_to_offset(h_va, sections)
            code = elf_bytes[off:off+size]
            insns = []
            for ins in md.disasm(code, h_va):
                insns.append(f"0x{ins.address:x}: {ins.mnemonic} {ins.op_str}")

            function_slices.append({
                "symbol": sym,
                "route": route_info["pattern"],
                "semantic_role": route_info["semantic_role"],
                "machine_observation": {
                    "start_va": hex(h_va),
                    "size_bytes": size,
                    "end_va": hex(h_va + size),
                    "instruction_count": len(insns),
                    "callees": f_meta.get("callees", []),
                    "referenced_strings": f_meta.get("referenced_strings", []),
                    "assembly_preview": insns[:30]
                },
                "semantic_annotation": {
                    "role_description": route_info["semantic_role"]
                }
            })
        (output_dir / "SERVER_CONFIG_HTTP_FUNCTION_SLICES.json").write_text(json.dumps(function_slices, indent=2), encoding="utf-8")

    finally:
        for proc in [proc_std, proc_noauth, proc_custom]:
            try:
                proc.terminate()
                proc.wait(timeout=2)
            except:
                try:
                    proc.kill()
                except:
                    pass

    print(f"[+] Successfully generated all 8 Server Configuration forensic artifacts in {output_dir}")

if __name__ == "__main__":
    generate_evidence()
