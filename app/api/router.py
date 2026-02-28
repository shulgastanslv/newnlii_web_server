from fastapi import APIRouter
from app.api.v1 import user
from app.api.v1 import post

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(post.router, prefix="/posts", tags=["Posts"])
