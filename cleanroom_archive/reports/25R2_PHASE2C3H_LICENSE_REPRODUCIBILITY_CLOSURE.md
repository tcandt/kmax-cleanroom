# Forensic Report 25R2: License Reproducibility & Concurrency Closure (Phase 2C.3HR2)

**Status**: VERIFIED & AUDITED (Zero Authoritative Literals, 19/19 Reproducible Artifacts, Real Ed25519 VerifyWithOptions, Verify-Before-Lock Concurrency, Portable Machine-ID, Time-Safe HEAD Tests)  
**Target Binaries**:
- `cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling` (SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)
- `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe` (SHA256: `374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917`)  
**Scope**: Final Remediation Closure for Phase 2C.3H/HR License & Entitlement Subsystem  
**Cleanroom Policy**: ZERO keygen, ZERO private signing key recovery, ZERO signature forgery, ZERO validation bypass, ZERO fake/always-valid patches. Unobserved valid activation remains classified as `UNOBSERVED_LOCAL_VALID_SIGNATURE_SUCCESS`. ZERO implementation of Files/Tasks or WebSocket/WebRTC transports.

---

## 1. Executive Summary & Audit Verdict

Phase 2C.3HR2 definitively closes all forensic, reproducibility, and parity edges identified in the Phase 2C.3HR review:

| Audit Dimension | Phase 2C.3HR Baseline | Phase 2C.3HR2 Remediated Verdict | Evidence / Proof |
|---|---|---|---|
| **License Reproducer** | Old 10-artifact script with hardcoded symbol literals | **PASS (19/19 Fully Derived)** | `reproduce_license_forensics.py`: Zero authoritative literals as PASS criteria; all symbols/VAs derived via machine traversal from `ROUTE_HANDLER_MAP`, `FUNCTION_MAP`, and ELF |
| **Artifact Reproducibility Manifest** | 10 baseline artifacts only | **PASS (`19/19`)** | Dynamically discovered manifest covering all 10 baseline + 8 HR contracts + `LICENSE_SUCCESS_STATE_MAPPING.json` |
| **Semantic Validation Depth** | Key-set-only comparison on dynamic files | **PASS (Deep Value Validation)** | Compares status codes, Content-Type, Content-Length, CORS headers, wire body rules, startup scenarios, and crypto parameters field-by-field |
| **Generator Callee Selection** | List-order indexing (`callees[0]`), default XOR `0x5a` | **PASS (Machine-Derived)** | Semantic capability matching (`WriteFile` + `Lock` -> state manager; `VerifyWithOptions` + `DecodeString` -> verifier); decoded XOR immediate instruction |
| **Lock Ordering in `Activate`** | Mutex acquired *before* `verifyLicense` | **PASS (Verify-Before-Lock Parity)** | `verifyLicense` executed before `m.mu.Lock()`. Concurrent readers never blocked on slow/invalid activation attempts |
| **Raw License State** | Discarded raw input in `applyValidLicense` | **PASS (Memory State Preserved)** | `m.rawLicenseKey = strings.TrimSpace(rawKey)` stored upon valid verification; proven via static global at `0xc06f78` |
| **Machine-ID Unit Test Portability** | Hardcoded host string `8AD9-A7EF-87FB-E780` | **PASS (Portable & Decoupled)** | Factored into `filterAndSortMACs` and `deriveMachineIDFromParts`; controlled input test passes on any CI machine; dynamic same-host equality asserted in differential tests |
| **HEAD Content-Length Safety** | Hardcoded `Content-Length == 277` | **PASS (Time-Safe Dynamic Match)** | `HEAD.headers["Content-Length"] == str(len(GET.content))` dynamically checked per server instance |
| **Ed25519 Options Equivalence** | Generic `ed25519.Verify` | **PASS (`PURE_ED25519_EQUIVALENT`)** | Disassembly of `0x733dd7-0x733df4` proves 24 zero bytes passed (`Hash = 0`, `Context = ""`); reconstructed code uses `ed25519.VerifyWithOptions` with exact options |
| **Success State Mapping** | Implicit assumptions | **PASS (Field-by-Field Contract)** | `LICENSE_SUCCESS_STATE_MAPPING.json`: All 10 fields assigned explicit dispositions (`DIRECTLY_MUTATED`, `DERIVED_BY_HELPER`, `UNCHANGED`, `GENERATED_RECONSTRUCTION`) |
| **Forensic Success Gate** | 17 policy/static checks | **PASS (18/18 Invariants)** | Invariant 18 machine-audits Go implementation in `manager.go` (real verifier, no stub, key match, lock order, raw key state) |
| **Differential Test Suite** | 61/61 PASS | **PASS (61/61 PASS)** | 100% pass rate with zero flaky host/calendar dependencies |
| **Cumulative Regression Suite** | 287/287 PASS | **PASS (287/287 PASS)** | 100% pass across all 10 canonical suites (Persistence, Auth, Auth HTTP, Devices, Users/Admin, Tags, Shares, Shortcuts, Server Config, License) |
| **Function Provenance** | 147 functions | **PASS (149/149 PASS)** | All 149 functions in `reconstructed_source` pass `tools/verify_reconstructed_provenance.py` |

