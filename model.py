from sqlalchemy import Column, Integer, String
from database import Base  # Correct car fichier s'appelle `model.py` et pas `models.py`

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100))
