# Stage 07 — Data Splits

## Purpose

Create leakage-safe train, validation, and test partitions for CRIC and RIVA while preserving the appropriate parent-level grouping structure.

## Split Strategy

- Random seed: 42
- Target proportion: 70% train / 15% validation / 15% test
- CRIC grouping unit: parent image
- RIVA grouping unit: parent slide
- Binary labels were retained at the learning-unit level.
- Split assignments were saved as fixed CSV files.

## CRIC

| Split | Parent Images | Normal (0) | Abnormal (1) | Learning Units |
|---|---:|---:|---:|---:|
| Train | 280 | 4,736 | 3,538 | 8,274 |
| Validation | 60 | 935 | 604 | 1,539 |
| Test | 60 | 1,108 | 613 | 1,721 |
| Total | 400 | 6,779 | 4,755 | 11,534 |

CRIC uses parent-image grouping because no reliable patient-level identifier is available in the provided metadata.

## RIVA

The published RIVA dataset contains 959 mini-patches sourced from 115 anonymized Pap smear slides. The local 959-image collection used in this project contains 111 distinct slide identifiers based on the dataset filename convention.

Therefore, the split operation uses the 111 represented parent slides rather than the 115 source slides reported for the complete collection.

| Split | Parent Slides | Normal (0) | Abnormal (1) | Learning Units |
|---|---:|---:|---:|---:|
| Train | 77 | 7,279 | 3,478 | 10,757 |
| Validation | 17 | 1,604 | 1,036 | 2,640 |
| Test | 17 | 1,634 | 918 | 2,552 |
| Total | 111 | 10,517 | 5,432 | 15,949 |

## Leakage Checks

### CRIC

- Parent-image overlap between train, validation, and test: none.
- Image leakage check: PASSED.

### RIVA

- Parent-slide overlap between train, validation, and test: none.
- Image leakage check: PASSED.
- Slide leakage check: PASSED.

All mini-patches belonging to the same represented RIVA slide remain within a single split.

## Saved Outputs

```text
data/splits/cric_splits.csv
data/splits/riva_splits.csv
These files contain the fixed split assignment for each learning unit.

Reproducibility

The split generation used a fixed random seed of 42 and parent-level grouping.

The resulting assignments were explicitly saved to CSV files rather than regenerated dynamically during later experiments.

Outcome

Stage 07 completed successfully.

Leakage-safe train, validation, and test partitions are now available for the subsequent fixed-split and reproducibility stage.


### `stage_07_data_splits_manifest.csv`

```csv
stage,artifact,type,path,description,status
07,data_splits,CSV,data/splits/cric_splits.csv,Fixed CRIC image-level train validation test assignments,complete
07,data_splits,CSV,data/splits/riva_splits.csv,Fixed RIVA slide-level train validation test assignments,complete
07,reproducibility,parameter,,Random seed 42 used for split generation,complete
07,leakage_check,validation,,CRIC image-level leakage check passed,complete
07,leakage_check,validation,,RIVA slide-level and image-level leakage checks passed,complete