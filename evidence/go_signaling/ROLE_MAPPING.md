# Semantic Role Mapping: WebRTC Signaling Server

## Forensic Integrity Principles
- **Strict Package Provenance Separation**: Provenance (`STDLIB`, `GO_RUNTIME`, `THIRD_PARTY`, `PROJECT`, `UNKNOWN_PACKAGE`) is kept independent from `semantic_role`.
- **Zero Dependency Role Leakage**: Generic library methods (`String`, `MarshalText`, `ReadFrom`, `AcceptTCPWithConn`, etc.) are never misclassified as application controllers.
- **Multi-Class Evidence Requirement**: `CONFIRMED_ROLE` for application functions strictly requires >= 2 independent evidence classes.
- **Preserved Obfuscated Symbols**: All garbled symbols are preserved verbatim.

### Verified Summary Counts (Arithmetic Invariant Checked)
- **Total Functions Evaluated**: 7571
- **CONFIRMED_ROLE**: 1970
- **INFERRED_ROLE**: 37
- **UNKNOWN**: 5564
- **Sum Verification**: `1970 + 37 + 5564 == 7571` (PASS)

### Package Provenance Distribution
- **GO_RUNTIME**: 1490
- **PROJECT**: 300
- **STDLIB**: 432
- **UNKNOWN_PACKAGE**: 5349

### Confirmed Application & Project Roles (>= 2 Independent Evidence Classes)

