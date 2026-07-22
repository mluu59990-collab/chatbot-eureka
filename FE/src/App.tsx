import { useAuth } from "./context/AuthContext";
import { AuthPage } from "./pages/AuthPage";
import { ChatPage } from "./pages/ChatPage";

export default function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg">
        <p className="font-mono text-sm text-ink-tertiary">Đang tải...</p>
      </div>
    );
  }

  return user ? <ChatPage /> : <AuthPage />;
}
