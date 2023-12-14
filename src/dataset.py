import os
from typing import Union, Optional
import pandas as pd

import albumentations as albu
import cv2
from torch.utils.data import Dataset


TRANSFORM_TYPE = Union[albu.BasicTransform, albu.BaseCompose]


class BarCodeDataset(Dataset):
    def __init__(
        self,
        df: pd.DataFrame,
        data_folder: str,
        transforms: Optional[TRANSFORM_TYPE] = None,
    ):
        self.transforms = transforms

        self.crops = []
        self.codes = []
        for i in range(len(df)):
            crop = cv2.imread(os.path.join(data_folder, df['filename'][i]))[..., ::-1]

            self.crops.append(crop)
            self.codes.append(str(df['code'][i]))

    def __getitem__(self, idx):
        text = self.codes[idx]
        image = self.crops[idx]

        data = {
            'image': image,
            'text': text,
            'text_length': len(text),
        }

        if self.transforms:
            data = self.transforms(**data)

        return data['image'], data['text'], data['text_length']

    def __len__(self):
        return len(self.crops)
