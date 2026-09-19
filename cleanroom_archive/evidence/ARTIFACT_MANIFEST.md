# Clean-Room Forensic Artifact Manifest

- **Total Cataloged Files**: 155
- **Total Combined Size**: 379.73 MB
- **Unique SHA256 Hashes**: 132
- **Duplicated Files Across Repositories**: 14

## Category Breakdown

| Category | Count | Total Size |
|---|---|---|
| `AGENT_DEPLOY_PACKAGE` | 1 | 17.14 MB |
| `ANDROID_APK_HELPER` | 4 | 0.37 MB |
| `CONFIG_METADATA` | 7 | 0.01 MB |
| `DOCUMENTATION_ASSET` | 8 | 1.45 MB |
| `GIT_METADATA` | 28 | 149.79 MB |
| `GO_AGENT_DAEMON` | 17 | 135.22 MB |
| `GO_SIGNALING_SERVER` | 7 | 55.14 MB |
| `MAGISK_MODULE_PACKAGE` | 1 | 17.14 MB |
| `MANAGEMENT_SCRIPT` | 14 | 0.03 MB |
| `SECURITY_CREDENTIAL` | 8 | 0.02 MB |
| `WEB_FRONTEND_COMPILED_BUNDLE` | 6 | 2.27 MB |
| `WEB_FRONTEND_SOURCE` | 52 | 1.08 MB |
| `WEB_PACKAGE_METADATA` | 2 | 0.05 MB |

## Core Binary Targets (Reverse Engineering Scope)

