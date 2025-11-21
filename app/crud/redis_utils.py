import json
from sqlalchemy.orm import Session
from app.redis_client import redis_client
from app.models.project import Project
from app.models.category import Category
from app.schemas.project import ProjectOut
from app.schemas.category import CategoryOut

def clear_redis_cache(pattern: str = None):
    """Очистить кеш Redis
    
    Args:
        pattern: Если указан, удаляет только ключи, соответствующие паттерну (например, "all_*")
                 Если None, очищает всю базу данных Redis
    """
    if pattern:
        # Удаляем ключи по паттерну
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            return {"detail": f"Cleared {len(keys)} keys matching pattern '{pattern}'"}
        return {"detail": f"No keys found matching pattern '{pattern}'"}
    else:
        # Очищаем всю базу данных
        redis_client.flushdb()
        return {"detail": "All Redis cache cleared"}

def refresh_projects_cache(db: Session):
    """Перезаписать кеш проектов из базы данных"""
    projects = db.query(Project).all()
    # Используем тот же метод, что и в get_all_projects_cached
    try:
        # Пробуем использовать from_orm (Pydantic v1)
        response = [ProjectOut.from_orm(project) for project in projects]
        json_data = json.dumps([item.dict() for item in response], default=str)
    except AttributeError:
        # Если from_orm не доступен, используем model_validate (Pydantic v2)
        response = [ProjectOut.model_validate(project) for project in projects]
        json_data = json.dumps([item.model_dump() for item in response], default=str)
    redis_client.set("all_projects", json_data, ex=300)
    return {"detail": f"Projects cache refreshed with {len(projects)} projects"}

def refresh_categories_cache(db: Session):
    """Перезаписать кеш категорий из базы данных"""
    categories = db.query(Category).all()
    response = [CategoryOut.model_validate(category) for category in categories]
    json_data = json.dumps([item.model_dump() for item in response], default=str)
    redis_client.set("all_categories", json_data, ex=300)
    return {"detail": f"Categories cache refreshed with {len(categories)} categories"}

def refresh_all_cache(db: Session):
    """Перезаписать весь кеш из базы данных"""
    projects_result = refresh_projects_cache(db)
    categories_result = refresh_categories_cache(db)
    return {
        "detail": "All cache refreshed",
        "projects": projects_result,
        "categories": categories_result
    }

def get_redis_keys(pattern: str = "*"):
    """Получить список всех ключей в Redis
    
    Args:
        pattern: Паттерн для поиска ключей (по умолчанию "*" - все ключи)
    
    Returns:
        Список ключей
    """
    keys = redis_client.keys(pattern)
    return {"keys": keys, "count": len(keys)}

