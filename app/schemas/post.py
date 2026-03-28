from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.comments import CommentOut
from app.schemas.user import UserOut

class TagResponse(BaseModel):
    id: int
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=50)
    
    model_config = ConfigDict(from_attributes=True)

class Tag(BaseModel):
    name: str = Field(..., max_length=50)
    slug: str = Field(..., max_length=50)
    
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    category: str = Field(..., max_length=50)
    status: str = Field(..., max_length=20)
    benefit: Optional[str] = Field(None, max_length=1000)
    aiOrigin: Optional[str] = Field(None, max_length=200)
    linkUrl: Optional[str] = Field(None, max_length=500)
    published: bool = False
    is_reply: bool = False
    images: List[str] = Field(default_factory=list, max_length=10)


class PostCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    category: str = Field(..., max_length=50)
    author_id : str
    status: str = Field(default="unsent", max_length=20)
    published: bool = False
    is_reply: bool = False
    images: List[str] = Field(default_factory=list)
    tags: List[Tag] = Field(default_factory=list)


class PostUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=5000)
    category: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)
    benefit: Optional[str] = Field(None, max_length=1000)
    aiOrigin: Optional[str] = Field(None, max_length=200)
    linkUrl: Optional[str] = Field(None, max_length=500)
    published: Optional[bool] = None
    is_reply: Optional[bool] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class PostOut(PostBase):
    id: int
    author_id: str
    author: UserOut
    is_deleted: bool = False
    tags: List[TagResponse] = []
    comments: List[CommentOut] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    saved_by : List[SavedPostOut] = None
    model_config = ConfigDict(from_attributes=True)


class SavedPostOut(BaseModel):
    id: int
    user_id: str
    post_id: int
    user: UserOut
    saved_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
