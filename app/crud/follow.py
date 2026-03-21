from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import Follow

def follow_user(
    db: Session,
    follower_id: str,
    following_id: str
) -> Follow:
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

def unfollow_user(
    db: Session,
    follower_id: str,
    following_id: str
) -> None:
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

def get_followers(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[Follow]:
        return db.query(Follow).filter(
            Follow.following_id == user_id
        ).order_by(
            Follow.created_at.desc()
        ).offset(skip).limit(limit).all()

def get_following(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100
) -> List[Follow]:
        return db.query(Follow).filter(
            Follow.follower_id == user_id
        ).order_by(
            Follow.created_at.desc()
        ).offset(skip).limit(limit).all()

def get_follow_count(
    db: Session,
    user_id: str
):
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
