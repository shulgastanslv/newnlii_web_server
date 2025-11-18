from pydantic import BaseModel

class Tag(BaseModel):
    name : str
    id : int
