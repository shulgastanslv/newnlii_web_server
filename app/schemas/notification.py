from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.notification import NotificationType, NotificationStatus
from app.schemas.post import PostOut
from app.schemas.user import UserOut


class NotificationBase(BaseModel):
    user_id: int
    actor_id: Optional[int] = None
    post_id: Optional[int] = None
    type: NotificationType
    status: NotificationStatus = NotificationStatus.UNREAD
    title: str = Field(..., max_length=200)
    content: Optional[str] = Field(None, max_length=1000)
    expires_at: Optional[datetime] = None


class NotificationCreate(BaseModel):
    user_id: int
    actor_id: Optional[int] = None
    post_id: Optional[int] = None
    type: NotificationType
    title: str = Field(..., max_length=200)
    content: Optional[str] = Field(None, max_length=1000)
    expires_at: Optional[datetime] = None


class NotificationUpdate(BaseModel):
    status: Optional[NotificationStatus] = None
    read_at: Optional[datetime] = None


class NotificationOut(NotificationBase):
    id: int
    created_at: datetime
    read_at: Optional[datetime] = None
    actor: Optional[UserOut] = None
    post: Optional[PostOut] = None
    user: UserOut
    
    model_config = ConfigDict(from_attributes=True)


class UnreadCountOut(BaseModel):
    user_id: int
    unread_count: int = 0
