"""
Database Configuration - Works with SQLite or PostgreSQL
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get database URL from environment or use SQLite default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{Path(__file__).parent.parent / 'cancercare.db'}"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Test connections before using
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

def get_db():
    """Get database session"""
    db = session()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    """Get a new database session (for direct use)"""
    return session()

def init_database():
    """Initialize database tables"""
    from core.models import Base
    Base.metadata.create_all(engine)