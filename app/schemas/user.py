from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.user import UserRole, UserStatus
from app.schemas.skill import SkillOut

class ProjectShort(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    wallet_address: str
    name: str
    role: Optional[UserRole] = UserRole.developer
    level: int = 0
    image_url: Optional[str] = "https://i.sstatic.net/34AD2.jpg"
    banner_url: Optional[str] = "https://www.visual.com.br/wp-content/uploads/2019/12/banner-default-1900.jpg"
    timezone: Optional[str] = None
    region: Optional[str] = None
    status: UserStatus = UserStatus.offline
    completed_orders: int = 0
    repeat_orders: int = 0
    rating: float = 0.0
    verified: bool = False
    description: Optional[str] = "No description"
    projects: Optional[List[ProjectShort]] = None


class UserCreate(UserBase):
    wallet_address: str
    role: str
    status: str

class UserUpdate(BaseModel):
    role: Optional[str] = None
    level: Optional[int] = None
    image_url: Optional[str] = None
    name: Optional[str] = None

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
