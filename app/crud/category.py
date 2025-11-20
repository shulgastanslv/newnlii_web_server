import json
from sqlalchemy.orm import Session
from app.redis_client import redis_client
from app.models.category import Category
from app.models.project import Project
from app.schemas.category import CategoryCreate, CategoryOut
from app.schemas.project import ProjectCreate

def create_category(db: Session, ctg: CategoryCreate):
    res = Category(
        name=ctg.name,
        parent_id = ctg.parent_id
    )
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

def get_all_categories(db : Session):
    return db.query(Category).all()

def get_all_categories_cached(db: Session):
    cached_categories = redis_client.get("all_categories")
    if cached_categories:
        categories_data = json.loads(cached_categories)
        # Возвращаем список Pydantic моделей, десериализованных из кеша
        return [CategoryOut(**cd) for cd in categories_data]

    categories = db.query(Category).all()
    response = [CategoryOut.model_validate(category) for category in categories]
    json_data = json.dumps([item.model_dump() for item in response])
    redis_client.set("all_categories", json_data, ex=300)  # кешировать 5 минут
    return response