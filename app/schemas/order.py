from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.models.order import Status
from app.schemas.project import ProjectOut
from app.schemas.user import UserOut
from app.schemas.project_image import ProjectImageOut

class OrderBase(BaseModel):
    project_id: int
    client_id: int
    developer_id: Optional[int] = None
    deadline : Optional[datetime] = None
    budget : float
    status: Optional[Status] = Status.open

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[Status] = None
    developer_id: Optional[int] = None

class OrderOut(OrderBase):
    id: int
    git_url: Optional[str] = None
    created_at: datetime
    project : ProjectOut
    client : UserOut
    developer : UserOut
    model_config = {
        "from_attributes": True
    }
