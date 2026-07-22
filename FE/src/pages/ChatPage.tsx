import { useEffect, useState } from "react";
import { api, ApiError } from "../api";
import type { Conversation, Message } from "../types";
import { Sidebar } from "../components/Sidebar";
import { ChatWindow } from "../components/ChatWindow";

export function ChatPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [creating, setCreating] = useState(false);
  const [sending, setSending] = useState(false);
  const [errorText, setErrorText] = useState<string | null>(null);

  // Tải danh sách conversation khi vào trang
  useEffect(() => {
    api
      .listConversations()
      .then((list) => {
        setConversations(list);
        if (list.length > 0) setActiveId(list[0].id);
      })
      .catch(() => setErrorText("Không tải được danh sách cuộc trò chuyện."));
  }, []);

  // Mỗi khi đổi conversation đang xem, tải lại tin nhắn của nó
  useEffect(() => {
    if (activeId === null) {
      setMessages([]);
      return;
    }
    setLoadingMessages(true);
    setErrorText(null);
    api
      .listMessages(activeId)
      .then(setMessages)
      .catch(() => setErrorText("Không tải được tin nhắn của cuộc trò chuyện này."))
      .finally(() => setLoadingMessages(false));
  }, [activeId]);

  async function handleCreateConversation() {
    setCreating(true);
    try {
      const conv = await api.createConversation(
        `Cuộc trò chuyện ${conversations.length + 1}`
      );
      setConversations((prev) => [conv, ...prev]);
      setActiveId(conv.id);
    } catch {
      setErrorText("Không tạo được cuộc trò chuyện mới.");
    } finally {
      setCreating(false);
    }
  }

  async function handleSend(content: string) {
    if (activeId === null) return;
    setErrorText(null);

    // Hiện tin nhắn user ngay lập tức (optimistic update),
    // vì backend chỉ trả về message của assistant, không trả lại message user vừa gửi
    const optimisticUserMessage: Message = {
      id: Date.now(),
      role: "user",
      content,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimisticUserMessage]);
    setSending(true);

    try {
      const aiMessage = await api.sendMessage(activeId, content);
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      const detail =
        err instanceof ApiError ? err.message : "Không gửi được tin nhắn, thử lại nhé.";
      setErrorText(detail);
      // Gửi thất bại: bỏ tin nhắn optimistic ra để không gây hiểu lầm là đã gửi thành công
      setMessages((prev) => prev.filter((m) => m.id !== optimisticUserMessage.id));
    } finally {
      setSending(false);
    }
  }

  const activeConversation =
    conversations.find((c) => c.id === activeId) ?? null;

  return (
    <div className="flex h-screen w-full overflow-hidden">
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={setActiveId}
        onCreate={handleCreateConversation}
        creating={creating}
      />
      <ChatWindow
        conversation={activeConversation}
        messages={messages}
        loadingMessages={loadingMessages}
        sending={sending}
        errorText={errorText}
        onSend={handleSend}
      />
    </div>
  );
}
