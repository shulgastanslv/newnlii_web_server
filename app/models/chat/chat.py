from sqlalchemy import Boolean, Column, Integer, ForeignKey, DateTime, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)

    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    last_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])

    messages = relationship(
        "Message",
        back_populates="chat",
        foreign_keys="Message.chat_id",
        cascade="all, delete-orphan",
    )

    last_message = relationship(
        "Message",
        foreign_keys=[last_message_id],
        post_update=True,
    )
 
class MessageType(enum.Enum):
    text = "text"
    image = "image"
    order = "order"
    request = "request"


from sqlalchemy import Enum

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    type = Column(Enum(MessageType, name="message_type"),
                  default=MessageType.text,
                  nullable=False)

    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    chat = relationship(
        "Chat",
        back_populates="messages",
        foreign_keys=[chat_id],
    )

    sender = relationship("User")
