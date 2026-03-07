import enum
from sqlalchemy import Boolean, Column, Enum, Float, Integer, String, DateTime, Text, UniqueConstraint, func, Table, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.base import Base
from datetime import datetime, timedelta

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
    


class PostStatus(str, enum.Enum):
    SENT = "sent",
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    UNSENT = "unsent"



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    status = Column(Enum(PostStatus), default=PostStatus.SENT, nullable=False)
    category = Column(String(50), nullable=True, server_default="general")
    author_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    views = Column(Integer, default=0, nullable=False)
    benefit = Column(Text, nullable=True)
    aiOrigin = Column(Text, nullable=True)
    linkUrl = Column(Text, nullable=True)
    saved_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False) 
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    images = Column(ARRAY(String), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    is_reply = Column(Boolean, default=False, nullable=False)
    author = relationship("User", foreign_keys=[author_id], back_populates="posts")
    saved_by = relationship("SavedPost", back_populates="post", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
   

class SavedPost(Base):
    __tablename__ = "saved_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = relationship("User", back_populates="saved_posts")
    post = relationship("Post", back_populates="saved_by")

class NotificationType(str, enum.Enum):
    COMMENT = "comment"
    SAVE = "save"
    FOLLOW = "follow"
    MENTION = "mention"
    TAG = "tag"
    SYSTEM = "system"


class NotificationStatus(str, enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete='SET NULL'), nullable=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), nullable=True)
    type = Column(Enum(NotificationType), nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.UNREAD, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    read_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    user = relationship("User", foreign_keys=[user_id], back_populates="notifications")
    actor = relationship("User", foreign_keys=[actor_id], backref="acted_notifications")
    post = relationship("Post", back_populates="notifications")
   

