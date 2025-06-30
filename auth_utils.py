import os
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import model 
import schemas  

load_dotenv(".env")

SECRET_KEY = os.getenv("JWT_SECRET", "123")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 40))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None)->str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def register_user(user_in: schemas.UserCreate, db: Session):
    existing = db.query(model.User).filter(
        model.User.username == user_in.username | model.User.email == user_in.email
    ).first()
    
    if existing:
        raise ValueError("Username or email already exist")

    user = model.User(
        username = user_in.username,
        email = user_in.email,
        password = get_password_hash(user_in.password)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub":str(user.id)})
    return {"access_token":token, "token_type":"bearer"}

def login_user(user_in: schemas.UserLogin, db: Session):
    user = db.query(model.User).filter(
        model.User.username == user_in.username
    ).first()

    if not user or not verify_password(user_in.password, user.password):
        raise ValueError("Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
