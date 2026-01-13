from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
import json

from app.api.deps import get_db
from app.db.session import SessionLocal
from app.schemas.chat.chat import (
    ChatCreate,
    ChatOut,
    MessageCreate,
    MessageOut,
    ChatListOut,
)
from app.crud.chat import chat as crud_chat
from app.crud.user import get_user_by_id
router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, chat_id: int, user_id: int, ws: WebSocket):
        await ws.accept()
        self.connections.setdefault(chat_id, {})[user_id] = ws

    def disconnect(self, chat_id: int, user_id: int):
        users = self.connections.get(chat_id)
        if not users:
            return
        users.pop(user_id, None)
        if not users:
            self.connections.pop(chat_id, None)

    async def broadcast(self, chat_id: int, data: dict, exclude: int | None = None):
        for uid, ws in list(self.connections.get(chat_id, {}).items()):
            if uid == exclude:
                continue
            try:
                await ws.send_json(data)
            except Exception:
                self.disconnect(chat_id, uid)


manager = ConnectionManager()


@router.post("/chats/", response_model=ChatOut)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    return crud_chat.create_chat(db, chat)

@router.get("/chats/{chat_id}", response_model=ChatOut)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    return crud_chat.get_chat_by_id(db, chat_id)


@router.get("/chats/user/{user_id}", response_model=List[ChatListOut])
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    return crud_chat.get_user_chats(db, user_id)

@router.get("/chats/", response_model=List[ChatListOut])
def get_all_chats_route(db: Session = Depends(get_db)):
    return crud_chat.get_all_chats(db)

@router.get("/chats/{chat_id}/messages", response_model=List[MessageOut])
def get_chat_messages(chat_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    messages = crud_chat.get_chat_messages(db, chat_id, limit, offset)
    return list(reversed(messages))

@router.post("/chats/{chat_id}/read")
def mark_as_read(chat_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud_chat.mark_messages_as_read(db, chat_id, user_id)

@router.websocket("/ws/{chat_id}/{user_id}")
async def websocket_endpoint(ws: WebSocket, chat_id: int, user_id: int):
    db = SessionLocal()
    try:
        chat = crud_chat.get_chat_by_id(db, chat_id)
        if user_id not in (chat.user1_id, chat.user2_id):
            await ws.close(code=1008)
            return
    finally:
        db.close()

    await manager.connect(chat_id, user_id, ws)
    await manager.broadcast(chat_id, {"type": "user_connected", "user_id": user_id}, exclude=user_id)

    try:
        while True:
            data = json.loads(await ws.receive_text())
            msg_type = data.get("type")

            if msg_type == "text":
                db = SessionLocal()
                try:
                    message = crud_chat.create_message(
                        db,
                        MessageCreate(chat_id=chat_id, content=data.get("content", ""), type="text"),
                        sender_id=user_id
                    )
                finally:
                    db.close()
                await manager.broadcast(
                    chat_id,
                    {
                        "type": "text",
                        "id": message.id,
                        "chat_id": chat_id,
                        "sender_id": user_id,
                        "content": message.content,
                        "created_at": message.created_at.isoformat(),
                        "is_read": message.is_read,
                    },
                )
            elif msg_type == "typing":
                await manager.broadcast(chat_id, {"type": "typing", "user_id": user_id}, exclude=user_id)
            elif msg_type == "order":
                db = SessionLocal()
                try:
                    message = crud_chat.create_message(
                        db,
                        MessageCreate(chat_id=chat_id, content=data.get("content", ""), type="order"),
                        sender_id=user_id
                    )
                finally:
                    db.close()
                sender = get_user_by_id(db, user_id)
                await manager.broadcast(
                    chat_id,
                    {
                           "type": message.type,
                            "id": message.id,
                            "chat_id": chat_id,
                            "sender_id": user_id,
                            "sender": {
                                "id": sender.id,
                                "name": sender.name,
                                "image_url": sender.image_url,
                            },
                            "content": message.content,
                            "created_at": message.created_at.isoformat(),
                            "is_read": message.is_read,
                    },
                )

            elif msg_type == "read":
                db = SessionLocal()
                try:
                    crud_chat.mark_messages_as_read(db, chat_id, user_id)
                finally:
                    db.close()

                await manager.broadcast(chat_id, {"type": "read", "user_id": user_id}, exclude=user_id)

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(chat_id, user_id)
        await manager.broadcast(chat_id, {"type": "user_disconnected", "user_id": user_id})