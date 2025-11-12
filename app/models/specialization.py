from sqlalchemy import Column, Integer, String, DateTime, Table, func, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship, backref

user_specializations = Table(
    "user_specializations",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("specialization_id", Integer, ForeignKey("specializations.id", ondelete="CASCADE"))
)

class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", secondary=user_specializations, back_populates="specializations")