import enum
from sqlalchemy import Boolean, Column, Enum, Float, Integer, String, DateTime, Text, UniqueConstraint, func, Table, ForeignKey, Index
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class PostStatus(str, enum.Enum):
    SENT = "sent"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    UNSENT = "unsent"

post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False),
    Index('ix_post_tags_post_id', 'post_id'),
    Index('ix_post_tags_tag_id', 'tag_id'),
    Index('ix_post_tags_created_at', 'created_at'),
)

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    slug = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
    
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    status = Column(Enum(PostStatus), default=PostStatus.SENT, nullable=False, index=True) 
    category = Column(String(50), nullable=True, server_default="general")
    author_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)    
    benefit = Column(Text, nullable=True)
    views = Column(Integer, default=0, nullable=False, index=True)
    aiOrigin = Column(Text, nullable=True)
    linkUrl = Column(Text, nullable=True)
    saved_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)  
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True) 
    images = Column(ARRAY(String), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True) 
    deleted_at = Column(DateTime, nullable=True, index=True)  
    is_reply = Column(Boolean, default=False, nullable=False, index=True) 

    __table_args__ = (
        Index('ix_posts_author_created', 'author_id', 'created_at'),
        Index('ix_posts_status_published', 'status', 'published'),
        Index('ix_posts_category_created', 'category', 'created_at'),
        Index('ix_posts_views_created', 'views', 'created_at'),
        Index('ix_posts_saved_count_created', 'saved_count', 'created_at'),
        Index('ix_posts_created_deleted', 'created_at', 'is_deleted'),
        Index('ix_posts_author_status', 'author_id', 'status'),
    )

    author = relationship("User", foreign_keys=[author_id], back_populates="posts")
    saved_by = relationship("SavedPost", back_populates="post", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")

class SavedPost(Base):
    __tablename__ = "saved_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), nullable=False, index=True)
    saved_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_saved_post_user_post"),
        Index('ix_saved_posts_user_saved', 'user_id', 'saved_at'),
        Index('ix_saved_posts_post_saved', 'post_id', 'saved_at'),
    )
    
    user = relationship("User", back_populates="saved_posts")
    post = relationship("Post", back_populates="saved_by")
   
