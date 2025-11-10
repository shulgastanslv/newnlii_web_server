from fastapi import APIRouter
from app.api.v1 import auth, project, skill, user, category, specialization, user_skills, user_specializations

api_router = APIRouter()
api_router.include_router(user_skills.router, prefix="/user_skills", tags=["User-Skills"])
api_router.include_router(user_specializations.router, prefix="/user_specializations", tags=["User-Specializations"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(project.router, prefix="/projects", tags=["Projects"])
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])
api_router.include_router(skill.router, prefix="/skills", tags=["Skills"])
api_router.include_router(specialization.router, prefix="/specializations", tags=["Specializations"])