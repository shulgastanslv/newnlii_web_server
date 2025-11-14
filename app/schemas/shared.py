from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: str

class UserRoleEnum(str, Enum):
    developer = "Developer"
    customer = "Customer"

class UserRoleStatus(str, Enum):
    developer = "Online"
    customer = "Offline"
    
class ProjectShort(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    created_at: Optional[datetime] = None
    budget: Optional[int] = None
    rating: Optional[float] = None
    is_favorite: Optional[bool] = None

    class Config:
        orm_mode = True

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
    projects : Optional[List[ProjectShort]] = None

class ProjectOut(ProjectBase):
    id: int
    image_url : str
    description : str
    category_id : int
    owner_id : int
    created_at: datetime
    budget : int
    crypto_type : str
    rating : float
    reviews_count : int
    is_favorite : bool
    owner: UserBase
    class Config:
        orm_mode = True