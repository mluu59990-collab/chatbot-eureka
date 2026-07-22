import type { Message } from "../types";

function formatTime(iso: string) {
  const d = new Date(iso);
  return d.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
}

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex items-start gap-3 animate-fadeIn ${
        isUser ? "flex-row-reverse" : ""
      }`}
    >
      <div
        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-md font-mono text-xs font-semibold ${
          isUser ? "bg-ink text-white" : "bg-accent text-white"
        }`}
      >
        {isUser ? "U" : "AI"}
      </div>

      <div className={`flex max-w-[72%] flex-col gap-1 ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={`whitespace-pre-wrap rounded-2xl px-4 py-2.5 text-[15px] leading-relaxed shadow-subtle ${
            isUser
              ? "rounded-tr-sm bg-accent text-white"
              : "rounded-tl-sm border border-border bg-surface text-ink"
          }`}
        >
          {message.content}
        </div>
        <span className="font-mono text-[11px] text-ink-tertiary">
          {formatTime(message.created_at)}
        </span>
      </div>
    </div>
  );
}

export function TypingBubble() {
  return (
    <div className="flex items-start gap-3 animate-fadeIn">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-accent font-mono text-xs font-semibold text-white">
        AI
      </div>
      <div className="flex items-center gap-1 rounded-2xl rounded-tl-sm border border-border bg-surface px-4 py-3 shadow-subtle">
        <span className="h-1.5 w-1.5 animate-dotPulse rounded-full bg-ink-tertiary [animation-delay:0ms]" />
        <span className="h-1.5 w-1.5 animate-dotPulse rounded-full bg-ink-tertiary [animation-delay:150ms]" />
        <span className="h-1.5 w-1.5 animate-dotPulse rounded-full bg-ink-tertiary [animation-delay:300ms]" />
      </div>
    </div>
  );
}
