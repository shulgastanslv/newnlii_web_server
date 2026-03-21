from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    value = Column(Integer, nullable=False, default=1, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_vote_user_post"),
        Index("ix_votes_post_value", "post_id", "value"),
        Index("ix_votes_user_created", "user_id", "created_at"),
        Index("ix_votes_post_created", "post_id", "created_at"),
    )

    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")
