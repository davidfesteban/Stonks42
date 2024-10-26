import json
from pathlib import Path
from typing import List

import numpy as np
import torch
from pydantic import BaseModel
from pymongo.cursor import Cursor
from torch.utils.data import IterableDataset

from data_pair import DataPair


class MongoNumpyCursorMapper:
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    def next(self):
        document = self._cursor.next()
        data_pair = DataPair(**document)

        inputs_array = np.array(data_pair.inputs, dtype=np.float32)
        expected_array = np.array(data_pair.expected, dtype=np.float32)

        return inputs_array, expected_array


class TensorExportDict(BaseModel):
    feature: List[float]
    expected: List[float]


class MongoDatasetTensorCache(IterableDataset):
    def __init__(self, cursor: Cursor):
        self.mapper = MongoNumpyCursorMapper(cursor)
        self.file_path = Path("tensor_cache.json")
        self.clear_cache()

    def __iter__(self):
        if self.file_path.exists():
            print("Loading data from cache...")
            with open(self.file_path, "r") as f:
                for line in f:
                    tensor_dict = TensorExportDict.parse_raw(line)
                    feature_tensor = torch.tensor(tensor_dict.feature, dtype=torch.float32)
                    expected_tensor = torch.tensor(tensor_dict.expected, dtype=torch.float32)
                    yield feature_tensor, expected_tensor
        else:
            print("Fetching data from MongoDB and caching...")
            self.file_path.touch()
            with open(self.file_path, "a") as f:
                while True:
                    try:
                        features, expected = self.mapper.next()
                        feature_tensor = torch.tensor(features, dtype=torch.float32)
                        expected_tensor = torch.tensor(expected, dtype=torch.float32)

                        f.write(TensorExportDict(feature=feature_tensor.tolist(),
                                                 expected=expected_tensor.tolist()).json() + "\n")
                        # TODO: Batch and manual flush. Write keeps in memory!
                        yield feature_tensor, expected_tensor
                    except StopIteration:
                        print("Stopped Iteration on Mongo Cursor")
                        break

    def clear_cache(self):
        if self.file_path.exists():
            self.file_path.unlink()
