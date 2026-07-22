from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from database import get_db
import models


# Cấu hình thuật toán mã hoá password
pwd_context = CryptContext(schemes = ["bcrypt"],deprecated = "auto")
# Cấu hình JWT(bi mat de ky token, thuat toan, thoi gian song)
load_dotenv(Path(__file__).resolve().parent / ".env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# Hamf biến password thành mã hash 1 chiều không thể giải mã
def hash_password(password:str) ->str:
    return pwd_context.hash(password)
#So sánh password thô người dùng nhập lúc đăng nhập với hash đã lưu trong DB trả về TRue/false
def verify_password(plain_password: str, hashed_password: str) ->bool:
    return pwd_context.verify(plain_password,hashed_password)
# Tạo jwt token chứa thông tin user (VD: email) + thời gian hết hạn, ký bằng Secret_key để server sau này verify được token có bị giả mạo hay không
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers ={"WWW-Authenticate":"Bearer"},
    )
    try:
        #jwt.decode: lam 2 viec: verify chu ky dam baor token do dung server ky va giai ma payload ra dict
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
