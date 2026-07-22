# App Chatbot

Ứng dụng chatbot full-stack gồm frontend React, backend FastAPI, database PostgreSQL, đăng nhập bằng JWT và tích hợp LLM qua API tương thích OpenAI.

Repo được tách thành hai phần chính:

- `FE/`: giao diện web React + TypeScript + Vite + Tailwind CSS
- `BE/`: API FastAPI + SQLAlchemy + PostgreSQL + Docker Compose

## Tính năng chính

- Đăng ký và đăng nhập tài khoản
- Xác thực request bằng JWT Bearer Token
- Tạo và xem danh sách cuộc trò chuyện
- Lưu lịch sử tin nhắn theo từng conversation
- Gửi tin nhắn người dùng và nhận phản hồi từ assistant
- Health check cho backend
- Docker Compose cho backend và PostgreSQL
- Có sẵn manifest Kubernetes và Helm chart cho hướng triển khai nâng cao

## Công nghệ sử dụng

| Phần | Công nghệ |
| --- | --- |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Backend | FastAPI, Uvicorn, Pydantic |
| Database | PostgreSQL 16, SQLAlchemy |
| Auth | JWT, passlib, bcrypt |
| AI | OpenAI-compatible SDK/provider |
| DevOps | Docker, Docker Compose, Kubernetes, Helm |

## Cấu trúc thư mục

```text
App_chatbot/
  BE/
    main.py                 # Khai báo FastAPI app và API routes
    models.py               # SQLAlchemy models
    schemas.py              # Pydantic schemas cho request/response
    auth.py                 # Hash password và xử lý JWT
    llm.py                  # Tích hợp LLM provider
    database.py             # Kết nối database và session
    docker-compose.yml      # Chạy PostgreSQL + backend
    Dockerfile              # Đóng gói backend
    k8s/                    # Kubernetes manifests
    chatbot-chart/          # Helm chart
  FE/
    src/
      api.ts                # API client gọi backend
      context/              # Auth context
      pages/                # Trang đăng nhập và chat
      components/           # Component giao diện chat
    package.json
    vite.config.ts
```

## Yêu cầu

- Docker Desktop
- Node.js 18+ và npm
- API key, base URL và model name của LLM provider

## Cấu hình môi trường

Tạo file `BE/.env` trước khi bật backend:

```env
SECRET_KEY=change-this-to-a-long-random-secret
LLM_API_KEY=your-llm-api-key
LLM_BASE_URL=https://your-llm-provider.example/v1
LLM_MODEL=your-model-name
```

Khi chạy bằng Docker Compose, `DATABASE_URL` đã được cấu hình sẵn trong `BE/docker-compose.yml`.

Nếu chạy backend trực tiếp trên máy, thêm dòng này vào `BE/.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/chatbot
```

Frontend mặc định gọi backend ở `http://localhost:9000`. Nếu cần đổi URL backend, tạo file `FE/.env`:

```env
VITE_API_URL=http://localhost:9000
```

## Chạy nhanh

### 1. Bật backend và database

```bash
cd BE
docker compose up --build
```

Backend chạy tại:

```text
http://localhost:9000
```

PostgreSQL được expose ra máy tại:

```text
localhost:5433
```

### 2. Bật frontend

Mở terminal thứ hai:

```bash
cd FE
npm install
npm run dev
```

Frontend chạy tại:

```text
http://localhost:9001
```

## Lệnh hay dùng

Bật backend/database:

```bash
cd BE
docker compose up
```

Bật backend/database và build lại image:

```bash
cd BE
docker compose up --build
```

Chạy backend/database ở chế độ nền:

```bash
cd BE
docker compose up -d
```

Tắt backend/database:

```bash
cd BE
docker compose down
```

Tắt và xoá luôn volume database local:

```bash
cd BE
docker compose down -v
```

Bật frontend:

```bash
cd FE
npm run dev
```

Build frontend:

```bash
cd FE
npm run build
```

## API chính

| Method | Endpoint | Mô tả |
| --- | --- | --- |
| `GET` | `/` | Kiểm tra backend đang chạy |
| `GET` | `/health/live` | Liveness check |
| `GET` | `/health/ready` | Readiness check |
| `POST` | `/register` | Đăng ký user |
| `POST` | `/login` | Đăng nhập và nhận JWT |
| `GET` | `/users/me` | Lấy thông tin user hiện tại |
| `GET` | `/conversations` | Lấy danh sách conversation |
| `POST` | `/conversations` | Tạo conversation mới |
| `GET` | `/conversations/{id}` | Lấy chi tiết một conversation |
| `GET` | `/conversations/{id}/messages` | Lấy danh sách tin nhắn |
| `POST` | `/conversations/{id}/messages` | Gửi tin nhắn và nhận phản hồi assistant |

Swagger UI của FastAPI có tại:

```text
http://localhost:9000/docs
```

## Ghi chú quan trọng

- Docker Compose hiện chạy `backend` và `PostgreSQL`; frontend vẫn chạy riêng bằng `npm run dev`.
- Dùng `docker compose up --build` sau khi sửa backend, `requirements.txt` hoặc `Dockerfile`.
- Dùng `docker compose up` cho những lần chạy bình thường khi image đã có sẵn.
- Không commit API key, secret thật hoặc thông tin production vào repo.

