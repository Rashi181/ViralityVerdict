from copy import deepcopy
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from pymongo.collection import Collection


class ImportRepository(Protocol):
    def create(self, owner_id: str, source: str, media: list[dict], limitations: list[str]) -> dict: ...
    def list_for_owner(self, owner_id: str) -> list[dict]: ...


class InMemoryImportRepository:
    def __init__(self) -> None: self.records: list[dict] = []
    def create(self, owner_id: str, source: str, media: list[dict], limitations: list[str]) -> dict:
        record = {"_id": str(uuid4()), "owner_id": owner_id, "source": source, "media": deepcopy(media), "status": "completed", "limitations": limitations, "created_at": datetime.now(UTC)}
        self.records.append(record); return deepcopy(record)
    def list_for_owner(self, owner_id: str) -> list[dict]: return [deepcopy(item) for item in self.records if item["owner_id"] == owner_id]


class MongoImportRepository:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection; self.collection.create_index([("owner_id", 1), ("created_at", -1)])
    def create(self, owner_id: str, source: str, media: list[dict], limitations: list[str]) -> dict:
        record = {"_id": str(uuid4()), "owner_id": owner_id, "source": source, "media": media, "status": "completed", "limitations": limitations, "created_at": datetime.now(UTC)}
        self.collection.insert_one(record); return record
    def list_for_owner(self, owner_id: str) -> list[dict]: return list(self.collection.find({"owner_id": owner_id}).sort("created_at", -1))
