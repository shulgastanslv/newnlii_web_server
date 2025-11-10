from app.db.session import engine
from app.db.base import Base
from app.models.orders import *
from app.models.user import *
from app.models.project import *
from app.models.category import *
from app.models.skill import *
from app.models.specialization import *

Base.metadata.create_all(bind=engine)
