# TODO: Make it reactive
# TODO: Grab env values
from typing import Any, List

import pymongo
from pymongo import MongoClient
from pymongo.cursor import Cursor

from src.dto.data_pair import DataPair


class MongoConnector:
    _client: MongoClient
    _db: Any
    _collection: Any

    def __init__(self):
        self._client = MongoClient('mongodb://admin:password@localhost:27017/')
        self._db = self._client['stonks']

    def find_by_collection_ordered_asc(self, collection: str) -> Cursor:
        results = self._db[collection].find({}).sort("createdAt", pymongo.ASCENDING)
        return results

    def save_data_pairs(self, collection: str, data_pairs: List[DataPair]):
        result = self._db[collection].insert_many([data_pair.dict() for data_pair in data_pairs])
        print(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
