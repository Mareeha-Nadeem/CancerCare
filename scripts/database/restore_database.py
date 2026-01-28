"""
Database Recreation Script - Recreate DB and restore all data
"""
import sys
sys.path.insert(0, 'e:/Misc/Extra/CancerCare -- Copy')

import json
import os
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("DATABASE RECREATION & RESTORATION")
print("=" * 70)

# Paths
DB_PATH = Path("cancercare.db")
BACKUP_FILE = Path("database_backup/full_backup_20260106_213845.json")

# Step 1: Move old database
if DB_PATH.exists():
    old_db = f"cancercare_conflicted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    os.rename(DB_PATH, old_db)
    print(f"\\n✅ Moved conflicted database to: {old_db}")

# Step 2: Create fresh database
print("\\n🔨 Creating fresh database...")

from core.db_config import init_database
init_database()

print("✅ Fresh database created!")

# Step 3: Verify tables
import sqlite3
conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print(f"\\n📊 Created tables ({len(tables)}):")
for table in tables:
    print(f"  - {table}")

conn.close()

# Step 4: Load backup data
print(f"\\n📂 Loading backup from: {BACKUP_FILE}")

with open(BACKUP_FILE, 'r') as f:
    backup_data = json.load(f)

print(f"✅ Loaded {len(backup_data)} tables from backup")

# Step 5: Restore data
print("\\n💾 Restoring data...")

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
total_restored = 0

for table_name, rows in backup_data.items():
    if table_name in model_map:
        model = model_map[table_name]
        
        print(f"\\n  📥 {table_name:30s}", end="")
        success = 0
        
        for row_data in rows:
            try:
                # Remove None and handle conversions
                clean_data = {k: v for k, v in row_data.items() if v is not None}
                obj = model(**clean_data)
                session.add(obj)
                session.flush()
                success += 1
            except Exception as e:
                session.rollback()
                # Try without problematic fields
                try:
                    # Remove auto-generated fields
                    for field in ['id', 'created_at', 'updated_at']:
                        clean_data.pop(field, None)
                    obj = model(**clean_data)
                    session.add(obj)
                    session.flush()
                    success += 1
                except:
                    pass
        
        try:
            session.commit()
            print(f" ✅ {success}/{len(rows)} rows")
            total_restored += success
        except Exception as e:
            session.rollback()
            print(f" ❌ Error: {e}")

session.close()

print(f"\\n{'=' * 70}")
print("RESTORATION COMPLETE!")
print(f"{'=' * 70}")
print(f"\\n✅ Successfully restored {total_restored:,} rows")
print(f"\\n🎉 Database is ready to use!")
print("\\n" + "=" * 70)
