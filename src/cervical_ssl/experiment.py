from pathlib import Path


def build_experiment_id(
    source_dataset,
    method,
    label_fraction,
    backbone,
    seed,
):
    """
    Build a deterministic experiment identifier.

    Example:
        cric_supervised_5pct_densenet121_seed42
    """

    fraction_text = f"{label_fraction:g}pct"

    return (
        f"{source_dataset}_"
        f"{method}_"
        f"{fraction_text}_"
        f"{backbone}_"
        f"seed{seed}"
    )


def create_experiment_dirs(project_root, experiment_id):
    """
    Create and return the standard directories for one experiment.
    """

    project_root = Path(project_root)

    results_dir = (
        project_root
        / "data"
        / "results"
        / "experiments"
        / experiment_id
    )

    checkpoint_dir = (
        project_root
        / "data"
        / "checkpoints"
        / "experiments"
        / experiment_id
    )

    curves_dir = results_dir / "curves"

    results_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    curves_dir.mkdir(parents=True, exist_ok=True)

    return {
        "results": results_dir,
        "checkpoints": checkpoint_dir,
        "curves": curves_dir,
    }