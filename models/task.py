from sqlalchemy import Column, Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    performer_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    deadline = Column(Date)
    priority = Column(Integer)
    description = Column(String)
    #attached_files = Column(Integer, ForeignKey("attaches.id"))

    # 1:M
    subtasks = relationship("Subtask", back_populates="task")

    # M:1
    author = relationship("User", foreign_keys=[author_id], back_populates="authored_tasks")
    performer = relationship("User", foreign_keys=[performer_id], back_populates="performed_tasks")
    project = relationship("Project", back_populates="tasks")