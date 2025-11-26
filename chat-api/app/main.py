
from app.db.session import engine
from app.db.base import Base
from app.api import chat, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Chat API",
    version="1.0.0"
)

# Настройка CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "https://devsy-five.vercel.app",
    "https://*.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(users.router, prefix="/chat/users", tags=["Users"])

@app.get("/chat/")
def root():
    return {
        "message": "Chat API",
        "docs": "/chat/docs",
        "websocket": "/chat/ws/{chat_id}/{user_id}"
    }


