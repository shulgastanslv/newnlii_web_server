from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from typing import List
from app.crud import specialization as crud_specialization
from app.schemas.specialization import SpecializationCreate, SpecializationOut

router = APIRouter()

@router.post("/create-specialization", response_model=SpecializationOut)
def create_specialization(value: SpecializationCreate, db: Session = Depends(get_db)):
    return crud_specialization.create_specialization(db, value)

@router.get("/", response_model=List[SpecializationOut])
def get_all_specializations(db: Session = Depends(get_db)):
    return crud_specialization.get_all_specializations(db)