import numpy as np
import torch
from pymongo.cursor import Cursor

from src.dto.data_pair import DataPair


class MongoTensorCursor:
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    def next(self):
        document = self._cursor.next()
        data_pair = DataPair(**document)

        feature_tensor = torch.tensor(np.array(data_pair.inputs, dtype=np.float32), dtype=torch.float32)
        expected_tensor = torch.tensor(np.array(data_pair.expected, dtype=np.float32), dtype=torch.float32)

        return feature_tensor, expected_tensor
