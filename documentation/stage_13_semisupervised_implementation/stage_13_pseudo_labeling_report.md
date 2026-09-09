# Stage 13 — Semi-Supervised Learning: Pseudo-Labeling

## 1. Purpose

Stage 13 implements and evaluates a pseudo-labeling based Semi-Supervised Learning (Semi-SL) method for cervical cytology image classification.

The purpose of this stage is to determine whether unlabeled source-domain data can improve classification performance when only a small fraction of the available source training data has ground-truth labels.

The experiment follows the project's predefined 5% labeled-data setting. The supervised baseline uses only the labeled 5% subset, while the Semi-SL experiment uses the same labeled subset together with high-confidence pseudo-labeled samples generated from the remaining unlabeled source-training data.

Pseudo-labeling is evaluated independently on both CRIC and RIVA.

The experiment is part of the broader research question:

> **Will semi-supervised learning help, hinder, or have no effect on cross-dataset generalization in cervical cytology?**

---

# 2. Experimental Design

The experiment follows the fixed train/validation/test partitions established during the earlier data-splitting and reproducibility stages.

For each dataset:

1. The frozen source-training partition is identified.
2. Five percent of the source-training units are selected as labeled data.
3. The remaining 95% of the source-training units are treated as unlabeled data.
4. A supervised warm-up model is trained using only the labeled 5%.
5. The warm-up model generates class predictions and confidence scores for the unlabeled data.
6. Only predictions satisfying a predefined confidence threshold are retained.
7. The retained predictions are assigned as pseudo-labels.
8. The original labeled data and accepted pseudo-labeled data are combined into a Semi-SL training pool.
9. A fresh DenseNet-121 model is trained on this combined pool.
10. Model selection is performed using validation Macro-F1.
11. The selected model is evaluated on the untouched source-domain test set.
12. Results are compared against the corresponding supervised 5% baseline.

The validation and test partitions remain separate from the pseudo-label generation process.

---

# 3. Binary Classification Task

Both datasets were harmonized to a binary classification task.

| Binary Label | Meaning                   |
| -----------: | ------------------------- |
|            0 | Normal / non-pathological |
|            1 | Abnormal / pathological   |

For evaluation, class `1` is treated as the positive class.

The evaluation metrics are:

* Accuracy
* Precision
* Sensitivity / Recall
* Specificity
* Macro-F1
* AUROC

Macro-F1 is used as the validation model-selection metric because the binary classes are not perfectly balanced and both classes should contribute to model-selection performance.

---

# 4. Backbone

The supervised backbone candidate analysis and controlled pilot in Stage 9 evaluated:

* ResNet-18
* DenseNet-121
* EfficientNet-B0
* ConvNeXt-Tiny
* Swin-Tiny
* ViT-B/16

DenseNet-121 was selected for subsequent experiments based on the practical trade-off between validation performance, computational cost, stability, and suitability for repeated experimentation.

The same DenseNet-121 backbone is used for the supervised and pseudo-labeling experiments to maintain a consistent comparison.

---

# 5. Training Configuration

The same core training configuration used for the finalized supervised baseline experiments is retained for the pseudo-labeling experiments.

| Parameter                   | Value                              |
| --------------------------- | ---------------------------------- |
| Backbone                    | DenseNet-121                       |
| Task                        | Binary classification              |
| Input size                  | 128 × 128                          |
| Optimizer                   | AdamW                              |
| Learning rate               | 0.0001                             |
| Weight decay                | 0.00001                            |
| Batch size                  | 32                                 |
| Maximum epochs              | 50                                 |
| Early-stopping patience     | 8                                  |
| Loss function               | Cross-Entropy Loss                 |
| Validation selection metric | Macro-F1                           |
| Random seed                 | 42                                 |
| Hardware                    | NVIDIA GeForce RTX 4050 Laptop GPU |
| Image normalization         | ImageNet normalization             |

The learning rate and weight decay correspond to the finalized supervised training protocol established before the Semi-SL experiments.

---

# 6. CRIC 5% Pseudo-Labeling

## 6.1 Data Pools

The frozen CRIC training partition contains 8,274 learning units.

At the 5% labeled setting:

| Pool                        | Units |
| --------------------------- | ----: |
| Full source training set    | 8,274 |
| Ground-truth labeled subset |   414 |
| Unlabeled subset            | 7,860 |
| Validation set              | 1,539 |
| Test set                    | 1,721 |

The labeled subset contains:

* 249 normal units
* 165 abnormal units

The unlabeled pool contains:

* 4,487 normal units
* 3,373 abnormal units

The ground-truth labels of the unlabeled pool are not used for pseudo-label generation or training.

---

