from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
import os

cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:3000")

app = FastAPI(
    title="Devsy Web Server API",
    version="1.0.0"
)

if cors_origins_env == "*":
    import re
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r".*", 
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
else:
    cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Devsy Web Server API",
        "docs": "/docs",
        "version": "1.0.0"
    }
