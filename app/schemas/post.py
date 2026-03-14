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
    is_deleted : bool = False
    images : List[str] = None
    tags: List[TagResponse] = []
    category : str
    status : str
    benefit: Optional[str] = None
    aiOrigin: Optional[str] = None
    linkUrl: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


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
  author : UserOut
  saved_by: List[SavedPostOut] = []
  comments: List[CommentsOut] = [] 

def serialize_post(post : PostOut):
    post_dict = {
        'id': post.id,
        'text': post.text,
        'published': post.published,
        'status': post.status if post.status else None,
        'category': post.category,
        'author_id': post.author_id,
        'benefit': post.benefit,
        'views': post.views,
        'aiOrigin': post.aiOrigin,
        'linkUrl': post.linkUrl,
        'created_at': post.created_at.isoformat() if post.created_at else None,
        'updated_at': post.updated_at.isoformat() if post.updated_at else None,
        'images': post.images,
        'is_deleted': post.is_deleted,
        'deleted_at': post.deleted_at.isoformat() if post.deleted_at else None,
        'is_reply': post.is_reply,
        'tags': [{'id': t.id, 'name': t.name, 'slug': t.slug} for t in post.tags]
    }
    
    if hasattr(post, 'author') and post.author:
        post_dict['author'] = {
            'id': post.author.id,
            'username': post.author.username,
            'email': post.author.email,
            'password' : post.author.password
        }
    else:
        post_dict['author'] = None
    
    return post_dict

from enum import Enum

class FeedFilter(str, Enum):
    foryou = "foryou"
    all = "all"
    following = "following"
    popular = "popular"
    new = "new"