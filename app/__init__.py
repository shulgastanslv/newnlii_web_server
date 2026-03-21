from app.db.session import engine
from app.db.base import Base
from app.models.user import *
from app.models.post import *
from app.models.comment import *
from app.models.notification import *
from app.models.vote import *


Base.metadata.create_all(bind=engine)
