import type { Conversation, Message, User } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:9000";
const TOKEN_KEY = "chatbot_access_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") detail = body.detail;
    } catch {
      // response wasn't JSON, keep default statusText
    }
    if (res.status === 401) clearToken();
    throw new ApiError(res.status, detail);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export { ApiError };

export const api = {
  register: (email: string, password: string) =>
    request<User>("/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  login: async (email: string, password: string) => {
    const data = await request<{ access_token: string; token_type: string }>(
      "/login",
      {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }
    );
    setToken(data.access_token);
    return data;
  },

  me: () => request<User>("/users/me"),

  listConversations: () => request<Conversation[]>("/conversations"),

  createConversation: (title: string) =>
    request<Conversation>("/conversations", {
      method: "POST",
      body: JSON.stringify({ title }),
    }),

  listMessages: (conversationId: number) =>
    request<Message[]>(`/conversations/${conversationId}/messages`),

  sendMessage: (conversationId: number, content: string) =>
    request<Message>(`/conversations/${conversationId}/messages`, {
      method: "POST",
      body: JSON.stringify({ content }),
    }),
};
