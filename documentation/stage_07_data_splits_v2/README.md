# Phase 07 V2 — Final Dataset Splits

## 1. Purpose

Phase 07 V2 creates the final train, validation, and test partitions
used for the cervical cytology Semi-Supervised Learning experiments.

The V2 protocol replaces the historical 70/15/15 split with the final:

- 70% training
- 10% validation
- 20% test

The existing Phase 06 preprocessing and 128x128 image crops are reused.
No image crops are regenerated in Phase 07 V2.

---

## 2. Input Data

Phase 07 V2 uses the existing Phase 06 learning-unit manifests:

```text
data/processed/cric_learning_units.csv
data/processed/riva_learning_units.csv
````

The corresponding preprocessed crops are already available under:

```text
data/processed/cric_crops/
data/processed/riva_crops/
```

### CRIC

* Learning units: 11,534
* Parent images: 400
* Normal: 6,779
* Abnormal: 4,755

### RIVA

* Learning units: 15,949
* Parent images: 959
* Parent slides: 111
* Normal: 10,517
* Abnormal: 5,432

---

## 3. Grouping Strategy

Splitting is performed at the parent-group level to prevent
information leakage between training, validation, and test sets.

### CRIC

The grouping unit is the parent image:

```text
image_filename
```

All annotated cells belonging to the same CRIC image are assigned
to the same split.

### RIVA

The grouping unit is the parent slide.

The slide identifier is derived from the RIVA filename:

```text
category_sample_patch.png
```

For example:

```text
LSIL_45_3.png
```

maps to:

```text
LSIL_45
```

All learning units belonging to the same slide are assigned to the
same split.

---

## 4. Final V2 Protocol

| Dataset | Grouping unit |      Train | Validation |       Test |
| ------- | ------------- | ---------: | ---------: | ---------: |
| CRIC    | Image         | 70% target | 10% target | 20% target |
| RIVA    | Slide         | 70% target | 10% target | 20% target |

Random seed:

```text
42
```

Because complete images/slides must remain intact, the final
learning-unit counts may differ slightly from the exact percentage
targets.

---

## 5. Final Split Results

### CRIC

Learning-unit counts:

| Split      | Learning units |
| ---------- | -------------: |
| Train      |          8,074 |
| Validation |          1,153 |
| Test       |          2,307 |
| Total      |         11,534 |

Group counts:

| Split      | Images |
| ---------- | -----: |
| Train      |    209 |
| Validation |     78 |
| Test       |    113 |
| Total      |    400 |

Class counts:

| Split      | Normal | Abnormal |
| ---------- | -----: | -------: |
| Train      |  4,482 |    3,592 |
| Validation |    694 |      459 |
| Test       |  1,603 |      704 |

Abnormal proportions:

| Split      | Abnormal proportion |
| ---------- | ------------------: |
| Train      |              0.4449 |
| Validation |              0.3981 |
| Test       |              0.3052 |

---

### RIVA

Learning-unit counts:

| Split      | Learning units |
| ---------- | -------------: |
| Train      |         11,171 |
| Validation |          1,582 |
| Test       |          3,196 |
| Total      |         15,949 |

Group counts:

| Split      | Slides |
| ---------- | -----: |
| Train      |     53 |
| Validation |     24 |
| Test       |     34 |
| Total      |    111 |

Class counts:

| Split      | Normal | Abnormal |
| ---------- | -----: | -------: |
| Train      |  7,332 |    3,839 |
| Validation |  1,115 |      467 |
| Test       |  2,070 |    1,126 |

Abnormal proportions:

| Split      | Abnormal proportion |
| ---------- | ------------------: |
| Train      |              0.3437 |
| Validation |              0.2952 |
| Test       |              0.3523 |

---

## 6. Leakage Validation

Group leakage checks were performed after creating the splits.

For CRIC:

```text
Grouping: image_filename
Result: NO GROUP LEAKAGE
```

For RIVA:

```text
Grouping: slide_id
Result: NO GROUP LEAKAGE
```

Every parent image in CRIC occurs in exactly one split.

Every parent slide in RIVA occurs in exactly one split.

---

## 7. Output Files

The final V2 split manifests are:

```text
data/splits_v2/cric_splits_v2.csv
data/splits_v2/riva_splits_v2.csv
```

These files are the authoritative split definitions for all
subsequent V2 experiments.

The historical split files under:

```text
data/splits/
```

are not used for the final V2 experiments.

---

## 8. Relationship to Semi-Supervised Learning

The 70/10/20 split is performed before applying the labeled-data
fractions used in the Semi-SL experiments.

The protocol is:

```text
ALL DATA
    |
    +---- 70% TRAIN
    |       |
    |       +---- 5% labeled
    |       +---- 95% unlabeled
    |
    +---- 10% VALIDATION
    |
    +---- 20% TEST
```

For the 10% labeled condition:

```text
ALL DATA
    |
    +---- 70% TRAIN
    |       |
    |       +---- 10% labeled
    |       +---- 90% unlabeled
    |
    +---- 10% VALIDATION
    |
    +---- 20% TEST
```

The validation and test sets remain fully labeled.

The target dataset in cross-dataset experiments is not used for
training, validation, model selection, normalization, or tuning.

---

## 9. Reproducibility

Phase 07 V2 uses:

```text
Seed: 42
Train: 70%
Validation: 10%
Test: 20%
CRIC grouping: image
RIVA grouping: slide
```

The split manifests are saved explicitly so that all subsequent
experiments use the same fixed partitions.

---

## 10. Status

Phase 07 V2 is complete.

Validation status:

```text
PASSED
```

Final protocol:

```text
FINAL_V2
```

````

