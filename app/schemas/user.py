from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id : Optional[int] = None
    username : str
    password : str
    email : str
    bio: Optional[str]
    avatar : Optional[str]
    location : Optional[str]
    push_notifications : bool
    likes_notifications : bool
    comments_notifications : bool
    closed : bool

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    pass
