from pydantic import BaseModel

class KeysBase(BaseModel):
    email: str
    key: str

class KeyCreate(KeysBase):
    pass

class KeysOut(BaseModel):
    id : int
    key : str
    model_config = {
        "from_attributes": True
    }
