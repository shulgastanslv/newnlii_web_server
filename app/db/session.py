from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.pool import NullPool

engine = create_engine(
    os.getenv("DATABASE_URL"),
    echo=True,
    client_encoding='utf8',
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)