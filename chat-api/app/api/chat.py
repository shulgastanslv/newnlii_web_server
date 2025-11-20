from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from app.api.deps import get_db
from app.schemas.chat import ChatCreate, ChatOut, MessageCreate, MessageOut, ChatListOut, WebSocketMessage
from app.crud import chat as crud_chat
from app.crud import user as crud_user

router = APIRouter()

# Хранилище активных WebSocket соединений
# Структура: {chat_id: {user_id: websocket}}
active_connections: dict[int, dict[int, WebSocket]] = {}


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int, user_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = {}
        self.active_connections[chat_id][user_id] = websocket

    def disconnect(self, chat_id: int, user_id: int):
        if chat_id in self.active_connections:
            if user_id in self.active_connections[chat_id]:
                del self.active_connections[chat_id][user_id]
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def send_personal_message(self, message: dict, chat_id: int, user_id: int):
        if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
            websocket = self.active_connections[chat_id][user_id]
            await websocket.send_json(message)

    async def broadcast_to_chat(self, message: dict, chat_id: int, exclude_user_id: int = None):
        if chat_id in self.active_connections:
            for user_id, websocket in self.active_connections[chat_id].items():
                if user_id != exclude_user_id:
                    await websocket.send_json(message)


manager = ConnectionManager()


@router.post("/chats/", response_model=ChatOut)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    """Создать новый чат между двумя пользователями"""
    return crud_chat.create_chat(db, chat)


@router.get("/chats/{chat_id}", response_model=ChatOut)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    """Получить чат по ID"""
    return crud_chat.get_chat_by_id(db, chat_id)


@router.get("/chats/user/{user_id}", response_model=List[dict])
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    """Получить все чаты пользователя"""
    return crud_chat.get_user_chats(db, user_id)


@router.get("/chats/{chat_id}/messages", response_model=List[MessageOut])
def get_chat_messages(
    chat_id: int,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Получить сообщения чата"""
    messages = crud_chat.get_chat_messages(db, chat_id, limit, offset)
    return list(reversed(messages))  # Возвращаем в хронологическом порядке


@router.post("/chats/{chat_id}/read")
def mark_as_read(chat_id: int, user_id: int, db: Session = Depends(get_db)):
    """Отметить сообщения как прочитанные"""
    return crud_chat.mark_messages_as_read(db, chat_id, user_id)


@router.websocket("/ws/{chat_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, user_id: int):
    """
    WebSocket endpoint для чата
    Подключение: ws://localhost:8000/ws/{chat_id}/{user_id}
    """
    await manager.connect(websocket, chat_id, user_id)
    
    # Проверяем существование пользователя и чата
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        user = crud_user.get_user_by_id(db, user_id)
        chat = crud_chat.get_chat_by_id(db, chat_id)
        
        # Проверяем, что пользователь является участником чата
        if chat.user1_id != user_id and chat.user2_id != user_id:
            await websocket.close(code=1008, reason="User is not a participant of this chat")
            return
    except HTTPException:
        await websocket.close(code=1008, reason="Chat or user not found")
        return
    finally:
        db.close()
    
    try:
        # Отправляем уведомление о подключении другим участникам
        await manager.broadcast_to_chat(
            {
                "type": "user_connected",
                "user_id": user_id,
                "chat_id": chat_id
            },
            chat_id,
            exclude_user_id=user_id
        )
        
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Обрабатываем разные типы сообщений
            if message_data.get("type") == "message":
                # Создаем сообщение в БД
                db = SessionLocal()
                try:
                    message_create = MessageCreate(
                        chat_id=chat_id,
                        content=message_data.get("content", "")
                    )
                    message = crud_chat.create_message(db, message_create, user_id)
                    
                    # Отправляем сообщение всем участникам чата
                    message_dict = {
                        "type": "message",
                        "id": message.id,
                        "chat_id": chat_id,
                        "sender_id": user_id,
                        "content": message.content,
                        "created_at": message.created_at.isoformat(),
                        "is_read": message.is_read
                    }
                    await manager.broadcast_to_chat(message_dict, chat_id)
                finally:
                    db.close()
                    
            elif message_data.get("type") == "typing":
                # Отправляем уведомление о наборе текста
                await manager.broadcast_to_chat(
                    {
                        "type": "typing",
                        "user_id": user_id,
                        "chat_id": chat_id
                    },
                    chat_id,
                    exclude_user_id=user_id
                )
                
            elif message_data.get("type") == "read":
                # Отмечаем сообщения как прочитанные
                db = SessionLocal()
                try:
                    crud_chat.mark_messages_as_read(db, chat_id, user_id)
                    await manager.broadcast_to_chat(
                        {
                            "type": "read",
                            "user_id": user_id,
                            "chat_id": chat_id
                        },
                        chat_id,
                        exclude_user_id=user_id
                    )
                finally:
                    db.close()
                    
    except WebSocketDisconnect:
        manager.disconnect(chat_id, user_id)
        # Уведомляем других участников об отключении
        await manager.broadcast_to_chat(
            {
                "type": "user_disconnected",
                "user_id": user_id,
                "chat_id": chat_id
            },
            chat_id
        )

