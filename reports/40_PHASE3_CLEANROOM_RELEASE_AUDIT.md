# Report 40: Phase 3AR Clean-Room Provenance, Reproducibility & Release Audit Hardening

## 1. Executive Summary

This report documents the comprehensive hardening, cross-phase fact reconciliation, fail-closed gate enforcement, and release readiness auditing for the **KMAX Clean-Room Recovery Project (Phase 3AR)**.

Baseline Git commit: **`efb67ca36e6cf70a87dc3a604b2cdb6d8814efed`** (`origin/main`).

Following strict clean-room governance:
- **Zero runtime behavior modifications**: `reconstructed_source/` remains untouched.
- **Zero capability expansion**: No AI execution, no ADB bridge/shell/PTY activation.
- **Fail-Closed Release Boundary**: `final_ready` remains strictly **`false`** throughout Phase 3AR.
- **No Release Tag**: Release git tag `cleanroom-v1.0.0` is strictly deferred to Phase 3B.
- **Total Release Conditions**: Exactly **11 internal executable verification gates** + **1 external independent clean-clone condition** = **12 Phase 3AR readiness conditions**.

### Formal Recovery Declaration
> **Clean-room recovery completed with 100% provenance accounting and release-audited protocol/functional parity within the approved runtime scope; intentionally deferred execution boundaries are explicitly documented.**

---

## 2. Approved Scope & Functional Boundaries

The clean-room project scope encompasses:
1. **Android Helper (`android-helper`)**: Decompiled and reconstructed from `libsys_core.so` (Scrcpy v3.3.4 server architecture, package `com.android.helper`, 154 classes, 1,061 declared methods).
2. **Go Signaling Server (`webrtc-signaling`)**: Reconstructed from Linux AMD64 binary `webrtc-signaling` and Windows AMD64 binary `webrtc-signaling.exe` (HTTP routes, session tokens, devices, users, tags, shares, shortcuts, files/tasks, license manager, and WebSocket relay hub).
3. **Go Device Agent (`cloudphone-agent`)**: Reconstructed from Linux ARM64 binary `cloudphone-agent` (signaling client, session coordinator, Pion WebRTC core engine, media tracks, and six DataChannels).
4. **Strict Scope Exclusions (Deferred Boundaries)**:
   - **AI Command Execution**: Original command dispatch mechanism forensically mapped; runtime OS process execution intentionally deferred (`AI-B5F-10`).
   - **ADB Daemon Bridge**: Dual-mode binary framing (CNXN 24-byte packet header vs raw PTY stream) forensically mapped; in-process PTY / shell path identified; live terminal/PTY bridge runtime intentionally deferred (`ADB-B6F-11`).
   - **Package Installer**: File upload chunk reassembly and path security enforced; host APK package installation (`install: true`) deferred (`FILE-B3-06`).

---

## 3. Original Artifact Inventory Completeness & Purge Reconciliation

Audited via `tools/audit/audit_original_artifacts.py`:
All **155 Phase 0 entries** recorded in `evidence/ARTIFACT_MANIFEST.json` are 100% classified and accounted for:
- **`REQUIRED_ORIGINAL_ARTIFACT`**: **65 / 65** authentic original binaries and extracts are fully materialized on disk and **100% SHA-256 hash-verified**.
- **`PURGED_FORBIDDEN_EXTERNAL_SOURCE`**: **90 / 90** entries correspond to the `ScrcpyOverWebRTC` external submodule explicitly purged during clean-room boundary remediation at commit `ef14fab`.
- **Unclassified / Unaccounted**: **0 / 155**.

---

## 4. Frozen Contract Historical Pinning & Dual Hash Representation

Audited via `tools/audit/audit_frozen_contracts.py` across all 15 registered contracts:
To prevent line-ending discrepancies on Windows (CRLF checkout bytes vs LF git-blob bytes) from altering historical integrity, every contract and errata entry records both:
- `historical_git_blob_sha256`: Verified via `git show <freeze_commit>:<artifact_path>`.
- `frozen_artifact_sha256`: Verified via on-disk SHA-256 computation.
- `freeze_commit`: Full 40-character commit hash verified in git commit history.
- `line_ending_policy`: Declared line ending normalization.

For contracts with formal errata:
- `errata_freeze_commit`, `errata_git_blob_sha256`, and `errata_artifact_sha256` are recorded and independently verified.

**Result**: 15 / 15 Frozen Contracts verified via historical git-blob and on-disk SHA-256 hashes.

---

## 5. Cross-Phase Reconciliation & Six-Channel Summary

