# Stage 04: Binary Label Mapping / Label Harmonization

## 1. Purpose

This stage establishes and validates the reproducible binary label specification for the core CRIC--RIVA study:

| Binary label | Primary scientific name |
|---:|---|
| 0 | Normal / non-pathological |
| 1 | Abnormal / pathological |

The wording **Normal / non-pathological** is intentional. For RIVA, `ENDO` and `INFL` are officially grouped as non-pathological/non-lesion; this does not claim that either is clinically identical to `NILM`.

This stage defines a mapping only. It does not alter raw labels, generate samples, crop images, convert coordinates, cluster annotations, select annotator consensus, split data, or train models.

## 2. Inputs

| Dataset | Raw input inspected | Label field used in this stage |
|---|---|---|
| CRIC | `cric_cervix/metadata/classifications.csv` | `bethesda_system` |
| RIVA | `riva_1.0/annotations/annotations.json` | point-level `keypointlabels` |

Supporting sources inspected during the preceding RIVA ground-truth review were the local RIVA license/citation, the official RIVA Zenodo record, its Scientific Data descriptor, official RIVA website, and official source repository.

## 3. Mapping manifest

The complete source-to-target mapping is preserved separately in:

`documentation/stage_04_label_mapping/binary_label_mapping_manifest.csv`

The manifest schema is:

```text
source_dataset,original_label,binary_label,binary_name,rationale
```

It is a specification only. It does not replace, overwrite, or modify any source metadata.

## 4. CRIC mapping and inventory

CRIC mapping is based on its observed `bethesda_system` values.

| Original label | Count | Binary label | Binary name |
|---|---:|---:|---|
| Negative for intraepithelial lesion | 6,779 | 0 | Normal / non-pathological |
| ASC-US | 606 | 1 | Abnormal / pathological |
| ASC-H | 925 | 1 | Abnormal / pathological |
| LSIL | 1,360 | 1 | Abnormal / pathological |
| HSIL | 1,703 | 1 | Abnormal / pathological |
| SCC | 161 | 1 | Abnormal / pathological |
| **Total** | **11,534** |  |  |

### CRIC binary counts

| Binary class | Count | Percentage |
|---|---:|---:|
| 0 -- Normal / non-pathological | 6,779 | 58.77% |
| 1 -- Abnormal / pathological | 4,755 | 41.23% |
| **Total** | **11,534** | **100.00%** |

## 5. RIVA mapping and inventory

RIVA mapping is based only on observed point-level `keypointlabels`.

**RIVA filename prefixes are retained as parent-slide diagnostic metadata and are NOT used as the cell-level classification target.**

| Original point label | Annotation-instance count | Binary label | Binary name |
|---|---:|---:|---|
| NILM | 9,457 | 0 | Normal / non-pathological |
| ENDO | 1,270 | 0 | Normal / non-pathological |
| INFL | 8,190 | 0 | Normal / non-pathological |
| ASCUS | 356 | 1 | Abnormal / pathological |
| ASCH | 416 | 1 | Abnormal / pathological |
| LSIL | 3,048 | 1 | Abnormal / pathological |
| HSIL | 1,835 | 1 | Abnormal / pathological |
| SCC | 1,586 | 1 | Abnormal / pathological |
| **Total** | **26,158** |  |  |

### RIVA binary counts

| Binary class | Annotation-instance count | Percentage |
|---|---:|---:|
| 0 -- Normal / non-pathological | 18,917 | 72.32% |
| 1 -- Abnormal / pathological | 7,241 | 27.68% |
| **Total** | **26,158** | **100.00%** |

**Important limitation:** RIVA annotation-instance counts at Stage 04 must not be interpreted as unique cell counts because multiple annotators may refer to the same underlying cell. They are not independent training samples.

## 6. Scientific rationale

CRIC uses six Bethesda-system cell labels. `Negative for intraepithelial lesion` is mapped to class 0; all observed atypical, intraepithelial-lesion, and carcinoma labels are mapped to class 1.

RIVA officially defines a broader pathological versus non-pathological grouping: pathological `{SCC, HSIL, ASCH, LSIL, ASCUS}` and non-pathological `{INFL, ENDO, NILM}`. Stage 04 adopts that published grouping exactly. In the local RIVA JSON, the raw spelling is `INFL`; that spelling is retained in the manifest.

Official RIVA sources used for this decision:

- Zenodo dataset record: <https://zenodo.org/records/17288879>
- Scientific Data descriptor: <https://doi.org/10.1038/s41597-025-06280-2>
- RIVA project website: <https://beta-digitalpapsdb.exactas.uba.ar/about>

## 7. Validation checks

| Check | Result | Evidence |
|---|---|---|
| Every observed CRIC label maps exactly once | PASS | 6 observed labels; 6 CRIC manifest rows; no duplicate original labels |
| Every observed RIVA point label maps exactly once | PASS | 8 observed labels; 8 RIVA manifest rows; no duplicate original labels |
| No raw labels are silently dropped | PASS | Observed-label inventories exactly equal manifest-label inventories for each dataset |
| No raw labels are overwritten | PASS | Mapping is stored only in a new separate CSV manifest; raw source files were not edited |
| CRIC binary counts equal mapped-source sums | PASS | 6,779 + 4,755 = 11,534 |
| RIVA binary counts equal mapped-source sums | PASS | 18,917 + 7,241 = 26,158 |
| Unexpected CRIC labels | PASS -- none | All observed values are in the manifest |
| Unexpected RIVA point labels | PASS -- none | All observed values are in the manifest |
| Raw CRIC tree unchanged during Stage 04 | PASS | Pre/post file count and SHA-256 tree digest match; see Section 9 |
| Raw RIVA tree unchanged during Stage 04 | PASS | Pre/post file count and SHA-256 tree digest match; see Section 9 |

## 8. Explicit Stage 05 boundary

The following are intentionally deferred to Stage 05 and have not been implemented or decided here:

- common learning-unit definition;
- cell-centered crop definition;
- coordinate conversion;
- handling multiple RIVA annotators;
- clustering of annotations referring to the same cell;
- consensus/single-target construction;
- CRIC-to-RIVA sample-unit compatibility.

No preprocessing, cropping, sample generation, data splitting, clustering, consensus construction, model training, or Semi-SL implementation is part of Stage 04.

## 9. Raw-data preservation and reproducibility

Raw-file preservation was checked by enumerating every file under each raw dataset root, computing SHA-256 for each file, sorting the `path|file-hash` records, and hashing that canonical list. The following pre-Stage-04 tree digests must match post-Stage-04 verification:

| Raw root | File count | SHA-256 of canonical file-hash list |
|---|---:|---|
| `cric_cervix/` | 403 | `268355f3f2b9b01ad699869abc79560b41c3d0fc285c0e8839910b252d9a3f55` |
| `riva_1.0/` | 961 | `8c378cbe429f7c34423bf98b7fb2b4c3fa49484c8720ca0f1f39fcba58a37353` |

The validation used the local raw source files named in Section 2 and the mapping manifest in this folder. Counts are deterministic from those sources. No random seed applies because this stage performs deterministic label-inventory and arithmetic validation only.

## 10. Output files

- `documentation/stage_04_label_mapping/binary_label_mapping_manifest.csv`
- `documentation/stage_04_label_mapping/stage_04_label_mapping_report.md`

## 11. Next dependency

Stage 05 must determine a common, leakage-safe sample unit and the policy for raw multi-annotator RIVA records before this mapping can be attached to model-ready samples.
