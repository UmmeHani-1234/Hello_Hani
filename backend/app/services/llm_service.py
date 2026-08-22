"""
LLM SERVICE.

Thin, isolated wrapper around the Groq chat-completions API.
Nothing else in the codebase should import the Groq SDK directly —
if we ever swap providers, this is the only file that changes.
"""

import json
import re

from groq import Groq

from app.config.settings import get_settings

settings = get_settings()
_client: Groq | None = None


def _visible_reply(content: str | None) -> str:
    """Remove reasoning markup sometimes returned by reasoning-capable models."""
    if not content:
        return "I couldn't generate a response just now. Please try again."

    reply = re.sub(
        r"(?:\*{1,3}\s*)?\\?<think\b[^>]*>[\s\S]*?\\?</think>(?:\s*\*{1,3})?",
        "",
        content,
        flags=re.IGNORECASE,
    )
    if re.search(r"\\?<think\b", reply, flags=re.IGNORECASE):
        return "I couldn't generate a clean reply just now. Please try again."
    return reply.strip() or "I couldn't generate a response just now. Please try again."


def get_client() -> Groq:
    # Lazily constructed so importing this module never requires a valid
    # key or a live network dependency (needed for tests / cold start).
    global _client
    if _client is None:
        if not settings.GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to backend/.env (see .env.example)."
            )
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


def chat_completion(messages: list[dict], temperature: float | None = None, max_tokens: int | None = None) -> str:
    """
    messages: list of {"role": "system" | "user" | "assistant", "content": str}
    Returns the assistant's reply text.
    """
    client = get_client()
    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=messages,
        temperature=temperature if temperature is not None else settings.LLM_TEMPERATURE,
        max_tokens=max_tokens if max_tokens is not None else settings.LLM_MAX_TOKENS,
        extra_body={"reasoning_effort": "none", "reasoning_format": "hidden"},
    )
    return _visible_reply(response.choices[0].message.content)


def extract_memories(user_message: str) -> list[dict]:
    """Extract only durable facts the user explicitly provided about Hani."""
    prompt = f"""Extract durable facts explicitly stated by the user about Hani.
Do not infer, correct, embellish, or save questions, requests, greetings, or
assistant-generated claims. Return JSON only in this exact shape:
{{"memories":[{{"memory":"fact stated by user","category":"relationship|project|preference|biography|general"}}]}}
If there are no durable facts to save, return {{"memories":[]}}.

User message: {user_message}"""
    response = get_client().chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[{"role": "system", "content": "You extract facts faithfully."}, {"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=300,
        response_format={"type": "json_object"},
        extra_body={"reasoning_effort": "none", "reasoning_format": "hidden"},
    )
    data = json.loads(response.choices[0].message.content or "{}")
    allowed_categories = {"relationship", "project", "preference", "biography", "general"}
    result = []
    for item in data.get("memories", []):
        memory = item.get("memory") if isinstance(item, dict) else None
        if isinstance(memory, str) and memory.strip() and len(memory.strip()) <= 500:
            category = item.get("category", "general")
            result.append({
                "memory": memory.strip(),
                "category": category if category in allowed_categories else "general",
            })
    return result
