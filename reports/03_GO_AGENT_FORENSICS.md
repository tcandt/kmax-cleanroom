# Forensic Report 03: CloudPhone Agent Binary Forensics (Phase 1B)

## 1. Scope & Execution Parameters
- **Primary Binary Analyzed**: `cloudphone-v0.3.6 (1)/android/cloudphone-agent` (ELF 64-bit AArch64, size 13,828,244 bytes, SHA256: `f3dc523f3fc5be91...`)
- **Corroborating Target**: `cloudphone-agent-magisk-v0.3.6 (1)/binaries/cloudphone-agent-armeabi-v7a` (ELF 32-bit ARM, size 14,155,924 bytes, SHA256: `7ea2249e9c3e5eb5...`)
- **Target OS & Role**: Android Linux device daemon. Orchestrates Scrcpy server, captures hardware screen/audio, and connects to WebRTC signaling.
- **Obfuscation Status**: Go statically linked binary compiled with `garble`. Pclntab section size `0x4ecd48` bytes.

## 2. Quantitative Metrics
| Metric | Value | Forensic Significance |
|---|---|---|
| **Total Functions Detected** | **15,398** | Complete function bounds in `.gopclntab` |
| **Functions with pclntab Entries** | **15,398 (100.00%)** | Zero unmapped function entries |
| **Readable Runtime / Pion / Stdlib Functions** | **8,942** | `runtime.*`, `github.com/pion/*`, stdlib |
| **Garbled Project Functions** | **6,456** | Custom agent orchestration & control logic |
| **JSON Schema Keys Recovered** | **169** | Protocol attributes for device, video, and control |
| **Environment Variables & Flags Recovered** | **18** | Configuration flags and fallback defaults |
| **Direct Callgraph Edges Extracted** | **2,361** | Verified call relationships |
| **High Confidence Inferred Functions** | **8,942 (Stdlib/Pion) + 185 (Agent Core)** | Core Scrcpy and WebRTC lifecycle handlers |
| **Unknown Project Functions** | **6,271** | Scrambled helpers reserved for Phase 2 |

## 3. Cross-Architecture Corroboration (ARM64 vs ARMv7)
- **Binary Parity**: The ARM64 and ARMv7 binaries implement identical protocol state machines.
- **Identical IPC Strings**: Both contain exact strings for scrcpy-server launch, UDS dial (`[Stream] Dial video UDS error: %v`), privilege dropping (`dropping privileges to shell (UID 2000)`), and hash integrity checking (`INTEGRITY ERROR: libsys_core.so hash mismatch`).
- **Pion WebRTC Stack**: Both embed the complete Pion WebRTC engine with dynamic bitrate adaptation and keyframe injection.

## 4. Key Behavioral Discoveries
1. **Scrcpy Helper Lifecycle Orchestration**:
   - The agent copies the companion helper from release assets to `/data/local/tmp/libsys_core.so`.
   - Checks SHA256 integrity to ensure runtime tampering has not occurred.
   - Drops privileges to shell (`UID 2000`) before executing `app_process / com.android.helper.CoreService`.
   - Maintains a watchdog: if an old scrcpy process fails to exit within 2 seconds, it issues a force-kill.
2. **IPC Channel Multiplexing**:
   - Communicates with `libsys_core.so` over three local abstract UNIX domain sockets (UDS): Video stream, Audio stream, and Control stream.
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
