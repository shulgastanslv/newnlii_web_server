from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, DateTime, Table, Text, UniqueConstraint, Index, ARRAY
from sqlalchemy.dialects.postgresql import ARRAY as PgARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import enum


class PostStatus(str, enum.Enum):
    SENT = "sent"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    UNSENT = "unsent"


post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False),
    Index("ix_post_tags_post_id", "post_id"),
    Index("ix_post_tags_tag_id", "tag_id"),
    Index("ix_post_tags_created_at", "created_at"),
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
    author_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    ai_origin = Column(Text, nullable=True)
    links = Column(PgARRAY(String), nullable=True)
    saved_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    images = Column(PgARRAY(String), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime, nullable=True, index=True)
    is_reply = Column(Boolean, default=False, nullable=False, index=True)

    __table_args__ = (
        Index("ix_posts_author_created", "author_id", "created_at"),
        Index("ix_posts_status_published", "status", "published"),
        Index("ix_posts_category_created", "category", "created_at"),
        Index("ix_posts_saved_count_created", "saved_count", "created_at"),
        Index("ix_posts_created_deleted", "created_at", "is_deleted"),
        Index("ix_posts_author_status", "author_id", "status"),
    )

    author = relationship("User", foreign_keys=[author_id], back_populates="posts")
    saved_by = relationship("SavedPost", back_populates="post", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")
    views = relationship("View", back_populates="post", cascade="all, delete-orphan")


class SavedPost(Base):
    __tablename__ = "saved_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    saved_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_saved_post_user_post"),
        Index("ix_saved_posts_user_saved", "user_id", "saved_at"),
        Index("ix_saved_posts_post_saved", "post_id", "saved_at"),
    )

    user = relationship("User", back_populates="saved_posts")
    post = relationship("Post", back_populates="saved_by")


class View(Base):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    viewed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    session_id = Column(String(255), nullable=True, index=True)

    __table_args__ = (
        Index("ix_views_post_user", "post_id", "user_id"),
        Index("ix_views_post_viewed", "post_id", "viewed_at"),
        Index("ix_views_user_viewed", "user_id", "viewed_at"),
    )

    post = relationship("Post", back_populates="views")
    user = relationship("User", back_populates="post_views")