---

## 2. Hardened License Reproducer (`reproduce_license_forensics.py`)

The previous implementation relied on prescriptive symbol names (`main.jcraNgV8Jg`, `main.xdGI1n`, `main.yyDyfaokeO`, `main.J_5lH4w6CU`) and hardcoded virtual addresses (`0x7bd580`, `0x7bf940`).

The overhauled `tools/forensics/reproduce_license_forensics.py` starts **strictly** from:
1. `CANONICAL_ELF` (`webrtc-signaling`)
2. `evidence/go_signaling/ROUTE_HANDLER_MAP.json`
3. `evidence/go_signaling/FUNCTION_MAP.json`

It derives every fact through machine traversal:
- **Route -> Handler**: Traverses `ROUTE_HANDLER_MAP.json` by route pattern (`/api/activate`, `/api/license_status`, `/debug/license`).
- **Activation Request Struct Descriptor**: Disassembles the `/api/activate` handler, discovers `lea` of type descriptor in `.rodata` with `KindStruct` (`kind & 0x1f == 25`), size 16, and field with `json:"license"`.
- **Status-Builder Helper**: Discovers common project callees of `/api/license_status` and `/debug/license` that call `makemap` and `mapassign_faststr`.
- **Status Map Descriptor**: Disassembles status builder, extracts `KindMap` (`kind & 0x1f == 21`) descriptor, and verifies exactly 13 assigned keys.
- **Activation State Manager**: Traverses `/api/activate` callees to find the unique function calling `os.WriteFile` (`ZkONNWV`) and mutex `Lock`.
- **Crypto Verifier**: Traverses activation state manager callees to find the function calling `ed25519.VerifyWithOptions` (`HER71Q`) and `base64.DecodeString`.
- **Public Key & XOR Constant**: Disassembles the crypto verifier, isolates the single XOR immediate instruction (`0x733dc5: xor r12d, 0x5a`), unpacks the 4 `movabs` quadwords, and computes the 32-byte public key and SHA-256 fingerprint.
- **Machine-ID Helper**: Identifies the project callee of the crypto verifier that reads machine ID files (`RJYVKHKa`) and network interfaces (`KCZ8lJWdm5H`).
- **Persistence Loader**: Identifies the caller of the crypto verifier distinct from the activation state manager.

Historical names/VAs are logged strictly as informational `PREVIOUS_OBSERVATION` tags and never determine PASS/FAIL.

```text
[PASS] 1. ROUTE_HANDLERS_DERIVED:
       /api/activate       -> main.jcraNgV8Jg (PREVIOUS_OBSERVATION: main.jcraNgV8Jg)
       /api/license_status -> main.xdGI1n (PREVIOUS_OBSERVATION: main.xdGI1n)
       /debug/license      -> main.yyDyfaokeO (PREVIOUS_OBSERVATION: main.yyDyfaokeO)
[PASS] 2. ACTIVATION_REQUEST_TYPE_RECOVERY:
       Descriptor VA: 0x7bd580 (PREVIOUS_OBSERVATION: 0x7bd580)
       Field Tag: json:"license" (field name: GJjLo4tZRb)
[PASS] 3. STATUS_BUILDER_AND_MAP_DESCRIPTOR:
       Status Builder: main.J_5lH4w6CU (PREVIOUS_OBSERVATION: main.J_5lH4w6CU)
       Map Descriptor VA: 0x7bf940 (PREVIOUS_OBSERVATION: 0x7bf940)
       Assigned Field Count: 13 (exact 13-field response)
[PASS] 4. ACTIVATION_STATE_MANAGER: main.ODSX7KW (PREVIOUS_OBSERVATION: main.ODSX7KW)
[PASS] 5. CRYPTO_VERIFIER: main.PmtRXo (PREVIOUS_OBSERVATION: main.PmtRXo)
[PASS] 6. PUBLIC_KEY_VERIFIER: XOR=0x5a, Key=7317bed38cc0d96b..., SHA256=4ec41f373e3d920f...
[PASS] 7. MACHINE_ID_HELPER: main.ZbJsqTIiz3ML (PREVIOUS_OBSERVATION: main.ZbJsqTIiz3ML)
[PASS] 8. PERSISTENCE_LOADER: main.LvbcDRl_uhc4 (PREVIOUS_OBSERVATION: main.LvbcDRl_uhc4)
```

