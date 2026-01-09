from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from app.models.chat.chat import Chat, Message
from app.models.user import User
from app.schemas.chat.chat import ChatCreate, MessageCreate, MessageOut, ChatListOut
from app.schemas.user import UserOut
from fastapi import HTTPException
from typing import List
from datetime import datetime

def create_chat(db: Session, chat: ChatCreate):
    user1, user2 = sorted([chat.user1_id, chat.user2_id])

    existing_chat = get_chat_by_users(db, user1, user2)
    if existing_chat:
        return existing_chat

    db_chat = Chat(user1_id=user1, user2_id=user2)
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
    user1, user2 = sorted([user1_id, user2_id])
    return db.query(Chat).filter(
        Chat.user1_id == user1,
        Chat.user2_id == user2
    ).first()

def get_user_chats(db: Session, user_id: int) -> List[ChatListOut]:
    chats = (
        db.query(Chat)
        .filter(or_(Chat.user1_id == user_id, Chat.user2_id == user_id))
        .order_by(Chat.updated_at.desc())
        .all()
    )

    result = []
    for chat in chats:
        other_user_id = (
            chat.user2_id if chat.user1_id == user_id else chat.user1_id
        )

        unread_count = (
            db.query(Message)
            .filter(
                Message.chat_id == chat.id,
                Message.sender_id != user_id,
                Message.is_read.is_(False)
            )
            .count()
        )

        result.append(ChatListOut(
            id=chat.id,
            user1_id=chat.user1_id,
            user2_id=chat.user2_id,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
            last_message=(
                MessageOut.model_validate(chat.last_message)
                if chat.last_message else None
            ),
            unread_count=unread_count,
            other_user=UserOut.model_validate(
                chat.user1 if chat.user2_id == user_id else chat.user2
            )
        ))

    return result


def create_message(db: Session, message: MessageCreate, sender_id: int):
    chat = get_chat_by_id(db, message.chat_id)

    db_message = Message(
        chat_id=chat.id,
        sender_id=sender_id,
        content=message.content,
        type=message.type,
        is_read=False,
    )

    db.add(db_message)
    db.flush()  # 🔥

    chat.last_message_id = db_message.id 
    chat.updated_at = func.now()

    db.commit()
    db.refresh(db_message)
    return db_message

def get_chat_messages(
    db: Session,
    chat_id: int,
    limit: int = 100,
    offset: int = 0
):
    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def mark_messages_as_read(db: Session, chat_id: int, user_id: int):
    db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.sender_id != user_id,
        Message.is_read.is_(False)
    ).update(
        {"is_read": True},
        synchronize_session=False
    )
    db.commit()
    return {"status": "ok"}
