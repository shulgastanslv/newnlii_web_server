from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comments import CommentCreate

def create_comment(db: Session, comment_in: CommentCreate) -> Comment:
    try:

        moscow_time = datetime.utcnow() + timedelta(hours=3)
        db_comment = Comment(
            post_id=comment_in.post_id,
            author_id=comment_in.author_id,
            text=comment_in.text,
            created_at=moscow_time,
            parent_id=comment_in.parent_id, 
        )

        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_comments_tree_by_post(
    db: Session,
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    include_deleted: bool = False
) -> List[Comment]:
    """Загружает дерево комментариев (только корневые + их replies рекурсивно)"""
    try:
        # Берем только корневые комментарии (parent_id IS NULL)
        query = db.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.parent_id.is_(None),  # ✅ Только корневые
            Comment.is_deleted == False
        )
        
        if not include_deleted:
            query = query.filter(Comment.is_deleted == False)
            
        # Пагинация только для корневых комментариев
        root_comments = query.order_by(Comment.created_at.asc()) \
            .offset(skip).limit(limit).all()
            
        # Рекурсивно загружаем replies для каждого корневого
        for comment in root_comments:
            comment.replies = get_replies_recursive(db, comment.id, include_deleted)
            
        return root_comments
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching comments tree: {str(e)}")

def get_replies_recursive(
    db: Session, 
    parent_id: int, 
    include_deleted: bool = False,
    level: int = 0,
    max_level: int = 5  # Защита от бесконечной рекурсии
) -> List[Comment]:
    """Рекурсивно загружает replies"""
    if level >= max_level:
        return []
        
    try:
        query = db.query(Comment).filter(
            Comment.parent_id == parent_id,
            Comment.is_deleted == False
        ).order_by(Comment.created_at.asc())
        
        replies = query.all()
        
        # Рекурсивно загружаем sub-replies
        for reply in replies:
            reply.replies = get_replies_recursive(db, reply.id, include_deleted, level + 1, max_level)
            
        return replies
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error loading replies: {str(e)}")


def get_comments_flat_by_post(
    db: Session,
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    include_deleted: bool = False
) -> List[Comment]:
    """Оставляем для обратной совместимости"""
    try:
        query = db.query(Comment).filter(Comment.post_id == post_id)
        if not include_deleted:
            query = query.filter(Comment.is_deleted == False)
        return query.order_by(Comment.created_at.asc()) \
            .offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching comments: {str(e)}")


def get_comment_by_id(db: Session, comment_id: int) -> Comment:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

def delete_comment(db: Session, comment_id: int, user_id: str) -> None:
    try:
        comment = db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.author_id == user_id,
            Comment.is_deleted == False
        ).first()
        
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found or access denied")
            
        # Soft delete + каскадно удаляем replies
        comment.is_deleted = True
        comment.deleted_at = datetime.now(timezone.utc)
        db.commit()
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting comment: {str(e)}")


def get_comment_count_by_post(db: Session, post_id: int) -> int:
    try:
        return db.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.is_deleted == False
        ).count()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error counting comments: {str(e)}")
   