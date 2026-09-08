# Stage 06 — Preprocessing

## Purpose

Prepare CRIC Cervix and RIVA 1.0 cell-level samples in a common image representation for later experiments.

## Preprocessing

For both datasets:

- Cell/nucleus coordinates are represented in image-pixel coordinates.
- A **128 × 128 RGB crop** is generated around each cell/nucleus.
- Crops near image boundaries are padded to maintain the fixed size.
- Parent image information is retained for each sample.
- Binary labels from Stage 04 are preserved.

### Coordinate handling

CRIC coordinates are already provided as pixel coordinates.

RIVA raw annotations use normalized coordinates, but the official RIVA processed/clustered dataset used in Stage 05 already contains pixel coordinates. Therefore, the official `nucleus_x` and `nucleus_y` values are used directly.

## Results

| Dataset | Learning Units | Parent Images | Valid Crops | Invalid Crops |
|---|---:|---:|---:|---:|
| CRIC | 11,534 | 400 | 11,534 | 0 |
| RIVA | 15,949 | 959 | 15,949 | 0 |

### CRIC

- Binary label 0: 6,779
- Binary label 1: 4,755
- Boundary-padded crops: 885

### RIVA

- Binary label 0: 10,517
- Binary label 1: 5,432
- Boundary-padded crops: 2,650

## Output

Processed manifests:

- `data/processed/cric_learning_units.csv`
- `data/processed/riva_learning_units.csv`

Processed crops:

- `data/processed/cric_crops/`
- `data/processed/riva_crops/`

## Key Outcome

Both datasets have been converted into valid 128 × 128 RGB cell-centered samples with corresponding binary labels.

**Stage 06 — COMPLETE**

## Next Stage

Stage 07 — Data Splits.