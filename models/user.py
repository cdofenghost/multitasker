from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    hashed_password = Column(String)