As reconciled in `evidence/final/PHASE3_CROSS_PHASE_FACT_MATRIX.json`:

| DataChannel Label | Creator | Consumer | Ingress Direction | Ordered Mode & Evidence | Request Framing | Response Framing | Downstream Target & Transport | Clean-Room Status |
|---|---|---|---|---|---|---|---|---|
| **`input-channel`** | Agent | Agent | Browser -> Agent | `true` (`STATIC_CONFIRMED`) | `JSON_TEXT` | None | UDS `@uds_sys_t_` (scrcpy ControlMessages) | `IMPLEMENTED_AND_TESTED` |
| **`clipboard-channel`** | Agent | Agent | BIDIRECTIONAL | `true` (`STATIC_CONFIRMED`) | `JSON_TEXT` | `JSON_TEXT` | Android ClipboardManager (`MemoryClipboardProvider`) | `IMPLEMENTED_AND_TESTED` |
| **`file-channel`** | Browser Client | Agent | Browser -> Agent | `true` (`REFERENCE_INTEROPERABILITY`) | Hybrid Metadata + Chunks | `NOT_RECOVERED` (`NO_CANONICAL_EGRESS_EVIDENCE`) | `FileSink` (`/data/local/tmp` target) | `IMPLEMENTED_SAFE_SCOPE` |
| **`camera-channel`** | Agent | Browser Client | BIDIRECTIONAL | `true` (`STATIC_CONFIRMED`) | Agent->Browser: `JSON_TEXT` | Browser->Agent: `RAW_BINARY` | Camera HAL TCP bridge **`127.0.0.1:9001`** (4-byte LE framing) | `IMPLEMENTED_AND_TESTED` |
| **`ai-command-channel`** | Browser Client | Agent | Browser -> Agent | `true` (`REFERENCE_INTEROPERABILITY`) | `JSON_TEXT` | `BINARY_JSON_BYTES` | Automation Engine (Parser only; execution deferred `AI-B5F-10`) | `SAFE_PARSER_INERT` |
| **`adb-channel`** | Browser Client | Agent | Browser -> Agent | `true` (`REFERENCE_INTEROPERABILITY`) | Dual-mode 24B LE / PTY | Dual-mode | In-process PTY (`/dev/ptmx`, `/system/bin/sh`; deferred `ADB-B6F-11`) | `INERT_FORENSIC_ONLY` |

### Key Forensic Findings
1. **Camera Bridge Canonical Endpoint**: The authoritative default endpoint is **`127.0.0.1:9001`** (backed by disassembly strings at VA `0x51ee80`). Preliminary references to `:8089` were reconciled and superseded.
2. **Camera Framing Boundary**: The 4-byte little-endian length prefix belongs strictly to the **Camera HAL TCP bridge protocol**, NOT WebRTC DataChannel wire framing.
3. **`file-channel.ordered` Taxonomy**: Reconciled from `STATIC_CONFIRMED` to **`REFERENCE_INTEROPERABILITY`** (as an inbound Browser-created channel, Agent binary does not call `CreateDataChannel`). Response framing is classified as **`NOT_RECOVERED`** (`NO_CANONICAL_EGRESS_EVIDENCE`).
4. **`adb-channel` Absence Phrasing Standard**: *No external TCP connection to 127.0.0.1:5555 was recovered from the adb-channel callgraph in either original Agent binary.* Authentic downstream is in-process PTY/shell path. Deferred execution boundary is **`ADB-B6F-11`**.

---

## 6. Android Helper DEX Method Count Invariant ($1,625 = 1,061 + 564$)

Audited via direct binary DEX parsing in `tools/audit/audit_method_count.py`:
- **Total Raw DEX Method IDs**: **1,625**
- **Class-Defined Helper Methods**: **1,061** (100% decompiled and verified in Phase 1A)
- **Non-Defined Method References**: **564**
  - `Ljava/*` (Java Platform Library): **279**
  - `Landroid/*` (Android Framework Library): **269**
  - `internal-class-owner` (inherited method references): **7**
    - 4 resolved to base methods (`Object.hashCode`, `Object.equals`, `Handler.sendEmptyMessage`, `Thread.start`)
    - 3 resolved to abstract `SurfaceCapture` methods
  - `synthetic array-owner clone()` references: **9** (Java compiler enum synthetic clones)
  - Unclassified: **0**
- **Mathematical Identity**: $1,061 + 279 + 269 + 7 + 9 = 1,625$ (**100% Exact Parity**).

---

## 7. Reconstructed Source Provenance Audit & Structural Locators

