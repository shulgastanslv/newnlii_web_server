from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.user import Follow


def follow_user(
    db: Session,
    follower_id: int,
    following_id: int
) -> Follow:
    try:

        moscow_time = datetime.utcnow() + timedelta(hours=3)

        if follower_id == following_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot follow yourself"
            )

        existing = db.query(Follow).filter(
            Follow.follower_id == follower_id,
            Follow.following_id == following_id
        ).first()

        if existing:
            return existing

        follow = Follow(
            follower_id=follower_id,
            following_id=following_id,
            created_at=moscow_time
        )

        db.add(follow)
        db.commit()
        db.refresh(follow)

        return follow

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


def unfollow_user(
    db: Session,
    follower_id: int,
    following_id: int
) -> None:
    try:
        follow = db.query(Follow).filter(
            Follow.follower_id == follower_id,
            Follow.following_id == following_id
        ).first()

        if not follow:
            raise HTTPException(
                status_code=404,
                detail="Follow relationship not found"
            )

        db.delete(follow)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


def get_followers(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Follow]:
    try:
        return db.query(Follow).filter(
            Follow.following_id == user_id
        ).order_by(
            Follow.created_at.desc()
        ).offset(skip).limit(limit).all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching followers: {str(e)}"
        )


def get_following(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Follow]:
    try:
        return db.query(Follow).filter(
            Follow.follower_id == user_id
        ).order_by(
            Follow.created_at.desc()
        ).offset(skip).limit(limit).all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching following: {str(e)}"
        )


def get_follow_count(
    db: Session,
    user_id: int
):
    try:
        followers_count = db.query(Follow).filter(
            Follow.following_id == user_id
        ).count()

        following_count = db.query(Follow).filter(
            Follow.follower_id == user_id
        ).count()

        return {
            "followers_count": followers_count,
            "following_count": following_count
        }

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error counting follows: {str(e)}"
        )