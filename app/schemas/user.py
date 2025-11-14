from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.shared import UserBase


class UserLogin(UserBase):
    wallet_address: str
    signature: str
    message: str

class UserUpdate(BaseModel):
    role: Optional[str] = None
    level: Optional[int] = None
    image_url: Optional[str] = None
    name: Optional[str] = None


class UserWallet(BaseModel):
    wallet_address: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
