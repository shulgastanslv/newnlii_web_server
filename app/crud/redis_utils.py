import json
from pathlib import Path
from sqlalchemy.orm import Session
from app.redis_client import redis_client
from app.models.project import Project
from app.models.category import Category
from app.schemas.project import ProjectOut

def clear_redis_cache(pattern: str = None):
    if pattern:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            return {"detail": f"Cleared {len(keys)} keys matching pattern '{pattern}'"}
        return {"detail": f"No keys found matching pattern '{pattern}'"}
    else:
        redis_client.flushdb()
        return {"detail": "All Redis cache cleared"}

def refresh_projects_cache(db: Session):
    projects = db.query(Project).all()
    try:
        response = [ProjectOut.from_orm(project) for project in projects]
        json_data = json.dumps([item.dict() for item in response], default=str)
    except AttributeError:
        response = [ProjectOut.model_validate(project) for project in projects]
        json_data = json.dumps([item.model_dump() for item in response], default=str)
    redis_client.set("all_projects", json_data, ex=300)
    return {"detail": f"Projects cache refreshed with {len(projects)} projects"}



def refresh_all_cache(db: Session):
    projects_result = refresh_projects_cache(db)
    return {"detail": "All cache refreshed", "projects": projects_result}

def get_redis_keys(pattern: str = "*"):
    keys = redis_client.keys(pattern)
    return {"keys": keys, "count": len(keys)}

