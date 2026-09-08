# Stage 10 — Training Infrastructure

## 1. Purpose

Stage 10 establishes the reusable and reproducible training infrastructure required for all downstream supervised and semi-supervised experiments.

The purpose of this stage is **not** to produce research conclusions or final model performance results. Instead, it verifies that the project has a stable training framework capable of supporting:

- supervised training,
- limited-label experiments,
- semi-supervised learning,
- source-domain evaluation,
- cross-dataset evaluation,
- checkpointing,
- early stopping,
- reproducibility,
- future backbone replacement,
- experiment logging,
- and later ablation experiments.

The infrastructure was implemented around the backbone selected during Stage 09B:

**DenseNet-121**

The implementation was intentionally designed so that the backbone itself is configurable rather than making DenseNet-121 the identity of the entire project.

---

## 2. Relationship to Previous Stages

Stage 10 depends on the outputs of the preceding stages.

The required upstream flow is:

Data acquisition
→ label harmonization
→ learning-unit standardization
→ preprocessing
→ fixed dataset splits
→ reproducibility freeze
→ backbone candidate analysis
→ supervised backbone pilot
→ training infrastructure

The infrastructure therefore assumes that:

1. CRIC learning units have already been standardized.
2. RIVA learning units have already been standardized.
3. Binary labels are already available.
4. Cell crops have already been generated.
5. Fixed train/validation/test assignments already exist.
6. CRIC grouping is image-level.
7. RIVA grouping is slide-level.
8. The selected supervised backbone is DenseNet-121.
9. The core experimental label fractions will later be 5% and 10%.

Stage 10 does **not** redefine any of those decisions.

---

## 3. Research Scope Preserved by Stage 10

The downstream research question remains:

> Will semi-supervised learning help, hinder, or have no effect on cross-dataset generalization in cervical cytology?

Stage 10 provides the machinery required to compare:

- supervised learning using a limited labeled subset,
- Semi-SL using the same labeled subset plus available unlabeled source data,
- source-domain performance,
- target-domain performance,
- and cross-domain degradation.

The infrastructure must therefore remain neutral enough that the supervised and Semi-SL branches can use the same underlying model architecture and evaluation framework.

---

## 4. Project Directory Structure

The Stage 10 implementation introduced the following reusable source modules:

```text
cervical-semi-sl/
│
├── configs/
│
├── data/
│   ├── processed/
│   │   ├── cric_crops/
│   │   ├── riva_crops/
│   │   ├── cric_learning_units.csv
│   │   └── riva_learning_units.csv
│   │
│   ├── splits/
│   │   ├── cric_splits.csv
│   │   └── riva_splits.csv
│   │
│   ├── checkpoints/
│   └── results/
│
├── documentation/
│   └── stage_10_training_infrastructure/
│
├── notebooks/
│   ├── phase10.ipynb
│   ├── phase11.ipynb
│   ├── phase12.ipynb
│   ├── phase13.ipynb
│   └── ...
│
└── src/
    └── cervical_ssl/
        ├── __init__.py
        ├── config.py
        ├── models.py
        ├── transforms.py
        ├── datasets.py
        ├── training.py
        ├── evaluation.py
        ├── checkpoints.py
        └── utils.py
```

The important architectural principle is:

```text
notebooks/
    ↓
experiment orchestration

src/cervical_ssl/
    ↓
reusable implementation

configs/
    ↓
experiment configuration

data/
    ↓
datasets, splits, checkpoints, results

documentation/
    ↓
research record
```

---

## 5. Why the Training Code Was Moved into `src/`

The project initially used notebook-based experimentation.

That is useful during exploration, but downstream research experiments require repeated execution under controlled conditions.

If the entire training implementation is copied independently into:

```text
phase11.ipynb
phase12.ipynb
phase13.ipynb
phase15.ipynb
```

then small differences can silently appear between experiments.

That creates a reproducibility risk.

Instead, the reusable implementation is stored in:

```text
src/cervical_ssl/
```

while notebooks control individual experiments.

This produces the following structure:

```text
Phase 11 notebook
       ↓
same training implementation

Phase 12 notebook
       ↓
same training implementation

Phase 13 notebook
       ↓
same training implementation
```

The notebooks should therefore contain experiment-specific configuration and orchestration rather than duplicated versions of the training engine.

---

## 6. `__init__.py`

File:

```text
src/cervical_ssl/__init__.py
```

Current status:

```text
EMPTY
```

This is intentional.

The file does not need to contain project logic.

Its current role is simply to allow `cervical_ssl` to function as a Python package.

For example:

```python
from src.cervical_ssl.models import create_model
```

works without requiring logic inside `__init__.py`.

There is no reason to populate the file merely for the sake of having content.

If package-level exports become useful later, they can be added, but this is not required by the current research design.

---

## 7. `utils.py`

File:

```text
src/cervical_ssl/utils.py
```

Current status:

```text
EMPTY
```

This is also intentional.

No arbitrary helper functions were placed into this file simply to make it non-empty.

Future functions should only be added here if they are genuinely shared by multiple modules.

Potential future examples include:

```python
set_seed()
save_json()
count_parameters()
create_experiment_directory()
```

However, these should only be added when the project actually needs them.

The principle is:

```text
Do not create utility functions just because a utils.py file exists.
```

---

# 8. `config.py`

File:

```text
src/cervical_ssl/config.py
```

Current implementation:

```python
from pathlib import Path


# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_ROOT = PROJECT_ROOT / "data"

PROCESSED_ROOT = DATA_ROOT / "processed"
SPLITS_ROOT = DATA_ROOT / "splits"
RESULTS_ROOT = DATA_ROOT / "results"
CHECKPOINT_ROOT = DATA_ROOT / "checkpoints"

CONFIG_ROOT = PROJECT_ROOT / "configs"


# ============================================================
# Dataset paths
# ============================================================

CRIC_CROPS = PROCESSED_ROOT / "cric_crops"
CRIC_MANIFEST = PROCESSED_ROOT / "cric_learning_units.csv"
CRIC_SPLITS = SPLITS_ROOT / "cric_splits.csv"

RIVA_CROPS = PROCESSED_ROOT / "riva_crops"
RIVA_MANIFEST = PROCESSED_ROOT / "riva_learning_units.csv"
RIVA_SPLITS = SPLITS_ROOT / "riva_splits.csv"


# ============================================================
# Reproducibility
# ============================================================

RANDOM_SEED = 42


# ============================================================
# Model configuration
# ============================================================

BACKBONE = "densenet121"

NUM_CLASSES = 2


# ============================================================
# Image / DataLoader configuration
# ============================================================

IMAGE_SIZE = 128

BATCH_SIZE = 32

NUM_WORKERS = 0

PIN_MEMORY = True


# ============================================================
# Optimizer / training configuration
# ============================================================

LEARNING_RATE = 1e-4

WEIGHT_DECAY = 0.0

EPOCHS = 3

EARLY_STOPPING_PATIENCE = 2
```

---

## 9. Important Configuration Principle

The configuration file centralizes parameters that are likely to be reused across experiments.

The current configuration includes:

```text
BACKBONE
NUM_CLASSES
IMAGE_SIZE
BATCH_SIZE
NUM_WORKERS
PIN_MEMORY
LEARNING_RATE
WEIGHT_DECAY
EPOCHS
EARLY_STOPPING_PATIENCE
RANDOM_SEED
```

This reduces the possibility that one notebook accidentally uses a different setting from another notebook.

However, configuration values that are genuinely experiment-specific should eventually be recorded by the corresponding experiment.

For example:

```text
Phase 11
    label fraction = 5%

Phase 12
    label fraction = 10%

Phase 13
    Semi-SL method = selected method
```

Those values should not be hidden inside unrelated infrastructure code.

---

# 10. Changing the Backbone in the Future

The current model configuration is:

```python
BACKBONE = "densenet121"
```

The architecture was deliberately designed around a model factory.

The important point is that downstream notebooks should not contain code such as:

```python
model = densenet121(...)
```

throughout the experiment.

Instead, they should request:

```python
model = create_model(
    backbone=BACKBONE,
    num_classes=NUM_CLASSES,
)
```

This means that the experiment code depends on the interface:

```text
create_model(...)
```

rather than directly depending on DenseNet-121.

---

## 11. Current `models.py`

File:

```text
src/cervical_ssl/models.py
```

Current implementation:

```python
import torch.nn as nn

from torchvision.models import (
    densenet121,
    DenseNet121_Weights,
)


def create_model(
    backbone: str,
    num_classes: int = 2,
):
    """
    Create a classification model for the requested backbone.

    Currently supported:
        - densenet121
    """

    if backbone == "densenet121":

        model = densenet121(
            weights=DenseNet121_Weights.DEFAULT
        )

        in_features = model.classifier.in_features

        model.classifier = nn.Linear(
            in_features,
            num_classes
        )

        return model

    raise ValueError(
        f"Unsupported backbone: {backbone}"
    )
```

---

# 12. How to Add Another Backbone

If a future experiment requires another backbone, the correct location to modify first is:

```text
src/cervical_ssl/models.py
```

For example, if ResNet-18 becomes necessary, the model factory should be expanded.

The pattern should remain:

```python
if backbone == "densenet121":
    ...
    return model

if backbone == "resnet18":
    ...
    return model
```

The experiment notebook should then be able to request:

```python
BACKBONE = "resnet18"
```

without rewriting the complete training loop.

However, adding a new model is **not only a `models.py` change**.

The following components must be checked:

```text
models.py
    ↓
input transform
    ↓
dataset/DataLoader compatibility
    ↓
GPU memory
    ↓
forward pass
    ↓
training
    ↓
evaluation
```

This is particularly important for Transformer architectures.

---

# 13. Backbone-Specific Input Sizes

The stored cell crops remain:

```text
128 × 128
```

The stored data should **not** be regenerated simply because a future backbone expects another input resolution.

Instead, the transform layer handles model-specific input requirements.

This was demonstrated during Stage 09B:

```text
Stored crop:
128 × 128

DenseNet-121:
128 × 128

ViT-B/16:
224 × 224
```

The ViT-B/16 TorchVision implementation required 224×224 input.

Therefore the correct architecture is:

```text
stored 128×128 crop
        ↓
backbone-specific transform
        ↓
required model input
```

rather than:

```text
stored crop
        ↓
permanently resize dataset
```

This preserves a single standardized preprocessing dataset.

---

# 14. `transforms.py`

File:

```text
src/cervical_ssl/transforms.py
```

Current implementation:

```python
import torchvision.transforms as transforms


_BACKBONE_CONFIG = {
    "densenet121": {
        "input_size": 128,
        "mean": [0.485, 0.456, 0.406],
        "std": [0.229, 0.224, 0.225],
    },
}


def _get_backbone_config(backbone: str):

    if backbone not in _BACKBONE_CONFIG:
        raise ValueError(
            f"Unsupported backbone: {backbone}"
        )

    return _BACKBONE_CONFIG[backbone]


def get_train_transform(backbone: str):

    config = _get_backbone_config(backbone)

    return transforms.Compose([
        transforms.Resize(
            (config["input_size"], config["input_size"])
        ),

        transforms.RandomHorizontalFlip(
            p=0.5
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=config["mean"],
            std=config["std"]
        ),
    ])


def get_val_transform(backbone: str):

    config = _get_backbone_config(backbone)

    return transforms.Compose([
        transforms.Resize(
            (config["input_size"], config["input_size"])
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=config["mean"],
            std=config["std"]
        ),
    ])
```

---

# 15. Adding a New Backbone to the Transform System

If a new backbone requires a different input size, add its configuration to:

```python
_BACKBONE_CONFIG
```

For example:

```python
_BACKBONE_CONFIG = {
    "densenet121": {
        "input_size": 128,
        "mean": [0.485, 0.456, 0.406],
        "std": [0.229, 0.224, 0.225],
    },

    "some_future_backbone": {
        "input_size": 224,
        "mean": [...],
        "std": [...],
    },
}
```

The important design rule is:

```text
backbone-specific preprocessing
        belongs in transforms.py
```

