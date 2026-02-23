from fastapi import APIRouter
from app.api.v1 import common, contact, notification,request, project, skill, user, category, specialization, user_skills, user_specializations, order, project_review, user_review, favorite, project_image, transaction, faq
from app.api.mistral_AI import router as mistral
from app.api.v1 import tags
from app.api.v1 import portfolio
from app.api.chat import chat

api_router = APIRouter()

api_router.include_router(user_skills.router, prefix="/user_skills", tags=["User-Skills"])
api_router.include_router(user_specializations.router, prefix="/user_specializations", tags=["User-Specializations"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(project.router, prefix="/projects", tags=["Projects"])
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])
api_router.include_router(skill.router, prefix="/skills", tags=["Skills"])
api_router.include_router(specialization.router, prefix="/specializations", tags=["Specializations"])
api_router.include_router(order.router, prefix="/orders", tags=["Orders"])
api_router.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(mistral.router, prefix="/mistral", tags=["Mistral"])
api_router.include_router(project_review.router, prefix="/project-reviews", tags=["Project Reviews"])
api_router.include_router(user_review.router, prefix="/user-reviews", tags=["User Reviews"])
api_router.include_router(favorite.router, prefix="/favorites", tags=["Favorites"])
api_router.include_router(project_image.router, prefix="/project-images", tags=["Project Images"])
api_router.include_router(faq.router, prefix="/faq", tags=["FAQ"])
api_router.include_router(tags.router, prefix="/tags", tags=["Tags"])
api_router.include_router(notification.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(request.router, prefix="/requests", tags=["Requests"])
api_router.include_router(common.router, prefix="/common", tags=["Common"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(contact.router, prefix="/contacts", tags=["Contacts"])