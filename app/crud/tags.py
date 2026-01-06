from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas.tags import TagOut
from fastapi import HTTPException

def get_all_tags(db: Session):
    tags = db.query(Tag).all()
    return [TagOut(id=tag.id, name=tag.name) for tag in tags]

def get_tag_by_id(db: Session, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagOut(id=tag.id, name=tag.name)

def get_tag_by_name(db: Session, name: str):
    tag = db.query(Tag).filter(Tag.name == name).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagOut(id=tag.id, name=tag.name)