from copy import deepcopy
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from pymongo.collection import Collection


class TrendRepository(Protocol):
    def create(self, owner_id: str, signals: list[dict]) -> list[dict]: ...
    def list_for_owner(self, owner_id: str) -> list[dict]: ...


class InMemoryTrendRepository:
    def __init__(self) -> None: self.signals: list[dict] = []
    def create(self, owner_id: str, signals: list[dict]) -> list[dict]:
        stored = [{"_id": str(uuid4()), "owner_id": owner_id, **deepcopy(signal), "retrieved_at": datetime.now(UTC)} for signal in signals]
        self.signals.extend(stored)
        return deepcopy(stored)
    def list_for_owner(self, owner_id: str) -> list[dict]:
        return [deepcopy(signal) for signal in self.signals if signal["owner_id"] == owner_id]


class MongoTrendRepository:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
        self.collection.create_index([("owner_id", 1), ("retrieved_at", -1)])
    def create(self, owner_id: str, signals: list[dict]) -> list[dict]:
        stored = [{"_id": str(uuid4()), "owner_id": owner_id, **signal, "retrieved_at": datetime.now(UTC)} for signal in signals]
        self.collection.insert_many(stored)
        return stored
    def list_for_owner(self, owner_id: str) -> list[dict]:
        return list(self.collection.find({"owner_id": owner_id}).sort("retrieved_at", -1))
