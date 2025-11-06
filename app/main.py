from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)
