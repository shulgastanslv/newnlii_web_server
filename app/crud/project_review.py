from sqlalchemy import func
from app.models.project import Project
from app.models.project_review import ProjectReview
from app.models.user import User
from app.schemas.project_review import ProjectReviewCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def has_review(db: Session, project_id: int, user_id: int):
    return db.query(ProjectReview).filter(ProjectReview.project_id == project_id, ProjectReview.user_id == user_id).first() is not None

def create_project_review(db: Session, review_in: ProjectReviewCreate):
    project = db.query(Project).filter(Project.id == review_in.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {review_in.project_id} not found"
        )
    user = db.query(User).filter(User.id == review_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {review_in.user_id} not found"
        )
    existing_review = db.query(ProjectReview).filter(
        ProjectReview.project_id == review_in.project_id,
        ProjectReview.user_id == review_in.user_id
    ).first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has already reviewed this project"
        )
    if review_in.score < 1 or review_in.score > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Score must be between 1 and 5"
        )
    
    db_review = ProjectReview(
        project_id=review_in.project_id,
        user_id=review_in.user_id,
        score=review_in.score,
        text=review_in.text
    )
    db.add(db_review)
    project.reviews_count += 1
    avg_rating = db.query(func.avg(ProjectReview.score)).filter(ProjectReview.project_id == review_in.project_id).scalar()
    project.rating = avg_rating or 0.0
    db.commit()
    db.refresh(db_review)
    from sqlalchemy.orm import joinedload
    db_review = db.query(ProjectReview).options(joinedload(ProjectReview.user)).filter(ProjectReview.id == db_review.id).first()
    return db_review

def get_reviews_by_project(db: Session, project_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(ProjectReview).options(joinedload(ProjectReview.user)).filter(ProjectReview.project_id == project_id).order_by(ProjectReview.created_at.desc()).all()

def get_received_reviews(db: Session, user_id: int):
    from sqlalchemy.orm import joinedload
    return db.query(ProjectReview).options(joinedload(ProjectReview.user)).join(Project).filter(Project.owner_id == user_id).order_by(ProjectReview.created_at.desc()).all()