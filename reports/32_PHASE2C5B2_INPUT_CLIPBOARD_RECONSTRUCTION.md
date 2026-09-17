# Phase 2C.5B2 Report: WebRTC Input & Clipboard DataChannel Clean-Room Reconstruction

**Phase**: Phase 2C.5B2  
**Date**: 2026-09-17  
**Contract Frozen SHA-256**: `3d7ebd83a675b2eb2103813a063cf012def36b98b4303f146b8b1c60ebaaa6f7`  
**Classification**: Clean-Room Behavioral/Protocol Reconstruction (Zero Claims of Literal Original Source)  
**Status**: CLOSED & FULLY VERIFIED  

---

## 1. Executive Summary & Scope Boundary

Phase 2C.5B2 completes the clean-room behavioral and protocol reconstruction of the two primary WebRTC DataChannels created by `cloudphone-agent`:
1. **`input-channel`**: Translates incoming JSON control events from the browser into exact big-endian binary scrcpy control frames dispatched toward the Android helper via the narrow `ControlSink` adapter (`@uds_sys_t_`).
2. **`clipboard-channel`**: Translates incoming JSON clipboard operations (`set_clipboard`, `get_clipboard`) and transmits response frames (`clipboard`) via the narrow `ClipboardProvider` adapter (`ClipboardManager`).

### Strict Phase Boundaries Maintained
- **Active Channels in B2**: `input-channel`, `clipboard-channel`.
- **Deferred Channels**: `camera-channel`, `file-channel`, `ai-command-channel`, and `adb-channel` remain strictly deferred with inert lifecycle hooks only. An automated verifier check enforces zero business handlers on deferred channels.
- **Signaling Server Boundary**: `webrtc-signaling` remains strictly a signaling relay (zero WebRTC / Pion imports).
- **Media Plane Boundary**: Full video/audio hardware capture pipeline remains deferred to Phase B5.

---

## 2. Implementation Contract Frozen First

Prior to modifying production source code, the Phase 2C.5B2 contract was machine-derived solely from frozen evidence and committed:
- **Contract Path**: `evidence/go_agent/webrtc/DATACHANNEL_B2_IMPLEMENTATION_CONTRACT.json`
- **Frozen SHA-256**: `3d7ebd83a675b2eb2103813a063cf012def36b98b4303f146b8b1c60ebaaa6f7`
- **Governing Evidence**:
  - `DATACHANNEL_LABEL_EVIDENCE.json`
  - `DATACHANNEL_FRAMING_MATRIX.json`
  - `DATACHANNEL_MESSAGE_TYPE_EVIDENCE.json`
  - `CONTROL_INPUT_PROTOCOL_CROSSMAP.json`
  - `AGENT_HELPER_IPC_SOCKET_MATRIX.json`
  - `WEBRTC_CORE_IMPLEMENTATION_CONTRACT.json`

---

## 3. Input Channel Protocol & Binary Control Translation

### Confirmed Event Discriminators
Derived from Agent binary disassembly (`woxaqqFN5Km.func8` at `0x9e39c0`):
- `inject_touch` / `touch`: Dispatched to `gnM0lsYaM` (`0x9cf7e0`).
- `inject_keycode`: String check at `0x9e3ace`, dispatched to `rKbdAxdt` (`0x9cce20`).
- `inject_text`: String check at `0x9e3a4d`, dispatched to `cMG2_76Q` (`0x9cd280`).
- `inject_scroll`: String check at `0x9e3c07`, dispatched to `yUpFvK` (`0x9cef40`).
- `hard_keyboard`: String check at `0x9e3b60`, dispatched to `ibGYZ1JMSNE` (`0x9cd720`).

### Big-Endian Binary Framing Specification

| Event | Message Type | Wire Length | Byte Layout & Endianness | Disassembly / Helper Source |
|---|---|---|---|---|
| **Touch** | `2` (`INJECT_TOUCH_EVENT`) | 32 bytes | `[type:1, action:1, pointerId:8 (BE), x:4 (BE), y:4 (BE), w:2 (BE), h:2 (BE), pressure:2 (BE), actionBtn:4 (BE), buttons:4 (BE)]` | AMD64 `0x9cfb54-0x9cfc0e` (`bswap`/`rol`), `ControlMessageReader.java:99` |
| **Keycode** | `0` (`INJECT_KEYCODE`) | 14 bytes | `[type:1, action:1, keycode:4 (BE), repeat:4 (BE), meta:4 (BE)]` | `ControlMessageReader.java:69` |
| **Text** | `1` (`INJECT_TEXT`) | 5 + N bytes | `[type:1, length:4 (BE uint32), utf8_bytes:N]` | `ControlMessageReader.java:95` |
| **Scroll** | `3` (`INJECT_SCROLL_EVENT`) | 21 bytes | `[type:1, x:4 (BE), y:4 (BE), w:2 (BE), h:2 (BE), hScroll:2 (BE i16), vScroll:2 (BE i16), buttons:4 (BE)]` | `ControlMessageReader.java:103` |
| **Hard Keyboard** | `15` (`OPEN_HARD_KEYBOARD_SETTINGS`) | 1 byte | `[type:1 (0x0f)]` | `ControlMessageReader.java:40` |

### Pressure Encoding
- Action `UP` (`1`): Pressure = `0x0000` (disassembly `mov word ptr [rax + 0x16], 0` at `0x9cfbbb`).
- Action `DOWN` (`0`) / `MOVE` (`2`): Pressure = `0xffff` (disassembly `mov word ptr [rax + 0x16], 0xffff` at `0x9cfbc4`).