## 6.2 Warm-Up Model

A DenseNet-121 model initialized using ImageNet-pretrained weights was trained using only the 414 labeled CRIC training units.

The model used:

* AdamW
* Learning rate = 1e-4
* Weight decay = 1e-5
* Batch size = 32
* Maximum epochs = 50
* Early-stopping patience = 8
* Validation Macro-F1 for model selection

The best warm-up checkpoint occurred at epoch 22, with a validation Macro-F1 of approximately 0.8892.

This checkpoint was subsequently used for pseudo-label generation.

---

## 6.3 Pseudo-Label Generation

The warm-up model was used to predict the unlabeled CRIC training units.

For each unlabeled sample:

1. The image was passed through the trained DenseNet-121.
2. Softmax probabilities were calculated.
3. The class with the highest probability was selected as the predicted class.
4. The highest probability was recorded as the confidence score.

Pseudo-label inference used the deterministic validation transformation rather than the stochastic training augmentation.

This ensures that pseudo-label generation is reproducible for a fixed model checkpoint and seed.

---

## 6.4 Confidence Threshold

A confidence threshold of:

**0.95**

was used for the final pseudo-label pool.

Predictions with confidence below 0.95 were rejected.

For CRIC:

| Category               | Count |
| ---------------------- | ----: |
| Unlabeled samples      | 7,860 |
| Accepted pseudo-labels | 5,918 |
| Rejected predictions   | 1,942 |

Accepted pseudo-label distribution:

| Pseudo-label | Count |
| -----------: | ----: |
|   0 — Normal | 3,454 |
| 1 — Abnormal | 2,464 |

The accepted pseudo-label pool therefore retained approximately 75.3% of the unlabeled samples.

The threshold was selected as a fixed high-confidence starting point rather than being presented as an empirically optimized threshold.

---

## 6.5 CRIC Semi-SL Training Pool

The final Semi-SL pool consisted of:

* 414 ground-truth labeled samples
* 5,918 accepted pseudo-labeled samples

Total:

**6,332 training samples**

The combined pool contained:

|        Label | Count |
| -----------: | ----: |
|   0 — Normal | 3,703 |
| 1 — Abnormal | 2,629 |

A fresh DenseNet-121 model was trained on this combined pool.

---

## 6.6 CRIC Semi-SL Training

The model was trained using the same core configuration as the supervised baseline.

The best validation Macro-F1 was:

**0.9119**

at epoch 1.

Early stopping occurred at epoch 9.

The best checkpoint was saved at:

`data/checkpoints/phase13/cric_pseudolabel_5pct/best_model.pt`

---

## 6.7 CRIC Test Results

The best Semi-SL checkpoint was evaluated on the untouched CRIC test set.

| Metric      | Supervised 5% | Pseudo-Labeling 5% | Difference |
| ----------- | ------------: | -----------------: | ---------: |
| Accuracy    |        0.8332 |             0.8466 |    +0.0134 |
| Precision   |        0.7547 |             0.7374 |    -0.0173 |
| Sensitivity |        0.7879 |             0.8842 |    +0.0963 |
| Specificity |        0.8583 |             0.8258 |    -0.0325 |
| Macro-F1    |        0.8199 |             0.8390 |    +0.0191 |
| AUROC       |        0.9072 |             0.9302 |    +0.0230 |

### CRIC Observation

Compared with the supervised 5% baseline:

* Accuracy increased by 1.34 percentage points.
* Sensitivity increased by 9.63 percentage points.
* Macro-F1 increased by 1.91 percentage points.
* AUROC increased by 2.30 percentage points.
* Precision decreased by 1.73 percentage points.
* Specificity decreased by 3.25 percentage points.

Therefore, under this single CRIC 5% pseudo-labeling experiment, the Semi-SL model produced higher Accuracy, Sensitivity, Macro-F1, and AUROC than the supervised baseline, while Precision and Specificity decreased.

No causal explanation is assigned to these changes at this stage.

---

# 7. RIVA 5% Pseudo-Labeling

## 7.1 Data Pools

The frozen RIVA training partition contains 10,757 learning units.

At the 5% labeled setting:

| Pool                        |  Units |
| --------------------------- | -----: |
| Full source training set    | 10,757 |
| Ground-truth labeled subset |    538 |
| Unlabeled subset            | 10,219 |
| Validation set              |  2,640 |
| Test set                    |  2,552 |

The labeled and unlabeled pools were generated from the fixed RIVA training partition using the project random seed.

---

## 7.2 Warm-Up Model

A DenseNet-121 model was trained using only the 538 labeled RIVA training units.

The training configuration remained identical to the CRIC experiment:

