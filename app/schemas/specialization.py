from pydantic import BaseModel

class SpecializationBase(BaseModel):
    name: str

class SpecializationCreate(SpecializationBase):
    pass

class SpecializationOut(SpecializationBase):
    id: int
    model_config = {
        "from_attributes": True
    }