# Forensic Audit: Clean-Room Binary Artifact Identity & Distribution Census

**Audit Milestone**: Phase 2R.1 — Evidence Normalization & Artifact Identity Repair  
**Timestamp**: 2026-09-16T06:00:00+07:00  
**Status**: AUDITED & CANONICALLY FROZEN  

---

## 1. Executive Summary

During Phase 2R, cross-mapping and flag extraction referenced binaries across the distribution archive `cloudphone-v0.3.6 (1)/`. To guarantee mathematical reproducibility and prevent semantic conflation between target architectures (Android ARM64 vs Linux AMD64 vs Windows AMD64), this audit formalizes the complete census of all binaries, their cryptographic SHA256 hashes, file sizes, architectures, and clean-room classifications.

---

## 2. Canonical Clean-Room Artifacts

Canonical artifacts are the primary reverse engineering targets protected by `tools/verify_phase2.py` (`EXPECTED_HASHES`). All baseline guarantees and differential tests are anchored against these binaries.

| Artifact Path | SHA256 Hash | Size (Bytes) | OS / Arch | Role | Classification |
|---|---|---|---|---|---|
| `cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling` | `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3` | 8,417,428 | Linux / AMD64 | Primary Signaling Server (Linux) | `CANONICAL_CLEANROOM_ARTIFACT` |
| `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe` | `374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917` | 8,676,352 | Windows / AMD64 | Primary Signaling Server (Windows) | `CANONICAL_CLEANROOM_ARTIFACT` |
| `cloudphone-v0.3.6 (1)/android/cloudphone-agent` | `9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4` | 13,828,244 | Android / ARM64 | Primary Agent Daemon (Android target) | `CANONICAL_CLEANROOM_ARTIFACT` |

---

## 3. Supplemental & Distributed Artifacts

The distribution archive contains additional binaries packaged for distribution, container deployments, and legacy architectures. These binaries must never be conflated with canonical artifacts without explicit qualification.

| Distributed Path | SHA256 Hash | Size (Bytes) | OS / Arch | Classification | Canonical Relation / Audit Notes |
|---|---|---|---|---|---|
| `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-arm64` | `9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4` | 13,828,244 | Android / ARM64 | `BYTE_IDENTICAL_ALIAS` | Exact copy of canonical `android/cloudphone-agent` located in `agentd/` deployment directory. |
| `cloudphone-v0.3.6 (1)/assets/agent/cloudphone-agent-arm64` | `9cc32ea3cffe29db0a362102b49288ffe58a8f940d05d1a2449356bc7cc93dd4` | 13,828,244 | Android / ARM64 | `BYTE_IDENTICAL_ALIAS` | Exact copy embedded inside signaling server HTTP asset download tree (`/assets/agent/`). |
| `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-amd64` | `15adc2a4c47c4d189d4e8e08e960434bdd55202d74bc3eeee0bf4713a6b8de16` | 14,663,828 | Linux / AMD64 | `SUPPLEMENTAL_DISTRIBUTED_ARTIFACT` | Distinct x86_64 ELF binary for Redroid container virtualization on AMD64 servers. Shares symbol table and CLI structure with canonical ARM64 agent, but has distinct binary layout. |
| `cloudphone-v0.3.6 (1)/assets/agent/cloudphone-agent-amd64` | `15adc2a4c47c4d189d4e8e08e960434bdd55202d74bc3eeee0bf4713a6b8de16` | 14,663,828 | Linux / AMD64 | `BYTE_IDENTICAL_ALIAS` | Exact copy of `agentd/cloudphone-agent-amd64` embedded in signaling asset download tree. |
| `cloudphone-v0.3.6 (1)/agentd/cloudphone-agent-armeabi-v7a` | `936f828fb30df461a2b45d5faa7fe1a50b0e6150cc2eda551c5f74bcefc815e5` | 14,155,924 | Android / ARM32 | `SUPPLEMENTAL_DISTRIBUTED_ARTIFACT` | 32-bit ARM ELF binary for legacy 32-bit Android device targets. |

---

## 4. Identity Handling Rules for Phase 2R.1 & Future Phases

1. **Strict Canonical Identity**: `tools/verify_phase2.py` and `evidence/reference/BASELINE.json` only accept the 3 canonical paths and exact SHA256 hashes.
2. **Explicit Qualification of Supplemental Binaries**: Any evidence or inspection derived from `agentd/cloudphone-agent-amd64` must explicitly cite that exact artifact path and hash, and cannot claim to represent `android/cloudphone-agent` without cross-build correlation.
3. **No Mixed Invariants**: Function counts, VA offsets, and disassembly from AMD64 agent binaries must never be merged into ARM64 forensic databases.
