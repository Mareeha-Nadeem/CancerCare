"""
Force create all tables directly without using the scoped session
"""
from sqlalchemy import create_engine
from pathlib import Path

# Create engine directly to cancercare.db
db_path = Path(__file__).parent / 'cancercare.db'
engine = create_engine(f'sqlite:///{db_path}', echo=True)

print(f"Database: {db_path}")
print(f"Engine URL: {engine.url}\n")

# Import models
from core.models import Base

# Create ALL tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("\nDone!")

# Verify
import sqlite3
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"\nTables created: {[t[0] for t in tables]}")
conn.close()
