# Patch Documentation: WebApp Mode Switch Reactivity (`Vt()` Reinit)

## 1. Metadata
- **Target Component**: `DevicePanel.vue` (minified in `public/assets/index-DIPw8r74.js` and `dist/assets/index-DIPw8r74.js`)
- **Baseline Checksum (SHA-256)**: `30f9494bd783a6b133ac63c3c5ad3bdb793c3cf257fb6395e78c869d755366cb`
- **Patched Checksum (SHA-256)**: `0da8adfd22e40e014ed25442163c0fff9b737be5ce64b624e074fe503945af60`
- **Patch Tool**: [`scripts/patches/patch-webapp-mode-switch.cjs`](file:///d:/KMAX-CLEANROOM/scripts/patches/patch-webapp-mode-switch.cjs)
- **Classification**: `FORENSIC_RUNTIME_PATCH` (Temporary recovery measure until Vue SFC component reconstruction).

---

## 2. Problem Description & Root Cause
In upstream `index-DIPw8r74.js`:
1. `DevicePanel` initializes its active transport stream as:
   ```javascript
   function Ue(X, Y) { return n.getDeviceMode(X) === "websocket" ? A9(X, Y) : Ty(X, Y); }
   const Se = uB(Ue(a.value, T.value));
   const Te = new Proxy({}, {
     get(X, Y) { const pe = Se.value; if (!pe) return; const Je = pe[Y]; return typeof Je == "function" ? (...kt) => Je.apply(pe, kt) : Je; },
     set(X, Y, pe) { return Se.value && (Se.value[Y] = pe), !0; }
   });
   ```
2. When WebRTC negotiation fails and the user clicks **"⚡ 改用 WebSocket 投屏"**, handler `Vt()` executed:
   ```javascript
   // Original upstream implementation
   function Vt() {
     const X = Ye.value ? "display" : "websocket";
     n.setDeviceMode(a.value, X);
   }
   ```
3. Because `Se.value` was not re-evaluated, `Te` remained bound to the defunct WebRTC instance (`Ty`).
4. Any touch, click, or keyboard input on the canvas called `Te.sendTouch()` / `Te.sendInjectKeycode()`, triggering:
   ```text
   [DataChannel] sendInjectKeycode failed: inputChannel is not open
   ```

---

## 3. Patch Diff & Behavior
The patch extends `Vt()` to re-instantiate `Se.value` and re-bind event listeners:

```diff
- function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X)}
+ function Vt(){const X=Ye.value?"display":"websocket";n.setDeviceMode(a.value,X);a.value&&(Te.disconnect(),Se.value=Ue(a.value,T.value),n.registerWebRTC(a.value,Te),yo())}
```

### Execution Flow:
1. `n.setDeviceMode(deviceId, "websocket")` sets the Pinia store mode.
2. `Te.disconnect()` cleans up the failed WebRTC session.
3. `Se.value = Ue(deviceId, options)` creates the `useWebSocketPreview` (`A9`) session.
4. `n.registerWebRTC(deviceId, Te)` updates the global store pointer.
5. `yo()` sets canvas getters, listens to frame size updates, and calls `Te.connect()`, which triggers `start_preview`.
6. Subsequent `sendTouch`, `sendInjectKeycode`, `sendScroll` calls are routed over WebSocket via `sendGroupControlEvent`.

---

## 4. Usage & Verification
To apply or verify the patch:
```powershell
node scripts/patches/patch-webapp-mode-switch.cjs
```

To revert to original upstream baseline:
```powershell
node scripts/patches/patch-webapp-mode-switch.cjs --revert
```
