from sqlalchemy.orm import Session
from app.models.request import Request
from app.models.user import User
from app.schemas.request import BuyRequest, RequestCreate, RequestExisting
from sqlalchemy.orm import joinedload

def create_request(db: Session, request: RequestCreate):
    user = db.query(User).filter(User.id == request.developer_id).with_for_update().first()
    if not user or user.total_request_count < 1:
        return None
    user.total_request_count -= 1
    db.commit()
    db.refresh(user)
    
    res = Request(project_id=request.project_id, client_id=request.client_id, 
                  developer_id=request.developer_id, status=request.status)
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

def buy_request(db: Session, value : BuyRequest):
    user = db.query(User).filter(User.wallet_address == value.address).with_for_update().first()
    if not user:
        return False
    user.total_request_count += value.count
    db.commit()
    db.refresh(user)
    return True

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

def get_requests_by_address(db: Session, address: str):
    user_id = db.query(User).filter(User.wallet_address == address).first().id
    return db.query(Request).filter(Request.developer_id == user_id).all()

def get_request(db: Session, request_id: int):
    return db.query(Request).filter(Request.id == request_id).first()

def delete_request(db: Session, request_id: int):
    res = db.query(Request).filter(Request.id == request_id).first()
    db.delete(res)
    db.commit()
    return res

def get_monthly_requests(db: Session, address: str):
    user_id = db.query(User).filter(User.wallet_address == address).first().id
    monthly_requests = db.query(User).filter(User.id == user_id).first().monthly_requests_count
    return monthly_requests

def get_total_requests(db: Session, address: str):
    user_id = db.query(User).filter(User.wallet_address == address).first().id
    total_requests = db.query(User).filter(User.id == user_id).first().total_request_count
    return total_requests

def request_exists(db: Session, address: str, project_id: int):
    user = db.query(User).filter(User.wallet_address == address).first()
    if not user:
        return None

    return (
        db.query(Request)
        .filter(
            Request.developer_id == user.id,
            Request.project_id == project_id
        )
        .first()
    )

def get_last_request_id(db: Session, address: str):
    user_id = db.query(User).filter(User.wallet_address == address).first().id
    request = db.query(Request).filter(Request.developer_id == user_id).order_by(Request.id.desc()).first()
    if request:
        req = db.query(Request).filter(Request.developer_id == user_id).order_by(Request.id.desc()).first().created_at
        return str(req)
    return str("No requests")