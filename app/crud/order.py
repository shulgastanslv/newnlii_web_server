from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate
from fastapi import HTTPException

def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    print(db_order)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_all_orders(db: Session):
    return db.query(Order).all()

def update_order(db: Session, order_id: int, order_update: OrderUpdate):
    order = get_order_by_id(db, order_id)
    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}
