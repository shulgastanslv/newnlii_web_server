from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from typing import List
from app.crud import skill as crud_skill
from app.schemas.skill import SkillCreate, SkillOut

router = APIRouter()

@router.post("/create-skill", response_model=SkillOut)
def create_skill(value: SkillCreate, db: Session = Depends(get_db)):
    return crud_skill.create_skill(db, value)

@router.get("/", response_model=List[SkillOut])
def get_all_skills(db: Session = Depends(get_db)):
    return crud_skill.get_all_skills(db)