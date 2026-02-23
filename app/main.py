from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
import os

cors_origins = [
    "http://localhost:3000",
    # "https://devsy-five.vercel.app",
    "https://*.vercel.app",
]

app = FastAPI(
    title="Newnlii Web Server API",
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
        "message": "Newnlii Web Server API",
        "docs": "/docs",
        "version": "1.0.0"
    }
