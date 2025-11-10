from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship, backref

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String, nullable=False)
    budget = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", backref="projects")
