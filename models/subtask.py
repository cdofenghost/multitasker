from sqlalchemy import Column, Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    perfomer_id = Column(Integer, ForeignKey("users.id"))
    deadline = Column(Date)
    priority = Column(Integer)
    color = Column(String)
    description = Column(String)
    #attached_files = Column(Integer, ForeignKey("attaches.id"))

    # M:1
    user = relationship("User", back_populates="tasks")
    task = relationship("Task", back_populates="subtasks")
    # attach = relationship("Attach", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")