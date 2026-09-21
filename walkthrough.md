# Phase E — English UI Normalization Walkthrough

## 1. Executive Summary
- **Objective**: Complete presentation normalization of KMAX Web Console to natural, professional English without introducing runtime i18n frameworks (`vue-i18n`), client state machines, or language switchers, while preserving all streaming, signaling, CoreService-hold, and input control logic from commit `e44dd2d`.
- **Status**: **ALL GATES PASS (100%)**.
- **A/B Runtime Regression**: Identical 17-step end-to-end streaming & control test suite executed on both pre-English baseline and post-English patch: **17/17 PASS on both runs**.
- **Reversibility**: `--revert` verified byte-for-byte SHA256 equality against baseline.
- **Visual Sweep**: 14 views and modals inspected for English naturalness and remaining secondary CJK boundaries.

---

## 2. Invariants & Phase E Acceptance Gates
- **Production Source of Truth**: All operations were conducted against `reconstructed_source/web-app/public/assets/index-DIPw8r74.js` as the sole source of truth.
- **Frozen Pre-English Baseline Hashes**:
  - `PRE_ENGLISH_SHA256_PUBLIC`: `18d6b4b260551dcf5662904f406172c38a86dfcdd35d5a01255a18d855ede168`
  - `PRE_ENGLISH_SHA256_DIST`: `18d6b4b260551dcf5662904f406172c38a86dfcdd35d5a01255a18d855ede168`
  - `PRE_ENGLISH_SHA256_INDEX_HTML`: `25c662ab2f1dcbd0b6f785589aff4faecb8d7ac2a71f72d25e2e246151923bac`
  - `PRE_ENGLISH_SHA256_DIST_INDEX_HTML`: `c5fe9f0240b96e8a457ef46348250e8a274a068556b40b8502b7f8d6385706ad`
- **Committed Post-English Normalization Hashes**:
  - `POST_ENGLISH_SHA256_PUBLIC`: `334563779fbe10893c9b39c9ab0816df1f4c6656024fc36ae9baf01d4513200c`
  - `POST_ENGLISH_SHA256_DIST`: `334563779fbe10893c9b39c9ab0816df1f4c6656024fc36ae9baf01d4513200c`
  - `POST_ENGLISH_SHA256_INDEX_HTML`: `e8bf81547b05e8ed73783cbcae9f9aeb43f923577789d8e8a65e603967228b85`
  - `POST_ENGLISH_SHA256_DIST_INDEX_HTML`: `babb7c96410b962c3197a7849dd09e464b36ac2cfc2fe9e9d586914426ca01be`

---

## 3. Category C Protected Literal Integrity Snapshot
To ensure zero regression of streaming lifecycles, WebRTC DataChannels, touch mapping, or CoreService hold logic, 21 protected literals were tracked before and after transformation with exact count equality enforced:

| Index | Protected Literal | Before Count | After Count | Integrity Status |
|:-----:|:------------------|:------------:|:-----------:|:----------------:|
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

