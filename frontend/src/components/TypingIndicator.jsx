import Mascot from "./Mascot.jsx";

export default function TypingIndicator() {
  return (
    <div className="flex items-start gap-2.5">
      <div className="shrink-0 mt-0.5">
        <Mascot size={28} thinking />
      </div>
      <div className="rounded-2xl rounded-tl-sm bg-white/90 border border-lilac-100 px-4 py-3 shadow-soft">
        <div className="flex gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-lilac-500 animate-bounce [animation-delay:-0.3s]" />
          <span className="w-1.5 h-1.5 rounded-full bg-lilac-500 animate-bounce [animation-delay:-0.15s]" />
          <span className="w-1.5 h-1.5 rounded-full bg-lilac-500 animate-bounce" />
        </div>
      </div>
    </div>
  );
}
