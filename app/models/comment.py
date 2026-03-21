from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Index, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, index=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime, nullable=True, index=True)

    __table_args__ = (
        Index("ix_comments_post_created", "post_id", "created_at"),
        Index("ix_comments_author_created", "author_id", "created_at"),
        Index("ix_comments_post_author", "post_id", "author_id"),
        Index("ix_comments_parent_created", "parent_id", "created_at"),
        Index("ix_comments_created_deleted", "created_at", "is_deleted"),
    )

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent = relationship(
        "Comment",
        remote_side=[id],
        back_populates="replies",
    )
    replies = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
