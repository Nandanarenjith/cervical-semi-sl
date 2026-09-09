# Stage 12 — Supervised 10% Baseline

## 1. Purpose

Stage 12 establishes the supervised learning baseline using 10% of the labeled training data from each dataset.

This stage provides the second supervised reference point for the later Semi-Supervised Learning experiments.

The 10% setting allows comparison with the 5% baseline and provides evidence about how supervised performance changes when twice as much labeled training data is available.

The same finalized training protocol used in Stage 11 is maintained.

---

# 2. Experimental Design

The fixed train/validation/test partitions established during earlier stages are used without modification.

### CRIC

| Split      | Learning Units |
| ---------- | -------------: |
| Training   |          8,274 |
| Validation |          1,539 |
| Test       |          1,721 |

10% labeled subset:

**827 labeled training learning units**

### RIVA

| Split      | Learning Units |
| ---------- | -------------: |
| Training   |         10,757 |
| Validation |          2,640 |
| Test       |          2,552 |

10% labeled subset:

**1,076 labeled training learning units**

The validation and test sets are kept unchanged and are not included in the labeled subset.

---

# 3. Binary Classification

Both datasets use the same harmonized binary task:

| Class | Meaning                   |
| ----- | ------------------------- |
| **0** | Normal / Non-pathological |
| **1** | Abnormal / Pathological   |

Class 1 includes abnormal and pathological categories, including both precancerous abnormalities and cancerous categories.

Therefore, the task should be described as:

**Normal vs Abnormal classification**

rather than cancer-vs-non-cancer classification.

---

# 4. Training Configuration

The official Phase 12 experiments use the finalized training protocol:

| Parameter               | Value               |
| ----------------------- | ------------------- |
| Backbone                | DenseNet-121        |
| Pretraining             | ImageNet            |
| Number of classes       | 2                   |
| Input size              | 128 × 128           |
| Optimizer               | AdamW               |
| Learning rate           | 1e-4                |
| Weight decay            | 1e-5                |
| Batch size              | 32                  |
| Maximum epochs          | 50                  |
| Early stopping patience | 8                   |
| Model-selection metric  | Validation Macro-F1 |
| Loss function           | Cross-Entropy Loss  |
| Random seed             | 42                  |
| Device                  | NVIDIA RTX 4050 GPU |

The maximum epoch value of 50 is an upper bound rather than a requirement to train for exactly 50 epochs.

Early stopping determines when training terminates based on validation Macro-F1.

---

# 5. Model Selection

The best checkpoint is selected according to validation Macro-F1.

Macro-F1 is used because the datasets contain class imbalance and the project aims to evaluate both Normal and Abnormal classes with equal importance during model selection.

The test set remains completely untouched until the final evaluation.

---

# 6. CRIC 10% Supervised Baseline

## 6.1 Experiment

**Experiment ID:**

`cric_supervised_10pct_densenet121_seed42`

Training samples:

**827**

Validation samples:

**1,539**

Test samples:

**1,721**

---

## 6.2 Training Behaviour

The model improved rapidly during the first several epochs.

The highest validation Macro-F1 occurred at:

**Epoch 5**

Best validation Macro-F1:

**0.907668**

Training continued after epoch 5 because early stopping allows validation fluctuations to be observed.

Training stopped at:

**Epoch 13**

after eight consecutive epochs without improvement over the best validation Macro-F1.

Training accuracy reached approximately 100% during later epochs, while validation Macro-F1 remained below the best value.

This indicates that the model was fitting the labeled training subset very strongly after the point at which validation performance had already peaked.

---

## 6.3 CRIC Test Results

The checkpoint from epoch 5 was evaluated on the untouched CRIC test set.

| Metric      |     Result |
| ----------- | ---------: |
| Accuracy    | **0.8669** |
| Precision   | **0.7981** |
| Sensitivity | **0.8385** |
| Specificity | **0.8827** |
| Macro-F1    | **0.8565** |
| AUROC       | **0.9266** |

Test samples:

**1,721**

Predictions generated:

**1,721**

---

# 7. RIVA 10% Supervised Baseline

## 7.1 Experiment

**Experiment ID:**

`riva_supervised_10pct_densenet121_seed42`

Training samples:

**1,076**

Validation samples:

**2,640**

Test samples:

**2,552**

---

## 7.2 Training Behaviour

The model showed rapid improvement in training performance.

The highest validation Macro-F1 occurred at:

**Epoch 15**

Best validation Macro-F1:

**0.785129**

Training stopped at:

**Epoch 23**

after eight consecutive epochs without improvement over the best validation Macro-F1.

