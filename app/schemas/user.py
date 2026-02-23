from typing import List, Optional
from datetime import datetime
from app.models.specialization import Specialization
from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    id : Optional[int] = None


class UserCreate(UserBase):
   pass

class UserOut(UserBase):
    pass
