from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from ..database import Base

# Посмотреть, как передавать файлы в БД

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    path = Column(String, unique=True)
