from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db
from app.crud import project_image as crud_project_image
from app.schemas.project_image import ProjectImageCreate, ProjectImageOut, ProjectImageUpdate

router = APIRouter()

@router.get("/project/{project_id}", response_model=List[ProjectImageOut])
def get_project_images(project_id: int, db: Session = Depends(get_db)):
    """Получить все картинки проекта"""
    return crud_project_image.get_project_images(db, project_id)

@router.get("/project/{project_id}/primary", response_model=Optional[ProjectImageOut])
def get_primary_project_image(project_id: int, db: Session = Depends(get_db)):
    """Получить основное изображение проекта"""
    return crud_project_image.get_primary_image(db, project_id)

@router.get("/{image_id}", response_model=ProjectImageOut)
def get_project_image(image_id: int, db: Session = Depends(get_db)):
    """Получить картинку по ID"""
    return crud_project_image.get_project_image_by_id(db, image_id)

@router.post("/", response_model=ProjectImageOut, status_code=status.HTTP_201_CREATED)
def create_project_image(image_in: ProjectImageCreate, db: Session = Depends(get_db)):
    """Создать новую картинку проекта"""
    return crud_project_image.create_project_image(db, image_in)

@router.put("/{image_id}", response_model=ProjectImageOut)
def update_project_image(image_id: int, image_update: ProjectImageUpdate, db: Session = Depends(get_db)):
    """Обновить картинку проекта"""
    return crud_project_image.update_project_image(db, image_id, image_update)

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_image(image_id: int, db: Session = Depends(get_db)):
    """Удалить картинку проекта"""
    crud_project_image.delete_project_image(db, image_id)
    return None

