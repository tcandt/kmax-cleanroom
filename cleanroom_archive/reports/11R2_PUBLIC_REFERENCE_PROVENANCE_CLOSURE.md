# Forensic Report 11R2: Public Reference Provenance Closure & Evidence-Derived Reproduction (Phase 2R.2)

**Phase**: 2R.2 (Remediation & Provenance Closure)  
**Status**: VERIFIED & REPRODUCIBLE (Master Gate: PASS)  
**Historical Continuity**: Reports 11 and 11R are preserved in repository history as sequential forensic milestones.

---

## 1. Executive Summary & Forensic Context

Phase 2R established the Lane A / Lane B clean-room separation to ingest public reference frontend intelligence (`tcandt/scrcpyoverwebrtc`) and architecture documentation (`hqw700/cloudphone-official`) without contaminating reconstructed backend code. Phase 2R.1 normalized canonical binary identities, separated supplemental build artifacts (`agentd/cloudphone-agent-amd64`), removed unobserved timeouts, and standardized coverage numerators/denominators.

However, forensic audit revealed a critical **provenance blocker**: the 8 frontend files under `evidence/reference/raw/web-app/` were originally materialized from an unpinned dirty local checkout (`79201f4...`) rather than the pinned public GitHub commit (`65567d777bccb11d2a6d93b6acc735478e880b5b`), resulting in Git blob SHA mismatches against upstream public repository trees. Furthermore, extraction and crossmap scripts relied largely on deterministic dictionary generation rather than authentic forensic parsing of raw source and binary bytes.

**Phase 2R.2 completes the forensic closure of the reference evidence pipeline:**
1. **Public Git Pinning**: Rematerialized all 8 frontend reference files directly from public GitHub commit `65567d777bccb11d2a6d93b6acc735478e880b5b` and 4 documentation files from `ceb66b20ad4c6f7b217d38852ea9ec2bd70fcd39`.
2. **Git Blob SHA1 Verification**: Verified all 12 raw files against `git_blob_sha = SHA1(b"blob " + decimal_size + b"\0" + raw_bytes)` matching the exact Git commit tree.
3. **Audit Record Preservation**: Updated `evidence/reference/REFERENCE_ACCESS_AUDIT.json` documenting the historical dirty checkout as `REJECTED_AS_CANONICAL_REFERENCE` due to `LOCAL_COMMIT_MISMATCH` and superseded by `PINNED_PUBLIC_GIT_REFERENCE`.
4. **Authentic Forensic Extractors**: Replaced template dictionary scripts with dynamic parsers (`extract_protocol_index.py`, `extract_datachannels.py`, `extract_signaling_state_machine.py`, `extract_agent_cli.py`).
5. **Granular Manual Annotations**: Created `evidence/reference/REFERENCE_ANNOTATIONS.json` binding manual semantic interpretations to exact line ranges and SHA256 hashes of raw source slices.
6. **Evidence-Derived Crossmap**: Converted `build_reference_crossmap.py` to dynamically ingest `ROUTE_HANDLER_MAP.json`, `clean_oracle_results.json`, `AUTH_HTTP_DIFFERENTIAL_RESULTS.json`, and scan canonical binary bytes for exact string offsets.
7. **Login Differential Alignment**: Fixed `/api/login` crossmap claim by dynamically binding to `AUTH_HTTP_DIFFERENTIAL_RESULTS.json:HTTP-01,HTTP-02,HTTP-03` (`valid -> 200 OK`, `invalid password -> 401 Unauthorized`, `missing credentials -> 400 Bad Request`).
8. **State Machine T06 Revalidation**: Confirmed that `useWebRTC.js` at commit `65567d7` does NOT contain an outbound `webrtc_failed` message; marked fallback as local reactive error state and `outbound_webrtc_failed` as `NOT_OBSERVED_IN_PINNED_SOURCE`.
9. **Zero-Diff Multi-Category Reproducibility**: `reproduce_reference_evidence.py` reports independent passes for source extraction, binary scanning, annotation stability, and crossmap evidence resolution.
10. **Zero Backend Modifications**: Zero bytes modified in `reconstructed_source/`. Reconstructed source remains clean and unpolluted.

