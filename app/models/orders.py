from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.db.base import Base

class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    budget = Column(Integer, nullable=False)
    deadline = Column(DateTime, nullable=False)

