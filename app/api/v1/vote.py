from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import votes as crud_vote
from app.schemas.votes import VoteCreate, VoteOut

router = APIRouter()

@router.get("/", response_model=List[VoteOut])
def get_votes_by_post(
    post_id: int = Query(...),
    db: Session = Depends(get_db)
):
    return crud_vote.get_votes_by_post(db, post_id)


@router.post("/", response_model=VoteOut, status_code=status.HTTP_201_CREATED)
def create_vote(
    vote_in: VoteCreate,
    db: Session = Depends(get_db)
):
    return crud_vote.create_vote(db, vote_in)


@router.delete("/")
def delete_vote(
    post_id: int = Query(...),
    user_id: str = Query(...),
    db: Session = Depends(get_db)
):
    crud_vote.delete_vote(db, post_id, user_id)
    return None