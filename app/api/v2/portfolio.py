from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import portfolio as crud
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioPublic,
    PortfolioInDB,
)

router = APIRouter()


@router.post(
    "/", response_model=PortfolioInDB, status_code=status.HTTP_201_CREATED
)
def create_portfolio(
    data: PortfolioCreate,
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    return crud.create_portfolio_item(
        db=db, user_id=user_id, data=data
    )


@router.get(
    "/me", response_model=List[PortfolioInDB]
)
def list_my_portfolio(
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_user_portfolio(
        db=db, user_id=user_id, include_private=True
    )


@router.get(
    "/user/{user_id}", response_model=List[PortfolioPublic]
)
def list_user_portfolio_public(
    user_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_user_portfolio(
        db=db, user_id=user_id, include_private=False
    )


@router.get(
    "/{item_id}", response_model=PortfolioPublic
)
def get_item_by_id(
    item_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_portfolio_item(
        db=db, item_id=item_id
    )

@router.get(
    "/", response_model=List[PortfolioPublic]
)
def get_all(
    db: Session = Depends(get_db),
):
    return crud.get_all(
        db=db
    )



@router.put(
    "/{item_id}", response_model=PortfolioInDB
)
def update_my_portfolio_item(
    item_id: int,
    data: PortfolioUpdate,
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    item = crud.get_portfolio_item(
        db=db, item_id=item_id, user_id=user_id
    )
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    return crud.update_portfolio_item(db=db, item=item, data=data)


@router.delete(
    "/{item_id}", status_code=status.HTTP_204_NO_CONTENT
)

def delete_my_portfolio_item(
    item_id: int,
    user_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    item = crud.get_portfolio_item(
        db=db, item_id=item_id, user_id=user_id
    )
    if not item:
        raise HTTPException(status_code=404, detail="Portfolio item not found")
    crud.delete_portfolio_item(db=db, item=item)
    return
