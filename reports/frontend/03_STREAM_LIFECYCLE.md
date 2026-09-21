# 03_STREAM_LIFECYCLE.md: Streaming Protocol & Lifecycle Invariants

## 1. Executive Summary
The KMAX streaming subsystem supports two distinct presentation pipelines:
1. **Primary**: Ultra-low-latency P2P WebRTC video (`display` / `camera` tracks) with SCTP DataChannels (`input-channel`, `clipboard-channel`).
2. **Secondary / Fallback**: TCP WebSocket raw H.264 NALU stream with WebCodecs hardware `VideoDecoder` or Canvas software renderer.

The golden invariant discovered and enforced in `e44dd2d` is that **switching from WebRTC to WebSocket must NOT terminate the WebRTC peer connection**, as doing so signals the device daemon to terminate the background `app_process` (CoreService), breaking subsequent streaming sessions.

---

## 2. WebRTC Streaming Lifecycle (`useWebRTC.js`)

```text
[CLOSED]
   │
   ▼ user opens device / mounts DeviceClient
[OPENING]
   │
   ├── connect signaling WebSocket (/connect_client?device_id=...)
   │   └─ [SIGNALING_CONNECTED]
   │
   ├── send { message_type: "connect", device_id }
   │
   ├── receive SDP offer -> create RTCPeerConnection
   │   └─ create answer -> send SDP answer
   │
   ├── trickle ICE candidates
   │
   ├── ontrack: MediaStream attached to <video>
   │   └─ triggers: MEDIA_READY
   │
   ├── ondatachannel: "input-channel" open
   │   └─ triggers: CONTROL_READY
   │
   ▼ (both MEDIA_READY & CONTROL_READY true)
[READY]
   └─ send { message_type: "stream_ready", device_id, mode: "webrtc", generation, attempt_id }
```

### Timeout & Failure Protection:
- 15-second watchdog timer monitors connection progression.
- If unfulfilled, emits `{ message_type: "stream_failed", reason: "RTC_CONNECT_TIMEOUT" }`.

---

## 3. WebSocket Stream Lifecycle (`useWebSocketStream.js`)

```text
[CLOSED]
   │
   ▼ mode switch / fallback triggered
[CONNECTING]
   │
   ├── connect WS stream endpoint
   │
   ├── send preview control subscription: start_preview
   │
   ├── receive binary NALU header / stream packets
   │
   ├── WebCodecs VideoDecoder configuration & frame decode
   │   └─ output ImageBitmap -> paint to <canvas class="video-stream">
   │
   ▼ (first frame painted)
[READY]
   └─ send { message_type: "stream_ready", device_id, mode: "websocket", generation, attempt_id }
```

---

## 4. WebRTC ↔ WebSocket Handoff Protocol (`[WebRTC-HOLD]`)

```text
User clicks "Switch to WebSocket" (Step 07)
   │
   ├── DeviceClient sets deviceMode = "websocket"
   │
   ├── useWebRTC.disconnect() is called:
   │   ├── Check: isActiveDevice && isWsMode?
   │   ├── TRUE -> DO NOT CLOSE PeerConnection!
   │   │   ├── Store { pc, ws } in window.__heldWebRTC[deviceId]
   │   │   ├── Retain CoreService app_process on Android device (Step 08 PASS)
   │   │   └── Detach <video>.srcObject only
   │   └── FALSE -> Full teardown (PeerConnection.close())
   │
   ▼
Mount useWebSocketStream (Canvas starts streaming) (Steps 09-11)
   │
User clicks "Switch to WebRTC" (Step 12)
   │
   ├── DeviceClient sets deviceMode = "display"
   ├── useWebSocketStream.disconnect() completes idempotently
   ├── Mount useWebRTC:
   │   ├── Checks window.__heldWebRTC[deviceId]
   │   └── Recovers or cleanly re-negotiates WebRTC session
   │
   ▼
WebRTC video returns & touch controls confirmed (Steps 13-14 PASS)
```

---

## 5. Touch & Geometry Mapping Contract (`[GEOMETRY]`, `[TOUCH-MAP]`)

When dispatching pointer events to the video surface, letterbox/pillarbox bars must be subtracted to ensure 100% geometric accuracy:

1. **Calculate Aspect Ratios**:
   $$\text{aspect}_{\text{frame}} = \frac{\text{videoWidth}}{\text{videoHeight}}, \quad \text{aspect}_{\text{viewport}} = \frac{\text{rect.width}}{\text{rect.height}}$$
2. **Compute Content Rect (Excluding Bars)**:
   * If $\text{aspect}_{\text{viewport}} > \text{aspect}_{\text{frame}}$ (pillarbox):
     $$\text{contentH} = \text{rect.height}, \quad \text{contentW} = \text{rect.height} \times \text{aspect}_{\text{frame}}$$
     $$\text{offsetX} = \frac{\text{rect.width} - \text{contentW}}{2}, \quad \text{offsetY} = 0$$
   * If $\text{aspect}_{\text{viewport}} \le \text{aspect}_{\text{frame}}$ (letterbox):
     $$\text{contentW} = \text{rect.width}, \quad \text{contentH} = \frac{\text{rect.width}}{\text{aspect}_{\text{frame}}}$$
     $$\text{offsetX} = 0, \quad \text{offsetY} = \frac{\text{rect.height} - \text{contentH}}{2}$$
3. **Normalize Coordinates**:
   $$u = \text{clamp}\left(0, 1, \frac{\text{clientX} - \text{rect.left} - \text{offsetX}}{\text{contentW}}\right)$$
   $$v = \text{clamp}\left(0, 1, \frac{\text{clientY} - \text{rect.top} - \text{offsetY}}{\text{contentH}}\right)$$
4. **Apply Device Rotation & Logical Scale**:
   * Map $(u, v)$ based on `rotation` ($0^\circ, 90^\circ, 180^\circ, 270^\circ$).
   * Scale to logical device resolution $(B.\text{value}, w.\text{value})$.
5. **Serialize Input**:
   Send payload `{ type: "touch", id, seq, client_ts_ms, action, x, y, w, h }` across DataChannel.
