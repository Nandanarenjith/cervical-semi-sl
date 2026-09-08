import torchvision.transforms as transforms


# ============================================================
# Backbone-specific transform configuration
# ============================================================

_BACKBONE_CONFIG = {
    "densenet121": {
        "input_size": 128,
        "mean": [0.485, 0.456, 0.406],
        "std": [0.229, 0.224, 0.225],
    },
}


# ============================================================
# Internal helper
# ============================================================

def _get_backbone_config(backbone: str):
    """
    Return preprocessing configuration for a backbone.
    """

    if backbone not in _BACKBONE_CONFIG:
        raise ValueError(
            f"Unsupported backbone: {backbone}"
        )

    return _BACKBONE_CONFIG[backbone]


# ============================================================
# Training transforms
# ============================================================

def get_train_transform(backbone: str):
    """
    Create the training transform pipeline for a backbone.

    Training transforms may include data augmentation.
    """

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


# ============================================================
# Validation / Test transforms
# ============================================================

def get_val_transform(backbone: str):
    """
    Create the validation/test transform pipeline.

    No random augmentation is applied here.
    """

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