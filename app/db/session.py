from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.pool import NullPool

engine = create_engine(os.getenv("DATABASE_URL"), echo=True, client_encoding='utf8', poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)