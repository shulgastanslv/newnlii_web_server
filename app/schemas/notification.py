from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.post import NotificationType, NotificationStatus
from app.schemas.post import PostBase
from app.schemas.user import UserOut

class NotificationBase(BaseModel):
    user_id: int
    actor_id: Optional[int] = None
    post_id: Optional[int] = None
    type: NotificationType
    status: NotificationStatus = NotificationStatus.UNREAD
    title: str
    content: Optional[str] = None
    expires_at: Optional[datetime] = None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    status: Optional[NotificationStatus] = None
    read_at: Optional[datetime] = None


class NotificationOut(NotificationBase):
    id: int
    created_at: datetime
    read_at: Optional[datetime] = None
    actor: Optional[UserOut] = None
    post: Optional[PostBase] = None

    class Config:
        from_attributes = True


class UnreadCountOut(BaseModel):
    user_id: int
    unread_count: int