from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)

    push_notifications = Column(Boolean, default=False)
    save_notifications = Column(Boolean, default=False)
    verify = Column(Boolean, default=False)
    google_id = Column(String, unique=True, index=True, nullable=True)
    is_google_verified = Column(Boolean, default=False)
    google_email_verified = Column(Boolean, default=False)
    is_google = Column(Boolean, default=False)

    comments_notifications = Column(Boolean, default=False)
    closed = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    saved_posts = relationship("SavedPost", back_populates="user")
    role = Column(String(20), default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    notifications = relationship(
        "Notification",
        foreign_keys="Notification.user_id",
        back_populates="user",
    )
    acted_notifications = relationship(
        "Notification",
        foreign_keys="Notification.actor_id",
        back_populates="actor",
    )

    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan",
    )
    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )

    votes = relationship("Vote", back_populates="user")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    post_views = relationship("View", back_populates="user")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("google_id", name="uq_users_google_id"),
    )


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    following_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")

    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="uq_follows_follower_following"),
        Index("ix_follows_follower", "follower_id"),
        Index("ix_follows_following", "following_id"),
        Index("ix_follows_created", "created_at"),
    )
