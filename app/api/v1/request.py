from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from typing import List
from app.crud import request as crud_request
from app.schemas.request import RequestCreate, RequestDevID, RequestExisting, RequestOut

router = APIRouter()

@router.post("/create-request", response_model=RequestOut)
def create_request(value: RequestCreate, db: Session = Depends(get_db)):
    return crud_request.create_request(db, value)

@router.get("/", response_model=List[RequestOut])
def get_all_requests(db: Session = Depends(get_db)):
    return crud_request.get_all_requests(db)

@router.get("/developer/{address}", response_model=List[RequestOut])
def get_requests_by_dev(address: str, db: Session = Depends(get_db)):
    return crud_request.get_developer_requests(db, address)

@router.get("/client/{user_id}", response_model=List[RequestOut])
def get_requests_by_client(user_id: int, db: Session = Depends(get_db)):
    return crud_request.get_client_requests(db, user_id)

@router.post("/dev_id", response_model=int | None)
def get_request_by_dev_id(req : RequestDevID, db: Session = Depends(get_db)):
    print(req)
    return crud_request.get_request_by_dev_id(db, req.dev_id, req.project_id)

@router.get("/user/{address}/stats")
def get_user_stats(address: str, db: Session = Depends(get_db)):
    
    return crud_request.get_user_stats(db, address)