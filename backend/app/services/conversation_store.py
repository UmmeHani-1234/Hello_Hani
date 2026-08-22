"""MongoDB persistence for chat conversations."""

from datetime import UTC, datetime

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.config.settings import get_settings

settings = get_settings()
_client: MongoClient | None = None


def get_database():
    """Return the configured database after verifying Atlas is reachable."""
    global _client
    if not settings.MONGODB_URI:
        raise RuntimeError("MONGODB_URI is not set. Add it to backend/.env.")

    if _client is None:
        _client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=7000)

    try:
        _client.admin.command("ping")
    except PyMongoError as exc:
        raise RuntimeError(f"MongoDB connection failed: {exc}") from exc

    return _client[settings.MONGODB_DB_NAME]


def _collection():
    return get_database()["conversations"]


def get_messages(conversation_id: str) -> list[dict] | None:
    document = _collection().find_one({"_id": conversation_id}, {"messages": 1})
    return document["messages"] if document else None


def append_messages(conversation_id: str, messages: list[dict]) -> None:
    now = datetime.now(UTC)
    _collection().update_one(
        {"_id": conversation_id},
        {
            "$push": {"messages": {"$each": messages}},
            "$set": {"updated_at": now},
            "$setOnInsert": {"created_at": now},
        },
        upsert=True,
    )


def delete_conversation(conversation_id: str) -> None:
    _collection().delete_one({"_id": conversation_id})
