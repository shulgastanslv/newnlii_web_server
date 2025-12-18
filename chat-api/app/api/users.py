from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud import user as crud_user

router = APIRouter()

@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud_user.get_user_by_id(db, user_id)


@router.get("/users/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)

