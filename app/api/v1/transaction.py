from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db
from app.models.transaction import Transaction, TransactionStatus
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.crud import transaction as crud_transaction

router = APIRouter()

@router.post("/", response_model=TransactionOut)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Проверяем, не существует ли уже транзакция с таким hash
    existing = crud_transaction.get_transaction_by_hash(db, transaction.transaction_hash)
    if existing:
        raise HTTPException(status_code=400, detail="Transaction with this hash already exists")
    return crud_transaction.create_transaction(db, transaction)

@router.get("/{transaction_id}", response_model=TransactionOut)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return crud_transaction.get_transaction_by_id(db, transaction_id)

@router.get("/hash/{transaction_hash}", response_model=TransactionOut)
def read_transaction_by_hash(transaction_hash: str, db: Session = Depends(get_db)):
    transaction = crud_transaction.get_transaction_by_hash(db, transaction_hash)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/", response_model=List[TransactionOut])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_transaction.get_all_transactions(db, skip=skip, limit=limit)

@router.get("/order/{order_id}", response_model=List[TransactionOut])
def read_transactions_by_order(order_id: int, db: Session = Depends(get_db)):
    return crud_transaction.get_transactions_by_order(db, order_id)

@router.put("/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_id: int, 
    transaction_update: TransactionUpdate, 
    db: Session = Depends(get_db)
):
    return crud_transaction.update_transaction(db, transaction_id, transaction_update)

@router.put("/hash/{transaction_hash}", response_model=TransactionOut)
def update_transaction_by_hash(
    transaction_hash: str, 
    transaction_update: TransactionUpdate, 
    db: Session = Depends(get_db)
):
    return crud_transaction.update_transaction_by_hash(db, transaction_hash, transaction_update)

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return crud_transaction.delete_transaction(db, transaction_id)

