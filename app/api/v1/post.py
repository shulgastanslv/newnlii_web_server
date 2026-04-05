from http.client import HTTPException
import random
from fastapi import APIRouter, Depends, Path, Query
from pydantic import BaseModel
import redis
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import post as crud_post
from typing import List, Optional
from app.schemas.post import PostCreate, PostOut, SavedPostOut

router = APIRouter()

class GetAllPosts(BaseModel):
    posts : List[PostOut]
    has_next : bool
    next_cursor : Optional[int] = None

@router.get("/", response_model=GetAllPosts)
def get_all_posts_route(
    cursor: int | None = None,
    tab: str = "foryou", 
    limit: int = Query(15, le=50),
    current_user_id: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    try:
        result = crud_post.get_posts(db, cursor=cursor, limit=limit, tab=tab, current_user_id=current_user_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    
@router.get("/user/{user_id}", response_model=List[PostOut])
def get_all_posts_by_userid_route(
    user_id: str,
    db: Session = Depends(get_db)
):
    try:
        result = crud_post.get_posts_by_user_id(db, user_id=user_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.get("/tag/{tag_name}", response_model=List[PostOut])
def get_all_posts_by_tag_route(
    tag_name: str,
    db: Session = Depends(get_db)
):
    try:
        result = crud_post.get_posts_by_tag(db, tag_name=tag_name)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

@router.get("/category/{category_name}", response_model=List[PostOut])
def get_all_posts_by_category_route(
    category_name: str,
    db: Session = Depends(get_db)
):
    try:
        result = crud_post.get_posts_by_category(db, category_name=category_name)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/saved/{user_id}", response_model=List[PostOut])
def get_saved_posts_by_userid_route(
    user_id: str,
    db: Session = Depends(get_db)
):
    try:
        result = crud_post.get_saved_posts(db, user_id=user_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.get("/{post_id}", response_model=PostOut)
def get_post_by_id_route(
    post_id: int = Path(..., description="ID поста", ge=1), 
    db: Session = Depends(get_db)
):
    try:
        return crud_post.get_post_by_id(db, post_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{post_id}", response_model=bool)
def delete_post_route(
    post_id: int = Path(..., description="ID поста", ge=1), 
    user_id: str = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    try:
        return crud_post.delete_post(db=db, post_id=post_id, user_id=user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/", response_model=PostOut, status_code=201)
def create_post_route(
    post: PostCreate, 
    db: Session = Depends(get_db)
):
    try:
        return crud_post.create_post(post, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post("/saved/{post_id}", status_code=201)
def save_post_route(
    post_id: int = Path(..., description="ID поста для сохранения", ge=1),
    user_id: str = Query(..., description="ID пользователя"),
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
    user_id: str = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    try:
        return crud_post.delete_saved_post(post_id, user_id, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