not scattered through individual notebooks.

---

# 16. Data Pipeline

The data pipeline is:

```text
manifest
   ↓
CervicalDataset
   ↓
transform
   ↓
tensor
   ↓
DataLoader
   ↓
training/evaluation
```

The dataset implementation is shared between CRIC and RIVA.

---

# 17. `datasets.py`

File:

```text
src/cervical_ssl/datasets.py
```

Current implementation:

```python
from pathlib import Path

import pandas as pd
import torch

from PIL import Image

from torch.utils.data import (
    Dataset,
    DataLoader,
)


class CervicalDataset(Dataset):
    """
    Dataset for standardized cervical cytology cell crops.
    """

    def __init__(
        self,
        manifest,
        transform=None,
        project_root=None,
    ):
        """
        Parameters
        ----------
        manifest : str, Path, or pandas.DataFrame
            CSV path or already-loaded dataframe.

        transform : torchvision transform, optional
            Transform applied to each image.

        project_root : str or Path, optional
            Project root used to resolve relative crop paths.
        """

        if isinstance(
            manifest,
            (str, Path)
        ):

            self.data = pd.read_csv(
                manifest
            )

        elif isinstance(
            manifest,
            pd.DataFrame
        ):

            self.data = (
                manifest
                .reset_index(drop=True)
                .copy()
            )

        else:

            raise TypeError(
                "manifest must be a CSV path, "
                "Path, or pandas DataFrame"
            )

        required_columns = {
            "crop_path",
            "binary_label",
        }

        missing_columns = (
            required_columns
            - set(self.data.columns)
        )

        if missing_columns:

            raise ValueError(
                f"Manifest is missing required "
                f"columns: {missing_columns}"
            )

        self.transform = transform

        if project_root is None:
            project_root = Path.cwd()

        self.project_root = Path(
            project_root
        )

    def __len__(self):

        return len(self.data)

    def __getitem__(self, index):

        row = self.data.iloc[index]

        image_path = Path(
            row["crop_path"]
        )

        if not image_path.is_absolute():

            image_path = (
                self.project_root
                / image_path
            )

        image = Image.open(
            image_path
        ).convert("RGB")

        label = int(
            row["binary_label"]
        )

        if self.transform is not None:

            image = self.transform(
                image
            )

        return (
            image,
            torch.tensor(
                label,
                dtype=torch.long
            )
        )


def create_dataloader(
    dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0,
    pin_memory=True,
):
    """
    Create a DataLoader for a cervical
    cytology dataset.
    """

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
```

---

# 18. Important Dataset Path Lesson

During Stage 10 development, a path-resolution problem occurred.

Some manifest paths were relative.

If they are interpreted relative to the notebook's current working directory, the program can look in the wrong location.

The dataset therefore accepts:

```python
project_root
```

and resolves relative crop paths using:

```python
if not image_path.is_absolute():

    image_path = (
        self.project_root
        / image_path
    )
```

This should not be removed casually.

If a future dataset produces another path-related error, check this module first.

---

# 19. DataLoader Configuration

The current configuration is:

```python
BATCH_SIZE = 32
NUM_WORKERS = 0
PIN_MEMORY = True
```

The DataLoader is created through:

```python
create_dataloader(...)
```

rather than repeatedly constructing DataLoaders manually throughout the project.

This makes future changes easier.

For example:

```text
GPU memory issue
      ↓
reduce batch size

CPU/DataLoader bottleneck
      ↓
consider changing NUM_WORKERS
```

These changes should be made through configuration rather than scattered notebook edits.

---

# 20. Why `NUM_WORKERS = 0`

The current value is:

```python
NUM_WORKERS = 0
```

This provides a simple and stable Windows-compatible baseline.

It avoids introducing multiprocessing-related notebook issues while the training pipeline is being established.

If later experiments demonstrate a DataLoader bottleneck, this can be increased and benchmarked.

It should not be changed merely for the sake of optimization.

---

# 21. Training Architecture

The training system has three layers:

```text
train_one_epoch()
        ↓
train_model()
        ↓
experiment notebook
```

Validation follows:

```text
validate_one_epoch()
        ↓
train_model()
```

This keeps the actual optimization logic separate from experiment orchestration.

---

# 22. `training.py`

The current implementation contains:

```text
train_one_epoch()
validate_one_epoch()
train_model()
```

The core training functions are:

```python
def train_one_epoch(
    model,
    dataloader,
    criterion,
    optimizer,
    device,
):
    ...
```

and:

```python
def validate_one_epoch(
    model,
    dataloader,
    criterion,
    device,
):
    ...
```

The multi-epoch wrapper is:

```python
def train_model(
    model,
    train_loader,
    val_loader,
    criterion,
    optimizer,
    device,
    epochs,
    checkpoint_path=None,
    early_stopping_patience=None,
):
    ...
```

---

# 23. Training History

Every epoch generates a record containing:

```text
epoch
train_loss
train_accuracy
val_loss
val_accuracy
train_time
val_time
```

Example:

```python
{
    "epoch": 1,
    "train_loss": 0.57,
    "train_accuracy": 0.70,
    "val_loss": 0.37,
    "val_accuracy": 0.87,
    "train_time": 0.77,
    "val_time": 0.14,
}
```

This history is returned as:

```python
result["history"]
```

This becomes important for later result tables and training curves.

---

# 24. Best-Model Selection

The current infrastructure selects the best model using:

```text
validation loss
```

The initial value is:

```python
best_val_loss = float("inf")
```

After each epoch:

```python
if val_result["loss"] < best_val_loss:
```

the current model is considered the best model.

The checkpoint is then saved.

This prevents the final epoch from automatically being treated as the best model.

---

# 25. Early Stopping

The infrastructure also supports:

```python
early_stopping_patience
```

The logic is:

```text
validation improves
       ↓
save model
reset patience

validation does not improve
       ↓
increase patience counter

patience reaches threshold
       ↓
stop training
```

Current configuration:

```python
EARLY_STOPPING_PATIENCE = 2
```

The actual final experimental setting may be adjusted later if the research protocol requires it, but it must be documented and kept identical between comparable experiments.

