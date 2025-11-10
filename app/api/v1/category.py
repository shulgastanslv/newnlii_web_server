from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import category as crud_category
from app.schemas.category import CategoryCreate, CategoryOut
from typing import List

router = APIRouter()

@router.post("/create-category", response_model=CategoryOut)
def create_category(value: CategoryCreate, db: Session = Depends(get_db)):
    return crud_category.create_category(db, value)

@router.get("/", response_model=List[CategoryOut])
def get_all_project(db: Session = Depends(get_db)):
    return crud_category.get_all_categories(db)
