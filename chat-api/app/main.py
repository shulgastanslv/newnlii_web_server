## v0.2

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from typing import List
from pydantic import BaseModel
import logging
import traceback

SQLALCHEMY_DATABASE_URL = "sqlite:///./chat.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)

    sent_chats = relationship("Chat", back_populates="sender", foreign_keys="Chat.sender_id")
    received_chats = relationship("Chat", back_populates="receiver", foreign_keys="Chat.receiver_id")
    sent_messages = relationship("Message", back_populates="sender")

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sender = relationship("User", back_populates="sent_chats", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_chats", foreign_keys=[receiver_id])
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    content = Column(Text, nullable=False)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    content: str

class ChatCreate(BaseModel):
    sender_id: int
    receiver_id: int

@app.post("/chats", response_model=int)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    if chat.sender_id == chat.receiver_id:
        raise ValueError("sender_id and receiver_id cannot be the same")

    existing_chat = db.query(Chat).filter(
        ((Chat.sender_id == chat.sender_id) & (Chat.receiver_id == chat.receiver_id)) |
        ((Chat.sender_id == chat.receiver_id) & (Chat.receiver_id == chat.sender_id))
    ).first()
    if existing_chat:
        return existing_chat.id
    db_chat = Chat(id =chat.receiver_id, sender_id=chat.sender_id, receiver_id=chat.receiver_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@app.post("/messages", response_model=int)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == message.chat_id).first()
    if not chat:
        return {"error": "Chat not found"}, 404
    db_message = Message(chat_id=message.chat_id, sender_id=message.sender_id, content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message.id

@app.get("/chat_info/{chat_id}")
def get_chat_info(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        return {"error": "Chat not found"}, 404
    return {"id": chat.id, "sender_id": chat.sender_id, "receiver_id": chat.receiver_id}

@app.get("/chats/{user_id}")
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    chats = db.query(Chat).filter((Chat.sender_id == user_id) | (Chat.receiver_id == user_id)).all()
    result = []
    for c in chats:
        result.append({"id": c.id, "sender_id": c.sender_id, "receiver_id": c.receiver_id})
    return result

@app.get("/messages/{chat_id}")
def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.chat_id == chat_id).all()
    return [{"id": m.id, "chat_id": m.chat_id, "sender_id": m.sender_id, "content": m.content} for m in messages]

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_message(self, user_id: int, message: dict):
        connections = self.active_connections.get(user_id, [])
        to_remove = []
        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:  # WebSocketDisconnect or RuntimeError on closed socket
                to_remove.append(ws)
        # Remove disconnected websockets
        for ws in to_remove:
            self.disconnect(user_id, ws)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await manager.connect(user_id, websocket)
    print(manager.active_connections)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(
            id=user_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    try:
        while True:
            data = await websocket.receive_json()
            receiver_id = data.get("receiver_id")
            content = data.get("content")

            chat = db.query(Chat).filter(
            ((Chat.sender_id == user_id) & (Chat.receiver_id == receiver_id)) |
            ((Chat.sender_id == receiver_id) & (Chat.receiver_id == user_id))
        ).first()
            if not chat:
                chat = Chat(sender_id=min(user_id, receiver_id), receiver_id=max(user_id, receiver_id))
                db.add(chat)
                db.commit()
                db.refresh(chat)

            chat_id = chat.id
            print(chat.sender_id)
            message = Message(chat_id=chat_id, sender_id=user_id, content=content)
            db.add(message)
            db.commit()
            db.refresh(message)

            await manager.send_message(chat.sender_id, {
                "chat_id": chat_id,
                "sender_id": user_id,
                "content": content
            })
            await manager.send_message(chat.receiver_id, {
                "chat_id": chat_id,
                "sender_id": user_id,
                "content": content
            })

    except WebSocketDisconnect:
        logging.error(f"WebSocket disconnected for user {user_id}")
        manager.disconnect(user_id, websocket)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        traceback.print_exc()


@app.get("/last_messages/{user_id}")
def get_last_messages(user_id: int, db: Session = Depends(get_db)):
    chats = db.query(Chat).filter((Chat.sender_id == user_id) | (Chat.receiver_id == user_id)).all()
    last_messages = []
    for chat in chats:
        last_message = (
            db.query(Message)
            .filter(Message.chat_id == chat.id)
            .order_by(Message.id.desc())
            .first()
        )
        if last_message:
            last_messages.append({
                "chat_id": chat.id,
                "last_message_id": last_message.id,
                "sender_id": last_message.sender_id,
                "content": last_message.content
            })
    return last_messages

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id} for u in users]


@app.get("/user_messages/{user_id}")
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.sender_id == user_id).all()
    return [{"id": m.id, "chat_id": m.chat_id, "content": m.content} for m in messages]


@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return {"detail": "Message deleted"}