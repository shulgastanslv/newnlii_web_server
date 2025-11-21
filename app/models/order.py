from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Text, func, Float
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class Status(enum.Enum):
    open = "open"
    closed = "closed"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    paid = "paid"
    
from sqlalchemy import Enum

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    developer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(Status, name="status_enum"), default=Status.open, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    budget = Column(Float, nullable=True)
    deadline = Column(DateTime, nullable=True)
    git_url = Column(Text, nullable=True)
    project = relationship("Project", backref="orders")
    client = relationship("User", foreign_keys=[client_id], backref="client_orders")
    developer = relationship("User", foreign_keys=[developer_id], backref="developer_orders")
