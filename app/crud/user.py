from http.client import HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        name=user.name,
        role=user.role,
        level = user.level,
        avatar_url = user.avatar_url,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_name(db: Session, name : str):
    return db.query(User).filter(User.name == name).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_name(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db: Session, user_id: int, update_data: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_data.role is not None:
        user.role = update_data.role
    if update_data.level is not None:
        user.level = update_data.level
    if update_data.avatar_url is not None:
        user.avatar_url = update_data.avatar_url

    db.commit()
    db.refresh(user)
    return user