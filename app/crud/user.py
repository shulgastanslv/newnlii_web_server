from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from fastapi import HTTPException
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    try:
        db_user = User(
         
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except (DataError, IntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
