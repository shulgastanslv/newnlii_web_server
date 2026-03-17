import enum
from sqlalchemy import Boolean, CheckConstraint, Column, Float, Integer, String, DateTime, Text, UniqueConstraint, func, Table, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    push_notifications = Column(Boolean, default=False)
    save_notifications = Column(Boolean, default=False)
    verify = Column(Boolean, default=False)
    comments_notifications = Column(Boolean, default=False)
    closed = Column(Boolean, default=False)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    saved_posts = relationship("SavedPost", back_populates="user")
    role = Column(String(20), default="user", nullable=False) 
    is_active = Column(Boolean, default=True, nullable=False)
    notifications = relationship("Notification", foreign_keys="Notification.user_id", back_populates="user", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan"
    )
    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan"
    )
    votes = relationship("Vote", back_populates="user")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    

class Follow(Base):
    __tablename__ = "follows"
    
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")
    