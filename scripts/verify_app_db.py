"""
Check which database file the app is actually using and verify the schema
"""
import sqlite3
from pathlib import Path

# Check app's database path from db_config
from core.db_config import engine
print(f"App is configured to use: {engine.url}")

# Extract the actual file path
db_url = str(engine.url)
if 'sqlite:///' in db_url:
    db_path_str = db_url.replace('sqlite:///', '')
    db_path = Path(db_path_str)
    print(f"Database file path: {db_path}")
    print(f"Database exists: {db_path.exists()}")
    
    if db_path.exists():
        # Check if post_diagnosis table exists
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"\nTables in database: {tables}")
        
        # Check if post_diagnosis exists
        if 'post_diagnosis' in tables:
            print("\n✓ post_diagnosis table exists")
            
            # Check its schema
            cursor.execute('PRAGMA table_info(post_diagnosis);')
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            print(f"Columns: {column_names}")
            
            if 'grade' in column_names:
                print("\n✓ grade column exists!")
            else:
                print("\n✗ grade column is MISSING!")
                print("\nNeed to add the grade column...")
        else:
            print("\n✗ post_diagnosis table does NOT exist!")
            print("\nNeed to create the table...")
        
        conn.close()
