from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_db
from app.crud import redis_utils

router = APIRouter()

@router.delete("/clear")
def clear_cache(
    pattern: Optional[str] = Query(None, description="Паттерн для удаления ключей (например, 'all_*'). Если не указан, очищается вся база данных")
):
    """Очистить кеш Redis
    
    - Если указан pattern: удаляет только ключи, соответствующие паттерну
    - Если pattern не указан: очищает всю базу данных Redis
    """
    try:
        return redis_utils.clear_redis_cache(pattern)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")

@router.post("/refresh/projects")
def refresh_projects_cache(db: Session = Depends(get_db)):
    """Перезаписать кеш проектов из базы данных"""
    try:
        return redis_utils.refresh_projects_cache(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing projects cache: {str(e)}")

@router.post("/refresh/categories")
def refresh_categories_cache(db: Session = Depends(get_db)):
    """Перезаписать кеш категорий из базы данных"""
    try:
        return redis_utils.refresh_categories_cache(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing categories cache: {str(e)}")

@router.post("/refresh/all")
def refresh_all_cache(db: Session = Depends(get_db)):
    """Перезаписать весь кеш из базы данных"""
    try:
        return redis_utils.refresh_all_cache(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing cache: {str(e)}")

@router.get("/keys")
def get_redis_keys(
    pattern: str = Query("*", description="Паттерн для поиска ключей (по умолчанию '*' - все ключи)")
):
    """Получить список всех ключей в Redis"""
    try:
        return redis_utils.get_redis_keys(pattern)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting keys: {str(e)}")

