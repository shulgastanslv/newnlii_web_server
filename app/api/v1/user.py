from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut, UserUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.get("/{id}", response_model=UserOut)
def read_user(id: int, db: Session = Depends(get_db)):
    return crud_user.get_user_by_id(db, id)

@router.patch("/{id}", response_model=UserOut)
def update_user(id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    return crud_user.update_user(db, id, update_data)