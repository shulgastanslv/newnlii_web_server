from sqlalchemy.orm import Session
from app.models.request import Request
from app.models.user import User
from app.schemas.request import RequestCreate, RequestExisting
from sqlalchemy.orm import joinedload

def create_request(db: Session, request: RequestCreate):
    res = Request(project_id=request.project_id, client_id=request.client_id, developer_id=request.developer_id, status=request.status)
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

def get_request_by_dev_id(db: Session, dev_id: int, project_id: int):
    res = db.query(Request).filter(Request.developer_id == dev_id and Request.project_id == project_id).first()
    print(res)
    if res:
        return res.id
    return None

def get_all_requests(db: Session):
    requests = db.query(Request).options(
    joinedload(Request.project),
    joinedload(Request.client),
    joinedload(Request.developer)
).all()
    
    return requests

def get_client_requests(db: Session, user_id: int):
    return db.query(Request).filter(Request.client_id == user_id).all()

def get_developer_requests(db: Session, address: str):
    user_id = db.query(User).filter(User.wallet_address == address).first().id
    return db.query(Request).filter(Request.developer_id == user_id).all()

def get_request(db: Session, request_id: int):
    return db.query(Request).filter(Request.id == request_id).first()

def delete_request(db: Session, request_id: int):
    res = db.query(Request).filter(Request.id == request_id).first()
    db.delete(res)
    db.commit()
    return res

def get_user_stats(db: Session, address: str):
    user_id = db.query(User).filter(User.wallet_address == address).first().id
    monthly_requests = db.query(User).filter(User.id == user_id).first().monthly_requests_count
    total_requests = db.query(User).filter(User.id == user_id).first().request_count
    return {"monthly_requests": monthly_requests, "total_requests": total_requests}