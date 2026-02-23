from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut, UserUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

