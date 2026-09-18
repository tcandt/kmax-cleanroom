# Phase 2C.5B6F Audit Report: WebRTC ADB-Channel Forensic Analysis, Dual-Mode Protocol Recovery & Downstream PTY Boundary

**Status**: FORENSIC BASELINE FROZEN & VERIFIED  
**Phases Covered**: Phase 2C.5B6F-A (Forensic Extraction, Dual-Architecture Disassembly, Proof of Absence of External 127.0.0.1:5555, PTY Downstream Mapping, Formal Historical Errata, and Contract Freeze)  
**Base Remote Commit**: `4b05495d7613084ac9b58b015292f71f27f9c9fb`  
**Step B6F-A Freeze Commit**: To be committed upon audit completion  
**Core Verdict**: **WebRTC `adb-channel` operates an in-process session-sticky dual-mode protocol handler (ADB-compatible 24B packet mode vs bare raw PTY mode) dispatching directly to an in-process PTY shell (`/dev/ptmx` -> `/system/bin/sh` or `/bin/sh`). No external TCP connection to `127.0.0.1:5555` exists. Reconstructed production source code remains strictly inert with zero execution logic.**

---

## 1. Executive Summary & Scope Boundaries

Phase 2C.5B6F achieves exhaustive forensic recovery of the WebRTC `adb-channel` subsystem across both original `cloudphone-agent` binaries (Android ARM64 and Linux AMD64). This phase addresses and supersedes historical assumptions from Phase 2C.5A regarding local ADB daemon bridges.

### 1.1 Strict Tripartite Boundary Taxonomy
In accordance with precision directives, all artifacts, classifications, and code boundaries maintain strict tripartite separation:

1. **ORIGINAL_BINARY_BEHAVIOR**:
   - The original agent implements an in-process protocol handler (`ADB_PACKET_COMPATIBLE_HANDLER` / `DUAL_MODE_PROTOCOL_HANDLER`) inside the `adb-channel` `OnMessage` callback.
   - The first inbound message discriminator evaluates payload length and header command: if `len >= 24` and `cmd == 0x4e584e43` (`CNXN`), it engages ADB packet framing; otherwise, it permanently selects bare raw PTY mode for the session.
   - The downstream execution boundary is an in-process pseudo-terminal (`pty.Open` on `/dev/ptmx` with pipe fallback) running an interactive shell (`/system/bin/sh` on Android ARM64, `/bin/sh` on Linux AMD64), with goroutines pumping stdout/stderr back over the DataChannel via `(*DataChannel).Send`.
2. **DEFERRED_ADB_BRIDGE_BOUNDARY**:
   - All in-process PTY mechanics, shell execution (`/system/bin/sh`, `/bin/sh`), process management, goroutine stream pumps, and ADB packet state machines are formally classified as `DEFERRED_ADB_BRIDGE_BOUNDARY`.
   - They are strictly excluded from clean-room production source code in Phase 2C.5.
3. **CLEAN_ROOM_PARITY_BOUNDARY (Phase 2C.5B6F-A)**:
   - Zero operational ADB daemon connection.
   - Zero TCP dial to `127.0.0.1:5555` or any network socket.
   - Zero PTY allocation or process execution in `reconstructed_source/`.
   - Production WebRTC `adb-channel` remains strictly inert with zero business callbacks attached.
   - Scope in Phase B6F-A is strictly limited to forensics, disassembly manifest, algorithmic derivation, shared validator, negative mutation suite, and formal report.

---

## 2. Machine-Bound Disassembly Evidence & Callgraph Analysis

Disassembly was performed using the canonical LLVM toolchain discovery on the original binaries:
- **ARM64**: `cloudphone-v0.3.6 (1)/android/cloudphone-agent` (SHA256: `9cc32ea3cffe...`)
- **AMD64**: `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-amd64` (SHA256: `15adc2a4c47c...`)

All extracted disassembly blocks are canonically captured in `tools/forensics/adb_channel/adb_channel_disassembly_manifest.json` (`8c170b6b881d...`).

### 2.1 Inbound Channel Dispatch & Label Matching
- **Channel Label**: Exact string `"adb-channel"` (11 bytes / `0xb`).
- **ARM64 Dispatcher**:
  - Located in `main.(*JJffa1S1Zv6).iIhwd_WXInS.func11` at `0x53f300`-`0x53f410`.
  - Label check at `0x53f388`-`0x53f3a0` compares label against `"adb-channel"`.
  - On match, instantiates channel context and registers OnMessage callback `0x516020` (`main.iIhwd_WXInS.func11.2`) via `(*DataChannel).OnMessage` (`0x499770`).
