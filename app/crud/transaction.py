from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from fastapi import HTTPException
from datetime import datetime
from app.models.transaction import TransactionStatus

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction_by_id(db: Session, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

def get_transaction_by_hash(db: Session, transaction_hash: str):
    transaction = db.query(Transaction).filter(Transaction.transaction_hash == transaction_hash).first()
    return transaction

def get_all_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()

def get_transactions_by_order(db: Session, order_id: int):
    return db.query(Transaction).filter(Transaction.order_id == order_id).all()

def update_transaction(db: Session, transaction_id: int, transaction_update: TransactionUpdate):
    transaction = get_transaction_by_id(db, transaction_id)
    for key, value in transaction_update.dict(exclude_unset=True).items():
        setattr(transaction, key, value)
    if transaction_update.status == TransactionStatus.confirmed and not transaction.confirmed_at:
        transaction.confirmed_at = datetime.utcnow()
    db.commit()
    db.refresh(transaction)
    return transaction

def update_transaction_by_hash(db: Session, transaction_hash: str, transaction_update: TransactionUpdate):
    transaction = get_transaction_by_hash(db, transaction_hash)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction_update.dict(exclude_unset=True).items():
        setattr(transaction, key, value)
    if transaction_update.status == TransactionStatus.confirmed and not transaction.confirmed_at:
        transaction.confirmed_at = datetime.utcnow()
    db.commit()
    db.refresh(transaction)
    return transaction

def delete_transaction(db: Session, transaction_id: int):
    transaction = get_transaction_by_id(db, transaction_id)
    db.delete(transaction)
    db.commit()
    return {"detail": "Transaction deleted"}

