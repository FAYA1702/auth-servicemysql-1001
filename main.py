from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from model import User  # Assure-toi que le fichier est bien model.py
from schemas import UserCreate, Token, UserLogin

import os
from dotenv import load_dotenv

from auth_utils import (
    register_user,
    login_user,
   
)

# Charger les variables d’environnement
load_dotenv(".env")

# Créer les tables si elles n’existent pas
Base.metadata.create_all(bind=engine)

# Initialiser l’app FastAPI
app = FastAPI()

# Middleware CORS (pour éviter les erreurs avec le frontend local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dépendance pour accéder à la base
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Route d’inscription
@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#  Route de connexion
@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        return login_user(user, db)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
