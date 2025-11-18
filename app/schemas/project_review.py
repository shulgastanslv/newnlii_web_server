from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.user import UserOut

class ProjectReviewCreate(BaseModel):
    project_id: int
    user_id: int
    score: float
    text: str

class ProjectReviewOut(BaseModel):
    id: int
    project_id: int
    user_id: int
    score: float
    text: str
    created_at: datetime
    user : UserOut
    class Config:
        orm_mode = True