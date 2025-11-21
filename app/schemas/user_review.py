from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.user import UserOut

class UserReviewCreate(BaseModel):
    reviewer_id: int = Field(..., description="ID пользователя, который оставляет отзыв")
    reviewed_user_id: int = Field(..., description="ID пользователя, на которого оставлен отзыв")
    score: float = Field(..., ge=1, le=5, description="Оценка от 1 до 5")
    text: str = Field(default="", description="Текст отзыва")

class UserReviewOut(BaseModel):
    id: int
    reviewer_id: int
    reviewed_user_id: int
    score: float
    text: str
    created_at: datetime
    reviewer: UserOut  # Пользователь, который оставил отзыв
    
    model_config = {
        "from_attributes": True
    }

class UserReviewUpdate(BaseModel):
    score: Optional[float] = Field(None, ge=1, le=5, description="Оценка от 1 до 5")
    text: Optional[str] = Field(None, description="Текст отзыва")

