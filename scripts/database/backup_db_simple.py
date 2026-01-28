"""
Simple Database Backup - Extract all data without SQLAlchemy
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "cancercare.db"
BACKUP_DIR = Path("database_backup")
BACKUP_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("DATABASE BACKUP UTILITY")
print("=" * 70)

if not Path(DB_PATH).exists():
    print(f"\\n❌ Database not found: {DB_PATH}")
    exit(1)

# Connect
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print(f"\\n📊 Found {len(tables)} tables:\\n")

# Backup each table
backup_data = {}
total_rows = 0

for table in tables:
    try:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        table_data = [dict(row) for row in rows]
        backup_data[table] = table_data
        total_rows += len(table_data)
        
        print(f"  ✅ {table:30s} - {len(table_data):5d} rows")
        
    except Exception as e:
        print(f"  ❌ {table:30s} - ERROR: {e}")

# Save backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = BACKUP_DIR / f"full_backup_{timestamp}.json"

with open(backup_file, 'w') as f:
    json.dump(backup_data, f, indent=2, default=str)

# Save table list
tables_file = BACKUP_DIR / f"tables_{timestamp}.txt"
with open(tables_file, 'w') as f:
    for table in tables:
        f.write(f"{table}\\n")

# Save schema
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
schemas = cursor.fetchall()

schema_file = BACKUP_DIR / f"schema_{timestamp}.sql"
with open(schema_file, 'w') as f:
    for schema in schemas:
        if schema[0]:
            f.write(schema[0] + ";\\n\\n")

conn.close()

print(f"\\n{'=' * 70}")
print("BACKUP COMPLETE!")
print(f"{'=' * 70}")
print(f"\\n📦 Summary:")
print(f"   Tables: {len(tables)}")
print(f"   Total Rows: {total_rows:,}")
print(f"\\n💾 Files created:")
print(f"   Data:   {backup_file}")
print(f"   Tables: {tables_file}")
print(f"   Schema: {schema_file}")
print(f"\\n✅ All data has been safely backed up!")
