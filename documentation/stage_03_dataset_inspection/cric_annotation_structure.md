# CRIC Cervix Dataset: Annotation Structure

## 1. Annotation Source Files

The CRIC annotation/classification information is stored locally in:

```text
cric_cervix/metadata/
├── classifications.csv
└── classifications.json
```

Both files describe cell classifications associated with the CRIC images.

## 2. CSV Annotation Structure

The CSV contains 11,534 cell-level records.

Columns:

```text
image_id
image_filename
image_doi
cell_id
bethesda_system
nucleus_x
nucleus_y
```

Each row corresponds to one classified cell.

Example:

```text
400,
9ae8a4edde40219bad6303cebc672ee4.png,
10.6084/m9.figshare.12230906,
1,
SCC,
792,
462
```

This means that:

- the cell belongs to image ID `400`
- the associated image is `9ae8a4edde40219bad6303cebc672ee4.png`
- the record has the CRIC/figshare DOI
- the cell identifier is `1`
- its Bethesda-system classification is `SCC`
- its nucleus location is approximately `(792, 462)`

## 3. JSON Annotation Structure

The JSON file is a list containing **400 image-level records**.

General structure:

```text
[
    {
        "image_id": ...,
        "image_doi": ...,
        "image_name": ...,
        "classifications": [
            {
                "cell_id": ...,
                "bethesda_system": ...,
                "nucleus_x": ...,
                "nucleus_y": ...
            },
            ...
        ]
    },
    ...
]
```

Thus, the hierarchy is:

```text
CRIC dataset
    └── image
         └── classifications
              └── cell
                   ├── cell_id
                   ├── bethesda_system
                   ├── nucleus_x
                   └── nucleus_y
```

## 4. Cell-Level Labels

Six distinct Bethesda-system values were observed:

```text
Negative for intraepithelial lesion
HSIL
LSIL
ASC-H
ASC-US
SCC
```

Their observed counts are:

| Bethesda label | Cell count |
|---|---:|
| Negative for intraepithelial lesion | 6,779 |
| HSIL | 1,703 |
| LSIL | 1,360 |
| ASC-H | 925 |
| ASC-US | 606 |
| SCC | 161 |
| **Total** | **11,534** |

The original labels should be retained during archaeology.

## 5. Nucleus Coordinates

Each cell classification includes:

```text
nucleus_x
nucleus_y
```

These represent the location of the cell nucleus within the parent image.

The inspected image size is:

```text
width  = 1376 pixels
height = 1020 pixels
```

Observed coordinates such as:

```text
nucleus_x = 792
nucleus_y = 462
```

are therefore consistent with pixel coordinates in the image.

### Why this matters

The coordinates can potentially be used to create cell-centered crops.

Conceptually:

```text
Full CRIC image
        │
        ├── nucleus coordinate
        │       (x, y)
        │
        ↓
   crop around nucleus
        │
        ↓
   cell image patch
        │
        ↓
   Bethesda label
```

However, the crop size and exact preprocessing strategy must be determined later. They should not be assumed from the archaeology alone.

## 6. One Image Can Contain Multiple Cells

The inspected JSON record for image `400` contains many classifications, with sequential `cell_id` values and different Bethesda labels.

For example, the same image contains cells labeled:

```text
SCC
Negative for intraepithelial lesion
LSIL
HSIL
ASC-H
...
```

Therefore:

```text
1 image ≠ 1 cell
```

and:

```text
1 image → multiple classified cells
```

This is a critical point for experimental design.

## 7. Annotation Granularity

The current metadata supports the following interpretation:

```text
Image-level object:
    image_id / image_name

Cell-level object:
    cell_id
    bethesda_system
    nucleus_x
    nucleus_y
```

Therefore, the CRIC annotations are fundamentally **cell-level classification annotations located inside larger Pap-smear images**.

The metadata does not, from the inspected fields alone, establish that the Bethesda label is an image-level diagnosis.

That distinction must be investigated before building an image-level classifier.

## 8. Relationship Between CSV and JSON

The CSV and JSON appear to encode the same underlying classification information in two representations:

### CSV

Flat table:

```text
image → cell → label + coordinates
```

