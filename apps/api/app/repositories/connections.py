from copy import deepcopy
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from pymongo.collection import Collection


class ConnectionRepository(Protocol):
    def save_connection(self, owner_id: str, encrypted_token: str, scopes: list[str]) -> dict: ...
    def connection_for_owner(self, owner_id: str) -> dict | None: ...
    def disconnect(self, owner_id: str) -> bool: ...
    def add_audit(self, owner_id: str, action: str, details: dict) -> dict: ...
    def audit_for_owner(self, owner_id: str) -> list[dict]: ...
    def save_oauth_state(self, owner_id: str, state: str) -> None: ...
    def consume_oauth_state(self, state: str) -> str | None: ...


class InMemoryConnectionRepository:
    def __init__(self) -> None:
        self.connections: list[dict] = []
        self.audits: list[dict] = []
        self.oauth_states: dict[str, str] = {}

    def save_connection(self, owner_id: str, encrypted_token: str, scopes: list[str]) -> dict:
        self.connections = [item for item in self.connections if item["owner_id"] != owner_id]
        record = {"_id": str(uuid4()), "owner_id": owner_id, "encrypted_token": encrypted_token, "scopes": scopes, "connected_at": datetime.now(UTC)}
        self.connections.append(record)
        return deepcopy(record)

    def connection_for_owner(self, owner_id: str) -> dict | None:
        return next((deepcopy(item) for item in self.connections if item["owner_id"] == owner_id), None)

    def disconnect(self, owner_id: str) -> bool:
        before = len(self.connections)
        self.connections = [item for item in self.connections if item["owner_id"] != owner_id]
        return len(self.connections) != before

    def add_audit(self, owner_id: str, action: str, details: dict) -> dict:
        record = {"_id": str(uuid4()), "owner_id": owner_id, "action": action, "details": deepcopy(details), "created_at": datetime.now(UTC)}
        self.audits.append(record)
        return deepcopy(record)

    def audit_for_owner(self, owner_id: str) -> list[dict]:
        return [deepcopy(item) for item in self.audits if item["owner_id"] == owner_id]
    def save_oauth_state(self, owner_id: str, state: str) -> None: self.oauth_states[state] = owner_id
    def consume_oauth_state(self, state: str) -> str | None: return self.oauth_states.pop(state, None)


class MongoConnectionRepository:
    def __init__(self, connections: Collection, audits: Collection) -> None:
        self.connections = connections
        self.audits = audits
        self.connections.create_index("owner_id", unique=True)
        self.audits.create_index([("owner_id", 1), ("created_at", -1)])
        self.states = connections.database.instagram_oauth_states
        self.states.create_index("state", unique=True)

    def save_connection(self, owner_id: str, encrypted_token: str, scopes: list[str]) -> dict:
        record = {"_id": str(uuid4()), "owner_id": owner_id, "encrypted_token": encrypted_token, "scopes": scopes, "connected_at": datetime.now(UTC)}
        self.connections.replace_one({"owner_id": owner_id}, record, upsert=True)
        return record

    def connection_for_owner(self, owner_id: str) -> dict | None:
        return self.connections.find_one({"owner_id": owner_id})

    def disconnect(self, owner_id: str) -> bool:
        return self.connections.delete_one({"owner_id": owner_id}).deleted_count == 1

    def add_audit(self, owner_id: str, action: str, details: dict) -> dict:
        record = {"_id": str(uuid4()), "owner_id": owner_id, "action": action, "details": details, "created_at": datetime.now(UTC)}
        self.audits.insert_one(record)
        return record

    def audit_for_owner(self, owner_id: str) -> list[dict]:
        return list(self.audits.find({"owner_id": owner_id}, {"encrypted_token": 0}).sort("created_at", -1))
    def save_oauth_state(self, owner_id: str, state: str) -> None:
        self.states.insert_one({"state": state, "owner_id": owner_id, "created_at": datetime.now(UTC)})
    def consume_oauth_state(self, state: str) -> str | None:
        record = self.states.find_one_and_delete({"state": state})
        return record["owner_id"] if record else None
