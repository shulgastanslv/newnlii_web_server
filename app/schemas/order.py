from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class OrderStatusEnum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class OrderBase(BaseModel):
    project_id: int
    client_id: int
    developer_id: Optional[int] = None
    deadline : Optional[datetime] = None
    budget :int
    status: Optional[OrderStatusEnum] = OrderStatusEnum.pending

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatusEnum] = None
    developer_id: Optional[int] = None

class OrderOut(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
