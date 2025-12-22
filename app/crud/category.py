from collections import Counter
import json
from pathlib import Path
from sqlalchemy import func
from sqlalchemy.orm import Session
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
    from sqlalchemy.orm import selectinload
    return db.query(Category).options(selectinload(Category.subcategories)).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_popular_categories(db: Session):
    result = db.query(Category).join(Project, Category.id == Project.category_id).order_by(func.count(Project.id).desc()).group_by(Category.id).limit(5).all()
    return result