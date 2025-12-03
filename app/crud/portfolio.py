from sqlalchemy.orm import Session
from typing import List, Optional
import app.models.portfolio as models
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate

def create_portfolio_item(
    db: Session, user_id: int, data: PortfolioCreate
) -> models.PortfolioItem:
    item = models.PortfolioItem(user_id=user_id, **data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_user_portfolio(
    db: Session, user_id: int, include_private: bool = False
) -> List[models.PortfolioItem]:
    q = db.query(models.PortfolioItem).filter(models.PortfolioItem.user_id == user_id)
    if not include_private:
        q = q.filter(models.PortfolioItem.is_public == 1)
    return q.order_by(models.PortfolioItem.created_at.desc()).all()

def get_portfolio_item(
    db: Session, item_id: int, user_id: Optional[int] = None
) -> Optional[models.PortfolioItem]:
    q = db.query(models.PortfolioItem).filter(models.PortfolioItem.id == item_id)
    if user_id is not None:
        q = q.filter(models.PortfolioItem.user_id == user_id)
    return q.first()

def update_portfolio_item(
    db: Session, item: models.PortfolioItem, data: PortfolioUpdate
) -> models.PortfolioItem:
    for field, value in data.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def delete_portfolio_item(db: Session, item: models.PortfolioItem) -> None:
    db.delete(item)
    db.commit()
