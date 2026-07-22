# Chatbot FE

Frontend React + TypeScript + Vite + Tailwind cho `App_chatbot`, kết nối tới backend FastAPI đã có sẵn (`/register`, `/login`, `/users/me`, `/conversations`, `/conversations/{id}/messages`).

## 1. Cài đặt

```bash
npm install
```

## 2. Cấu hình URL backend (nếu cần)

Mặc định app gọi tới `http://localhost:9000`. Nếu backend chạy ở địa chỉ khác, tạo file `.env` (copy từ `.env.example`):

```bash
cp .env.example .env
```

và sửa `VITE_API_URL` cho đúng.

## 3. QUAN TRỌNG — bật CORS ở backend trước khi chạy FE

Vì FE (`localhost:9001`) và BE (`localhost:9000`) chạy ở 2 port khác nhau, trình duyệt sẽ chặn request bằng chính sách CORS nếu backend chưa cho phép. Thêm đoạn sau vào `main.py`, **ngay sau dòng `app = FastAPI()`**:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9001", "http://127.0.0.1:9001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Không thêm đoạn này, mọi request từ FE tới BE sẽ bị lỗi `Failed to fetch` / CORS error trên console trình duyệt dù backend chạy hoàn toàn bình thường.

## 4. Chạy dev server

Terminal 1 — chạy backend (trong thư mục `BE` của `App_chatbot`):
```bash
uvicorn main:app --reload --port 9000
```

Terminal 2 — chạy frontend (trong thư mục project này):
```bash
npm run dev
```

Mở `http://localhost:9001`.

## Cấu trúc project

```
src/
  api.ts                 # Gọi API backend, tự đính kèm JWT vào header Authorization
  types.ts                # Type khớp với schemas.py bên backend
  context/AuthContext.tsx # Quản lý trạng thái đăng nhập toàn app
  pages/AuthPage.tsx      # Màn hình Login/Register
  pages/ChatPage.tsx      # Màn hình chính: sidebar + khung chat
  components/Sidebar.tsx      # Danh sách conversations, nút tạo mới, logout
  components/ChatWindow.tsx   # Khung tin nhắn + ô nhập
  components/MessageBubble.tsx # 1 bong bóng tin nhắn + hiệu ứng "đang gõ"
```

## Lưu ý về cách lưu token

Token JWT được lưu ở `localStorage` (key `chatbot_access_token`) để giữ đăng nhập qua các lần refresh trang. Khi API trả về `401` (token hết hạn/không hợp lệ), token sẽ tự động bị xoá và người dùng quay lại màn hình đăng nhập ở lần gọi API tiếp theo.
