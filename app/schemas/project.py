from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    category_id: int
    image_url: str
    budget: int

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    budget: Optional[int] = None
    category_id: Optional[int] = None

class ProjectOut(ProjectBase):
    id: int
    image_url : str
    description : str
    category_id : int
    owner_id : int
    created_at: datetime
    budget : int
    class Config:
        orm_mode = True
