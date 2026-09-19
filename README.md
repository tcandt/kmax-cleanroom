# KMAX Clean-Room Reverse Engineering & Source Recovery

[![Clean-Room Protocol](https://img.shields.io/badge/Clean--Room-Authorized%20Source%20Recovery-blue.svg)](cleanroom_archive/RULES.md)
[![Release](https://img.shields.io/badge/Release-cleanroom--v1.0.0-success.svg)](https://github.com/tcandt/kmax-cleanroom/releases/tag/cleanroom-v1.0.0)
[![Provenance Coverage](https://img.shields.io/badge/Provenance-100%25%20Traceable%20(324%2F324)-brightgreen.svg)](cleanroom_archive/evidence/final/RECONSTRUCTED_SOURCE_PROVENANCE_FINAL.json)
[![Verification Gates](https://img.shields.io/badge/Release%20Gates-11%2F11%20PASS-success.svg)](cleanroom_archive/reports/41_PHASE3B_FINAL_RELEASE_ATTESTATION.md)

This repository contains the clean-room reverse-engineering, architecture reconstruction, and reproducible build restoration for the **KMAX / CloudPhone WebRTC** ecosystem, derived strictly from original distributed release artifacts.

---

## 1. Clean-Room Core Principles

This project operates under strict clean-room isolation rules documented in [cleanroom_archive/RULES.md](cleanroom_archive/RULES.md):

1. **Source Isolation**: Zero access to forbidden external proprietary directories or prior unverified source.
2. **Read-Only Original Artifacts**: All canonical inputs in `cleanroom_archive/cloudphone-v0.3.6 (1)` and `cleanroom_archive/cloudphone-agent-magisk-v0.3.6 (1)` are immutable and cryptographically pinned.
3. **Evidence-First Engineering**: Every reconstructed function and subsystem links directly to verified binary offsets, strings, disassembly, or decompilation evidence.
4. **No Fabrication**: If original symbol names, comments, or types cannot be proven from binary evidence, they are classified according to strict provenance taxonomy (`RECONSTRUCTED_FROM_BINARY`, `GENERATED_ADAPTER`, `IMPLEMENTATION_CHOICE`, etc.). Zero `UNKNOWN` functions exist in production code.
5. **Continuous Auditability**: Every critical decision and phase milestone is recorded in [cleanroom_archive/CLEANROOM_AUDIT_LOG.md](cleanroom_archive/CLEANROOM_AUDIT_LOG.md).

---

## 2. Release Status & Phase Milestones

The project achieved formal clean-room release closure at tag [`cleanroom-v1.0.0`](https://github.com/tcandt/kmax-cleanroom/releases/tag/cleanroom-v1.0.0) (commit `4ee87c6db0b201375dc9795e812072dd9f2f71da`).

| Milestone | Scope & Description | Status | Key Deliverables & Reports |
|---|---|---|---|
| **Phase 0** | Forensic Inventory & Cryptographic Baseline | **DONE** | [00_INVENTORY.md](cleanroom_archive/reports/00_INVENTORY.md), [ARTIFACT_MANIFEST.json](cleanroom_archive/evidence/ARTIFACT_MANIFEST.json), [Hashes](cleanroom_archive/evidence/hashes/) |
| **Incident 00A** | Clean-Room Boundary Remediation & Quarantine | **DONE** | [00A_CLEANROOM_BOUNDARY_REMEDIATION.md](cleanroom_archive/reports/00A_CLEANROOM_BOUNDARY_REMEDIATION.md) |
| **Phase 1A** | Android Helper Direct Decompilation & DEX Audit | **DONE** | [01_ANDROID_DECOMPILE.md](cleanroom_archive/reports/01_ANDROID_DECOMPILE.md), [CLASS_MAP.json](cleanroom_archive/evidence/android/CLASS_MAP.json) |
| **Phase 1B** | Go Signaling & Agent Binary Forensics | **DONE** | [02_GO_SIGNALING_FORENSICS.md](cleanroom_archive/reports/02_GO_SIGNALING_FORENSICS.md), [03_GO_AGENT_FORENSICS.md](cleanroom_archive/reports/03_GO_AGENT_FORENSICS.md) |
| **Phase 2** | Differential Engines, Protocol Contracts & Forensic Gates | **DONE** | [02B_ROLE_MAPPING_VALIDATION.md](cleanroom_archive/reports/02B_ROLE_MAPPING_VALIDATION.md), [02C_PHASE2_REPRODUCIBILITY.md](cleanroom_archive/reports/02C_PHASE2_REPRODUCIBILITY.md) |
| **Phase 3A** | Clean-Room Go Source Reconstruction & Provenance Binding | **DONE** | 324/324 functions audited; 15 frozen contracts verified |
| **Phase 3ARR2** | Master Verifier Hardening & Clean-Clone Verification | **DONE** | [PHASE3ARR2_READINESS_DASHBOARD.json](cleanroom_archive/evidence/final/PHASE3ARR2_READINESS_DASHBOARD.json) |
| **Phase 3B** | Release Closure, Final Manifest Freeze & Tagging | **RELEASED** | Tag [`cleanroom-v1.0.0`](https://github.com/tcandt/kmax-cleanroom/releases/tag/cleanroom-v1.0.0), [41_PHASE3B_FINAL_RELEASE_ATTESTATION.md](cleanroom_archive/reports/41_PHASE3B_FINAL_RELEASE_ATTESTATION.md) |
| **Post-Release** | Layout V2 Root Consolidation (`cleanroom_archive/`) | **DONE** | [POST_RELEASE_LAYOUT_V2_MAPPING.json](cleanroom_archive/evidence/post_release/POST_RELEASE_LAYOUT_V2_MAPPING.json) |

---

## 3. Forensic Artifact Inventory Summary

Forensic cataloging across all 155 canonical input files revealed critical technical findings:

1. **`libsys_core.so` is an Android APK**:
   - Packaged as a standard ZIP with `AndroidManifest.xml` and `classes.dex` (DEX version 035, 154 classes, 1,625 methods).
   - Package name: `com.android.helper` (`v3.3.4-2af7ccc1`).
   - Completely un-obfuscated DEX (intact classes like `CoreService`, `Options`, `AudioCapture`, `CleanUp`, `FakeContext`).
2. **Go Binaries Obfuscated with `garble`**:
   - Signaling server (`webrtc-signaling`) and Agent daemon (`cloudphone-agent`) had scrambled symbol names (`main.Gee4zB`, etc.).
   - `pclntab` structures (`magic: 0xfbffffff`) and plaintext string tables remained intact, allowing complete function boundary and route recovery.
3. **Web Frontend Upstream Parity**:
   - `web-app` matches 1:1 the production bundle assets in `cleanroom_archive/cloudphone-v0.3.6 (1)/assets/assets/`.

Full forensic analysis is available in [cleanroom_archive/reports/00_INVENTORY.md](cleanroom_archive/reports/00_INVENTORY.md) and [cleanroom_archive/evidence/ARTIFACT_MANIFEST.md](cleanroom_archive/evidence/ARTIFACT_MANIFEST.md).

---

## 4. Repository Structure (Layout V2)

The repository root is organized into two primary top-level directories:

```text
KMAX-CLEANROOM/
├── cleanroom_archive/              # Consolidated forensic archive, original artifacts & audit tools
│   ├── cloudphone-v0.3.6 (1)/      # Original binaries and release distribution (read-only)
│   ├── cloudphone-agent-magisk-v0.3.6 (1)/ # Original Magisk module package (read-only)
│   ├── original_snapshot/          # Original unpacked artifacts snapshot
│   ├── raw_extraction/             # Raw extraction outputs (DEX/APK/disassembly)
│   ├── tools/                      # Forensic derivation engines & verification tools
│   ├── evidence/                   # Frozen forensic evidence & contracts
│   ├── reports/                    # Milestone audit & attestation reports
│   ├── tests/                      # Negative mutation suites & forensic unit tests
│   ├── build/                      # Build scaffolding
│   ├── logs/                       # Audit & verification execution logs
│   ├── requirements-forensics.txt  # Forensic Python environment dependencies
│   ├── CLEANROOM_AUDIT_LOG.md      # Comprehensive audit trail
│   ├── RULES.md                    # Clean-room governance & operational rules
│   └── walkthrough.md              # Historical verification walkthroughs
│
├── reconstructed_source/           # Clean-room reconstructed production source
│   ├── cloudphone-agent/           # Go device agent daemon (Full tracked production source, 44 files)
│   ├── webrtc-signaling/           # Go WebRTC signaling server (Full tracked production source, 31 files)
│   ├── android-app/                # Empty-tree stub (deferred outside v1.0.0 scope)
│   ├── android-helper/             # Empty-tree stub (DEX bytecode decompiled in cleanroom_archive/)
│   └── web-app/                    # Empty-tree stub (assets archived in cleanroom_archive/)
│
├── README.md                       # Repository entry point & orientation
└── .gitignore                      # Git ignore rules
```

---

## 5. Provenance Classification Tags

Every reconstructed file and function is marked with a standardized provenance header:

```go
// CLEANROOM-PROVENANCE:
// Classification: RECONSTRUCTED_FROM_BINARY
// Evidence:
//   binary: webrtc-signaling (windows_amd64 / linux_amd64)
//   offset: 0x...
//   strings: "/api/login", "username", "password"
// Confidence: HIGH
```

Formally audited provenance breakdown across 324 reconstructed production functions:
- `RECONSTRUCTED_FROM_BINARY`: 131 functions (40.4%)
- `GENERATED_ADAPTER`: 119 functions (36.7%)
- `IMPLEMENTATION_CHOICE`: 27 functions (8.3%)
- `RECONSTRUCTED_FROM_PROTOCOL`: 21 functions (6.5%)
- `GENERATED_TEST_INTERFACE`: 18 functions (5.6%)
- `GENERATED_BUILD_FILE`: 8 files (2.5%)
- `UNKNOWN`: 0 functions (0.0% — zero unmapped functions)

---

## 6. Post-Release Verification

To run the complete 11-gate release audit suite against the repository:

```bash
cd cleanroom_archive
python tools/verify_release.py
```

To run individual module unit tests:
```bash
# CloudPhone Agent
cd reconstructed_source/cloudphone-agent
go test ./...

# WebRTC Signaling Server
cd reconstructed_source/webrtc-signaling
go test ./...
```
