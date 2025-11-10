from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from typing import List
from app.crud import user_skills as crud_skills
from app.schemas.skill import SkillOut
from app.schemas.user import UserOut

router = APIRouter()

@router.post("/{user_id}/add-skill", response_model=UserOut)
def add_skill(user_id: int, skill_id: int, db: Session = Depends(get_db)):
    print(user_id)
    print(skill_id)
    return crud_skills.add_skill_to_user(db, user_id, skill_id)

@router.delete("/{user_id}", response_model=UserOut)
def remove_skill(user_id: int, skill_id: int, db: Session = Depends(get_db)):
    return crud_skills.remove_skill_from_user(db, user_id, skill_id)

@router.get("/{user_id}", response_model=List[SkillOut])
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    return crud_skills.get_user_skills(db, user_id)
