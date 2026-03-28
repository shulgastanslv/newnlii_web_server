from typing import List
from fastapi import APIRouter, Depends, Path, Query, status, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import comments as crud_comment
from app.schemas.comments import CommentCreate, CommentOut


router = APIRouter()


@router.get("/", response_model=List[CommentOut])
def get_comments(
    post_id: int = Query(..., description="ID поста"),
    tree: bool = Query(True, description="Загружать дерево комментариев (true) или плоский список (false)"),
    skip: int = Query(0, ge=0, description="Пропустить первые N комментариев (только для корневых при tree=true)"),
    limit: int = Query(100, ge=1, le=500, description="Максимум комментариев"),
    include_deleted: bool = Query(False, description="Включить удалённые комментарии"),
    db: Session = Depends(get_db)
):
    """Получить комментарии поста в виде дерева или плоского списка"""
    if tree:
        return crud_comment.get_comments_tree_by_post(
            db, post_id=post_id, skip=skip, limit=limit, include_deleted=include_deleted
        )
    else:
        return crud_comment.get_comments_flat_by_post(
            db, post_id=post_id, skip=skip, limit=limit, include_deleted=include_deleted
        )


@router.get("/{comment_id}", response_model=CommentOut)
def get_comment(
    comment_id: int = Path(..., ge=1, description="ID комментария"),
    include_replies: bool = Query(False, description="Включить replies рекурсивно"),
    db: Session = Depends(get_db)
):
    """Получить конкретный комментарий с опциональными replies"""
    comment = crud_comment.get_comment_by_id(db, comment_id)
    
    if include_replies:
        comment.replies = crud_comment.get_replies_recursive(db, comment_id)
    
    return comment


@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_in: CommentCreate,
    db: Session = Depends(get_db)
):
    """Создать комментарий или ответ (если указан parent_id)"""
    # Валидация parent_id
    if comment_in.parent_id:
        parent = crud_comment.get_comment_by_id(db, comment_in.parent_id)
        if parent.post_id != comment_in.post_id:
            raise HTTPException(
                status_code=400, 
                detail="Parent comment must belong to the same post"
            )
        if parent.is_deleted:
            raise HTTPException(
                status_code=400, 
                detail="Cannot reply to deleted comment"
            )
    
    return crud_comment.create_comment(db, comment_in)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    current_user_id: str,
    comment_id: int = Path(..., ge=1, description="ID комментария"),
    db: Session = Depends(get_db),
):
    """Soft delete комментария (автор или модератор)"""
    crud_comment.delete_comment(db, comment_id, current_user_id)
    return None


@router.get("/count/{post_id}", response_model=int)
def get_comment_count(
    post_id: int = Path(..., ge=1, description="ID поста"),
    db: Session = Depends(get_db)
):
    """Получить количество комментариев поста"""
    return crud_comment.get_comment_count_by_post(db, post_id)