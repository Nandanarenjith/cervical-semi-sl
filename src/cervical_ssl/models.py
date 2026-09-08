import torch.nn as nn

from torchvision.models import (
    densenet121,
    DenseNet121_Weights,
)


def create_model(backbone: str, num_classes: int = 2):
    """
    Create a classification model for the requested backbone.

    Currently supported:
        - densenet121

    Parameters
    ----------
    backbone : str
        Name of the backbone architecture.
    num_classes : int
        Number of output classes.

    Returns
    -------
    nn.Module
        Configured classification model.
    """

    if backbone == "densenet121":

        model = densenet121(
            weights=DenseNet121_Weights.DEFAULT
        )

        # Replace ImageNet's 1000-class classifier
        # with our binary classification head.
        in_features = model.classifier.in_features

        model.classifier = nn.Linear(
            in_features,
            num_classes
        )

        return model

    raise ValueError(
        f"Unsupported backbone: {backbone}"
    )