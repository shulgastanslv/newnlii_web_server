from typing import List, Optional
from pydantic import BaseModel
from app.schemas.project_image import ProjectImageOut


class ProjectShort(BaseModel):
    id: int
    name: str
    category_id: int
    description: str
    budget: float
    crypto_type: int
    images: Optional[List[ProjectImageOut]] = None
    visible : bool
    model_config = {"from_attributes": True}