---

## 4. Clipboard Channel Protocol & System Boundary

### Protocol Specification
- **`set_clipboard`**: Ingress frame with fields `{ "type": "set_clipboard", "text": string, "paste": bool, "source": string, "origin_client_id": string }`. Handled at `0x9e3860` and passed to `ClipboardProvider.Set(text, paste, originClientID)`.
- **`get_clipboard`**: Ingress query frame `{ "type": "get_clipboard" }`. Handled at `0x9e38ce`, queries `ClipboardProvider.Get()`, and transmits response frame over `clipboard-channel`.
- **`clipboard`**: Egress response frame `{ "type": "clipboard", "text": string, "source": "device", "origin_client_id": null }`.
- **Literal Provenance**: `origin_client_id` is an exact verified string in binary rodata (`0xb5...`).
- **Payload Bounds**: Maximum payload length enforced at 262,130 bytes matching `CLIPBOARD_TEXT_MAX_LENGTH`.

---

## 5. Real SCTP DataChannel E2E Verification

The test `TestWebRTCDataChannelsE2E` in `tests/webrtc_e2e_test.go` verifies true SCTP DataChannel communication across standard WebRTC peers:
1. **Input E2E**: Browser sends JSON touch event over SCTP `input-channel` -> Agent `HandleInputMessage` decodes -> serializes 32-byte big-endian scrcpy frame -> writes to `ControlSink`. Verified exact byte match:
   ```text
   [PASS] input-channel SCTP E2E: Browser JSON -> Agent -> ControlSink verified with exact 32-byte scrcpy frame
   ```
2. **Clipboard Set E2E**: Browser sends `set_clipboard` over SCTP `clipboard-channel` -> Agent updates `ClipboardProvider` with text and metadata:
   ```text
   [PASS] clipboard-channel set_clipboard SCTP E2E verified in ClipboardProvider
   ```
3. **Clipboard Get E2E**: Browser sends `get_clipboard` over SCTP `clipboard-channel` -> Agent queries `ClipboardProvider` -> transmits JSON response back over SCTP -> Browser parses and validates:
   ```text
   [PASS] clipboard-channel get_clipboard SCTP E2E verified: Agent -> Browser response confirmed
   ```

---

## 6. Differential Results & Parity Counters

From `evidence/go_agent/webrtc/DATACHANNEL_B2_DIFFERENTIAL_RESULT.json`:
```json
{
  "counters": {
    "exact_protocol_parity_total": 16,
    "exact_protocol_parity_passed": 16,
    "exact_binary_frame_total": 5,
    "exact_binary_frame_passed": 5,
    "semantic_parity_total": 4,
    "semantic_parity_passed": 4,
    "runtime_e2e_total": 4,
    "runtime_e2e_passed": 4,
    "verified_divergence_total": 0,
    "environment_unavailable_total": 0,
    "implementation_choice_tests": 8,
    "failed_total": 0
  },
  "overall_verdict": "PASS_PHASE_2C5B2_CLOSED"
}
```

---

## 7. Full Suite Regression Results

| Suite | Scope | Result | Details |
|---|---|---|---|
| **Agent Suite** (`go test -v ./...`) | `cloudphone-agent` | **33/33 PASS** | 21 in `pkg/webrtc`, 4 in `pkg/signaling`, 4 in `pkg/agent`, 4 in `tests/` |
| **Signaling Suite** (`go test ./...`) | `webrtc-signaling` | **PASS** | Existing transport & auth suites intact |
| **Transport Differential** | `transport_differential_test.py` | **48/48 PASS** | Tested against authentic original binary oracle |
| **WebRTC Forensics** | `reproduce_webrtc_datachannel_forensics.py` | **14/14 PASS** | 19/19 gate dimensions verified |
| **Transport Forensics** | `reproduce_transport_forensics.py` | **23/23 PASS** | Zero hardcoded offsets, 100% semantic derivation |
| **Master Verifier** (`verify_phase2.py`) | Whole Cleanroom Workspace | **21/21 Sections PASS** | Zero-mutation audit passed cleanly |

---

## 8. Source Provenance Classification

All delivered symbols in `reconstructed_source/cloudphone-agent` are classified in `evidence/go_agent/webrtc/DATACHANNEL_B2_SOURCE_PROVENANCE.json`:
- `EncodeTouchEvent`, `EncodeKeycodeEvent`, `EncodeTextEvent`, `EncodeScrollEvent`, `EncodeHardKeyboardEvent`: `RECONSTRUCTED_FROM_BINARY`.
- `HandleInputMessage`, `HandleClipboardMessage`: `RECONSTRUCTED_FROM_BINARY`.
- `TouchEvent`, `KeycodeEvent`, `TextEvent`, `ScrollEvent`, `SetClipboardMessage`, `GetClipboardMessage`: `RECONSTRUCTED_FROM_PROTOCOL`.
- `ControlSink`, `ClipboardProvider`, `DataChannels.SetControlSink`, `Coordinator.SetControlSink`: `GENERATED_ADAPTER`.
- `MemoryControlSink`, `MemoryClipboardProvider`: `IMPLEMENTATION_CHOICE`.

---

## 9. Next Steps
Phase 2C.5B2 is **COMPLETE and CLOSED**.
Per user instructions, Phase 2C.5B3 (`file-channel` reconstruction) will await explicit review and authorization before proceeding.
