from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_wallet
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectBase, ProjectCreate

def create_project(wallet_address : str, db: Session, project: ProjectCreate):
    user = get_user_by_wallet(db, wallet_address)
    res = Project(
        name=project.name,
        description=project.description,
        category_id=project.category_id,
        image_url=project.image_url,
        budget=project.budget,
        owner_id=user.id,
        crypto_type = project.crypto_type
    )
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

def get_all_projects(db: Session):
    return db.query(Project).all()

def get_project_by_id(db: Session, id: int):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

def update_project(db: Session, project_id: int, project_update: ProjectBase):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"detail": "Project deleted"}
