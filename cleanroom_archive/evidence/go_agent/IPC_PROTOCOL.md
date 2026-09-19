# CloudPhone Agent: IPC Protocol & Scrcpy Helper Interaction

## 1. Helper Deployment & Execution Protocol

1. **Payload Distribution**: The agent embeds or downloads `libsys_core.so`.
2. **Stealth Staging**: Target path is `/data/local/tmp/libsys_core.so`.
3. **Hash Integrity Verification**: Prior to launch, the agent verifies file integrity (`INTEGRITY ERROR: libsys_core.so hash mismatch`).
4. **Permission Dropping**: Dropped privileges to shell UID 2000 (`Run scrcpy-server by dropping privileges to shell (UID 2000) for touch input support`).
5. **Execution Command**: Launches `com.android.helper.CoreService` via Android's `app_process`.
6. **Lifecycle Management**: Kills orphaned processes with a 2-second timeout before force-killing.

## 2. IPC Sockets & Channel Multiplexing

- **UDS Video Channel**: Local abstract socket for H.264/H.265 raw NAL stream ingestion (`[Stream] Dial video UDS error: %v`).
- **UDS Control Channel**: Binary touch, keycode, and clipboard command injection (`ControlMessage`, `PositionMapper`).
- **Dynamic Bitrate Control**: Real-time adjustment of scrcpy encoder bitrate (`[Agent] Dynamically adjusted scrcpy-server video bitrate to %d bps`).
- **Dual-Profile Multiplexer**: Low-profile for background previews; high-profile for active WebRTC peer sessions.
