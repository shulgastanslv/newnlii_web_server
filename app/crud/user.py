from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from fastapi import HTTPException
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate, UserUpdate

def create_user(db: Session, user: UserCreate):
    try:
        db_user = User(
            wallet_address=user.wallet_address,
            name=user.name,
            role=user.role,
            status=user.status,
            banner_url = user.banner_url,
            level=user.level,
            image_url=user.image_url,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except (DataError, IntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")


def get_user_by_wallet(db: Session, wallet_address: str):
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def login_or_create_user(wallet_address: str, db: Session):
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if user:
        return user
    user_in = UserCreate(
        wallet_address=wallet_address,
        role=UserRole.developer,
        name=f'{wallet_address}',
        status=UserStatus.online,
    )
    user = create_user(db, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="Failed to create user")
    return user


def update_user_role(db: Session, wallet_address: str, new_role: str):
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        user.role = new_role
        db.commit()
        db.refresh(user)
        return user
    except (DataError, IntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")


def get_wallet_by_id(id: str, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"wallet_address": user.wallet_address}


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, id: str):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db: Session, wallet_address: str, update_data: UserUpdate):
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        if update_data.role is not None:
            user.role = update_data.role
        if update_data.level is not None:
            user.level = update_data.level
        if update_data.image_url is not None:
            user.image_url = update_data.image_url
        if update_data.name is not None:
            user.name = update_data.name
        if update_data.banner_url is not None:
            user.banner_url = update_data.banner_url
        if update_data.description is not None:
            user.description = update_data.description
        if update_data.region is not None:
            user.region = update_data.region
        if update_data.timezone is not None:
            user.timezone = update_data.timezone
        if update_data.status is not None:
            user.status = update_data.status
        db.commit()
        db.refresh(user)
        return user
    except (DataError, IntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
