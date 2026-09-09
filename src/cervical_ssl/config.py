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

WEIGHT_DECAY = 1e-5

EPOCHS = 3

EARLY_STOPPING_PATIENCE = 2