### JSON

Hierarchical structure:

```text
image
 └── classifications
      ├── cell
      ├── cell
      └── cell
```

The CSV is convenient for:

- pandas analysis
- counting labels
- grouping by image
- checking missing values
- generating experiment tables

The JSON is convenient for:

- reconstructing image → cell relationships
- iterating through classifications belonging to each image
- extracting coordinates for individual images

## 9. Important Data Integrity Checks

Before preprocessing, the following checks should be performed.

### A. Image-count consistency

Verify:

```text
number of local PNG images = 400
number of JSON image records = 400
```

Currently both are confirmed as 400.

### B. Classification-count consistency

Verify:

```text
CSV rows = 11,534
JSON classification objects = 11,534
```

The CSV count is confirmed. The JSON total should be explicitly counted programmatically.

### C. Filename correspondence

Check whether every:

```text
image_filename
```

in the CSV/JSON has a corresponding local file in:

```text
cric_cervix/images/
```

This is especially important because the local filenames observed so far are hash-like.

### D. Cell-ID uniqueness

Check whether `cell_id` is unique:

- globally, or
- only within each image.

Do not assume global uniqueness until verified.

### E. Coordinate validity

Check:

```text
0 <= nucleus_x < 1376
0 <= nucleus_y < 1020
```

for every cell.

Any out-of-range coordinate should be investigated.

### F. Missing values

Check for missing:

- image IDs
- image filenames
- cell IDs
- Bethesda labels
- nucleus coordinates

### G. Cells per image

Calculate:

```text
number of classified cells per image
```

This will show whether annotation density is uniform or highly variable.

## 10. Label Imbalance

The cell labels are substantially imbalanced.

The largest class is:

```text
Negative for intraepithelial lesion = 6,779
```

The smallest is:

```text
SCC = 161
```

This imbalance will matter for:

- train/validation splitting
- supervised baselines
- semi-supervised learning
- class-weighting or sampling decisions
- macro-F1
- sensitivity/specificity
- confusion-matrix interpretation

However, no balancing strategy should be selected during archaeology.

## 11. Critical Experimental Warning

Because multiple cells come from the same image, and potentially multiple images could come from the same patient/slide, **randomly splitting individual cells can cause data leakage** if related cells from the same source appear in both training and test sets.

Therefore, before constructing the SSL split, the project should establish the highest reliable grouping level available, such as:

```text
patient → slide/image → cell
```

The exact grouping hierarchy must be verified from the CRIC metadata/documentation rather than assumed.

## 12. Current Annotation-Archaeology Status

### Confirmed

- [x] 400 image records in JSON
- [x] 11,534 cell classifications in CSV
- [x] Seven CSV fields
- [x] Six Bethesda-system labels
- [x] Cell IDs present
- [x] Nucleus coordinates present
- [x] Multiple cells can belong to one image
- [x] Coordinates are consistent with 1376 × 1020 images

### Still to verify

- [ ] Total JSON cell count
- [ ] CSV ↔ JSON exact record equality
- [ ] Metadata filename ↔ local filename mapping
- [ ] Cell-ID uniqueness scope
- [ ] Coordinate validity for all cells
- [ ] Missing-value checks
- [ ] Cells per image distribution
- [ ] Patient/slide identifiers
- [ ] Image-level diagnosis/ground-truth definition
- [ ] Any official dataset split

## 13. Working Representation for Later Processing

Until the remaining archaeology is complete, the safest conceptual representation is:

```text
CRIC Image
│
├── image_id
├── image_filename
├── image metadata
│
└── Cells
    ├── cell_id
    ├── Bethesda label
    ├── nucleus_x
    └── nucleus_y
```

Later, after the data integrity and grouping checks are complete, this can be transformed into the representation required by the SSL experiment.

## 14. Preliminary Conclusion

CRIC should currently be treated as a **cell-annotated image dataset**, not automatically as a simple image-classification dataset.

The annotation metadata provides the information needed to locate classified nuclei and associate them with Bethesda-system cell labels. This makes cell-centered patch extraction a possible downstream approach, but the final experimental unit and label strategy must be decided only after the remaining dataset archaeology is completed.
