from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Text, func, Float
from app.db.base import Base

class Keys(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, index=True, nullable=False)
    key = Column(Text, index=True,  nullable=False)