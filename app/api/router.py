from fastapi import APIRouter
from app.api.v1 import user, views
from app.api.v1 import post
from app.api.v1 import tag
from app.api.v1 import notification
from app.api.v1 import comments
from app.api.v1 import follow
from app.api.v1 import vote

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(post.router, prefix="/posts", tags=["Posts"])
api_router.include_router(tag.router, prefix="/tags", tags=["Tags"])
api_router.include_router(notification.router, prefix="/notifications", tags=["Notificatios"])
api_router.include_router(comments.router, prefix="/comments", tags=["Comments"])
api_router.include_router(follow.router, prefix="/follows", tags=["Follows"])
api_router.include_router(vote.router, prefix="/votes", tags=["Votes"])
api_router.include_router(views.router, prefix="/views", tags=["Views"])
