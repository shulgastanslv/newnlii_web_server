import enum
from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, Text, func, Enum
from app.db.base import Base
from sqlalchemy.orm import relationship, backref


from sqlalchemy import Enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
   