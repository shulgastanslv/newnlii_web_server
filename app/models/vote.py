import enum
from sqlalchemy import Boolean, Column, Enum, Float, Integer, String, DateTime, Text, UniqueConstraint, func, Table, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from app.db.base import Base
from datetime import datetime

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

    user = relationship("User", back_populates="votes") 
    post = relationship("Post", back_populates="votes")