from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.chat.chat import Chat, Message
from app.models.user import User
from app.schemas.chat.chat import ChatCreate, MessageCreate, MessageOut, ChatListOut
from app.schemas.user import UserOut
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime


def create_chat(db: Session, chat: ChatCreate):
    existing_chat = get_chat_by_users(db, chat.user1_id, chat.user2_id)
    if existing_chat:
        return existing_chat
    
    db_chat = Chat(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_chat_by_id(db: Session, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


def get_chat_by_users(db: Session, user1_id: int, user2_id: int):
    return db.query(Chat).filter(
        or_(
            and_(Chat.user1_id == user1_id, Chat.user2_id == user2_id),
            and_(Chat.user1_id == user2_id, Chat.user2_id == user1_id)
        )
    ).first()


def get_user_chats(db: Session, user_id: int) -> List[ChatListOut]:
    chats = db.query(Chat).filter(
        or_(Chat.user1_id == user_id, Chat.user2_id == user_id)
    ).all()
    
    result = []
    for chat in chats:
        last_message = db.query(Message).filter(
            Message.chat_id == chat.id
        ).order_by(Message.created_at.desc()).first()
        
        unread_count = db.query(Message).filter(
            Message.chat_id == chat.id,
            Message.sender_id != user_id,
            Message.is_read == 0
        ).count()
        
        other_user_id = chat.user2_id if chat.user1_id == user_id else chat.user1_id
        other_user = db.query(User).filter(User.id == other_user_id).first()
        
        last_message_out = MessageOut.model_validate(last_message) if last_message else None
        other_user_out = UserOut.model_validate(other_user) if other_user else None
        
        result.append(ChatListOut(
            id=chat.id,
            user1_id=chat.user1_id,
            user2_id=chat.user2_id,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
            last_message=last_message_out,
            unread_count=unread_count,
            other_user=other_user_out
        ))
    
    return result


def create_message(db: Session, message: MessageCreate, sender_id: int):
    chat = get_chat_by_id(db, message.chat_id)
    chat.updated_at = datetime.now()
    
    db_message = Message(
        chat_id=message.chat_id,
        sender_id=sender_id,
        content=message.content,
        is_read=0
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_chat_messages(db: Session, chat_id: int, limit: int = 100, offset: int = 0):
    return db.query(Message).filter(
        Message.chat_id == chat_id
    ).order_by(Message.created_at.desc()).offset(offset).limit(limit).all()


def mark_messages_as_read(db: Session, chat_id: int, user_id: int):
    db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.sender_id != user_id,
        Message.is_read == 0
    ).update({"is_read": 1})
    db.commit()
    return {"status": "messages marked as read"}

