from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

roles = ["Developer", "Customer"]

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: Optional[str] = roles[0]
    level: Optional[int] = 0
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    role: Optional[str] = None
    level: Optional[int] = None
    avatar_url: Optional[str] = None

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
