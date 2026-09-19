# Forensic Report 03: CloudPhone Agent Binary Forensics (Phase 1B / Phase 2 Remediation)

## 1. Scope & Execution Parameters
- **Primary Binary Analyzed**: `cloudphone-v0.3.6 (1)/android/cloudphone-agent` (ELF 64-bit AArch64, size 13,828,244 bytes, SHA256: `9cc32ea3cffe29db...`)
- **Corroborating Target**: `cloudphone-agent-magisk-v0.3.6 (1)/binaries/cloudphone-agent-armeabi-v7a` (ELF 32-bit ARM, size 14,155,924 bytes, SHA256: `7ea2249e9c3e5eb5...`)
- **Target OS & Role**: Android Linux device daemon. Orchestrates Scrcpy server, captures hardware screen/audio, and connects to WebRTC signaling.
- **Parser Remediation (Blocker A)**: Validated via `tests/test_pclntab_parser.py` (documented in `reports/02A_PCLNTAB_PARSER_VALIDATION.md`). Structurally parses `functab -> _func -> nameOff` traversal with 100.00% valid symbol names.

## 2. Quantitative Metrics
| Metric | Value | Forensic Significance |
|---|---|---|
| **Total Functions Detected** | **15,398** | Exact function boundaries in `.gopclntab` |
| **Functions with Valid pclntab Entries** | **15,398 (100.00%)** | Zero unmapped or malformed entries |
| **Preserved Runtime / Stdlib Functions** | **2,485** | `runtime.*` (1,425), `reflect.*` (429), `internal/abi.*` (193), `syscall.*` (172), `sync.*` (67), stdlib (199) |
| **Garbled Project & Library Functions** | **12,913** | Obfuscated agent orchestration & Pion WebRTC stack |
| **Functions with Confirmed Roles** | **2,587** | 2,485 stdlib + 102 project functions with direct string xrefs |
| **Garbled Functions Reserved for Decompilation** | **12,811** | Zero guesswork role assignment; kept as UNKNOWN |
| **JSON Schema Keys Recovered** | **169** | Protocol attributes for device, video, and control |
| **Environment Variables & Flags Recovered** | **18** | Configuration flags and fallback defaults |
| **Functions with Exact String Xrefs** | **366** | Exact ADRP + ADD AArch64 pointer matches into `.rodata` |
| **Functions with Direct Callgraph Edges** | **12,737** | Extracted direct `BL` branch relationships |

## 3. Cross-Architecture Corroboration (ARM64 vs ARMv7)
- **Binary Parity**: The ARM64 and ARMv7 binaries implement identical protocol state machines.
- **Identical IPC Strings**: Both contain exact strings for scrcpy-server launch, UDS dial (`[Stream] Dial video UDS error: %v`), privilege dropping (`dropping privileges to shell (UID 2000)`), and hash integrity checking (`INTEGRITY ERROR: libsys_core.so hash mismatch`).
- **Pion WebRTC Stack**: Both embed the Pion WebRTC v3.3.6 engine with dynamic bitrate adaptation and keyframe injection.

## 4. Key Behavioral Discoveries
1. **Scrcpy Helper Lifecycle Orchestration**:
   - The agent copies the companion helper from release assets to `/data/local/tmp/libsys_core.so`.
   - Checks SHA256 integrity to ensure runtime tampering has not occurred.
   - Drops privileges to shell (`UID 2000`) before executing `app_process / com.android.helper.CoreService`.
   - Maintains a watchdog: if an old scrcpy process fails to exit within 2 seconds, it issues a force-kill.
2. **IPC Channel Multiplexing**:
   - Communicates with `libsys_core.so` over abstract UNIX domain sockets (UDS):
     - `@scrcpy`: Video stream (H.264/H.265 NAL units preceded by 12-byte PTS/flag headers)
     - `@scrcpy_audio`: Raw PCM or Opus audio packets
     - `@scrcpy_control`: Binary input control packets (`ControlMessageReader.java`)
     - `@scrcpy_touch`: High-rate touch event injection socket
3. **Dual-Profile Video Engine**:
   - **Low-Profile**: Runs low-bitrate background preview when no active clients are connected.
   - **High-Profile**: Dynamically spins up high-resolution hardware encoding upon active WebRTC client connection.
   - Dynamically throttles encoder bitrate in real time (`scrcpy-server video bitrate to %d bps`).
4. **DataChannel Protocols**:
   - `control`: Receives binary touch events and Unicode clipboard injection (`setClipboard with paste=true`).
   - `group_control_event`: Broadcasts touch/key commands across multiple devices simultaneously.
   - `adb`: Bridges remote web ADB connections directly to local device adbd.
   - `shell`: Interactive remote terminal stream.
   - `heartbeat`: `HEARTBEAT-ACK` latency measurement.
