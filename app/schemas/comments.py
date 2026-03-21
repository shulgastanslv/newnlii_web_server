from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.schemas.user import UserOut

class CommentBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

class CommentCreate(BaseModel):
    post_id: int = Field(..., gt=0)
    author_id: str = Field(..., gt=0)
    text: str = Field(..., min_length=1, max_length=2000)

class CommentOut(CommentBase):
    id: int
    post_id: int
    author_id: str
    author: UserOut
    created_at: datetime
    updated_at: Optional[datetime] = None 
    is_deleted: bool = False
    model_config = ConfigDict(from_attributes=True)
