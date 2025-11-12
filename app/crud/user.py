from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserLogin, UserUpdate

def create_user(db: Session, user: UserLogin):
    db_user = User(
        wallet_address=user.wallet_address,
        name=user.name,
        role=user.role,
        level=user.level,
        image_url=user.image_url,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_wallet(db: Session, wallet_address: str):
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_wallet_by_id(id: str, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"wallet_address" : user.wallet_address}

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db: Session, wallet_address: int, update_data: UserUpdate):
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_data.role is not None:
        user.role = update_data.role
    if update_data.level is not None:
        user.level = update_data.level
    if update_data.image_url is not None:
        user.image_url = update_data.image_url
    if update_data.name is not None:
        user.name = update_data.name

    db.commit()
    db.refresh(user)
    return user
