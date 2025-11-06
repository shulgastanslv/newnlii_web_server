from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="developer")
    created_at = Column(DateTime, server_default=func.now())
