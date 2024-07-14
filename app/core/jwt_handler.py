import jwt
from datetime import datetime, timedelta
from typing import Optional
from os import environ

SECRET_KEY = environ.get("SECRET_KEY",default="mystrongsecret")
ALGORITHM = environ.get("ALGORITHM",default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = environ.get("ACCESS_TOKEN_EXPIRE_MINUTES",30)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


