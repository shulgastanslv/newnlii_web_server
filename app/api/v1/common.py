from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import category as category_crud
from app.models.user import User
from app.schemas.category import CategoryOut

router = APIRouter()

@router.get("/popular-categories", response_model=List[CategoryOut])
def get_popular_categories(db: Session = Depends(get_db)):
    return category_crud.get_popular_categories(db)

def calculate_profile_fill_level(user: User) -> int:
    fields = {
        "name": (user.name, 10),
        "image_url": (user.image_url, 10),
        "banner_url": (user.banner_url, 10),
        "description": (user.description, 15),
        "region": (user.region, 10),
        "timezone": (user.timezone, 10),
        "skills": (user.skills, 15),
        "specializations": (user.specializations, 20),
    }

    score = sum(weight for value, weight in fields.values() if value)
    return min(score, 100)

@router.get("/profile_fill_level/{user_id}", response_model=int)
def profile_fill_level_route(user_id : int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return calculate_profile_fill_level(user)


