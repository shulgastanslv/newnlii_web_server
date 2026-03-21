from http.client import HTTPException
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut, UserUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def get_all_users_route(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id_route(
    user_id: str, 
    db: Session = Depends(get_db)
):
    return crud_user.get_user_by_id(db, user_id)

@router.get("/email/{email}", response_model=UserOut)
def get_user_by_email_route(email: str, db: Session = Depends(get_db)):
    return crud_user.get_user_by_email(db, email)

@router.post("/", response_model=UserOut)
def create_user_route(user : UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(user, db)

@router.patch("/update", response_model=UserOut)
def update_user_route(user : UserUpdate, db: Session = Depends(get_db)):
    return crud_user.update_user(db, user)