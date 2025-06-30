from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv(".env")  # Charge les variables d’environnement

DATABASE_URL = os.getenv("MYSQL_URL")  # Doit correspondre au nom exact dans .env

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
