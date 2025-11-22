from typing import List
from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from fastapi import HTTPException
from app.models.project import Project

def get_favorites_count(db: Session, project_id: int):
    return db.query(Favorite).filter(Favorite.project_id == project_id).count()

def is_favorite(db: Session, project_id: int, user_id: int):
    return db.query(Favorite).filter(Favorite.project_id == project_id, Favorite.user_id == user_id).first() is not None
    
def add_favorite(db: Session, user_id: int, project_id: int):
    favorite = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.project_id == project_id).first()
    if favorite:
        return favorite
    favorite = Favorite(user_id=user_id, project_id=project_id)
    project = db.query(Project).filter(Project.id == project_id).first()
    project.is_favorite = True
    db.add(project)
    db.commit()
    db.refresh(project)
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
    project = db.query(Project).filter(Project.id == project_id).first()
    project.is_favorite = False
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"detail": "Favorite removed"}

def get_favorites_by_user(db: Session, user_id: int) -> List[Favorite]:
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()