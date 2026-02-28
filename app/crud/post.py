from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session, joinedload
from app.models.post import Post, SavedPost, Tag, post_tags
from app.schemas.post import PostCreate


def get_posts(db: Session) -> List[Post]:
    try:
        posts = db.query(Post).options(
            joinedload(Post.tags)
        ).order_by(Post.published.desc()).all()
        
        return posts
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching posts: {str(e)}"
        )
    

def get_popular_tags(limit : int, min_posts : int, db: Session):
    try:
        popular_tags = db.query(
                Tag.id,
                Tag.name,
                Tag.slug,
                func.count(post_tags.c.post_id).label('posts_count')
            ).join(
                post_tags, Tag.id == post_tags.c.tag_id
            ).group_by(
                Tag.id, Tag.name, Tag.slug
            ).having(
                func.count(post_tags.c.post_id) >= min_posts
            ).order_by(
                func.count(post_tags.c.post_id).desc()
            ).limit(limit).all()
       
        if not popular_tags:
            return []
       
        result = [
            {
                "id": tag.id,
                "name": tag.name,
                "slug": tag.slug,
                "posts_count": tag.posts_count
            }
            for tag in popular_tags
        ]
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching tags: {str(e)}"
        )
    

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
    
def get_user_saved_posts(user_id: int, db: Session, skip: int = 0, limit: int = 100):
    try:
        saved_posts = db.query(SavedPost)\
            .filter(SavedPost.user_id == user_id)\
            .order_by(SavedPost.saved_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        return saved_posts
        
    except Exception as e:
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

def create_post(post_data: PostCreate, db: Session):
    try:
        db_post = Post(
            text=post_data.text,
            published=post_data.published,
            author_id=post_data.author_id,
            images=post_data.images or [],
            is_reply = post_data.is_reply,
            category=post_data.category,
            created_at=datetime.utcnow()
        )
        
        db.add(db_post)
        db.flush()
        
        if post_data.tags:
            for tag_name in post_data.tags:
                if tag_name:
                    tag = db.query(Tag).filter(Tag.name == tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name, slug=tag_name)
                        db.add(tag)
                        db.flush()
                    db.execute(
                        post_tags.insert().values(
                            post_id=db_post.id,
                            tag_id=tag.id,
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