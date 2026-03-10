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
    status = Column(Enum(PostStatus), default=PostStatus.SENT, nullable=False, index=True)  # Добавлен индекс
    category = Column(String(50), nullable=True, server_default="general")
    author_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)  # Добавлен индекс    
    benefit = Column(Text, nullable=True)
    views = Column(Integer, default=0, nullable=False, index=True)
    aiOrigin = Column(Text, nullable=True)
    linkUrl = Column(Text, nullable=True)
    saved_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)  # Добавлен индекс
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)  # Добавлен индекс
    images = Column(ARRAY(String), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # Добавлен индекс
    deleted_at = Column(DateTime, nullable=True, index=True)  # Добавлен индекс
    is_reply = Column(Boolean, default=False, nullable=False, index=True)  # Добавлен индекс

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
    actor_id = Column(Integer, ForeignKey("users.id", ondelete='SET NULL'), nullable=True, index=True)  # Добавлен индекс
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), nullable=True, index=True)
    type = Column(Enum(NotificationType), nullable=False, index=True)  # Добавлен индекс
    status = Column(Enum(NotificationStatus), default=NotificationStatus.UNREAD, nullable=False, index=True)  # Добавлен индекс
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    read_at = Column(DateTime, nullable=True, index=True)  # Добавлен индекс
    expires_at = Column(DateTime, nullable=True, index=True)  # Добавлен индекс
    
    __table_args__ = (
        Index('ix_notifications_user_status_created', 'user_id', 'status', 'created_at'),
        Index('ix_notifications_user_type_created', 'user_id', 'type', 'created_at'),
        Index('ix_notifications_actor_created', 'actor_id', 'created_at'),
        Index('ix_notifications_expires_unread', 'expires_at', 'status'),
    )
    
    user = relationship("User", foreign_keys=[user_id], back_populates="notifications")
    actor = relationship("User", foreign_keys=[actor_id], backref="acted_notifications")
    post = relationship("Post", back_populates="notifications")
   
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)  # Добавлен индекс
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  # Добавлен индекс
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)  # Добавлен индекс
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)  # Добавлен индекс
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)  # Добавлен индекс
    deleted_at = Column(DateTime, nullable=True, index=True)  # Добавлен индекс

    __table_args__ = (
        Index('ix_comments_post_created', 'post_id', 'created_at'),
        Index('ix_comments_author_created', 'author_id', 'created_at'),
        Index('ix_comments_post_author', 'post_id', 'author_id'),
        Index('ix_comments_created_deleted', 'created_at', 'is_deleted'),
    )

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)  # Индекс уже есть в table_args
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)  # Индекс уже есть в table_args
    value = Column(Integer, nullable=False, default=1, index=True)  # Добавлен индекс
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)  # Добавлен индекс
    
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_vote_user_post"),
        Index("ix_votes_post_id", "post_id"),
        Index("ix_votes_user_id", "user_id"),
        Index('ix_votes_post_value', 'post_id', 'value'),  # Добавлен составной индекс
        Index('ix_votes_user_created', 'user_id', 'created_at'),  # Добавлен составной индекс
        Index('ix_votes_post_created', 'post_id', 'created_at'),  # Добавлен составной индекс
    )

    user = relationship("User", backref="votes")
    post = relationship("Post", backref="votes")