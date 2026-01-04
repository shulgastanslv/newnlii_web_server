from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.request import RequestStatus
from app.schemas.project import ProjectOut
from app.schemas.user import UserOut


class RequestBase(BaseModel):
    status : RequestStatus
    project_id : int
    client_id : int
    developer_id : int
    created_at : Optional[datetime] = datetime

class RequestCreate(RequestBase):
    pass

class RequestOut(RequestBase):
    id: int
    project: ProjectOut
    client: UserOut
    developer: UserOut
    model_config = {
        "from_attributes": True
    }


class RequestDevID(BaseModel):
    dev_id : int
    project_id : int
class RequestExisting(RequestBase):
    id: int