from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.specialization import Specialization
from app.models.user import UserRole, UserStatus
from app.schemas.common import ProjectShort
from app.schemas.skill import SkillOut
from app.schemas.specialization import SpecializationOut

class UserBase(BaseModel):
    id : Optional[int] = None
    wallet_address: str
    name: str
    role: Optional[UserRole] = UserRole.developer
    level: int = 0
    image_url: Optional[str] = "https://i.sstatic.net/34AD2.jpg"
    banner_url: Optional[str] = "https://www.visual.com.br/wp-content/uploads/2019/12/banner-default-1900.jpg"
    timezone: Optional[str] = None
    region: Optional[str] = None
    status: UserStatus = UserStatus.offline
    completed_orders_count: int = 0
    repeat_orders: int = 0
    rating: float = 0.0
    favorites_count : int
    verified: bool = False
    description: Optional[str] = "No description"
    projects: Optional[List[ProjectShort]] = None
    skills: Optional[List[SkillOut]] = None
    specializations: Optional[List[SpecializationOut]] = None
    request_count : int
    monthly_requests_count : int
    model_config = {
            "use_enum_values": True,
        "from_attributes": True
        }


class UserCreate(UserBase):
    wallet_address: str
    role: str
    status: str

class UserUpdate(BaseModel):
    role: Optional[str] = None
    level: Optional[int] = None
    image_url: Optional[str] = None
    banner_url: Optional[str] = None
    description: Optional[str] = None
    region: Optional[str] = None
    timezone: Optional[str] = None
    status: Optional[str] = None
    name: Optional[str] = None

class UserOut(UserBase):
    id: int
    created_at: datetime
    request_count : int
    model_config = {"from_attributes": True}

