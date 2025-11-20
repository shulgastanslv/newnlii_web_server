from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str | None = None


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