- **AMD64 Dispatcher**:
  - Located in `main.(*IDhLgq).woxaqqFN5Km.func11` at `0x9e3000`-`0x9e3120`.
  - Label check at `0x9e3080`-`0x9e30a0` compares label against `"adb-channel"`.
  - On match, registers OnMessage callback `0x9b3020` (`main.woxaqqFN5Km.func11.2`) via `(*DataChannel).OnMessage` (`0x9244a0`).
- **Lifecycle Scoping**:
  - Exactly one callback is registered: `(*DataChannel).OnMessage`.
  - No branch-specific `OnOpen` or `OnClose` handler was recovered for `adb-channel`.

---

## 3. Exhaustive Proof of Absence of External `127.0.0.1:5555` Bridge

Historical Phase 2C.5A documentation hypothesized that `adb-channel` forwarded raw binary streams to a `"Local ADB daemon / 127.0.0.1:5555 / reverse shell"`. B6F forensic analysis proves this hypothesis false.

### 3.1 Multilayer Absence Proof
1. **Literal & Encoded String Scanning**:
   - Search for ASCII `"127.0.0.1:5555"`, `"127.0.0.1"`, `":5555"`, and `"5555"` yields **zero** matches in the `adb-channel` callgraph or relevant project packages.
   - UTF-8 and split string construction scanning yielded zero occurrences.
2. **Reachable Callgraph Trace**:
   - Every function reachable from `adb-channel` handler (`0x515000`-`0x51a000` on ARM64, 67 direct/indirect calls; `0x9b2000`-`0x9b7000` on AMD64, 62 direct/indirect calls) was audited.
   - **Zero calls** to `net.Dial`, `net.DialTCP`, `net.DialTimeout`, or any standard library networking API exist in the callgraph.
3. **Immediate & Socket Parameter Analysis**:
   - Port 5555 (`0x15b3`) does not appear as an immediate operand in any function in the `adb-channel` dispatch subtree.
   - No sockaddr structures or endpoint addresses are constructed.
4. **Authoritative Verdict**:
   - *"No external TCP ADB-daemon connection path to 127.0.0.1:5555 was recovered from the adb-channel callgraph in either original Agent binary."*

---

## 4. Authentic Downstream Architecture: In-Process PTY & Shell Execution

Instead of proxying to an external TCP socket, the original agent embeds an in-process interactive terminal shell:

### 4.1 Terminal Initialization & PTY Allocation
- **PTY Setup Function**:
  - ARM64: `0x516590`-`0x516640` calls `0x519bf0`.
  - AMD64: `0x9b3590`-`0x9b3640` calls `0x9b6be0`.
- **Window Size**: Defaults to 80 columns x 24 rows (`0x50` cols, `0x18` rows) passed to `pty.Setsize`.
- **PTY Device**:
  - Opens `/dev/ptmx` via `pty.Open()`.
  - Includes fallback to standard `os.Pipe()` pairs (`stdin`, `stdout`, `stderr`) if PTY allocation fails.

### 4.2 Interactive Shell Process Spawning
- **Shell Target**:
  - Android ARM64: executes `/system/bin/sh`.
  - Linux AMD64: executes `/bin/sh`.
- **Stream Redirection & Pump Goroutines**:
  - Connects the PTY slave file descriptor to the child shell process.
  - Spawns a background goroutine to read stdout/stderr from the master PTY descriptor.
  - Slices read from PTY are directly transmitted back to the browser over the DataChannel via `(*DataChannel).Send` (ARM64 `0x49a3d0`, AMD64 `0x9250c0`).
  - Spawns a supervisor goroutine that awaits process exit (`cmd.Wait()`) and closes PTY file descriptors.

---

## 5. Session-Sticky Dual-Mode Protocol Lifecycle

The `adb-channel` handler exhibits dual-mode behavior depending on the client's initial transmission:

```
[Inbound DataChannel Message]
             │
             ▼
     First Message in Session?
      ├── YES ──► Check: len >= 24 AND cmd == 0x4e584e43 ('CNXN')?
      │             ├── MATCH   ──► Set is_bare_pty_mode = false (ADB Packet Mode)
      │             └── NO MATCH ─► Set is_bare_pty_mode = true  (Bare PTY Mode)
      │                                Log: "First packet is not ADB, switching to BARE raw PTY mode"
      └── NO  ──► Dispatch according to persisted session mode state
```

### 5.1 Mode Persistence & Session Stickiness
- The mode flag is stored in the channel session context struct.
- Once decided on the first packet, **the mode is sticky for the lifetime of the WebRTC DataChannel session**.
- Mode switching during an active channel session is not supported.

