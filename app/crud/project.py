from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.models.project import Project
from app.schemas.project import ProjectCreate

def create_project(db: Session, project: ProjectCreate):
    res = Project(
        name=project.name,
        description = project.description,
        owner_id = project.owner_id
    )
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

def get_all_projects(db : Session):
    return db.query(Project).all()
