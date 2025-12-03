from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PortfolioBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_url: Optional[str] = None
    repo_url: Optional[str] = None
    tech_stack: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    is_public: int = True

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_url: Optional[str] = None
    repo_url: Optional[str] = None
    tech_stack: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    is_public: Optional[bool] = None

class PortfolioInDB(PortfolioBase):
    id: int
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class PortfolioPublic(PortfolioInDB):
    pass
