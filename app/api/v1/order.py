from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.order import Order, Status
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

@router.post("/order_index", response_model=int)
def get_order_index(db: Session = Depends(get_db)):
    res = crud_order.get_order_index(db)
    return res

@router.get("/open/{project_id}")
def get_open_order_for_project(project_id: int, db: Session = Depends(get_db)):
    return crud_order.get_order_by_project(db, project_id)

@router.post("/close/{order_id}", response_model=OrderOut)
def order_close(order_id : int, db: Session = Depends(get_db)):
    return crud_order.order_close(order_id, db)

@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    return crud_order.update_order(db, order_id, order_update)

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return crud_order.delete_order(db, order_id)

@router.post("/{order_id}/deliver", response_model=OrderOut)
def deliver_order(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud_order.update_order_status(db, order_id, status="in_progress")

@router.post("/{order_id}/pay")
async def pay_order(
    order_id: int, 
    db: Session = Depends(get_db)
):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status == Status.paid:
        raise HTTPException(status_code=400, detail="Order is already paid")
    
    if not order.budget:
        raise HTTPException(status_code=400, detail="Order budget is not set")
    
@router.post("/{order_id}/accept", response_model=OrderOut)
def accept_order(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud_order.update_order_status(db, order_id, status="paid")