Training accuracy approached 100% during later epochs while validation Macro-F1 fluctuated and declined after the best checkpoint.

This provides evidence of strong fitting of the labeled training data and limited additional validation benefit from continued training.

---

## 7.3 RIVA Test Results

The checkpoint from epoch 15 was evaluated on the untouched RIVA test set.

| Metric      |     Result |
| ----------- | ---------: |
| Accuracy    | **0.7010** |
| Precision   | **0.5815** |
| Sensitivity | **0.6024** |
| Specificity | **0.7564** |
| Macro-F1    | **0.6780** |
| AUROC       | **0.7507** |

Test samples:

**2,552**

Predictions generated:

**2,552**

---

# 8. CRIC vs RIVA — 10% Baseline

| Dataset | Accuracy | Precision | Sensitivity | Specificity | Macro-F1 |  AUROC |
| ------- | -------: | --------: | ----------: | ----------: | -------: | -----: |
| CRIC    |   0.8669 |    0.7981 |      0.8385 |      0.8827 |   0.8565 | 0.9266 |
| RIVA    |   0.7010 |    0.5815 |      0.6024 |      0.7564 |   0.6780 | 0.7507 |

The supervised 10% baseline produces higher test performance on CRIC than RIVA across all reported metrics.

This comparison is descriptive and does not by itself establish why the datasets differ in difficulty.

---

# 9. 5% vs 10% Supervised Baselines

The completed supervised experiments provide the following comparison.

| Dataset | Label Fraction | Accuracy | Precision | Sensitivity | Specificity | Macro-F1 |  AUROC |
| ------- | -------------: | -------: | --------: | ----------: | ----------: | -------: | -----: |
| CRIC    |             5% |   0.8332 |    0.7547 |      0.7879 |      0.8583 |   0.8199 | 0.9072 |
| CRIC    |            10% |   0.8669 |    0.7981 |      0.8385 |      0.8827 |   0.8565 | 0.9266 |
| RIVA    |             5% |   0.6799 |    0.5611 |      0.5054 |      0.7778 |   0.6443 | 0.7166 |
| RIVA    |            10% |   0.7010 |    0.5815 |      0.6024 |      0.7564 |   0.6780 | 0.7507 |

### Observed pattern

For CRIC, increasing the labeled fraction from 5% to 10% is associated with higher values for all six reported test metrics.

For RIVA, increasing the labeled fraction from 5% to 10% is associated with higher Accuracy, Precision, Sensitivity, Macro-F1, and AUROC, while Specificity decreases from 0.7778 to 0.7564.

These are observed experimental results and should be interpreted descriptively rather than as causal proof.

---

# 10. Interpretation

The 10% experiments provide a supervised reference with twice the labeled training fraction of the 5% setting.

The results show that additional labeled training data can be associated with improved supervised test performance, although the magnitude and behaviour differ between CRIC and RIVA.

The training histories also show that high training accuracy can be reached while validation performance stops improving, demonstrating the importance of validation-based checkpoint selection and early stopping.

The RIVA experiments remain more challenging than the corresponding CRIC experiments under the same overall training protocol.

---

# 11. Role in the Overall Study

Stage 12 completes the supervised baseline branch at the two core labeled-data settings:

* 5%
* 10%

These baselines provide the references needed for the Semi-SL experiments.

The later comparison will ask whether adding unlabeled training data through Semi-SL can improve over the corresponding supervised baseline.

For example:

**CRIC 5%**

> 414 labeled units → Supervised

versus

> 414 labeled units + remaining unlabeled training units → Semi-SL

Similarly:

**CRIC 10%**

> 827 labeled units → Supervised

versus

> 827 labeled units + remaining unlabeled training units → Semi-SL

The same structure will be applied to RIVA.

---

# 12. Reproducibility

The following were fixed:

* random seed: 42
* dataset partitions
* 10% label fraction
* DenseNet-121
* ImageNet initialization
* input resolution
* batch size
* optimizer
* learning rate
* weight decay
* maximum epochs
* early stopping patience
* validation Macro-F1 model selection

Experiment configurations, labeled subsets, metrics, histories, curves, and checkpoints are stored in the corresponding experiment directories.

---

# 13. Stage 12 Conclusion

Stage 12 successfully establishes the supervised 10% baselines for both CRIC and RIVA.

Final test Macro-F1 values are:

* **CRIC: 0.8565**
* **RIVA: 0.6780**

Together with Stage 11, these experiments establish the supervised reference framework required for the next stage: Semi-Supervised Learning.

The next experimental question is whether Semi-SL can use the unlabeled portion of the training data to improve performance over these supervised baselines, particularly when evaluating cross-dataset generalization.
