"""
Proper Database Migration Script
Adds missing columns to existing medical_images table
"""
import sqlite3
import os

# Find the database file
db_files = [f for f in os.listdir('.') if f.endswith('.db')]
print(f"Found database files: {db_files}")

DB_PATH = "cancer_care.db" if "cancer_care.db" in db_files else db_files[0] if db_files else "cancer_care.db"
print(f"Using database: {DB_PATH}")

def check_and_add_columns():
    """Check which columns exist and add missing ones"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(medical_images)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    print(f"\nExisting columns in medical_images: {existing_columns}")
    
    # Columns to add
    new_columns = {
        "tumor_size_mm2": "REAL",
        "tumor_position_x": "REAL",
        "tumor_position_y": "REAL",
        "tumor_position_desc": "VARCHAR(50)",
        "tumor_mass_g": "REAL",
        "aggression_level": "INTEGER",
        "aggression_description": "VARCHAR(100)"
    }
    
    print("\nAdding missing columns...")
    for col_name, col_type in new_columns.items():
        if col_name not in existing_columns:
            try:
                sql = f"ALTER TABLE medical_images ADD COLUMN {col_name} {col_type}"
                cursor.execute(sql)
                print(f"✓ Added: {col_name}")
            except Exception as e:
                print(f"✗ Error adding {col_name}: {e}")
        else:
            print(f"⊘ Already exists: {col_name}")
    
    conn.commit()
    
    # Verify
    cursor.execute("PRAGMA table_info(medical_images)")
    final_columns = {row[1] for row in cursor.fetchall()}
    print(f"\n✓ Final column count: {len(final_columns)}")
    print(f"✓ New columns added: {len(final_columns - existing_columns)}")
    
    conn.close()
    print("\nMigration complete!")

if __name__ == "__main__":
    check_and_add_columns()
