from sqlalchemy import Column, Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"))
    perfomer_id = Column(Integer, ForeignKey("users.id"))
    deadline = Column(Date)
    priority = Column(Integer)
    color = Column(String)
    description = Column(String)
    #attached_files = Column(Integer, ForeignKey("attaches.id"))

    # M:1
    user = relationship("User", back_populates="tasks")
    # attach = relationship("Attach", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")

    # 1:M
    subtasks = relationship("Subtask", back_populates="task")