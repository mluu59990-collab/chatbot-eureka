import { useEffect, useRef, useState } from "react";
import type { Conversation, Message } from "../types";
import { MessageBubble, TypingBubble } from "./MessageBubble";

interface ChatWindowProps {
  conversation: Conversation | null;
  messages: Message[];
  loadingMessages: boolean;
  sending: boolean;
  errorText: string | null;
  onSend: (content: string) => void;
}

export function ChatWindow({
  conversation,
  messages,
  loadingMessages,
  sending,
  errorText,
  onSend,
}: ChatWindowProps) {
  const [draft, setDraft] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  function submit() {
    const content = draft.trim();
    if (!content || sending) return;
    onSend(content);
    setDraft("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function autoGrow(el: HTMLTextAreaElement) {
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  }

  if (!conversation) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center gap-2 bg-bg text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-accent-soft font-mono text-lg text-accent">
          {"</>"}
        </div>
        <p className="text-sm text-ink-secondary">
          Chọn một cuộc trò chuyện, hoặc tạo cuộc trò chuyện mới để bắt đầu.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col bg-bg">
      <header className="flex items-center justify-between border-b border-border bg-surface px-6 py-4">
        <h1 className="truncate text-sm font-semibold text-ink">
          {conversation.title}
        </h1>
        <span className="font-mono text-xs text-ink-tertiary">
          #{conversation.id}
        </span>
      </header>

      <div className="flex-1 overflow-y-auto px-6 py-6">
        {loadingMessages ? (
          <p className="text-sm text-ink-tertiary">Đang tải tin nhắn...</p>
        ) : (
          <div className="mx-auto flex max-w-3xl flex-col gap-5">
            {messages.length === 0 && (
              <p className="text-center text-sm text-ink-tertiary">
                Chưa có tin nhắn. Hãy đặt câu hỏi đầu tiên.
              </p>
            )}
            {messages.map((m) => (
              <MessageBubble key={m.id} message={m} />
            ))}
            {sending && <TypingBubble />}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <div className="border-t border-border bg-surface px-6 py-4">
        <div className="mx-auto max-w-3xl">
          {errorText && (
            <p className="mb-2 rounded-md bg-danger-soft px-3 py-2 text-xs text-danger">
              {errorText}
            </p>
          )}
          <div className="flex items-end gap-2 rounded-xl border border-border bg-bg px-3 py-2 focus-within:border-accent">
            <textarea
              ref={textareaRef}
              value={draft}
              onChange={(e) => {
                setDraft(e.target.value);
                autoGrow(e.target);
              }}
              onKeyDown={handleKeyDown}
              rows={1}
              placeholder="Nhập tin nhắn... (Enter để gửi, Shift+Enter xuống dòng)"
              className="max-h-40 flex-1 resize-none bg-transparent py-1.5 text-sm text-ink placeholder:text-ink-tertiary focus:outline-none"
            />
            <button
              onClick={submit}
              disabled={!draft.trim() || sending}
              className="shrink-0 rounded-lg bg-accent px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-40"
            >
              Gửi
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
