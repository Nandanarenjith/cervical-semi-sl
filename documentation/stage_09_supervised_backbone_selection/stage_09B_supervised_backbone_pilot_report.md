# Stage 09B — Supervised Backbone Practical Pilot

## 1. Purpose

Stage 09B performs a controlled practical pilot to select the supervised backbone for the subsequent experiments.

Unlike Stage 09A, which established the candidate pool from architectural and implementation considerations, Stage 09B evaluates the candidate architectures empirically using the actual CRIC cell-centered crops.

The objective is not to establish final research performance. Instead, the pilot provides evidence for selecting a backbone that offers a strong combination of validation performance, training stability, and computational practicality for the repeated supervised and Semi-SL experiments that follow.

---

## 2. Experimental Dataset

The pilot was performed using the fixed CRIC dataset partitions established during Stages 07 and 08.

| Property | Value |
|---|---|
| Dataset | CRIC Cervix |
| Training learning units | 8,274 |
| Validation learning units | 1,539 |
| Test learning units | Not used for backbone selection |
| Input crop | 128 × 128 RGB |
| Classification | Binary |
| Class 0 | Normal / non-pathological |
| Class 1 | Abnormal / pathological |
| Random seed | 42 |

The test split was not used during backbone selection.

This preserves the test set for subsequent evaluation.

---

## 3. Pilot Configuration

The same core training configuration was applied to the candidate models.

| Parameter | Setting |
|---|---|
| Epochs | 3 |
| Batch size | 32 |
| Optimizer | AdamW |
| Learning rate | 1 × 10⁻⁴ |
| Loss | Cross-Entropy Loss |
| GPU | NVIDIA GeForce RTX 4050 Laptop GPU |
| Primary validation metric | Macro-F1 |
| Additional metric | Accuracy |

ImageNet-pretrained weights were used where available.

The stored project crops remained 128 × 128 pixels.

For ViT-B/16, which requires 224 × 224 input in the TorchVision implementation, the 128 × 128 crop was resized to 224 × 224 at model input time. The stored crop itself was not modified.

---

## 4. Candidate Architectures

The following six candidates were evaluated:

1. ResNet-18
2. DenseNet-121
3. EfficientNet-B0
4. ConvNeXt-Tiny
5. Swin-Tiny
6. ViT-B/16

All models were modified to produce two output classes corresponding to the binary project labels.

---

## 5. Pilot Results

The following results were obtained from the controlled three-epoch pilot.

| Backbone | Best Validation Macro-F1 | Best Validation Accuracy | Training Time |
|---|---:|---:|---:|
| ViT-B/16 | **0.937684** | **0.940871** | 3066.99 s |
| DenseNet-121 | 0.934519 | 0.937622 | 121.52 s |
| Swin-Tiny | 0.932256 | 0.935023 | 200.44 s |
| ConvNeXt-Tiny | 0.927991 | 0.931124 | 158.84 s |
| EfficientNet-B0 | 0.917731 | 0.921378 | 81.85 s |
| ResNet-18 | 0.914962 | 0.918129 | 65.24 s |

---

## 6. Training Behaviour

### ResNet-18

ResNet-18 reached a validation Macro-F1 of 0.9150 at its best epoch.

Its training performance increased rapidly, while validation performance decreased slightly after the first epoch:

| Epoch | Train Macro-F1 | Validation Macro-F1 |
|---|---:|---:|
| 1 | 0.8760 | 0.9150 |
| 2 | 0.9674 | 0.9136 |
| 3 | 0.9858 | 0.9046 |

This indicates increasing separation between training and validation performance during the short pilot.

---

### DenseNet-121

DenseNet-121 showed strong and relatively stable validation performance.

| Epoch | Train Macro-F1 | Validation Macro-F1 |
|---|---:|---:|
| 1 | 0.8825 | 0.9174 |
| 2 | 0.9663 | 0.9307 |
| 3 | 0.9865 | **0.9345** |

Validation Macro-F1 improved throughout the three-epoch pilot, reaching the second-highest overall value among the candidates.

---

### EfficientNet-B0

EfficientNet-B0 showed steady improvement but achieved lower validation performance than DenseNet-121 and the Transformer candidates.

