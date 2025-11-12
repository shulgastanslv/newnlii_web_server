from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import project as crud_project
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from typing import List

router = APIRouter()

@router.post("/{wallet_address}", response_model=ProjectOut)
def create_project(wallet_address: str, value: ProjectCreate, db: Session = Depends(get_db)):
    try:
        return crud_project.create_project(wallet_address, db, value)
    except HTTPException as ex:
        raise ex

@router.get("/", response_model=List[ProjectOut])
def get_all_project(db: Session = Depends(get_db)):
    return crud_project.get_all_projects(db)

@router.put("/{id}", response_model=ProjectOut)
def update_project(id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    try:
        return crud_project.update_project(db, id, project_update)
    except HTTPException as ex:
        raise ex

@router.delete("/{id}")
def delete_project(id: int, db: Session = Depends(get_db)):
    try:
        return crud_project.delete_project(db, id)
    except HTTPException as ex:
        raise ex

@router.get("/{id}", response_model=ProjectOut)
def get_project(id: int, db: Session = Depends(get_db)):
    try:
        return crud_project.get_project_by_id(db, id)
    except HTTPException as ex:
        raise ex