---

# 26. Checkpointing

File:

```text
src/cervical_ssl/checkpoints.py
```

Current implementation:

```python
from pathlib import Path

import torch


def save_checkpoint(
    model,
    optimizer,
    epoch,
    metrics,
    path,
    scheduler=None,
):
    """
    Save a training checkpoint.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    checkpoint = {
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "metrics": metrics,
    }

    if scheduler is not None:

        checkpoint[
            "scheduler_state_dict"
        ] = scheduler.state_dict()

    torch.save(
        checkpoint,
        path,
    )


def load_checkpoint(
    model,
    optimizer,
    path,
    scheduler=None,
    device="cpu",
):
    """
    Load a training checkpoint.
    """

    path = Path(path)

    checkpoint = torch.load(
        path,
        map_location=device,
        weights_only=False,
    )

    model.load_state_dict(
        checkpoint[
            "model_state_dict"
        ]
    )

    optimizer.load_state_dict(
        checkpoint[
            "optimizer_state_dict"
        ]
    )

    if (
        scheduler is not None
        and "scheduler_state_dict"
        in checkpoint
    ):

        scheduler.load_state_dict(
            checkpoint[
                "scheduler_state_dict"
            ]
        )

    return checkpoint
```

---

# 27. Important PyTorch 2.11 Checkpoint Lesson

During Stage 10 testing, checkpoint loading initially failed because of the changed/default behavior of:

```python
torch.load()
```

with the installed PyTorch version.

The working implementation explicitly uses:

```python
weights_only=False
```

Therefore, if checkpoint loading breaks after a future PyTorch upgrade, this function should be checked first.

Do not randomly modify checkpoint-loading code in individual notebooks.

The centralized function is:

```text
src/cervical_ssl/checkpoints.py
```

---

# 28. Checkpoint Contents

Each checkpoint stores:

```text
epoch
model_state_dict
optimizer_state_dict
metrics
```

and optionally:

```text
scheduler_state_dict
```

This provides enough information to restore the training state for supported workflows.

---

# 29. Evaluation

File:

```text
src/cervical_ssl/evaluation.py
```

The evaluation system calculates the metrics specified by the research design:

```text
Accuracy
Precision
Recall / Sensitivity
Specificity
Macro-F1
AUROC
```

The function is:

```python
evaluate_model(
    model,
    dataloader,
    device,
)
```

---

# 30. Binary Evaluation Convention

The evaluation function treats:

```text
0 = Normal / non-pathological
1 = Abnormal / pathological
```

The positive-class probability is therefore:

```python
probabilities[:, 1]
```

This is used for AUROC.

The confusion matrix is explicitly created using:

```python
labels=[0, 1]
```

and produces:

```text
TN
FP
FN
TP
```

Specificity is calculated as:

```text
TN / (TN + FP)
```

This convention must remain consistent across all later experiments.

---

# 31. Evaluation Output

The evaluation function returns:

```python
{
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "specificity": specificity,
    "macro_f1": macro_f1,
    "auroc": auroc,
}
```

This common output format is important for later experiment tables.

For example:

```text
Phase 11
        ↓
evaluation dictionary

Phase 12
        ↓
same dictionary structure

Phase 13
        ↓
same dictionary structure

Phase 15
        ↓
same dictionary structure
```

This makes downstream result aggregation easier.

---

# 32. AUROC Requirement

AUROC requires both classes to be present in the evaluation target.

The implementation therefore checks:

```python
if len(np.unique(y_true)) == 2:
```

If only one class is present:

```python
auroc = float("nan")
```

This avoids producing a misleading AUROC.

---

# 33. Stage 10 Testing Strategy

Stage 10 was validated incrementally rather than immediately launching a full research experiment.

The following components were tested:

```text
1. Environment / GPU
2. Model factory
3. Transform factory
4. Dataset
5. DataLoader
6. Training loop
7. Evaluation
8. Checkpoint save/load
9. Training history
10. Best checkpoint / early stopping
11. Configuration
12. End-to-end integration
```

This allowed errors to be isolated at the correct layer.

---

# 34. GPU Verification

The working environment was verified as:

```text
Python: 3.14.6
PyTorch: 2.11.0+cu128
Torchvision: 0.26.0+cu128
CUDA available: True
GPU: NVIDIA GeForce RTX 4050 Laptop GPU
GPU memory: approximately 6 GB
```

The GPU tensor test passed.

Therefore, no additional PyTorch/CUDA installation was required for Stage 10.

---

# 35. Model Factory Verification

DenseNet-121 successfully initialized on the GPU.

The classifier was:

```text
Linear(
    in_features=1024,
    out_features=2,
    bias=True
)
```

This confirms that the pretrained DenseNet-121 backbone was successfully converted to the project's binary classification task.

---

# 36. Transform Verification

DenseNet-121 training transformation:

```text
Resize → 128×128
RandomHorizontalFlip(p=0.5)
ToTensor
ImageNet normalization
```

Validation transformation:

```text
Resize → 128×128
ToTensor
ImageNet normalization
```

A real CRIC crop was successfully transformed to:

```text
torch.Size([3, 128, 128])
float32
```

---

# 37. Dataset Verification

The CRIC standardized manifest contained:

```text
11,534 learning units
```

A real dataset sample successfully produced:

```text
Image:
[3, 128, 128]

dtype:
torch.float32

Label:
torch.int64
```

This confirmed that:

```text
manifest
→ image path
→ image loading
→ transformation
→ binary label
```

worked correctly.

---

# 38. DataLoader Verification

The DataLoader test successfully produced:

```text
Dataset size: 11534
Batch size: 32
Image batch shape: [32, 3, 128, 128]
Label batch shape: [32]
Image dtype: float32
Label dtype: int64
```

This confirmed that batches could be passed to the model.

---

# 39. Training Loop Verification

The training loop was tested using only a 64-sample subset.

Example output:

```text
Training result:
loss: 0.8621
accuracy: 0.3750

Validation result:
loss: 0.4589
accuracy: 0.8281
```

These numbers are **not research results**.

They exist only to demonstrate that:

```text
forward pass
→ loss
→ backward pass
→ optimizer step
```

works.

---

# 40. Evaluation Verification

The evaluation function was also tested on the infrastructure subset.

It successfully produced:

```text
accuracy
precision
recall
specificity
macro_f1
auroc
```

Again, these values are not research results.

They are functional verification outputs.

They must not be included in the final research comparison tables as experimental results.

---

# 41. Checkpoint Verification

A checkpoint was successfully written to:

```text
data/checkpoints/phase10_test_checkpoint.pt
```

and successfully loaded.

The checkpoint contained:

```text
Epoch
Metrics
Model state
Optimizer state
```

This confirms that checkpoint persistence is operational.

---

# 42. Training History Verification

A 2-epoch test successfully recorded:

```text
Number of epochs recorded: 2
```

Each record contained:

```text
epoch
train_loss
train_accuracy
val_loss
val_accuracy
train_time
val_time
```

This confirms that later experiments can produce structured epoch-level histories.

---

# 43. Best Checkpoint Verification

A 3-epoch test successfully saved the best checkpoint after each improvement.

Example:

```text
Epoch 1
→ Best checkpoint saved

Epoch 2
→ Best checkpoint saved

Epoch 3
→ Best checkpoint saved
```

The reported best epoch was:

```text
Best epoch: 3
```

This confirms that best-model tracking is operational.

---

# 44. End-to-End Verification

The final infrastructure test connected:

```text
Configuration
        ↓
CRIC split
        ↓
Transform
        ↓
CervicalDataset
        ↓
DataLoader
        ↓
DenseNet-121
        ↓
CrossEntropyLoss
        ↓
AdamW
        ↓
Training
        ↓
Best checkpoint
        ↓
Evaluation
```

The test used:

```text
64 samples
2 epochs
batch size 32
DenseNet-121
```

The checkpoint was successfully created.

Therefore, the infrastructure passed its end-to-end execution test.

---

# 45. Important Interpretation of End-to-End Metrics

The final infrastructure test produced metrics such as:

```text
accuracy: 0.562500
precision: 0.034483
recall: 1.000000
specificity: 0.555556
macro_f1: 0.390476
auroc: 0.984127
```

These values should **not** be interpreted as model performance.

The test deliberately used:

```text
64 samples
2 training epochs
same small subset for train/validation
```

Its purpose was only:

```text
Does the complete software pipeline execute correctly?
```

Therefore:

```text
Stage 10 metrics ≠ research results
```

---

# 46. Why the Actual Research Experiments Start in Stage 11

Stage 10 intentionally stops before the 5% baseline.

This separation is important.

Stage 10 answers:

> Can the training infrastructure reliably execute the intended experiment?

Stage 11 answers:

> How well does supervised learning perform with only 5% labeled training data?

Therefore, the first genuine research performance results begin in:

```text
Stage 11
```

---

# 47. How Future Phase Errors Should Be Debugged

The modular structure gives a defined debugging path.

If a **model creation** error occurs:

```text
Check:
src/cervical_ssl/models.py
```

If an **input-size/transform** error occurs:

```text
Check:
src/cervical_ssl/transforms.py
```

If an **image path or label** error occurs:

```text
Check:
src/cervical_ssl/datasets.py
```

If a **batch/DataLoader** error occurs:

```text
Check:
src/cervical_ssl/datasets.py
```

If a **loss/backpropagation/training** error occurs:

```text
Check:
src/cervical_ssl/training.py
```

If an **evaluation metric** error occurs:

```text
Check:
src/cervical_ssl/evaluation.py
```

If a **checkpoint save/load** error occurs:

```text
Check:
src/cervical_ssl/checkpoints.py
```

If a **global parameter** is wrong:

```text
Check:
src/cervical_ssl/config.py
```

If a genuinely reusable helper is missing:

```text
Consider:
src/cervical_ssl/utils.py
```

---

# 48. Rule for Fixing Future Errors

Do not immediately patch the current notebook when the problem belongs to a reusable module.

For example, if every future experiment has:

```text
model input size mismatch
```

do not add a one-off:

```python
images = resize(images)
```

inside Phase 13.

Instead, determine whether the correct fix belongs in:

```text
transforms.py
```

Likewise, if every experiment needs the same checkpoint-loading correction, fix:

```text
checkpoints.py
```

rather than duplicating the correction in each notebook.

This preserves consistency across the experiment matrix.

---

# 49. Rule for Modifying `.py` Files

During development, when a reusable module needs to change, the safest workflow is:

```text
1. Identify the module.
2. Replace the complete file with the corrected version.
3. Save it.
4. Reload the module if the notebook kernel is still running.
5. Run its verification cell.
```

For example:

```python
import importlib
import src.cervical_ssl.training as training_module

importlib.reload(training_module)
```

For a clean final notebook execution, the preferred approach is:

```text
Restart kernel
→ Run All
```

This guarantees that the notebook is executing the current saved versions of the source modules.

---

# 50. Rule for Adding New Backbones

When adding a future backbone, verify these components in order:

```text
1. models.py
        ↓
2. transforms.py
        ↓
3. forward-pass compatibility
        ↓
4. GPU memory
        ↓
5. DataLoader batch compatibility
        ↓
6. short training test
        ↓
7. evaluation test
```

Do not select a new backbone based solely on whether it imports successfully.

The Stage 09B pilot demonstrated why.

ViT-B/16 imported successfully and passed a 224×224 forward pass, but its standard TorchVision implementation failed with the project's stored 128×128 input until a backbone-specific transform was introduced.

---

# 51. New Backbone Checklist

For any future backbone:

```text
[ ] Add import
[ ] Add model creation logic
[ ] Replace classification head
[ ] Add input configuration
[ ] Verify required image size
[ ] Verify normalization
[ ] Test one real crop
[ ] Test one batch
[ ] Test GPU forward pass
[ ] Test short training
[ ] Test evaluation
[ ] Compare practical runtime
[ ] Record configuration
```

Only after those checks should the backbone be used in a research experiment.

---

# 52. Do Not Modify Stored Crops for a Backbone

The standardized crops are:

```text
CRIC:
128×128

RIVA:
128×128
```

These should remain stable.

If a future model requires:

```text
224×224
```

or another resolution, modify:

```text
src/cervical_ssl/transforms.py
```

rather than regenerating all stored crops.

This ensures that the underlying preprocessing dataset remains fixed across model comparisons.

---

# 53. Fair Comparison Requirement

For the supervised versus Semi-SL comparison, the model architecture should remain the same.

Conceptually:

```text
Supervised:
DenseNet-121
        +
5% labeled data

Semi-SL:
DenseNet-121
        +
same 5% labeled data
        +
remaining unlabeled source data
```

The infrastructure supports this because model creation is centralized.

The Semi-SL implementation should therefore not silently introduce a different backbone unless that is explicitly part of a separate experiment.

---

# 54. Target-Dataset Protection

Stage 10 provides generic training infrastructure, but later experiments must enforce the research protocol.

For cross-dataset evaluation:

```text
Source dataset
    ↓
training
    ↓
validation
    ↓
model selection

Target dataset
    ↓
ONLY final evaluation
```

The target dataset must not be used for:

```text
training
validation
hyperparameter tuning
threshold tuning
early stopping
model selection
normalization statistics
```

The training infrastructure itself should therefore receive only the source training and source validation loaders during source training.

---

# 55. Source and Target Evaluation

The reusable evaluation function can be applied to either dataset.

For example:

```python
source_metrics = evaluate_model(
    model=model,
    dataloader=source_test_loader,
    device=DEVICE,
)

target_metrics = evaluate_model(
    model=model,
    dataloader=target_test_loader,
    device=DEVICE,
)
```

The important distinction is not the evaluation function itself.

The important distinction is **when and why each loader is used**.

The target loader must remain completely unseen during model development.

---

# 56. Label Fraction Handling

The training infrastructure does not hard-code the 5% or 10% label fraction.

This is intentional.

Those belong to experiment-level logic.

Later:

```text
Phase 11:
5% supervised baseline

Phase 12:
10% supervised baseline

Phase 13:
Semi-SL implementation

Phase 16:
10% core experiments
```

The infrastructure should support all of these without rewriting the training engine.

---

# 57. Reproducibility Requirements

Every genuine experiment should eventually record:

```text
random seed
dataset
split definition
label fraction
labeled sample count
unlabeled sample count
backbone
input size
batch size
optimizer
learning rate
weight decay
number of epochs
early stopping setting
checkpoint
validation-selection criterion
evaluation metrics
```

Stage 10 provides the underlying configuration and checkpoint mechanisms required to support this.

---

# 58. Random Seed

Current seed:

```python
RANDOM_SEED = 42
```

The Stage 10 notebook initializes:

```python
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
```

and when CUDA is available:

```python
torch.cuda.manual_seed(RANDOM_SEED)
torch.cuda.manual_seed_all(RANDOM_SEED)
```

The seed should be explicitly recorded for every core experiment.

---

# 59. Experiment-Specific Seeds

If later experiments require multiple seeds, they should not silently overwrite the meaning of the original Stage 10 configuration.

Instead, experiment configuration should explicitly record something like:

```text
experiment_seed = 42
```

and if multiple seeds are used:

```text
42
43
44
...
```

The exact multi-seed design should be defined at the appropriate experimental stage rather than introduced prematurely in Stage 10.

---

# 60. Optimizer

The infrastructure test uses:

```python
AdamW(
    model.parameters(),
    lr=1e-4,
    weight_decay=0.0,
)
```

The Stage 10 infrastructure establishes the ability to configure these values.

The final research hyperparameters must be explicitly recorded in the corresponding experiment documentation.

Stage 10 should not be interpreted as claiming that:

```text
AdamW + 1e-4 + weight_decay=0
```

is the scientifically optimal configuration.

It is the currently established training configuration for infrastructure development.

---

# 61. Loss Function

The binary classification model currently uses:

```python
nn.CrossEntropyLoss()
```

with:

```text
class 0 = Normal
class 1 = Abnormal
```

This is compatible with the two-logit model output:

```text
[logit_normal, logit_abnormal]
```

and the evaluation function obtains the abnormal probability through:

```python
softmax(outputs, dim=1)[:, 1]
```

---

# 62. Checkpoint Naming

Stage 10 test checkpoints include names such as:

```text
phase10_test_checkpoint.pt
phase10_best_model_test.pt
phase10_end_to_end_test.pt
```

These are infrastructure-test artifacts.

Future research experiments should use experiment-specific names that identify the actual experiment.

For example:

```text
phase11_cric_supervised_5pct_best.pt
```

or a structured experiment identifier.

The exact naming convention should be fixed before the large experiment matrix is executed.

---

# 63. Results Directory

The project uses:

```text
data/results/
```

for experiment outputs.

Backbone pilot results from Stage 09B were stored under:

```text
data/results/phase9b/
```

The same organizational principle should continue.

For example:

```text
data/results/phase11/
data/results/phase12/
data/results/phase13/
```

This prevents research results from becoming mixed with temporary infrastructure-test outputs.

---

# 64. Checkpoint Directory

Model checkpoints are stored under:

```text
data/checkpoints/
```

Infrastructure tests may leave temporary files there.

Before final packaging, temporary Stage 10 test artifacts should be distinguished from genuine research checkpoints.

---

# 65. Notebook Design

The project intentionally uses simple notebook names:

```text
phase10.ipynb
phase11.ipynb
phase12.ipynb
phase13.ipynb
...
```

The detailed meaning of each phase belongs in:

```text
documentation/
```

rather than being encoded into increasingly long notebook filenames.

This keeps the repository easier to navigate.

---

# 66. Notebook Responsibility

A downstream notebook should primarily contain:

```text
1. Load configuration
2. Load fixed data/splits
3. Construct experiment-specific subsets
4. Construct DataLoaders
5. Construct model
6. Construct optimizer/loss
7. Call reusable training functions
8. Evaluate
9. Save experiment outputs
10. Print concise experiment summary
```

It should not duplicate the entire training engine.

---

# 67. Phase 10 Notebook

The Phase 10 notebook is:

