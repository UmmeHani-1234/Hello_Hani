import { useEffect, useRef, useState } from "react";
import Mascot from "./components/Mascot.jsx";
import MessageBubble from "./components/MessageBubble.jsx";
import TypingIndicator from "./components/TypingIndicator.jsx";
import { sendMessage } from "./services/api.js";

const SUGGESTIONS = [
  "How's your day going?",
  "What are you doing today?",
  "What's on your mind?",
  "what do you want to know about Hani?",
];

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isTyping]);

  async function handleSend(text) {
    const trimmed = (text ?? input).trim();
    if (!trimmed || isTyping) return;

    setError(null);
    setMessages((m) => [...m, { role: "user", content: trimmed }]);
    setInput("");
    setIsTyping(true);

    try {
      const data = await sendMessage(trimmed, conversationId);
      setConversationId(data.conversation_id);
      setMessages((m) => [...m, { role: "assistant", content: data.reply }]);
    } catch (err) {
      setError(err.message || "Something went wrong reaching Hani's Digital Twin.");
    } finally {
      setIsTyping(false);
    }
  }

  function handleNewConversation() {
    setMessages([]);
    setConversationId(null);
    setError(null);
  }

  const hasStarted = messages.length > 0;

  return (
    <div className="min-h-screen flex flex-col items-center px-4 py-6 md:py-10">
      <div className="w-full max-w-2xl flex flex-col h-[88vh]">
        {/* header */}
        <header className="flex items-center justify-between px-1 pb-5">
          <div className="flex items-center gap-3">
            <Mascot size={44} />
            <div>
              <h1 className="font-display font-semibold text-xl leading-none text-ink">
                Hani <span className="text-lilac-500">·</span> Digital Twin
              </h1>
              <p className="text-xs text-ink-soft mt-1">Ask me anything about Hani.</p>
            </div>
          </div>
          {hasStarted && (
            <button
              onClick={handleNewConversation}
              className="text-xs font-medium text-ink-soft hover:text-ink border border-lilac-100 hover:border-lilac-300 rounded-full px-3.5 py-2 transition-colors bg-white/70"
            >
              New conversation
            </button>
          )}
        </header>

        {/* chat surface */}
        <div className="flex-1 rounded-3xl bg-white/60 backdrop-blur-sm border border-white shadow-soft flex flex-col overflow-hidden">
          <div ref={scrollRef} className="flex-1 overflow-y-auto scroll-thin px-5 py-6 space-y-4">
            {!hasStarted && (
              <div className="h-full flex flex-col items-center justify-center text-center gap-4 py-10">
                <Mascot size={72} />
                <div>
                  <p className="font-display text-lg text-ink">Hey, I'm Hani's twin.</p>
                  <p className="text-sm text-ink-soft mt-1 max-w-sm">
                    I talk, reason, and answer the way she would — built from what's
                    actually known about her, nothing invented.
                  </p>
                </div>
                <div className="flex flex-col gap-2 w-full max-w-sm pt-2">
                  {SUGGESTIONS.map((s) => (
                    <button
                      key={s}
                      onClick={() => handleSend(s)}
                      className="text-sm text-left px-4 py-2.5 rounded-xl bg-white border border-lilac-100 hover:border-lilac-300 text-ink-soft hover:text-ink transition-colors"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((m, i) => (
              <MessageBubble key={i} role={m.role} content={m.content} />
            ))}

            {isTyping && <TypingIndicator />}

            {error && (
              <div className="text-sm text-rose-600 bg-rose-50 border border-rose-100 rounded-xl px-4 py-3">
                {error}
              </div>
            )}
          </div>

          {/* input */}
          <div className="border-t border-lilac-100 bg-white/70 px-4 py-3">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center gap-2"
            >
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me anything…"
                className="flex-1 bg-transparent outline-none text-[15px] text-ink placeholder:text-ink-soft/70 px-2 py-2"
              />
              <button
                type="submit"
                disabled={!input.trim() || isTyping}
                className="rounded-full bg-onyx text-white w-10 h-10 flex items-center justify-center disabled:opacity-30 transition-opacity"
                aria-label="Send message"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M4 12L20 4L14 20L11 13L4 12Z" stroke="white" strokeWidth="1.8" strokeLinejoin="round" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
