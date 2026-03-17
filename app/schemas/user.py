from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=100)
    push_notifications: bool = False
    likes_notifications: bool = False
    comments_notifications: bool = False
    closed: bool = False
    verify: bool = False

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, description="Hashed password")
    email: str = Field(..., min_length=5, max_length=100)

class UserOut(UserBase):
    id: Optional[int] = None
    verify: bool = False
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, min_length=5, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=100)
    push_notifications: bool = False
    likes_notifications: bool = False
    comments_notifications: bool = False
    closed: bool = False



