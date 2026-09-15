# Forensic Report 02C: Phase 2 Reproducibility & Tooling Pipeline

**Status**: 100% REPRODUCIBLE IN-REPO TOOLING

## 1. Committed Reproducibility Tooling Suite

All forensic tools have been committed into the repository under `tools/`:
- `tools/forensics/pclntab_parser.py`: Portable, version-aware Go pclntab parser with invariant checking.
- `tools/forensics/regenerate_function_maps.py`: Extracts exact function boundaries and direct callgraphs.
- `tools/forensics/regenerate_role_mappings.py`: Re-derives role mappings with strict provenance separation.
- `tools/oracle/clean_oracle_prober.py`: Portable clean dynamic oracle prober.
- `tools/oracle/fixtures/`: Baseline deterministic data fixtures (`users.json`, `shares.json`, `device_tags.json`).
- `tools/verify_phase2.py`: Unified verification entry point enforcing all Phase 2 invariants.

## 2. Clean Clone Reproduction Instructions

```bash
git clone https://github.com/tcandt/kmax-cleanroom.git
cd kmax-cleanroom
python tests/test_pclntab_parser.py
python tools/verify_phase2.py
```
