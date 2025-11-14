from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, Text, func
from app.db.base import Base
from sqlalchemy.orm import relationship, backref

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    level = Column(Integer, nullable=False, default=0)
    role = Column(String, nullable=False, default="developer")
    status = Column(String, nullable=False, default="active")
    region = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
        
    completed_orders = Column(Integer, nullable=False,default=0)
    repeat_orders = Column(Integer,nullable=False, default=0)
    rating = Column(Float, nullable=False, default=0.0)
    verified = Column(Boolean, default=False)
    
    user_reviews = relationship('ProjectReview', backref='user')
    skills = relationship("Skill", secondary="user_skills", back_populates="users")
    specializations = relationship("Specialization", secondary="user_specializations", back_populates="users")
    projects = relationship("Project", back_populates="owner")