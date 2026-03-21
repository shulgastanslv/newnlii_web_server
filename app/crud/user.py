from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from uuid import uuid4

def get_users (db: Session):
    users = db.query(User).all()
    return users

def update_user(db: Session, user_update: UserUpdate): 
    db_user = db.query(User).filter(User.id == user_update.id).first() 
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def create_user (user : UserCreate, db : Session):
    try:
        moscow_time = datetime.utcnow() + timedelta(hours=3)
        user_id = str(uuid4())

        db_user = User(
          id = user_id,
          username = user.username or user_id,
          password = user.password,
          email = user.email,
          created_at = moscow_time,
          is_google = user.is_google
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except (DataError, IntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"User error while creating: {str(e)}")
    
def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_id (db: Session, id : str):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user