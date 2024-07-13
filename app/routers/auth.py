from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlmodel import select
from typing import Optional
from pydantic import BaseModel
from core import jwt_handler, security
from db import models, database


router = APIRouter(prefix='/auth', tags=['auth'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    

    
@router.post("/register_or_login", response_model=jwt_handler.Token)
async def register_or_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    statement = select(models.User).where(models.User.email == form_data.username)
    result = db.exec(statement)
    user = result.first()

    if user:
        # User exists, verify password
        if not security.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        # User does not exist, create a new user
        hashed_password = security.get_password_hash(form_data.password)
        new_user = models.User(
            name=form_data.username.split("@")[0],  # Assuming name is part of the email before '@'
            email=form_data.username,
            hashed_password=hashed_password,
            is_admin=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user

    # Generate access token
    access_token = jwt_handler.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=jwt_handler.Token)
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends(), db: Session = Depends(database.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt_handler.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def get_user_by_email(db: Session, email: str):
    statement = select(models.User).where(models.User.email == email)
    results = db.exec(statement)
    return results.first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt_handler.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    email = payload.get("sub")
    if email is None:
        raise credentials_exception
    statement = select(models.User).where(models.User.email == email)
    results = db.exec(statement)
    user = results.first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/users/me", response_model=models.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user