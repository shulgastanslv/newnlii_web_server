import json
from datetime import datetime, time, timedelta, timezone
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload
from app.encoders import DateTimeEncoder
from app.models.post import Post, SavedPost, Tag, post_tags
from app.models.comment import Comment
from app.schemas.post import PostCreate, PostOut
from app.redis_client import redis_client




def get_posts(
    db: Session, 
    cursor: Optional[int] = None, 
    limit: int = 15, 
    user_id: Optional[str] = None, 
):
    cache_key = f"posts:{cursor}:{limit}:{user_id}"
    
    cached_result = redis_client.get_json(cache_key)
    if cached_result:
        return {
            'posts': [PostOut.model_validate(post) for post in cached_result],
            'cache_result': cached_result,
            'has_next': False,
            'next_cursor': None
        }
    
    query = db.query(Post).options(selectinload(Post.tags), 
                                   selectinload(Post.comments).selectinload(Comment.author), 
                                   selectinload(Post.saved_by),
                                    selectinload(Post.votes) )     
    if cursor:
        query = query.filter(Post.id < cursor)
    if user_id:
        query = query.filter(Post.author_id == user_id) 
    query = query.order_by(Post.id.desc())
    
    posts = query.limit(limit + 1).all()
    
    has_next = len(posts) > limit
    if has_next:
        posts = posts[:-1]
    
    pydantic_posts = [PostOut.model_validate(post) for post in posts]
    
    result = {
        'posts': pydantic_posts,
        'cache_result': [post.model_dump() for post in pydantic_posts],
        'has_next': has_next,
        'next_cursor': posts[-1].id if posts else None
    }
    
    redis_client.setex(cache_key, 60, result['cache_result'])

    return result

def preload_posts(db: Session, limit: int = 50) -> Dict[str, Any]:
    cache_key = "posts:preload:latest"
    
    if redis_client.exists(cache_key):
        return {"status": "already_preloaded", "count": redis_client.get_json(cache_key + ":count")}
    
    query = db.query(Post).options(
        selectinload(Post.tags), 
        selectinload(Post.comments).selectinload(Comment.author), 
        selectinload(Post.votes)
    ).order_by(Post.id.desc())
    
    posts = query.limit(limit).all()
    
    if not posts:
        return {"status": "no_posts", "count": 0}
    
    pydantic_posts = [PostOut.model_validate(post) for post in posts]
    cache_data = [post.model_dump() for post in pydantic_posts]
    
    redis_client.setex(cache_key, 300, cache_data)  # 5 минут TTL
    
    redis_client.setex(cache_key + ":count", 300, len(cache_data))
    redis_client.setex(cache_key + ":timestamp", 300, int(time.time()))
    redis_client.setex(cache_key + ":limit", 300, limit)
    
    return {
        "status": "success",
        "count": len(cache_data),
        "key": cache_key,
        "ttl": 300
    }
    
def save_post(id: int, user_id: int, db: Session):
        existing_save = db.query(SavedPost).filter(
            SavedPost.post_id == id,
            SavedPost.user_id == user_id
        ).first()
        
        if existing_save:
            raise HTTPException(
                status_code=400,
                detail="Post already saved by this user"
            )
        
        save_post = SavedPost(
            post_id=id,
            user_id=user_id,
            saved_at=datetime.now(timezone.utc)
        )
        db.add(save_post)
        db.commit() 
        db.refresh(save_post) 
        
        return save_post
        
def delete_saved_post(id: int, user_id: int, db: Session):
        saved_post = db.query(SavedPost).filter(
            SavedPost.post_id == id,
            SavedPost.user_id == user_id
        ).first()
        
        if not saved_post:
            raise HTTPException(
                status_code=404,
                detail="Saved post not found"
            )
        
        db.delete(saved_post)
        db.commit()
        
        return {"message": "Post unsaved successfully"}

def create_post(post_data: PostCreate, db: Session):
        moscow_time = datetime.utcnow() + timedelta(hours=3)

        db_post = Post(
            text=post_data.text,
            published=post_data.published,
            author_id=post_data.author_id,
            images=post_data.images or [],
            is_reply = post_data.is_reply,
            category=post_data.category,
            created_at=moscow_time,
            status = post_data.status,
        )
        
        db.add(db_post)
        db.flush()

        if post_data.tags:
            for tag_obj in post_data.tags:
                tag_name = tag_obj.name if hasattr(tag_obj, 'name') else str(tag_obj)
                
                if tag_name:
                    existing_tag = db.query(Tag).filter(Tag.name == tag_name).first()
                    
                    if not existing_tag:
                        new_tag = Tag(
                            name=tag_name, 
                            slug=tag_name.lower().replace(' ', '-')
                        )
                        db.add(new_tag)
                        db.flush()
                        tag_id = new_tag.id
                    else:
                        tag_id = existing_tag.id
                    db.execute(
                        post_tags.insert().values(
                            post_id=db_post.id,
                            tag_id=tag_id,
                            created_at=datetime.utcnow()
                        )
                    )
        
        
        
        db.commit()
        db.refresh(db_post)
        return db_post
    
def get_post_by_id(db: Session, id: int) -> Post:

    try:
        post = db.query(Post).filter(Post.id == id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching post: {str(e)}")
    
def get_popular_tags(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        
        cache_key = f"popular:{limit}"
        
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            return json.loads(cached_result)
    
        popular_tags = db.query(
            Tag.id,
            Tag.name,
            Tag.slug,
            func.count(post_tags.c.post_id).label('usage_count')
        ).join(
            post_tags, Tag.id == post_tags.c.tag_id
        ).group_by(
            Tag.id, Tag.name, Tag.slug
        ).order_by(
            func.count(post_tags.c.post_id).desc()
        ).limit(limit).all()
        
        # serialize_tags = [serialize_tag(tag) for tag in popular_tags]
          
        redis_client.setex(
            cache_key, 
            300, 
            json.dumps([], cls=DateTimeEncoder)

        )

        return []

def delete_post(post_id: int, user_id: int, db: Session):
        post = db.query(Post).filter(
            Post.id == post_id,
            Post.author_id == user_id
        ).first()
        
        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post post not found"
            )
        
        db.delete(post)
        db.commit()
        
        return True
  
