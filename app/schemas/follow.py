from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class FollowCreate(BaseModel):
    follower_id: int = Field(..., gt=0)
    following_id: int = Field(..., gt=0)


class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
