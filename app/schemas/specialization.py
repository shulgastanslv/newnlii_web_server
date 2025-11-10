from pydantic import BaseModel

class SpecializationBase(BaseModel):
    name: str

class SpecializationCreate(SpecializationBase):
    pass

class SpecializationOut(SpecializationBase):
    id: int
    class Config:
        orm_mode = True