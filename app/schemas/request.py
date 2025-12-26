from datetime import datetime
from pydantic import BaseModel

from app.models.request import RequestStatus
from app.schemas.project import ProjectOut
from app.schemas.user import UserOut


class RequestBase(BaseModel):
    id: int
    status : RequestStatus
    project_id : int
    client_id : int
    developer_id : int
    created_at : datetime

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