---

## 2. Public Git Tree Manifest & Exact Blob Verification

All 12 reference files stored under `evidence/reference/raw/` have been rematerialized and verified against their upstream Git commit tree:

```
git_blob_sha = SHA1(b"blob " + str(len(raw_bytes)).encode("ascii") + b"\0" + raw_bytes)
```

| Component | Relative Path | Public Repository & Pinned Commit | Size (B) | Lines | Expected Git Blob SHA | Computed Git Blob SHA | Verification |
|---|---|---|---|---|---|---|---|
| WebRTC Client | `web-app/src/composables/useWebRTC.js` | `tcandt/scrcpyoverwebrtc@65567d7` | 52,011 | 1,622 | `cb6b0451b0640d9c787f567fd97b54c621ca4da0` | `cb6b0451b0640d9c787f567fd97b54c621ca4da0` | **MATCH** |
| WS Stream Client | `web-app/src/composables/useWebSocketStream.js` | `tcandt/scrcpyoverwebrtc@65567d7` | 23,366 | 807 | `c9c48f42d326b9b3e226957501b4c3fd5b152513` | `c9c48f42d326b9b3e226957501b4c3fd5b152513` | **MATCH** |
| Device Store | `web-app/src/stores/devices.js` | `tcandt/scrcpyoverwebrtc@65567d7` | 34,124 | 1,048 | `42867285c44074de0b5cab05d32742f03267609a` | `42867285c44074de0b5cab05d32742f03267609a` | **MATCH** |
| Auth Store | `web-app/src/stores/auth.js` | `tcandt/scrcpyoverwebrtc@65567d7` | 5,796 | 188 | `c6d2238fed65c3bdb0f274fcfd710b86be16bc61` | `c6d2238fed65c3bdb0f274fcfd710b86be16bc61` | **MATCH** |
| Tags Store | `web-app/src/stores/tags.js` | `tcandt/scrcpyoverwebrtc@65567d7` | 7,227 | 276 | `1146339c52c1ff69dc691d6c9f5f03718a0ef1b8` | `1146339c52c1ff69dc691d6c9f5f03718a0ef1b8` | **MATCH** |
| Main Client View | `web-app/src/views/DeviceClient.vue` | `tcandt/scrcpyoverwebrtc@65567d7` | 117,820 | 3,263 | `77c093d90f42feb83d0ef8152f3ddb63f8f4a170` | `77c093d90f42feb83d0ef8152f3ddb63f8f4a170` | **MATCH** |
| Demo Engine | `web-app/src/demo/demoEngine.js` | `tcandt/scrcpyoverwebrtc@65567d7` | 11,158 | 329 | `a714202cff9c5f2cf57453924a2380d590e2c91f` | `a714202cff9c5f2cf57453924a2380d590e2c91f` | **MATCH** |
| Demo Env | `web-app/.env.demo` | `tcandt/scrcpyoverwebrtc@65567d7` | 77 | 2 | `029cb11855199810684b48d1d5ba4a45f1a09a61` | `029cb11855199810684b48d1d5ba4a45f1a09a61` | **MATCH** |
| Architecture Doc | `docs/architecture.md` | `hqw700/cloudphone-official@ceb66b2` | 6,561 | 240 | `233c7fa98897ee1fa44f479fdfa1961ee4d4f29a` | `233c7fa98897ee1fa44f479fdfa1961ee4d4f29a` | **MATCH** |
| Agent Deploy Doc | `docs/agent-deploy.md` | `hqw700/cloudphone-official@ceb66b2` | 4,271 | 185 | `43926831e7bbfe6b2a4778393c5979eb170d1991` | `43926831e7bbfe6b2a4778393c5979eb170d1991` | **MATCH** |
| Quickstart Doc | `docs/quickstart.md` | `hqw700/cloudphone-official@ceb66b2` | 3,923 | 165 | `a84cb954dae2aeefd17d5c760a927063f2537617` | `a84cb954dae2aeefd17d5c760a927063f2537617` | **MATCH** |
| Project Index Doc | `docs/index.md` | `hqw700/cloudphone-official@ceb66b2` | 2,893 | 120 | `e50c4aa30560b4ef4255ca8c531d05451994e098` | `e50c4aa30560b4ef4255ca8c531d05451994e098` | **MATCH** |

