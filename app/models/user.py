from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base
from sqlalchemy.orm import relationship, backref

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    level = Column(Integer, nullable=False, default=0)
    role = Column(String, nullable=False, default="developer")
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    skills = relationship("Skill", secondary="user_skills", back_populates="users")
    specializations = relationship("Specialization", secondary="user_specializations", back_populates="users")