Audited via `tools/audit/audit_reconstructed_source_provenance.py` across all 324 production functions in `reconstructed_source/`:
- Every function is mapped to an authoritative structural locator:
  - `CONTRACT_ID`: Verifiable structural identifier in a frozen JSON contract.
  - `JSON_POINTER`: RFC 6901 pointer resolvable in an evidence contract.
  - `SYMBOL`: Direct symbol in disassembly facts or symbol map.
  - `PHASE_RULE`: Authoritative architectural pattern in `PROVENANCE_RULES.json`.
- **UNKNOWN Production Functions**: **0** (100.00% Provenance Completeness).
- **Structural Validation Failures**: **0**.

---

## 8. Clean-Room Contamination Audit & Historical Tree Inspection

Audited via `tools/audit/audit_cleanroom_contamination.py` across all 69 reachable Git commits:
- **Multi-Tier Forensic Verdicts**:
  1. `CURRENT_TREE_CLEAN`: Working tree contains 0 forbidden strings, 0 submodules, 0 gitlinks.
  2. `HISTORICAL_TREE_AUDITED`: Full Git commit tree history inspected.
  3. `HISTORICAL_REMEDIATION_PRESENT`: Identified pre-`ef14fab` external submodule gitlink and verified formal purge at commit `ef14fab`.
  4. `POST_REMEDIATION_HISTORY_CLEAN`: All 67 reachable commits after `ef14fab` up to HEAD are strictly clean.

### Forensic Contamination Disclosure
> Current tree clean: CURRENT_TREE_CLEAN.
> Historical external-source exposure identified (pre-ef14fab ScrcpyOverWebRTC gitlink & .gitmodules).
> Remediation boundary documented at ef14fab (reports/00A_CLEANROOM_BOUNDARY_REMEDIATION.md).
> All reachable post-remediation commits clean under declared audit policy: POST_REMEDIATION_HISTORY_CLEAN.

---

## 9. Toolchain Reproducibility & Portability

Audited via `tools/audit/audit_toolchain.py`:
- **Python**: 3.13.13 (sys.executable)
- **Go**: go1.26.3 (which go / GOROOT)
- **Git**: 2.54.0.windows.1 (which git)
- **LLVM / llvm-objdump**: LLVM version 22.1.8
- **CGO C Compiler**: `gcc.exe` driver wrapper invoking Clang backend (version 22.1.8)
- **Workstation Paths**: Zero hardcoded paths in production or tooling.
- **Baksmali Tooling Classification**:
  `HISTORICAL_ARCHIVAL_OUTPUT_PRESENT` (Archival artifact present from Phase 1A; not independently re-verified in Phase 3AR).

---

## 10. Fail-Closed Negative Mutation Suite (18 Tests)

Audited via `tools/test_release_negative.py`:
18 / 18 real negative mutations executed against actual production validators using isolated temporary directories:
1. `MUTATION-01`: Tampered contract SHA-256 $\rightarrow$ **REJECTED (FAIL-CLOSED)**
2. `MUTATION-02`: Wrong historical baseline commit $\rightarrow$ **REJECTED (FAIL-CLOSED)**
3. `MUTATION-03`: Tampered original artifact hash $\rightarrow$ **REJECTED (FAIL-CLOSED)**
4. `MUTATION-04`: Missing original artifact file $\rightarrow$ **REJECTED (FAIL-CLOSED)**
5. `MUTATION-05`: Missing required tool in toolchain manifest $\rightarrow$ **REJECTED (FAIL-CLOSED)**
6. `MUTATION-06`: UNKNOWN production function $\rightarrow$ **REJECTED (FAIL-CLOSED)**
7. `MUTATION-07`: Invalid provenance locator / non-existent fact ID $\rightarrow$ **REJECTED (FAIL-CLOSED)**
8. `MUTATION-08`: Clean-room contamination injection $\rightarrow$ **REJECTED (FAIL-CLOSED)**
9. `MUTATION-09`: Inverted DataChannel creator/consumer $\rightarrow$ **REJECTED (FAIL-CLOSED)**
10. `MUTATION-10`: Wrong camera endpoint (8089 instead of 9001) $\rightarrow$ **REJECTED (FAIL-CLOSED)**
11. `MUTATION-11`: Method count discrepancy $\rightarrow$ **REJECTED (FAIL-CLOSED)**
12. `MUTATION-12`: Dirty working tree detection $\rightarrow$ **REJECTED (FAIL-CLOSED)**
13. `MUTATION-13`: Absolute workstation path dependency leak $\rightarrow$ **REJECTED (FAIL-CLOSED)**
14. `MUTATION-14`: Missing mapped critical test $\rightarrow$ **REJECTED (FAIL-CLOSED)**
15. `MUTATION-15`: Skipped critical test $\rightarrow$ **REJECTED (FAIL-CLOSED)**
16. `MUTATION-16`: Missing required formal errata $\rightarrow$ **REJECTED (FAIL-CLOSED)**
17. `MUTATION-17`: Clean-clone dependency on untracked file $\rightarrow$ **REJECTED (FAIL-CLOSED)**
18. `MUTATION-18`: Wrong errata freeze commit or blob hash $\rightarrow$ **REJECTED (FAIL-CLOSED)**

