from fastapi import APIRouter
from app.api.v1 import user
from app.api.v1 import post
from app.api.v1 import tag
from app.api.v1 import notification


api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(post.router, prefix="/posts", tags=["Posts"])
api_router.include_router(tag.router, prefix="/tags", tags=["Tags"])
api_router.include_router(notification.router, prefix="/notifications", tags=["Notificatios"])