| Subsystem | Relative Path | Size | Architecture | Runtime / Obfuscation | SHA256 |
|---|---|---|---|---|---|
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/action.sh` | 1,881 B | Unknown | N/A | `9671f4c1fdb5eb4d...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/binaries/cloudphone-agent-amd64` | 14,663,828 B | x86_64 (AMD64) | none/unknown | `15adc2a4c47c4d18...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/binaries/cloudphone-agent-arm64` | 13,828,244 B | AArch64 (ARM64) | none/unknown | `9cc32ea3cffe29db...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/binaries/cloudphone-agent-armeabi-v7a` | 14,155,924 B | ARM (32-bit) | none/unknown | `936f828fb30df461...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/cloudphone-ctl` | 10,501 B | Unknown | N/A | `572705aeb46fcd32...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/config.conf` | 498 B | Unknown | N/A | `e656205770c2d325...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/customize.sh` | 2,257 B | Unknown | N/A | `d38aa30cfa479e05...` |
| `android-helper` | `cloudphone-agent-magisk-v0.3.6 (1)/libsys_core.so` | 96,988 B | neutral / DEX | DEX (Unobfuscated) | `19a16c9bd7143538...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/module.prop` | 355 B | Unknown | N/A | `e514832a928705a6...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/service.sh` | 3,707 B | Unknown | N/A | `c9855ae5a3105cc5...` |
| `cloudphone-agent` | `cloudphone-agent-magisk-v0.3.6 (1)/uninstall.sh` | 271 B | Unknown | N/A | `59630eb0ae070990...` |
| `cloudphone-agent` | `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-amd64` | 14,663,828 B | x86_64 (AMD64) | none/unknown | `15adc2a4c47c4d18...` |
| `cloudphone-agent` | `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-arm64` | 13,828,244 B | AArch64 (ARM64) | none/unknown | `9cc32ea3cffe29db...` |
| `cloudphone-agent` | `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-armeabi-v7a` | 14,155,924 B | ARM (32-bit) | none/unknown | `936f828fb30df461...` |
| `android-helper` | `cloudphone-v0.3.6 (1)/agentd/libsys_core.so` | 96,988 B | neutral / DEX | DEX (Unobfuscated) | `19a16c9bd7143538...` |
| `cloudphone-agent` | `cloudphone-v0.3.6 (1)/android/cloudphone-agent` | 13,828,244 B | AArch64 (ARM64) | none/unknown | `9cc32ea3cffe29db...` |
| `android-helper` | `cloudphone-v0.3.6 (1)/android/libsys_core.so` | 96,988 B | neutral / DEX | DEX (Unobfuscated) | `19a16c9bd7143538...` |
| `webrtc-signaling` | `cloudphone-v0.3.6 (1)/android/webrtc-signaling` | 7,930,004 B | AArch64 (ARM64) | garble (Go symbol scramble) | `537be428fa7e2c6d...` |
| `cloudphone-agent` | `cloudphone-v0.3.6 (1)/assets/agent/cloudphone-agent-amd64` | 14,663,828 B | x86_64 (AMD64) | none/unknown | `15adc2a4c47c4d18...` |
| `cloudphone-agent` | `cloudphone-v0.3.6 (1)/assets/agent/cloudphone-agent-arm64` | 13,828,244 B | AArch64 (ARM64) | none/unknown | `9cc32ea3cffe29db...` |
| `cloudphone-agent` | `cloudphone-v0.3.6 (1)/assets/agent/cloudphone-agent-armeabi-v7a` | 14,155,924 B | ARM (32-bit) | none/unknown | `936f828fb30df461...` |
| `android-helper` | `cloudphone-v0.3.6 (1)/assets/agent/libsys_core.so` | 96,988 B | neutral / DEX | DEX (Unobfuscated) | `19a16c9bd7143538...` |
| `webrtc-signaling` | `cloudphone-v0.3.6 (1)/bin/darwin_amd64/webrtc-signaling` | 8,678,176 B | x86_64 (AMD64) | garble (Go symbol scramble) | `c9c3887121f2ef58...` |
| `webrtc-signaling` | `cloudphone-v0.3.6 (1)/bin/darwin_arm64/webrtc-signaling` | 8,176,146 B | ARM64 | garble (Go symbol scramble) | `cba217d56446c0c6...` |
| `webrtc-signaling` | `cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling` | 8,417,428 B | x86_64 (AMD64) | garble (Go symbol scramble) | `6865f05fe59838b7...` |
| `webrtc-signaling` | `cloudphone-v0.3.6 (1)/bin/linux_arm64/webrtc-signaling` | 7,930,004 B | AArch64 (ARM64) | garble (Go symbol scramble) | `537be428fa7e2c6d...` |
| `webrtc-signaling` | `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe` | 8,676,352 B | x86_64 (AMD64) | garble (Go symbol scramble) | `374a9d7898a92e9f...` |
| `webrtc-signaling` | `cloudphone-v0.3.6 (1)/bin/windows_arm64/webrtc-signaling.exe` | 8,012,288 B | ARM64 | garble (Go symbol scramble) | `a9f582aaf6cea1fe...` |

## Exact Duplicates Cross-Referencing

Identical binaries present across multiple deployment packaging directories:

### SHA256: `15adc2a4c47c4d189d4e8e08e960434bdd55202d74bc3eeee0bf4713a6b8de16`
- `cloudphone-agent-magisk-v0.3.6 (1)/binaries/cloudphone-agent-amd64`
- `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-amd64`
- `cloudphone-v0.3.6 (1)/assets/agent/cloudphone-agent-amd64`

### SHA256: `9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4`
- `cloudphone-agent-magisk-v0.3.6 (1)/binaries/cloudphone-agent-arm64`
- `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-arm64`
- `cloudphone-v0.3.6 (1)/android/cloudphone-agent`
- `cloudphone-v0.3.6 (1)/assets/agent/cloudphone-agent-arm64`

### SHA256: `936f828fb30df461a2b45d5faa7fe1a50b0e6150cc2eda551c5f74bcefc815e5`
- `cloudphone-agent-magisk-v0.3.6 (1)/binaries/cloudphone-agent-armeabi-v7a`
- `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-armeabi-v7a`
- `cloudphone-v0.3.6 (1)/assets/agent/cloudphone-agent-armeabi-v7a`

### SHA256: `19a16c9bd714353816c4d814b8c187ed91aac7447fd23ff8be6b78eacc815528`
- `cloudphone-agent-magisk-v0.3.6 (1)/libsys_core.so`
- `cloudphone-v0.3.6 (1)/agentd/libsys_core.so`
- `cloudphone-v0.3.6 (1)/android/libsys_core.so`
- `cloudphone-v0.3.6 (1)/assets/agent/libsys_core.so`

### SHA256: `24c023bee2c6f8b41c425acc5e5f196fdf4de27bcd4216d905c824cf722583f4`
- `cloudphone-v0.3.6 (1)/android/certs/create_certs.sh`
- `cloudphone-v0.3.6 (1)/certs/create_certs.sh`

### SHA256: `de3d24a08365ae917c1c17cbb60079fd20b4ed640f9b5d41a4777d7b3cf192bd`
- `cloudphone-v0.3.6 (1)/android/certs/server.crt`
- `cloudphone-v0.3.6 (1)/certs/server.crt`

### SHA256: `a2aae5aa0a09d534587679eff7b4d6322e7489a61699043d76cacc59ebccc621`
- `cloudphone-v0.3.6 (1)/android/certs/server.key`
- `cloudphone-v0.3.6 (1)/certs/server.key`

### SHA256: `611dedfa232ec6355a0f6da45349c16341827afa5eada5ed075634c8c8ac1077`
- `cloudphone-v0.3.6 (1)/android/certs/server.p12`
- `cloudphone-v0.3.6 (1)/certs/server.p12`

### SHA256: `27d663627cbfb969eb3546ef4a0b17c17ca6ad5f878234a483542343496cfb02`
- `cloudphone-v0.3.6 (1)/android/certs/trusted.pem`
- `cloudphone-v0.3.6 (1)/certs/trusted.pem`

### SHA256: `537be428fa7e2c6d2599e2df9d98e38020e6fa66e73991286bdebf47177feac5`
- `cloudphone-v0.3.6 (1)/android/webrtc-signaling`
- `cloudphone-v0.3.6 (1)/bin/linux_arm64/webrtc-signaling`

### SHA256: `d90f33aa9e98aa15fded20f609a908f09ecd8de524c67d326f1060808c49d882`
- `cloudphone-v0.3.6 (1)/assets/assets/wework.jpg`
- `ScrcpyOverWebRTC/web-app/public/assets/wework.jpg`

### SHA256: `59248024d9f1d1058b9320a97412493989466687482c00502c0b27ef0190b2b8`
- `cloudphone-v0.3.6 (1)/bin/darwin_amd64/run.sh`
- `cloudphone-v0.3.6 (1)/bin/darwin_arm64/run.sh`
- `cloudphone-v0.3.6 (1)/bin/linux_amd64/run.sh`
- `cloudphone-v0.3.6 (1)/bin/linux_arm64/run.sh`

### SHA256: `d309aa9901be7cdd96b43411cf96191fe46fbe293a27c1cdeaaa2478d545d61c`
- `cloudphone-v0.3.6 (1)/bin/windows_amd64/run.bat`
- `cloudphone-v0.3.6 (1)/bin/windows_arm64/run.bat`

