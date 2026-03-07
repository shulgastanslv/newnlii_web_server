from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.schemas.user import UserOut

class CommentsBase(BaseModel):
    text: str


class CommentsCreate(CommentsBase):
    post_id: int
    author_id: int


class CommentsOut(CommentsBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    author : UserOut
    class Config:
        from_attributes = True