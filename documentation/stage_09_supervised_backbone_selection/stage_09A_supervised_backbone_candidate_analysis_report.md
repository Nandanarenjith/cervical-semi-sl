# Stage 09A — Supervised Backbone Candidate Analysis

## 1. Purpose

Stage 09A evaluates candidate image-classification backbones for the supervised branch of the cervical cytology Semi-Supervised Learning (Semi-SL) framework.

The purpose of this stage is to establish a technically justified candidate pool before conducting practical backbone experimentation. The final backbone was intentionally not fixed during the design stage and was to be selected during implementation based on dataset characteristics, computational requirements, and experimental suitability.

The analysis considers both CNN-based and Transformer-based architectures to provide architectural diversity.

---

## 2. Dataset and Input Characteristics

The project uses cell-centered image crops generated during preprocessing.

| Property | Value |
|---|---|
| Primary pilot dataset | CRIC Cervix |
| Learning unit | Cell-centered crop |
| Crop size | 128 × 128 pixels |
| Image channels | RGB |
| Classification task | Binary |
| Class 0 | Normal / non-pathological |
| Class 1 | Abnormal / pathological |
| Training split | 8,274 learning units |
| Validation split | 1,539 learning units |
| Fixed random seed | 42 |

The fixed CRIC image-level train/validation/test partitions established in Stage 07 and frozen in Stage 08 were retained.

---

## 3. Candidate Backbone Pool

Six candidate architectures were considered.

| Backbone | Family | Approx. Parameters | Approx. GFLOPS | Pretraining | Rationale |
|---|---|---:|---:|---|---|
| ResNet-18 | CNN | 11.7M | 1.81 | ImageNet-1K | Lightweight general CNN baseline |
| DenseNet-121 | CNN | 8.0M | 2.83 | ImageNet-1K | Dense feature reuse and medical-imaging suitability |
| EfficientNet-B0 | CNN | 5.3M | 0.39 | ImageNet-1K | Parameter-efficient architecture with cervical Semi-SL precedent |
| ConvNeXt-Tiny | CNN | 28.6M | 4.46 | ImageNet-1K | Modern CNN architecture |
| Swin-Tiny | Transformer | 28.3M | 4.49 | ImageNet-1K | Hierarchical Transformer architecture |
| ViT-B/16 | Transformer | 86.6M | 17.56 | ImageNet-1K | Pure Vision Transformer architecture |

The parameter and computational figures are architecture-level reference values used for candidate analysis. Actual trainable parameter counts can differ after replacing the classification head with a two-class output.

---

## 4. Selection Considerations

The candidate architectures were considered using the following implementation-oriented criteria:

1. **Literature relevance**  
   Whether the architecture has demonstrated relevance to medical imaging or cervical cytology.

2. **Availability of pretrained weights**  
   Availability of ImageNet-pretrained models supports transfer learning and reduces the need to train large feature extractors from scratch.

3. **Compatibility with the project data**  
   The models need to be usable with the project's cell-centered crops.

4. **Model capacity**  
   The architecture should provide sufficient representation capacity for distinguishing normal and abnormal cervical cytology cells.

5. **Computational requirements**  
   The model should be practical for repeated experiments on the available RTX 4050 laptop GPU.

6. **Semi-SL compatibility**  
   The backbone should be suitable for later supervised and Semi-SL experiments using the same core architecture.

7. **Architectural diversity**  
   CNN and Transformer candidates were retained so that the practical pilot could compare different architectural families.

8. **Reproducibility**  
   The selected architecture should be practical to train repeatedly under controlled experimental conditions.

---

## 5. Candidate Evidence

The final candidate pool was intentionally kept broad enough to include lightweight CNNs, modern CNNs, and Transformer architectures.

### ResNet-18

ResNet-18 was included as a lightweight and widely established CNN baseline. Its relatively low computational requirement makes it suitable as a reference architecture.

### DenseNet-121

DenseNet-121 was included because dense feature reuse can provide effective representations while maintaining a moderate parameter count. Dense connectivity also makes it relevant to medical-imaging applications.

### EfficientNet-B0

EfficientNet-B0 was included because of its strong parameter and computational efficiency. It also has precedent in cervical cytology Semi-SL work, making it particularly relevant to the project.

### ConvNeXt-Tiny

ConvNeXt-Tiny represents a modern CNN design and provides a higher-capacity CNN candidate than ResNet-18, DenseNet-121, and EfficientNet-B0.

### Swin-Tiny

Swin-Tiny represents a hierarchical Transformer architecture. Its inclusion provides a Transformer alternative that uses local hierarchical processing rather than the global patch processing of a standard ViT.

### ViT-B/16

ViT-B/16 represents a pure Vision Transformer architecture and provides a high-capacity Transformer candidate. The standard TorchVision implementation requires 224 × 224 input images, which differs from the project's stored 128 × 128 crops and therefore requires model-specific input preprocessing.

---

## 6. Stage 09A Outcome

Stage 09A established the following six-model candidate pool:

- ResNet-18
- DenseNet-121
- EfficientNet-B0
- ConvNeXt-Tiny
- Swin-Tiny
- ViT-B/16

No backbone was selected solely from the literature analysis.

The candidate pool was carried forward to Stage 09B for controlled empirical evaluation on the actual CRIC training and validation data.

---

## 7. Reproducibility

The candidate analysis was documented in:

`notebooks/phase9a.ipynb`

The stage documentation is stored under:

`documentation/stage_09_supervised_backbone_selection/`

The analysis did not modify the raw datasets, fixed dataset partitions, or preprocessing outputs.