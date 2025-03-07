from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    hashed_password = Column(String)

    # 1:M
    tasks = relationship("Task", back_populates="user")
    categories = relationship("Category", back_populates="user")