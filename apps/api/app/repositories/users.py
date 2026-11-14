from copy import deepcopy
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


class EmailAlreadyExistsError(Exception):
    pass


class UserRepository(Protocol):
    def create(self, *, email: str, display_name: str, password_hash: str) -> dict: ...
    def find_by_email(self, email: str) -> dict | None: ...
    def find_by_id(self, user_id: str) -> dict | None: ...
    def set_onboarding(self, user_id: str, onboarding: dict) -> dict: ...


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users: dict[str, dict] = {}

    def create(self, *, email: str, display_name: str, password_hash: str) -> dict:
        if self.find_by_email(email):
            raise EmailAlreadyExistsError
        user = {
            "_id": str(uuid4()), "email": email.lower(), "display_name": display_name,
            "password_hash": password_hash, "created_at": datetime.now(UTC), "onboarding": None,
        }
        self.users[user["_id"]] = user
        return deepcopy(user)

    def find_by_email(self, email: str) -> dict | None:
        return next((deepcopy(user) for user in self.users.values() if user["email"] == email.lower()), None)

    def find_by_id(self, user_id: str) -> dict | None:
        user = self.users.get(user_id)
        return deepcopy(user) if user else None

    def set_onboarding(self, user_id: str, onboarding: dict) -> dict:
        self.users[user_id]["onboarding"] = deepcopy(onboarding)
        return deepcopy(self.users[user_id])


class MongoUserRepository:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection
        self.collection.create_index("email", unique=True)

    def create(self, *, email: str, display_name: str, password_hash: str) -> dict:
        user = {
            "_id": str(uuid4()), "email": email.lower(), "display_name": display_name,
            "password_hash": password_hash, "created_at": datetime.now(UTC), "onboarding": None,
        }
        try:
            self.collection.insert_one(user)
        except DuplicateKeyError as error:
            raise EmailAlreadyExistsError from error
        return user

    def find_by_email(self, email: str) -> dict | None:
        return self.collection.find_one({"email": email.lower()})

    def find_by_id(self, user_id: str) -> dict | None:
        return self.collection.find_one({"_id": user_id})

    def set_onboarding(self, user_id: str, onboarding: dict) -> dict:
        return self.collection.find_one_and_update(
            {"_id": user_id}, {"$set": {"onboarding": onboarding}}, return_document=True
        )