---

## 11. Intentional Divergences Registry

Audited via `evidence/final/INTENTIONAL_DIVERGENCES.json`:
1. `DIVERGENCE-AI-EXEC`: AI command process execution deferred (Safe parser only).
2. `DIVERGENCE-ADB-BRIDGE`: Live interactive shell/PTY bridge deferred (Inert topology hooks only).
3. `DIVERGENCE-FILE-INSTALLER`: APK installer execution deferred (File transfer only).
4. `DIVERGENCE-CAMERA-HARDWARE`: Virtual camera kernel driver abstracted via TCP bridge socket **`127.0.0.1:9001`**.
5. `DIVERGENCE-CLIPBOARD-MOCK`: Android system clipboard service mocked via `MemoryClipboardProvider`.
6. `DIVERGENCE-INPUT-UDS-MOCK`: Android input UDS socket mocked via `ControlSink`.

---

## 12. Two-Stage Clean Clone & Readiness Verification Architecture

To prevent self-referential clean-clone paradoxes, Phase 3AR is staged across two distinct commits:

```text
Phase 3AR-A: Audit Hardening & Reconciliation
  - All 11 internal gates hardened & verified
  - clean_clone_verified = false
  - final_ready = false
  - Commit & Push to origin/main
        ↓
Independent Clean-Clone Execution
  - git clone d:\KMAX-CLEANROOM <external_temp>
  - git checkout <Phase 3AR-A SHA>
  - python tools/verify_release.py
  - python tools/test_release_negative.py
  - git status strictly clean
        ↓
Phase 3AR-B: Evidence-Only Closure
  - Record CLEAN_CLONE_VERIFICATION_RESULTS.json with subject commit = <Phase 3AR-A SHA>
  - clean_clone_verified = true
  - final_ready = false (MANDATORY)
  - Zero production code edits
  - Commit & Push to origin/main
        ↓
HALT FOR USER REVIEW (No release tag created)
```

---

## 13. Phase 3AR Readiness Summary (12 Conditions)

| Condition # | Gate Name | Type | Target Criteria | Status |
|---|---|---|---|---|
| **Condition 1** | Phase 2 Master Verifier | Internal | 27 audit sections, Go race tests, differentials | **PASS** |
| **Condition 2** | Source Provenance Audit | Internal | 324 funcs, 0 UNKNOWN, structural locators verified | **PASS** |
| **Condition 3** | Contamination & History Audit | Internal | 0 forbidden traces, post-remediation clean | **PASS** |
| **Condition 4** | Original Artifacts Inventory | Internal | 155/155 classified, 65/65 required hash-verified | **PASS** |
| **Condition 5** | Frozen Contract Historical Pinning | Internal | 15/15 git-blob & disk hashes verified | **PASS** |
| **Condition 6** | Toolchain Manifest & Policy | Internal | Zero hardcoded paths, required compilers valid | **PASS** |
| **Condition 7** | Cross-Phase Fact Matrix | Internal | 6 DataChannels verified with canonical facts | **PASS** |
| **Condition 8** | Android DEX Method Count | Internal | 1,625 = 1,061 defined + 564 non-defined | **PASS** |
| **Condition 9** | Intentional Divergences Registry | Internal | Camera 127.0.0.1:9001, deferred boundaries explicit | **PASS** |
| **Condition 10**| Negative Mutation Suite | Internal | 18/18 fail-closed mutations rejected | **PASS** |
| **Condition 11**| Working Tree Cleanliness | Internal | git status --porcelain strictly empty | **PENDING COMMIT** |
| **Condition 12**| Independent Clean-Clone | External | Fresh clone of 3AR-A passes all verifiers | **PENDING STAGE-B** |

### Phase 3AR Status: **STAGE-A VERIFIED — READY FOR COMMIT & INDEPENDENT CLEAN CLONE**
Release readiness: `clean_clone_verified = false`, `final_ready = false`.
Release tag `cleanroom-v1.0.0` is strictly NOT created in Phase 3AR.
