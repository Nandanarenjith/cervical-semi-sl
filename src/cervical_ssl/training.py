import time

import torch

from .checkpoints import save_checkpoint


def train_one_epoch(
    model,
    dataloader,
    criterion,
    optimizer,
    device,
):
    """
    Train the model for one epoch.
    """

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    start_time = time.time()

    for images, labels in dataloader:

        images = images.to(
            device,
            non_blocking=True,
        )

        labels = labels.to(
            device,
            non_blocking=True,
        )

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels,
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item() * images.size(0)
        )

        predictions = outputs.argmax(dim=1)

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_accuracy = correct / total
    epoch_time = time.time() - start_time

    return {
        "loss": epoch_loss,
        "accuracy": epoch_accuracy,
        "time": epoch_time,
    }


def validate_one_epoch(
    model,
    dataloader,
    criterion,
    device,
):
    """
    Evaluate the model for one epoch.
    """

    model.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    start_time = time.time()

    with torch.no_grad():

        for images, labels in dataloader:

            images = images.to(
                device,
                non_blocking=True,
            )

            labels = labels.to(
                device,
                non_blocking=True,
            )

            outputs = model(images)

            loss = criterion(
                outputs,
                labels,
            )

            running_loss += (
                loss.item() * images.size(0)
            )

            predictions = outputs.argmax(dim=1)

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_accuracy = correct / total
    epoch_time = time.time() - start_time

    return {
        "loss": epoch_loss,
        "accuracy": epoch_accuracy,
        "time": epoch_time,
    }


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
    """
    Train a model for multiple epochs.

    The best model is selected using validation loss.

    Returns:
        training history
        best validation loss
        best epoch
    """

    history = []

    best_val_loss = float("inf")
    best_epoch = 0
    patience_counter = 0

    for epoch in range(1, epochs + 1):

        train_result = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
        )

        val_result = validate_one_epoch(
            model=model,
            dataloader=val_loader,
            criterion=criterion,
            device=device,
        )

        epoch_record = {
            "epoch": epoch,
            "train_loss": train_result["loss"],
            "train_accuracy": train_result["accuracy"],
            "val_loss": val_result["loss"],
            "val_accuracy": val_result["accuracy"],
            "train_time": train_result["time"],
            "val_time": val_result["time"],
        }

        history.append(epoch_record)

        print(
            f"Epoch {epoch}/{epochs} | "
            f"Train Loss: {train_result['loss']:.4f} | "
            f"Train Acc: {train_result['accuracy']:.4f} | "
            f"Val Loss: {val_result['loss']:.4f} | "
            f"Val Acc: {val_result['accuracy']:.4f}"
        )

        # ----------------------------------------------------
        # Best model tracking
        # ----------------------------------------------------

        if val_result["loss"] < best_val_loss:

            best_val_loss = val_result["loss"]
            best_epoch = epoch
            patience_counter = 0

            if checkpoint_path is not None:

                save_checkpoint(
                    model=model,
                    optimizer=optimizer,
                    epoch=epoch,
                    metrics=epoch_record,
                    path=checkpoint_path,
                )

                print(
                    f"  → Best checkpoint saved "
                    f"(epoch {epoch})"
                )

        else:

            patience_counter += 1

        # ----------------------------------------------------
        # Early stopping
        # ----------------------------------------------------

        if (
            early_stopping_patience is not None
            and patience_counter >= early_stopping_patience
        ):

            print(
                f"  → Early stopping triggered "
                f"after epoch {epoch}"
            )

            break

    return {
        "history": history,
        "best_val_loss": best_val_loss,
        "best_epoch": best_epoch,
    }