"""Verified profile knowledge used to ground Digital Twin responses."""

import re
from datetime import UTC, datetime

from app.config.settings import get_settings
from app.services.conversation_store import get_database

settings = get_settings()


def seed_knowledge(entries: list[dict]) -> int:
    """Upsert trusted profile entries by stable slug."""
    collection = get_database()["knowledge"]
    now = datetime.now(UTC)
    for entry in entries:
        collection.update_one(
            {"slug": entry["slug"]},
            {"$set": {**entry, "updated_at": now}, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )
    return len(entries)


def relevant_knowledge(query: str) -> list[dict]:
    """Retrieve only profile entries whose configured topic keywords match."""
    terms = {term.casefold() for term in re.findall(r"[A-Za-z]{3,}", query)}
    if not terms:
        return []

    documents = (
        get_database()["knowledge"]
        .find(
            {"keywords": {"$in": list(terms)}},
            {"_id": 0, "category": 1, "content": 1},
        )
        .limit(settings.TOP_K)
    )
    return list(documents)
