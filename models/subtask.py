from sqlalchemy import Column, Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    perfomer_id = Column(Integer, ForeignKey("users.id"))
    deadline = Column(Date)
    priority = Column(Integer)
    color = Column(String)
    description = Column(String)
    #attached_files = Column(Integer, ForeignKey("attaches.id"))

    # M:1
    author = relationship("User", foreign_keys=[author_id], back_populates="authored_subtasks")
    performer = relationship("User", foreign_keys=[perfomer_id], back_populates="performed_subtasks")
    task = relationship("Task", back_populates="subtasks")