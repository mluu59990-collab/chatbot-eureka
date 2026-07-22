import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

#Đối tượng quản lý kết nối thật tới postgres
engine = create_engine(DATABASE_URL)
#Tạo ra 1 phiên làm việc với DB mỗi khi có request tới API
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Lớp gốc để các bảng sau này kês thừa
Base = declarative_base()
#Hàm dùng trong fasst API để đóng mở session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
