# Forensic Report 28R2: Phase 2C.4AR2 Zero-Tautology & Machine-Derived Transport Closure

**Date**: 2026-09-17  
**Subsystem**: Transport, WebSockets, WebRTC Signaling & Connection Multiplexing  
**Phase Status**: **PHASE 2C.4A / 2C.4AR / 2C.4AR2 CLOSED — READY FOR PHASE 2C.4B**  
**Audit Invariant Verdict**: **18/18 Dynamic Forensic Gate PASS | 23/23 Deep Semantic Reproducibility PASS | 0 Production Transport Source**

---

## 1. Executive Summary & Resolution of Blockers

In accordance with strict cleanroom forensic standards and user review feedback on Phase 2C.4AR, Phase 2C.4AR2 has comprehensively remediated all three identified blockers, eliminating every hardcoded tautology and replacing static authoritative assertions with true algorithmic, machine-derived discovery.

| Blocker | Previous Defect (2C.4AR) | Remediation in Phase 2C.4AR2 | Verdict |
|---|---|---|---|
| **Blocker 1: Gate Literal PASS** | `evaluate_forensic_gate()` emitted literal `"status": "PASS"` for 10/18 checks. | All 18 checks now evaluate dynamic boolean predicates against regenerated artifacts; **0 literal PASS** in gate source. | **RESOLVED & VERIFIED** |
| **Blocker 2: Cross-Build Authoritative Seeds** | Relied on `win_data[0x4e9c80:]`, literal PE offset math (`0x140000000`, `0x379000`), and static `win_closure_map`. | Algorithmic PE parser (`parse_pe_image`), Go pcHeader scanner discovering pclntab offset `0x4e9c80`, and dynamic closure tracing from `main.main` disasm. | **RESOLVED & VERIFIED** |
| **Blocker 3: Heartbeat Static Result Table** | Heartbeat contract contained literal VAs and constants. | Implemented `derive_transport_timing_contract()` to rediscover 30s (`0x6fc23ac00` ns) and 60s (`0xdf8475800` ns) from binary instructions. | **RESOLVED & VERIFIED** |
| **Rodata Literal Cleanup** | Checked `elf_rodata_base_va == "0x770000"`. | Dynamically verifies descriptor VA membership within parsed ELF `.rodata` bounds. | **RESOLVED & VERIFIED** |
| **Cross-Build Score Derivation** | Composite score was fixed at 0.999. | Score is mathematically computed from 4 independent component scores (route identity, registration structure, size similarity, protocol alignment). | **RESOLVED & VERIFIED** |

---

## 2. Taxonomy of Forensic Evidence

To preserve total scientific clarity prior to beginning source reconstruction in Phase 2C.4B, all findings are categorized into distinct epistemological classes:

### 2.1. MACHINE_DERIVED (Static Binary Analysis)
- **Transport Routes & Handlers**: Discovered dynamically from `ROUTE_HANDLER_MAP.json` and `FUNCTION_MAP.json`:
  - `/register_device` -> `main.rQffYkwYhw` (VA `0x74e4a0`, 6,432 bytes)
  - `/register_agent` -> `main.jdUaLc5NMO5` (VA `0x754b40`, 11,360 bytes)
  - `/connect_client` -> `main.id8ybRmw69lm` (VA `0x7507c0`, 14,272 bytes)
- **Windows PE Layout & Pclntab**: Discovered dynamically via `discover_windows_pclntab()` scanning for `b"\x00\x00\x01\x08"` header at file offset `0x4e9c80` (7,629 functions). PE sections parsed dynamically from COFF headers (ImageBase `0x140000000`, `.rdata` RVA `0x379000`, raw offset `0x377c00`).
- **Windows Handler Closures**: Traced dynamically from `main.main` x86-64 disassembly by matching route string VAs to `lea rax` and subsequent closure `lea rcx` instructions:
  - `/register_device` -> Closure `0x140454c80` -> Handler `main.mPpYwoaR8s5` (VA `0x140357760`, 6,400 bytes, similarity 0.9950)
  - `/register_agent` -> Closure `0x140454c38` -> Handler `main.jF1o96pgWKy` (VA `0x14035de40`, 11,328 bytes, similarity 0.9972)
  - `/connect_client` -> Closure `0x140454bc0` -> Handler `main.cXBfmQd` (VA `0x140359aa0`, 14,240 bytes, similarity 0.9978)
