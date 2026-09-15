# Forensic Report 02B: Semantic Role Mapping Validation (Phase 2B.6)

**Status**: VERIFIED & AUDITED (Automated Invariant Check: PASS)

## 1. Mathematical Count Invariants

| Binary Target | Total Functions | CONFIRMED_ROLE | INFERRED_ROLE | UNKNOWN | Sum Formula | Result |
|---|---|---|---|---|---|---|
| `webrtc-signaling` (Linux AMD64) | 7571 | 1968 | 37 | 5566 | `1968 + 37 + 5566 == 7571` | **PASS** |
| `cloudphone-agent` (Android ARM64) | 15398 | 2582 | 135 | 12681 | `2582 + 135 + 12681 == 15398` | **PASS** |

## 2. Elimination of Semantic Over-Classification

- **Strict Package Provenance**: Provenance (`GO_RUNTIME`, `STDLIB`, `THIRD_PARTY`, `PROJECT`, `UNKNOWN_PACKAGE`) is separated from `semantic_role`.
- **Zero Leaked Generic Methods**: 0 generic methods (`String`, `MarshalText`, `ReadFrom`, `AcceptTCPWithConn`, etc.) receive project application roles.
- **Two-Class Evidence Rule**: Every confirmed project role is backed by at least 2 independent evidence classes (e.g. route registration closure + instruction xref + dynamic oracle confirmation).
