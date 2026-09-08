# CRIC Cervix Dataset: Initial Findings

## 1. Dataset Location

Local dataset directory:

```text
cervical-semi-sl/
└── cric_cervix/
    ├── images/
    └── metadata/
        ├── README.md
        ├── classifications.csv
        └── classifications.json
```

## 2. Local Dataset Size

The local `cric_cervix` directory contains:

- **400 PNG images**
- **3 metadata files**
- **403 total files**
- Approximate local size observed: **811 MB**

The image count of 400 is consistent with the CRIC Cervix dataset collection described in the project documentation.

## 3. Image Properties

The local image inspection confirmed:

- Number of images: **400**
- File format: **PNG**
- Image dimensions: **1376 × 1020 pixels**
- Image mode: **RGB**
- Image filenames in the local `images/` directory are hash-like identifiers, for example:

```text
008df697b9283d9ad4774096584d2efb.png
00b1e59ebc3e7be500ef7548207d44e2.png
011fda505d7e4af4b8cc57545343624d.png
```

## 4. Classification CSV

File:

```text
cric_cervix/metadata/classifications.csv
```

The CSV contains **11,534 classification records** plus one header row, as confirmed by:

```text
wc -l classifications.csv
11535
```

Therefore:

- Data rows: **11,534**
- Header row: **1**
- Total CSV lines: **11,535**

The CSV has **7 columns**:

| Column | Meaning observed |
|---|---|
| `image_id` | CRIC image identifier |
| `image_filename` | Image filename associated with the classification |
| `image_doi` | DOI associated with the image record |
| `cell_id` | Identifier of the classified cell |
| `bethesda_system` | Bethesda-system cell classification |
| `nucleus_x` | X-coordinate of the annotated nucleus |
| `nucleus_y` | Y-coordinate of the annotated nucleus |

## 5. Bethesda-System Labels

The observed `bethesda_system` values are:

| Label | Number of cells |
|---|---:|
| Negative for intraepithelial lesion | 6,779 |
| HSIL | 1,703 |
| LSIL | 1,360 |
| ASC-H | 925 |
| ASC-US | 606 |
| SCC | 161 |
| **Total** | **11,534** |

Thus, the local CRIC classification metadata contains **six distinct cell-level labels**.

### Important

Do not collapse or remap these labels during dataset archaeology. The original Bethesda-system terminology should be preserved until the final experimental label scheme is explicitly defined.

## 6. JSON Structure

File:

```text
cric_cervix/metadata/classifications.json
```

The JSON is a **list**, not a dictionary.

It contains:

```text
400 top-level entries
```

Each top-level entry represents an image record and has the following general structure:

```text
{
    image_id,
    image_doi,
    image_name,
    classifications: [
        {
            cell_id,
            bethesda_system,
            nucleus_x,
            nucleus_y
        },
        ...
    ]
}
```

For example, the first inspected image record has:

```text
image_id: 400
image_name: 9ae8a4edde40219bad6303cebc672ee4.png
```

and contains multiple cell classifications.

## 7. Image-Level vs Cell-Level Information

The classification metadata is clearly organized around **cells associated with images**.

A single image can contain multiple cells, and each cell has:

- a `cell_id`
- a Bethesda-system label
- a nucleus X coordinate
- a nucleus Y coordinate

Therefore, the CRIC metadata should not automatically be interpreted as one classification label per whole image.

This distinction is important for the planned SSL experiments because the project must decide whether the learning unit is:

1. the annotated cell,
2. a cropped cell patch, or
3. the complete Pap-smear image.

The current archaeology establishes that the source metadata provides **cell-level labels and nucleus coordinates within images**.

## 8. Current Filename Situation

The local image directory uses hash-like PNG filenames, while the classification metadata contains filenames such as:

```text
9ae8a4edde40219bad6303cebc672ee4.png
```

The first inspected CSV record and JSON record agree on the same image filename:

```text
9ae8a4edde40219bad6303cebc672ee4.png
```

However, the local `images/` directory also contains hash-like filenames. Therefore, a complete filename correspondence check is still required before preprocessing.

We should explicitly verify:

```text
metadata image_filename
        ↓
local image filename
```

for all 400 image records.

## 9. Coordinate Information

Each classified cell contains:

```text
nucleus_x
nucleus_y
```

The observed values are pixel-like coordinates. For example:

```text
nucleus_x = 792
nucleus_y = 462
```

Given the confirmed image size of 1376 × 1020 pixels, these coordinates are consistent with positions inside the image.

The coordinates should be preserved because they may be required later for extracting cell-centered image patches.

## 10. Data-Archaeology Status

### Confirmed

- [x] Local CRIC directory exists
- [x] 400 PNG images present
- [x] Image dimensions are 1376 × 1020
- [x] Images are RGB
- [x] Classification CSV exists
- [x] 11,534 cell classification rows
- [x] CSV has 7 columns
- [x] Six Bethesda-system labels observed
- [x] Classification JSON exists
- [x] JSON has 400 image records
- [x] Cell IDs and nucleus coordinates are available

### Still to investigate

- [ ] Exact mapping between metadata filenames and local hash-like filenames
- [ ] Number of cells per image
- [ ] Whether every image has classifications
- [ ] Image-level diagnosis/ground truth interpretation
- [ ] Patient IDs
- [ ] Slide/specimen IDs
- [ ] Potential patient-level or slide-level grouping
- [ ] Duplicate/related images
- [ ] Official train/test split, if any
- [ ] Exact relationship between CRIC image IDs and local filenames
- [ ] Whether all cell labels should be used directly for the proposed SSL task

## 11. Preliminary Conclusion

The local CRIC dataset appears to contain the **complete 400-image collection** together with its classification metadata.

The most important structural finding is that CRIC provides **cell-level Bethesda classifications and nucleus coordinates associated with 400 RGB Pap-smear images**. The classification table contains **11,534 annotated/classified cells across six labels**.

No preprocessing, cropping, label merging, or train/test splitting should be performed yet. The remaining archaeology should first establish the exact mapping between the local image files and metadata, as well as the patient/slide structure and the correct experimental unit.
