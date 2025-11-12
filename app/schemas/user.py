from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserRoleEnum(str, Enum):
    developer = "Developer"
    customer = "Customer"

class UserBase(BaseModel):
    wallet_address: str
    name: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    level: Optional[int] = 0
    image_url: Optional[str] = None

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
