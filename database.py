from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase): 
    pass

DATABASE_URL = "postgresql://user:password@localhost:5432/db"

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
