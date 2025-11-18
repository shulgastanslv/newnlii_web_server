from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, constr
from app.schemas.category import CategoryOut
from app.schemas.tag import Tag
from app.schemas.user import UserBase

class ProjectBase(BaseModel):
    name: str
    id : int
    image_url: str
    category_id: int
    description: str
    budget: float
    crypto_type: int
    visible : bool
    tags: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    class Config:
        orm_mode = True

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    image_url: str
    budget: float
    category_id: int
    tags: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    visible: Optional[bool]

class ProjectOut(ProjectBase):
    owner: UserBase
    category: CategoryOut

