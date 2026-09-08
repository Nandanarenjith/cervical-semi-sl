from pathlib import Path

import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader


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

        if isinstance(manifest, (str, Path)):
            self.data = pd.read_csv(manifest)

        elif isinstance(manifest, pd.DataFrame):
            self.data = manifest.reset_index(drop=True).copy()

        else:
            raise TypeError(
                "manifest must be a CSV path, Path, or pandas DataFrame"
            )

        required_columns = {
            "crop_path",
            "binary_label",
        }

        missing_columns = required_columns - set(self.data.columns)

        if missing_columns:
            raise ValueError(
                f"Manifest is missing required columns: {missing_columns}"
            )

        self.transform = transform

        if project_root is None:
            project_root = Path.cwd()

        self.project_root = Path(project_root)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        row = self.data.iloc[index]

        image_path = Path(row["crop_path"])

        if not image_path.is_absolute():
            image_path = self.project_root / image_path

        image = Image.open(image_path).convert("RGB")

        label = int(row["binary_label"])

        if self.transform is not None:
            image = self.transform(image)

        return image, torch.tensor(label, dtype=torch.long)


def create_dataloader(
    dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0,
    pin_memory=True,
):
    """
    Create a DataLoader for a cervical cytology dataset.
    """

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )