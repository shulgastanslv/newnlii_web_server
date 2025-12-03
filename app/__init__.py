from app.db.session import engine
from app.db.base import Base
from app.models.order import *
from app.models.user import *
from app.models.project import *
from app.models.category import *
from app.models.skill import *
from app.models.tag import *
from app.models.specialization import *
from app.models.project_review import *
from app.models.user_review import *
from app.models.favorite import *
from app.models.project_image import *
from app.models.transaction import *
from app.models.keys import *
from app.models.portfolio import *
Base.metadata.create_all(bind=engine)
