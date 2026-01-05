"""
Fix Database Schema - Add Missing Columns to cancercare.db
"""
import sqlite3

DB_PATH = "cancercare.db"  # The actual database file being used

def fix_database():
    """Add missing tumor detail columns to medical_images table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Connecting to: {DB_PATH}")
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medical_images'")
    if not cursor.fetchone():
        print("✗ ERROR: medical_images table does not exist!")
        print("   Run: python -c \"from core.db_config import init_database; init_database()\"")
        conn.close()
        return
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(medical_images)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    print(f"✓ Found {len(existing_columns)} existing columns")
    
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
    
    added = 0
    print("\nAdding missing columns...")
    for col_name, col_type in new_columns.items():
        if col_name not in existing_columns:
            try:
                sql = f"ALTER TABLE medical_images ADD COLUMN {col_name} {col_type}"
                cursor.execute(sql)
                print(f"  ✓ Added: {col_name}")
                added += 1
            except Exception as e:
                print(f"  ✗ Error adding {col_name}: {e}")
        else:
            print(f"  ⊘ Already exists: {col_name}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Migration complete! Added {added} new columns.")
    print("✓ Restart the Streamlit app to apply changes.")

if __name__ == "__main__":
    fix_database()
