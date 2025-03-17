from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    avatar = Column(String)
    hashed_password = Column(String)

    # 1:M
    authored_tasks = relationship("Task", foreign_keys='Task.author_id', back_populates="author")
    performed_tasks = relationship("Task", foreign_keys='Task.performer_id', back_populates="performer")

    authored_subtasks = relationship("Subtask", foreign_keys='Subtask.author_id', back_populates="author")
    performed_subtasks = relationship("Subtask", foreign_keys='Subtask.performer_id', back_populates="performer")

    categories = relationship("Category", back_populates="user")
