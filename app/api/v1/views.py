from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import views as crud_view
from app.schemas.views import ViewCreate, ViewOut

router = APIRouter()

@router.get("/posts/{post_id}", response_model=List[ViewOut])
def get_views_by_post(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Получает список просмотров поста с возможностью фильтрации по дате.
    """
    return crud_view.get_views_by_post(db, post_id, skip, limit, start_date, end_date)

@router.get("/posts/{post_id}/count")
def get_views_count_by_post(
    post_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    unique: bool = Query(False, description="Подсчитывать только уникальные просмотры"),
    db: Session = Depends(get_db)
):
    """
    Получает количество просмотров поста.
    Если unique=True, возвращает количество уникальных просмотров (по user_id/session_id).
    """
    if unique:
        count = crud_view.get_unique_views_count_by_post(db, post_id, start_date, end_date)
    else:
        count = crud_view.get_views_count_by_post(db, post_id, start_date, end_date)
    
    return {"post_id": post_id, "views_count": count, "unique": unique}

@router.get("/users/{user_id}", response_model=List[ViewOut])
def get_views_by_user(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Получает список просмотров пользователя по его ID.
    """
    return crud_view.get_views_by_user(db, user_id, skip, limit)

@router.post("/", response_model=ViewOut, status_code=status.HTTP_201_CREATED)
def create_view(
    view_in: ViewCreate,
    db: Session = Depends(get_db)
):
    """
    Создает запись о просмотре поста.
    
    Требуется указать либо user_id, либо session_id:
    - Для авторизованных пользователей передается user_id
    - Для неавторизованных передается session_id
    """
    # Проверяем, что указан либо user_id, либо session_id
    if not view_in.user_id and not view_in.session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either user_id or session_id must be provided"
        )
    
    # Если указан user_id, проверяем его существование в БД
    if view_in.user_id:
        from app.models.user import User
        user = db.query(User).filter(User.id == view_in.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {view_in.user_id} not found"
            )
    
    return crud_view.create_view(db, view_in)

@router.delete("/")
def delete_view(
    post_id: int = Query(..., description="ID поста"),
    user_id: Optional[str] = Query(None, description="ID пользователя"),
    session_id: Optional[str] = Query(None, description="ID сессии"),
    db: Session = Depends(get_db)
):
    """
    Удаляет просмотр поста для конкретного пользователя или сессии.
    """
    if not user_id and not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either user_id or session_id must be provided"
        )
    
    return crud_view.delete_view(db, post_id, user_id, session_id)

@router.delete("/posts/{post_id}")
def delete_views_by_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Удаляет все просмотры поста.
    """
    deleted_count = crud_view.delete_views_by_post(db, post_id)
    return {"deleted_count": deleted_count}

@router.delete("/cleanup/old")
def delete_old_views(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Удаляет просмотры старше указанного количества дней.
    """
    deleted_count = crud_view.delete_old_views(db, days)
    return {"deleted_count": deleted_count, "older_than_days": days}