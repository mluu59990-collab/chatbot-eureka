import type { Conversation } from "../types";
import { useAuth } from "../context/AuthContext";

interface SidebarProps {
  conversations: Conversation[];
  activeId: number | null;
  onSelect: (id: number) => void;
  onCreate: () => void;
  creating: boolean;
}

function initialsOf(email: string) {
  return email.slice(0, 2).toUpperCase();
}

export function Sidebar({
  conversations,
  activeId,
  onSelect,
  onCreate,
  creating,
}: SidebarProps) {
  const { user, logout } = useAuth();

  return (
    <aside className="flex h-full w-72 shrink-0 flex-col border-r border-border bg-surface">
      <div className="flex items-center gap-2 px-5 py-5">
        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-ink font-mono text-sm font-semibold text-white">
          {"</>"}
        </div>
        <span className="font-mono text-sm font-semibold tracking-tight text-ink">
          chatbot_
        </span>
      </div>

      <div className="px-3">
        <button
          onClick={onCreate}
          disabled={creating}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-accent px-3 py-2.5 text-sm font-medium text-white transition-colors hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-60"
        >
          <span className="text-base leading-none">+</span>
          {creating ? "Đang tạo..." : "Cuộc trò chuyện mới"}
        </button>
      </div>

      <nav className="mt-4 flex-1 space-y-0.5 overflow-y-auto px-3 pb-3">
        {conversations.length === 0 && (
          <p className="px-2 py-6 text-center text-sm text-ink-tertiary">
            Chưa có cuộc trò chuyện nào.
          </p>
        )}
        {conversations.map((c) => {
          const isActive = c.id === activeId;
          return (
            <button
              key={c.id}
              onClick={() => onSelect(c.id)}
              className={`block w-full truncate rounded-md px-3 py-2 text-left text-sm transition-colors ${
                isActive
                  ? "border-l-2 border-accent bg-accent-soft pl-[10px] font-medium text-accent"
                  : "border-l-2 border-transparent text-ink-secondary hover:bg-bg hover:text-ink"
              }`}
              title={c.title}
            >
              {c.title || "Cuộc trò chuyện"}
            </button>
          );
        })}
      </nav>

      <div className="flex items-center gap-2 border-t border-border px-4 py-3">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-bg font-mono text-xs font-semibold text-ink-secondary ring-1 ring-border">
          {user ? initialsOf(user.email) : "??"}
        </div>
        <span className="flex-1 truncate text-sm text-ink-secondary">
          {user?.email}
        </span>
        <button
          onClick={logout}
          className="rounded-md px-2 py-1 text-xs font-medium text-ink-tertiary transition-colors hover:bg-danger-soft hover:text-danger"
        >
          Đăng xuất
        </button>
      </div>
    </aside>
  );
}