Generated canonical manifest: `evidence/reference/PUBLIC_REFERENCE_TREE_MANIFEST.json`.

---

## 3. Reference Access Audit Update

The reference access audit in `evidence/reference/REFERENCE_ACCESS_AUDIT.json` was updated to maintain strict historical record of the provenance defect and its remediation:

```json
{
  "audit_version": "2.0",
  "historical_input_status": "REJECTED_AS_CANONICAL_REFERENCE",
  "reason": "LOCAL_COMMIT_MISMATCH",
  "historical_details": "Local working copy at 79201f47490e627be7d147e533adaadb1d532ba2 was dirty and diverged from pinned public commit 65567d777bccb11d2a6d93b6acc735478e880b5b.",
  "replacement": "PINNED_PUBLIC_GIT_REFERENCE",
  "canonical_tree_manifest": "evidence/reference/PUBLIC_REFERENCE_TREE_MANIFEST.json",
  "allowed_reference_lane": "evidence/reference/raw/"
}
```

---

## 4. Evidence-Driven Extraction vs. Hard-Coded Generation

All extractor tools were rewritten to parse raw source text and scan binary bytes directly:

1. **`tools/reference/extract_protocol_index.py`**:
   - Parses regex `['"`](/(?:api|connect_client|register_agent)[^'"`\s?#]*)` across `web-app/` JS/Vue files.
   - Extracts all WebSocket send payloads, incoming dispatch messages, and demo isolation paths.
2. **`tools/reference/extract_datachannels.py`**:
   - Parses `pc.createDataChannel` labels (`file-channel`, `ai-command-channel`, `adb-channel`) and options (`{ ordered: true }`).
   - Parses `binaryType` assignments (`arraybuffer`).
   - Parses `pc.ondatachannel` event branches (`input-channel`, `clipboard-channel`, `camera-channel`).
   - Extracts JSON event payloads for `touch` and `inject_scroll`.
3. **`tools/reference/extract_signaling_state_machine.py`**:
   - Scans `useWebRTC.js` for default command timeout: detects `timeoutMs = 15000`.
   - Checks presence of `webrtc_failed` outbound message: confirms absent in commit `65567d7` (`outbound_webrtc_failed = "NOT_OBSERVED_IN_PINNED_SOURCE"`).
4. **`tools/reference/extract_agent_cli.py`**:
   - Scans canonical ARM64 `cloudphone-agent` and supplemental AMD64 `cloudphone-agent-amd64` bytes directly.
   - Records exact file offsets and occurrence counts for flag names and environment fallbacks (`CP_AGENT_ID`, `CP_AGENT_ROOT`).
5. **`tools/reference/build_reference_crossmap.py`**:
   - Dynamically loads `ROUTE_HANDLER_MAP.json` to resolve route VAs and symbols.
   - Dynamically loads `clean_oracle_results.json` and `AUTH_HTTP_DIFFERENTIAL_RESULTS.json` to resolve oracle observations.
   - Scans binary bytes for string offsets and SHA256 integrity.

---

## 5. Resolution of Crossmap Inconsistencies & Login Binding

### 5.1 Corrected Login Differential Binding
Previously, the crossmap hardcoded an inaccurate claim that invalid login returns `400`. The actual verified differential results in `AUTH_HTTP_DIFFERENTIAL_RESULTS.json` establish:

- **`HTTP-01`**: Valid credentials -> `200 OK` (schema: `assigned_devices`, `role`, `token`, `username`; 64-char lowercase hex token).
- **`HTTP-02`**: Invalid password -> `401 Unauthorized` (`Invalid username or password\n`, `text/plain; charset=utf-8`).
- **`HTTP-03`**: Missing credentials -> `400 Bad Request` (`Username and password are required\n`).
- **`HTTP-04`**: Expired account -> `403 Forbidden` (`账号已到期，请联系管理员延时\n`).
- **`HTTP-05`**: Malformed JSON -> `400 Bad Request` (`Invalid JSON\n`).

`build_reference_crossmap.py` now binds directly to `AUTH_HTTP_DIFFERENTIAL_RESULTS.json:HTTP-01,HTTP-02,HTTP-03` with observed status codes and bodies extracted from the differential artifact.

### 5.2 Unconfirmed Binary Evidence Demotion
- **`channel: file-channel`**: Present in reference frontend (`useWebRTC.js:579`), but string search in canonical `cloudphone-agent` returns not found. Correctly classified as `UNCONFIRMED_HYPOTHESIS`.
- **`payload: request-offer`**: Present in reference frontend (`useWebRTC.js:134`), but isolated string literal not present in agent binary. Correctly classified as `UNCONFIRMED_HYPOTHESIS`.

---

## 6. Comprehensive Forensic Metrics

| Metric Identifier | Exact Numerator / Denominator | Metric Value | Classification |
|---|---|---|---|
| `SIGNALING_FUNCTION_TABLE_COVERAGE` | 7571 / 7571 | 100.0% | Complete Invariant |
| `AGENT_FUNCTION_TABLE_COVERAGE` | 15398 / 15398 | 100.0% | Complete Invariant |
| `ROUTE_DISCOVERY_COVERAGE` | 43 / 43 | 100.0% | Complete Invariant |
| `FRONTEND_ROUTE_BINARY_MATCH` | 35 / 37 | 94.6% | Evidence-Backed |
| `RECONSTRUCTED_ROUTE_COUNT` | 4 / 43 | 9.3% | Exact Measured Count |
| `IMPLEMENTED_SURFACE_DIFFERENTIAL_PASS_RATE` | 38 / 38 | 100.0% | Exact Differential Pass |
| `ESTIMATED_FUNCTIONAL_RECONSTRUCTION_PROGRESS` | ~15–20% | ESTIMATE | Qualitative Functional Scope |

---

## 7. True Reproducibility Audit Results

Running `tools/reference/reproduce_reference_evidence.py` regenerates all 5 reference artifacts into a clean temporary directory and audits output bit-for-bit:

```text
[PASS] SOURCE_EXTRACTION_REPRODUCIBLE: True
[PASS] BINARY_EVIDENCE_REPRODUCIBLE:   True
[PASS] ANNOTATION_STABLE:              True
[PASS] CROSSMAP_REPRODUCIBLE:          True
==================================================
REPRODUCIBILITY VERDICT: PASS
==================================================
```

---

## 8. Verification & Gate Checklist

| Item | Requirement | Verification Result |
|---|---|---|
| Public Reference Commits | Pinned to resolvable commits (`65567d7`, `ceb66b2`) | **PASS** |
| Git Blob SHAs | All 12 raw files match computed Git blob SHAs | **PASS** |
| Dirty Checkout Purge | Local dirty checkout rejected; audit updated | **PASS** |
| Dynamic Source Extraction | Extracted dynamically from raw reference files | **PASS** |
| Dynamic Binary Scanning | Flag offsets scanned directly in binary | **PASS** |
| Crossmap Resolution | All evidence records resolve to underlying artifacts | **PASS** |
| Login Contract Parity | 401 vs 400 bound to `AUTH_HTTP_DIFFERENTIAL_RESULTS.json` | **PASS** |
| State Machine T06 | Verified no `webrtc_failed` in commit `65567d7` | **PASS** |
| Persistence Regression | 8/8 test cases pass | **PASS** |
| Auth Core Regression | 12/12 test cases pass | **PASS** |
| Auth HTTP Differential | 18/18 test cases pass | **PASS** |
| Cleanroom Source Provenance | 59/59 functions audited pass | **PASS** |
| Scope Boundary | Zero lines in `reconstructed_source/` touched | **PASS** |

---

## 9. Conclusion

Phase 2R.2 establishes an immutable, evidence-derived, publicly pinned reference foundation. The reference evidence pipeline is fully verified, reproducible, and ready to guide Phase 2C.3B (Devices/Registry REST) upon user authorization.
