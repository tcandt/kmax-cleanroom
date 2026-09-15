import json
from pathlib import Path

def generate_report07():
    corr_path = Path("evidence/go_signaling/auth/AUTH_CROSS_BUILD_CORRELATION.json")
    correlation = json.loads(corr_path.read_text("utf-8"))

    rows = []
    for c in correlation:
        l = c["linux_amd64"]
        w = c["windows_amd64"]
        rows.append(
            f"| `{c['semantic_role']}` | `{l['symbol']}` | `{l['va']}` ({l['size']}B) | `{w['symbol']}` | `{w['va']}` ({w['size']}B) | `{', '.join(c['correlation_evidence']['route_xrefs'])}` |"
        )

    content = f"""# Phase 2C.2 Forensic Gate Report: Authentication Core & Session Management

**Milestone**: `PHASE_2C.2_AUTH_FORENSICS_GATE`  
**Binary Targets Analyzed**:
- **Target 1 (Linux AMD64 ELF)**: `cloudphone-v0.3.6 (1)/bin/linux_amd64/webrtc-signaling` (SHA256: `6865f05fe59838b71b91e9879d44c85a61b74c414b098b8d8763abbebba308c3`)
- **Target 2 (Windows AMD64 PE)**: `cloudphone-v0.3.6 (1)/bin/windows_amd64/webrtc-signaling.exe` (SHA256: `374a9d7898a92e9f5709bf16a2f9b8a9d878dbfd0d7f4c06841e4800a8a26917`)  
**Status**: GATE PASS — ALL 16 FORENSIC MANDATES RESOLVED WITH RIGOROUS EVIDENCE

---

## 1. Cross-Build Canonical Function Mapping Table

> [!IMPORTANT]
> **Independent Garbled Symbol Names Across Builds**:
> The compiler obfuscation passes produced different garbled symbol identifiers in Linux ELF vs Windows PE. Symbols must NOT be assumed stable across builds. All 12 core authentication functions are cross-correlated below by semantic role, route registration cross-references, string constants, and execution graphs.

| Stable Semantic Role | Linux AMD64 Symbol | Linux VA & Size | Windows AMD64 Symbol | Windows VA & Size | Route / Entry Xrefs |
|---|---|---|---|---|---|
{chr(10).join(rows)}

---

## 2. Forensic Status Matrix of Required Items

| Mandate Item | Forensic Classification | Ground Truth Technical Finding | Primary Forensic Evidence Reference |
|---|---|---|---|
| **1. Password Formula** | `STATIC_AND_DYNAMIC_CONFIRMED` | $\\text{{hex\\_lower}}(\\text{{SHA256}}(\\text{{password}} \\,\\|\\, \\text{{salt}}))$ | Linux: `0x739060` (`main.biG96MFIwa`); Windows: `0x140342220` (`main.sMCA9mvX`), `runtime.concatbyte2` |
| **2. Password Comparison** | `STATIC_AND_DYNAMIC_CONFIRMED` | Strict length equality check followed by `runtime.memequal` on 64 bytes. Case-sensitive lowercase hex. | Linux: `0x73e292`–`0x73e2ad` (`main.ltOjwqsMl5q8`); Windows: `0x140347390` (`main.u4r2NulQUnF`) |
| **3. Token Random Source** | `STATIC_BINARY_EVIDENCE` | Standard library `crypto/rand.Read` reading 32 bytes (`RANDOM_INPUT_BITS = 256`). | Linux: `0x73926b` (`main.d2SHxnu`); Windows: `0x14034242b` (`main.af9fyOpAy`) |
| **4. Token Encoding** | `STATIC_AND_DYNAMIC_CONFIRMED` | Byte-by-byte nibble mapping via lowercase hex lookup table `"0123456789abcdef"`. | Linux: `0x7392ad` (table at `0x827245`); Windows: `0x14034246d` (table at `0x1404327da`) |
| **5. Token Format & Length** | `STATIC_AND_DYNAMIC_CONFIRMED` | Fixed 64-character lowercase ASCII hex string. Zero JWT segments (0 dots), non-UUID, opaque random token. | Linux: `0x739279` (`makeslice(64)`); Windows: `0x140342439` (`makeslice(64)`), Dynamic Oracle |
| **6. Token Creation Behavior** | `STATIC_AND_DYNAMIC_CONFIRMED` | Consecutive logins generate distinct cryptographically random tokens. | Linux: `0x739320` (`main.vT6rYK_v`); Windows: `0x1403424e0` (`main.wdxJrUcsH`) |
| **7. Session Map Type** | `STATIC_BINARY_EVIDENCE` | Thread-safe `map[string]Session` where key is string and value is 40-byte struct stored directly in map. | Linux: `0x7c01c0` (map descriptor), `0x7d6ee0` (elem descriptor); Windows: `0x14041aa20`, `0x140428fa0` |
| **8. Session Struct Layout** | `STATIC_BINARY_EVIDENCE` | 40-byte struct with 2 fields: Field 0 (`string`, offset 0, 16B = Username), Field 1 (`time.Time`, offset 16, 24B = ExpiresAt). | Linux: `0x7d6ee0` (struct descriptor); Windows: `0x140428fa0` |
| **9. Session TTL Expiry** | `STATIC_BINARY_EVIDENCE` | Constant `0x4e94914f0000` nanoseconds = 86,400 seconds = exactly **24 hours**. | Linux: `0x739365` (`movabs rdi, 0x4e94914f0000`); Windows: `0x140342535` (`time.Time.Add`) |
| **10. Lazy Session Expiry** | `STATIC_AND_DYNAMIC_CONFIRMED` | Checked on every token lookup. If `time.Now().After(session.ExpiresAt)`, token is immediately deleted under mutex lock. | Linux: `0x73b2c9`–`0x73b495` (`main.lYKp_Iuf`); Windows: `0x140344480`–`0x1403445e0` (`main.mLWT3o`) |
| **11. Periodic Cleanup Sweeper** | `STATIC_BINARY_EVIDENCE` | Background goroutine spawned on 1-minute ticker (`0xdf8475800` ns). Purges all active tokens of expired user accounts (`User.ExpiresAt`). | Linux: `0x73a500` / `0x73a580` (`main.cFpPBbFet`/`func1`); Windows: `0x1403436e0` / `0x140343760` (`main.wFSLlBV`/`func1`) |
| **12. Logout Revocation** | `STATIC_AND_DYNAMIC_CONFIRMED` | Token explicitly deleted from `sessionMap` under mutex lock. Idempotent; always returns 200 `{{"status":"success"}}`. | Linux: `0x7409a0` (`main.bjWkHiittd`); Windows: `0x140349bc0` (`main.blPINsMc3`) |
| **13. Multiple Sessions** | `STATIC_AND_DYNAMIC_CONFIRMED` | Same account can hold multiple concurrent valid sessions. Revoking session A does NOT invalidate session B. | Linux: `0x7393af` (map key is token); Windows: `0x140342590`, Dynamic Oracle |
| **14. Process Restart Behavior** | `STATIC_AND_DYNAMIC_CONFIRMED` | `SESSION_MEMORY_ONLY`. Sessions reside exclusively in heap memory; zero session files written to disk. Restart invalidates all tokens. | TC-AUTH-11 runtime verification on both original and reconstructed |
| **15. User `ExpiresAt` Semantics**| `STATIC_AND_DYNAMIC_CONFIRMED` | Distinct from Session TTL. Account expiration rejects login with 403, rejects active session lookups with 401, and triggers sweeper eviction. | Linux: `0x73e263` (`main.ltOjwqsMl5q8`); Windows: `0x140347463` (`main.u4r2NulQUnF`) |
| **16. Auth Bypass Mode Source** | `STATIC_BINARY_EVIDENCE` | Dual configuration: CLI flag `-no-auth` registered via `flag.Bool` AND environment variable `NO_AUTH=true`. | Linux: `0x732c28` (`"no-auth"`), `0x73b0b1` (`os.Getenv("NO_AUTH")`); Windows: `0x14036e2f1`, `0x140344280` |

---

## 3. Token Generator Error Path Disassembly Analysis

Static analysis of token generation in both targets:
- **Linux AMD64 `main.d2SHxnu` (`0x73926b`)**:
  ```assembly
  0x73926b: call crypto/rand.Read
  0x739270: nop
  0x739271: nop
  0x739272: lea rax, [rip + 0x650c7]  ; overwrites rax/rbx unconditionally without testing err
  ```
- **Windows AMD64 `main.af9fyOpAy` (`0x14034242b`)**:
  ```assembly
  0x14034242b: call crypto/rand.Read
  0x140342430: nop
  0x140342431: nop
  0x140342432: lea rax, [rip + 0x65b87] ; overwrites rax/rbx unconditionally without testing err
  ```
- **Finding**: Original binary ignores errors returned by `crypto/rand.Read` (`TOKEN_RANDOM_FAILURE_BEHAVIOR: ORIGINAL_DISCARDS_ERROR`).
- **Clean-Room Implementation**: Wraps `rand.Read` error check returning `fmt.Errorf("failed to read random bytes: %w", err)` classified as `GENERATED_ERROR_ADAPTER` for defensive Go best practice while preserving identical behavior on success.

---

## 4. Architectural Scope Enforcement

1. **Absence of Reconstructed HTTP Handlers**:
   Zero `net/http` handlers, no `ServeHTTP`, and no HTTP server routing are introduced in Phase 2C.2.
2. **Behavior-Slice Provenance Mapping**:
   Core methods (`AuthenticateCredentials`, `ValidateToken`, `Logout`, `GetUserProfile`) are cleanly isolated as `BEHAVIOR_SLICE` mappings of their corresponding binary handlers, leaving HTTP layer reconstruction strictly to Phase 2C.3.
3. **Stateful Test Interface**:
   `cmd/auth-tool/main.go` runs as `serve-stdio` to maintain an in-memory `SessionManager` instance across requests without disk persistence shortcuts.
"""
    Path("reports/07_PHASE2C2_AUTH_FORENSICS.md").write_text(content, encoding="utf-8")
    print("Wrote normalized reports/07_PHASE2C2_AUTH_FORENSICS.md")

if __name__ == "__main__":
    generate_report07()
