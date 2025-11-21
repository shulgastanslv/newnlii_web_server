import json
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.crud.user import get_user_by_wallet
from app.models.project import Project
from app.models.skill import Skill
from app.models.tag import Tag
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.redis_client import redis_client

def create_project(wallet_address: str, db: Session, project: ProjectCreate):
    user = get_user_by_wallet(db, wallet_address)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Validate required fields
    if not project.name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name cannot be empty")
    if not project.description.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project description cannot be empty")
    if project.category_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category ID")
    if project.budget < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget cannot be negative")
    if project.crypto_type < 0 or project.crypto_type == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Crypto type cannot be empty")

    # Fetch skills and tags from database if provided
    skills = []
    if project.skills:
        skills = db.query(Skill).filter(Skill.id.in_(project.skills)).all()
        if len(skills) != len(project.skills):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more skill IDs are invalid")
    print(skills)
    tags = []
    if project.tags:
        tags = db.query(Tag).filter(Tag.id.in_(project.tags)).all()
        if len(tags) != len(project.tags):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more tag IDs are invalid")

    new_project = Project(
        name=project.name.strip(),
        description=project.description.strip(),
        category_id=project.category_id,
        budget=project.budget,
        owner_id=user.id,
        crypto_type=project.crypto_type,
        visible=project.visible,
        short_description=project.short_description,
        estimated_duration=project.estimated_duration,
        features=project.features,
        external_links=project.external_links,
        packages=project.packages,
        moderation_status=project.moderation_status,
        video_url=project.video_url
    )
    
    new_project.skills = skills
    new_project.tags = tags
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def get_all_projects(db: Session):
    return db.query(Project).all()

def get_all_projects_cached(db: Session):
    cached_projects = redis_client.get("all_projects")
    if cached_projects:
        try:
            projects_data = json.loads(cached_projects)
            return [ProjectOut(**pd) for pd in projects_data]
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            # If cached data is corrupted or incomplete, invalidate cache and query from DB
            redis_client.delete("all_projects")
    
    # Eagerly load owner and category relationships to ensure all required fields are available
    projects = db.query(Project).options(
        joinedload(Project.owner),
        joinedload(Project.category)
    ).all()
    response = [ProjectOut.from_orm(project) for project in projects] 
    json_data = json.dumps([item.dict() for item in response], default=str)
    redis_client.set("all_projects", json_data, ex=300) 
    return response


def get_project_by_id(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


def update_project(db: Session, project_id: int, project_update: ProjectUpdate):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = project_update.dict(exclude_unset=True)

    if "name" in update_data and update_data["name"] is not None:
        if not update_data["name"].strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name cannot be empty")
        project.name = update_data["name"].strip()

    if "description" in update_data and update_data["description"] is not None:
        if not update_data["description"].strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project description cannot be empty")
        project.description = update_data["description"].strip()

    if "category_id" in update_data and update_data["category_id"] is not None:
        if update_data["category_id"] <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category ID")
        project.category_id = update_data["category_id"]

    if "image_url" in update_data and update_data["image_url"] is not None:
        if not update_data["image_url"].strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image URL cannot be empty")
        project.image_url = update_data["image_url"].strip()

    if "budget" in update_data and update_data["budget"] is not None:
        if update_data["budget"] < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget cannot be negative")
        project.budget = update_data["budget"]

    if "crypto_type" in update_data and update_data["crypto_type"] is not None:
        if not update_data["crypto_type"].strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Crypto type cannot be empty")
        project.crypto_type = update_data["crypto_type"].strip()

    if "visible" in update_data and update_data["visible"] is not None:
        project.visible = update_data["visible"]

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully"}
