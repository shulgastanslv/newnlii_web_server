from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserOut

class FollowCreate(BaseModel):
    follower_id: str = Field(..., gt=0)
    following_id: str = Field(..., gt=0)

class FollowResponse(BaseModel):
    id: int
    follower_id: str
    following_id: str
    created_at: datetime
    follower : UserOut
    following : UserOut
    model_config = ConfigDict(from_attributes=True)
