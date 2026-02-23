import enum
from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, Text, func, Table, ForeignKey, Index
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
    likes_notifications = Column(Boolean, default=False)
    comments_notifications = Column(Boolean, default=False)
    closed = Column(Boolean, default=False)
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    authorId = Column(Integer, ForeignKey("users.id"), nullable=False)
    location = Column(String, nullable=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    createdAt = Column(DateTime, default=datetime.utcnow)
    images = Column(ARRAY(String), nullable=True) 
    tags = Column(ARRAY(String), nullable=True)
    
    author = relationship("User", back_populates="posts")
    
    # Индексы
    __table_args__ = (
        Index('ix_posts_authorId', 'authorId'),
        Index('ix_posts_createdAt', 'createdAt'),
    )