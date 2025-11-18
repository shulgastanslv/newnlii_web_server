from datetime import datetime
from pydantic import BaseModel

class FavoriteBase(BaseModel):
    project_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteOut(FavoriteBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True