from sqlalchemy import func
from app.models.user_review import UserReview
from app.models.user import User
from app.schemas.user_review import UserReviewCreate, UserReviewUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create_user_review(db: Session, review_in: UserReviewCreate):
    reviewer = db.query(User).filter(User.id == review_in.reviewer_id).first()
    if not reviewer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reviewer with id {review_in.reviewer_id} not found"
        )
    reviewed_user = db.query(User).filter(User.id == review_in.reviewed_user_id).first()
    if not reviewed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reviewed user with id {review_in.reviewed_user_id} not found"
        )
    existing_review = db.query(UserReview).filter(
        UserReview.reviewer_id == review_in.reviewer_id,
        UserReview.reviewed_user_id == review_in.reviewed_user_id
    ).first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has already reviewed this user"
        )
    if review_in.score < 1 or review_in.score > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Score must be between 1 and 5"
        )
    
    db_review = UserReview(
        reviewer_id=review_in.reviewer_id,
        reviewed_user_id=review_in.reviewed_user_id,
        score=review_in.score,
        text=review_in.text
    )
    db.add(db_review)
    db.flush()
    reviewed_user.rating = db.query(func.avg(UserReview.score)).filter(
        UserReview.reviewed_user_id == review_in.reviewed_user_id
    ).scalar() or 0.0
    db.commit()
    db.refresh(db_review)
    from sqlalchemy.orm import joinedload
    db_review = db.query(UserReview).options(joinedload(UserReview.reviewer)).filter(
        UserReview.id == db_review.id
    ).first()
    return db_review

def get_reviews_by_user(db: Session, user_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(UserReview).options(joinedload(UserReview.reviewer)).filter(
        UserReview.reviewed_user_id == user_id
    ).order_by(UserReview.created_at.desc()).all()

def get_reviews_by_reviewer(db: Session, reviewer_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(UserReview).options(joinedload(UserReview.reviewer)).filter(
        UserReview.reviewer_id == reviewer_id
    ).order_by(UserReview.created_at.desc()).all()

def get_user_review_by_id(db: Session, review_id: int):
    from sqlalchemy.orm import joinedload
    review = db.query(UserReview).options(joinedload(UserReview.reviewer)).filter(
        UserReview.id == review_id
    ).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    return review

def update_user_review(db: Session, review_id: int, review_update: UserReviewUpdate):
    review = db.query(UserReview).filter(UserReview.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    if review_update.score is not None:
        if review_update.score < 1 or review_update.score > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Score must be between 1 and 5"
            )
        review.score = review_update.score
    
    if review_update.text is not None:
        review.text = review_update.text
    reviewed_user = db.query(User).filter(User.id == review.reviewed_user_id).first()
    if reviewed_user:
        reviewed_user.rating = db.query(func.avg(UserReview.score)).filter(
            UserReview.reviewed_user_id == review.reviewed_user_id
        ).scalar() or 0.0
    
    db.commit()
    db.refresh(review)
    from sqlalchemy.orm import joinedload
    review = db.query(UserReview).options(joinedload(UserReview.reviewer)).filter(
        UserReview.id == review_id
    ).first()
    return review

def delete_user_review(db: Session, review_id: int):
    review = db.query(UserReview).filter(UserReview.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found"
        )
    
    reviewed_user_id = review.reviewed_user_id
    db.delete(review)
    reviewed_user = db.query(User).filter(User.id == reviewed_user_id).first()
    if reviewed_user:
        reviewed_user.rating = db.query(func.avg(UserReview.score)).filter(
            UserReview.reviewed_user_id == reviewed_user_id
        ).scalar() or 0.0
    
    db.commit()
    return {"message": "Review deleted successfully"}

