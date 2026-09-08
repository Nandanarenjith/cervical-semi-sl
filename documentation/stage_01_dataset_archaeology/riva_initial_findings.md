# RIVA Dataset: Initial Archaeology Findings

## Dataset

Dataset: RIVA 1.0

The RIVA dataset is currently being inspected as one of the two core datasets for the cervical-semi-sl project.

## Initial folder structure

The dataset contains an `annotations` directory.

The annotation file currently identified is:

`riva_1.0/annotations/annotations.json`

An image directory is also present in the dataset and is being inspected for its exact structure and correspondence with the annotation entries.

## Annotation organization

The `annotations.json` file contains a JSON dictionary.

Each top-level key appears to identify an individual sample/image. Examples observed include:

- `LSIL_45_3`
- `LSIL_7_7`
- `HSIL_11_5`
- `SCC_3_1`
- `ASCUS_1_17`
- `NILM_1_1`

Each sample can contain annotations from one or more annotators.

Examples observed include:

- `annotator_1`
- `annotator_2`

## Initial observations

The annotation entries contain point annotations.

Each point contains:

- `x`
- `y`
- `keypointlabels`

The `x` and `y` values appear to be normalized coordinates rather than raw pixel coordinates, since observed values range approximately from 0 to 100.

Observed annotation labels include:

- `NILM`
- `ASCUS`
- `INFL`

Additional diagnostic categories are also represented in the sample identifiers, including:

- `LSIL`
- `HSIL`
- `SCC`
- `ASCH`

## Important caution

The diagnostic prefix in a sample identifier has NOT yet been formally established as the ground-truth classification field for our experiments.

The relationship between:

1. the sample/image identifier,
2. the annotation labels,
3. the annotators, and
4. the final dataset-level ground truth

must be investigated before defining the binary Normal/Abnormal mapping.

## Questions remaining

The following need to be investigated before preprocessing:

- Exact RIVA image folder structure
- Number of images
- Image formats
- Image dimensions
- Exact correspondence between image filenames and annotation keys
- Complete set of annotation labels
- Number of annotators and their coverage
- Whether annotations represent individual cells or another image/sample unit
- How the official RIVA ground truth should be interpreted
- Whether patient/slide identifiers are available
- Whether duplicate or related samples exist
- Whether an official train/test split exists

## Status

RIVA archaeology and inspection are IN PROGRESS.

No preprocessing or label mapping decisions have been made yet.