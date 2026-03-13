from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy import case, func
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session, joinedload
from app.models.post import Comment, Post, SavedPost, Tag, Vote, post_tags
from app.models.user import Follow, User
from app.schemas.post import FeedFilter, PostCreate

def get_posts(
    db: Session, 
    cursor: Optional[int] = None, 
    limit: int = 15, 
    filter: FeedFilter = FeedFilter.new,
    user_id: Optional[int] = None, 
    category: Optional[str] = None
):
    query = db.query(Post).options(joinedload(Post.tags))
    
    if category:
        query = query.filter(Post.category == category)
    
    if filter == FeedFilter.following:
        if user_id is None:
            raise ValueError("User_id required for following feed")
        query = query.join(
            Follow, 
            Follow.following_id == Post.author_id
        ).filter(Follow.follower_id == user_id)
    
    if filter == FeedFilter.popular:
        # Для popular считаем количество комментариев
        query = query.outerjoin(Comment).group_by(Post.id)
        query = query.order_by(func.count(Comment.id).desc(), Post.id.desc())
        if cursor:
            # Для popular нужна специальная логика пагинации
            subquery = db.query(Post.id).outerjoin(Comment).group_by(Post.id).having(
                func.count(Comment.id) < cursor
            ).subquery()
            query = query.filter(Post.id.in_(subquery))
    
    elif filter == FeedFilter.foryou:
        likes = func.sum(case((Vote.value == 1, 1), else_=0)).label('likes')
        dislikes = func.sum(case((Vote.value == -1, 1), else_=0)).label('dislikes')
        rating = (likes - dislikes).label('rating')
        
        query = query.outerjoin(Vote, Vote.post_id == Post.id)\
                    .group_by(Post.id)\
                    .order_by(rating.desc(), Post.id.desc())
        
        if cursor:
            query = query.having(
                (rating < cursor) | 
                ((rating == cursor) & (Post.id < cursor))
            )
    
    else:
        order_by = [Post.created_at.desc()]
        if cursor:
            query = query.filter(Post.id < cursor)
        query = query.order_by(*order_by)
    
    posts = query.limit(limit + 1).all()
    
    return posts

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
    