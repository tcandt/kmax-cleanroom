# 01_ROUTE_MAP.md: Frontend Routing & Navigation Contracts

## 1. Overview & Router Architecture
- **Router Library**: `vue-router v4.6.4`
- **History Mode**: Hash-based history (`createWebHashHistory()`) to ensure zero reliance on backend server fallback rewriting.
- **Base URL**: `/#/`

---

## 2. Route Specifications

| Route Path | View / Component | Purpose / Responsibilities | Auth Guard / Role |
|:-----------|:-----------------|:---------------------------|:------------------|
| `/` | `Dashboard` (`DeviceMatrix.vue`) | Primary console view: Device matrix grid, online/offline statistics, search/filter bar, group control mode, display preferences, top navigation. | Required (`isLoggedIn`). Redirects to `/login` if unauthenticated. |
| `/login` | `Login.vue` | Standalone authentication page: username/password credentials, token exchange with `/api/login`, policy initialization. | Public. Redirects to `/` upon successful login. |
| `/deploy` | `DeployPage.vue` | Batch deployment matrix: APK installation, shell script execution across selected/grouped devices, task status logs. | Admin only (`isAdmin`). |
| `/monitor` | `Monitor.vue` | Cluster health & performance metrics: CPU, memory, FPS, network throughput graphs powered by ECharts. | Admin only (`isAdmin`). |
| `/advanced` | `AdvancedPage.vue` | System configuration, network proxies, COTURN/STUN parameters, agent daemon management. | Admin only (`isAdmin`). |
| `/share` | `ShareAdminPage.vue` / `ShareDevice.vue` | Guest access link management: token generation, permission toggles (read-only vs control), expiration timer. | Authenticated user / Admin. |

---

## 3. Sub-route & Modal Triggers (Hash / Query / Store State)

Rather than full page transitions, secondary management interfaces operate via reactive store state on the primary dashboard:

| Feature / Dialog | Trigger Mechanism | Target Store / State | Target Component |
|:-----------------|:------------------|:---------------------|:-----------------|
| Device Streaming View | Click device card / `ctrlKey + click` | `devices.focusedDeviceId` / `selectedDevice` | `DeviceClient.vue` (docked or overlay) |
| Multi-Device Control | Multi-select mode toggle | `devices.isMultiDeviceActive` | `MultiDeviceContainer.vue` |
| Tag Management | Topbar "Tags" button click | `devices.showTagManagerModal = true` | `TagManagerModal.vue` |
| Global Settings / Policy | Topbar "Settings" button click | `devices.showGlobalSettingsModal = true` | `SettingsModal.vue` / `UserPolicyModal.vue` |
| Connection Settings | Topbar / Context menu "Connection Settings" | `device.showConnectionSettingsModal = true` | `CardConnectModal.vue` (Video/Preview/Audio/Advanced tabs) |
| Display Preferences | "Display Options" dropdown button | Local state popover | Resolution scale, FPS limit, direct preview interaction |

---

## 4. Navigation Guards & Parity Invariants
1. **Unauthenticated Redirection**: If `!token.value && !noAuthMode.value`, navigation to any route other than `/login` must redirect to `#/login`.
2. **Hash Stability**: Route transitions must not reload the page or trigger disconnect on active WebRTC peer connections unless explicitly commanded.
3. **Session Persistence**: Auth tokens (`auth_token`), usernames (`auth_user`), and roles (`auth_role`) are persisted in `localStorage`.
