# Forensic Report 25R: Phase 2C.3HR License Local-Crypto & Contract Closure

**Status**: VERIFIED & AUDITED (Master Verifier Phase 2: PASS)  
**Target Binary**: `webrtc-signaling` (Linux AMD64 SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)  
**Cleanroom Package**: `pkg/license`, `pkg/types`, `pkg/httpapi`  
**Cumulative Verification**: **287/287 PASS (100%)** across all 10 canonical differential suites  
**Phase 2C.3HR License Differential Result**: **61/61 PASS (100%)** (expanded from 26 to 61 cases)  
**Phase 2C.1 Persistence Differential Result**: **8/8 PASS (100%)**  
**Cleanroom Provenance Compliance**: **147/147 functions PASS (100%)**  
**Success Classification**: `UNOBSERVED_LOCAL_VALID_SIGNATURE_SUCCESS`  

---

## 1. Executive Summary

Phase 2C.3HR executes the definitive closure of the License & Entitlement subsystem, resolving all architectural, cryptographic, wire, and provenance gaps identified during forensic review.

Key accomplishments:
1. **Exact Machine ID Parity (`main.ZbJsqTIiz3ML`)**: Recovered the 5-step hardware derivation algorithm (system UUID candidate files + filtered non-virtual network interfaces + CPU core count + SHA-256 formatting). Reconstructed code produces character-for-character exact match on the host system: `8AD9-A7EF-87FB-E780`.
2. **Faithful Local Ed25519 Public Verifier (`main.PmtRXo`)**: Fully reconstructed the offline cryptographic validation pipeline using the embedded 32-byte Ed25519 public key (`7317bed38cc0d96bd5ff35c48fc57822083757823ebac181e4ad0b08e460e820`, deobfuscated via byte-wise XOR `0x5a`). The 6-step pipeline reproduces exact error diagnostics (`"授权码格式错误"`, `"非法的 Base64 编码"`, `"数字签名格式无效"`, `"授权数字签名校验失败，可能已被篡改"`, `"机器码不匹配"`).
3. **Startup License File Matrix (`main.LvbcDRl_uhc4`)**: Differential probing confirmed that unverified or corrupted `license.txt` files gracefully degrade to built-in promotional entitlement without mutating the file or setting `status=expired`.
4. **Online Devices Calculation (`main.fWkBbskiJi`)**: Binary disassembly of struct offset `0x35` (`Ihq7ZEVc`, bool) proved that `current_devices` counts online devices only.
5. **Wire Protocol Parity (HEAD & /debug/license)**: Restored byte-exact `Content-Length: 277` on bodyless HEAD requests and permissive 7-verb handling on `/debug/license` without CORS headers.
6. **Strict Cleanroom Invariants**: ZERO keygen, ZERO private key recovery, ZERO signature forgery, ZERO validation bypass. Unobserved successful activation remains strictly classified as `UNOBSERVED_LOCAL_VALID_SIGNATURE_SUCCESS`.

---

## 2. Cryptographic Architecture & Verifier Reconstruction

### 2.1 Embedded Ed25519 Public Key Evidence
Through disassembly of `main.PmtRXo` (`0x733c40`), 4 `movabs` instructions load 64-bit constants that are subsequently XORed with `0x5a`:

```
0x733cfc: movabs rdx, 0x31839ad689e44d29
0x733d06: movabs rdx, 0x78229fd59e6fa58f
0x733d10: movabs rdx, 0xdb9be064d80d6d52
0x733d1a: movabs rdx, 0x7ab23abe5251f7be
```

XOR `0x5a` deobfuscation produces the 32-byte Ed25519 public key:
- **Hex**: `7317bed38cc0d96bd5ff35c48fc57822083757823ebac181e4ad0b08e460e820`
- **Base64**: `cxe+04zA2WvV/zXEj8V4Igg3V4I+usGB5K0LCORg6CA=`
- **SHA256 Fingerprint**: `4ec41f373e3d920fb155df761a8cd47b453659a8aeba799f46818ac3575dd91c`
- **Callee**: `ETQ5mBYyCQ.HER71Q` (`0x52ae40`, standard Go mapping: `crypto/ed25519.VerifyWithOptions`)

### 2.2 Reconstructed Validation Pipeline
The verifier pipeline in `pkg/license/manager.go` faithfully replicates all 6 binary steps:

| Step | Operation | Binary Call / Instruction | Failure Diagnostic |
|---|---|---|---|
| 1 | Trim & Split | `strings.TrimSpace`, `strings.Split(s, ".")` (must be 2 parts) | `授权码格式错误` |
| 2 | Base64 Decode Payload | `base64.StdEncoding.DecodeString(parts[0])` | `非法的 Base64 编码` |
| 3 | Hex Decode Signature | `hex.DecodeString(parts[1])` (must be exactly 64 bytes) | `数字签名格式无效` |
| 4 | Ed25519 Verify | `ed25519.VerifyWithOptions(pubKey, payloadBytes, sigBytes, ...)` | `授权数字签名校验失败，可能已被篡改` |
| 5 | JSON Claims Unmarshal | `json.Unmarshal(payloadBytes, &claims)` (struct descriptor `0x7ed2a0`) | `无效的授权声明内容` |
| 6 | Machine ID Binding | `claims.machine_id == manager.machineID` | `机器码不匹配: 授权绑定 %s, 当前系统为 %s` |

### 2.3 Claims Struct Layout (Descriptor `0x7ed2a0`)
Recovered from ELF type descriptors (56 bytes):
```go
type licenseClaims struct {
    MachineID  string `json:"machine_id"` // offset 0 (16B) - FLdrjU
    MaxDevices int    `json:"max_devices"`// offset 16 (8B) - FzadFNPQCB
    ExpiresAt  string `json:"expires_at"` // offset 24 (16B) - TF9svpC2ha
    Customer   string `json:"customer"`   // offset 40 (16B) - M6ofLo6ey
}
```

---

## 3. Hardware Machine ID Derivation (`main.ZbJsqTIiz3ML`)

Disassembly of `main.ZbJsqTIiz3ML` (`0x732ec0`, 3456 bytes) revealed the deterministic machine fingerprinting algorithm:

1. **System UUID**: Scans `/sys/class/dmi/id/product_uuid`, `/etc/machine-id`, `/var/lib/dbus/machine-id`. Takes the first accessible non-empty value.
2. **Network MAC Addresses**: Calls `net.Interfaces()`. Excludes loopback (`flags & 4 != 0`) and interfaces whose lowercased name begins with any of 13 prefixes: `utun`, `tun`, `tap`, `docker`, `veth` (which matches Hyper-V `vEthernet`), `br-`, `bridge`, `awdl`, `llw`, `p2p`, `gif`, `stf`, `vlan`. Normalizes MACs to colon-separated lowercase hex, sorts lexicographically with `sort.Strings`, and joins with comma.
3. **CPU Cores**: Formats core count as `cores:%d` (`runtime.NumCPU()`).
4. **Hashing & Formatting**:
   - Joins components with pipe separator: `uuid|macs|cores`.
   - Computes `crypto/sha256.Sum256`.
   - Takes first 16 hex characters (`hexStr[0:16]`).
   - Formats into 4 groups of 4 characters: `%s-%s-%s-%s`.
   - Converts to uppercase (`strings.ToUpper`).

**Host Parity Verification**:
- Original Oracle: `8AD9-A7EF-87FB-E780`
- Reconstructed Engine: `8AD9-A7EF-87FB-E780`
- Result: **CHARACTER-FOR-CHARACTER BIT-EXACT MATCH (HIGH CONFIDENCE)**

---

## 4. Startup License File Matrix (`main.LvbcDRl_uhc4`)

Differential probing against the original daemon across 6 startup file configurations demonstrated that the server never crashes or corrupts file state on invalid license input:

| Case ID | Scenario | File State | Resulting Source | Resulting Status | License File Mutated? | Parity |
|---|---|---|---|---|---|---|
| `STARTUP-LIC-01` | No License File | Missing | `built-in` | `valid` | No | **MATCH** |
| `STARTUP-LIC-02` | Empty File | 0 bytes | `built-in` | `valid` | No | **MATCH** |
| `STARTUP-LIC-03` | Whitespace File | ` \n\t \n` | `built-in` | `valid` | No | **MATCH** |
| `STARTUP-LIC-04` | Invalid Plaintext | `not-a-valid-license` | `built-in` | `valid` | No | **MATCH** |
| `STARTUP-LIC-05` | Malformed Base64 | `!!!bad-base64!!!.sig` | `built-in` | `valid` | No | **MATCH** |
| `STARTUP-LIC-06` | Invalid Ed25519 Sig | valid base64, bad sig | `built-in` | `valid` | No | **MATCH** |

In all 6 cases, the daemon logs the diagnostic and retains built-in promotional entitlement (`license_source: "built-in"`, `promo: true`, `max_devices: 20`, `post_promo_max_devices: 10`).

---

## 5. Differential Verification Results (61/61 PASS)

The differential test suite (`tests/differential/license/test_license_http_diff.py`) was expanded from 26 to 61 cases:

- **Baseline HTTP REST Contract (Cases 1–19)**: 19/19 PASS
- **Exact Machine ID Parity (Case G)**: 1/1 PASS
- **HEAD Representation Headers (Case H)**: 1/1 PASS (`Content-Length: 277`, wire bodyless)
- **`/debug/license` Verb Parity (Cases D1–D14)**: 14/14 PASS (7 verbs with `-debug`, 7 verbs without `-debug`)
- **JSON Parser Edge Cases (Cases J1–J10)**: 10/10 PASS (null body, arrays, unicode, numbers, nested objects)
- **Cryptographic Failure Diagnostics (Cases C1–C4)**: 4/4 PASS (format, base64, sig length, signature verification)
- **Live Startup File Matrix (Cases S1–S6)**: 6/6 PASS (missing, empty, whitespace, text, base64, signature)
- **Other Edge Invariants (Cases 20–25)**: 6/6 PASS

**Total License Pass Rate**: **61/61 PASS (100%)**

---

## 6. Dynamic Cumulative Differential Denominator Audit

Section 15.10 dynamically audits all 10 canonical differential suites in the repository:

| Suite | Domain | Artifact Path | Passed | Total | Rate |
|---|---|---|---|---|---|
| 1 | Auth Core | `evidence/go_signaling/auth/AUTH_DIFFERENTIAL_RESULTS.json` | 12 | 12 | 100% |
| 2 | Auth HTTP | `evidence/go_signaling/http/AUTH_HTTP_DIFFERENTIAL_RESULTS.json` | 18 | 18 | 100% |
| 3 | Devices | `evidence/go_signaling/devices/DEVICE_HTTP_DIFFERENTIAL_RESULTS.json` | 28 | 28 | 100% |
| 4 | Users / Admin | `evidence/go_signaling/users/USER_ADMIN_HTTP_DIFFERENTIAL_RESULTS.json` | 30 | 30 | 100% |
| 5 | Device Tags | `evidence/go_signaling/tags/TAG_HTTP_DIFFERENTIAL_RESULTS.json` | 20 | 20 | 100% |
| 6 | Shares | `evidence/go_signaling/shares/SHARE_HTTP_DIFFERENTIAL_RESULTS.json` | 36 | 36 | 100% |
| 7 | Shortcuts | `evidence/go_signaling/shortcuts/SHORTCUT_HTTP_DIFFERENTIAL_RESULTS.json` | 19 | 19 | 100% |
| 8 | Server Config | `evidence/go_signaling/server_config/SERVER_CONFIG_HTTP_DIFFERENTIAL_RESULTS.json` | 55 | 55 | 100% |
| 9 | License REST | `evidence/go_signaling/license/LICENSE_HTTP_DIFFERENTIAL_RESULTS.json` | 61 | 61 | 100% |
| 10 | Persistence | `evidence/go_signaling/persistence/PERSISTENCE_DIFFERENTIAL_RESULTS.json` | 8 | 8 | 100% |
| **TOTAL** | **All Domains** | **10 Canonical Differential Test Suites** | **287** | **287** | **100%** |

---

## 7. Artifact Manifest (17/17 Canonical Evidence Files)

The `evidence/go_signaling/license/` directory contains 17 validated forensic artifacts:
1. `LICENSE_ROUTE_FAMILY.json`
2. `LICENSE_ROUTE_METHOD_MATRIX.json`
3. `LICENSE_AUTH_MATRIX.json`
4. `LICENSE_TYPE_EVIDENCE.json`
5. `LICENSE_STATUS_CONTRACT.json`
6. `LICENSE_ACTIVATION_REJECTION_CONTRACT.json`
7. `LICENSE_PERSISTENCE_CONTRACT.json`
8. `LICENSE_VALIDATION_FUNCTION_SLICES.json`
9. `LICENSE_NETWORK_DEPENDENCY.json`
10. `LICENSE_FAILED_ACTIVATION_STATE_MATRIX.json`
11. `LICENSE_PUBLIC_VERIFIER_EVIDENCE.json`
12. `LICENSE_CRYPTO_VERIFICATION_CONTRACT.json`
13. `LICENSE_CRYPTO_FUNCTION_SLICES.json`
14. `LICENSE_SUCCESS_PATH_STATIC_CONTRACT.json`
15. `LICENSE_MACHINE_ID_CONTRACT.json`
16. `LICENSE_STARTUP_FILE_MATRIX.json`
17. `LICENSE_CURRENT_DEVICES_CROSS_CONTRACT.json`

Plus verification summaries:
- `LICENSE_FORENSIC_GATE_RESULT.json` (17/17 invariants PASS)
- `LICENSE_HTTP_DIFFERENTIAL_RESULTS.json` (61/61 cases PASS)

---

## 8. Conclusion & Scope Boundary Hard Stop

With **287/287 cumulative differential cases passing (100%)**, zero keygen/bypass violations, exact machine ID parity, local Ed25519 verification, startup file resilience, and 100% function provenance compliance, **Phase 2C.3HR is formally COMPLETE and CLOSED**.

Per user instruction, a **HARD STOP** is observed before initiating Phase 2C.3I (Files/Tasks) or WebSocket/WebRTC transports.
