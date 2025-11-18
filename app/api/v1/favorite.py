from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import favorite as crud_favorite
from app.schemas.favorite import FavoriteCreate, FavoriteOut
from typing import List

router = APIRouter()

@router.post("/", response_model=FavoriteOut)
def add_favorite(data: FavoriteCreate, user_id: int, db: Session = Depends(get_db)):
    return crud_favorite.add_favorite(db, user_id=user_id, project_id=data.project_id)

@router.delete("/", response_model=dict)
def remove_favorite(project_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud_favorite.remove_favorite(db, user_id=user_id, project_id=project_id)

@router.get("/", response_model=List[FavoriteOut])
def get_user_favorites(user_id: int, db: Session = Depends(get_db)):
    return crud_favorite.get_favorites_by_user(db, user_id=user_id)
