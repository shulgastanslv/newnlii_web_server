from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ProjectImageBase(BaseModel):
    image_url: str
    alt_text: Optional[str] = None
    order: int = 0
    is_primary: bool = False

class ProjectImageCreate(ProjectImageBase):
    project_id: int

class ProjectImageUpdate(BaseModel):
    image_url: Optional[str] = None
    alt_text: Optional[str] = None
    order: Optional[int] = None
    is_primary: Optional[bool] = None

class ProjectImageOut(ProjectImageBase):
    id: int
    project_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

