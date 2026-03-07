from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import follow as crud_follow
from app.schemas.follow import FollowResponse

router = APIRouter()


@router.post("/", response_model=FollowResponse, status_code=status.HTTP_201_CREATED)
def follow_user(
    follower_id: int = Query(..., description="ID пользователя, который подписывается"),
    following_id: int = Query(..., description="ID пользователя, на которого подписываются"),
    db: Session = Depends(get_db)
):
    return crud_follow.follow_user(db, follower_id, following_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    follower_id: int = Query(..., description="ID пользователя, который отписывается"),
    following_id: int = Query(..., description="ID пользователя, от которого отписываются"),
    db: Session = Depends(get_db)
):
    crud_follow.unfollow_user(db, follower_id, following_id)
    return None


@router.get("/followers", response_model=List[FollowResponse])
def get_followers(
    user_id: int = Query(..., description="ID пользователя для получения подписчиков"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    return crud_follow.get_followers(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/following", response_model=List[FollowResponse])
def get_following(
    user_id: int = Query(..., description="ID пользователя для получения подписок"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    return crud_follow.get_following(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/status")
def follow_status(
    follower_id: int = Query(..., description="ID потенциального подписчика"),
    following_id: int = Query(..., description="ID потенциального пользователя, на которого подписываются"),
    db: Session = Depends(get_db)
):
    is_following = crud_follow.get_following(db, user_id=follower_id)
    following_ids = [f.following_id for f in is_following]
    return {"is_following": following_id in following_ids}



@router.get("/count")
def follow_status(
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    res = crud_follow.get_follow_count(db, user_id=user_id)
    return res