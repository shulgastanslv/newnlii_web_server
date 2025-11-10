from typing import List, Optional
from pydantic import BaseModel, EmailStr


class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    subcategories: List[CategoryBase]

    class Config:
        orm_mode = True