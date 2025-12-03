from http.client import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import keys as crud_keys
from app.schemas.keys import KeysOut

router = APIRouter()
 
class AuthResponse(BaseModel):
    key : str
    email : str

class AuthRequest(BaseModel):
    key  : str

class CreateKeyRequest(BaseModel):
    email  : str

class RemoveKeyRequest(BaseModel):
    id  : int

@router.post("/valid_key", response_model=bool)
def auth_user(request: AuthRequest, db: Session = Depends(get_db)):
    return crud_keys.valid_key(db, request.key)

@router.post("/create_key", response_model=str)
def auth_user(request: CreateKeyRequest, db: Session = Depends(get_db)):
    return crud_keys.create_key(db, request.email)

@router.delete("/remove_key", response_model=str)
def auth_user(request: RemoveKeyRequest, db: Session = Depends(get_db)):
    return crud_keys.remove_key(db, request.id)

@router.get("/keys", response_model=List[KeysOut])
def auth_user(db: Session = Depends(get_db)):
    return crud_keys.get_all_keys(db)
