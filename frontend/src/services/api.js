const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function visibleReply(reply) {
  const cleaned = String(reply ?? "").replace(
    /(?:\*{1,3}\s*)?\\?<think\b[^>]*>[\s\S]*?\\?<\/think>(?:\s*\*{1,3})?/gi,
    "",
  ).trim();

  if (/\\?<think\b/i.test(cleaned)) {
    return "I couldn't generate a clean reply just now. Please try again.";
  }

  return cleaned || "I couldn't generate a response just now. Please try again.";
}

export async function sendMessage(message, conversationId) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }

  const data = await res.json();
  return { ...data, reply: visibleReply(data.reply) };
}
