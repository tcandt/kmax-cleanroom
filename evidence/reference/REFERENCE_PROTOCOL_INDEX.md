# Reference Protocol Index (Public Frontend & Documentation)

**Evidence Class**: `SOURCE_REFERENCE_CANDIDATE`  
**Upstream References**:  
- `tcandt/scrcpyoverwebrtc` (commit: `65567d777bccb11d2a6d93b6acc735478e880b5b`)
- `hqw700/cloudphone-official` (commit: `ceb66b20ad4c6f7b217d38852ea9ec2bd70fcd39`)

> [!IMPORTANT]
> All items in this document represent **hypotheses and candidates** derived from the public reference frontend and documentation. No implementation code is copied into cleanroom source. Every item must be corroborated against original binary static evidence before backend code reconstruction.

## 1. Transport Endpoints

### WebSocket Routes
| Endpoint | Direction / Role | Query Parameters | Source Reference |
|---|---|---|---|
| `/connect_client` | Client signaling | `?token=`, `?share_token=`, `?share_pwd=` | `useWebRTC.js:78-83`, `devices.js:669` |
| `/register_agent` | Agent upstream connection | `?id=<agent_id>` | `agent-deploy.md`, `DEVELOPMENT.md` |

### HTTP Endpoints
| Method | Path | Role & Functional Description |
|---|---|---|
| `POST` | `/api/login` | Authentication: credentials login and session token issuance |
| `ANY` | `/api/logout` | Authentication: session revocation |
| `ANY` | `/api/auth-status` | Authentication: check whether noAuth mode is active |
| `ANY` | `/api/me` | Authentication: retrieve authenticated user profile |
| `GET` | `/api/devices` | Device: list active and registered devices |
| `GET/POST/DELETE` | `/api/devices/` | Device: manage specific device by ID |
| `GET/POST/PUT/DELETE` | `/api/tags` | Tags: manage device categories and label associations |
| `GET` | `/api/admin/users` | Admin: list user accounts |
| `POST` | `/api/admin/users/create` | Admin: create new user account |
| `POST` | `/api/admin/users/update` | Admin: update account properties / expiration |
| `POST` | `/api/admin/users/delete` | Admin: remove user account |
| `POST` | `/api/admin/users/reset_password` | Admin: reset user password |
| `POST` | `/api/admin/users/rename` | Admin: rename user account |
| `POST` | `/api/admin/users/update_note` | Admin: update user note field |
| `POST` | `/api/admin/users/kick` | Admin: kick active user sessions |
| `POST` | `/api/admin/assign` | Admin: assign device permissions to user |
| `POST` | `/api/share/create` | Share: create temporary sharing link for device |
| `GET` | `/api/share/list` | Share: list active share tokens |
| `POST` | `/api/share/revoke` | Share: revoke share token |
| `POST` | `/api/share/extend` | Share: extend share token lifetime |
| `POST` | `/api/share/update` | Share: update share token properties |
| `GET` | `/api/share/info` | Share: fetch metadata for shared device |
| `POST` | `/api/share/redeem_card` | Share: redeem card code for device access |
| `GET/POST` | `/api/default_settings` | Config: global default settings (bitrate, fps, etc.) |
| `GET/POST` | `/api/ice_servers` | Config: STUN/TURN server list |
| `GET` | `/api/server/addresses` | Config: query external server IPs |
| `GET/POST` | `/api/shortcuts` | Config: keyboard shortcut mappings |
| `GET` | `/api/version` | System: signaling server version |
| `GET` | `/api/license_status` | System: query license status |
| `POST` | `/api/activate` | System: apply license key |
| `GET/DELETE` | `/api/files` | Files: file management listing and deletion |
| `GET/POST` | `/api/tasks` | Tasks: batch task execution |
| `GET` | `/api/tasks/details` | Tasks: query task execution status |
| `GET/POST` | `/api/user/ai-config` | User: AI assistant integration settings |
| `POST` | `/upload` | Upload: file/APK upload endpoint |
| `GET` | `/downloads/` | Static: agent executable / APK downloads |
| `GET` | `/snapshots/` | Static: device screenshot thumbnail serving |

## 2. WebSocket Signaling Messages (`message_type`)

