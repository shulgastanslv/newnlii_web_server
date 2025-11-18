from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, Table, Text, func, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship, backref

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="User")
    image_url = Column(String, nullable=False, default="https://i.sstatic.net/34AD2.jpg")
    description = Column(Text, nullable=False, default="No description")
    budget = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    crypto_type = Column(Integer, nullable=False, default=0)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    is_favorite = Column(Boolean, default=False)
    
    visible = Column(Boolean, default=True, nullable=False)
    moderation_status = Column(String, default="pending", nullable=False)
    views_count = Column(Integer, default=0, nullable=False)

    external_links = Column(Text, nullable=True)

    skills = relationship(
        "Skill",
        secondary="project_skills",
        back_populates="projects"
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