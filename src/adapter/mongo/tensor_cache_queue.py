from pathlib import Path
from queue import Queue
from threading import Thread, Event
from typing import List

import torch
from pydantic import BaseModel
from pymongo.cursor import Cursor
from torch.utils.data import IterableDataset

from src.adapter.mongo.mongo_tensor_cursor import MongoTensorCursor


class TensorExportDict(BaseModel):
    feature: List[float]
    expected: List[float]


class TensorCacheQueue(IterableDataset):
    def __init__(self, cursor: Cursor):
        self.mapper = MongoTensorCursor(cursor)
        # TODO: Support multiple Queue for multiple training
        self.file_path = Path("../../../output/tmp/tensor_cache.json")
        self.memory_data = Queue()
        self.cache_min_size = 500
        self.clear_cache()

        self.stop_event = Event()
        self.populate_thread = Thread(target=self.__keep_size, daemon=True)

        # Start the populate thread
        self.populate_thread.start()

    def __keep_size(self):
        database_exhausted = False
        self.file_path.touch()
        file_read = None

        while not self.stop_event.is_set():
            if self.memory_data.qsize() < self.cache_min_size:
                if database_exhausted:
                    line = file_read.readline()

                    if not line:
                        file_read.seek(0)
                        self.memory_data.put(None)
                    else:
                        tensor_dict = TensorExportDict.parse_raw(line)
                        self.memory_data.put((torch.tensor(tensor_dict.feature, dtype=torch.float32),
                                              torch.tensor(tensor_dict.expected, dtype=torch.float32)))
                else:
                    try:
                        feature_tensor, expected_tensor = self.mapper.next()
                        self.memory_data.put((feature_tensor, expected_tensor))
                        with open(self.file_path, "a") as f:
                            f.write(TensorExportDict(feature=feature_tensor.tolist(),
                                                     expected=expected_tensor.tolist()).json() + "\n")
                    except StopIteration:
                        self.memory_data.put(None)
                        file_read = open(self.file_path, "r")
                        database_exhausted = True

    def __iter__(self):
        data = self.memory_data.get()
        while data is not None:
            feature, expected = data
            yield feature, expected
            data = self.memory_data.get()

    def __del__(self):
        # Set the stop event to signal the thread to stop
        self.stop_event.set()
        # Wait for the populate thread to finish if it's still running
        if self.populate_thread.is_alive():
            self.populate_thread.join()

    def clear_cache(self):
        if self.file_path.exists():
            self.file_path.unlink()
