from http.client import HTTPException
import random
from fastapi import APIRouter, Depends, Path, Query
import redis
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import post as crud_post
from typing import List, Optional
from app.schemas.post import FeedFilter, PostCreate, PostOut, SavedPostOut

router = APIRouter()

@router.get("/", response_model=List[PostOut])
def get_all_posts_route(
    cursor: int | None = None,
    limit: int = Query(5, ge=1, le=50),
    userId : int | None = None,
    db: Session = Depends(get_db)
):
    result = crud_post.get_posts(db, cursor=cursor, limit=limit, user_id=userId)
    # Возвращаем только посты, has_next можно передать в заголовках
    return result['posts']

@router.get("/{post_id}", response_model=PostOut)
def get_post_by_id_route(
    post_id: int = Path(..., description="ID поста", ge=1), 
    db: Session = Depends(get_db)
):
    return crud_post.get_post_by_id(db, post_id)

@router.delete("/{post_id}", response_model=bool)
def delete_post_route(
    post_id: int = Path(..., description="ID поста", ge=1), 
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    return crud_post.delete_post(db=db, post_id=post_id, user_id=user_id)

@router.post("/", response_model=PostOut, status_code=201)
def create_post_route(
    post: PostCreate, 
    db: Session = Depends(get_db)
):
    try:
        print(post)
        return crud_post.create_post(post, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post("/saved/{post_id}", status_code=201)
def save_post_route(
    post_id: int = Path(..., description="ID поста для сохранения", ge=1),
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    post = crud_post.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    
    return crud_post.save_post(post_id, user_id, db)


@router.delete("/saved/{post_id}", status_code=200)
def unsave_post_route(
    post_id: int = Path(..., description="ID поста для удаления из сохраненных", ge=1),
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    return crud_post.delete_saved_post(post_id, user_id, db)

@router.get("/saved/user/{user_id}", response_model=List[SavedPostOut])
def get_user_saved_posts_route(
    user_id: int = Path(..., description="ID пользователя", ge=1),
    skip: int = Query(0, description="Skip N saved posts", ge=0),
    limit: int = Query(100, description="Limit results", ge=1, le=500),
    db: Session = Depends(get_db)
):
    return crud_post.get_user_saved_posts(user_id, db, skip, limit)

@router.get("/saved/check/{post_id}", response_model=dict)
def check_post_saved_route(
    post_id: int = Path(..., description="ID поста для проверки", ge=1),
    user_id: int = Query(..., description="ID пользователя"), 
    db: Session = Depends(get_db)
):
    is_saved = crud_post.is_post_saved_by_user(post_id, user_id, db)
    return {
        "post_id": post_id,
        "user_id": user_id,
        "is_saved": is_saved
    }

@router.get("/saved_count/{post_id}", status_code=200)
def get_saved_count_route(
    post_id: int = Path(..., description="ID поста для удаления из сохраненных", ge=1),
    db: Session = Depends(get_db)
):
    return crud_post.get_saved_count(post_id, db)

@router.post("/{post_id}/view", response_model=PostOut)
def add_view_route(
    post_id: int = Path(..., description="ID поста", ge=1),
    db: Session = Depends(get_db)
):
    post = crud_post.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    updated_post = crud_post.increment_post_views(db, post_id)
    return updated_post
