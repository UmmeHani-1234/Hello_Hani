import Mascot from "./Mascot.jsx";

export default function MessageBubble({ role, content }) {
  const isUser = role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[75%] rounded-2xl rounded-tr-sm bg-onyx text-white px-4 py-3 text-[15px] leading-relaxed shadow-soft">
          {content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-2.5">
      <div className="shrink-0 mt-0.5">
        <Mascot size={28} />
      </div>
      <div className="max-w-[75%] rounded-2xl rounded-tl-sm bg-white/90 border border-lilac-100 px-4 py-3 text-[15px] leading-relaxed text-ink shadow-soft">
        {content}
      </div>
    </div>
  );
}
