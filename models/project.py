from sqlalchemy import Column, Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    icon = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))

    # 1:M
    tasks = relationship("Task", cascade="all, delete", back_populates="project")
    
    # M:1
    category = relationship("Category", cascade="all, delete", back_populates="projects")

