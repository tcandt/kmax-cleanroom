# KMAX Clean-Room Reverse Engineering & Source Recovery

[![Clean-Room Protocol](https://img.shields.io/badge/Clean--Room-Authorized%20Source%20Recovery-blue.svg)](RULES.md)
[![Parity Target](https://img.shields.io/badge/Parity%20Target-%E2%89%A599%25%20Behavioral-success.svg)](reports/00_INVENTORY.md)
[![Provenance Coverage](https://img.shields.io/badge/Provenance-100%25%20Traceable-brightgreen.svg)](evidence/ARTIFACT_MANIFEST.md)

This repository contains the clean-room reverse-engineering, architecture reconstruction, and reproducible build restoration for the **KMAX / CloudPhone WebRTC** ecosystem, derived strictly from original distributed release artifacts.

---

## 1. Clean-Room Core Principles

This project operates under strict clean-room isolation rules documented in [RULES.md](RULES.md):

1. **Source Isolation**: Zero access to forbidden directories (`D:\KMAX\`, `D:\ScrcpyOverWebRTC\ScrcpyOverWebRTC-FullSource\`, or prior reconstructed source).
2. **Read-Only Original Artifacts**: All inputs in `cloudphone-v0.3.6 (1)`, `cloudphone-agent-magisk-v0.3.6 (1)`, and `ScrcpyOverWebRTC` are immutable.
3. **Evidence-First Engineering**: Every reconstructed function and subsystem must link directly to verified binary offsets, strings, or decompilation evidence.
4. **No Fabrication**: If original symbol names, comments, or types cannot be proven from binary evidence, they are classified as `UNKNOWN` or `RECONSTRUCTED_FROM_BINARY`.
5. **Continuous Auditability**: Every critical decision and phase milestone is recorded in [CLEANROOM_AUDIT_LOG.md](CLEANROOM_AUDIT_LOG.md).

---

## 2. Phase Status & Roadmap

| Phase | Description | Status | Key Deliverables |
|---|---|---|---|
| **Phase 0** | Forensic Inventory & Cryptographic Baseline | **DONE** | [00_INVENTORY.md](reports/00_INVENTORY.md), [ARTIFACT_MANIFEST.json](evidence/ARTIFACT_MANIFEST.json), [Hashes](evidence/hashes/) |
| **Incident 00A** | Clean-Room Boundary Remediation | **DONE** | [00A_CLEANROOM_BOUNDARY_REMEDIATION.md](reports/00A_CLEANROOM_BOUNDARY_REMEDIATION.md) (Quarantine upstream source) |
| **Phase 1A** | Android Helper Direct Decompilation | **DONE** | [01_ANDROID_DECOMPILE.md](reports/01_ANDROID_DECOMPILE.md), [CLASS_MAP.json](evidence/android/CLASS_MAP.json), [METHOD_MAP.json](evidence/android/METHOD_MAP.json) |
| **Phase 1B** | Go Signaling Server & Agent Forensics | **DONE** | [02_GO_SIGNALING_FORENSICS.md](reports/02_GO_SIGNALING_FORENSICS.md), [03_GO_AGENT_FORENSICS.md](reports/03_GO_AGENT_FORENSICS.md), [HTTP_ROUTES.md](evidence/go_signaling/HTTP_ROUTES.md) |
| **Phase 2 / 5** | Protocol Contract & Architecture Reconstruction | *Ready* | REST, WebSocket, DataChannel specs, Function mapping |
| **Phase 4** | Native Components & JNI Inspection | *Pending* | IPC & audio capture pipeline analysis |
| **Phase 5** | Complete Protocol & Contract Reconstruction | *Pending* | REST, WebSocket, & DataChannel protocol specs |
| **Phase 6** | Clean Source Code Reconstruction | *Pending* | Buildable Go, Java, and Vue source code |
| **Phase 7** | Independent Reproducible Build | *Pending* | Standalone Docker & multi-platform compilation |
| **Phase 8** | Differential Behavioral Testing | *Pending* | Parity test suite (target $\ge$ 99%) |
| **Phase 9** | Physical Android Device Validation | *Pending* | Touch, video streaming, Magisk root verification |
| **Phase 10** | Clean-Room Completion & Separate Audit | *Pending* | Final verification sign-off |

---

## 3. Forensic Artifact Inventory Summary (Phase 0)

Forensic cataloging across all 155 input files revealed critical technical findings:

1. **`libsys_core.so` is an Android APK**:
   - Packaged as a standard ZIP with `AndroidManifest.xml` and `classes.dex` (DEX version 035, 154 classes, 1,625 methods).
   - Package name: `com.android.helper` (`v3.3.4-2af7ccc1`).
   - Completely un-obfuscated DEX (intact classes like `CoreService`, `Options`, `AudioCapture`, `CleanUp`, `FakeContext`).
2. **Go Binaries Obfuscated with `garble`**:
   - Signaling server (`webrtc-signaling`) and Agent daemon (`cloudphone-agent`) have scrambled symbol names (`main.Gee4zB`, etc.).
   - `pclntab` structures (`magic: 0xfbffffff`) and plaintext string tables are intact, allowing complete function boundary and route recovery.
3. **Web Frontend Upstream Parity**:
   - `ScrcpyOverWebRTC/web-app` matches 1:1 the production bundle assets in `cloudphone-v0.3.6 (1)/assets/assets/`.

Full forensic analysis is available in [reports/00_INVENTORY.md](reports/00_INVENTORY.md) and [evidence/ARTIFACT_MANIFEST.md](evidence/ARTIFACT_MANIFEST.md).

---

## 4. Repository Structure

```text
KMAX-CLEANROOM/
├── cleanroom_archive/              # Consolidated forensic archive & audit toolchain
│   ├── cloudphone-v0.3.6 (1)/      # Original binaries and release distribution
│   ├── cloudphone-agent-magisk-v0.3.6 (1)/ # Original Magisk module package
│   ├── original_snapshot/          # Original unpacked artifacts snapshot
│   ├── raw_extraction/             # Raw extraction outputs (DEX/APK/disassembly)
│   ├── tools/                      # Forensic derivation engines & verification tools
│   ├── evidence/                   # Frozen forensic evidence & contracts
│   ├── reports/                    # Milestone audit & attestation reports
│   ├── tests/                      # Negative mutations & forensic unit tests
│   ├── build/                      # Build scaffolding
│   ├── logs/                       # Audit & verification execution logs
│   ├── requirements-forensics.txt  # Forensic Python environment dependencies
│   ├── CLEANROOM_AUDIT_LOG.md      # Comprehensive audit trail
│   ├── RULES.md                    # Clean-room governance & operational rules
│   └── walkthrough.md              # Historical verification walkthroughs
│
├── reconstructed_source/           # Full clean-room reconstructed production source
│   ├── android-app/                # Android companion application
│   ├── android-helper/             # Android Scrcpy helper service
│   ├── cloudphone-agent/           # Go device agent daemon
│   ├── web-app/                    # Vue 3 management console
│   └── webrtc-signaling/           # Go WebRTC signaling server
│
├── README.md                       # Repository entry point & orientation
└── .gitignore                      # Git ignore rules
```

---

## 5. Provenance Classification Tags

Every reconstructed file and function will be marked with a standardized provenance header:

```go
// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Evidence:
//   binary: webrtc-signaling (windows_amd64 / linux_amd64)
//   offset: 0x...
//   strings: "/api/login", "username", "password"
// Confidence: HIGH
```

Allowed classifications:
- `DIRECT_DECOMPILE`: Source recovered directly from DEX/APK bytecode.
- `DIRECT_SYMBOL_RECOVERY`: Symbols extracted directly from binary pclntab/exports.
- `RECONSTRUCTED_FROM_BINARY`: Synthesized from disassembly, strings, and cross-references.
- `RECONSTRUCTED_FROM_PROTOCOL`: Implemented from observed HTTP/WebSocket network contracts.
- `GENERATED_BUILD_FILE`: Build configuration independently recreated.
- `THIRD_PARTY`: Upstream dependency (e.g. Pion WebRTC, Vue, Gorilla WebSocket).
- `UNKNOWN`: Insufficient evidence to verify original implementation.
