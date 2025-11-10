from pydantic import BaseModel, EmailStr
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    owner_id : int

class ProjectOut(ProjectBase):
    id: int
    image_url : str
    description : str
    owner_id : int
    category_id : int
    created_at: datetime
    budget : int
    class Config:
        orm_mode = True