```text
notebooks/phase10.ipynb
```

It was used to verify the infrastructure incrementally.

Its purpose is therefore different from future research notebooks.

Future notebooks should not import or execute:

```text
phase10.ipynb
```

as a dependency.

They should import reusable Python modules:

```python
from src.cervical_ssl.models import create_model
from src.cervical_ssl.datasets import CervicalDataset
from src.cervical_ssl.training import train_model
from src.cervical_ssl.evaluation import evaluate_model
```

This is the correct dependency direction.

---

# 68. Correct Dependency Direction

The intended architecture is:

```text
                    ┌──────────────┐
                    │   configs    │
                    └──────┬───────┘
                           │
                           ↓
┌──────────────┐    ┌──────────────┐
│ phase11.ipynb│───→│ src modules  │
└──────────────┘    └──────────────┘
                           │
                           ↓
                    data / results
```

Not:

```text
phase11.ipynb
      ↓
phase10.ipynb
      ↓
phase9b.ipynb
```

This avoids turning notebooks into a fragile chain of dependencies.

---

# 69. Why This Matters for Later Phases

The project contains many experiments.

If every phase directly depends on the previous notebook, then a small change in an early notebook could alter later experiments unexpectedly.

With reusable modules:

```text
Phase 11 ─┐
Phase 12 ─┤
Phase 13 ─┤
Phase 15 ─┤
Phase 16 ─┤──→ same controlled infrastructure
Phase 17 ─┤
Phase 18 ─┤
Phase 19 ─┘
```

This is much safer for a research project.

---

# 70. What Stage 10 Does Not Decide

Stage 10 does not permanently decide:

```text
final learning rate
final weight decay
final number of epochs
final Semi-SL algorithm
final augmentation policy
final confidence threshold
final EMA configuration
final pseudo-label threshold
final ablation matrix
final multi-seed strategy
```

Those decisions belong to the appropriate later experimental stages.

Stage 10 provides the machinery required to implement them.

---

# 71. Semi-Supervised Learning Extension

The Stage 10 infrastructure was intentionally designed so that Semi-SL can later be added without replacing the basic model infrastructure.

The eventual architecture can conceptually become:

```text
labeled loader
      ↓
supervised loss
      ↓
model
      ↑
      │
unlabeled loader
      ↓
consistency / pseudo-label mechanism
      ↓
unsupervised loss
```

The exact algorithm is intentionally not fixed in Stage 10.

The model factory, transforms, dataset, DataLoader, checkpointing, and evaluation components remain reusable.

---

# 72. Future Semi-SL Dataset Requirement

The existing:

```python
CervicalDataset
```

returns:

```python
image, label
```

This is sufficient for supervised training.

A Semi-SL implementation may eventually require additional information, such as:

```text
weakly augmented image
strongly augmented image
optional label
sample identifier
```

If that becomes necessary, the correct place to extend the data interface is:

```text
src/cervical_ssl/datasets.py
```

rather than adding ad-hoc tuple construction throughout Phase 13.

The existing supervised dataset behavior should remain available so that the supervised baseline remains unchanged.

---

# 73. Future Scheduler Support

The checkpoint implementation already accepts:

```python
scheduler=None
```

and can save/load:

```python
scheduler_state_dict
```

This means a future experiment can introduce a learning-rate scheduler without redesigning the checkpoint format.

For example:

```python
save_checkpoint(
    model=model,
    optimizer=optimizer,
    epoch=epoch,
    metrics=metrics,
    path=checkpoint_path,
    scheduler=scheduler,
)
```

The scheduler itself should only be introduced when justified by the experimental protocol.

---

# 74. Future Resume Training

Because checkpoints store:

```text
model state
optimizer state
epoch
metrics
```

future training can be resumed from a saved checkpoint.

The general pattern is:

```python
checkpoint = load_checkpoint(
    model=model,
    optimizer=optimizer,
    path=checkpoint_path,
    device=DEVICE,
)

start_epoch = checkpoint["epoch"] + 1
```

If a scheduler is used, it should also be passed to `load_checkpoint()`.

---

# 75. Important Distinction: Resume vs Best-Model Evaluation

These are different operations.

```text
Resume training
    ↓
continue optimization

Best-model selection
    ↓
select checkpoint associated with
best validation performance
```

A final research experiment should evaluate the model corresponding to the documented model-selection criterion.

It should not automatically evaluate whatever model happens to remain in memory after the final epoch.

---

# 76. Model Selection Criterion

Current Stage 10 infrastructure uses:

```text
validation loss
```

as the best-checkpoint criterion.

This is important because later experiments should use a consistent selection rule.

If the research protocol later decides that another criterion should be used, the change must be documented and applied consistently to all comparable experiments.

---

# 77. No Target-Domain Model Selection

Even though the evaluation function can calculate metrics on any dataset, target-domain metrics must not be used for model selection in the cross-dataset experiments.

Incorrect:

```text
train on CRIC
→ compare several checkpoints on RIVA
→ choose best RIVA checkpoint
```

Correct:

```text
train on CRIC
→ select checkpoint using CRIC validation
→ evaluate selected checkpoint on RIVA test
```

This distinction is essential to preserving an independent target-domain evaluation.

---

# 78. GPU Memory Considerations

The RTX 4050 laptop GPU has approximately:

```text
6 GB VRAM
```

DenseNet-121 was selected partly because it provides a practical compromise between predictive performance and training cost.

Stage 09B demonstrated that:

```text
DenseNet-121
```

had nearly the same pilot validation performance as ViT-B/16 while being dramatically faster in the pilot.

The Stage 10 infrastructure therefore uses DenseNet-121 as the practical downstream backbone.

---

# 79. What to Change if CUDA Out-of-Memory Occurs

If a later real experiment produces:

```text
CUDA out of memory
```

the first configuration to inspect is:

```python
BATCH_SIZE = 32
```

The value can be reduced, for example:

```python
BATCH_SIZE = 16
```

or:

```python
BATCH_SIZE = 8
```

The change must be recorded in the experiment configuration.

Do not silently change batch size halfway through a comparison without recording it.

---

