from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class VoteBase(BaseModel):
    value: int = Field(..., ge=-1, le=1)

class VoteCreate(BaseModel):
    post_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    value: int = Field(..., ge=-1, le=1)

class VoteOut(VoteBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
