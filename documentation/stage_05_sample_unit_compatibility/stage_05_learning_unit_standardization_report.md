# Stage 05 — Learning Unit Standardization

## Purpose

The purpose of Stage 05 was to establish a standardized learning-unit representation for the RIVA dataset that can be used consistently in subsequent preprocessing and Semi-Supervised Learning experiments.

The official RIVA processed/clustered annotations were used rather than reconstructing the clustering process from the raw annotations.

---

## Input

Dataset:

- RIVA 1.0
- 959 images
- Official clustered/processed annotation file

Official processed annotation file:

`riva_official/Raw annotations and clustering/processed_annotations/processed.csv`

The official processed file contains one row per clustered cell, resulting in:

- **15,949 unique cell-level learning units**

---

## Standardized Learning Unit

Each RIVA learning unit contains:

| Field | Description |
|---|---|
| `dataset` | Dataset identifier (`RIVA`) |
| `image_filename` | Parent RIVA image |
| `x_norm` | Normalized x-coordinate |
| `y_norm` | Normalized y-coordinate |
| `class_bethesda` | Official Bethesda-level cell label |
| `class_annotated` | Cell annotation label |
| `cluster_idx` | Official RIVA cluster identifier |
| `binary_label` | Project binary target |

The parent image is retained for every cell so that cell-level samples remain traceable to their source image.

---

## Binary Label Mapping

For the project, cervical cytology categories are mapped to two classes:

### Class 0 — Normal / Non-pathological

- NILM
- ENDO
- INFL

### Class 1 — Abnormal / Pathological

- ASCUS
- ASCH
- LSIL
- HSIL
- CA

The original RIVA labels are preserved in the standardized table. Only the additional `binary_label` field represents the project-level binary task.

---

## Result

The standardized RIVA table contains:

**15,949 learning units**

Binary distribution:

| Binary Label | Meaning | Count |
|---:|---|---:|
| 0 | Normal / Non-pathological | 10,517 |
| 1 | Abnormal / Pathological | 5,432 |
| **Total** | | **15,949** |

No labels were left unmapped.

---

## Important Dataset Structure

The learning unit is a **cell**, but cells belong to parent RIVA images.

Therefore, the parent image remains an important grouping variable for subsequent dataset partitioning. Cells from the same parent image should not be independently distributed across training and validation/test partitions.

This prevents information leakage caused by visually related cells originating from the same image.

---

## Key Outcome

Stage 05 establishes the RIVA dataset in a form suitable for the next preprocessing stage.

At the end of this stage:

- RIVA cell-level learning units are standardized.
- Official RIVA clustering is retained.
- Original labels are preserved.
- Binary project labels are available.
- Every learning unit has a valid binary label.
- The dataset is ready for coordinate conversion and cell-centered image preparation.

---

## Next Stage

The next stage is **image/sample preparation**.

The main tasks are:

1. Convert RIVA normalized coordinates to image-pixel coordinates.
2. Generate consistent cell-centered crops/samples.
3. Establish the common sample representation needed for CRIC and RIVA.
4. Perform final preprocessing and integrity checks.
5. Prepare the datasets for leakage-safe train/validation/test partitioning.

This stage should preserve the parent-image relationship required for later cross-dataset evaluation.