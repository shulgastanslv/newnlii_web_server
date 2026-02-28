from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id : Optional[int] = None
    username : str
    password : str
    email : str
    bio: Optional[str] = None
    avatar : Optional[str] = None
    location : Optional[str] = None
    push_notifications : bool = False
    likes_notifications : bool = False
    comments_notifications : bool = False
    closed : bool = False

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    pass
