from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.project_image import ProjectImage
from app.models.project import Project
from app.schemas.project_image import ProjectImageCreate, ProjectImageUpdate

def get_project_images(db: Session, project_id: int) -> List[ProjectImage]:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return db.query(ProjectImage).filter(ProjectImage.project_id == project_id).order_by(ProjectImage.order, ProjectImage.created_at).all()

def get_project_image_by_id(db: Session, image_id: int) -> ProjectImage:
    image = db.query(ProjectImage).filter(ProjectImage.id == image_id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project image with id {image_id} not found"
        )
    return image

def create_project_image(db: Session, image_in: ProjectImageCreate) -> ProjectImage:
    project = db.query(Project).filter(Project.id == image_in.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {image_in.project_id} not found"
        )
    if image_in.is_primary:
        db.query(ProjectImage).filter(
            ProjectImage.project_id == image_in.project_id,
            ProjectImage.is_primary == True
        ).update({ProjectImage.is_primary: False})
    
    db_image = ProjectImage(
        project_id=image_in.project_id,
        image_url=image_in.image_url,
        alt_text=image_in.alt_text,
        order=image_in.order,
        is_primary=image_in.is_primary
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def update_project_image(db: Session, image_id: int, image_update: ProjectImageUpdate) -> ProjectImage:
    image = db.query(ProjectImage).filter(ProjectImage.id == image_id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project image with id {image_id} not found"
        )
    
    update_data = image_update.dict(exclude_unset=True)
    if update_data.get("is_primary") is True:
        db.query(ProjectImage).filter(
            ProjectImage.project_id == image.project_id,
            ProjectImage.id != image_id,
            ProjectImage.is_primary == True
        ).update({ProjectImage.is_primary: False})
    
    for field, value in update_data.items():
        setattr(image, field, value)
    
    db.commit()
    db.refresh(image)
    return image

def delete_project_image(db: Session, image_id: int) -> dict:
    image = db.query(ProjectImage).filter(ProjectImage.id == image_id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project image with id {image_id} not found"
        )
    db.delete(image)
    db.commit()
    return {"detail": "Project image deleted successfully"}

def get_primary_image(db: Session, project_id: int) -> Optional[ProjectImage]:
    return db.query(ProjectImage).filter(
        ProjectImage.project_id == project_id,
        ProjectImage.is_primary == True
    ).first()

