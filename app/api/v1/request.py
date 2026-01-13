from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from typing import List
from app.crud import request as crud_request
from app.schemas.request import BuyRequest, RequestCreate, RequestDevID, RequestExisting, RequestOut

router = APIRouter()

@router.post("/create-request", response_model=RequestOut)
def create_request(value: RequestCreate, db: Session = Depends(get_db)):
    return crud_request.create_request(db, value)

@router.get("/", response_model=List[RequestOut])
def get_all_requests(db: Session = Depends(get_db)):
    return crud_request.get_all_requests(db)

@router.get("/{address}", response_model=List[RequestOut])
def get_requests_route(address: str, db: Session = Depends(get_db)):
    return crud_request.get_requests_by_address(db, address)

@router.get("/total-requests/{address}", response_model=int)
def get_total_requests_route(address: str, db: Session = Depends(get_db)):
    return crud_request.get_total_requests(db, address)

@router.get("/monthly-requests/{address}", response_model=int)
def get_monthly_requests_route(address: str, db: Session = Depends(get_db)):
    return crud_request.get_monthly_requests(db, address)

@router.get("/exists/{address}/project/{project_id}", response_model=bool)
def request_exists_route(address: str, project_id : int, db: Session = Depends(get_db)):
   res = crud_request.request_exists(db, address, project_id)
   if res:
       return True
   return False

@router.get("/last-request/{address}", response_model=str)
def get_last_request_id_route(address: str, db: Session = Depends(get_db)):
    return crud_request.get_last_request_id(db, address)

@router.post("/buy-request", response_model=bool)
def buy_request(value: BuyRequest, db: Session = Depends(get_db)):
    return crud_request.buy_request(db, value)