# 06_COMPONENT_INVENTORY.md: Reconstructed Component Hierarchy & Responsibilities

## 1. Executive Summary
This document categorizes all UI components identified in the production bundle `index-DIPw8r74.js`, mapping them into a clean, modular component tree for reconstructed source development across Phases F1–F3.

---

## 2. Component Taxonomy & Inventory

### 2.1 Core Application Shell & Navigation
* **`App.vue`**: Top-level application wrapper, router viewport mount, global notification toast provider.
* **`Login.vue`**: Authentication form (username, password, token exchange).

---

### 2.2 Primary Views
* **`views/DeviceMatrix.vue`** (`Dashboard`):
  * Header bar: Online count badge, promotion quota badge, search input (`⌘K`), Display Options dropdown, Group Control button, Tags button, Settings button, User profile badge.
  * Device grid / table: Renders responsive cards (`DeviceCard.vue`) or rows (`DeviceListItem.vue`).
  * Empty state & loading skeleton.
* **`views/DeviceClient.vue`**:
  * Single-device remote control viewport.
  * WebRTC `<video>` and WebSocket `<canvas>` stream surfaces.
  * Floating / docked toolbar: Power, Home, Back, Volume, Mute, Terminal, Keymap, Clipboard, Stream mode switch, Disconnect.
  * Stream telemetry HUD: Bitrate, FPS, RTT, jitter, resolution.
* **`views/DeployPage.vue`**: Batch APK installer and shell task runner.
* **`views/Monitor.vue`**: ECharts cluster performance telemetry.
* **`views/AdvancedPage.vue`**: System daemon configurations and COTURN/STUN parameters.
* **`views/ShareAdminPage.vue`**: Share link management table.

---

### 2.3 Multi-Device Workspace (`components/multi/`)
* **`MultiDeviceContainer.vue`**: Multi-device manager mounted when multiple devices are selected.
  * **`MultiGridTiling.vue`**: Grid tiling layout for multi-device view.
  * **`MultiTabsView.vue`**: Tabbed layout with pill close buttons (`×`).
  * **`MultiFloatingWorkspace.vue`**: Draggable, resizable floating windows.
  * **`MultiDeviceItem.vue`**: Individual device stream instance in multi-view.

---

### 2.4 Modals & Configuration Dialogs (`components/modals/`)
* **`CardConnectModal.vue`** (*Connection Settings*):
  * **Video Tab**: Max resolution, FPS limits, bitrate, BWE congestion control toggle.
  * **Thumbnail Preview Tab**: Preview resolution and JPEG quality.
  * **Audio Tab**: Audio stream toggle and codec settings.
  * **Advanced Tab**: ICE candidate pool, turn credentials, hardware decoding flags.
* **`TagManagerModal.vue`** (*Device Tags*):
  * Tag list with color chips.
  * New tag name input and submit button (`Add`).
  * Batch device tag assignment.
* **`SettingsModal.vue` / `UserPolicyModal.vue`** (*User Permissions / Settings*):
  * User roles, password reset, permission policy flags.
* **`KeymapEditor.vue`**: Game / app key mapping overlay onto touch coordinates.
* **`ScreenshotModal.vue`**: Frame capture preview and download.
* **`ShareModal.vue`**: Create guest access links with expiry.
* **`LicensePanel.vue`**: Machine ID display, license key activation form, quota usage indicator.

---

## 3. Phased Implementation Roadmap
* **Phase F1**: Composables (`useWebRTC.js`, `useWebSocketStream.js`) & Stores (`devices.js`, `auth.js`, `tags.js`).
* **Phase F2**: `DeviceClient.vue` (Single device streaming, controls, telemetry).
* **Phase F3A**: Shell & Router (`App.vue`, `main.js`, `router/index.js`, `Login.vue`).
* **Phase F3B**: Device Matrix (`DeviceMatrix.vue`, `DeviceCard.vue`).
* **Phase F3C**: Dialogs & Settings (`CardConnectModal.vue`, `TagManagerModal.vue`, `SettingsModal.vue`).
* **Phase F3D**: Secondary Pages (`DeployPage.vue`, `ShareAdminPage.vue`, `Monitor.vue`).
