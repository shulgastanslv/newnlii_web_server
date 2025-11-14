from typing import List, Optional
from pydantic import BaseModel
from app.schemas.shared import ProjectBase

class ProjectCreate(ProjectBase):
    category_id: int
    image_url: str
    budget: int
    crypto_type : str
    tags: Optional[List[str]] = []
    skills: Optional[List[str]] = []

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    budget: Optional[int] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    skills: Optional[List[str]] = None