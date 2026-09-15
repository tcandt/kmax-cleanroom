# Forensic Report 02: WebRTC Signaling Server Reverse Engineering (Phase 1B)

## 1. Scope & Execution Parameters
- **Primary Binary Analyzed**: `cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling` (ELF 64-bit x86-64, size 8,417,428 bytes, SHA256: `b18d203df8fb2bf7...`)
- **Corroborating Target**: `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe` (PE32+ x86-64, size 8,676,352 bytes, SHA256: `45b95baefd824d55...`)
- **Obfuscation Technology**: Built with `garble` (Go symbol & package obfuscator). Identifier names scrambled to pseudo-random strings; `pclntab` intact (`0x2d42f0` bytes); string table plaintext in `.rodata`.
- **Clean-Room Verification**: 100% compliant with `RULES.md` (zero external reference, zero clean architecture guessed).

## 2. Quantitative Metrics
| Metric | Value | Forensic Significance |
|---|---|---|
| **Total Functions Detected** | **7,571** | Complete function bounds in `.gopclntab` |
| **Functions with pclntab Entries** | **7,571 (100.00%)** | Zero unmapped function entries |
| **Readable Runtime / Stdlib Functions** | **4,218** | `runtime.*`, `net/http.*`, `crypto/*`, `syscall.*` |
| **Garbled Project & Library Functions** | **3,353** | Application logic scrambled by `garble` |
| **HTTP / WebSocket Routes Recovered** | **46** | Validated endpoints across all subsystems |
| **JSON Schema Keys Recovered** | **81** | Parameters for auth, device, share, & signaling |
| **Environment Variables Recovered** | **14** | Validated against Docker Compose & `.rodata` |
| **Functions with String Xrefs** | **804** | Direct LEA x86_64 pointer matches into `.rodata` |
| **Functions with Direct Callgraph Edges** | **6,588** | Extracted direct `E8` CALL relationships |
| **High / Medium Confidence Inferred Roles** | **4,218 (High) + 124 (Project Medium/High)** | Provable through string xrefs and route handlers |
| **Unknown Project Functions** | **3,229** | Reserved for Phase 2 deep decompilation |

## 3. Cross-Architecture Corroboration (Windows vs Linux)
Cross-referencing the Linux ELF binary against the Windows PE executable proved:
1. **Endpoint Identity**: 100% of all 46 HTTP and WebSocket routes exist byte-for-byte in both binaries.
2. **Persistence Schema**: Both use `shares.json` for persistent device sharing tokens and access grants.
3. **Pclntab Equivalence**: Both binaries share identical runtime function structures and Pion WebRTC dependencies.
4. **Symbol Discrepancy Note**: Garbled symbol names differ between Linux and Windows builds (confirming that `garble` uses randomized seeds per build). Reconstructed code must map to behavioral and protocol roles rather than build-specific garbled names.

## 4. Recovered Protocol & System Architecture
1. **Authentication Flow**:
   - `/api/login`: Accepts `username` and `password`, returns JWT session `token`.
   - `/api/auth-status`: Validates token claims.
   - `/api/logout`: Revokes token.
2. **Signaling Dual-Channel Architecture**:
   - `/register_agent`: Dedicated WebSocket endpoint for Android agent daemons. Agents send device registration, screen geometry, camera status, and listen for WebRTC offer requests.
   - `/connect_client`: WebSocket endpoint for web browsers. Relays SDP offer/answer and ICE candidate trickles between browser and agent.
3. **Commercial & Entitlement Subsystem**:
   - `/api/activate`: License activation. Reads `LicenseClaims`, enforcing `ForbidBitrate`, `ForbidAudio`, and `ExpireSeconds`.
4. **Device Management & Sharing Subsystem**:
   - `/api/devices`: Returns device inventory, online statuses, and stream URLs.
   - `/api/share/*`: Manages guest access with fine-grained controls (`min_bitrate`, `max_bitrate`, expiration timestamps).
