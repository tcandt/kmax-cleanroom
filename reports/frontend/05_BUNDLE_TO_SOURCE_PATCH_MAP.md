# 05_BUNDLE_TO_SOURCE_PATCH_MAP.md: Bundle Patches to Source Code Mapping

## 1. Executive Summary
This document provides the definitive semantic mapping between the minified production bundle patches (from `apply-r5-hotpath-recovery.cjs` and commit `e44dd2d`) and their corresponding functions in the reconstructed Vue source code.

Every functional hotpath fix applied to `index-DIPw8r74.js` is mapped to an explicit, typed, readable source function to guarantee zero regression during source reconstruction.

---

## 2. Comprehensive Patch-to-Source Mapping Table

| Patch ID & Name | Bundle Minified Target | Recovered Semantic Meaning | Reference Source Function | Target Reconstructed Source Function | Regression Test Step |
|:----------------|:-----------------------|:---------------------------|:--------------------------|:-------------------------------------|:--------------------:|
| **Patch 1**: PeerConnection Tracking | `A=new RTCPeerConnection(...)` | Assign unified `__sessionId` and track active `PeerConnection` globally. | `useWebRTC.js:createPeerConnection()` | `src/composables/useWebRTC.js` -> `createPeerConnection()` | Step 01 |
| **Patch 2**: DataChannel Lifecycle & Readiness | `d.onopen=()=>{...}` on `input-channel` | Trigger `CONTROL_READY` when `input-channel` opens; track DC open/close lifecycle. | `useWebRTC.js:setupDataChannel()` | `src/composables/useWebRTC.js` -> `onDataChannelOpen()` | Step 01, Step 03 |
| **Patch 3**: Touch Geometry & Rotation | `function Ot(P,ue,_e,Ue=0,Se=null)` | Calculate letterbox/pillarbox offsets, normalize $(u,v)$, apply device rotation, scale to logical $(W,H)$, log `[GEOMETRY]` & `[TOUCH-MAP]`. | `useWebRTC.js:sendTouch()` | `src/composables/useWebRTC.js` -> `sendTouch(action, clientX, clientY, pointerId, options)` | Step 03, Step 14 |
| **Patch 4**: WebSocket Keycode Translation | `function Qe(ae)` | Parse `input keyevent {code}` string command and dispatch keydown/keyup events. | `useWebSocketStream.js:sendCommand()` | `src/composables/useWebSocketStream.js` -> `injectKeycode(action, code)` | Step 06, Step 11 |
| **Patch 5**: WS Touch Diagnostics & UP Guarantee | `function z(ae,Ne,ze,et=0,lt=null)` | Guaranteed UP touch delivery on canvas edge mouseup; drop logging for out-of-bounds coords. | `useWebSocketStream.js:sendTouch()` | `src/composables/useWebSocketStream.js` -> `sendTouch(action, x, y, id)` | Step 10 |
| **Patch 6**: DevicePanel Mode Switch & Mount | `function Vt(){...}` | Synchronize mode switches with `window.__deviceModes` and store; preserve native switch. | `DeviceClient.vue:toggleMode()` | `src/views/DeviceClient.vue` -> `toggleStreamMode()` | Step 07, Step 12 |
| **Patch 7**: DevicePanel Unmount Lifecycle | `Te.disconnect(),...` | Log disposal and unregister WebRTC handle on component unmount. | `DeviceClient.vue:onUnmounted()` | `src/views/DeviceClient.vue` -> `onBeforeUnmount()` | Step 15 |
| **Patch 8**: Mouse Event Deduplication & UP | `function ZS(X)` | Handle mouse down, route middle/right clicks to HOME/BACK, focus hidden keyboard capture input. | `DeviceClient.vue:onMouseDown()` | `src/views/DeviceClient.vue` -> `handleMouseDown(event)` | Step 03, Step 04, Step 05 |
| **Patch 19c**: Store Mode Mirroring & Cleanup | `function Me(Ce,Ke="display")` | Mirror active mode to `window.__deviceModes` and clean up `window.__heldWebRTC` on reset. | `stores/devices.js:setDeviceMode()` | `src/stores/devices.js` -> `setDeviceMode(deviceId, mode)` | Step 07, Step 15 |
| **Patch 20**: WebRTC Hold on WS Switch (`e44dd2d`) | `function se(){...const isWs=...}` | **CRITICAL**: If switching to WebSocket mode while device active, DO NOT close PeerConnection; stash in `window.__heldWebRTC` to protect CoreService `app_process` from teardown. | `useWebRTC.js:disconnect()` | `src/composables/useWebRTC.js` -> `disconnect(options = { preserveSession: false })` | Step 07, Step 08 |
| **Patch 21**: Idempotent WS Disconnect | `function yt(){..._wsDisposed...}` | Guard against duplicate disconnects with instance ID and disposed flag. | `useWebSocketStream.js:disconnect()` | `src/composables/useWebSocketStream.js` -> `disconnect()` | Step 12 |
| **Patch 22**: Signaling OnOpen & Ready ACKs | `c.onopen=()=>{..._checkRtcReady...}` | Send `stream_ready` when both media & control ready; arm 15s watchdog timer. | `useWebRTC.js:initSignaling()` | `src/composables/useWebRTC.js` -> `checkAndEmitReady()` | Step 01, Step 02 |
| **Patch 22b**: WebRTC OnConnectionStateChange NACK | `A.onconnectionstatechange=()=>{...}` | Handle `connected` (close old held PC) and `failed` (emit `stream_failed`). | `useWebRTC.js:onConnectionStateChange()` | `src/composables/useWebRTC.js` -> `handleConnectionStateChange()` | Step 01, Step 13 |
| **Patch 23a**: WS Timeout NACK | `function w(){...FIRST_FRAME_TIMEOUT...}` | Send `stream_failed` with reason `FIRST_FRAME_TIMEOUT` if no frames received within 10s. | `useWebSocketStream.js:startTimeout()` | `src/composables/useWebSocketStream.js` -> `armTimeoutWatchdog()` | Step 09 |
| **Patch 23b/c**: WS First Frame ACKs | `e(Ne,0,0...),c.value||(...stream_ready...)` | Send `stream_ready` on first WebCodecs video frame decode or Canvas paint. | `useWebSocketStream.js:onFrameDecoded()` | `src/composables/useWebSocketStream.js` -> `onFirstFrameRendered()` | Step 09 |
| **Patch 24**: Component Render Key Epoch | `key:\`${i.deviceId}_...\`` | Append connection epoch and attempt ID to component key to guarantee clean DOM remounting. | `DeviceMatrix.vue:DeviceClient mount` | `src/views/DeviceMatrix.vue` -> `:key="\`${device.id}_${mode}_${epoch}\`"` | Step 16, Step 17 |

---

## 3. Implementation Directives for Phase F1 & F2
1. **Never use ad-hoc patching in source**: Every fix above must be written as clear, maintainable TypeScript/JavaScript with meaningful variable and function names.
2. **Preserve exact protocol messages**: Message types like `"stream_ready"`, `"stream_failed"`, `"connect"`, DataChannel labels `"input-channel"`, `"clipboard-channel"`, and touch payload structures must remain identical down to the byte.
3. **Explicit Session Holding**: Implement `holdWebRTCSession()` and `resumeWebRTCSession()` as explicit first-class methods in `useWebRTC.js`.