* AdamW
* Learning rate = 1e-4
* Weight decay = 1e-5
* Batch size = 32
* Maximum epochs = 50
* Early-stopping patience = 8
* Validation Macro-F1 for model selection
* Random seed = 42

The resulting warm-up checkpoint was used to generate predictions for the unlabeled RIVA training pool.

---

## 7.3 Deterministic Pseudo-Label Generation

The warm-up RIVA model was used to predict all 10,219 unlabeled RIVA training units.

For each sample, the predicted class and maximum softmax probability were recorded.

The deterministic validation transformation was used for inference so that pseudo-label generation was not affected by random training augmentation.

---

## 7.4 Confidence Threshold

The same fixed confidence threshold used for the CRIC experiment was applied:

**0.95**

Only predictions with confidence ≥ 0.95 were accepted into the final pseudo-labeled pool.

The threshold was treated as a predefined high-confidence operating point rather than as a dataset-specific optimized parameter.

---

## 7.5 RIVA Semi-SL Training

The accepted pseudo-labeled samples were combined with the 538 ground-truth labeled samples.

A fresh DenseNet-121 model was then trained using the combined Semi-SL pool.

The training configuration remained identical to the supervised and CRIC pseudo-labeling experiments.

The best validation Macro-F1 was:

**0.7870**

at epoch 15.

Training continued until early stopping was triggered at epoch 23.

The best checkpoint was saved at:

`data/checkpoints/phase13/riva_pseudolabel_5pct/best_model.pt`

---

# 8. RIVA Test Results

The best RIVA Semi-SL checkpoint was evaluated on the untouched RIVA test partition.

| Metric      | Supervised 5% | Pseudo-Labeling 5% | Difference |
| ----------- | ------------: | -----------------: | ---------: |
| Accuracy    |        0.6799 |             0.6516 |    -0.0283 |
| Precision   |        0.5611 |             0.5167 |    -0.0444 |
| Sensitivity |        0.5054 |             0.4891 |    -0.0163 |
| Specificity |        0.7778 |             0.7430 |    -0.0348 |
| Macro-F1    |        0.6443 |             0.6173 |    -0.0270 |
| AUROC       |        0.7166 |             0.7077 |    -0.0089 |

### RIVA Observation

Compared with the supervised 5% baseline, pseudo-labeling produced lower values for all six evaluated test metrics:

* Accuracy decreased by 2.83 percentage points.
* Precision decreased by 4.44 percentage points.
* Sensitivity decreased by 1.63 percentage points.
* Specificity decreased by 3.48 percentage points.
* Macro-F1 decreased by 2.70 percentage points.
* AUROC decreased by 0.89 percentage points.

Therefore, under this single RIVA 5% pseudo-labeling experiment, pseudo-labeling did not improve performance relative to the supervised 5% baseline.

---

# 9. Cross-Dataset Comparison of Pseudo-Labeling Behavior

The two datasets produced different outcomes under the same general pseudo-labeling methodology.

| Dataset | Supervised Macro-F1 | Pseudo-Label Macro-F1 | Difference |
| ------- | ------------------: | --------------------: | ---------: |
| CRIC    |              0.8199 |                0.8390 |    +0.0191 |
| RIVA    |              0.6443 |                0.6173 |    -0.0270 |

The corresponding AUROC values were:

| Dataset | Supervised AUROC | Pseudo-Label AUROC | Difference |
| ------- | ---------------: | -----------------: | ---------: |
| CRIC    |           0.9072 |             0.9302 |    +0.0230 |
| RIVA    |           0.7166 |             0.7077 |    -0.0089 |

These results demonstrate that the effect of pseudo-labeling was not uniform across the two datasets.

CRIC showed an improvement in Macro-F1 and AUROC, whereas RIVA showed a decrease in both metrics.

This dataset-dependent behavior is directly relevant to the project's broader objective of determining whether Semi-SL helps, hinders, or has no effect under different data conditions.

However, these observations should not yet be interpreted as evidence of a specific causal mechanism. Further Semi-SL methods and cross-dataset experiments are required.

---

# 10. Model Selection and Evaluation Integrity

The following principles were maintained during the experiments:

### Fixed data partitions

The train, validation, and test assignments were inherited from the frozen split stage.

### Same labeled fraction

Both supervised and pseudo-labeling experiments use the same 5% labeled setting.

### Same backbone

DenseNet-121 is used for both branches.

### Same core optimization configuration

The optimizer, learning rate, weight decay, batch size, maximum epochs, early-stopping patience, and random seed are kept consistent.

### Validation-based model selection

Macro-F1 on the validation partition is used to select the best checkpoint.

### Independent test evaluation

The test partition is not used for model selection or pseudo-label generation.

