from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.post import Comment
from app.schemas.comments import CommentsCreate


def create_comment(db: Session, comment_in: CommentsCreate) -> Comment:
    try:

        moscow_time = datetime.utcnow() + timedelta(hours=3)
        db_comment = Comment(
            post_id=comment_in.post_id,
            author_id=comment_in.author_id,
            text=comment_in.text,
            created_at=moscow_time
        )

        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_comments_by_post(
    db: Session,
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    include_deleted: bool = False
) -> List[Comment]:

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



def delete_comment(
    db: Session,
    comment_id: int,
    user_id: int
) -> None:

    try:
        comment = db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.author_id == user_id,
            Comment.is_deleted == False
        ).first()

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found or access denied")

        # Soft delete
        comment.is_deleted = True
        comment.deleted_at = datetime.now(timezone.utc)

        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(status_code=500, detail=f"Error deleting comment: {str(e)}")


def get_comment_count_by_post(db: Session, post_id: int) -> int:
    try:
        return db.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.is_deleted == False
        ).count()

    except SQLAlchemyError as e:
        raise Exception(status_code=500, detail=f"Error counting comments: {str(e)}")