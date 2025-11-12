from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.crud import order as crud_order

router = APIRouter()

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db, order)

@router.get("/{order_id}", response_model=OrderOut)
def read_order(order_id: int, db: Session = Depends(get_db)):
    return crud_order.get_order_by_id(db, order_id)

@router.get("/", response_model=List[OrderOut])
def read_orders(db: Session = Depends(get_db)):
    return crud_order.get_all_orders(db)

@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    return crud_order.update_order(db, order_id, order_update)

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return crud_order.delete_order(db, order_id)
