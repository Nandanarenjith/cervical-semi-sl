# Stage 08 — Fixed Splits & Reproducibility

## Purpose

Freeze the train, validation, and test assignments created in Stage 07 and establish a reproducible configuration for all subsequent experiments.

## Reproducibility Configuration

- Random seed: 42
- CRIC grouping unit: parent image
- RIVA grouping unit: parent slide
- Split policy: 70% train / 15% validation / 15% test
- Binary task:
  - 0 = Normal / non-pathological
  - 1 = Abnormal / pathological

## CRIC

| Split | Learning Units | Images |
|---|---:|---:|
| Train | 8,274 | 280 |
| Validation | 1,539 | 60 |
| Test | 1,721 | 60 |
| Total | 11,534 | 400 |

Image-level leakage check: PASSED.

## RIVA

| Split | Learning Units | Images | Parent Slides |
|---|---:|---:|---:|
| Train | 10,757 | 671 | 77 |
| Validation | 2,640 | 144 | 17 |
| Test | 2,552 | 144 | 17 |
| Total | 15,949 | 959 | 111 |

Slide-level leakage check: PASSED.

Image-level leakage check: PASSED.

## Fixed Outputs

```text
data/splits/cric_splits.csv
data/splits/riva_splits.csv
configs/phase8_reproducibility.json

The split CSV files contain the fixed assignment of each learning unit to train, validation, or test.

The reproducibility configuration records the random seed, grouping strategy, dataset sizes, split policy, and binary label definition.

Integrity
CRIC fixed split integrity: PASSED
CRIC image leakage: PASSED
RIVA fixed split integrity: PASSED
RIVA slide leakage: PASSED
Random seed recorded: PASSED
Outcome

Stage 08 completed successfully.

The dataset partitions are now fixed and will be reused consistently across supervised and semi-supervised experiments.


### `stage_08_fixed_splits_reproducibility_manifest.csv`

```csv
stage,artifact,type,path,description,status
08,fixed_splits,CSV,data/splits/cric_splits.csv,Fixed CRIC image-level train validation test assignments,complete
08,fixed_splits,CSV,data/splits/riva_splits.csv,Fixed RIVA slide-level train validation test assignments,complete
08,reproducibility,JSON,configs/phase8_reproducibility.json,Reproducibility configuration with seed and split policy,complete
08,integrity_check,validation,,CRIC fixed split and image leakage checks passed,complete
08,integrity_check,validation,,RIVA fixed split and slide leakage checks passed,complete