### Client-to-Server Messages
| message_type | Required / Optional Fields | Functional Description | Source |
|---|---|---|---|
| `connect` | `message_type`, `device_id` | Sent by client immediately after WebSocket connection to target device session | `web-app/src/composables/useWebRTC.js:92-95` |
| `forward` | `message_type`, `device_id`, `payload` | Wraps signaling payloads (request-offer, answer, ice-candidate) forwarded to Agent | `web-app/src/composables/useWebRTC.js:140` |
| `command` | `message_type`, `device_id`, `request_id`, `command` | Direct shell/command execution request forwarded to agent via signaling server | `web-app/src/composables/useWebRTC.js:271-276` |
| `inject_data` | `message_type`, `device_id`, `channel`, `payload`, `target_device_ids` | Injects touch/input/clipboard data into agent channel via signaling fallback or multicast | `web-app/src/composables/useWebRTC.js:253-262, web-app/src/stores/devices.js:610` |
| `group_control_event` | `message_type`, `origin_device_id`, `target_device_ids`, `event` | Multicast batch control event replicated across group of target devices | `web-app/src/stores/devices.js:593` |
| `action` | `message_type`, `device_id`, `fps`, `max_size`, `bitrate`, `stay_awake` | Controls H.264 preview stream generation on agent | `web-app/src/stores/devices.js:573` |
| `quit_agent` | `message_type`, `device_id` | Requests signaling server to instruct agent to terminate | `web-app/src/stores/devices.js:787` |

### Server-to-Client Messages
| message_type | Payload Content | Functional Description | Source |
|---|---|---|---|
| `config` | `message_type`, `ice_servers` | Server acknowledges connect request and provides STUN/TURN ICE configuration | `web-app/src/composables/useWebRTC.js:126-131` |
| `device_info` | `message_type`, `device_info` | Provides agent version, screen resolution, and hardware display metadata | `web-app/src/composables/useWebRTC.js:142, 158-169` |
| `device_msg` | `message_type`, `payload` | Encapsulates messages routed from Agent to Browser (offer, ice-candidate, command_result, scrcpy_error) | `web-app/src/composables/useWebRTC.js:145-147, 171-249` |
| `screenshot_response` | `message_type`, `data` | Returns raw screenshot captured from device display | `web-app/src/composables/useWebRTC.js:148-150` |
| `error` | `message_type`, `error` | Notifies client of server-side or device connection error | `web-app/src/composables/useWebRTC.js:151-154` |
| `snapshot_update` | `message_type`, `device_id`, `timestamp` | Broadcast notification that device thumbnail snapshot has refreshed | `web-app/src/stores/devices.js:682` |
| `device_list_update` | `message_type`, `devices` | Broadcast notification of online/offline status changes across device inventory | `web-app/src/stores/devices.js:690` |
| `tags_update` | `message_type`, `tags` | Broadcast notification of modified device tags and categories | `web-app/src/stores/devices.js:692` |
| `task_status_updated` | `message_type`, `task_id`, `status`, `progress` | Broadcast notification of progress updates on background asynchronous batch tasks | `web-app/src/stores/devices.js:697` |
| `license_update` | `message_type`, `license` | Broadcast notification of license entitlement updates | `web-app/src/stores/devices.js:706` |

## 3. Signaling Forward Payloads (`device_msg` & `forward`)

| Payload `type` | Direction | Content / Parameters | Functional Purpose |
|---|---|---|---|
| `request-offer` | Browser -> Signaling -> Agent | `type`, `ip_preference`, `scrcpy_options` | Client triggers Agent to generate and initiate an SDP offer with desired codec/options |
| `offer` | Agent -> Signaling -> Browser | `type`, `sdp`, `camera_support` | Agent presents WebRTC offer containing H.264 video track and media parameters |
| `answer` | Browser -> Signaling -> Agent | `type`, `sdp` | Browser accepts offer and submits SDP answer to negotiate P2P media session |
| `ice-candidate` | Bi-directional (Browser <-> Signaling <-> Agent) | `type`, `candidate` | Trickle ICE candidate exchange to discover viable STUN/TURN host/srflx/relay network pairs |
| `command_result` | Agent -> Signaling -> Browser | `type`, `request_id`, `output`, `exit_code` | Returns execution output and exit status of shell command dispatched to agent |
| `scrcpy_error` | Agent -> Signaling -> Browser | `type`, `message` | Reports failure in starting scrcpy-server or camera HAL initialization |
