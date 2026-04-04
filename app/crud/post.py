import json
from datetime import datetime, time, timedelta, timezone
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload
from app.encoders import DateTimeEncoder
from app.models.post import Post, SavedPost, Tag, post_tags
from app.models.comment import Comment
from app.models.user import Follow, User
from app.schemas.post import PostCreate, PostOut
from app.redis_client import redis_client


def get_posts(
    db: Session,
    cursor: Optional[int] = None,
    limit: int = 15,
    current_user_id: Optional[str] = None, 
    tab : str = "foryou",
):

    query = db.query(Post).options(
        selectinload(Post.tags),
        selectinload(Post.comments).selectinload(Comment.author),
        selectinload(Post.saved_by),
        selectinload(Post.votes),
    )

    if tab == "new":
        # Посты за последние 24 часа, сортировка по убыванию (новые сверху)
        yesterday = datetime.now() - timedelta(days=1)
        query = query.filter(Post.created_at >= yesterday)
        order_field = Post.created_at.desc()
    elif tab == "following":
        # Только посты от авторов, на которых подписан текущий пользователь
        if current_user_id:
           query = query.join(Post.author).join(
            Follow, Follow.following_id == User.id  # following_id - на кого подписаны
            ).filter(
                Follow.follower_id == current_user_id  # follower_id - кто подписан
            )
        else:
            # Если пользователь не авторизован, показываем пустой результат
            return {
                "posts": [],
                "next_cursor": None,
                "has_next": False
            }
        order_field = Post.id.desc()
        
    else:  # "foryou" - алгоритмическая лента (для примера - просто последние)
        order_field = Post.id.desc()
    
    if cursor is not None:
        if tab == "new":
            # Для new используем created_at для курсора
            cursor_post = db.query(Post).filter(Post.id == cursor).first()
            if cursor_post:
                query = query.filter(Post.created_at < cursor_post.created_at)
        else:
            query = query.filter(Post.id < cursor)
    
    # Сортировка
    query = query.order_by(order_field)
    
    posts = query.limit(limit + 1).all()
    
    has_more = len(posts) > limit
    
    if has_more:
        posts = posts[:limit]
        next_cursor = posts[-1].id
    else:
        next_cursor = None
    
    return {
        "posts": posts,
        "next_cursor": next_cursor,
        "has_next": has_more,
    }
 
def get_posts_by_user_id(db: Session, user_id: str):
    cache_key = f"user_posts:{user_id}"
    
    # Пытаемся получить из кэша
    cached_result = redis_client.get_json(cache_key)
    if cached_result:
        return [PostOut.model_validate(post) for post in cached_result]
    
    # Если нет в кэше - запрос в БД
    posts = db.query(Post).filter(Post.author_id == user_id).order_by(Post.created_at.desc()).all()
    
    # Конвертируем в Pydantic
    pydantic_posts = [PostOut.model_validate(post) for post in posts]
    
    # Сохраняем в кэш на 60 секунд
    redis_client.setex(cache_key, 600, [p.model_dump() for p in pydantic_posts])
    
    return pydantic_posts

def get_saved_posts(db: Session, user_id: str):
    cache_key = f"saved_posts:{user_id}"
    
    # Пытаемся получить из кэша
    cached_result = redis_client.get_json(cache_key)
    if cached_result:
        return [PostOut.model_validate(post) for post in cached_result]
    
    # Если нет в кэше - запрос в БД
    saved_posts = db.query(SavedPost).filter(
        SavedPost.user_id == user_id
    ).order_by(SavedPost.saved_at.desc()).all()
    
    posts = [saved.post for saved in saved_posts if saved.post]
    
    # Конвертируем в Pydantic
    pydantic_posts = [PostOut.model_validate(post) for post in posts]
    
    # Сохраняем в кэш на 60 секунд
    redis_client.setex(cache_key, 600, [p.model_dump() for p in pydantic_posts])
    
    return pydantic_posts
 
def save_post(id: int, user_id: str, db: Session):
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
        
def delete_saved_post(id: int, user_id: str, db: Session):
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
        redis_client.invalidate_keys_by_pattern("posts:cursor:*")
        redis_client.invalidate_keys_by_pattern(f"user_posts:{post_data.author_id}")

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
    cache_key = f"popular_tags:{limit}"

    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    subquery = db.query(
        Tag.id,
        Tag.name,
        Tag.slug,
        func.count(post_tags.c.post_id).label("usage_count"),
    ).join(
        post_tags, Tag.id == post_tags.c.tag_id
    ).group_by(
        Tag.id, Tag.name, Tag.slug
    ).order_by(
        func.count(post_tags.c.post_id).desc()
    ).limit(limit).subquery()

    rows = db.query(
        subquery.c.id,
        subquery.c.name,
        subquery.c.slug,
        subquery.c.usage_count,
    ).all()

    result = [
        {
            "id": row.id,
            "name": row.name,
            "slug": row.slug,
            "usage_count": row.usage_count,
        }
        for row in rows
    ]

    # кэш
    redis_client.setex(
        cache_key,
        300,
        json.dumps(result, cls=DateTimeEncoder),
    )

    return result

def delete_post(post_id: int, user_id: str, db: Session):
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
        redis_client.invalidate_keys_by_pattern("posts:cursor:*")
        redis_client.invalidate_keys_by_pattern(f"user_posts:{user_id}")

        return True
  
