# Stage 11 — Supervised 5% Baseline

## 1. Purpose

Stage 11 establishes the supervised learning baseline using only 5% of the labeled training data from each dataset.

The purpose of this stage is to provide a controlled supervised reference against which the later Semi-Supervised Learning (Semi-SL) methods can be compared.

The supervised model uses:

* DenseNet-121 backbone
* ImageNet-pretrained weights
* Binary Normal vs Abnormal classification
* AdamW optimizer
* Cross-Entropy Loss
* Fixed 5% labeled training subset
* Validation Macro-F1 for model selection
* Fixed validation and test sets
* Early stopping

The same training protocol is applied independently to CRIC and RIVA.

---

## 2. Experimental Design

The project uses fixed group-aware train/validation/test splits established during earlier stages.

### CRIC

| Split      | Learning Units |
| ---------- | -------------: |
| Training   |          8,274 |
| Validation |          1,539 |
| Test       |          1,721 |

The 5% labeled subset contains:

**414 labeled training learning units**

The validation and test sets remain unchanged and are not included in the labeled subset.

### RIVA

| Split      | Learning Units |
| ---------- | -------------: |
| Training   |         10,757 |
| Validation |          2,640 |
| Test       |          2,552 |

The 5% labeled subset contains:

**538 labeled training learning units**

The validation and test sets remain unchanged.

---

## 3. Binary Classification

Both datasets are harmonized into two classes.

### Class 0 — Normal / Non-pathological

Class 0 represents cells without pathological abnormality under the project-level binary mapping.

### Class 1 — Abnormal / Pathological

Class 1 represents abnormal/pathological cells.

This class includes both precancerous abnormalities and cancerous categories.

Therefore, this is **not a cancer-vs-non-cancer classification task**.

The classification task is:

**Normal / Non-pathological vs Abnormal / Pathological**

---

## 4. Training Configuration

The finalized training configuration used for the official Phase 11 experiments is:

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

The 50-epoch value represents the maximum training duration. Training may terminate earlier when the validation Macro-F1 fails to improve for the specified patience period.

---

## 5. Model Selection

The best model checkpoint is selected using **validation Macro-F1**.

Macro-F1 was selected because the binary classes are not perfectly balanced, and the project aims to give equal importance to the Normal and Abnormal classes during model selection.

The test set is not used for:

* training,
* checkpoint selection,
* hyperparameter tuning, or
* early stopping.

The test set is reserved for final evaluation.

---

# 6. CRIC 5% Supervised Baseline

## 6.1 Experiment

**Experiment ID:**

`cric_supervised_5pct_densenet121_seed42`

Training samples:

**414**

Validation samples:

**1,539**

Test samples:

**1,721**

---

## 6.2 Training Behaviour

The model reached very high training accuracy rapidly.

Training accuracy reached approximately 100% from epoch 7 onward, while validation Macro-F1 continued to fluctuate.

The best validation Macro-F1 occurred at:

**Epoch 13**

Best validation Macro-F1:

**0.886325**

Training stopped at:

**Epoch 21**

because the validation Macro-F1 did not improve for eight consecutive epochs after the best checkpoint.

This behaviour is consistent with the limited amount of labeled training data available in the 5% setting. The model can fit the small labeled subset very strongly, while validation performance does not continue improving at the same rate.

---

## 6.3 CRIC Test Results

The best checkpoint from epoch 13 was evaluated on the untouched CRIC test set.

| Metric      |     Result |
| ----------- | ---------: |
| Accuracy    | **0.8332** |
| Precision   | **0.7547** |
| Sensitivity | **0.7879** |
| Specificity | **0.8583** |
| Macro-F1    | **0.8199** |
| AUROC       | **0.9072** |

Test samples:

**1,721**

Predictions generated:

**1,721**

---

# 7. RIVA 5% Supervised Baseline

## 7.1 Experiment

**Experiment ID:**

`riva_supervised_5pct_densenet121_seed42`

Training samples:

**538**

Validation samples:

**2,640**

Test samples:

**2,552**

---

## 7.2 Training Behaviour

The model rapidly increased its training accuracy, reaching approximately 100% during later epochs.

Validation performance improved initially but subsequently fluctuated.

The best validation Macro-F1 occurred at:

**Epoch 13**

Best validation Macro-F1:

**0.753238**

Training stopped at:

**Epoch 21**

after eight consecutive epochs without improvement in validation Macro-F1.

The separation between near-perfect training accuracy and substantially lower validation performance indicates strong fitting of the limited labeled training subset.

---

## 7.3 RIVA Test Results

The best checkpoint from epoch 13 was evaluated on the untouched RIVA test set.

| Metric      |     Result |
| ----------- | ---------: |
| Accuracy    | **0.6799** |
| Precision   | **0.5611** |
| Sensitivity | **0.5054** |
| Specificity | **0.7778** |
| Macro-F1    | **0.6443** |
| AUROC       | **0.7166** |

Test samples:

**2,552**

Predictions generated:

**2,552**

---

# 8. CRIC vs RIVA — 5% Baseline

| Dataset | Accuracy | Precision | Sensitivity | Specificity | Macro-F1 |  AUROC |
| ------- | -------: | --------: | ----------: | ----------: | -------: | -----: |
| CRIC    |   0.8332 |    0.7547 |      0.7879 |      0.8583 |   0.8199 | 0.9072 |
| RIVA    |   0.6799 |    0.5611 |      0.5054 |      0.7778 |   0.6443 | 0.7166 |

The supervised 5% baseline shows higher test performance on CRIC than on RIVA across all reported metrics.

This result is descriptive and does not by itself establish the cause of the performance difference.

---

# 9. Interpretation

The 5% experiments demonstrate that supervised learning is feasible with a small labeled subset, but the models can fit the available labeled examples very strongly.

Both experiments show:

* rapid improvement in training performance,
* near-perfect training accuracy during later epochs,
* lower and more variable validation performance,
* early stopping before the maximum of 50 epochs.

The difference between training and validation behaviour is consistent with overfitting pressure in the low-label regime.

The RIVA baseline produces lower test performance than the CRIC baseline under the same overall training protocol.

These supervised baselines provide the reference point for the upcoming Semi-SL experiments.

---

# 10. Role in the Overall Study

The Phase 11 supervised baseline is important because later Semi-SL experiments will use the same 5% labeled setting.

The key comparison will be:

**5% Supervised**

> 5% labeled data → supervised DenseNet-121

versus

**5% Semi-SL**

> 5% labeled data + remaining unlabeled training data → Semi-SL DenseNet-121

This allows the effect of using unlabeled data to be evaluated under a controlled comparison.

---

# 11. Reproducibility

The following were fixed for the experiments:

* random seed: 42
* dataset partitions
* 5% label fraction
* DenseNet-121 backbone
* ImageNet initialization
* image size
* batch size
* optimizer
* learning rate
* weight decay
* maximum epochs
* early stopping patience
* validation Macro-F1 model selection

Experiment-specific configurations, labeled subsets, metrics, training histories, curves, and model checkpoints are stored under the project's experiment results and checkpoint directories.

---

# 12. Stage 11 Conclusion

Stage 11 successfully establishes the supervised 5% baseline for both CRIC and RIVA.

The final test Macro-F1 values are:

* **CRIC: 0.8199**
* **RIVA: 0.6443**

These results form the supervised reference for evaluating whether Semi-Supervised Learning can make better use of limited labeled data and improve generalization, particularly under cross-dataset evaluation.
