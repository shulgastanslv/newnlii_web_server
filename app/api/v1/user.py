from datetime import datetime
import secrets
from fastapi import FastAPI, HTTPException, status, BackgroundTasks, Depends, APIRouter
import random
from pydantic import BaseModel
from fastapi import status
from sqlalchemy.orm import Session
from app.redis_client import redis_client
from app.api.deps import get_db
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut, UserUpdate
from typing import List
import resend
from passlib.context import CryptContext

router = APIRouter()

resend.api_key = "re_gMYqDpqM_KpN8q5CnVSYzGLXtPVh5VzNA"

@router.get("/", response_model=List[UserOut])
def get_all_users_route(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id_route(
    user_id: str, 
    db: Session = Depends(get_db)
):
    return crud_user.get_user_by_id(db, user_id)

@router.get("/email/{email}", response_model=UserOut)
def get_user_by_email_route(email: str, db: Session = Depends(get_db)):
    return crud_user.get_user_by_email(db, email)

@router.post("/", response_model=UserOut)
def create_user_route(user : UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(user, db)

@router.patch("/update", response_model=UserOut)
def update_user_route(user : UserUpdate, db: Session = Depends(get_db)):
    return crud_user.update_user(db, user)


class ForgotPasswordRequest(BaseModel):
    email: str

class VerifyCodeRequest(BaseModel):
    email: str
    code: str

class ResetPasswordRequest(BaseModel):
    email: str
    password: str
    reset_token: str 
    
def send_reset_code_email(email: str, code: str):
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": "Код сброса пароля",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2>Ваш код для сброса пароля</h2>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; 
                           text-align: center; font-size: 24px; font-weight: bold; 
                           letter-spacing: 4px; color: #333;">
                    {code}
                </div>
                <p style="margin-top: 20px;">Код действителен 10 минут.</p>
                <p style="color: #666;">Если вы не запрашивали сброс пароля, проигнорируйте это письмо.</p>
            </div>
            """
        })
        print(f"Код отправлен на {email}")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest, 
    background_tasks: BackgroundTasks
):
    email = request.email
    
    code = f"{random.randint(100000, 999999)}"
    
    redis_client.setex(
        f"reset_code:{email}", 
        600,  # 10 минут
        code
    )
    
    background_tasks.add_task(send_reset_code_email, email, code)
    
    return {
        "success": True, 
        "message": "Код отправлен на вашу почту"
    }
    
@router.post("/verify-code")
async def verify_code(request: VerifyCodeRequest):
    """Проверка кода подтверждения"""
    email = request.email
    code = request.code
    
    stored_code = redis_client.get(f"reset_code:{email}")
    
    if not stored_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Код не найден или истек"
        )
    
    if stored_code.decode('utf-8') != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный код"
        )
    
    redis_client.delete(f"reset_code:{email}")
    reset_token = secrets.token_urlsafe(32)

    redis_client.setex(f"reset_token:{email}", 600, reset_token)
    
    return {
        "success": True,
        "reset_token": reset_token,
        "message": "Код подтвержден"
    }
    
    
@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest,  db: Session = Depends(get_db)):
    email = request.email
    password = request.password
    pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

    if len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен содержать минимум 6 символов"
        )
    
    stored_token = redis_client.get(f"reset_token:{email}")
    
    if not stored_token or stored_token.decode() != request.reset_token:
        raise HTTPException(400, "Неверный или истекший токен")
  
    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    
    hashed_password = pwd_context.hash(password)
    update = UserUpdate(
        id=user.id,
        password = hashed_password
    )
    crud_user.update_user(db, update)
    redis_client.delete(f"reset_code:{email}")
    redis_client.delete(f"reset_token:{email}")
    
    return {
        "success": True,
        "message": "Пароль успешно изменен"
    }
