from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.specialization import Specialization

def add_specialization_to_user(db: Session, user_id: int, specialization_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    spec = db.query(Specialization).filter(Specialization.id == specialization_id).first()
    if not user or not spec:
        raise HTTPException(status_code=404, detail="User or Specialization not found")

    if spec not in user.specializations:
        user.specializations.append(spec)
        db.commit()
        db.refresh(user)
    return user

def remove_specialization_from_user(db: Session, user_id: int, specialization_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    spec = db.query(Specialization).filter(Specialization.id == specialization_id).first()
    if not user or not spec:
        raise HTTPException(status_code=404, detail="User or Specialization not found")

    if spec in user.specializations:
        user.specializations.remove(spec)
        db.commit()
        db.refresh(user)
    return user

def get_user_specializations(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.specializations
