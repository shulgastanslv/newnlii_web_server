from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class ProjectReview(Base):
    __tablename__ = "project_reviews"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float, nullable=False)
    text = Column(Text, default="")
    created_at = Column(DateTime, default=func.now())