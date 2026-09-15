# KMAX CLEAN ROOM RULES

## 1. Source isolation & Absolute Prohibitions

This project is a strict clean-room reverse-engineering and source recovery project.

Forbidden sources and actions:

- `D:\KMAX\`
- `D:\ScrcpyOverWebRTC\ScrcpyOverWebRTC-FullSource\`
- Any `recovered_source` directory outside this workspace
- Previous reconstructed Git repositories or backups containing previously recovered code
- **NO git clone of upstream source** (e.g. `https://github.com/hqw700/ScrcpyOverWebRTC`)
- **NO git submodule containing source code**
- **NO GitHub source code browsing**
- **NO comparison against upstream source code** until `CLEANROOM_RECOVERY_COMPLETE` is formally declared
- **NO reading any previous recovered source**

Never read, copy, compare against, or infer from them.

## 2. Allowed evidence

Only original distributed release artifacts located under:

- `D:\KMAX-CLEANROOM\cloudphone-agent-magisk-v0.3.6 (1)\`
- `D:\KMAX-CLEANROOM\cloudphone-v0.3.6 (1)\`

For frontend reconstruction, the ONLY accepted evidence is:

- `D:\KMAX-CLEANROOM\cloudphone-v0.3.6 (1)\assets\`

Any previous reference to upstream GitHub repository source during initial Phase 0 is formally classified:

`CONTAMINATED_REFERENCE_EXPOSURE`

and its findings are quarantined. Reconstructed frontend code must be synthesized solely from compiled distribution bundles in `cloudphone-v0.3.6 (1)\assets\`.

## 3. Original artifacts are immutable

Never modify input artifacts.
Treat original release directories as strictly READ-ONLY.

All working output goes to:

- `evidence/`
- `raw_extraction/`
- `reconstructed_source/`
- `tests/`
- `reports/`
- `build/`
- `logs/`

## 4. Raw extraction is immutable

Never manually edit raw JADX, Smali, apktool, disassembly, strings, or tool exports under `raw_extraction/`.

## 5. Preserve original language

Do not translate Chinese strings during forensic recovery.
Do not rewrite original runtime strings for readability.

Original: `"设备连接失败"`  
Preserve: `"设备连接失败"` (Do NOT replace with `"Device connection failed"`).

## 6. No invented provenance

Every reconstructed class, method, function, and structure must link to verifiable binary evidence.

Classification must be strictly one of:

- `DIRECT_DECOMPILE`
- `DIRECT_SYMBOL_RECOVERY`
- `RECONSTRUCTED_FROM_BINARY`
- `RECONSTRUCTED_FROM_PROTOCOL`
- `GENERATED_BUILD_FILE`
- `THIRD_PARTY`
- `UNKNOWN`
- `CONTAMINATED_REFERENCE_EXPOSURE` (Quarantine tag)

## 7. Go code rule

Go native binaries cannot be "directly decompiled to original Go source".
Recovered Go code must be classified:

`RECONSTRUCTED_FROM_BINARY`

unless direct source-level evidence exists.

## 8. No source-first reconstruction

Do not begin by designing clean architecture.
First recover:

binary structure  
→ symbols  
→ strings  
→ call graph  
→ protocols  
→ behavior  

Then reconstruct code.

## 9. No copying

Do not copy code from old KMAX projects, old FullSource, previous Git commits, or external repositories.

## 10. Evidence before implementation

Every reconstructed subsystem requires an evidence report before implementation begins.

## 11. Build independence

The recovered source must build without requiring project binaries from the original release, except clearly identified third-party binary dependencies.

## 12. No false 100% claims

Never claim 100% original source recovery unless directly provable.

Target:
- 100% provenance traceability
- $\ge$ 99% behavioral parity
- $\ge$ 99% protocol parity

## 13. Audit log

All important actions, milestone completions, and any accidental exposure to forbidden source must be logged in:

`CLEANROOM_AUDIT_LOG.md`
