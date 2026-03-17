import enum
from sqlalchemy import Boolean, Column, Enum, Float, Integer, String, DateTime, Text, func, Table, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from app.db.base import Base
from datetime import datetime

class NotificationType(str, enum.Enum):
    COMMENT = "comment"
    SAVE = "save"
    FOLLOW = "follow"
    MENTION = "mention"
    TAG = "tag"
    SYSTEM = "system"
    

class NotificationStatus(str, enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"
    
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)
    actor_id = Column(Integer, ForeignKey("users.id", ondelete='SET NULL'), nullable=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), nullable=True, index=True)
    type = Column(Enum(NotificationType), nullable=False, index=True) 
    status = Column(Enum(NotificationStatus), default=NotificationStatus.UNREAD, nullable=False, index=True) 
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    read_at = Column(DateTime, nullable=True, index=True)
    expires_at = Column(DateTime, nullable=True, index=True)
    
    __table_args__ = (
        Index('ix_notifications_user_status_created', 'user_id', 'status', 'created_at'),
        Index('ix_notifications_user_type_created', 'user_id', 'type', 'created_at'),
        Index('ix_notifications_actor_created', 'actor_id', 'created_at'),
        Index('ix_notifications_expires_unread', 'expires_at', 'status'),
    )
    
    user = relationship("User", foreign_keys=[user_id], back_populates="notifications")
    actor = relationship("User", foreign_keys=[actor_id], backref="acted_notifications")
    post = relationship("Post", back_populates="notifications")