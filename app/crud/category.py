from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.models.category import Category
from app.models.project import Project
from app.schemas.category import CategoryCreate
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