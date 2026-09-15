# Forensic Session Type Evidence (`SESSION_TYPE_EVIDENCE.md`)

**Binary Descriptor**: `0x7d6ee0` (`.rodata`)  
**Map Descriptor**: `0x7c01c0` (`.rodata`)  
**Classification**: `DIRECT_TYPE_RECOVERY`  
**Status**: CONFIRMED VIA RO-DATA RUNTIME STRUCT DESCRIPTORS

---

## 1. Type Structure Overview

The in-memory session record in `webrtc-signaling` is stored in a map:

```go
map[string]struct {
    HDz5Nf     string    // semantic: Username
    GkWDh_Jc_q time.Time // semantic: ExpiresAt
}
```

- **Map Descriptor VA**: `0x7c01c0` (kind `53` = `reflect.Map`)
- **Key Type VA**: `0x79e2c0` (`string`, size 16 bytes)
- **Value Struct Descriptor VA**: `0x7d6ee0` (`struct`, size 40 bytes)
- **Bucket Type VA**: `0x7cb920`
- **Value Semantics**: The 40-byte struct is stored **directly as a value** in the map buckets (`runtime.mapassign_faststr`), not as a heap pointer.

---

## 2. Struct Field Layout Table

| Field Index | Forensic Symbol | Semantic Role | Byte Offset | Size | Go Type | Instruction Accesses |
|---|---|---|---|---|---|---|
| **0** | `HDz5Nf` | `Username` | `0` (`0x00`) | 16 B | `string` | Written at `0x739379`, read at `0x73b235`, compared at `0x73ab58` |
| **1** | `GkWDh_Jc_q` | `ExpiresAt` | `16` (`0x10`) | 24 B | `time.Time` | Written at `0x739388` (`+24h`), read at `0x73b2ba` (`time.Time.After`) |

**Total Struct Size**: Exactly **40 bytes** (`0x28` bytes).  
**Total Field Count**: Exactly **2 fields**.

> [!IMPORTANT]
> **Negative Field Invariants**:
> The `Session` struct does **NOT** contain:
> - `Role` (retrieved dynamically from `UsersStore` via `session.Username` on each request)
> - `CreatedAt` (not stored in struct; only `ExpiresAt` is calculated and retained)
> - `RemoteAddr` / `IP` (not stored in session struct)
> - `User` pointer (stores raw `string` username, looking up `UsersStore` under RLock on lookup)
