# Semantic Role Mapping: WebRTC Signaling Server

## Forensic Integrity Principles
- **Zero Stdlib Misattribution**: Standard library and Go runtime functions are classified under runtime/stdlib categories and never assigned application roles.
- **Evidence Provenance**: Every application role is tied directly to instruction xrefs, route registration disassembly, or string tokens.
- **Garbled Symbols Preserved**: All obfuscated symbols are preserved verbatim.

### Classification Summary
- **Total Functions Evaluated**: 7571
- **CONFIRMED_ROLE**: 1982
- **INFERRED_ROLE**: 0
- **UNKNOWN**: 11178

| VA | Symbol Name | Role | Classification | Confidence | Evidence |
|---|---|---|---|---|---|
| `0x589820` | `xLZFT3Ek4bwX.(*kdYa7i).Set` | `DEVICE_TAGGING_AND_ORGANIZATION` | `CONFIRMED_ROLE` | 0.90 | Direct reference to /api/tags and device_tags.json |
| `0x6ac6e0` | `Y0caeZ_zze.ombt6RC6kde` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x735400` | `main.J_5lH4w6CU` | `LICENSE_AND_ENTITLEMENT_MANAGER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to license activation and machine_id verification |
| `0x736ae0` | `main.aOfaLG` | `ADMIN_USER_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to admin user management and users.json persistence |
| `0x737880` | `main.w3H7BXxDC` | `DEVICE_TAGGING_AND_ORGANIZATION` | `CONFIRMED_ROLE` | 0.90 | Direct reference to /api/tags and device_tags.json |
| `0x73a580` | `main.cFpPBbFet.func1` | `AUTH_LOGOUT_AND_TOKEN_REVOCATION` | `CONFIRMED_ROLE` | 0.98 | Direct reference to /api/logout and token revocation |
| `0x73dd00` | `main.ltOjwqsMl5q8` | `AUTH_LOGIN_HANDLER` | `CONFIRMED_ROLE` | 0.98 | Direct reference to /api/login and credential verification |
| `0x73e7c0` | `main.ajyljXiIN8` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x73ec40` | `main.bwvBd1LWVr` | `AUTH_STATUS_HANDLER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/auth-status |
| `0x73ffc0` | `main.jc6UOob61gVD` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x7409a0` | `main.bjWkHiittd` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x740f40` | `main.sGuPXW2D` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x7432a0` | `main.as5uExtX` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x744140` | `main.zrTQTiT` | `AUTH_LOGIN_HANDLER` | `CONFIRMED_ROLE` | 0.98 | Direct reference to /api/login and credential verification |
| `0x744c20` | `main.m3nYlgst` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x745ba0` | `main._Wcin_o` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x7464e0` | `main.daDbGP` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x746e80` | `main.rmHttgOpxTKh` | `AUTH_LOGIN_HANDLER` | `CONFIRMED_ROLE` | 0.98 | Direct reference to /api/login and credential verification |
| `0x747880` | `main.eIddSiN_g` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x74b4e0` | `main.hPaJPN` | `LICENSE_AND_ENTITLEMENT_MANAGER` | `CONFIRMED_ROLE` | 0.95 | Direct reference to license activation and machine_id verification |
| `0x74b6c0` | `main.jcraNgV8Jg` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x74da60` | `main.rXQMyuE` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x74e4a0` | `main.rQffYkwYhw` | `ADMIN_USER_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to admin user management and users.json persistence |
| `0x758c80` | `main.swqKgLrjAZT9` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x75afa0` | `main.koVbnsD4T0d` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x75c240` | `main.cYYycnP3` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x75e5a0` | `main.nFuQn_o` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x75ee20` | `main.d1oM4aHeERk4` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x75fb20` | `main.nMFGdqfO` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x760480` | `main.busbgD` | `AUTH_LOGIN_HANDLER` | `CONFIRMED_ROLE` | 0.98 | Direct reference to /api/login and credential verification |
| `0x761a20` | `main.iSjKlH94xCO` | `AUTH_LOGIN_HANDLER` | `CONFIRMED_ROLE` | 0.98 | Direct reference to /api/login and credential verification |
| `0x769d40` | `main.bFT5Enmzua` | `DEVICE_TAGGING_AND_ORGANIZATION` | `CONFIRMED_ROLE` | 0.90 | Direct reference to /api/tags and device_tags.json |
| `0x76a4c0` | `main.k7fAFNISQp_m` | `DEVICE_REGISTRY_AND_MANAGEMENT` | `CONFIRMED_ROLE` | 0.95 | Direct reference to /api/devices and device state management |
| `0x76ba00` | `main.gevbuZQhJ` | `DEVICE_TAGGING_AND_ORGANIZATION` | `CONFIRMED_ROLE` | 0.90 | Direct reference to /api/tags and device_tags.json |

*Total Project Identified Roles: 34. Complete mapping in ROLE_MAPPING.json*
