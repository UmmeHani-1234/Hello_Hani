from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config.settings import get_settings
from app.prompts.context_builder import build_context
from app.services.conversation_store import (
    append_messages,
    delete_conversation as delete_stored_conversation,
    get_messages,
)
from app.services.llm_service import chat_completion, extract_memories
from app.services.knowledge_store import relevant_knowledge
from app.services.memory_store import relevant_memories, store_memories

router = APIRouter(prefix="/api", tags=["chat"])
settings = get_settings()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str
    debug: dict | None = None


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    conversation_id = payload.conversation_id or str(uuid4())
    try:
        history = get_messages(conversation_id) or []
        memories = relevant_memories(message)
        knowledge = relevant_knowledge(message)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    messages = build_context(
        query=message,
        conversation_history=history,
        retrieved_knowledge=knowledge,
        retrieved_memories=memories,
    )

    try:
        reply = chat_completion(messages)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM call failed: {e}")

    new_messages = [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    try:
        append_messages(conversation_id, new_messages)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    # Memory extraction is best-effort: a chat reply should not fail if it cannot run.
    try:
        store_memories(extract_memories(message), conversation_id)
    except Exception:
        pass

    debug = None
    if settings.DEBUG_RAG:
        debug = {"context_messages": len(messages), "history_length": len(history) + len(new_messages)}

    return ChatResponse(reply=reply, conversation_id=conversation_id, debug=debug)


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    try:
        messages = get_messages(conversation_id)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    if messages is None:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return {"conversation_id": conversation_id, "messages": messages}


@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    try:
        delete_stored_conversation(conversation_id)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return {"deleted": True}