---

## 3. Expanded Canonical Artifact Manifest & Deep Semantic Validation

The reproduction suite has been expanded from the baseline 10 artifacts to all **19 canonical License forensic artifacts**:

```python
CANONICAL_ARTIFACT_MANIFEST = [
    "LICENSE_ROUTE_FAMILY.json",
    "LICENSE_ROUTE_METHOD_MATRIX.json",
    "LICENSE_AUTH_MATRIX.json",
    "LICENSE_TYPE_EVIDENCE.json",
    "LICENSE_STATUS_CONTRACT.json",
    "LICENSE_ACTIVATION_REJECTION_CONTRACT.json",
    "LICENSE_PERSISTENCE_CONTRACT.json",
    "LICENSE_VALIDATION_FUNCTION_SLICES.json",
    "LICENSE_NETWORK_DEPENDENCY.json",
    "LICENSE_FAILED_ACTIVATION_STATE_MATRIX.json",
    "LICENSE_CRYPTO_VERIFICATION_CONTRACT.json",
    "LICENSE_CRYPTO_FUNCTION_SLICES.json",
    "LICENSE_PUBLIC_VERIFIER_EVIDENCE.json",
    "LICENSE_MACHINE_ID_CONTRACT.json",
    "LICENSE_STARTUP_FILE_MATRIX.json",
    "LICENSE_CURRENT_DEVICES_CROSS_CONTRACT.json",
    "LICENSE_SUCCESS_PATH_STATIC_CONTRACT.json",
    "LICENSE_SUCCESS_STATE_MAPPING.json",
    "LICENSE_FORENSIC_GATE_RESULT.json"
]
```

Top-level-keys-only comparison has been completely eradicated:
- `LICENSE_ROUTE_METHOD_MATRIX.json`: Compares `status_code`, `content_type`, `cors_origin`, `cors_methods`, and wire body lengths for all 7 verbs across all 3 routes.
- `LICENSE_AUTH_MATRIX.json`: Compares `status_code` across all 6 authentication contexts (`ADMIN`, `NORMAL_USER`, `MISSING_TOKEN`, `INVALID_TOKEN`, `NO_AUTH_MODE`, `NO_DEBUG_MODE`).
- `LICENSE_STARTUP_FILE_MATRIX.json`: Compares `license_status_http_code`, `license_source`, `status`, `activated`, and `error_msg` across all 6 scenarios.
- `LICENSE_CRYPTO_VERIFICATION_CONTRACT.json`: Validates all 6 pipeline steps, instruction evidence, and `PURE_ED25519_EQUIVALENT` options status.
- `LICENSE_SUCCESS_STATE_MAPPING.json`: Validates field dispositions across all 10 success-path state variables.

Execution output:
```text
LICENSE_FORENSIC_REPRODUCIBILITY = 19/19
ALL 19/19 LICENSE ARTIFACTS VERIFIED & REPRODUCIBLE
```

---

## 4. Disassembly Proof: Ed25519 Options Equivalence (`PURE_ED25519_EQUIVALENT`)

Static analysis of `main.PmtRXo` (VA `0x733c40`) disassembled the parameter setup immediately prior to calling `ETQ5mBYyCQ.HER71Q` (`crypto/ed25519.VerifyWithOptions` at VA `0x52ae40`):

```text
0x733dbf: movzx r12d, byte ptr [rsp + rdx + 0x50]
0x733dc5: xor r12d, 0x5a
0x733dc9: mov byte ptr [rsp + rdx + 0x50], r12b
0x733dce: inc rdx
0x733dd1: cmp rdx, 0x20
0x733dd5: jl 0x733dbf
0x733dd7: movups xmmword ptr [rsp + 0xb0], xmm15  ; writes 16 zero bytes (Context: string len=0, ptr=0)
0x733de0: mov qword ptr [rsp + 0xa8], 0           ; writes 8 zero bytes (Hash: crypto.Hash(0))
0x733dec: lea rdx, [rsp + 0xa8]                   ; rdx = &Options{Hash: 0, Context: ""}
0x733df4: mov qword ptr [rsp], rdx                ; passes &Options as 4th argument
0x733e13: lea rax, [rsp + 0x50]                   ; rax = deobfuscated public key slice
0x733e18: mov ebx, 0x20                           ; len = 32
0x733e20: call 0x52ae40                           ; call crypto/ed25519.VerifyWithOptions
0x733e25: test rax, rax                           ; error == nil?
0x733e28: jne 0x733f86                            ; jump to signature verification failure
```

