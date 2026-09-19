# Phase 2C.3G — Server Configuration Forensic & Contract Errata Report (23R)

**Execution Timestamp**: `2026-09-16 08:45:00 UTC`  
**Target Canonical Binary**: `webrtc-signaling` (Linux AMD64 ELF, SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Scope**: Reconciliation between initial prose in Report 22 / Report 23 and canonical machine-derived structured evidence in `evidence/go_signaling/server_config/`.

---

## 1. Executive Summary & Purpose

During rigorous pre-flight review, several prose generalizations in [Report 22](file:///d:/KMAX-CLEANROOM/reports/22_PHASE2C3G_SERVER_CONFIG_FORENSICS.md) and [Report 23](file:///d:/KMAX-CLEANROOM/reports/23_PHASE2C3G_SERVER_CONFIG_RECONSTRUCTION.md) were identified where prose descriptions differed from the canonical structured oracle evidence and Capstone machine derivations.

This errata document records the canonical corrections, reconciles all discrepancies, and establishes the authoritative behavior contracts implemented and verified in the cleanroom codebase.

---

## 2. Itemized Errata & Corrections

### Erratum 1: Route-Specific CORS Headers
- **Report 22 Prose Claim**:
  Section 1 claimed that all 4 handlers write standardized CORS headers:
  `Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE`
  `Access-Control-Allow-Headers: Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization`
- **Canonical Machine Evidence** (`SERVER_CONFIG_ROUTE_METHOD_MATRIX.json`):
  Each handler writes route-specific CORS headers:
  - `/api/server/addresses`:
    - `Access-Control-Allow-Methods`: `GET, OPTIONS`
    - `Access-Control-Allow-Headers`: `Content-Type, Authorization`
  - `/api/ice_servers`:
    - `Access-Control-Allow-Methods`: `GET, OPTIONS`
    - `Access-Control-Allow-Headers`: `Content-Type, Authorization`
  - `/api/version`:
    - `Access-Control-Allow-Methods`: `GET, OPTIONS`
    - `Access-Control-Allow-Headers`: `Content-Type, Authorization`
  - `/api/default_settings`:
    - `Access-Control-Allow-Methods`: `GET, POST, OPTIONS`
    - `Access-Control-Allow-Headers`: `Content-Type, Authorization`
- **Resolution**:
  The cleanroom handlers in [server_config_handlers.go](file:///d:/KMAX-CLEANROOM/reconstructed_source/webrtc-signaling/pkg/httpapi/server_config_handlers.go) strictly adhere to the route-specific CORS headers proven by the oracle method matrix.

---

### Erratum 2: ICE CLI Configuration Parsing & Precedence
- **Prior Assumption / Prose**:
  Assumed symmetric URI parsing for `turn:` and `turns:`, and general URI parsing.
- **Empirical Oracle Evidence** (`ICE_SERVER_CLI_MATRIX.json`):
  Controlled 12-probe dynamic testing against the canonical Go binary oracle proved:
  1. `turn:user:pass@host:port`: The original binary extracts `username` and `credential` and strips `user:pass@` from the URL, yielding `turn:host:port`.
  2. `turns:user:pass@host:port`: The original binary does **not** extract userinfo for `turns:`; it leaves the URL intact with empty credentials.
  3. Empty flag `-ice_servers=`: Falls back to default STUN (`stun:stun.l.google.com:19302`).
  4. Precedence: Specifying `-ice_servers` strictly overrides `-stun_server`, regardless of flag ordering.
  5. Fallback: Specifying only `-stun_server` uses the custom STUN server when `-ice_servers` is omitted.
- **Resolution**:
  Cleanroom parser `ParseICEServers` was bounded strictly to the empirical behavior of the original binary oracle.

---

### Erratum 3: External Address CLI Flag Classification
- **Prior Assumption / Prose**:
  Hypothesized that an `-external-addr` or `-external_addr` flag might mutate `/api/server/addresses`.
- **Empirical Oracle Evidence** (`SERVER_ADDRESSES_CONTRACT.json`):
  1. Probing original binary with `-external-addr` exits with code 1 (`flag provided but not defined: -external-addr`).
  2. Flag table inspection confirms no such flag exists in the signaling server binary.
  3. REST classification: `REST_EFFECT_NONE`.
- **Resolution**:
  Formally classified as `REST_EFFECT_NONE` and marked `DEFERRED_TO_TRANSPORT_PHASE`. The REST endpoint `/api/server/addresses` derives its addresses strictly from `r.Host` and host network interfaces (`net.InterfaceAddrs()`).

---

### Erratum 4: Machine Derivation vs Literal Virtual Address Authorities
- **Report 22 Prose**:
  Cited fixed virtual addresses (`0x7e24e0`, `0x797460`, `0x7bf940`, `0xbeee00/10/20`) as authoritative values.
- **Remediation Invariant**:
  All addresses were converted to `query_seed` / `hypothesis`. The generator [generate_server_config_forensics.py](file:///d:/KMAX-CLEANROOM/tools/forensics/generate_server_config_forensics.py) and reproducer [reproduce_server_config_forensics.py](file:///d:/KMAX-CLEANROOM/tools/forensics/reproduce_server_config_forensics.py) independently derive:
  - ICE Server Struct: Capstone disassembly of `main.vREP2EE2` -> `convTslice` RIP operand -> `KindSlice` (`0x797460`) -> `elem` pointer -> `KindStruct` (`0x7e24e0`).
  - Default Settings Map: Disassembly of `main.j0yBBXR1Hjl` -> `KindMap` LEA operand (`0x7bf940`).
  - Version Globals: Disassembly of `main.ys0CAJV5f5k` -> `.data` RIP operands (`0xbeee00`, `0xbeee10`, `0xbeee20`).
- **Reproducer Status**:
  [reproduce_server_config_forensics.py](file:///d:/KMAX-CLEANROOM/tools/forensics/reproduce_server_config_forensics.py) verifies all 10/10 artifacts with 100% pass rate.

---

## 3. Authoritative Contract Summary

| Endpoint | Methods Allowed | CORS Methods | Auth Required | Storage / Lifecycle |
|---|---|---|---|---|
| `/api/server/addresses` | Permissive (GET/POST/PUT/PATCH/DELETE) | `GET, OPTIONS` | Yes (Admin/User) | Request Host + OS Network Interfaces |
| `/api/default_settings` | Strict GET, POST | `GET, POST, OPTIONS` | GET: Admin/User<br>POST: Admin Only | In-Memory Global (`map[string]interface{}`), Resets on restart |
| `/api/ice_servers` | Permissive (GET/POST/PUT/PATCH/DELETE) | `GET, OPTIONS` | Yes (Admin/User) | Process CLI Flag State (`[]main.Py1TDt`) |
| `/api/version` | Permissive (GET/POST/PUT/PATCH/DELETE) | `GET, OPTIONS` | **No (Public)** | Compile-Time Static Globals (`.data`) |

All differential test suites (`55/55 PASS`) and forensic reproducers (`10/10 PASS`) confirm exact parity with this authoritative matrix.
