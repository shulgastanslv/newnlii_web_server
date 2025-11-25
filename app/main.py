from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
import os

# CORS origins - можно настроить через переменную окружения
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:3000")
if cors_origins_env == "*":
    cors_origins = ["*"]
else:
    cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]

app = FastAPI(
    title="Devsy Web Server API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Devsy Web Server API",
        "docs": "/docs",
        "version": "1.0.0"
    }
