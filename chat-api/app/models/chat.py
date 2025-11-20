from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    
    user1 = relationship("User", foreign_keys=[user1_id], backref="chats_as_user1")
    user2 = relationship("User", foreign_keys=[user2_id], backref="chats_as_user2")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    is_read = Column(Integer, default=0, nullable=False)  # 0 - не прочитано, 1 - прочитано
    
    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", backref="sent_messages")

