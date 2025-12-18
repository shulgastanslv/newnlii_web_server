from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import category as category_crud
from app.schemas.category import CategoryOut

router = APIRouter()

@router.get("/popular-categories", response_model=List[CategoryOut])
def get_popular_categories(db: Session = Depends(get_db)):
    return category_crud.get_popular_categories(db)

