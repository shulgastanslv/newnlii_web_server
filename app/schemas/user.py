from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    id : Optional[str]
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
    is_google : bool = False

class UserCreate(BaseModel):
    user_id : str
    username: Optional[str]  = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8, description="Hashed password")
    email: str = Field(..., min_length=5, max_length=100)
    is_google : bool = False
    
class UserOut(UserBase):
    id: str 
    password: Optional[str] = Field(None, min_length=8, description="Hashed password")
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    id : Optional[str]
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, min_length=5, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=100)
    push_notifications: bool = False
    likes_notifications: bool = False
    comments_notifications: bool = False
    closed: bool = False



