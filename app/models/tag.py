from sqlalchemy import Column, Integer, String, DateTime, Table, func, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

project_tags = Table(
    "project_tags",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    projects = relationship(
        "Project",
        secondary=project_tags,
        back_populates="tags"
    )