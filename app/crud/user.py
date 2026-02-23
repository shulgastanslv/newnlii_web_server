from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate

def get_users (db: Session):
    users = db.query(User).all()
    return users

def create_user (user : UserCreate, db : Session):
    try:
        db_user = User(
          username = user.username,
          password = user.password,
          email = user.email,
        )
        print(str(db_user))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except (DataError, IntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"User error while creating: {str(e)}")
    
def get_user_by_email(db: Session, email: str):
    print("get by email")
    user = db.query(User).filter(User.email == email).first()
    print(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user