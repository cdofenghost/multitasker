from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    icon = Column(String)
    hashed_password = Column(String)

    # 1:M
    authored_tasks = relationship("Task", foreign_keys='Task.author_id', back_populates="author", cascade="all, delete")
    performed_tasks = relationship("Task", foreign_keys='Task.performer_id', back_populates="performer", cascade="all, delete")

    authored_subtasks = relationship("Subtask", foreign_keys='Subtask.author_id', back_populates="author", cascade="all, delete")
    performed_subtasks = relationship("Subtask", foreign_keys='Subtask.performer_id', back_populates="performer", cascade="all, delete")

    categories = relationship("Category", back_populates="user", cascade="all, delete")

# class AccessToken(Base):
#     __tablename__ = 'refresh_tokens'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     token = Column(String(100), unique=True, nullable=False)
#     expires_at = Column(DateTime, nullable=False)

#     user = relationship("User", back_populates="refresh_tokens")


# class RevokedToken(Base):
#     __tablename__ = 'revoked_tokens'

#     id = Column(Integer, primary_key=True, index=True)
#     token = Column(String(100), unique=True, nullable=False)
#     revoked_at = Column(DateTime, nullable=False)
