from sqlalchemy import Column, Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    # M:1
    tasks = relationship("Task", back_populates="project")