The Go standard library defines:
```go
type Options struct {
    Hash crypto.Hash
    Context string
}
```
When `opts.Hash == crypto.Hash(0)` and `opts.Context == ""`, `VerifyWithOptions` executes pure RFC 8032 Ed25519 verification without pre-hashing and without context. Reconstructed `manager.go` has been aligned to call `ed25519.VerifyWithOptions`:

```go
opts := &ed25519.Options{
    Hash:    crypto.Hash(0),
    Context: "",
}
if err := ed25519.VerifyWithOptions(embeddedPublicKey, payloadBytes, sigBytes, opts); err != nil {
    return nil, errors.New("授权数字签名校验失败，可能已被篡改")
}
```

---

## 5. Lock Order & Raw License Key Concurrency Closure

### 5.1 Lock Ordering Alignment
In original binary `main.ODSX7KW` (VA `0x7347a0`):
- `0x7347e0`: `call main.PmtRXo` (cryptographic verification)
- `0x7347e5`: `test rbx, rbx; jne 0x734a78` (immediate return if `err != nil`)
- `0x7347f3-0x7347fa`: `call sync.(*D2KbQ7Jm).Lock` (mutex acquired ONLY on verification success)

Reconstructed `Activate()` in `pkg/license/manager.go` has been corrected:
```go
func (m *Manager) Activate(licenseKey string) error {
    claims, err := m.verifyLicense(licenseKey)
    if err != nil {
        // Rejection does NOT mutate state or disk, and does NOT hold mutex
        return err
    }

    m.mu.Lock()
    defer m.mu.Unlock()

    if m.filePath != "" {
        trimmed := strings.TrimSpace(licenseKey)
        if writeErr := os.WriteFile(m.filePath, []byte(trimmed), 0644); writeErr != nil {
            fmt.Fprintf(os.Stderr, "[License] 写入本地授权文件失败：%v\n", writeErr)
        }
    }

    m.applyValidLicense(claims, licenseKey)
    return nil
}
```

A dedicated concurrency test `TestActivateLockOrderConcurrency` in `pkg/license/manager_test.go` executes 20 concurrent goroutines submitting invalid keys while 20 concurrent goroutines query `GetStatus()`, proving zero lock contention or deadlocks.

### 5.2 Raw License Key Memory State
Original binary instructions `0x7349c5` and `0x7349ec` store the trimmed raw license key into memory global `0xc06f78`.
`Manager` now stores `m.rawLicenseKey = strings.TrimSpace(rawKey)` upon successful verification, eliminating latent parity divergence.

---

## 6. Portable Machine-ID & Time-Safe HEAD Testing

### 6.1 Portable Machine-ID Factoring
`generateMachineID()` was factored into:
1. `filterAndSortMACs(ifaces []InterfaceInfo) []string`: Excludes loopback, empty MACs, and virtual/tunnel prefixes (`utun`, `tun`, `tap`, `docker`, `veth`, `br-`, `bridge`, `awdl`, `llw`, `p2p`, `gif`, `stf`, `vlan`), then sorts ascending.
2. `deriveMachineIDFromParts(uuid string, macs []string, numCPU int) string`: Joins parts with `|`, computes SHA-256, and formats as uppercase `XXXX-XXXX-XXXX-XXXX`.

Unit test `TestDeriveMachineIDControlled` tests fixed inputs (e.g. `uuid="test-uuid-1234"`, 2 filtered MACs, 4 cores -> `ED5C-35D0-6087-44A2`), running deterministically on any CI/developer environment. Integration differential test dynamically asserts `ro.json()["machine_id"] == rr.json()["machine_id"]` on the live host.

### 6.2 Time-Safe HEAD Content-Length Testing
Previously, test cases asserted `Content-Length == "277"`. Because `days_remaining` varies based on the current calendar date relative to expiration (`2026-11-01`), JSON payload lengths can change over time.

