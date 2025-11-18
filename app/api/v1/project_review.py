from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import project_review as project_review
from app.schemas.project_review import ProjectReviewCreate, ProjectReviewOut

router = APIRouter()

@router.post("/{project_id}", response_model=ProjectReviewOut)
def add_review_to_project(project_id: int, review: ProjectReviewCreate, db: Session = Depends(get_db)):
    if review.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID in path and body must match")
    try:
        return project_review.create_project_review(db, review)
    except HTTPException as ex:
        raise ex


@router.get("/{project_id}", response_model=list[ProjectReviewOut])
def get_all_reviews(project_id: int, db: Session = Depends(get_db)):
    reviews = project_review.get_reviews_by_project(db, project_id)
    return reviews