### 5.2 Mode Characteristics
1. **ADB Packet Mode (`is_bare_pty_mode = false`)**:
   - Parses incoming frames as 24-byte ADB packet headers.
   - Evaluates commands (`CNXN`, `OPEN`, `WRTE`, `OKAY`, `CLSE`).
   - Translates `WRTE` payloads into PTY stdin writes.
   - Encapsulates PTY stdout into outbound ADB `WRTE` packets.
2. **Bare Raw PTY Mode (`is_bare_pty_mode = true`)**:
   - Bypasses packet parsing entirely.
   - Treats incoming bytes directly as raw keyboard/terminal input written to PTY stdin.
   - Directly transmits raw shell output bytes to WebRTC DataChannel via `(*DataChannel).Send`.

---

## 6. 24-Byte ADB Packet Header Layout & State Machine Provenance

For clients operating in ADB Packet Mode, packet framing conforms to the 24-byte little-endian header layout:

### 6.1 Machine-Recovered Field Layout
| Offset | Field Width | Machine Type | Semantic Role (`REFERENCE_BACKGROUND`) | Invariant / Validation |
|---|---|---|---|---|
| `+0` (`0x00`) | 4 bytes | `uint32` LE | `command` | Matches recognized command magic constants |
| `+4` (`0x04`) | 4 bytes | `uint32` LE | `arg0` | First command argument (e.g. remote ID, version) |
| `+8` (`0x08`) | 4 bytes | `uint32` LE | `arg1` | Second command argument (e.g. local ID, maxdata) |
| `+12` (`0x0c`) | 4 bytes | `uint32` LE | `data_length` | Length of attached payload buffer |
| `+16` (`0x10`) | 4 bytes | `uint32` LE | `data_crc32` | Checksum / CRC32 of attached payload |
| `+20` (`0x14`) | 4 bytes | `uint32` LE | `magic` | Checksum: `magic == command ^ 0xFFFFFFFF` |

### 6.2 Command Magic Constants
Recovered directly from disassembly comparison instructions:
- `CNXN` (`0x4e584e43`): Connection handshake (`"CNXN"`)
- `OPEN` (`0x4e45504f`): Open stream service (`"OPEN"`)
- `OKAY` (`0x59414b4f`): Acknowledge / stream ready (`"OKAY"`)
- `WRTE` (`0x45545257`): Write payload stream (`"WRTE"`)
- `CLSE` (`0x45534c43`): Close stream service (`"CLSE"`)

---

## 7. Formal Historical Errata for Phase 2C.5A

In accordance with strict immutability rules, historical artifacts in Phase 2C.5A remain intact. Formal superseding errata are cataloged in `evidence/go_agent/webrtc/ADB_CHANNEL_B6F_CONTRACT_ERRATA.json`:

1. **Correction `ADB-B6F-ERRATA-01`**:
   - **Historical Target**: `DATACHANNEL_FRAMING_MATRIX.json` (`adb-channel.target_downstream`) & `30_PHASE2C5A_WEBRTC_DATACHANNEL_MEDIA_FORENSICS.md` ("Reverse shell / local ADB daemon bridge").
   - **Corrected Finding**: Superseded from `"Local ADB daemon / 127.0.0.1:5555 / reverse shell"` to `"In-process PTY shell (/dev/ptmx -> /system/bin/sh or /bin/sh) with session-sticky dual-mode protocol handler (ADB packet mode vs bare PTY mode). Zero external TCP connection to 127.0.0.1:5555."`
2. **Correction `ADB-B6F-ERRATA-02`**:
   - **Historical Target**: `DATACHANNEL_LABEL_EVIDENCE.json` (`adb-channel.ordered_evidence`).
   - **Corrected Finding**: Inbound `ordered=true` parameter originates solely from client-side WebRTC construction (`pc.createDataChannel('adb-channel', { ordered: true })`) and is classified as `REFERENCE_ONLY`. The agent binary accepts any inbound DataChannel matching label `"adb-channel"` without asserting ordered delivery.

---

## 8. B6F Frozen Artifacts & Canonical Hashes

All 8 B6F forensic artifacts have been algorithmically derived, semantically validated, and frozen:

