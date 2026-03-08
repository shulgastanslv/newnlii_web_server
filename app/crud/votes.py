from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.post import Vote
from app.schemas.votes import VoteCreate


def create_vote(db: Session, vote_in : VoteCreate):

    try:
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
            created_at=datetime.utcnow()
        )

        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)

        return db_vote

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_votes_by_post(db: Session, post_id: int):

    try:
        return db.query(Vote).filter(
            Vote.post_id == post_id
        ).all()

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_vote(db: Session, post_id: int, user_id: int):

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