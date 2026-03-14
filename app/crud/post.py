from datetime import datetime, timedelta, timezone
import json
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy import case, func
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session, joinedload
from app.models.post import Comment, Post, SavedPost, Tag, Vote, post_tags
from app.models.user import Follow, User
from app.schemas.post import FeedFilter, PostCreate
import redis
import json
from typing import Optional, List, Any
from datetime import timedelta

redis_client = redis.Redis(
    host='localhost', 
    port=6379, 
    db=0, 
    decode_responses=True,
    password=None
)

class DateTimeEncoder(json.JSONEncoder):
    """Кастомный encoder для обработки datetime и Enum"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, 'value'):  # для Enum
            return obj.value
        return super().default(obj)

def serialize_post(post):
    """Преобразует объект Post в словарь для JSON с учетом всех нужных полей"""
    # Базовые поля поста
    post_dict = {
        'id': post.id,
        'text': post.text,
        'published': post.published,
        'status': post.status.value if post.status else None,
        'category': post.category,
        'author_id': post.author_id,
        'benefit': post.benefit,
        'views': post.views,
        'aiOrigin': post.aiOrigin,
        'linkUrl': post.linkUrl,
        'saved_count': post.saved_count,
        'created_at': post.created_at.isoformat() if post.created_at else None,
        'updated_at': post.updated_at.isoformat() if post.updated_at else None,
        'images': post.images,
        'is_deleted': post.is_deleted,
        'deleted_at': post.deleted_at.isoformat() if post.deleted_at else None,
        'is_reply': post.is_reply,
        'tags': [{'id': t.id, 'name': t.name, 'slug': t.slug} for t in post.tags]
    }
    
    # Добавляем автора если он есть (загружен через relationship)
    if hasattr(post, 'author') and post.author:
        post_dict['author'] = {
            'id': post.author.id,
            'username': post.author.username,
            'email': post.author.email,
            'password' : post.author.password
            # добавьте другие поля автора которые нужны в PostOut
        }
    else:
        # Если автор не загружен, можно оставить null или загрузить отдельно
        post_dict['author'] = None
    
    return post_dict

def invalidate_post_cache(pattern="posts:*"):
    """Очищает кэш постов по паттерну"""
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)


def get_posts(
    db: Session, 
    cursor: Optional[int] = None, 
    limit: int = 15, 
    user_id: Optional[int] = None, 
):
    cache_key = f"posts:{cursor}:{limit}:{user_id}"
    
    # Пытаемся получить из кэша
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    
    # Базовый запрос
    query = db.query(Post).options(joinedload(Post.tags))
    
    # Применяем cursor пагинацию (по id, так как это проще для курсора)
    if cursor:
        query = query.filter(Post.id < cursor)
    
    # Сортировка по id (убывающая)
    query = query.order_by(Post.id.desc())
    
    # Запрашиваем limit + 1 чтобы понять, есть ли следующая страница
    posts = query.limit(limit + 1).all()
    
    # Определяем, есть ли еще посты
    has_next = len(posts) > limit
    if has_next:
        posts = posts[:-1]  # удаляем лишний пост
    
    # Сериализуем
    serialized_posts = [serialize_post(post) for post in posts]
    
    # Добавляем флаг has_next в результат
    result = {
        'posts': serialized_posts,
        'has_next': has_next,
        'next_cursor': posts[-1].id if posts else None
    }
    
    # Кэшируем
    redis_client.setex(
        cache_key, 
        30,  # 30 секунд кэша
        json.dumps(result, cls=DateTimeEncoder)
    )
    
    return result

def save_post(id: int, user_id: int, db: Session):
    try:
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
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Database integrity error occurred"
        )
    except DataError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid data format"
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while saving the post"
        )

def delete_saved_post(id: int, user_id: int, db: Session):
    try:
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
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while unsaving the post"
        )
    


def get_user_saved_posts(
    user_id: int,
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    try:
        posts = (
            db.query(Post)
            .join(SavedPost, SavedPost.post_id == Post.id)
            .filter(SavedPost.user_id == user_id)
            .order_by(SavedPost.saved_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return posts

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching saved posts"
        )
    
def is_post_saved_by_user(id: int, user_id: int, db: Session) -> bool:
    try:
        exists = db.query(SavedPost).filter(
            SavedPost.post_id == id,
            SavedPost.user_id == user_id
        ).first() is not None
        
        return exists
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while checking saved status"
        )

def get_saved_count(post_id : int, db : Session) -> int:
    try:
        post_count = db.query(SavedPost).filter(
            SavedPost.post_id == post_id,
        ).count()
        
        return {"post_id" : post_id, "count" : post_count}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while checking saved posts"
        )

def create_post(post_data: PostCreate, db: Session):
    try:
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
            benefit = post_data.benefit,
            aiOrigin = post_data.aiOrigin,
            linkUrl = post_data.linkUrl
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
        
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Post with this data already exists: {str(e)}")
    except DataError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating post: {str(e)}")
    
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
    
    try:
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
        
        result = [
            {
                'id': tag.id,
                'name': tag.name,
                'slug': tag.slug,
                'usage_count': tag.usage_count
            }
            for tag in popular_tags
        ]
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching popular tags: {str(e)}"
        )

def increment_post_views(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.views += 1
        db.commit()
        db.refresh(post)
    return post


def delete_post(post_id: int, user_id: int, db: Session):
    try:
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
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while unsaving the post"
        )
    