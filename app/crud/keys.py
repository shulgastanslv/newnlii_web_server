from typing import List
from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from fastapi import HTTPException
from app.models.keys import Keys
from app.models.project import Project
from key_generator.key_generator import generate
from app.schemas.keys import KeyCreate, KeysOut

def create_key(db: Session, email: str):
    exists = db.query(Keys).filter(Keys.email == email).first()
    if exists:
        raise HTTPException(status_code=404, detail="Email already added!")
    key = generate(seed=101).get_key()
    print(key)
    print(email)
    entry = Keys(
        email = email,
        key=key
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return key

def remove_key(db: Session, id : int):
    key = db.query(Keys).filter(Keys.id == id).first()
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    db.delete(key)
    db.commit()
    db.refresh(key)
    return "Key was removed"

def get_all_keys(db: Session) -> List[KeysOut]:
    return db.query(Keys).all()

def valid_key(db: Session, key : str) -> bool:
    if db.query(Keys).filter(Keys.key == key).first(): 
        return True
    return False