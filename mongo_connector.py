# TODO: Make it reactive
from typing import Any

import pymongo
from pymongo import MongoClient
from pymongo.cursor import Cursor


class MongoConnector:
    _client: MongoClient
    _db: Any
    _collection: Any

    def __init__(self, collection_name: str):
        self._client = MongoClient('mongodb://localhost:27017/')
        self._db = self._client['stonks']
        self._collection = self._db[collection_name]

    def find_by_topic_ordered_asc(self, topic: str) -> Cursor:
        query = {"topic": topic}
        results = self._collection.find(query).sort("createdAt", pymongo.ASCENDING)
        return results
