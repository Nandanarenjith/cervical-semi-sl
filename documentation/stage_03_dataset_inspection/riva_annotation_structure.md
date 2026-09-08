# RIVA Dataset: Annotation Structure

## Annotation file

File inspected:

`riva_1.0/annotations/annotations.json`

## Top-level structure

The JSON file is a dictionary.

Each key corresponds to a sample/image identifier.

Example:

`LSIL_45_3`

The value associated with each sample is another dictionary containing annotator-specific annotations.

## Annotator structure

A sample may contain annotations under keys such as:

- `annotator_1`
- `annotator_2`

Therefore, multiple annotators may have provided annotations for the same sample.

## Point annotation structure

Each annotation is represented as an object containing:

```text
x
y
keypointlabels

Example structure:

{
    "x": <coordinate>,
    "y": <coordinate>,
    "keypointlabels": "<label>"
}

The coordinates observed in the inspected entries range from approximately 0 to 100, indicating that they are likely normalized coordinates.

This must be verified against the RIVA dataset documentation or image dimensions before being used programmatically.

Observed keypoint labels

Labels observed in the inspected portion include:

NILM
ASCUS
INFL

The dataset contains additional diagnostic categories represented in sample identifiers, including:

LSIL
HSIL
SCC
ASCH

The complete annotation-label vocabulary has not yet been established.

Example observations

For sample LSIL_45_3, annotations from annotator_2 were observed.

The annotations included keypoints labelled ASCUS and INFL.

For sample LSIL_7_7, annotations from annotator_1 included keypoints labelled ASCUS, NILM, and INFL.

Interpretation status

At this stage, these labels are recorded as observed dataset labels only.

No assumptions are being made yet about:

binary classification labels,
positive/negative class definitions,
ground-truth generation,
annotator consensus,
or how cell-level annotations should be converted into an image/sample-level classification.

These decisions belong to later stages after the complete RIVA structure has been inspected.

Next inspection requirements

The next RIVA inspection should determine:

Total number of annotation entries
Complete set of annotation labels
Number of annotations per sample
Annotator distribution
Image count
Image filename structure
Image-to-annotation correspondence
Image dimensions
Whether sample identifiers encode the official diagnostic class
Whether patient/slide metadata is available