### Deterministic pseudo-label inference

The final pseudo-label generation uses the deterministic validation transformation.

---

# 11. Reproducibility

The experiments use:

* Random seed: 42
* Fixed train/validation/test splits
* Fixed 5% labeled fraction
* DenseNet-121
* Fixed training configuration
* Fixed pseudo-label confidence threshold of 0.95
* Recorded experiment identifiers
* Saved model checkpoints
* Saved training histories
* Saved evaluation metrics
* Saved pseudo-label statistics
* Saved comparison tables
* Saved training curves

The experiment identifiers are:

### CRIC

`cric_pseudolabel_5pct_densenet121_seed42`

### RIVA

`riva_pseudolabel_5pct_densenet121_seed42`

---

# 12. Saved Artifacts

## CRIC

Results:

`data/results/phase13/cric_pseudolabel_5pct_densenet121_seed42/`

The directory contains:

* `metrics.json`
* `supervised_vs_pseudolabeling.csv`
* `pseudo_label_statistics.json`
* `training_history.csv`
* `training_history.json`
* `artifact_summary.json`
* `curves/loss_curve.png`
* `curves/accuracy_curve.png`
* `curves/macro_f1_curve.png`
* `curves/sensitivity_specificity_curve.png`

Checkpoint:

`data/checkpoints/phase13/cric_pseudolabel_5pct/best_model.pt`

Warm-up checkpoint:

`data/checkpoints/phase13/cric_pseudolabel_5pct_warmup/best_model.pt`

---

## RIVA

Results:

`data/results/phase13/riva_pseudolabel_5pct_densenet121_seed42/`

The directory contains:

* `metrics.json`
* `supervised_vs_pseudolabeling.csv`
* `pseudo_label_statistics.json`
* `training_history.csv`
* `training_history.json`
* `artifact_summary.json`
* `curves/loss_curve.png`
* `curves/accuracy_curve.png`
* `curves/macro_f1_curve.png`
* `curves/sensitivity_specificity_curve.png`

Checkpoint:

`data/checkpoints/phase13/riva_pseudolabel_5pct/best_model.pt`

Warm-up checkpoint:

`data/checkpoints/phase13/riva_pseudolabel_5pct_warmup/best_model.pt`

---

# 13. Interpretation

The 5% pseudo-labeling experiments produced contrasting outcomes.

For CRIC, pseudo-labeling improved several overall performance measures relative to the supervised 5% baseline, particularly Sensitivity, Macro-F1, and AUROC.

For RIVA, pseudo-labeling reduced all evaluated test metrics relative to the corresponding supervised baseline.

Therefore, the current evidence does not support a general statement that pseudo-labeling consistently improves cervical cytology classification under limited labels.

Instead, the initial experiments show that the effect of pseudo-labeling can differ between datasets.

This is an important experimental observation because the project's objective is not to assume that Semi-SL always helps, but to investigate whether it can help, hinder, or have no effect under different dataset conditions.

The present results are based on one seed and one pseudo-labeling configuration per dataset. Consequently, they should be treated as controlled experimental observations rather than definitive statistical conclusions.

---

# 14. Limitations of the Current Experiment

The following limitations apply to the current Stage 13 results:

1. Only the 5% labeled setting has been evaluated with pseudo-labeling.
2. Only one Semi-SL algorithm has been evaluated so far.
3. The experiments use a single random seed.
4. The confidence threshold is fixed at 0.95 and has not been comprehensively optimized.
5. The experiments do not yet establish why the two datasets respond differently.
6. Cross-dataset transfer evaluation has not yet been performed for this Semi-SL model.

These limitations are addressed through subsequent Semi-SL and cross-dataset experiments.

---

# 15. Stage 13 Conclusion

Stage 13 successfully implemented pseudo-labeling based Semi-Supervised Learning for the 5% labeled setting on both CRIC and RIVA.

The implementation used a supervised warm-up model to generate high-confidence pseudo-labels from the remaining unlabeled source-training data. A fresh DenseNet-121 model was then trained using the combination of ground-truth and accepted pseudo-labeled samples.

The experimental results were dataset-dependent:

* **CRIC:** Macro-F1 increased from 0.8199 to 0.8390.
* **RIVA:** Macro-F1 decreased from 0.6443 to 0.6173.

Thus, the initial pseudo-labeling experiments demonstrate that Semi-SL does not necessarily provide a uniform benefit across cervical cytology datasets.

These results provide the first experimental evidence for the project's broader investigation into whether Semi-SL can help, hinder, or have no effect under different data conditions.

Stage 13 therefore establishes the initial pseudo-labeling baseline for comparison with additional Semi-SL methods and later cross-dataset evaluation.
