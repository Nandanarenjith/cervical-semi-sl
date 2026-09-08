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
    path.parent.mkdir(parents=True, exist_ok=True)

    checkpoint = {
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "metrics": metrics,
    }

    if scheduler is not None:
        checkpoint["scheduler_state_dict"] = scheduler.state_dict()

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
        checkpoint["model_state_dict"]
    )

    optimizer.load_state_dict(
        checkpoint["optimizer_state_dict"]
    )

    if (
        scheduler is not None
        and "scheduler_state_dict" in checkpoint
    ):
        scheduler.load_state_dict(
            checkpoint["scheduler_state_dict"]
        )

    return checkpoint