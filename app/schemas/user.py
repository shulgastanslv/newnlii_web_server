from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id : Optional[int] = None
    username : str
    password : str
    email : str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    pass
