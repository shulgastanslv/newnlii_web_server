from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.comments import CommentsOut
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
    status : str
    benefit: Optional[str] = None
    aiOrigin: Optional[str] = None
    linkUrl: Optional[str] = None

class PostCreate(PostBase):
    pass

class SavedPostOut(BaseModel):
  id : int
  user_id : int
  post_id  : int
  user : UserOut
  saved_at : datetime
  class Config:
        from_attributes = True 

class PostOut(PostBase):
  created_at: datetime
  author : UserOut
  saved_by: List[SavedPostOut] = []
  comments: List[CommentsOut] = [] 


from enum import Enum

class FeedFilter(str, Enum):
    foryou = "foryou"
    all = "all"
    following = "following"
    popular = "popular"
    new = "new"