# 02_STORE_CONTRACTS.md: Pinia State Management Contracts

## 1. Store Architecture
- **State Framework**: `Pinia v2.3.1` using Vue 3 Composition API (`defineStore(id, () => { ... })`).
- **Persistence**: Hybrid in-memory reactivity + `localStorage` synchronization for view preferences and credentials.

---

## 2. Store Specifications

### 2.1 `useAuthStore` (`id: 'auth'`)
Manages authentication token, user identity, permissions, and policy restrictions.

* **State**:
  * `token`: `ref<string>` (from `localStorage.getItem('auth_token')`)
  * `username`: `ref<string>` (from `localStorage.getItem('auth_user')`)
  * `role`: `ref<'admin' | 'user'>` (from `localStorage.getItem('auth_role')`)
  * `assignedDevices`: `ref<string[]>` (IDs of devices accessible by this user)
  * `noAuthMode`: `ref<boolean>` (enabled in demo/local offline mode)
  * `userPolicy`: `ref<Object | null>` (policies returned by `/api/me`, e.g. `forbid_bitrate`, `forbid_fps`, `forbid_resolution`)
* **Computed**:
  * `isLoggedIn`: `computed(() => noAuthMode.value || !!token.value)`
  * `isAdmin`: `computed(() => noAuthMode.value || role.value === 'admin')`
* **Actions**:
  * `login(username, password)`: POST to `/api/login`, updates reactive state & `localStorage`.
  * `logout()`: Clears reactive state & `localStorage`, redirects to `#/login`.
  * `fetchMe()`: GET `/api/me` to refresh assigned devices and policy flags.

---

### 2.2 `useDeviceStore` (`id: 'devices'`)
Primary state coordinator for device matrix, stream registration, telemetry, and connection modes.

* **State**:
  * `devices`: `ref<Device[]>` (all registered cloud devices)
  * `loading`: `ref<boolean>`
  * `error`: `ref<string | null>`
  * `deviceModes`: `ref<Record<string, 'display' | 'websocket'>>` (active streaming protocol per device)
  * `searchQuery`: `ref<string>` (matrix search filter)
  * `cardSize`: `ref<number>` (matrix card zoom: 150px - 350px, default 200px)
  * `viewMode`: `ref<'grid' | 'table'>`
  * `focusedDeviceId`: `ref<string | null>`
  * `licenseMaxDevices`: `ref<number>`
  * `licenseCurrentDevices`: `ref<number>`
  * `licenseStatus`: `ref<'valid' | 'expired' | 'promo'>`
* **Computed**:
  * `onlineDevices`: `computed(() => devices.value.filter(d => d.status === 'online').sort((a,b) => a.id.localeCompare(b.id)))`
  * `offlineDevices`: `computed(() => devices.value.filter(d => d.status !== 'online'))`
  * `licenseUsedCount`: `computed(() => licenseCurrentDevices.value || onlineDevices.value.length)`
* **Actions**:
  * `fetchDevices()`: Polls or receives `/api/devices` status updates.
  * `setDeviceMode(deviceId, mode)`: Sets `'display'` (WebRTC) or `'websocket'` for `deviceId`. Mirrored to `window.__deviceModes`.
  * `getDeviceMode(deviceId)`: Returns active streaming mode (default `'display'`).
  * `registerWebRTC(deviceId, rtcInstance)`: Registers active WebRTC composable handle.
  * `unregisterWebRTC(deviceId)`: Unregisters handle upon component unmount.
  * `closeDevice(deviceId)`: Terminates active stream view and cleans up held sessions.

---

### 2.3 `useTagStore` (`id: 'deviceTags'`)
Device grouping, labeling, and batch selection filter management.

* **State**:
  * `tags`: `ref<Tag[]>` (`{ id: string, name: string, color: string }`)
  * `deviceTags`: `ref<Record<string, string[]>>` (mapping deviceId -> array of tag IDs)
  * `selectedTagIds`: `ref<string[]>` (active filter tags)
* **Computed**:
  * `tagMap`: `computed(() => new Map(tags.value.map(t => [t.id, t])))`
* **Actions**:
  * `createTag(name, color)`: Generates tag ID and persists to `localStorage`.
  * `deleteTag(id)`: Removes tag and detaches from all devices.
  * `toggleFilterTag(id)`: Filters device matrix by selected tags.
  * `assignTags(deviceId, tagIds)`: Replaces tags associated with `deviceId`.

---

## 3. Invariants
- `deviceModes` must synchronize with `window.__deviceModes` to ensure non-Vue test scripts and telemetry hooks read the authoritative mode.
- Store actions must never invoke destructive `disconnect()` on WebRTC instances during a WebRTC-to-WS switch (enforcing the `[WebRTC-HOLD]` contract).
