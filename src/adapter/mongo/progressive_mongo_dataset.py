from typing import Callable, Mapping, Any, Tuple

import torch
from torch._C._te import Tensor
from torch.utils.data import IterableDataset, DataLoader
from pymongo import MongoClient

from src.adapter.mongo.mongo_connector import MongoConnector
from src.model.model_definition_gen_A0 import ModelDefinitionGenA0
from pymongo.cursor import Cursor


class ProgressiveMongoDataset(IterableDataset):
    def __init__(self, client: MongoConnector, query_function: Callable[[MongoConnector], Cursor],
                 query_count: Callable[[MongoConnector], Cursor],
                 mapper: Callable[[Mapping[str, Any]], Tuple[Tensor, Tensor]]):
        self.client = client
        self.query_function = query_function
        self.query_count = query_count
        self.mapper = mapper

    def __iter__(self):
        cursor = self.query_function(self.client)

        for document in cursor:
            yield self.mapper(document)

    def __len__(self):
        return self.query_count(self.client)
