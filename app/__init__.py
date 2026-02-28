from app.db.session import engine
from app.db.base import Base
from app.models.user import *
from app.models.post import *

Base.metadata.create_all(bind=engine)
