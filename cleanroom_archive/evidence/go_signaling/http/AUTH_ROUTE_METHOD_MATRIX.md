# Forensic Evidence: Auth Route HTTP Method Matrix

**Target**: `webrtc-signaling` (Linux AMD64 / Windows AMD64)  
**Scope**: `/api/login`, `/api/logout`, `/api/auth-status`, `/api/me` across 7 HTTP verbs  

---

| Route | Method | Status | Content-Type | Allow Header | Body Schema | Session Mutation |
|---|---|---|---|---|---|---|
| `/api/login` | `GET` | 405 | `text/plain; charset=utf-8` | *(none)* | `PLAIN_TEXT` | False |
| `/api/login` | `POST` | 200 | `application/json` | *(none)* | `['assigned_devices', 'role', 'token', 'username']` | True |
| `/api/login` | `PUT` | 405 | `text/plain; charset=utf-8` | *(none)* | `PLAIN_TEXT` | False |
| `/api/login` | `PATCH` | 405 | `text/plain; charset=utf-8` | *(none)* | `PLAIN_TEXT` | False |
| `/api/login` | `DELETE` | 405 | `text/plain; charset=utf-8` | *(none)* | `PLAIN_TEXT` | False |
| `/api/login` | `OPTIONS` | 200 | `` | *(none)* | `EMPTY` | False |
| `/api/login` | `HEAD` | 405 | `text/plain; charset=utf-8` | *(none)* | `EMPTY` | False |
| `/api/logout` | `GET` | 200 | `application/json` | *(none)* | `['status']` | False |
| `/api/logout` | `POST` | 200 | `application/json` | *(none)* | `['status']` | True |
| `/api/logout` | `PUT` | 200 | `application/json` | *(none)* | `['status']` | False |
| `/api/logout` | `PATCH` | 200 | `application/json` | *(none)* | `['status']` | False |
| `/api/logout` | `DELETE` | 200 | `application/json` | *(none)* | `['status']` | False |
| `/api/logout` | `OPTIONS` | 200 | `` | *(none)* | `EMPTY` | False |
| `/api/logout` | `HEAD` | 200 | `application/json` | *(none)* | `EMPTY` | False |
| `/api/auth-status` | `GET` | 200 | `application/json` | *(none)* | `['noAuth']` | False |
| `/api/auth-status` | `POST` | 200 | `application/json` | *(none)* | `['noAuth']` | False |
| `/api/auth-status` | `PUT` | 200 | `application/json` | *(none)* | `['noAuth']` | False |
| `/api/auth-status` | `PATCH` | 200 | `application/json` | *(none)* | `['noAuth']` | False |
| `/api/auth-status` | `DELETE` | 200 | `application/json` | *(none)* | `['noAuth']` | False |
| `/api/auth-status` | `OPTIONS` | 200 | `` | *(none)* | `EMPTY` | False |
| `/api/auth-status` | `HEAD` | 200 | `application/json` | *(none)* | `EMPTY` | False |
| `/api/me` | `GET` | 200 | `application/json` | *(none)* | `['ai_config', 'assigned_devices', 'expires_at', 'forbid_audio', 'forbid_bitrate', 'forbid_fps', 'forbid_resolution', 'role', 'settings', 'username']` | False |
| `/api/me` | `POST` | 200 | `application/json` | *(none)* | `['ai_config', 'assigned_devices', 'expires_at', 'forbid_audio', 'forbid_bitrate', 'forbid_fps', 'forbid_resolution', 'role', 'settings', 'username']` | False |
| `/api/me` | `PUT` | 200 | `application/json` | *(none)* | `['ai_config', 'assigned_devices', 'expires_at', 'forbid_audio', 'forbid_bitrate', 'forbid_fps', 'forbid_resolution', 'role', 'settings', 'username']` | False |
| `/api/me` | `PATCH` | 200 | `application/json` | *(none)* | `['ai_config', 'assigned_devices', 'expires_at', 'forbid_audio', 'forbid_bitrate', 'forbid_fps', 'forbid_resolution', 'role', 'settings', 'username']` | False |
| `/api/me` | `DELETE` | 200 | `application/json` | *(none)* | `['ai_config', 'assigned_devices', 'expires_at', 'forbid_audio', 'forbid_bitrate', 'forbid_fps', 'forbid_resolution', 'role', 'settings', 'username']` | False |
| `/api/me` | `OPTIONS` | 200 | `` | *(none)* | `EMPTY` | False |
| `/api/me` | `HEAD` | 200 | `application/json` | *(none)* | `EMPTY` | False |
