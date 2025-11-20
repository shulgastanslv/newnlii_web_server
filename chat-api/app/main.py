from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.api import chat, users

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Chat API",
    description="Chat API with WebSocket support using FastAPI and SQLite",
    version="1.0.0"
)

# Настройка CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(chat.router, tags=["Chat"])
app.include_router(users.router, tags=["Users"])


@app.get("/")
def root():
    return {
        "message": "Chat API with WebSocket",
        "docs": "/docs",
        "websocket": "/ws/{chat_id}/{user_id}"
    }

