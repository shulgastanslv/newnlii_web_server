import json
from pathlib import Path
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
    project_root = Path(__file__).parent.parent.parent
    categories_file = project_root / "categories.json"
    
    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
        
        response = [CategoryOut(**category) for category in categories_data]
        json_data = json.dumps([item.model_dump() for item in response])
        redis_client.set("all_categories", json_data, ex=300)
        return response
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл categories.json не найден по пути: {categories_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка при чтении JSON файла: {e}")