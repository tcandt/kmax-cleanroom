# 04_DOM_BEHAVIOR_CONTRACTS.md: DOM Selectors & Interaction Contracts

## 1. Executive Summary
This document freezes all DOM element contracts, CSS classes, attributes, and interaction patterns required by automated regression suites (`test-regression-flow.cjs`, `click-retry.cjs`, `test-find-ws-btn.cjs`, `verify-live-dom-cjk.cjs`). Reconstructed Vue components MUST maintain exact structural compatibility with these contracts.

---

## 2. Interactive DOM Contracts

### 2.1 Streaming Media Viewports
| Media Protocol | Element Selector | Required Attributes / Properties | Event Handlers |
|:---------------|:-----------------|:---------------------------------|:---------------|
| WebRTC Video | `video.video-stream` | `autoplay`, `playsinline`, `muted`. `videoWidth > 0`, `videoHeight > 0`, `paused === false`. | `mousedown`, `mousemove`, `mouseup`, `contextmenu` (prevent default) |
| WebSocket Canvas | `canvas.video-stream` | `width > 0`, `height > 0`. | `mousedown`, `mousemove`, `mouseup` |

---

### 2.2 Navigation & Control Action Buttons
| Control Action | Primary Selector | Fallback / Title Contract | Behavior / Event |
|:---------------|:-----------------|:--------------------------|:-----------------|
| Switch Stream Protocol | `button[data-action="switch-stream"]` | `button.sidebar-btn[title*="WebSocket"]` or `button.sidebar-btn[title*="WebRTC"]` | Toggles streaming protocol between WebRTC and WebSocket. |
| Stream Retry | `button.retry-btn[data-action="retry"]` | `button.retry-btn` with text content `"Retry"` | Retries signaling / connection negotiation. |
| Android HOME | `button[title="HOME"]` | `.nav-btn[title="HOME"]` or `.sidebar-btn` | Injects Android Keycode 3 (KEYCODE_HOME). |
| Android BACK | `button[title="BACK"]` | `.nav-btn[title="BACK"]` or `.sidebar-btn` | Injects Android Keycode 4 (KEYCODE_BACK). |
| Android POWER | `button[title="POWER"]` | `.nav-btn[title="POWER"]` | Injects Android Keycode 26 (KEYCODE_POWER). |
| Device Close / Teardown | `.close-stream-btn` | `.item-btn.close-btn` or `button[title="Close"]` | Closes active device stream and returns to matrix. |

---

### 2.3 Device Matrix & Selection
| Component Surface | Target Selector | Contract / Attributes |
|:------------------|:----------------|:----------------------|
| Device Card (Matrix) | `.device-card` | Contains `.device-name` matching device ID/alias. Click or `ctrlKey + click` opens device view. |
| Online Badge | `.online-chip`, `.status-badge` | Text format: `"{N} Online"`. |
| Display Options Popover | `button:has(.btn-text:contains("Display Options ▾"))` | Opens view scale / FPS / direct preview interaction toggles. |
| Tag Management Button | `.top-action-btn:contains("Tags")` | Opens `TagManagerModal`. |
| Settings Button | `.top-action-btn:contains("Settings")` | Opens `SettingsModal`. |
| Group Control Toggle | `.top-action-btn:contains("Group Control")` | Toggles batch multi-select mode. |

---

### 2.4 Keyboard & Input Capture
- **Element**: Hidden textarea or input element with `.keyboard-capture-input` or focused on click.
- **Behavior**: Focused when clicking on video surface to route `keydown` and `keyup` events to `input-channel`.
- **Composition / IME Support**: Listens to `compositionstart` / `compositionend` for CJK / accented inputs.

---

### 2.5 Telemetry & Status Badges
- **Selector**: `.stream-meta`, `.fps-badge`, `.header-meta`.
- **Text Format**: Contains telemetry metrics: `SRC {fps} | RX {kbps} | E2E ~{ms} | RTT {ms} | UDP p2p`.
- **Mode Badge**: Shows `"WebRTC"` or `"WebSocket"`.
