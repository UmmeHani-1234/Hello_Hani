"""Durable, user-provided facts that can be used in later conversations."""

from datetime import UTC, datetime
from hashlib import sha256
import re

from app.config.settings import get_settings
from app.services.conversation_store import get_database

settings = get_settings()


def relevant_memories(query: str) -> list[dict]:
    """Return memories only when the current message mentions their topic."""
    terms = {term.casefold() for term in re.findall(r"[A-Za-z]{3,}", query)}
    if not terms:
        return []

    documents = (
        get_database()["memories"]
        .find(
            {"$or": [{"memory": re.compile(rf"\b{re.escape(term)}\b", re.I)} for term in terms]},
            {"_id": 0, "memory": 1, "category": 1},
        )
        .sort("updated_at", -1)
        .limit(settings.MEMORY_TOP_K)
    )
    return list(documents)


def store_memories(memories: list[dict], conversation_id: str) -> int:
    """Upsert extracted facts without duplicating the same memory."""
    collection = get_database()["memories"]
    now = datetime.now(UTC)
    stored = 0

    for item in memories:
        memory = item["memory"].strip()
        fingerprint = sha256(memory.casefold().encode("utf-8")).hexdigest()
        collection.update_one(
            {"fingerprint": fingerprint},
            {
                "$set": {
                    "memory": memory,
                    "category": item.get("category", "general"),
                    "updated_at": now,
                    "last_conversation_id": conversation_id,
                },
                "$setOnInsert": {"created_at": now, "fingerprint": fingerprint},
                "$inc": {"observation_count": 1},
            },
            upsert=True,
        )
        stored += 1

    return stored
