from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.post import View
from app.schemas.views import ViewCreate
from app.redis_client import redis_client

def create_view(db: Session, view_in: ViewCreate):
    """
    Создает запись о просмотре поста.
    Если пользователь/сессия уже просматривал пост сегодня, новый просмотр не создается.
    """
    try:
        # Определяем время в Москве
        moscow_time = datetime.utcnow() + timedelta(hours=3)
        
        # Проверяем, был ли просмотр от этого пользователя/сессии за последние 24 часа
        today_start = moscow_time.replace(hour=0, minute=0, second=0, microsecond=0)
        
        query = db.query(View).filter(
            View.post_id == view_in.post_id,
            View.viewed_at >= today_start
        )
        
        # Фильтруем по user_id или session_id
        if view_in.user_id:
            query = query.filter(View.user_id == view_in.user_id)
        elif view_in.session_id:
            query = query.filter(View.session_id == view_in.session_id)
        else:
            # Если нет ни user_id, ни session_id, не создаем просмотр
            raise ValueError("Either user_id or session_id must be provided")
        
        existing_view = query.first()
        
        # Если просмотр уже был сегодня, возвращаем существующий
        if existing_view:
            return existing_view
        
        # Создаем новый просмотр
        db_view = View(
            post_id=view_in.post_id,
            user_id=view_in.user_id,
            session_id=view_in.session_id,
            viewed_at=moscow_time
        )
        
        db.add(db_view)
        db.commit()
        db.refresh(db_view)
        
        # Инвалидируем кэш для списка постов
        redis_client.invalidate_keys_by_pattern("posts:cursor:*")
        # Инвалидируем кэш для конкретного поста
        redis_client.invalidate_keys_by_pattern(f"posts:detail:{view_in.post_id}:*")
        
        return db_view
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_views_by_post(
    db: Session, 
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: datetime = None,
    end_date: datetime = None
):
    """
    Получает список просмотров поста с возможностью фильтрации по дате.
    """
    try:
        query = db.query(View).filter(View.post_id == post_id)
        
        if start_date:
            query = query.filter(View.viewed_at >= start_date)
        if end_date:
            query = query.filter(View.viewed_at <= end_date)
        
        return query.order_by(View.viewed_at.desc()).offset(skip).limit(limit).all()
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_views_by_user(
    db: Session,
    user_id: str,
    skip: int = 0,
    limit: int = 100
):
    """
    Получает список просмотров пользователя.
    """
    try:
        return db.query(View).filter(
            View.user_id == user_id
        ).order_by(View.viewed_at.desc()).offset(skip).limit(limit).all()
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_views_count_by_post(
    db: Session,
    post_id: int,
    start_date: datetime = None,
    end_date: datetime = None
) -> int:
    """
    Получает количество просмотров поста с возможностью фильтрации по дате.
    """
    try:
        query = db.query(View).filter(View.post_id == post_id)
        
        if start_date:
            query = query.filter(View.viewed_at >= start_date)
        if end_date:
            query = query.filter(View.viewed_at <= end_date)
        
        return query.count()
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_unique_views_count_by_post(
    db: Session,
    post_id: int,
    start_date: datetime = None,
    end_date: datetime = None
) -> int:
    """
    Получает количество уникальных просмотров поста (по user_id и session_id).
    """
    try:
        from sqlalchemy import func, distinct, or_
        
        query = db.query(View).filter(View.post_id == post_id)
        
        if start_date:
            query = query.filter(View.viewed_at >= start_date)
        if end_date:
            query = query.filter(View.viewed_at <= end_date)
        
        # Подсчитываем уникальные комбинации user_id и session_id
        # Где user_id не NULL или session_id не NULL
        unique_views = query.filter(
            or_(View.user_id.isnot(None), View.session_id.isnot(None))
        ).distinct(View.user_id, View.session_id).count()
        
        return unique_views
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def delete_view(db: Session, post_id: int, user_id: str = None, session_id: str = None):
    """
    Удаляет конкретный просмотр поста для пользователя или сессии.
    """
    try:
        query = db.query(View).filter(View.post_id == post_id)
        
        if user_id:
            query = query.filter(View.user_id == user_id)
        elif session_id:
            query = query.filter(View.session_id == session_id)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Either user_id or session_id must be provided"
            )
        
        view = query.first()
        
        if not view:
            raise HTTPException(status_code=404, detail="View not found")
        
        db.delete(view)
        db.commit()
        
        # Инвалидируем кэш
        redis_client.invalidate_keys_by_pattern("posts:cursor:*")
        redis_client.invalidate_keys_by_pattern(f"posts:detail:{post_id}:*")
        
        return {"message": "View deleted successfully"}
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def delete_views_by_post(db: Session, post_id: int):
    """
    Удаляет все просмотры поста.
    """
    try:
        deleted_count = db.query(View).filter(View.post_id == post_id).delete()
        db.commit()
        
        # Инвалидируем кэш
        redis_client.invalidate_keys_by_pattern("posts:cursor:*")
        redis_client.invalidate_keys_by_pattern(f"posts:detail:{post_id}:*")
        
        return deleted_count
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def delete_old_views(db: Session, days: int = 30):
    """
    Удаляет просмотры старше указанного количества дней.
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted_count = db.query(View).filter(View.viewed_at < cutoff_date).delete()
        db.commit()
        
        return deleted_count
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")