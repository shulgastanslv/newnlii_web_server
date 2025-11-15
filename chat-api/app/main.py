from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from typing import List
from collections import defaultdict
import json

DATABASE_URL = "sqlite:///./test.db" 
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    messages = relationship("Message", back_populates="sender")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

ws_connections = defaultdict(list)

@app.post("/users/", response_model=dict)
def create_user(name: str = Form(...), db: Session = Depends(get_db)):
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name}

@app.get("/conversation/", response_model=dict)
def get_or_create_conversation(sender_id: int, receiver_id: int, db: Session = Depends(get_db)):
    c = db.query(Conversation).filter(
        or_(
            ((Conversation.sender_id == sender_id) & (Conversation.receiver_id == receiver_id)),
            ((Conversation.sender_id == receiver_id) & (Conversation.receiver_id == sender_id))
        )
    ).first()
    if not c:
        c = Conversation(sender_id=sender_id, receiver_id=receiver_id)
        db.add(c)
        db.commit()
        db.refresh(c)
    return {
        "id": c.id,
        "sender_id": c.sender_id,
        "receiver_id": c.receiver_id,
        "name": f"dialog_{c.id}",
    }

@app.get("/messages/", response_model=List[dict])
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
    print(messages)
    return [{
    "id": m.id,
    "sender_id": m.sender_id,
    "content": m.content,
    "time": m.timestamp.isoformat(),
    "sender": db.query(User).get(m.sender_id).name if db.query(User).get(m.sender_id) else "Unknown"
} for m in messages]

@app.get("/messages/all/", response_model=List[dict])
def get_all_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.timestamp.desc()).offset(skip).limit(limit).all()
    return [{
        "id": m.id,
        "sender": db.query(User).get(m.sender_id).name if m.sender_id else "Unknown",
        "sender_id": m.sender_id,
        "content": m.content,
        "conversation_id": m.conversation_id,
        "time": m.timestamp.isoformat(),
    } for m in messages]

@app.get("/conversations/", response_model=List[dict])
def get_user_conversations(user_id: int, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(
        (Conversation.sender_id == user_id) | (Conversation.receiver_id == user_id)
    ).all()
    return [{
        "id": c.id,
        "sender_id": c.sender_id,
        "receiver_id": c.receiver_id,
        "name": f"dialog_{c.id}",
    } for c in conversations]

@app.websocket("/ws/chat/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: int):
    await websocket.accept()
    ws_connections[conversation_id].append(websocket)
    db = SessionLocal()
    try:
        while True:
            data = await websocket.receive_text()
            obj = json.loads(data)
            sender_id = obj["sender_id"]
            content = obj["content"]

            # сохраняем сообщение
            msg = Message(
                conversation_id=conversation_id,
                sender_id=sender_id,
                content=content
            )
            db.add(msg)
            db.commit()
            db.refresh(msg)

            user_obj = db.query(User).get(sender_id)
            sender_name = user_obj.name if user_obj else "Unknown"

            msg_payload = json.dumps({
                    "id": msg.id,
                    "sender": sender_name,
                    "sender_id": sender_id,
                    "content": content,
                    "time": msg.timestamp.isoformat(),
                    })
            for ws in ws_connections[conversation_id]:
                try:
                    await ws.send_text(msg_payload)
                except Exception:
                    pass
            for ws in ws_connections[conversation_id]:
                try:
                    await ws.send_text(msg_payload)
                except Exception:
                    pass
    except WebSocketDisconnect:
        ws_connections[conversation_id].remove(websocket)
        db.close()

