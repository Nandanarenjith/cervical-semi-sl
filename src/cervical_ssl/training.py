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

    In addition to loss and accuracy, computes
    Macro-F1, sensitivity, and specificity.
    """

    model.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    all_labels = []
    all_predictions = []

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

            all_labels.extend(
                labels.cpu().numpy()
            )

            all_predictions.extend(
                predictions.cpu().numpy()
            )

    epoch_loss = running_loss / total
    epoch_accuracy = correct / total

    # --------------------------------------------------------
    # Classification metrics
    # --------------------------------------------------------

    from sklearn.metrics import (
        f1_score,
        confusion_matrix,
        recall_score,
    )

    macro_f1 = f1_score(
        all_labels,
        all_predictions,
        average="macro",
        zero_division=0,
    )

    sensitivity = recall_score(
        all_labels,
        all_predictions,
        pos_label=1,
        zero_division=0,
    )

    tn, fp, fn, tp = confusion_matrix(
        all_labels,
        all_predictions,
        labels=[0, 1],
    ).ravel()

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else 0.0
    )

    epoch_time = time.time() - start_time

    return {
        "loss": epoch_loss,
        "accuracy": epoch_accuracy,
        "macro_f1": macro_f1,
        "sensitivity": sensitivity,
        "specificity": specificity,
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
    selection_metric="macro_f1",
):
    """
    Train a model for multiple epochs.

    The best model is selected using the requested
    validation metric.

    Supported selection metrics:
        - macro_f1
        - sensitivity
        - specificity
        - accuracy
        - loss

    Default:
        macro_f1

    Returns:
        training history
        best validation metric
        best epoch
    """

    history = []

    best_metric = (
        float("inf")
        if selection_metric == "loss"
        else -float("inf")
    )

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
            "val_macro_f1": val_result["macro_f1"],
            "val_sensitivity": val_result["sensitivity"],
            "val_specificity": val_result["specificity"],
            "train_time": train_result["time"],
            "val_time": val_result["time"],
        }

        history.append(epoch_record)

        print(
            f"Epoch {epoch}/{epochs} | "
            f"Train Loss: {train_result['loss']:.4f} | "
            f"Train Acc: {train_result['accuracy']:.4f} | "
            f"Val Loss: {val_result['loss']:.4f} | "
            f"Val Acc: {val_result['accuracy']:.4f} | "
            f"Val Macro-F1: {val_result['macro_f1']:.4f} | "
            f"Val Sensitivity: {val_result['sensitivity']:.4f} | "
            f"Val Specificity: {val_result['specificity']:.4f}"
        )

        # ----------------------------------------------------
        # Determine current selection value
        # ----------------------------------------------------

        if selection_metric == "macro_f1":
            current_metric = val_result["macro_f1"]

        elif selection_metric == "sensitivity":
            current_metric = val_result["sensitivity"]

        elif selection_metric == "specificity":
            current_metric = val_result["specificity"]

        elif selection_metric == "accuracy":
            current_metric = val_result["accuracy"]

        elif selection_metric == "loss":
            current_metric = val_result["loss"]

        else:
            raise ValueError(
                f"Unsupported selection metric: "
                f"{selection_metric}"
            )

        # ----------------------------------------------------
        # Determine whether this is the best model
        # ----------------------------------------------------

        if selection_metric == "loss":
            improved = current_metric < best_metric
        else:
            improved = current_metric > best_metric

        if improved:

            best_metric = current_metric
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
                    f"(epoch {epoch}, "
                    f"{selection_metric}="
                    f"{current_metric:.4f})"
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
        "best_metric": best_metric,
        "best_epoch": best_epoch,
        "selection_metric": selection_metric,
    }