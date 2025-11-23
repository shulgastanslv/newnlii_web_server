from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String, Float, func, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class TransactionStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    failed = "failed"

from sqlalchemy import Enum

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    transaction_hash = Column(String, unique=True, nullable=False, index=True)
    from_address = Column(String, nullable=False)
    to_address = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(TransactionStatus, name="transaction_status_enum"), default=TransactionStatus.pending, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    confirmed_at = Column(DateTime, nullable=True)
    blockchain_type = Column(Integer, nullable=True, default=0)  # 0 = ETH, 1 = BSC, etc.
    error_message = Column(Text, nullable=True)  # Сообщение об ошибке, если транзакция failed
    
    order = relationship("Order", backref="transactions")

