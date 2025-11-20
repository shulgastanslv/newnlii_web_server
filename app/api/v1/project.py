from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db
from app.crud import project as crud_project
from app.models.category import Category
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter()

@router.post("/wallet/{wallet_address}", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(wallet_address: str, project_in: ProjectCreate, db: Session = Depends(get_db)):
    return crud_project.create_project(wallet_address, db, project_in)

@router.get("/", response_model=List[ProjectOut])
def get_all_projects(
    db: Session = Depends(get_db),
    query: Optional[str] = None,
    user_id: Optional[int] = None,
    category: Optional[str] = None,
    seller: Optional[str] = None,
    budget: Optional[str] = None,
    sort: Optional[str] = None,
):
    
    return crud_project.get_all_projects_cached(db)
    # q = db.query(Project)

    # if query:
    #     like_query = f"%{query}%"
    #     q = q.filter(or_(Project.name.ilike(like_query), Project.description.ilike(like_query)))

    # if user_id:
    #     q = q.filter(Project.owner_id == user_id)

    # if category and category.lower() != "all":
    #     q = q.join(Project.category).filter(Category.name == category)

    # if seller:
    #     q = q.join(Project.owner)
    #     if seller == "top":
    #         q = q.filter(User.rating != None)
    #     elif seller == "verified":
    #         q = q.filter(User.verified == True)

    # if budget:
    #     try:
    #         if budget.endswith(">"):
    #             amount = int(budget[:-1])
    #             q = q.filter(Project.budget > amount)
    #         else:
    #             amount = int(budget)
    #             q = q.filter(Project.budget <= amount)
    #     except ValueError:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid budget filter")

    # if sort:
    #     if sort == "budget_asc":
    #         q = q.order_by(Project.budget.asc())
    #     elif sort == "budget_desc":
    #         q = q.order_by(Project.budget.desc())
    #     elif sort == "newest":
    #         q = q.order_by(Project.created_at.desc())

    # return q.all()

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return crud_project.get_project_by_id(db, project_id)

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    return crud_project.update_project(db, project_id, project_update)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    crud_project.delete_project(db, project_id)
    return {"detail": "Project deleted successfully"}
