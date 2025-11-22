from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.crud import project_review as project_review
from app.schemas.project_review import ProjectReviewCreate, ProjectReviewOut

router = APIRouter()

@router.get("/received", response_model=List[ProjectReviewOut])
def get_received_reviews(user_id: int, db: Session = Depends(get_db)):
    """Get reviews for projects owned by a user"""
    reviews = project_review.get_received_reviews(db, user_id)
    return reviews

@router.post("/project/{project_id}", response_model=ProjectReviewOut, status_code=201)
def add_review_to_project(project_id: int, review: ProjectReviewCreate, db: Session = Depends(get_db)):
    """Добавить отзыв на проект"""
    if review.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID in path and body must match")
    try:
        return project_review.create_project_review(db, review)
    except HTTPException as ex:
        raise ex


@router.get("/project/{project_id}", response_model=List[ProjectReviewOut])
def get_all_reviews(project_id: int, db: Session = Depends(get_db)):
    """Получить все отзывы проекта"""
    reviews = project_review.get_reviews_by_project(db, project_id)
    return reviews

@router.get("/has_review/{project_id}/{user_id}", response_model=bool)
def has_review(project_id: int, user_id: int, db: Session = Depends(get_db)):
    return project_review.has_review(db, project_id, user_id)