## 4. Phase E3 Engine Implementation
- **Script**: [`scripts/ui/apply-ui-english.cjs`](file:///d:/KMAX-CLEANROOM/scripts/ui/apply-ui-english.cjs)
- **Transactional Protocol**:
  ```text
  APPLY
    read all targets
    ↓
  validate all input SHA
    ↓
  validate 80/80 anchors & UNCLASSIFIED = 0
    ↓
  validate 21/21 protected literals snapshot
    ↓
  perform transformations in memory
    ↓
  syntax validation (node --input-type=module --check)
    ↓
  write *.tmp
    ↓
  atomic rename
  ```
- **Execution Modes**:
  - `--dry-run`: Full in-memory verification and post-hash calculation with `WRITE FILES = 0`. Verified PASS.
  - Live apply: Atomic rename commit across `public`, `dist`, and `index.html`.
  - `--revert`: Inverts transformations, validates syntax, asserts byte-for-byte equality to `PRE_ENGLISH_SHA256_*`, and atomically renames. Tested and verified 100% reversible.

---

## 5. Phase E4 Verification Results
- **Script**: [`scripts/ui/verify-ui-english.cjs`](file:///d:/KMAX-CLEANROOM/scripts/ui/verify-ui-english.cjs)
- **Verification Gates**:
  1. Post-English SHA256 Hashes: **PASS** (all 4 files matched predicted hashes).
  2. Protected Literal Exact Counts: **PASS** (21/21 counts intact).
  3. Replacement Rule Integrity: **PASS** (71/71 rules verified; 0 Chinese residue, 1 English match each).
  4. HTML Normalization: **PASS** (`<html lang="en">` verified; `lang="zh-CN"` absent).
  5. Transformed JS Syntax: **PASS** (`node --input-type=module --check` exit code 0).
  6. Inventory Classification Audit: **PASS** (807/807 accounted for; `UNCLASSIFIED = 0`).

---

## 6. Phase E5: A/B Runtime Streaming Regression Results
The standardized 17-step runtime regression test suite [`scripts/test-regression-flow.cjs`](file:///d:/KMAX-CLEANROOM/scripts/test-regression-flow.cjs) was executed twice under identical conditions:

| Step # | Test Step Name | Pre-English Run (`e44dd2d`) | Post-English Run (Phase E Patch) |
|:------:|:---------------|:---------------------------:|:--------------------------------:|
| 01 | Device connects | **PASS** (Mode=display, State=READY) | **PASS** (Mode=display, State=READY) |
| 02 | WebRTC video READY | **PASS** (544x960, live) | **PASS** (544x960, live) |
| 03 | Touch DOWN/UP works | **PASS** (dispatched) | **PASS** (dispatched) |
| 04 | HOME works | **PASS** (Title=HOME) | **PASS** (Title=HOME) |
| 05 | BACK works | **PASS** (Title=BACK) | **PASS** (Title=BACK) |
| 06 | Keyboard/input works | **PASS** (Textarea input dispatched) | **PASS** (Textarea input dispatched) |
| 07 | Switch WebRTC → WebSocket | **PASS** (Title="当前为 WebRTC 直连...") | **PASS** (Title="Currently WebRTC...") |
| 08 | CoreService remains alive | **PASS** (PID alive in `ps`) | **PASS** (PID alive in `ps`) |
| 09 | WS video READY | **PASS** (Canvas 544x960, Mode=websocket) | **PASS** (Canvas 544x960, Mode=websocket) |
| 10 | WS touch works | **PASS** (Canvas touch injected) | **PASS** (Canvas touch injected) |
| 11 | WS HOME/BACK works | **PASS** (Executed) | **PASS** (Executed) |
| 12 | Switch WebSocket → WebRTC | **PASS** (Title="当前为 WebSocket 投屏...") | **PASS** (Title="Currently WebSocket...") |
| 13 | WebRTC video returns | **PASS** (Video 544x960, Mode=display) | **PASS** (Video 544x960, Mode=display) |
| 14 | Touch works again | **PASS** (dispatched) | **PASS** (dispatched) |
| 15 | Close device | **PASS** (Closed cleanly) | **PASS** (Closed cleanly) |
| 16 | Reopen device | **PASS** (544x960 stream attached) | **PASS** (544x960 stream attached) |
| 17 | Video + control work | **PASS** (Touch & HOME confirmed) | **PASS** (Touch & HOME confirmed) |
| **Result** | **Overall Gate Status** | **PRE-TRANSLATION: PASS** | **POST-TRANSLATION: PASS** |

---

## 7. UI Visual Sweep Audit & Natural English Assessment

A comprehensive visual inspection of the live web application (`http://localhost:3111/`) was conducted across all operational flows, dialogs, and navigation routes.

### 7.1 Verified Natural English Elements (Phase E Primary Scope)
- **Application Shell & Document Metadata**:
  - `lang`: `"en"`
  - `title`: `"Cloud Phone"`
- **Primary Sidebar Navigation**:
  - `Cloud Phone`, `Devices`, `Dashboard`, `Group Control`, `Files`, `Deploy`, `Terminal`, `Peripherals`, `Share`, `Settings`, `Sign out`, `Tags`, `Manage`, `All devices`, `Recently added`, `Offline devices`, `Share & License Management`, `v0.3.6 (2693ef1)`.
- **License / Subscription Notice**:
  - `"Promotion · 13/20 devices"` (clean, idiomatic English).
- **DeviceClient Remote Streaming Toolbar**:
  - Navigation & System keys: `Back`, `Home`, `Recent Tasks`, `Power`, `Volume Up`, `Volume Down`.
  - Media & Layout toggles: `Rotate`, `Resolution`, `Add Shortcut`, `Settings`, `Close`.
  - Bidirectional Mode Switch Tooltips:
    - `"Currently WebRTC direct connection, click to switch to WebSocket stream"`
    - `"Currently WebSocket stream, click to switch to WebRTC direct connection"`
  - Diagnostics: `E2E ~38ms`, `JB 22ms`, `RTT 5ms`, `SRC 0 | RX 0 | DEC 0 | PRES 0`.
- **Connection Error / Recovery States**:
  - Retry button: `"Retry"`.

### 7.2 Quality Assessment: Natural English vs Literal Translation
- All 71 mapped replacement rules use idiomatic, industry-standard Android control terms (`Recent Tasks` rather than literal "Recent", `Add Shortcut` rather than "Add Key", `Switch to WebSocket stream` rather than "Switch WebSocket Screen Projection").
- No grammatical, syntactic, or character rendering defects observed.

### 7.3 Preserved Boundaries & Remaining Chinese Strings (Future Phase Scope)
As defined in the Phase E plan, modifications were strictly bounded to avoid touching unverified code paths that could risk streaming or data structures:
- **Matrix View Topbar**: `云虚机矩阵` ("Cloud Phone Matrix"), `13 台在线` ("13 Online"), `显示选项 ▾` ("Display Options ▾"), `多机直连 (1) ✕` ("Multi-device Direct Connect ✕"), `群控` ("Group Control"), `标签` ("Tags"), `设置` ("Settings"), `管理员` ("Administrator").
- **Card Hover Overlay**: `进入控制` ("Control" / "Enter Control").
- **Secondary Multi-Device Toolbar**: `添加虚机` ("Add Device"), `平铺` ("Tile"), `浮窗` ("Float"), `焦点独占` ("Exclusive Focus"), `群控主控` ("Master Control"), `终端` ("Terminal").
- **Management Dialogs** (e.g. User Permission Modal triggered via Settings): `用户权限管理`, `+ 新建用户`, `用户名`, `角色`, `在线状态`, `有效期`, `已分配设备`, `当前控制`, `备注`, `操作`.

These strings remain safely accounted for in Category A of `ui-english-map.json` (727 strings) and can be mapped in future UI polish phases.

---

## 8. Final Git Review & Release Checkpoint

### 8.1 Modified & Untracked Files Review
```text
Modified:
  reconstructed_source/web-app/index.html                     (html lang="en")
  reconstructed_source/web-app/public/assets/index-DIPw8r74.js (production JS bundle)
  scripts/click-retry.cjs                                     (hardened bilingual selector)
  scripts/test-find-ws-btn.cjs                                (hardened bilingual selector)
  scripts/test-switch-back.cjs                                (hardened bilingual selector)

Untracked:
  scripts/test-regression-flow.cjs                            (17-step A/B regression suite)
  scripts/ui/apply-ui-english.cjs                             (transactional patch engine)
  scripts/ui/verify-ui-english.cjs                            (static verification engine)
  scripts/ui/ui-english-map.json                              (807-string inventory & 71 rules)
  walkthrough.md                                              (Phase E documentation)
```
- Zero temporary or debug scratch files are staged.
- Working tree is clean and scoped exactly to Phase E deliverables.

### 8.2 Checkpoint Commit & Tag
- **Commit Message**:
  ```text
  feat(ui): normalize KMAX web console to English with regression-safe patching

  - add transactional English UI normalization engine
  - preserve WebRTC/WS/CoreService protected literals
  - harden regression selectors
  - add reversible SHA-verified patch/revert flow
  - verify 17/17 pre/post streaming regression
  - normalize html lang to en
  ```
- **Tag**: `phase-e-english-ui-v1`
