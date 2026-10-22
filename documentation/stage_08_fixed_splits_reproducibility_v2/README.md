# Phase 08 V2 — Final Reproducibility

## Purpose

Locks the final experimental protocol for the cervical Semi-SL study.

## Final Protocol

- Protocol: FINAL_V2
- Seed: 42
- Train / Validation / Test: 70% / 10% / 20%
- CRIC grouping: image
- RIVA grouping: slide
- Image size: 128×128 RGB
- Labels:
  - 0 = Normal / Non-pathological
  - 1 = Abnormal / Pathological
- Semi-SL labeled fractions: 5% and 10%

## Split Files

- `data/splits_v2/cric_splits_v2.csv`
- `data/splits_v2/riva_splits_v2.csv`

## Reproducibility

The protocol and settings are stored in:

`configs/phase8_v2_reproducibility.json`

All final V2 experiments must use these settings and the V2 split files.

## Status

**COMPLETE — FINAL V2 PROTOCOL LOCKED**