# 80. What to Change if Training Is Too Slow

Check:

```text
backbone
batch size
DataLoader workers
input size
augmentation
GPU utilization
```

The first code locations to inspect are:

```text
config.py
transforms.py
datasets.py
models.py
```

Do not prematurely replace DenseNet-121 because of a single slow run.

Stage 09B already established its practical suitability relative to the tested candidate pool.

---

# 81. What to Change if Validation Behaves Strangely

Check:

```text
training.py
```

and verify:

```python
model.train()
```

for training and:

```python
model.eval()
```

for validation.

Also verify:

```python
with torch.no_grad():
```

is used during validation.

Then inspect:

```text
split assignments
label distribution
transforms
```

before modifying the model.

---

# 82. What to Change if Metrics Look Wrong

Check the following in order:

```text
1. binary label mapping
2. y_true
3. y_pred
4. positive class definition
5. confusion matrix
6. probability column used for AUROC
```

The current positive class is:

```text
1 = Abnormal / pathological
```

Therefore:

```python
probabilities[:, 1]
```

must continue to represent the abnormal probability.

---

# 83. What to Change if AUROC Becomes NaN

Check whether the evaluation dataset contains both classes.

Use:

```python
np.unique(y_true)
```

If only one class exists, AUROC cannot be meaningfully calculated.

This should trigger investigation of:

```text
split composition
label mapping
subset selection
```

rather than arbitrary changes to the AUROC function.

---

# 84. Research Dataset Integrity

Stage 10 does not change the fixed splits.

The downstream experiment code must continue using:

```text
CRIC image-level split
RIVA slide-level split
```

because cells from the same parent image/slide must not leak across train/validation/test.

The training infrastructure should consume the split assignments rather than regenerate them.

---

# 85. Do Not Regenerate Splits in Phase 11+

Later notebooks should load:

```text
data/splits/cric_splits.csv
data/splits/riva_splits.csv
```

rather than creating new random train/validation/test partitions.

This preserves the Stage 08 reproducibility freeze.

---

# 86. Do Not Rebuild the Preprocessing Dataset

Later phases should consume:

```text
data/processed/cric_crops/
data/processed/riva_crops/
```

and the corresponding manifests.

They should not silently regenerate crops with different:

```text
crop size
coordinate interpretation
padding behavior
label mapping
```

unless a new, explicitly documented preprocessing experiment is being performed.

---

# 87. Phase 10 Completion Criteria

Stage 10 is considered complete because the following requirements passed:

```text
[✓] GPU available
[✓] Selected backbone initializes
[✓] Binary classification head works
[✓] Backbone-specific transforms work
[✓] Real crop loads correctly
[✓] Dataset returns image + label
[✓] DataLoader produces valid batches
[✓] Training loop works
[✓] Validation loop works
[✓] Training history is recorded
[✓] Evaluation metrics work
[✓] Checkpoint save works
[✓] Checkpoint load works
[✓] Best-model tracking works
[✓] Early stopping infrastructure works
[✓] Configuration works
[✓] End-to-end pipeline works
```

---

# 88. Final Stage 10 Architecture

The resulting architecture is:

```text
                    ┌──────────────────────┐
                    │      config.py       │
                    │                      │
                    │ backbone             │
                    │ batch size           │
                    │ learning rate        │
                    │ seed                 │
                    │ epochs               │
                    └──────────┬───────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │     transforms.py    │
                    │                      │
                    │ train transform      │
                    │ validation transform │
                    └──────────┬───────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │     datasets.py      │
                    │                      │
                    │ CervicalDataset      │
                    │ DataLoader            │
                    └──────────┬───────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │       models.py      │
                    │                      │
                    │ create_model()       │
                    │ DenseNet-121         │
                    └──────────┬───────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │      training.py     │
                    │                      │
                    │ train_one_epoch      │
                    │ validate_one_epoch   │
                    │ train_model           │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ↓                      ↓
          ┌──────────────────┐   ┌──────────────────┐
          │ checkpoints.py   │   │ evaluation.py   │
          │                  │   │                  │
          │ save             │   │ Accuracy         │
          │ load             │   │ Precision        │
          │ resume           │   │ Recall           │
          └──────────────────┘   │ Specificity      │
                                 │ Macro-F1         │
                                 │ AUROC            │
                                 └──────────────────┘
```

---

# 89. Final Design Principle

The most important architectural decision in Stage 10 is:

```text
Experiment logic ≠ training implementation
```

The notebooks decide:

```text
WHAT experiment to run
```

The reusable modules decide:

```text
HOW training is performed
```

Therefore:

```text
Phase 11
5% supervised
       ↓
same infrastructure

Phase 12
10% supervised
       ↓
same infrastructure

Phase 13
Semi-SL
       ↓
same model/data/evaluation infrastructure

Phase 15
Cross-dataset evaluation
       ↓
same evaluation infrastructure

Phase 16+
Core experiment matrix
       ↓
same controlled infrastructure
```

This separation is essential for a credible comparison between supervised and Semi-SL methods.

---

# 90. Stage 10 Final Status

```text
STATUS: COMPLETE

Selected backbone:
DenseNet-121

Training device:
NVIDIA GeForce RTX 4050 Laptop GPU

Input crop:
128 × 128

Classification:
Binary

Class 0:
Normal / non-pathological

Class 1:
Abnormal / pathological

Training framework:
PyTorch

Optimizer:
AdamW

Current infrastructure learning rate:
1e-4

Current infrastructure batch size:
32

Current infrastructure seed:
42

Checkpointing:
Implemented

Best-model selection:
Implemented

Early stopping:
Implemented

Evaluation:
Implemented

End-to-end test:
PASSED
```

---

# 91. Transition to Stage 11

Stage 10 now provides the stable infrastructure required for the first actual baseline experiment.

The next research stage is:

```text
Stage 11 — Supervised 5% Baseline
```

The purpose of Stage 11 is to establish the supervised reference point using:

```text
5% labeled source training data
```

while preserving the fixed train/validation/test split and the selected DenseNet-121 backbone.

The Stage 11 result will become one of the principal reference points against which later Semi-SL experiments are compared.