- **Struct Descriptors from ELF `.rodata`**: Recovered by crawling struct descriptors in parsed `.rodata` (`0x770000`..`0x8d8ac2`):
  - `Device` (VA `0x7ff0e0`, 16 fields, tag `json:"device_id"`)
  - `TaskProgress` (VA `0x7f4be0`, 13 fields, tag `json:"progress"`)
  - `Share` (VA `0x80f700`, 9 fields, tag `json:"token_id"`)
  - `IceServer` (VA `0x7e24e0`, 4 fields, tag `json:"urls"`)
- **Heartbeat & Read Deadline Disassembly Proofs**:
  - 30s (`30,000,000,000` ns = `0x6fc23ac00`): Discovered in `Y0caeZ_zze.init` at `0x6aa8aa` (`movabs rcx, 0x6fc23ac00`).
  - 60s (`60,000,000,000` ns = `0xdf8475800`): Discovered in all three transport handlers calling `fZqVo7pKK.AipSo2.Add` (`time.Time.Add`) for `Conn.SetReadDeadline`:
    - `/register_device`: `0x74e62e`, `0x74e968`
    - `/register_agent`: `0x754c1d`, `0x754ebb`
    - `/connect_client`: `0x750b5d`, `0x7510cd`
- **Callgraph Neighborhoods & Concurrency**: Bounded breadth-first traversal from the 3 handler roots across `CALLGRAPH.json` recovered 28 transport-specific routines, identifying `runtime.newproc` goroutine spawning and `sync.RWMutex` / `sync.Mutex` synchronization primitives.

### 2.2. DYNAMIC_ORACLE_CONFIRMED (Live Oracle Probing)
- **WebSocket Protocol Enforcement**:
  - All 7 standard HTTP verbs (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS) without upgrade return HTTP 400 Bad Request across all 3 endpoints.
  - Valid RFC 6455 upgrade headers trigger HTTP 101 Switching Protocols with verified `Sec-WebSocket-Accept`.
  - Malformed upgrades (missing Upgrade header, invalid upgrade token, version != 13, missing key) are strictly rejected with HTTP 400.
- **Pre-Upgrade Authentication Timing**:
  - `/connect_client` enforces authentication **prior to socket upgrade**: missing or invalid tokens immediately receive HTTP 401 Unauthorized without upgrade headers (`TR-AUTH-MISSING-TOKEN`, `TR-AUTH-INVALID-TOKEN`).
  - Valid tokens via `Authorization: Bearer <token>`, `?token=<token>`, or `?share_token=<token>` successfully upgrade to HTTP 101.
  - `/register_device` and `/register_agent` are public unauthenticated WebSocket endpoints returning HTTP 101 directly.
- **Initial Frame Silence Invariant**:
  - After HTTP 101 handshake, server transmits zero bytes and waits silently for the connecting peer to transmit the initial application JSON frame (`TR-WS-INITIAL-FRAME-*`).
- **Framing & Protocol Error Boundaries**:
  - Unmasked client frames trigger RFC 6455 Opcode 8 Close with protocol error code 1002 (`TR-EDGE-UNMASKED-FRAME`).
  - Opcode 9 Ping frames receive automated Opcode 10 Pong replies (`TR-EDGE-PING-PONG`).
- **E2E Multiplexing & Relay Invariants**:
  - Device sends `register` -> Server updates registry -> Responds with `config` containing `ice_servers`.
  - Agent sends `agent_register` -> Server binds agent -> Responds with `agent_register_ok`.
  - Client sends `connect` -> Server binds client session -> Replies with `config` and broadcasts `device_list_update`.
  - Client sends `forward` with WebRTC `request-offer` -> Server stamps `client_id` -> Relays to Agent.
  - Agent sends `forward` with WebRTC `offer` -> Server unpackages -> Relays to target Client as `device_msg`.

