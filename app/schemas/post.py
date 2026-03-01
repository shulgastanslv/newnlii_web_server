from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.user import UserOut

class TagResponse(BaseModel):
    name: str
    slug: str
    
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    id : Optional[int] = None
    text : str
    published : bool = False
    author_id : int
    views : int = 0
    is_reply : bool = False
    images : List[str] = None
    tags: List[TagResponse] = []
    category : str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
  created_at: datetime
  author : UserOut


class SavedPostOut(PostBase):
  created_at: datetime
  author : UserOut