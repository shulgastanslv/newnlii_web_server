from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user as crud_user
from app.schemas.user import UserLogin, UserOut, UserUpdate, UserWallet
from typing import List

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_user(user: UserLogin, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/{wallet_address}", response_model=UserOut)
def get_by_wallet(wallet_address: str, db: Session = Depends(get_db)):
    print(wallet_address)
    return crud_user.get_user_by_wallet(db, wallet_address)
    
@router.get("/id/{id}", response_model=UserWallet)
def get_wallet_by_id(id: str, db: Session = Depends(get_db)):
    return crud_user.get_wallet_by_id(id, db)

@router.get("/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.patch("/{wallet_address}", response_model=UserOut)
def update_user(wallet_address: str, update_data: UserUpdate, db: Session = Depends(get_db)):
    return crud_user.update_user(db, wallet_address, update_data)
