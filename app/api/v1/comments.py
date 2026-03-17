from typing import List
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import comments as crud_comment
from app.schemas.comments import CommentCreate, CommentOut

router = APIRouter()

@router.get("/", response_model=List[CommentOut])
def get_comments_by_post(
    post_id: int = Query(..., description="ID поста"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    include_deleted: bool = Query(False, description="Включить удалённые комментарии"),
    db: Session = Depends(get_db)
):
    return crud_comment.get_comments_by_post(
        db,
        post_id=post_id,
        skip=skip,
        limit=limit,
        include_deleted=include_deleted
    )

@router.get("/{comment_id}", response_model=CommentOut)
def get_comment(
    comment_id: int = Path(..., ge=1),
    db: Session = Depends(get_db)
):
    return crud_comment.get_comment_by_id(db, comment_id)

@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_in: CommentCreate,
    db: Session = Depends(get_db)
):
    return crud_comment.create_comment(db, comment_in)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int = Path(..., ge=1),
    user_id: int = Query(..., description="ID автора комментария"),
    db: Session = Depends(get_db)
):
    crud_comment.delete_comment(db, comment_id, user_id)
    return None