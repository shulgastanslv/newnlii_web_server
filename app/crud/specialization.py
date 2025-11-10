from sqlalchemy.orm import Session
from app.models.specialization import Specialization
from app.schemas.specialization import SpecializationCreate

def create_specialization(db: Session, specialization: SpecializationCreate):
    res = Specialization(name=specialization.name)
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

def get_all_specializations(db: Session):
    return db.query(Specialization).all()