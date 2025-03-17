from sqlalchemy import Column, Date, ForeignKey, Integer, String, CheckConstraint, ARRAY
from sqlalchemy.orm import relationship
from ..database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


    # 1:M
    projects = relationship("Project", back_populates="category")
    
    # M:1
    user = relationship("User", back_populates="categories")