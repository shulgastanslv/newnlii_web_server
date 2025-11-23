from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.transaction import TransactionStatus

class TransactionBase(BaseModel):
    order_id: int
    transaction_hash: str
    from_address: str
    to_address: str
    amount: float
    status: Optional[TransactionStatus] = TransactionStatus.pending
    blockchain_type: Optional[int] = 0

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    status: Optional[TransactionStatus] = None
    confirmed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class TransactionOut(TransactionBase):
    id: int
    created_at: datetime
    confirmed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }

