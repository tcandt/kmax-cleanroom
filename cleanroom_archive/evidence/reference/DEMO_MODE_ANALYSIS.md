# Forensic Analysis: Frontend Demo Mode vs Real Protocol Path

**Evidence Classification**: `PUBLIC_REFERENCE_INTELLIGENCE`  
**Target Repository**: `tcandt/scrcpyoverwebrtc` (commit: `65567d777bccb11d2a6d93b6acc735478e880b5b`)  
**Analyzed Files**:
- `web-app/.env.demo`
- `web-app/src/mock/demoEngine.js`
- `web-app/src/composables/useWebRTC.js`

---

## 1. Executive Summary

Static code inspection of the public web frontend confirms the presence of an integrated **Simulation / Demo Engine** controlled by the environment variable `VITE_DEMO_MODE=true`.

When `VITE_DEMO_MODE` is enabled:
1. All WebSocket signaling connections (`/connect_client`) are **completely short-circuited**.
2. WebRTC peer connections (`RTCPeerConnection`), SDP negotiations, and DataChannels are **never created**.
3. Devices, metrics, and responses are simulated entirely within the browser via `web-app/src/mock/demoEngine.js`.

> [!WARNING]
> **METHODOLOGICAL DIRECTIVE**:
> Demo mode artifacts (`demo.html` or demo builds) **MUST NOT** be used as a backend dynamic oracle for signaling traffic, WebRTC negotiation, agent protocol framing, or binary wire formats. All backend protocol claims must be verified exclusively against the real protocol path (`REAL_PROTOCOL_PATH`) confirmed by binary evidence.

---

## 2. Code Evidence of Short-Circuiting

### A. Environment Configuration (`web-app/.env.demo`)
```ini
VITE_DEMO_MODE=true
VITE_APP_TITLE=云手机管理控制台 (Demo 演示版)
```

### B. Immediate Signaling Bypass in `useWebRTC.js`
In `web-app/src/composables/useWebRTC.js` (lines 65-75):
```javascript
  function connect(shareTokenParam = null, sharePwdParam = '') {
    status.value = 'connecting'
    error.value = null

    if (import.meta.env.VITE_DEMO_MODE === 'true') {
      setTimeout(() => {
        status.value = 'connected'
      }, 300)
      return
    }

    const wsProtocol = location.protocol === 'https:' ? 'wss:' : 'ws:'
    const token = localStorage.getItem('auth_token') || ''
    let wsUrl = `${wsProtocol}//${location.host}/connect_client?token=${encodeURIComponent(token)}`
    ...
```
**Observation**: If `VITE_DEMO_MODE === 'true'`, the function sets `status.value = 'connected'` after 300ms and immediately returns, never instantiating a `WebSocket` or `RTCPeerConnection`.

### C. Synthetic Mock Engine (`web-app/src/mock/demoEngine.js`)
`demoEngine.js` defines:
- `MOCK_DEVICES`: 3 hardcoded devices (`Pixel-6Pro-ARM64`, `Redroid-S22-Container`, `Xiaomi13-Magisk-v030`).
- Mock statistics generator: CPU, RAM, temperature, network up/down metrics generated on an interval timer.
- Simulated commands: Synthetic responses for shell command execution.

---

## 3. Separation of Protocol Paths

| Dimension | `REAL_PROTOCOL_PATH` | `MOCK_DEMO_PATH` |
|---|---|---|
| **Activation Flag** | `VITE_DEMO_MODE=false` (or unset) | `VITE_DEMO_MODE=true` (`.env.demo`) |
| **Signaling Transport** | Real WebSocket to `/connect_client?token=...` | None (bypassed at line 73) |
| **ICE & SDP Handshake** | Real SDP offer/answer exchange, Trickle ICE | None (mock state transition after 300ms) |
| **Video Stream** | Real WebRTC video track (H.264 decoded via `<video>`) or WebSocket TCP | Simulated canvas animation or static placeholder |
| **DataChannels** | Real P2P DataChannels (`input-channel`, `clipboard-channel`, etc.) | Mock DOM listeners |
| **Server Requirement** | Requires live `webrtc-signaling` + `cloudphone-agent` | Completely offline / standalone static HTML |
| **Cleanroom Oracle Value** | **HIGH**: Exact protocol specifications | **ZERO for backend protocol**: Useful only for UI/UX inventory |

---

## 4. Methodological Conclusion

1. **UI/UX & Workflow Value**: The public reference repo provides accurate inventories of UI views, user options, settings keys, and intended workflows.
2. **Backend Oracle Value**: Wire-level protocol rules must be corroborated against the Go signaling binary (`webrtc-signaling`) and Go agent binary (`cloudphone-agent`) via disassembly, pclntab symbols, and dynamic network tests.
