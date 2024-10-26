import numpy as np
import torch
from pymongo.cursor import Cursor
from torch.utils.data import IterableDataset

from data_pair import DataPair


class MongoNumpyMapper:
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    def next(self):
        document = self._cursor.next()
        data_pair = DataPair(**document)

        inputs_array = np.array(data_pair.inputs, dtype=np.float32)
        expected_array = np.array(data_pair.expected, dtype=np.float32)

        return inputs_array, expected_array


class MongoDataset(IterableDataset):
    def __init__(self, cursor: Cursor):
        self.mapper = MongoNumpyMapper(cursor)

    def __iter__(self):
        while True:
            try:
                features, expected = self.mapper.next()
                feature_tensor = torch.tensor(features, dtype=torch.float32)
                expected_tensor = torch.tensor(expected, dtype=torch.float32)
                yield feature_tensor, expected_tensor
            except StopIteration:
                break
