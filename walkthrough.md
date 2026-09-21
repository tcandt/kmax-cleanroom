# Phase E6 — Residual English UI Completion Walkthrough (V2 Complete)

## 1. Executive Summary
- **Objective**: Complete all residual English UI normalization across the KMAX Web Console starting from baseline `02f7085` (`phase-e-english-ui-v1`), achieving `0 visible CJK` in the live DOM across all 14 screens, dropdowns, dialogs, and interactive modals, while maintaining strict streaming stability and zero functional regression.
- **Outcome**: **100% English Web Console Confirmed (`TOTAL LIVE DOM VISIBLE CJK: 0`)**.
- **Static Verification**: All 6 static verification gates passed (`scripts/ui/verify-ui-english.cjs`).
- **Runtime Regression**: 17/17 end-to-end streaming, WebRTC ↔ WebSocket mode switching, touch, keyboard, and reconnect gates passed (`scripts/test-regression-flow.cjs`).
- **Reversibility**: Revert round-trip verified byte-for-byte back to V1 SHA `334563779fbe...` and forward to V2 SHA `295a41f179bc...`.

---

## 2. Invariants & Hashes

### Baseline Input (Phase E1–E5 / `phase-e-english-ui-v1` at `02f7085`)
- `V1_SHA256_PUBLIC`: `334563779fbe10893c9b39c9ab0816df1f4c6656024fc36ae9baf01d4513200c`
- `V1_SHA256_DIST`: `334563779fbe10893c9b39c9ab0816df1f4c6656024fc36ae9baf01d4513200c`
- `V1_SHA256_INDEX_HTML`: `e8bf81547b05e8ed73783cbcae9f9aeb43f923577789d8e8a65e603967228b85`
- `V1_SHA256_DIST_INDEX_HTML`: `babb7c96410b962c3197a7849dd09e464b36ac2cfc2fe9e9d586914426ca01be`

### Final Normalization Output (Phase E6 / `phase-e-english-ui-v2-complete`)
- `V2_SHA256_PUBLIC`: `295a41f179bc05b94222abe5a9512b59851dfee67b0bb6a3c1ed166315c73f79`
- `V2_SHA256_DIST`: `295a41f179bc05b94222abe5a9512b59851dfee67b0bb6a3c1ed166315c73f79`
- `V2_SHA256_INDEX_HTML`: `e8bf81547b05e8ed73783cbcae9f9aeb43f923577789d8e8a65e603967228b85`
- `V2_SHA256_DIST_INDEX_HTML`: `babb7c96410b962c3197a7849dd09e464b36ac2cfc2fe9e9d586914426ca01be`

---

## 3. Category C Protected Literal Exact Counts (21/21 Intact)

All 21 protected Category C literals were verified before and after transformation with exact count equality enforced:

| Index | Protected Literal | Baseline Count | Post-E6 Count | Status |
|:-----:|:------------------|:--------------:|:-------------:|:------:|
| 0 | `display` | 156 | 156 | **PASS** |
| 1 | `camera` | 176 | 176 | **PASS** |
| 2 | `websocket` | 15 | 15 | **PASS** |
| 3 | `input-channel` | 3 | 3 | **PASS** |
| 4 | `clipboard-channel` | 3 | 3 | **PASS** |
| 5 | `stream_ready` | 4 | 4 | **PASS** |
| 6 | `stream_failed` | 3 | 3 | **PASS** |
| 7 | `MEDIA_READY` | 2 | 2 | **PASS** |
| 8 | `CONTROL_READY` | 2 | 2 | **PASS** |
| 9 | `READY` | 11 | 11 | **PASS** |
| 10 | `OPENING` | 3 | 3 | **PASS** |
| 11 | `CLOSED` | 9 | 9 | **PASS** |
| 12 | `FAILED` | 4 | 4 | **PASS** |
| 13 | `touch` | 59 | 59 | **PASS** |
| 14 | `keydown` | 9 | 9 | **PASS** |
| 15 | `keyup` | 3 | 3 | **PASS** |
| 16 | `[GEOMETRY]` | 1 | 1 | **PASS** |
| 17 | `[TOUCH-MAP]` | 1 | 1 | **PASS** |
| 18 | `[LIFECYCLE]` | 3 | 3 | **PASS** |
| 19 | `[READY-CHECK]` | 1 | 1 | **PASS** |
| 20 | `[WebRTC-HOLD]` | 2 | 2 | **PASS** |

---

## 4. Static Verification Gates (`verify-ui-english.cjs`)

```text
================================================================
Phase E6: English UI Normalization Verification (V2 Complete)
================================================================

--- Gate 1: Post-English V2 SHA256 Verification ---
  [PASS] public_bundle   : 295a41f179bc05b94222abe5a9512b59851dfee67b0bb6a3c1ed166315c73f79
  [PASS] dist_bundle     : 295a41f179bc05b94222abe5a9512b59851dfee67b0bb6a3c1ed166315c73f79
  [PASS] public_html     : e8bf81547b05e8ed73783cbcae9f9aeb43f923577789d8e8a65e603967228b85
  [PASS] dist_html       : babb7c96410b962c3197a7849dd09e464b36ac2cfc2fe9e9d586914426ca01be

--- Gate 2: Protected Literal Exact Counts Verification ---
  [PASS] All 21/21 protected literals exactly preserved

--- Gate 3: Replacement Rule Integrity Verification ---
  [PASS] All 207/207 active replacement rules verified
         (= 71 V1 replacement rules + 136 E6 replacement rules)
  [PASS] ui-english-map.json: 216 total entries
         (= 207 active replacement rules + 9 protected definitions)

--- Gate 4: HTML lang="en" Normalization Verification ---
  [PASS] public_html: lang="en" verified, lang="zh-CN" absent
  [PASS] dist_html: lang="en" verified, lang="zh-CN" absent

--- Gate 5: Transformed JS Syntax Verification ---
  [PASS] Transformed bundle passes node --input-type=module --check

--- Gate 6: CJK Inventory Classification Audit ---
  Remaining CJK literals accounted for: 675
  Category A: 579, B: 73, C: 12, D: 1, Vendor: 10
  UNCLASSIFIED: 0
  [PASS] UNCLASSIFIED = 0, full inventory classified

================================================================
PHASE E6 VERIFICATION = PASS
All 6 static and structural verification gates PASSED.
================================================================
```