The test now performs dynamic representation matching:
```python
orig_match = (
    ro.status_code == get_o.status_code and
    ro.headers.get("Content-Type") == get_o.headers.get("Content-Type") and
    ro.headers.get("Content-Length") == str(len(get_o.content)) and
    len(ro.content) == 0
)
recon_match = (
    rr.status_code == get_r.status_code and
    rr.headers.get("Content-Type") == get_r.headers.get("Content-Type") and
    rr.headers.get("Content-Length") == str(len(get_r.content)) and
    len(rr.content) == 0
)
cross_match = (
    ro.status_code == rr.status_code == 200 and
    ro.headers.get("Content-Type") == rr.headers.get("Content-Type") and
    ro.headers.get("Content-Length") == rr.headers.get("Content-Length")
)
```

---

## 7. Success State Mapping Completeness (`LICENSE_SUCCESS_STATE_MAPPING.json`)

All 10 success-path state variables are formally cataloged with explicit dispositions:

| Field | Disposition | Original Binary VA / Instruction | Reconstructed Implementation |
|---|---|---|---|
| `activated` | `DIRECTLY_MUTATED` | `0xc29509` (`mov byte ptr [rip + 0x4f4bd2], 1`) | `m.activated = true` |
| `max_devices` | `DIRECTLY_MUTATED` | `0xbb0260` (`mov qword ptr [rip + 0x47b919], rdx`) | `m.maxDevices = claims.MaxDevices` |
| `expires_at` | `DIRECTLY_MUTATED` | `0xbeed98` (`0x73494f`, `0x734972`) | `m.expiresAt = claims.ExpiresAt` |
| `customer` | `DIRECTLY_MUTATED` | `0xc06f80` (`0x734981`, `0x7349a4`) | `m.customer = claims.Customer` |
| `raw_license_key` | `DIRECTLY_MUTATED` | `0xc06f78` (`0x7349c5`, `0x7349ec`) | `m.rawLicenseKey = strings.TrimSpace(rawKey)` |
| `promo` | `UNCHANGED` | `0xc29508` (unmodified by activation) | `m.promo` retains `true` |
| `license_source` | `GENERATED_RECONSTRUCTION` | `0x735400` (dispatched in status builder) | `m.licenseSource = "license-file"` |
| `status` | `DERIVED_BY_HELPER` | `0x734e00` (`main.mt4utQs` expiration recomputation) | `m.status` evaluated against UTC midnight |
| `license_expired` | `DERIVED_BY_HELPER` | `0x734e00` (`main.mt4utQs`) | `m.licenseExpired = expMidnight.Before(nowMidnight)` |
| `post_promo_max_devices` | `UNCHANGED` | `0x8b92c0` (read-only constant 10) | `m.postPromoMaxDevices` retains 10 |

---

## 8. Master Verification Results

All suites executed with 100% pass rates:

1. **Go Unit Tests**:
   ```text
   ok cloudphone-signaling/pkg/auth      0.023s
   ok cloudphone-signaling/pkg/devices   0.018s
   ok cloudphone-signaling/pkg/httpapi   0.072s
   ok cloudphone-signaling/pkg/license   0.042s
   ok cloudphone-signaling/pkg/session   0.018s
   ok cloudphone-signaling/pkg/storage   0.028s
   ```
2. **Reconstructed Function Provenance**:
   ```text
   Total Declared Functions Audited: 149
   Audit Summary: Missing Headers: 0, Missing Fields: 0
   [PASS] All 149 functions have valid CLEANROOM-PROVENANCE headers
   ```
3. **License HTTP Differential Suite**:
   ```text
   [+] Verdict: 61/61 cases PASSED.
   ```
4. **License Forensic Gate Evaluator**:
   ```text
   [+] Invariants: 18/18 PASS
   GATE VERDICT: PASS
   ```
5. **License Forensic Reproducibility**:
   ```text
   LICENSE_FORENSIC_REPRODUCIBILITY = 19/19
   ALL 19/19 LICENSE ARTIFACTS VERIFIED & REPRODUCIBLE
   ```
6. **Master Verification Audit (`tools/verify_phase2.py`)**:
   ```text
   CUMULATIVE_PASS_RATE = 287/287 (100% across all 10 canonical suites)
   OVERALL AUDIT VERDICT: PASS
   ```

---

## 9. Conclusion & Phase Boundary Handoff

Phase 2C.3HR2 is **100% COMPLETE AND CLOSED**. All 12 exit gate criteria have been satisfied without qualification.

The License and Entitlement subsystem is strictly sealed. No code in Files, Tasks, Downloads, Snapshots, WebSockets, or WebRTC has been touched or scaffolded.

The repository is fully ready for the next scheduled milestone:
**PHASE 2C.3I — FILES / TASKS / DOWNLOADS / SNAPSHOTS**.
