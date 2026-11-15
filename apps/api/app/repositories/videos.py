from copy import deepcopy
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4
from pymongo.collection import Collection
from pymongo import ReturnDocument

class VideoRepository(Protocol):
    def create(self, owner_id: str, data: dict) -> dict: ...
    def list_for_owner(self, owner_id: str) -> list[dict]: ...
    def find_for_owner(self, owner_id: str, video_id: str) -> dict | None: ...
    def update_for_owner(self, owner_id: str, video_id: str, changes: dict) -> dict | None: ...

class InMemoryVideoRepository:
    def __init__(self) -> None: self.records: list[dict] = []
    def create(self, owner_id: str, data: dict) -> dict:
        record={"_id":str(uuid4()),"owner_id":owner_id,**deepcopy(data),"created_at":datetime.now(UTC)}; self.records.append(record); return deepcopy(record)
    def list_for_owner(self, owner_id: str) -> list[dict]: return [deepcopy(x) for x in self.records if x["owner_id"]==owner_id]
    def find_for_owner(self, owner_id: str, video_id: str) -> dict | None:
        return next((deepcopy(x) for x in self.records if x["owner_id"] == owner_id and x["_id"] == video_id), None)
    def update_for_owner(self, owner_id: str, video_id: str, changes: dict) -> dict | None:
        for record in self.records:
            if record["owner_id"] == owner_id and record["_id"] == video_id:
                record.update(deepcopy(changes))
                return deepcopy(record)
        return None

class MongoVideoRepository:
    def __init__(self, collection: Collection) -> None: self.collection=collection; self.collection.create_index([("owner_id",1),("created_at",-1)])
    def create(self, owner_id: str, data: dict) -> dict:
        record={"_id":str(uuid4()),"owner_id":owner_id,**data,"created_at":datetime.now(UTC)}; self.collection.insert_one(record); return record
    def list_for_owner(self, owner_id: str) -> list[dict]: return list(self.collection.find({"owner_id":owner_id}).sort("created_at",-1))
    def find_for_owner(self, owner_id: str, video_id: str) -> dict | None: return self.collection.find_one({"_id":video_id,"owner_id":owner_id})
    def update_for_owner(self, owner_id: str, video_id: str, changes: dict) -> dict | None:
        return self.collection.find_one_and_update({"_id": video_id, "owner_id": owner_id}, {"$set": changes}, return_document=ReturnDocument.AFTER)
