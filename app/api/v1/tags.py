

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import tags as crud_tags
from app.schemas.tags import TagOut
from typing import List

router = APIRouter()


@router.get("/", response_model=List[TagOut])
def get_all_tags(db: Session = Depends(get_db)):
    return crud_tags.get_all_tags(db)