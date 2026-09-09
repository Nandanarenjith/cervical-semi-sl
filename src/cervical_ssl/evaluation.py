import numpy as np
import torch

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)


def predict_model(
    model,
    dataloader,
    device,
):
    """
    Generate predictions and positive-class probabilities.

    Returns
    -------
    y_true : numpy.ndarray
        Ground-truth binary labels.

    y_pred : numpy.ndarray
        Predicted binary labels.

    y_prob : numpy.ndarray
        Positive-class probabilities.
    """

    model.eval()

    all_labels = []
    all_predictions = []
    all_probabilities = []

    with torch.no_grad():

        for images, labels in dataloader:

            images = images.to(device)

            outputs = model(images)

            probabilities = torch.softmax(
                outputs,
                dim=1,
            )

            predictions = torch.argmax(
                probabilities,
                dim=1,
            )

            all_labels.extend(
                labels.cpu().numpy()
            )

            all_predictions.extend(
                predictions.cpu().numpy()
            )

            all_probabilities.extend(
                probabilities[:, 1]
                .cpu()
                .numpy()
            )

    y_true = np.asarray(
        all_labels,
        dtype=np.int64,
    )

    y_pred = np.asarray(
        all_predictions,
        dtype=np.int64,
    )

    y_prob = np.asarray(
        all_probabilities,
        dtype=np.float32,
    )

    return (
        y_true,
        y_pred,
        y_prob,
    )


def evaluate_model(
    model,
    dataloader,
    device,
):
    """
    Evaluate a binary cervical cytology classifier.

    Returns
    -------
    dict
        Accuracy, precision, recall/sensitivity,
        specificity, macro-F1, and AUROC.
    """

    y_true, y_pred, y_prob = predict_model(
        model=model,
        dataloader=dataloader,
        device=device,
    )

    accuracy = accuracy_score(
        y_true,
        y_pred,
    )

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else 0.0
    )

    macro_f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0,
    )

    if len(np.unique(y_true)) == 2:

        auroc = roc_auc_score(
            y_true,
            y_prob,
        )

    else:

        auroc = float("nan")

    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "specificity": float(specificity),
        "macro_f1": float(macro_f1),
        "auroc": float(auroc),
    }