from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from typing import List
from app.crud import user_specializations as crud_skills
from app.schemas.specialization import SpecializationOut
from app.schemas.user import UserOut

router = APIRouter()


@router.post("/{user_id}/add-specialization", response_model=UserOut)
def add_specialization(user_id: int, specialization_id: int, db: Session = Depends(get_db)):
    return crud_skills.add_specialization_to_user(db, user_id, specialization_id)

@router.delete("/{user_id}/remove-specialization", response_model=UserOut)
def remove_specialization(user_id: int, specialization_id: int, db: Session = Depends(get_db)):
    return crud_skills.remove_specialization_from_user(db, user_id, specialization_id)

@router.get("/{user_id}", response_model=List[SpecializationOut])
def get_user_specializations(user_id: int, db: Session = Depends(get_db)):
    return crud_skills.get_user_specializations(db, user_id)
