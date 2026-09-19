# Forensic Report 11R: Reference Evidence Normalization, Artifact Identity Repair, and Reproducibility Closure

**Audit Milestone**: `PHASE_2R.1_REFERENCE_EVIDENCE_REMEDIATION`  
**Supersedes**: [Report 11](file:///d:/KMAX-CLEANROOM/reports/11_REFERENCE_INTELLIGENCE_CROSSMAP.md)  
**Cleanroom Commit Baseline**: `906b9aff14d25a8743bcef1ce223acd3ece32e47`  
**Reference Sources Snapshot**:
- `tcandt/scrcpyoverwebrtc` (commit: `65567d777bccb11d2a6d93b6acc735478e880b5b`)
- `hqw700/cloudphone-official` (commit: `ceb66b20ad4c6f7b217d38852ea9ec2bd70fcd39`)  
**Audit Status**: VERIFIED, NORMALIZED & CANONICALLY FROZEN  

---

## 1. Executive Summary & Remediation Mandate

Following the review of Phase 2R commit `739812eee33cec484fce70443bb8d4294beb2f0d`, Phase 2C.3B (Devices/Registry REST) was placed on strict **HOLD** to remediate critical evidence layer deficiencies:
1. **Artifact Identity Discrepancy**: `BASELINE.json` previously listed non-canonical hashes. It has now been reconciled with the canonical clean-room originals protected by `tools/verify_phase2.py`.
2. **Canonical vs. Supplemental Agent Distinction**: The primary Android agent (`android/cloudphone-agent`, ARM64) is separated from the supplemental container agent (`agentd/cloudphone-agent-amd64`, x86_64) and distribution aliases.
3. **DataChannel Matrix Framing Correction**: `input-channel` framing was corrected from an unproven binary packet protocol to the JSON string framing (`type: 'touch'` / `type: 'inject_scroll'`) directly observed in reference frontend source. Unproven properties (`ordered`, `binaryType`) on agent-created channels have been downgraded to `UNKNOWN_FROM_FRONTEND`.
4. **Signaling State Machine Timeouts**: Unsupported speculative timeouts (10s, 5s, 15s, 3s) and TCP fallback claims were removed. Timeouts are set to `null` with `timeout_evidence: "NOT_OBSERVED"` except for `executeCommandP2P` (15,000ms).
5. **Granular Evidence Classes**: Coarse `STATIC_BINARY_EVIDENCE` was decomposed into 8 granular binary classes. `BINARY_SEMANTIC_CONFIRMED` now strictly requires `PUBLIC_REFERENCE` + at least 2 independent binary classes.
6. **Committed Tooling & Zero-Diff Reproducibility**: All extraction tools were moved from `scratch/` into `tools/reference/`, read exclusively from immutable local snapshots in `evidence/reference/raw/`, and are verified via `tools/reference/reproduce_reference_evidence.py`.
7. **Mathematically Defined Metrics**: Unsupported aggregate percentages (98.5%, 92.0%, ~45-50%) have been replaced with deterministically measured counts and numerators/denominators.

---

## 2. Canonical Clean-Room Artifact Identity Census

All baseline guarantees and verification tools are anchored against these 3 canonical originals:

| Canonical Path | SHA256 Hash | Size (B) | OS / Arch | Role | Status |
|---|---|---|---|---|---|
| `cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling` | `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3` | 8,417,428 | Linux / AMD64 | Primary Signaling Server (Linux) | `CANONICAL_CLEANROOM_ARTIFACT` |
| `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe` | `374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917` | 8,676,352 | Windows / AMD64 | Primary Signaling Server (Windows) | `CANONICAL_CLEANROOM_ARTIFACT` |
| `cloudphone-v0.3.6 (1)/android/cloudphone-agent` | `9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4` | 13,828,244 | Android / ARM64 | Primary Agent Daemon (Android target) | `CANONICAL_CLEANROOM_ARTIFACT` |

### Supplemental & Distributed Artifacts Audit

| Distributed Path | SHA256 Hash | Size (B) | Architecture | Classification |
|---|---|---|---|---|
| `agentd/cloudphone-agent-arm64` | `9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4` | 13,828,244 | Android / ARM64 | `BYTE_IDENTICAL_ALIAS` |
| `assets/agent/cloudphone-agent-arm64` | `9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4` | 13,828,244 | Android / ARM64 | `BYTE_IDENTICAL_ALIAS` |
| `agentd/cloudphone-agent-amd64` | `15adc2a4c47c4d189d4e8e08e960434bdd55202d74bc3eeee0bf4713a6b8de16` | 14,663,828 | Linux / AMD64 | `SUPPLEMENTAL_DISTRIBUTED_ARTIFACT` |
| `assets/agent/cloudphone-agent-amd64` | `15adc2a4c47c4d189d4e8e08e960434bdd55202d74bc3eeee0bf4713a6b8de16` | 14,663,828 | Linux / AMD64 | `BYTE_IDENTICAL_ALIAS` |
| `agentd/cloudphone-agent-armeabi-v7a` | `936f828fb30df461a2b45d5faa7fe1a50b0e6150cc2eda551c5f74bcefc815e5` | 14,155,924 | Android / ARM32 | `SUPPLEMENTAL_DISTRIBUTED_ARTIFACT` |

Full audit details are documented in [ARTIFACT_IDENTITY_AUDIT.md](file:///d:/KMAX-CLEANROOM/evidence/reference/ARTIFACT_IDENTITY_AUDIT.md) and [ARTIFACT_IDENTITY_AUDIT.json](file:///d:/KMAX-CLEANROOM/evidence/reference/ARTIFACT_IDENTITY_AUDIT.json).

---

## 3. Reference Access Exception & Materialized Snapshots

During Phase 2R, external public reference repositories were read outside `D:\KMAX-CLEANROOM`. This access has been formally classified and audited as `AUTHORIZED_REFERENCE_LANE_EXTERNAL_READ` in [REFERENCE_ACCESS_AUDIT.json](file:///d:/KMAX-CLEANROOM/evidence/reference/REFERENCE_ACCESS_AUDIT.json):
- **Lane A Isolation**: Pure clean-room reconstruction remained strictly isolated. No reference code was copied into `reconstructed_source/`.
- **Decoupling from Mutable Checkouts**: All 12 consumed reference source files have been pinned with Git blob SHA, SHA256 content hashes, line counts, and materialized locally into `evidence/reference/raw/`.
- **Cryptographic Pinned Hashes**: Pinned in [REFERENCE_SOURCE_HASHES.json](file:///d:/KMAX-CLEANROOM/evidence/reference/REFERENCE_SOURCE_HASHES.json). All 12 files verified identical to upstream pinned commits.

---

## 4. Corrected WebRTC DataChannel Protocol Matrix

In [DATACHANNEL_REFERENCE_MATRIX.json](file:///d:/KMAX-CLEANROOM/evidence/reference/DATACHANNEL_REFERENCE_MATRIX.json), every channel attribute is categorized into `REFERENCE_OBSERVED`, `BINARY_CONFIRMED`, `INFERRED`, or `UNKNOWN`:

| Channel Label | Creator Side | Negotiation | Ordered | Binary Type | Framing / Message Schema | Evidence Classification |
|---|---|---|---|---|---|---|
| `input-channel` | Agent | `pc.ondatachannel` | `UNKNOWN` | `UNKNOWN` | JSON string: `touch` (`id`, `seq`, `client_ts_ms`, `action`, `x`, `y`, `w`, `h`), `inject_scroll` (`seq`, `x`, `y`, `w`, `h`, `scroll_h`, `scroll_v`), `inject_text`, `inject_keycode` | `REFERENCE_OBSERVED` (Framing); `UNKNOWN_FROM_FRONTEND` (ordered/binaryType) |
| `clipboard-channel` | Agent | `pc.ondatachannel` | `UNKNOWN` | `UNKNOWN` | JSON string or UTF-8 ArrayBuffer: `{type: 'clipboard', text, source, origin_client_id}` | `REFERENCE_OBSERVED` (Schema); `UNKNOWN_FROM_FRONTEND` (transport) |
| `camera-channel` | Agent | `pc.ondatachannel` | `UNKNOWN` | `UNKNOWN` | JSON control messages: `{action: 'start' \| 'stop'}` + binary frames | `REFERENCE_OBSERVED` (Control); `UNKNOWN_FROM_FRONTEND` (transport) |
| `file-channel` | Browser | `pc.createDataChannel` | `true` | `arraybuffer` | JSON control commands (`file_start`) + binary chunk ArrayBuffers | `REFERENCE_OBSERVED` |
| `ai-command-channel` | Browser | `pc.createDataChannel` | `true` | `arraybuffer` | JSON string: `{request_id, command}` | `REFERENCE_OBSERVED` |
| `adb-channel` | Browser | `pc.createDataChannel` | `true` | `arraybuffer` | Raw ADB transport packets via `channel.send(buf)` | `REFERENCE_OBSERVED` |

*Note*: The prior hypothesis that `input-channel` uses a binary control packet protocol has been explicitly demoted to `INFERRED` / `UNPROVEN_HYPOTHESIS`. The frontend source definitively dispatches `JSON.stringify` strings.

---

## 5. Corrected Client Signaling State Machine

In [CLIENT_SIGNALING_STATE_MACHINE.json](file:///d:/KMAX-CLEANROOM/evidence/reference/CLIENT_SIGNALING_STATE_MACHINE.json), unsupported timeout values and speculative fallback mechanisms have been purged:

| Transition ID | From State | To State | Trigger | Timeout (ms) | Timeout Evidence | Observed Fallback Behavior | Fallback Evidence |
|---|---|---|---|---|---|---|---|
| `T01_CONNECT` | `DISCONNECTED` | `CONNECTING_WS` | `connect()` | `null` | `NOT_OBSERVED` | `null` (Promise reject on onerror) | `NOT_OBSERVED` |
| `T02_WS_OPEN` | `CONNECTING_WS` | `WS_CONNECTED_SIGNALING` | `ws.onopen` | `null` | `NOT_OBSERVED` | `null` | `NOT_OBSERVED` |
| `T03_CONFIG_RECEIVED` | `WS_CONNECTED_SIGNALING` | `WAITING_OFFER` | `config` message | `null` | `NOT_OBSERVED` | `null` | `NOT_OBSERVED` |
| `T04_OFFER_RECEIVED` | `WAITING_OFFER` | `CREATING_ANSWER` | `device_msg: offer` | `null` | `NOT_OBSERVED` | Transition to `ERROR` on SDP exception | `REFERENCE_OBSERVED` |
| `T05_SEND_ANSWER` | `CREATING_ANSWER` | `SENDING_ANSWER_TRICKLE_ICE` | `setLocalDescription` | `null` | `NOT_OBSERVED` | `null` | `NOT_OBSERVED` |
| `T06_ICE_EXCHANGE` | `SENDING_ANSWER_TRICKLE_ICE` | `CONNECTED_P2P` | `pc.connected` | `null` | `NOT_OBSERVED` | Sends `webrtc_failed` message on ICE disconnect | `REFERENCE_OBSERVED` |
| `T07_COMMAND_EXECUTION` | `CONNECTED_P2P` | `CONNECTED_P2P` | `executeCommandP2P()` | **15000** | `REFERENCE_OBSERVED` | Falls back to signaling WS `command` or rejects | `REFERENCE_OBSERVED` |
| `T08_TERMINATION` | `ANY` | `DISCONNECTED` | Disconnect / unload | `null` | `NOT_OBSERVED` | `ws.close()`, `pc.close()`, cleanup | `REFERENCE_OBSERVED` |

*Note*: Automatic fallback to `useWebSocketStream` upon ICE failure was an unsupported assumption. The frontend only dispatches `message_type: 'webrtc_failed'`; switching to WebSocket stream mode requires manual user intervention or application-level reinitialization.

---

## 6. Granular Evidence Classes & Multi-Evidence Crossmap

In [REFERENCE_TO_BINARY_CROSSMAP.json](file:///d:/KMAX-CLEANROOM/evidence/reference/REFERENCE_TO_BINARY_CROSSMAP.json), coarse `STATIC_BINARY_EVIDENCE` has been replaced with granular evidence classes:

$$\text{Classification} = \begin{cases} 
\text{BINARY\_SEMANTIC\_CONFIRMED} & \text{if } \text{PUBLIC\_REFERENCE} + \ge 2 \text{ independent binary classes} \\
\text{REFERENCE\_CORROBORATED} & \text{if } \text{PUBLIC\_REFERENCE} + \ge 1 \text{ binary class} \\
\text{UNCONFIRMED\_HYPOTHESIS} & \text{otherwise}
\end{cases}$$

### Crossmap Inventory Summary

- **Total Mapped Items**: 24 items
- **`BINARY_SEMANTIC_CONFIRMED`**: 23 items (backed by `PUBLIC_REFERENCE` + 2–3 independent binary classes: `ROUTE_REGISTRATION`, `DISASSEMBLY_CONTROL_FLOW`, `DYNAMIC_ORACLE`, `BINARY_STRING`, `BINARY_XREF`)
- **`REFERENCE_CORROBORATED`**: 1 item (`channel: file-channel`, backed by `PUBLIC_REFERENCE` + `BINARY_STRING`)
- **Unconfirmed Items**: 0 items

### Agent CLI Flags Reclassification

In [AGENT_CLI_REFERENCE_MATRIX.json](file:///d:/KMAX-CLEANROOM/evidence/reference/AGENT_CLI_REFERENCE_MATRIX.json), flags are no longer given high confidence based merely on string adjacency:
- **`SEMANTIC_XREF_CONFIRMED` (HIGH Confidence)**: `-id` (env `CP_AGENT_ID`), `-signaling` (dialer xref), `-jar` (app_process xref), `-root` (env `CP_AGENT_ROOT`).
- **`FLAG_REGISTRATION_CONFIRMED` (HIGH Confidence)**: `-external-addr` (Pion NAT address), `-webrtc-port` (Pion port).
- **`STRING_PRESENT` (MEDIUM_INFERRED Confidence)**: `-camera-addr`, `-camera-size`, `-camera-facing`, `-ice-servers`. These 4 flags were discovered solely via `.rodata` string inspection; their semantic roles are inferred from names and context. Both `agentd/cloudphone-agent-amd64` and `android/cloudphone-agent` are explicitly cited.

---

## 7. Mathematically Defined Progress & Coverage Metrics

All aggregate, non-denominated percentages from Report 11 have been replaced with deterministically measured metrics:

| Metric Name | Value | Definition / Denominator | Classification |
|---|---|---|---|
| `SIGNALING_FUNCTION_TABLE_COVERAGE` | **7,571 / 7,571 (100.0%)** | Discovered functions in `webrtc-signaling` pclntab | Deterministic Forensic Metric |
| `AGENT_FUNCTION_TABLE_COVERAGE` | **15,398 / 15,398 (100.0%)** | Discovered functions in `cloudphone-agent` pclntab | Deterministic Forensic Metric |
| `ROUTE_DISCOVERY_COVERAGE` | **43 / 43 (100.0%)** | Runtime routes registered in `main.main` route table | Deterministic Forensic Metric |
| `FRONTEND_ROUTE_BINARY_MATCH` | **35 / 37 (94.6%)** | Reference HTTP routes with exact matches in binary route table | Deterministic Metric |
| `RECONSTRUCTED_ROUTE_COUNT` | **4 / 43 (9.3%)** | Reconstructed routes in `reconstructed_source/` (`/api/login`, `/api/logout`, `/api/auth-status`, `/api/me`) | Deterministic Source Metric |
| `IMPLEMENTED_SURFACE_DIFFERENTIAL_PASS_RATE` | **38 / 38 (100.0%)** | Executed differential tests across Persistence (8/8), Auth Core (12/12), and Auth HTTP (18/18) | Test Pass Rate (NOT Code Coverage) |
| `ESTIMATED_FUNCTIONAL_RECONSTRUCTION_PROGRESS` | **~15–20%** | Estimated progress of total signaling server functionality (Auth & Persistence complete; Devices, Admin, WebSocket signaling, WebRTC negotiation pending) | **ESTIMATE (NOT A FORENSIC COVERAGE METRIC)** |

---

## 8. Committed Reference Tooling & Reproducibility Audit

The reference intelligence pipeline is fully committed in the repository under `tools/reference/`:
- `tools/reference/extract_protocol_index.py`: Extracts endpoints, WS messages, forward payloads.
- `tools/reference/extract_datachannels.py`: Extracts DataChannels with granular evidence classification.
- `tools/reference/extract_signaling_state_machine.py`: Extracts state machine with verified timeouts.
- `tools/reference/extract_agent_cli.py`: Extracts CLI flags with granular evidence levels.
- `tools/reference/build_reference_crossmap.py`: Builds multi-evidence crossmap with strict gating.
- `tools/reference/reproduce_reference_evidence.py`: Master reproducibility verifier; regenerates into temporary directory and performs bit/key exact verification.

Execution of `python tools/reference/reproduce_reference_evidence.py`:
```text
==================================================
PHASE 2R.1 REFERENCE EVIDENCE REPRODUCIBILITY CHECK
==================================================
[PASS] REFERENCE_PROTOCOL_INDEX.json            (Bit/Key Exact Match)
[PASS] DATACHANNEL_REFERENCE_MATRIX.json        (Bit/Key Exact Match)
[PASS] CLIENT_SIGNALING_STATE_MACHINE.json      (Bit/Key Exact Match)
[PASS] AGENT_CLI_REFERENCE_MATRIX.json          (Bit/Key Exact Match)
[PASS] REFERENCE_TO_BINARY_CROSSMAP.json        (Bit/Key Exact Match)
==================================================
REPRODUCIBILITY VERDICT: PASS
==================================================
```

---

## 9. Verification Summary & Strict Exit Gate Status

- **Canonical Artifact Hashes**: All 3 canonical binaries match verified SHA256 hashes.
- **`BASELINE.json` Integrity**: Exact match against `EXPECTED_HASHES`.
- **Reference Content Hashes**: All 12 materialized reference files cryptographically verified.
- **DataChannel Framing**: Corrected to JSON string framing; unproven properties downgraded.
- **State Machine**: Unsupported timeouts and fallbacks removed.
- **Evidence Classes**: Granular binary classes enforced ($\ge 2$ classes for confirmed items).
- **Regression Invariants**: 8/8 persistence differential, 12/12 auth core differential, 18/18 auth HTTP differential, 59/59 provenance checks all **PASS**.
- **Scope Boundary**: Phase 2C.3B Devices/Registry remains strictly unstarted. Zero premature code written.
