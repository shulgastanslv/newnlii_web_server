from sqlalchemy import func
from app.models.project import Project
from app.models.project_review import ProjectReview
from app.schemas.project_review import ProjectReviewCreate
from sqlalchemy.orm import Session

def create_project_review(db: Session, review_in: ProjectReviewCreate):
    db_review = ProjectReview(
        project_id=review_in.project_id,
        user_id=review_in.user_id,
        score=review_in.score,
        text=review_in.text
    )
    db.add(db_review)

    project = db.query(Project).filter(Project.id == review_in.project_id).first()
    if project:
        project.reviews_count += 1

        avg_rating = db.query(func.avg(ProjectReview.score)).filter(ProjectReview.project_id == review_in.project_id).scalar()
        project.rating = avg_rating

    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_by_project(db: Session, project_id: int):
    return db.query(ProjectReview).filter(ProjectReview.project_id == project_id).order_by(ProjectReview.created_at.desc()).all()
