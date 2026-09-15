# KMAX CLEAN ROOM RULES

## 1. Source isolation

This project is a clean-room recovery.

Forbidden sources:

- D:\KMAX\
- D:\ScrcpyOverWebRTC\ScrcpyOverWebRTC-FullSource\
- any recovered_source directory outside this workspace
- previous reconstructed Git repositories
- backups containing previously recovered code

Never read them.

## 2. Allowed evidence

Only original distributed artifacts already present under D:\KMAX-CLEANROOM may be used.

## 3. Original artifacts are immutable

Never modify input artifacts.

All output goes to:

- evidence/
- raw_extraction/
- reconstructed_source/
- tests/
- reports/
- build/
- logs/

## 4. Raw extraction is immutable

Never manually edit raw JADX, Smali, disassembly, strings or Ghidra exports.

## 5. Preserve original language

Do not translate Chinese strings during forensic recovery.

Do not rewrite original runtime strings for readability.

## 6. No invented provenance

Every reconstructed function must have evidence.

Classification must be one of:

- DIRECT_DECOMPILE
- DIRECT_SYMBOL_RECOVERY
- RECONSTRUCTED_FROM_BINARY
- RECONSTRUCTED_FROM_PROTOCOL
- GENERATED_BUILD_FILE
- THIRD_PARTY
- UNKNOWN

## 7. Go code rule

Go native binaries are not "directly decompiled to original Go source".

Recovered Go code must normally be classified:

RECONSTRUCTED_FROM_BINARY

unless direct source-level evidence exists.

## 8. No source-first reconstruction

Do not begin by designing a clean architecture.

First recover:

binary structure
→ symbols
→ strings
→ call graph
→ protocols
→ behavior

Then reconstruct code.

## 9. No copying

Do not copy code from:

- old KMAX project
- old FullSource
- old recovered source
- previous Git commit
- previous generated implementation

## 10. Evidence before implementation

Every reconstructed subsystem requires an evidence report before implementation begins.

## 11. Build independence

The recovered source must build without requiring project binaries from the original release, except clearly identified third-party binary dependencies.

## 12. No false 100% claims

Never claim 100% original source recovery unless directly provable.

Target:

100% provenance
>=99% behavioral parity
>=99% protocol parity

## 13. Audit log

All important actions and any accidental exposure to forbidden source must be logged in:

CLEANROOM_AUDIT_LOG.md
