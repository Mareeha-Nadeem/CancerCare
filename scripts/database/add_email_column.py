"""
Add email column to existing patients table
"""
import sqlite3
from pathlib import Path

def add_email_column():
    """Add email column to patients table"""
    db_path = Path("cancercare.db")
    
    if not db_path.exists():
        print("❌ Database not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(patients)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'email' in columns:
            print("✅ Email column already exists!")
            conn.close()
            return True
        
        # Add email column
        cursor.execute("ALTER TABLE patients ADD COLUMN email TEXT")
        conn.commit()
        
        print("✅ Email column added successfully!")
        
        # Verify
        cursor.execute("PRAGMA table_info(patients)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"   Current columns: {', '.join(columns)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    add_email_column()
