from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from typing import List
from core.connection_manager import ConnectionManager
from db.session import get_db
from models.user import User
from models.message import Message

app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws/chat/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, db: Session = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            user = db.query(User).filter(User.username == username).first()
            if not user:
                user = User(username=username)
                db.add(user)
                db.commit()
                db.refresh(user)
            message = Message(text=data, owner_id=user.id)
            db.add(message)
            db.commit()
            db.refresh(message)
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} покинул чат")

@app.post("/messages/")
async def create_message(username: str, text: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    message = Message(text=text, owner_id=user.id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@app.get("/messages/")
async def get_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.timestamp.desc()).offset(skip).limit(limit).all()
    return messages
