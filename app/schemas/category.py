from typing import List, Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int]

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    subcategories: List[CategoryBase]

    class Config:
        orm_mode = True