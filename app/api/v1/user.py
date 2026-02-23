from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def get_all_users_route(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.post("/", response_model=UserOut)
def create_user_route(user : UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(user, db)