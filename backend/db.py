from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# sqlite file in project (kept simple)
DB_PATH = os.environ.get("DATABASE_URL", "sqlite:///./submissions.db")
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False} if "sqlite" in DB_PATH else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
