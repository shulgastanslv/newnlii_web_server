from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    developer_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # исполнитель может быть назначен позже
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.pending, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    budget = Column(Integer, nullable=True)
    deadline = Column(DateTime, nullable=True)
    project = relationship("Project", backref="orders")
    client = relationship("User", foreign_keys=[client_id], backref="client_orders")
    developer = relationship("User", foreign_keys=[developer_id], backref="developer_orders")
