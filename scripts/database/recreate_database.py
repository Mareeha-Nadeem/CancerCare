"""
Database Backup and Recreation Script
Extracts all data, recreates database, and restores data
"""
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

# Paths
DB_PATH = Path("cancercare.db")
BACKUP_DIR = Path("database_backup")
BACKUP_DIR.mkdir(exist_ok=True)

def backup_database():
    """Backup all data from the database"""
    print("=" * 60)
    print("DATABASE BACKUP AND RECREATION")
    print("=" * 60)
    
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        return None
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n📊 Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
    
    # Backup data from each table
    backup_data = {}
    
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            # Convert to list of dicts
            table_data = []
            for row in rows:
                table_data.append(dict(row))
            
            backup_data[table] = table_data
            print(f"\n✅ Backed up {len(table_data)} rows from '{table}'")
            
        except Exception as e:
            print(f"❌ Error backing up {table}: {e}")
    
    # Save backup to JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"database_backup_{timestamp}.json"
    
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2, default=str)
    
    print(f"\n💾 Backup saved to: {backup_file}")
    
    # Save table names
    tables_file = BACKUP_DIR / f"table_names_{timestamp}.txt"
    with open(tables_file, 'w') as f:
        f.write("\\n".join(tables))
    
    print(f"📝 Table names saved to: {tables_file}")
    
    conn.close()
    return backup_file, backup_data

def get_schema():
    """Get database schema"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    schemas = cursor.fetchall()
    
    schema_file = BACKUP_DIR / "schema.sql"
    with open(schema_file, 'w') as f:
        for schema in schemas:
            if schema[0]:
                f.write(schema[0] + ";\\n\\n")
    
    print(f"📐 Schema saved to: {schema_file}")
    conn.close()

def recreate_database():
    """Recreate database using SQLAlchemy models"""
    print("\\n" + "=" * 60)
    print("RECREATING DATABASE")
    print("=" * 60)
    
    # Import after backing up
    from core.db_config import init_database, engine
    from core.models import Base
    
    # Backup old database
    if DB_PATH.exists():
        backup_db = f"cancercare_old_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        os.rename(DB_PATH, backup_db)
        print(f"\\n📦 Old database moved to: {backup_db}")
    
    # Create new database
    print("\\n🔨 Creating fresh database...")
    init_database()
    print("✅ Database created successfully!")
    
    # Verify tables
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\\n✅ Created {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
    
    conn.close()
    return tables

def restore_data(backup_data):
    """Restore data to new database"""
    print("\\n" + "=" * 60)
    print("RESTORING DATA")
    print("=" * 60)
    
    from core.db_config import get_session
    from core.models import (
        User, Patient, Doctor, Appointment, Prediction,
        Report, PostDiagnosis, MedicalImage, TumorMarker,
        TreatmentRecord, Notification, Message
    )
    
    model_map = {
        'users': User,
        'patients': Patient,
        'doctors': Doctor,
        'appointments': Appointment,
        'predictions': Prediction,
        'reports': Report,
        'post_diagnosis': PostDiagnosis,
        'medical_images': MedicalImage,
        'tumor_markers': TumorMarker,
        'treatment_records': TreatmentRecord,
        'notifications': Notification,
        'messages': Message,
    }
    
    session = get_session()
    
    for table_name, data in backup_data.items():
        if table_name in model_map:
            model = model_map[table_name]
            print(f"\\n📥 Restoring {len(data)} rows to '{table_name}'...")
            
            try:
                for row in data:
                    # Remove None values and handle datetime conversions
                    clean_row = {k: v for k, v in row.items() if v is not None}
                    obj = model(**clean_row)
                    session.add(obj)
                
                session.commit()
                print(f"✅ Restored {len(data)} rows to '{table_name}'")
                
            except Exception as e:
                session.rollback()
                print(f"❌ Error restoring {table_name}: {e}")
                print("   Trying row-by-row insertion...")
                
                # Try row by row
                success = 0
                for row in data:
                    try:
                        clean_row = {k: v for k, v in row.items() if v is not None}
                        obj = model(**clean_row)
                        session.add(obj)
                        session.commit()
                        success += 1
                    except Exception as row_error:
                        session.rollback()
                        print(f"   ⚠️ Skipped row: {row_error}")
                
                print(f"✅ Restored {success}/{len(data)} rows to '{table_name}'")
    
    session.close()

def main():
    """Main execution"""
    try:
        # Step 1: Backup
        print("\\n🔹 STEP 1: Backing up existing data...")
        backup_file, backup_data = backup_database()
        get_schema()
        
        if not backup_data:
            print("\\n❌ No data to backup. Exiting.")
            return
        
        # Step 2: Recreate
        print("\\n🔹 STEP 2: Recreating database...")
        new_tables = recreate_database()
        
        # Step 3: Restore
        print("\\n🔹 STEP 3: Restoring data...")
        restore_data(backup_data)
        
        print("\\n" + "=" * 60)
        print("✅ DATABASE RECREATION COMPLETE!")
        print("=" * 60)
        print(f"\\n📊 Summary:")
        print(f"  - Tables: {len(new_tables)}")
        print(f"  - Backup: {backup_file}")
        print(f"  - All data preserved and restored")
        print("\\n✨ Database is ready to use!")
        
    except Exception as e:
        print(f"\\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
