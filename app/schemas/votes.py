from pydantic import BaseModel
from datetime import datetime


class VoteBase(BaseModel):
    value: int


class VoteCreate(VoteBase):
    post_id: int
    user_id: int


class VoteOut(VoteBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True