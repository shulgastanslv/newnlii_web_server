from typing import List
from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from fastapi import HTTPException


def add_favorite(db: Session, user_id: int, project_id: int):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.project_id == project_id).first()
    if favorite:
        return favorite
    favorite = Favorite(user_id=user_id, project_id=project_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

def remove_favorite(db: Session, user_id: int, project_id: int):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.project_id == project_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
    return {"detail": "Favorite removed"}

def get_favorites_by_user(db: Session, user_id: int) -> List[Favorite]:
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()