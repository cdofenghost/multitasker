from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base

# Посмотреть, как передавать файлы в БД

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    revoked_at = Column(DateTime)