import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str , hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode , settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(days=7)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode , settings.SECRET_KEY, algorithm=settings.ALGORITHM)
