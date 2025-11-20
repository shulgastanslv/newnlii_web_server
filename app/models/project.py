from datetime import datetime
from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, Table, Text, func, ForeignKey, inspect
from app.db.base import Base
from sqlalchemy.orm import relationship, backref

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="User")
    description = Column(Text, nullable=False, default="No description")
    budget = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    crypto_type = Column(Integer, nullable=False, default=0)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    is_favorite = Column(Boolean, default=False)
    features = Column(Text, nullable=True) 
    estimated_duration = Column(String, nullable=True)
    likes_count = Column(Integer, default=0, nullable=False)
    visible = Column(Boolean, default=True, nullable=False)
    moderation_status = Column(String, default="pending", nullable=False)
    views_count = Column(Integer, default=0, nullable=False)
    short_description = Column(String, nullable=True) 
    external_links = Column(Text, nullable=True)
    video_url = Column(String, nullable=True)
    packages = Column(Text, nullable=True)
    skills = relationship(
        "Skill",
        secondary="project_skills",
        back_populates="projects"
    )
    images = relationship(
    "ProjectImage",
    back_populates="project",
    cascade="all, delete-orphan",
    order_by="ProjectImage.order"
    )
    tags = relationship(
        "Tag",
        secondary="project_tags",
        back_populates="projects"
    )
    owner = relationship("User", back_populates="projects")
    category = relationship("Category", backref="projects")
    reviews = relationship("ProjectReview", backref="project")
    favorites = relationship("Favorite", backref="project", cascade="all, delete-orphan")

    @classmethod
    def from_dict(cls, data):
        return cls(**data)