from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.crud import user_review as crud_user_review
from app.schemas.user_review import UserReviewCreate, UserReviewOut, UserReviewUpdate

router = APIRouter()

@router.post("/", response_model=UserReviewOut, status_code=201)
def create_user_review(review: UserReviewCreate, db: Session = Depends(get_db)):
    """Создать отзыв на пользователя"""
    try:
        return crud_user_review.create_user_review(db, review)
    except HTTPException as ex:
        raise ex

@router.get("/user/{user_id}", response_model=List[UserReviewOut])
def get_reviews_by_user(user_id: int, db: Session = Depends(get_db)):
    """Получить все отзывы на пользователя"""
    reviews = crud_user_review.get_reviews_by_user(db, user_id)
    return reviews

@router.get("/reviewer/{reviewer_id}", response_model=List[UserReviewOut])
def get_reviews_by_reviewer(reviewer_id: int, db: Session = Depends(get_db)):
    """Получить все отзывы, которые оставил пользователь"""
    reviews = crud_user_review.get_reviews_by_reviewer(db, reviewer_id)
    return reviews

@router.get("/{review_id}", response_model=UserReviewOut)
def get_user_review(review_id: int, db: Session = Depends(get_db)):
    """Получить отзыв по ID"""
    try:
        return crud_user_review.get_user_review_by_id(db, review_id)
    except HTTPException as ex:
        raise ex

@router.put("/{review_id}", response_model=UserReviewOut)
def update_user_review(review_id: int, review_update: UserReviewUpdate, db: Session = Depends(get_db)):
    """Обновить отзыв пользователя"""
    try:
        return crud_user_review.update_user_review(db, review_id, review_update)
    except HTTPException as ex:
        raise ex

@router.delete("/{review_id}")
def delete_user_review(review_id: int, db: Session = Depends(get_db)):
    """Удалить отзыв пользователя"""
    try:
        return crud_user_review.delete_user_review(db, review_id)
    except HTTPException as ex:
        raise ex

