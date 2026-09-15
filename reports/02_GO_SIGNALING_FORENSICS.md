# Forensic Report 02: WebRTC Signaling Server Reverse Engineering (Phase 1B / Phase 2 Remediation)

## 1. Scope & Execution Parameters
- **Primary Binary Analyzed**: `cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling` (ELF 64-bit x86-64, size 8,417,428 bytes, SHA256: `6865f05fe59838b7...`)
- **Corroborating Target**: `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe` (PE32+ x86-64, size 8,676,352 bytes, SHA256: `374a9d7898a92e9f...`)
- **Obfuscation Technology**: Built with `garble` (Go symbol & package obfuscator). Identifier names scrambled to pseudo-random strings; `pclntab` intact (`0x2d42f0` bytes); string table plaintext in `.rodata`.
- **Parser Remediation (Blocker A)**: Successfully resolved via `tests/test_pclntab_parser.py` (documented in `reports/02A_PCLNTAB_PARSER_VALIDATION.md`). Structurally parses `functab -> _func -> nameOff` traversal with 100.00% valid symbol names.

## 2. Quantitative Metrics
| Metric | Value | Forensic Significance |
|---|---|---|
| **Total Functions Detected** | **7,571** | Exact function boundaries in `.gopclntab` |
| **Functions with Valid pclntab Entries** | **7,571 (100.00%)** | Zero unmapped or malformed entries |
| **Preserved Runtime / Stdlib Functions** | **1,948** | `runtime.*` (1,459), `reflect.*` (180), `syscall.*` (91), `sync.*` (51), `internal/abi.*` (25), stdlib (142) |
| **Garbled Project & Library Functions** | **5,623** | `main.*` (282) and obfuscated internal packages |
| **Functions with Confirmed Roles** | **1,982** | 1,948 stdlib + 34 project functions with direct string xrefs |
| **Garbled Functions Reserved for Decompilation** | **5,589** | Zero guesswork role assignment; kept as UNKNOWN |
| **Statically Registered Routes (`main.main`)** | **42** | Verified directly in `main.main` route registration disassembly |
| **JSON Schema Keys Recovered** | **81** | Parameters for auth, device, share, & signaling |
| **Functions with Exact String Xrefs** | **1,152** | Exact LEA x86_64 pointer matches into `.rodata` |
| **Direct Callgraph Edges Extracted** | **6,557** | Extracted direct `E8` CALL relationships |

## 3. Disassembly of Route Registration in `main.main`
Static disassembly of `main.main` (`VA: 0x7647a0` to `0x766980`) proves sequential registration of exactly 42 routes via `net/http.ServeMux.HandleFunc` (`Y0caeZ_zze.XpauMa5YLU`) and `Handle` (`Y0caeZ_zze.Rn6GpSlD5Rni`):

1. `[0x76596c]` `/api/tags`
2. `[0x765984]` `/api/shortcuts`
3. `[0x7659a0]` `/api/auth-status`
4. `[0x7659b8]` `/api/activate`
5. `[0x7659d0]` `/api/license_status`
6. `[0x7659e8]` `/debug/license`
7. `[0x765a00]` `/api/login`
8. `[0x765a18]` `/api/register`
9. `[0x765a30]` `/api/me`
10. `[0x765a48]` `/api/user/ai-config`
11. `[0x765a60]` `/api/logout`
12. `[0x765a78]` `/api/admin/users`
13. `[0x765a90]` `/api/admin/users/rename`
14. `[0x765aa8]` `/api/admin/assign`
15. `[0x765ac0]` `/api/admin/users/create`
16. `[0x765ad8]` `/api/admin/users/delete`
17. `[0x765af0]` `/api/admin/users/update_note`
18. `[0x765b08]` `/api/admin/users/update`
19. `[0x765b20]` `/api/admin/users/reset_password`
20. `[0x765b38]` `/api/admin/users/kick`
21. `[0x765b50]` `/api/share/create`
22. `[0x765b68]` `/api/share/list`
23. `[0x765b80]` `/api/share/revoke`
24. `[0x765b98]` `/api/share/extend`
25. `[0x765bb0]` `/api/share/update`
26. `[0x765bc8]` `/api/share/info`
27. `[0x765be0]` `/api/share/redeem_card`
28. `[0x765bf8]` `/api/server/addresses`
29. `[0x765c10]` `/register_device`
30. `[0x765c28]` `/register_agent`
31. `[0x765c40]` `/connect_client`
32. `[0x765c58]` `/devices`
33. `[0x765c70]` `/api/devices/`
34. `[0x765c88]` `/upload`
35. `[0x765ca0]` `/api/files`
36. `[0x765cb8]` `/api/tasks`
37. `[0x765cd0]` `/api/tasks/details`
38. `[0x765ce8]` `/api/default_settings`
39. `[0x765d00]` `/api/ice_servers`
40. `[0x765d18]` `/api/version`
41. `[0x765d6b]` `/snapshots/`
42. `[0x765e31]` `/`

### Distinct Status of Candidate Strings
Strings such as `/api/turn`, `/api/devices/list`, `/api/admin/users/register_device`, and `/downloads` exist in `.rodata` or frontend assets, but are NOT registered in `main.main`. The dynamic oracle confirms `/api/turn` returns `404 Not Found` for all tested HTTP methods (GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD). It is strictly classified as `STATIC_STRING_CANDIDATE / NOT_RUNTIME_REGISTERED`.

## 4. Cross-Architecture Corroboration (Windows vs Linux)
Cross-referencing the Linux ELF binary against the Windows PE executable proved:
1. **Endpoint Identity**: All 42 registered routes and WebSocket endpoints exist in both binaries.
2. **Persistence Schema**: Both rely on `data/users.json`, `data/shares.json`, and `data/device_tags.json`.
3. **Pclntab Equivalence**: Both binaries share identical runtime function structures and Gorilla WebSocket dependencies.
4. **Symbol Discrepancy Note**: Garbled symbol names differ between Linux and Windows builds (confirming randomized seed per compilation).
