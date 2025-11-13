from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.project import Project
from app.schemas.project import ProjectOut

class UserRoleEnum(str, Enum):
    developer = "Developer"
    customer = "Customer"


class UserRoleStatus(str, Enum):
    developer = "Online"
    customer = "Offline"

class UserBase(BaseModel):
    wallet_address: str
    name: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    level: Optional[int] = 0
    image_url: Optional[str] = None
    banner_url: Optional[str] = None
    timezone: Optional[str] = None
    region: Optional[str] = None
    status: UserRoleStatus = "Offline"
    completed_orders: Optional[int] = 0
    repeat_orders: Optional[int] = 0
    rating: Optional[float] = 0.0
    verified: Optional[bool] = False
    description : Optional[str] = None
    projects: List[ProjectOut] = []

class UserLogin(UserBase):
    wallet_address: str
    signature: str
    message: str

class UserUpdate(BaseModel):
    role: Optional[str] = None
    level: Optional[int] = None
    image_url: Optional[str] = None
    name: Optional[str] = None


class UserWallet(BaseModel):
    wallet_address: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