| VA | Symbol Name | Provenance | Semantic Role | Conf | Evidence Classes |
|---|---|---|---|---|---|
| `0x6e0340` | `Y0caeZ_zze.MB_aa9i.ServeHTTP` | `PROJECT` | `STATIC_FILE_SERVER` | 0.98 | B: Route registration pointer from main.main closure table for '/downloads/'; E: Clean dynamic oracle confirmed route '/downloads/' is responsive |
| `0x736ae0` | `main.aOfaLG` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.95 | A: References 'users.json' persistence; C: References user admin credentials |
| `0x737880` | `main.w3H7BXxDC` | `PROJECT` | `DEVICE_TAGGING_AND_ORGANIZATION` | 0.95 | A: References 'device_tags.json' persistence; C: References deviceTags schema key |
| `0x73be00` | `main.kWD78W` | `PROJECT` | `DEVICE_SHARING_SUBMODULE` | 0.95 | A: References 'shares.json' persistence; C: References sharing protocol parameters |
| `0x73dd00` | `main.ltOjwqsMl5q8` | `PROJECT` | `AUTH_LOGIN_HANDLER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/login'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/login' is responsive |
| `0x73e7c0` | `main.ajyljXiIN8` | `PROJECT` | `USER_REGISTRATION_HANDLER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/register'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/register' is responsive |
| `0x73ec40` | `main.bwvBd1LWVr` | `PROJECT` | `AUTH_STATUS_HANDLER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/auth-status'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/auth-status' is responsive |
| `0x73f100` | `main.gJ0OHScnGnWZ` | `PROJECT` | `USER_PROFILE_HANDLER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/me'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/me' is responsive |
| `0x73ffc0` | `main.jc6UOob61gVD` | `PROJECT` | `AI_CONFIG_HANDLER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/user/ai-config'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/user/ai-config' is responsive |
| `0x7409a0` | `main.bjWkHiittd` | `PROJECT` | `AUTH_LOGOUT_AND_TOKEN_REVOCATION` | 0.98 | B: Route registration pointer from main.main closure table for '/api/logout'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/logout' is responsive |
| `0x740f40` | `main.sGuPXW2D` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/users/rename'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/users/rename' is responsive |
| `0x741ec0` | `main.eiuBQux8` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/users'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/users' is responsive |
| `0x7432a0` | `main.as5uExtX` | `PROJECT` | `ADMIN_DEVICE_ASSIGNMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/assign'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/assign' is responsive |
| `0x744140` | `main.zrTQTiT` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/users/create'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/users/create' is responsive |
| `0x744c20` | `main.m3nYlgst` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/users/update'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/users/update' is responsive |
| `0x745ba0` | `main._Wcin_o` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/users/delete'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/users/delete' is responsive |
| `0x7464e0` | `main.daDbGP` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/users/update_note'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/users/update_note' is responsive |
| `0x746e80` | `main.rmHttgOpxTKh` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/users/reset_password'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/users/reset_password' is responsive |
| `0x747880` | `main.eIddSiN_g` | `PROJECT` | `ADMIN_USER_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/admin/users/kick'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/admin/users/kick' is responsive |
| `0x748c20` | `main.(*OIR9dZw9ZyV).ServeHTTP` | `PROJECT` | `STATIC_WEB_ASSET_SERVER` | 0.98 | B: Route registration pointer from main.main closure table for '/'; E: Clean dynamic oracle confirmed route '/' is responsive |
| `0x74b6c0` | `main.jcraNgV8Jg` | `PROJECT` | `LICENSE_AND_ENTITLEMENT_MANAGER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/activate'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/activate' is responsive |
| `0x74bf60` | `main.yyDyfaokeO` | `PROJECT` | `LICENSE_AND_ENTITLEMENT_MANAGER` | 0.98 | B: Route registration pointer from main.main closure table for '/debug/license'; E: Clean dynamic oracle confirmed route '/debug/license' is responsive |
| `0x74c220` | `main.xdGI1n` | `PROJECT` | `LICENSE_AND_ENTITLEMENT_MANAGER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/license_status'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/license_status' is responsive |
| `0x74cf80` | `main.i2EgUTaLmQs` | `PROJECT` | `DEVICE_REGISTRY_AND_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/devices'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/devices' is responsive |
| `0x74da60` | `main.rXQMyuE` | `PROJECT` | `DEVICE_REGISTRY_AND_MANAGEMENT` | 0.98 | B: Route registration pointer from main.main closure table for '/api/devices/'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/devices/' is responsive |
| `0x74e4a0` | `main.rQffYkwYhw` | `PROJECT` | `DEVICE_REGISTRATION_HANDLER` | 0.98 | B: Route registration pointer from main.main closure table for '/register_device'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/register_device' is responsive |
| `0x7507c0` | `main.id8ybRmw69lm` | `PROJECT` | `WEBSOCKET_CLIENT_BRIDGE_HUB` | 0.98 | B: Route registration pointer from main.main closure table for '/connect_client'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/connect_client' is responsive |
| `0x754b40` | `main.jdUaLc5NMO5` | `PROJECT` | `WEBSOCKET_AGENT_REGISTRATION_HUB` | 0.98 | B: Route registration pointer from main.main closure table for '/register_agent'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/register_agent' is responsive |
| `0x758c80` | `main.swqKgLrjAZT9` | `PROJECT` | `FILE_TRANSMISSION_AND_TASK_MANAGER` | 0.98 | B: Route registration pointer from main.main closure table for '/upload'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/upload' is responsive |
| `0x75a2c0` | `main.qa3RvDW` | `PROJECT` | `FILE_TRANSMISSION_AND_TASK_MANAGER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/files'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/files' is responsive |
| `0x75afa0` | `main.koVbnsD4T0d` | `PROJECT` | `FILE_TRANSMISSION_AND_TASK_MANAGER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/tasks'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/tasks' is responsive |
| `0x75c240` | `main.cYYycnP3` | `PROJECT` | `DEVICE_SHARING_SUBMODULE` | 0.98 | B: Route registration pointer from main.main closure table for '/api/share/create'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/share/create' is responsive |
| `0x75d9a0` | `main._0VLCRLL` | `PROJECT` | `DEVICE_SHARING_SUBMODULE` | 0.98 | B: Route registration pointer from main.main closure table for '/api/share/list'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/share/list' is responsive |
| `0x75e5a0` | `main.nFuQn_o` | `PROJECT` | `DEVICE_SHARING_SUBMODULE` | 0.98 | B: Route registration pointer from main.main closure table for '/api/share/revoke'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/share/revoke' is responsive |
| `0x75ee20` | `main.d1oM4aHeERk4` | `PROJECT` | `DEVICE_SHARING_SUBMODULE` | 0.98 | B: Route registration pointer from main.main closure table for '/api/share/extend'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/share/extend' is responsive |
| `0x75fb20` | `main.nMFGdqfO` | `PROJECT` | `DEVICE_SHARING_SUBMODULE` | 0.98 | B: Route registration pointer from main.main closure table for '/api/share/update'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/share/update' is responsive |
| `0x760480` | `main.busbgD` | `PROJECT` | `DEVICE_SHARING_SUBMODULE` | 0.98 | B: Route registration pointer from main.main closure table for '/api/share/info'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/share/info' is responsive |
| `0x761a20` | `main.iSjKlH94xCO` | `PROJECT` | `DEVICE_SHARING_SUBMODULE` | 0.98 | B: Route registration pointer from main.main closure table for '/api/share/redeem_card'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/share/redeem_card' is responsive |
| `0x7632a0` | `main.vz0hZo0q1IzM` | `PROJECT` | `SERVER_CONFIGURATION_DISPATCHER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/server/addresses'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/server/addresses' is responsive |
| `0x763ec0` | `main.bhMId7t5J` | `PROJECT` | `FILE_TRANSMISSION_AND_TASK_MANAGER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/tasks/details'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/tasks/details' is responsive |
| `0x7647a0` | `main.main` | `PROJECT` | `APPLICATION_ENTRYPOINT_AND_ROUTER` | 1.00 | A: Disassembly contains 42 route registration strings; B: Entry point registers HTTP multiplexer; D: Calls net/http.ListenAndServe listener; E: Dynamic oracle verified server responds on configured port |
| `0x768500` | `main.vREP2EE2` | `PROJECT` | `ICE_SERVERS_CONFIGURATION` | 0.98 | B: Route registration pointer from main.main closure table for '/api/ice_servers'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/ice_servers' is responsive |
| `0x768980` | `main.j0yBBXR1Hjl` | `PROJECT` | `SERVER_CONFIGURATION_DISPATCHER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/default_settings'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/default_settings' is responsive |
| `0x769840` | `main.ys0CAJV5f5k` | `PROJECT` | `VERSION_INFO_DISPATCHER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/version'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/version' is responsive |
| `0x76ba00` | `main.gevbuZQhJ` | `PROJECT` | `DEVICE_TAGGING_AND_ORGANIZATION` | 0.95 | A: References 'device_tags.json' persistence; C: References deviceTags schema key |
| `0x76d200` | `main.main.func2` | `PROJECT` | `DEVICE_TAGGING_AND_ORGANIZATION` | 0.98 | B: Route registration pointer from main.main closure table for '/api/tags'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/tags' is responsive |
| `0x76d4c0` | `main.main.func3` | `PROJECT` | `SHORTCUT_SETTINGS_HANDLER` | 0.98 | B: Route registration pointer from main.main closure table for '/api/shortcuts'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/api/shortcuts' is responsive |
| `0x76da00` | `main.main.func5` | `PROJECT` | `SNAPSHOT_HANDLER` | 0.98 | B: Route registration pointer from main.main closure table for '/snapshots/'; A: Instruction xrefs contain matching domain parameters; E: Clean dynamic oracle confirmed route '/snapshots/' is responsive |

*Total Confirmed Project Roles: 48. Complete mapping in ROLE_MAPPING.json*
