from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
class ConversationCreate(BaseModel):
    title: str
class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    class Config:
        from_attributes = True
class MessageCreate(BaseModel):
    content: str
class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    class Config:
        from_attributes = True

#UserCreate — dữ liệu client gửi lên khi đăng ký (email + password thô, chưa mã hóa)
#UserOut — dữ liệu server trả về cho client (không có password_hash, tránh lộ thông tin nhạy cảm)
#Token — dữ liệu trả về sau khi đăng nhập thành công (JWT token)
#class Config: from_attributes = True — cho phép Pydantic đọc trực tiếp từ object SQLAlchemy (models.User) thay vì chỉ nhận dict

#Tại sao cần tách riêng schemas.py và models.py: models.py mô tả bảng thật trong DB (có cả password_hash), còn schemas.py mô tả dữ liệu API cho phép client thấy/gửi — tách ra để không bao giờ vô tình trả password_hash về cho client.