| Artifact Path | SHA256 Hash | Classification |
|---|---|---|
| `evidence/go_agent/webrtc/ADB_CHANNEL_B6F_PROTOCOL_SPEC.json` | `fc9e91c19d660030212db8d3dc2ddca34d0b6c22624f6ae59fd4482767267303` | PROTOCOL_SPEC |
| `evidence/go_agent/webrtc/ADB_CHANNEL_B6F_TOPOLOGY.json` | `2210779398554f40a4cedc956a19e89cf5592087f8ec2601eced1e00a541d7ee` | TOPOLOGY |
| `evidence/go_agent/webrtc/ADB_CHANNEL_B6F_MESSAGE_FRAMING.json` | `67dec1f8db5a6553893c98e70480a3fbc1f546b8e3f29abf90d3b026738cce18` | MESSAGE_FRAMING |
| `evidence/go_agent/webrtc/ADB_CHANNEL_B6F_CALLGRAPH.json` | `53a22f4e251e18072fb0ebe32d985f11553f3c72130157565c36e439ebeef412` | CALLGRAPH |
| `evidence/go_agent/webrtc/ADB_CHANNEL_B6F_SOURCE_PROVENANCE.json` | `9c8ef88aa6689d42df7cec191e29a22a6dc115ec2411e3cfa31ecbd40e6823fd` | SOURCE_PROVENANCE |
| `evidence/go_agent/webrtc/ADB_CHANNEL_B6F_IMPLEMENTATION_CONTRACT.json` | `1b1aba53ef39786fadafaab772e11c0611198403f8910f951a507ff4b06fc3ea` | IMPLEMENTATION_CONTRACT |
| `evidence/go_agent/webrtc/ADB_CHANNEL_B6F_CONTRACT_ERRATA.json` | `2e7d9b875e52d59d7d08a8ecbb6730eee2965358205a77f4b1a78e83e0ec77e9` | FORMAL_ERRATA |
| `evidence/go_agent/webrtc/adb_channel_disassembly_manifest.json` | `8c170b6b881dbf19709079cd03de677adcc803f366e365d7ac8a72e688caf334` | DISASSEMBLY_MANIFEST |

### Contract Taxonomy Breakdown
- **Total Requirements**: 13 (`ADB-B6F-01` through `ADB-B6F-13`)
- **Original Static Evidence**: 8
- **Reference Background**: 2
- **Safe Scope Guard**: 1
- **Deferred Execution**: 1
- **Audit Provenance Guard**: 1
- **Unknown / Unverified**: 0

---

## 9. Verification & Anti-Tautology Audit Suite

1. **Independent Algorithmic Derivation (`derive_adb_channel_protocol.py`)**:
   - Constructs all 6 semantic artifacts directly from `adb_channel_disassembly_manifest.json` without referencing canonical outputs.
   - Enforced by static output-dependency audit (Case 17).
2. **Forensic Reproducer (`reproduce_adb_channel_forensics.py --check`)**:
   - Validates binary hashes, extracts fresh disassembly into a clean temporary directory, re-derives all artifacts, and asserts exact byte-for-byte SHA256 equivalence against canonical baselines.
3. **Negative Mutation Suite (`test_adb_channel_forensics_negative.py`)**:
   - **19/19 Test Cases PASS**:
     - Cases 1-5: Channel identity, creator side, ordered property, response API, session-sticky lifecycle.
     - Cases 6-8: Packet header length (24B), field alignment, command constant set.
     - Cases 9-11: Downstream classification, 0 reachable `net.Dial`, `DEFERRED_ADB_BRIDGE_BOUNDARY`.
     - Cases 12-14: Terminal boundary, dispatch site VAs, binary send API callsites.
     - Case 15: Taxonomy integrity.
     - Case 16: Anti-tautology tamper rejection.
     - Case 17: Output-dependency guard.
     - Case 18: Errata missing correction rejection.
     - Case 19: Production tree inertness audit.
4. **Master Verifier Integration (`tools/verify_phase2.py`)**:
   - Section 26.1: Frozen contract & taxonomy invariant.
   - Section 26.2: Forensic reproducer & negative mutation invariant.
   - Section 26.3: Dual-architecture evidence & provenance invariant.
   - Section 26.4: Production boundary & channel inertness invariant.

---

## 10. Conclusion & Stop Boundary

Phase 2C.5B6F-A is fully frozen and verified. The forensic truth regarding WebRTC `adb-channel` has been permanently bound to binary evidence:
- Downstream is an in-process PTY shell (`/dev/ptmx` -> `/system/bin/sh` / `/bin/sh`).
- Zero external TCP connection to `127.0.0.1:5555` exists.
- In-process packet processing and PTY execution remain strictly deferred (`DEFERRED_ADB_BRIDGE_BOUNDARY`).
- Clean-room production source code remains completely untouched and 100% inert.

**Execution stops here in accordance with Phase 2C.5B6F-A freeze directives. No runtime ADB parsers, PTY simulators, or bridge connections are implemented.**
