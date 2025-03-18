from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .utils.secret_data import DATABASE_URL

class Base(DeclarativeBase): 
    pass

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    return engine

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
