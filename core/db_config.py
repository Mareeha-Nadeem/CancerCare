from sqlalchemy import create_engine
from sqlalchemy import sessionmaker, scoped_session
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:1234@localhost:5432/cancercare"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()