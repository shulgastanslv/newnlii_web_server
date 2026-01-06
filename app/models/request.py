import enum
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, DateTime, Text, func, Enum
from app.db.base import Base
from sqlalchemy.orm import relationship, backref

class RequestStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    none = "none"

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    developer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(RequestStatus, name="request_status_enum"), default=RequestStatus.none, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    project = relationship("Project", backref="requests")
    client = relationship("User", foreign_keys=[client_id], backref="client_requests")
    developer = relationship("User", foreign_keys=[developer_id], backref="developer_requests")



  