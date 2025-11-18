from sqlalchemy import Column, Integer, String, DateTime, Table, func, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship, backref

user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE"))
)

project_skills = Table(
    "project_skills",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", secondary=user_skills, back_populates="skills")
    projects = relationship(
        "Project",
        secondary=project_skills,
        back_populates="skills"
    )