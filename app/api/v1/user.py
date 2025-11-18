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

@router.post("/login", response_model=UserOut)
def login_user(wallet_address: str, db: Session = Depends(get_db)):
    user = crud_user.login_or_create_user(wallet_address, db)
    return user

@router.get("/{wallet_address}", response_model=UserOut)
def get_user_by_wallet(wallet_address: str, db: Session = Depends(get_db)):
    return crud_user.get_user_by_wallet(db, wallet_address)

@router.get("/id/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    return crud_user.get_user_by_id(db, user_id)

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.patch("/{wallet_address}", response_model=UserOut)
def update_user(wallet_address: str, update_data: UserUpdate, db: Session = Depends(get_db)):
    return crud_user.update_user(db, wallet_address, update_data)

@router.patch("/{wallet_address}/role", response_model=UserOut)
def change_user_role(wallet_address: str, new_role: str, db: Session = Depends(get_db)):
    return crud_user.update_user_role(db, wallet_address, new_role)
