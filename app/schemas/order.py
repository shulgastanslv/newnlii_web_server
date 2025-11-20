from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.order import Status
from app.schemas.project import ProjectOut

class OrderBase(BaseModel):
    project_id: int
    client_id: int
    developer_id: Optional[int] = None
    deadline : Optional[datetime] = None
    budget :int
    status: Optional[Status] = Status.open

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[Status] = None
    developer_id: Optional[int] = None

class OrderOut(OrderBase):
    id: int
    created_at: datetime
    project : ProjectOut
    model_config = {
        "from_attributes": True
    }
