# Semantic Role Mapping: CloudPhone Agent Daemon

## Forensic Integrity Principles
- **Strict Package Provenance Separation**: Provenance (`STDLIB`, `GO_RUNTIME`, `THIRD_PARTY`, `PROJECT`, `UNKNOWN_PACKAGE`) is kept independent from `semantic_role`.
- **Zero Dependency Role Leakage**: Generic library methods (`String`, `MarshalText`, `ReadFrom`, `AcceptTCPWithConn`, etc.) are never misclassified as application controllers.
- **Multi-Class Evidence Requirement**: `CONFIRMED_ROLE` for application functions strictly requires >= 2 independent evidence classes.
- **Preserved Obfuscated Symbols**: All garbled symbols are preserved verbatim.

### Verified Summary Counts (Arithmetic Invariant Checked)
- **Total Functions Evaluated**: 15398
- **CONFIRMED_ROLE**: 2582
- **INFERRED_ROLE**: 135
- **UNKNOWN**: 12681
- **Sum Verification**: `2582 + 135 + 12681 == 15398` (PASS)

### Package Provenance Distribution
- **GO_RUNTIME**: 1623
- **PROJECT**: 458
- **STDLIB**: 945
- **THIRD_PARTY**: 1454
- **UNKNOWN_PACKAGE**: 10918

### Confirmed Application & Project Roles (>= 2 Independent Evidence Classes)

| VA | Symbol Name | Provenance | Semantic Role | Conf | Evidence Classes |
|---|---|---|---|---|---|
| `0x4aad90` | `IV04EXWpwj.z3qLXTPYDa` | `PROJECT` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy_audio' socket; C: Audio format negotiation logic |
| `0x5163a0` | `main.(*JJffa1S1Zv6)._kTtL83Kr.func3` | `PROJECT` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy_audio' socket; C: Audio format negotiation logic |
| `0x51a5b0` | `main.(*JJffa1S1Zv6).p6Eufk` | `PROJECT` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy_audio' socket; C: Audio format negotiation logic |
| `0x51cc60` | `main.wG6mNWE7EMO` | `PROJECT` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy_audio' socket; C: Audio format negotiation logic |
| `0x51cdb0` | `main.dOpxv5FpG` | `PROJECT` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy_audio' socket; C: Audio format negotiation logic |
| `0x51d120` | `main.main` | `PROJECT` | `AGENT_DAEMON_ENTRYPOINT` | 1.00 | A: Contains CLI flag strings (-signaling, -id, -webrtc_port); B: Program main entrypoint; C: UDS socket initialization loop |
| `0x51f980` | `main.main.func1` | `PROJECT` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy_audio' socket; C: Audio format negotiation logic |
| `0x5277e0` | `main.(*JJffa1S1Zv6).yJhdib9D3` | `PROJECT` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy' video socket; C: 12-byte PTS header packetizer logic |
| `0x52dd20` | `main.(*JJffa1S1Zv6).iDVUAml6wT7` | `PROJECT` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy' video socket; C: 12-byte PTS header packetizer logic |
| `0x531dd0` | `main.(*JJffa1S1Zv6).abCsHT4G3.func1` | `PROJECT` | `SCRCPY_DAEMON_AND_IPC_CONTROLLER` | 0.95 | A: Instruction xref to 'libsys_core.so' companion staging; C: Privilege drop string 'dropping privileges to shell (UID 2000)' |
| `0x535290` | `main.(*JJffa1S1Zv6).jdmbieL5j4J8` | `PROJECT` | `AGENT_WEBRTC_PEERCONNECTION_MANAGER` | 0.95 | A: Instruction xref to '/register_agent' signaling; C: WebRTC peer connection state handling |
| `0x53c730` | `main.(*JJffa1S1Zv6).iIhwd_WXInS` | `PROJECT` | `AUDIO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy_audio' socket; C: Audio format negotiation logic |
| `0x5418a0` | `main.(*JJffa1S1Zv6).cQbtHJ` | `PROJECT` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy' video socket; C: 12-byte PTS header packetizer logic |
| `0x5490a0` | `main.(*JJffa1S1Zv6).xctC9p6wn` | `PROJECT` | `VIDEO_STREAM_INGESTION_AND_PACKETIZER` | 0.95 | A: Instruction xref to '@scrcpy' video socket; C: 12-byte PTS header packetizer logic |

*Total Confirmed Project Roles: 14. Complete mapping in ROLE_MAPPING.json*