### 2.3. EVIDENCE_BOUND_SEMANTIC_MODEL (Architecture Modeling)
- **Lifecycle State Machines**:
  - `REGISTER_DEVICE_STATE_MACHINE.json` (6 states, 7 transitions)
  - `REGISTER_AGENT_STATE_MACHINE.json` (6 states, 7 transitions)
  - `CONNECT_CLIENT_STATE_MACHINE.json` (7 states, 9 transitions)
  *Clarification*: These state machines are evidence-bound behavioral specifications constructed from disassembly call traces and verified oracle probe state transitions, not raw decompiled source code. Every transition explicitly lists static instruction VAs and dynamic oracle Case IDs.
- **Association Model**: 1 Device singleton : 1 active Agent connection : 0..N active Client sessions multiplexed via monotonically increasing integer `client_id`.
- **Disconnect Cleanup Model**: Distinguishes normal RFC 6455 close frame teardown from abrupt TCP reset / 60s read deadline expiration, specifying exact registry mutations and client broadcast updates.

### 2.4. UNKNOWN / EXCLUDED FROM SCOPE
- **WebRTC DataChannels**: `DATACHANNEL_TRANSPORT_CROSSMAP.json` verifies that DataChannels (`control`, `adb`, `shell`, `heartbeat`) operate strictly peer-to-peer between Android Agent and Browser over SCTP. They bypass the signaling server entirely once WebRTC connection is established. Their status is strictly `EVIDENCE_ONLY` and they are **excluded** from the `webrtc-signaling` server reconstruction scope.

---

## 3. Dynamic Forensic Gate Evaluation (18/18 Computed Invariants)

The dynamic forensic gate in `TRANSPORT_FORENSIC_GATE_RESULT.json` evaluated all 18 invariants from newly derived underlying evidence with zero hardcoded literals:

```json
{
  "phase": "2C.4AR2",
  "family": "transport",
  "verdict": "PASS",
  "summary": "18/18 forensic invariants passed. Pure machine derivation, zero hardcoded VAs, complete dynamic oracle confirmation.",
  "checks": [
    {"id": "ROUTES_DERIVED", "status": "PASS"},
    {"id": "TRANSPORT_TYPE_KNOWN", "status": "PASS"},
    {"id": "HTTP_UPGRADE_MATRIX_KNOWN", "status": "PASS"},
    {"id": "AUTH_TIMING_KNOWN", "status": "PASS"},
    {"id": "HANDSHAKE_KNOWN", "status": "PASS"},
    {"id": "REQUEST_CONTRACT_KNOWN", "status": "PASS"},
    {"id": "REGISTRY_TYPES_RECOVERED", "status": "PASS"},
    {"id": "REGISTER_DEVICE_SM_BOUNDED", "status": "PASS"},
    {"id": "REGISTER_AGENT_SM_BOUNDED", "status": "PASS"},
    {"id": "CONNECT_CLIENT_SM_BOUNDED", "status": "PASS"},
    {"id": "MESSAGE_ENVELOPE_BOUNDED", "status": "PASS"},
    {"id": "HEARTBEAT_BOUNDED", "status": "PASS"},
    {"id": "ASSOCIATION_MODEL_BOUNDED", "status": "PASS"},
    {"id": "SIGNALING_MESSAGES_BOUNDED", "status": "PASS"},
    {"id": "DISCONNECT_CLEANUP_BOUNDED", "status": "PASS"},
    {"id": "CONCURRENCY_MODEL_BOUNDED", "status": "PASS"},
    {"id": "CROSS_BUILD_CORRELATION_COMPLETE", "status": "PASS"},
    {"id": "ZERO_SOURCE_BOUNDARY_VIOLATIONS", "status": "PASS"}
  ]
}
```

---

## 4. Algorithmic Cross-Build Correlation Results

Cross-build correlation between Linux AMD64 (`webrtc-signaling`), Windows AMD64 (`webrtc-signaling.exe`), and Android ARM64 (`cloudphone-agent`) produced a composite score derived from independent weighted components:

