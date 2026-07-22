import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { ApiError } from "../api";

export function AuthPage() {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const isLogin = mode === "login";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password);
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Không kết nối được tới server. Kiểm tra lại backend đang chạy chưa.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-bg px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-ink font-mono text-lg font-semibold text-white">
            {"</>"}
          </div>
          <div className="text-center">
            <h1 className="font-mono text-lg font-semibold tracking-tight text-ink">
              chatbot_
            </h1>
            <p className="mt-1 text-sm text-ink-secondary">
              {isLogin ? "Đăng nhập để tiếp tục" : "Tạo tài khoản mới"}
            </p>
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-surface p-6 shadow-panel">
          <div className="mb-6 flex rounded-lg bg-bg p-1">
            <button
              type="button"
              onClick={() => {
                setMode("login");
                setError(null);
              }}
              className={`flex-1 rounded-md py-1.5 text-sm font-medium transition-colors ${
                isLogin ? "bg-surface text-ink shadow-subtle" : "text-ink-tertiary"
              }`}
            >
              Đăng nhập
            </button>
            <button
              type="button"
              onClick={() => {
                setMode("register");
                setError(null);
              }}
              className={`flex-1 rounded-md py-1.5 text-sm font-medium transition-colors ${
                !isLogin ? "bg-surface text-ink shadow-subtle" : "text-ink-tertiary"
              }`}
            >
              Đăng ký
            </button>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-ink-secondary">Email</span>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="ban@example.com"
                className="rounded-lg border border-border bg-bg px-3 py-2 text-sm text-ink placeholder:text-ink-tertiary focus:border-accent"
              />
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-ink-secondary">Mật khẩu</span>
              <input
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="rounded-lg border border-border bg-bg px-3 py-2 text-sm text-ink placeholder:text-ink-tertiary focus:border-accent"
              />
            </label>

            {error && (
              <p className="rounded-md bg-danger-soft px-3 py-2 text-xs text-danger">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="mt-1 rounded-lg bg-accent py-2.5 text-sm font-medium text-white transition-colors hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-60"
            >
              {submitting
                ? "Đang xử lý..."
                : isLogin
                ? "Đăng nhập"
                : "Tạo tài khoản"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
