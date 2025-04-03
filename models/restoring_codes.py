from sqlalchemy import Column, Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class RestoringCode(Base):
    __tablename__ = "restoring_codes"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    code = Column(Integer, default=None)