---

## 5. Interactive Live DOM CJK Sweep (10 Automated Scenarios Covering 14 Views & Modals)

A deep interactive Chrome DevTools Protocol (CDP) sweep was executed across 10 automated scenarios covering 14 interactive views, dialogs, dropdowns, and modals:
- Matrix Grid & Navigation Header
- Display Options Popover (Resolution scale, FPS, direct preview interaction)
- Device Card Context Menu (Actions, terminal, restart, settings)
- Tag Management Modal (Tag list, input, submit, close)
- Group Control Mode & Batch Action Bar
- User Permissions & Global Settings Modal
- Connection Settings Modal (Video, Preview, Audio, Advanced tabs)
- Single Device Streaming View (DeviceClient canvas, in-use banner)
- Streaming Toolbar & WebRTC ↔ WebSocket Mode Switch
- Telemetry Overlay & Stream Status Badges
- Route `/deploy` (Deployment matrix)
- Route `/share` (Share link generator)

| Scenario | Scope / Views Covered | Visible CJK Found | Status |
|:---------|:----------------------|:-----------------:|:------:|
| 1. Dashboard / Matrix View (Main) | Header, grid, statistics badges, device cards | 0 | **PASS** |
| 2. Display Options Dropdown | Resolution scale, FPS, interactive card toggles | 0 | **PASS** |
| 3. Device Card More Actions Menu | Context actions, restart, terminal, settings | 0 | **PASS** |
| 4. Tag Management Dialog | Tag list, input placeholder, add/submit button | 0 | **PASS** |
| 5. Group Control Mode Active | Group selection bar, batch actions, tag filters | 0 | **PASS** |
| 6. User Permissions / Settings Dialog | Tabs, permission switches, connection configs | 0 | **PASS** |
| 7. Route: `/deploy` | Deployment matrix, task triggers, logs | 0 | **PASS** |
| 8. Route: `/share` | Share link generator, duration pickers, permissions | 0 | **PASS** |
| 9. Single Device Control View | Streaming canvas, telemetry headers, in-use banner | 0 | **PASS** |
| 10. Streaming Toolbar & Mode Switch | Control bar, WebRTC ↔ WebSocket switch, popovers | 0 | **PASS** |

**Total Live DOM Visible CJK across all views: 0**.

---

## 6. Runtime Streaming Regression Results (`test-regression-flow.cjs`)

The standardized 17-step end-to-end regression suite was executed against Samsung_S7_182:

```text
================================================================
KMAX Web Console: 17-Step End-to-End Streaming Regression Gate
Target: Samsung_S7_182 (192.168.1.182:5555)
================================================================
Connected to browser via CDP.

--- Phase 1: WebRTC Streaming & Control Verification ---
[Step 01] Device connects                    : PASS Mode=display, State=READY
[Step 02] WebRTC video READY                 : PASS 544x960
[Step 03] Touch DOWN/UP works                : PASS Coords=(1806.4, 612.8)
[Step 04] HOME works                         : PASS Title=HOME
[Step 05] BACK works                         : PASS Title=BACK
[Step 06] Keyboard/input works               : PASS Textarea input dispatched

--- Phase 2: WebRTC -> WebSocket Switch & CoreService Preservation ---
[Step 07] Switch WebRTC -> WebSocket         : PASS Title=Currently WebRTC, click to switch to WebSocket
[Step 08] CoreService remains alive          : PASS ps=shell 14994 app_process
[Step 09] WS video READY                     : PASS Canvas=544x960, Mode=websocket
[Step 10] WS touch works                     : PASS Coords=(1806.4, 612.8)
[Step 11] WS HOME/BACK works                 : PASS HOME & BACK executed

--- Phase 3: WebSocket -> WebRTC Switch Back ---
[Step 12] Switch WebSocket -> WebRTC         : PASS Title=Currently WebSocket, click to switch to WebRTC
[Step 13] WebRTC video returns               : PASS Video=544x960, Mode=display
[Step 14] Touch works again                  : PASS Coords=(1806.4, 612.8)

--- Phase 4: Teardown & Reopen Verification ---
[Step 15] Close device                       : PASS Closed via item-btn close-btn
Reopening Samsung_S7_182...
[Step 16] Reopen device                      : PASS Resolution=544x960
[Step 17] Video + control work               : PASS Touch & HOME confirmed after reopen

================================================================
REGRESSION GATE = PASS (17/17 STEPS)
================================================================
```

---

## 7. Reversibility Verification (Byte-for-Byte Round-Trip)

1. **Revert Execution**:
   `node scripts/ui/apply-ui-english.cjs --revert`
   Restored `public_bundle` and `dist_bundle` to exact V1 SHA:
   `334563779fbe10893c9b39c9ab0816df1f4c6656024fc36ae9baf01d4513200c`
2. **Re-Apply Execution**:
   `node scripts/ui/apply-ui-english.cjs`
   Committed `public_bundle` and `dist_bundle` to exact V2 SHA:
   `295a41f179bc05b94222abe5a9512b59851dfee67b0bb6a3c1ed166315c73f79`
3. **Verification**:
   `node scripts/ui/verify-ui-english.cjs` -> **All 6 gates PASS**.
