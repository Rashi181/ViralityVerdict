from copy import deepcopy
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from pymongo.collection import Collection


class AudienceRepository(Protocol):
    def create(self, owner_id: str, aggregates: list[dict], limitations: list[str]) -> dict: ...
    def latest_for_owner(self, owner_id: str) -> dict | None: ...
    def save_feedback(self, owner_id: str, note: str) -> dict: ...
    def latest_feedback(self, owner_id: str) -> dict | None: ...


class InMemoryAudienceRepository:
    def __init__(self) -> None:
        self.records: list[dict] = []
        self.feedback: dict[str, dict] = {}

    def create(self, owner_id: str, aggregates: list[dict], limitations: list[str]) -> dict:
        record = {"_id": str(uuid4()), "owner_id": owner_id, "aggregates": deepcopy(aggregates), "limitations": limitations, "created_at": datetime.now(UTC)}
        self.records.append(record)
        return deepcopy(record)

    def latest_for_owner(self, owner_id: str) -> dict | None:
        record = next((item for item in reversed(self.records) if item["owner_id"] == owner_id), None)
        return deepcopy(record) if record else None

    def save_feedback(self, owner_id: str, note: str) -> dict:
        record = {"owner_id": owner_id, "note": note, "updated_at": datetime.now(UTC)}
        self.feedback[owner_id] = record
        return deepcopy(record)

    def latest_feedback(self, owner_id: str) -> dict | None:
        record = self.feedback.get(owner_id)
        return deepcopy(record) if record else None


class MongoAudienceRepository:
    def __init__(self, collection: Collection, feedback_collection: Collection) -> None:
        self.collection = collection
        self.feedback_collection = feedback_collection
        self.collection.create_index([("owner_id", 1), ("created_at", -1)])
        self.feedback_collection.create_index("owner_id", unique=True)

    def create(self, owner_id: str, aggregates: list[dict], limitations: list[str]) -> dict:
        record = {"_id": str(uuid4()), "owner_id": owner_id, "aggregates": aggregates, "limitations": limitations, "created_at": datetime.now(UTC)}
        self.collection.insert_one(record)
        return record

    def latest_for_owner(self, owner_id: str) -> dict | None:
        return self.collection.find_one({"owner_id": owner_id}, sort=[("created_at", -1)])

    def save_feedback(self, owner_id: str, note: str) -> dict:
        record = {"owner_id": owner_id, "note": note, "updated_at": datetime.now(UTC)}
        self.feedback_collection.update_one({"owner_id": owner_id}, {"$set": record}, upsert=True)
        return record

    def latest_feedback(self, owner_id: str) -> dict | None:
        return self.feedback_collection.find_one({"owner_id": owner_id})
