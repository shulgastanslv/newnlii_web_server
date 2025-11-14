from db.base import Base
from db.base import engine

Base.metadata.create_all(bind=engine)