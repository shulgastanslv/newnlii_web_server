from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        name=user.name,
        role=user.role,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_name(db: Session, name : str):
    return db.query(User).filter(User.name == name).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_name(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user