| Epoch | Train Macro-F1 | Validation Macro-F1 |
|---|---:|---:|
| 1 | 0.8253 | 0.8993 |
| 2 | 0.9231 | 0.9140 |
| 3 | 0.9595 | 0.9177 |

Its main advantage was computational efficiency.

---

### ConvNeXt-Tiny

ConvNeXt-Tiny produced strong validation performance and remained competitive with the other higher-capacity architectures.

| Epoch | Train Macro-F1 | Validation Macro-F1 |
|---|---:|---:|
| 1 | 0.8837 | 0.9257 |
| 2 | 0.9606 | **0.9280** |
| 3 | 0.9833 | 0.9236 |

The highest validation Macro-F1 occurred at epoch 2.

---

### Swin-Tiny

Swin-Tiny achieved strong validation performance with a relatively stable first two epochs.

| Epoch | Train Macro-F1 | Validation Macro-F1 |
|---|---:|---:|
| 1 | 0.8805 | 0.9303 |
| 2 | 0.9331 | **0.9323** |
| 3 | 0.9573 | 0.9263 |

Its best validation Macro-F1 was 0.9323.

---

### ViT-B/16

ViT-B/16 achieved the highest validation Macro-F1 and accuracy in the pilot.

| Epoch | Train Macro-F1 | Validation Macro-F1 |
|---|---:|---:|
| 1 | 0.8691 | **0.9377** |
| 2 | 0.9248 | 0.7905 |
| 3 | 0.9461 | 0.9235 |

However, the model required substantially more training time than the CNN candidates.

The three-epoch training time was approximately 3,067 seconds, or about 51 minutes, compared with approximately 122 seconds for DenseNet-121.

The validation behaviour also showed a substantial temporary drop during epoch 2.

---

## 7. Backbone Selection

### Selected Backbone: DenseNet-121

DenseNet-121 was selected as the supervised backbone for the subsequent project experiments.

The selection was based on the combination of:

- strong validation Macro-F1;
- strong validation accuracy;
- stable improvement across the three pilot epochs;
- substantially lower computational cost than ViT-B/16;
- practical suitability for repeated experiments;
- availability of ImageNet-pretrained weights;
- suitability for the planned supervised and Semi-SL branches.

ViT-B/16 achieved a slightly higher best validation Macro-F1:

- ViT-B/16: **0.937684**
- DenseNet-121: **0.934519**

The absolute difference was approximately **0.0032 Macro-F1**.

However, ViT-B/16 required approximately **25 times more training time** than DenseNet-121 in this pilot.

Therefore, selecting ViT-B/16 solely because of its highest validation score would provide only a marginal pilot improvement at a substantially higher computational cost.

DenseNet-121 provides a more practical balance between predictive performance and computational efficiency for the larger set of experiments required in the project.

---

## 8. Interpretation and Scope

The pilot is a backbone-selection experiment and should not be interpreted as the final performance comparison of the research methods.

In particular:

- The pilot used only three epochs.
- The validation set was used for model/backbone selection.
- The test set was not used.
- The pilot does not establish the final performance of DenseNet-121.
- The pilot does not establish whether Semi-SL improves generalization.
- The pilot does not replace the planned supervised baselines or cross-dataset experiments.

The selected DenseNet-121 backbone will therefore be used consistently in subsequent controlled experiments to allow fair comparison between supervised and Semi-SL approaches.

---

## 9. Reproducibility Artifacts

The practical pilot was implemented in:

`notebooks/phase9b.ipynb`

The complete pilot results were saved to:

`data/results/phase9b/backbone_pilot_results.csv`

The backbone selection record was saved to:

`data/results/phase9b/backbone_selection.json`

The selected backbone recorded in the selection record is:

`DenseNet-121`

The experiment used the fixed dataset partitions established in Stage 08 and did not modify the raw dataset or preprocessing outputs.

---

## 10. Stage 09 Outcome

Stage 09 established the supervised backbone for the remainder of the experimental framework.

### Final decision

**DenseNet-121**

### Basis

**Strong validation performance + stable pilot behaviour + substantially lower computational cost + suitability for repeated supervised and Semi-SL experiments.**

Stage 09 is therefore complete.