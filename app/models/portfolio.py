from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class PortfolioItem(Base):
    __tablename__ = "portfolio_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title = Column(String(200), nullable=False)
    short_title = Column(String(80), nullable=True)
    short_description = Column(String(160), nullable=True)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String(500), nullable=False)
    aspect_ratio = Column(Float, nullable=True)
    project_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    repo_url = Column(String(500), nullable=True)
    tech_stack = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    category = Column(String(100), index=True, nullable=True)
    role = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    saves_count = Column(Integer, default=0)
    is_public = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    display_priority = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="portfolio_items")
