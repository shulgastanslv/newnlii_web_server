from datetime import datetime, timedelta
from uuid import uuid4
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError, IntegrityError
from fastapi import HTTPException
from app.crypto import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.redis_client import redis_client

def _user_to_cache(user: User) -> dict:
    return UserOut.model_validate(user).model_dump()

def _cache_user(user: User, expiration: int = 600):  # 10 минут
    key = f"user:{user.id}"
    redis_client.setex(key, expiration, _user_to_cache(user))

def _uncache_user(user_id: str):
    redis_client.delete(f"user:{user_id}")

def get_user_by_id(db: Session, id: str):
    cache_key = f"user:{id}"
    cached = redis_client.get_json(cache_key)
    if cached:
        return UserOut.model_validate(cached)

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    _cache_user(user)
    return UserOut.model_validate(user)

def get_user_by_email(db: Session, email: str):
    email_cache_key = f"user:email:{email}"
    cached = redis_client.get_json(email_cache_key)
    if cached:
        return UserOut.model_validate(cached)

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    _cache_user(user)  # user:{id}
    redis_client.setex(
        email_cache_key,
        60 * 10,  # 10 минут
        UserOut.model_validate(user).model_dump(),
    )

    return UserOut.model_validate(user)

def create_user(user_create: UserCreate, db: Session):
    try:
        moscow_time = datetime.utcnow() + timedelta(hours=3)
        userId = user_create.user_id
        if user_create.is_google:
            hashed_password = None
        else:
            if not user_create.password:
                raise HTTPException(
                    status_code=400,
                    detail="Password is required for non‑Google users"
                )
            hashed_password = hash_password(password=user_create.password)
            userId=str(uuid4()),

        db_user = User(
            id=userId,
            username=user_create.username or userId,
            password=hashed_password,
            email=user_create.email,
            created_at=moscow_time,
            is_google=user_create.is_google,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        _cache_user(db_user)
        redis_client.setex(
            f"user:email:{db_user.email}",
            60 * 10,
            UserOut.model_validate(db_user).model_dump(),
        )

        return UserOut.model_validate(db_user)


    except (DataError, IntegrityError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"User error while creating: {str(e)}")

class UpdatePassword(BaseModel):
    password: str  # незахэшированный новый пароль
    
def update_password(db: Session, user_id: int, new_password: str) -> UserOut:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hash_password(new_password)

    db_user.password = hashed_password  

    db.commit()
    db.refresh(db_user)

    _uncache_user(db_user.id)
    _cache_user(db_user)
    if db_user.email:
        redis_client.setex(
            f"user:email:{db_user.email}",
            60 * 10,
            UserOut.model_validate(db_user).model_dump(),
        )

    return UserOut.model_validate(db_user)


def update_user(db: Session, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_update.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    # обновляем кэш по id и по email
    _uncache_user(db_user.id)
    _cache_user(db_user)
    if db_user.email:
        redis_client.setex(
            f"user:email:{db_user.email}",
            60 * 10,
            UserOut.model_validate(db_user).model_dump(),
        )

    return UserOut.model_validate(db_user)

def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.email:
        redis_client.delete(f"user:email:{db_user.email}")

    db.delete(db_user)
    db.commit()

    _uncache_user(user_id)
    return {"message": "User deleted"}

def get_users(db: Session):
    users = db.query(User).all()
    return [UserOut.model_validate(u) for u in users]
