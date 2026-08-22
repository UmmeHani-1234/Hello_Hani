"""
CONTEXT BUILDER.

Assembles the structured context sent to the LLM. In Phase 1 (before
RAG and long-term memory exist) this only combines personality +
recent conversation history + the current question. Phases 3-8 will
extend this same function to also inject retrieved knowledge and
retrieved memories, without changing its external shape.
"""

from app.prompts.personality import HANI_PERSONALITY_PROMPT


def build_context(
    query: str,
    conversation_history: list[dict] | None = None,
    retrieved_knowledge: list[dict] | None = None,
    retrieved_memories: list[dict] | None = None,
) -> list[dict]:
    """
    Returns a list of chat messages ready to send to the LLM:
    [system, ...history, user].
    """
    system_sections = [HANI_PERSONALITY_PROMPT]

    if retrieved_knowledge:
        knowledge_block = "\n".join(
            f"- ({item.get('category', 'general')}) {item['content']}"
            for item in retrieved_knowledge
        )
        system_sections.append(f"## Relevant knowledge about Hani\n{knowledge_block}")
    else:
        system_sections.append(
            "## Relevant knowledge about Hani\n(No knowledge base connected yet — "
            "Phase 2+. Do not invent facts to fill this gap.)"
        )

    if retrieved_memories:
        memory_block = "\n".join(f"- {m['memory']}" for m in retrieved_memories)
        system_sections.append(f"## Relevant memory\n{memory_block}")

    messages = [{"role": "system", "content": "\n\n".join(system_sections)}]

    for turn in (conversation_history or [])[-10:]:
        messages.append({"role": turn["role"], "content": turn["content"]})

    messages.append({"role": "user", "content": query})
    return messages
