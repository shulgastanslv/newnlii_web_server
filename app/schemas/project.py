from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, constr
from app.schemas.category import CategoryOut
from app.schemas.skill import SkillOut
from app.schemas.tag import Tag
from app.schemas.user import UserBase

class ProjectBase(BaseModel):
    name: str
    id: Optional[int] = None
    category_id: int
    description: str
    budget: float
    crypto_type: int
    visible: bool
    tags: Optional[List[Tag]] = None
    skills: Optional[List[SkillOut]] = None
    short_description: Optional[str] = None
    estimated_duration: Optional[str] = None
    features: Optional[str] = None
    external_links: Optional[str] = None
    packages: Optional[str] = None
    moderation_status: Optional[str] = None
    video_url: Optional[str] = None
    model_config = {
        "from_attributes" : True
    }

class ProjectCreate(ProjectBase):
    id: Optional[int] = None
    skills: Optional[List[int]] = None
    tags: Optional[List[int]] = None
    model_config = {
        "from_attributes" : True
    }

class ProjectUpdate(BaseModel):
    budget: float
    category_id: int
    tags: Optional[List[int]] = None
    skills: Optional[List[int]] = None
    visible: Optional[bool] = None
    model_config = {
        "from_attributes" : True
    }

class ProjectOut(ProjectBase):
    owner: Optional[UserBase]
    category: Optional[CategoryOut] 
    model_config = {
         "use_enum_values": True,
        "from_attributes" : True
    }

