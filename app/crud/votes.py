from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.vote import Vote
from app.schemas.votes import VoteCreate

def create_vote(db: Session, vote_in : VoteCreate):

        moscow_time = datetime.utcnow() + timedelta(hours=3)

        vote = db.query(Vote).filter(
            Vote.user_id == vote_in.user_id,
            Vote.post_id == vote_in.post_id
        ).first()

        if vote:
            vote.value = vote_in.value
            db.commit()
            db.refresh(vote)
            return vote

        db_vote = Vote(
            user_id=vote_in.user_id,
            post_id=vote_in.post_id,
            value=vote_in.value,
            created_at=moscow_time
        )

        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)

        return db_vote

def get_votes_by_post(db: Session, post_id: int):

        return db.query(Vote).filter(
            Vote.post_id == post_id
        ).all()

def delete_vote(db: Session, post_id: int, user_id: str):
    try:
        vote = db.query(Vote).filter(
            Vote.post_id == post_id,
            Vote.user_id == user_id
        ).first()

        if not vote:
            raise HTTPException(status_code=404, detail="Vote not found")

        db.delete(vote)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))