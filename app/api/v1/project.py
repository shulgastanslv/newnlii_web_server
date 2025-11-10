from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import project as crud_project
from app.schemas.project import ProjectCreate, ProjectOut
from typing import List

router = APIRouter()

@router.post("/create-project", response_model=ProjectOut)
def create_project(value: ProjectCreate, db: Session = Depends(get_db)):
    return crud_project.create_project(db, value)

@router.get("/", response_model=List[ProjectOut])
def get_all_project(db: Session = Depends(get_db)):
    return crud_project.get_all_projects(db)
