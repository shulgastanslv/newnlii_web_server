from http.client import HTTPException
import random
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import post as crud_post
from typing import Any, Dict, List, Optional

router = APIRouter()

@router.get("/popular", response_model=List[Dict[str, Any]])
def check_post_saved_route(
    db: Session = Depends(get_db)
):
    tags = crud_post.get_popular_tags(db)
    return tags