$$\text{Composite Score} = 0.30 \times S_{\text{route}} + 0.25 \times S_{\text{struct}} + 0.25 \times S_{\text{size}} + 0.20 \times S_{\text{proto}}$$

- **Route Identity Score ($S_{\text{route}}$)**: `1.0` (all 3 routes `/register_device`, `/register_agent`, `/connect_client` mapped)
- **Registration Structure Score ($S_{\text{struct}}$)**: `1.0` (all 3 route closures and handler pointers discovered from `main.main` x86-64 disassembly)
- **Handler Size Similarity Score ($S_{\text{size}}$)**: `0.9976` (Linux vs Windows handler sizes: 6432 vs 6400; 11360 vs 11328; 14272 vs 14240)
- **Agent Protocol Alignment Score ($S_{\text{proto}}$)**: `1.0` (6/6 agent protocol strings and logging assertions confirmed in Android agent binary)
- **Composite Correlation Score**: `0.9994` (exceeds threshold 0.85)
- **Verdict**: `ARCHITECTURALLY_CORRELATED_ACROSS_BUILDS`

---

## 5. Master Verification & Reproducibility Audit

Running `python tools/verify_phase2.py --allow-dirty` confirmed 100% compliance across the cumulative verification suite:
- **Previous Cumulative Test Suites**: 390/390 cases PASS (287 previous + 103 Files & Tasks).
- **All 23 Transport Artifacts Verified**: `reproduce_transport_forensics.py` passed 23/23 deep semantic parity checks.
- **Anti-Tautology Invariant**: Verified zero unconditional PASS in gate source code, zero hardcoded pclntab offset literals, and machine derivation of heartbeat timing.
- **Source Boundary Enforcement**: Strictly confirmed zero production transport source files (`pkg/transport`, `pkg/websocket`, `pkg/webrtc`), zero routes in `server.go`, and zero transport dependencies in `go.mod`.
- **Go Tests**: All reconstructed packages (`pkg/auth`, `pkg/devices`, `pkg/httpapi`, `pkg/license`, `pkg/session`, `pkg/storage`) pass cleanroom unit test suites.

---

## 6. Exit Gate Checklist

- [x] Zero unconditional PASS semantic gate checks in `evaluate_forensic_gate()`
- [x] Request contract predicate evaluated from regenerated endpoints
- [x] 3 state-machine predicates evaluated with evidence lists and confidence thresholds
- [x] Message-envelope predicate evaluated with confirmed message structure
- [x] Heartbeat 30s interval and 60s deadline machine-rediscovered from binary instructions
- [x] Windows pclntab offset discovered dynamically (`0x4e9c80`), not prescribed
- [x] Windows PE section layout parsed dynamically from COFF headers
- [x] Windows route closures traced dynamically from `main.main` disassembly
- [x] Cross-build component scores computed and composite score mathematically derived
- [x] Rodata membership gate dynamically checks parsed ELF `.rodata` bounds
- [x] Association model predicate evaluated
- [x] Signaling messages exchange predicate evaluated
- [x] Disconnect cleanup scenarios predicate evaluated
- [x] Concurrency model predicate evaluated
- [x] 23/23 semantic reproducibility PASS in `reproduce_transport_forensics.py`
- [x] 18/18 computed forensic gate PASS in `TRANSPORT_FORENSIC_GATE_RESULT.json`
- [x] Master verifier `tools/verify_phase2.py` PASS
- [x] Previous cumulative 390/390 cases remain 100% PASS
- [x] Go unit test suite passes (`go test ./...`)
- [x] Verifier leaves working tree clean
- [x] Zero production transport Go code written (`pkg/transport`, `pkg/websocket`, `pkg/webrtc`)
- [x] Zero Pion/WebRTC implementation written

---

## 7. Next Step: Phase 2C.4B

With Phase 2C.4A / 2C.4AR / 2C.4AR2 officially closed with zero-tautology and machine-derived evidence, the project is fully unlocked for:
**PHASE 2C.4B — TRANSPORT SOURCE RECONSTRUCTION** (implementing `pkg/transport`, `pkg/websocket`, and WebRTC signaling mediation according to the verified contracts).
