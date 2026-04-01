from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class ViewBase(BaseModel):
    post_id: int = Field(..., gt=0)
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ViewCreate(ViewBase):
    pass

class ViewOut(ViewBase):
    id: int
    viewed_at: datetime
    
    model_config = ConfigDict(from_attributes=True)