"""
Database Migration Script
Adds missing tumor detail columns to medical_images table
"""
import sqlite3
from pathlib import Path

# Database path
DB_PATH = "cancer_care.db"

def migrate_database():
    """Add new tumor detail columns"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    # List of columns to add
    columns_to_add = [
        ("tumor_size_mm2", "REAL"),
        ("tumor_position_x", "REAL"),
        ("tumor_position_y", "REAL"),
        ("tumor_position_desc", "VARCHAR(50)"),
        ("tumor_mass_g", "REAL"),
        ("aggression_level", "INTEGER"),
        ("aggression_description", "VARCHAR(100)")
    ]
    
    for column_name, column_type in columns_to_add:
        try:
            sql = f"ALTER TABLE medical_images ADD COLUMN {column_name} {column_type}"
            cursor.execute(sql)
            print(f"✓ Added column: {column_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"⊘ Column already exists: {column_name}")
            else:
                print(f"✗ Error adding {column_name}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\nMigration complete!")
    print("Database updated with new tumor detail columns.")

if __name__ == "__main__":
    migrate_database()
