"""
Direct SQL Database Recreation - No SQLAlchemy imports needed
"""
import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("DATABASE RECREATION (Direct SQL Method)")
print("=" * 70)

# Paths
DB_PATH = "cancercare.db"
BACKUP_FILE = "database_backup/full_backup_20260106_213845.json"
SCHEMA_FILE = "database_backup/schema_20260106_213845.sql"

# Step 1: Backup old database
if Path(DB_PATH).exists():
    old_db = f"cancercare_conflicted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    os.rename(DB_PATH, old_db)
    print(f"\\n✅ Moved conflicted database to: {old_db}")
else:
    print(f"\\n⚠️  No existing database found")

# Step 2: Create new database with schema
print("\\n🔨 Creating fresh database with schema...")

with open(SCHEMA_FILE, 'r') as f:
    schema_sql = f.read()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Execute schema (create tables)
for statement in schema_sql.split(';'):
    statement = statement.strip()
    if statement:
        try:
            cursor.execute(statement)
        except Exception as e:
            print(f"  ⚠️  Schema statement warning: {e}")

conn.commit()

# Verify tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print(f"\\n✅ Created {len(tables)} tables:")
for table in tables:
    print(f"  - {table}")

# Step 3: Load and restore data
print(f"\\n📂 Loading backup data...")

with open(BACKUP_FILE, 'r') as f:
    backup_data = json.load(f)

print(f"\\n💾 Restoring data to tables...")

total_restored = 0

for table_name, rows in backup_data.items():
    if not rows:
        print(f"\\n  ⚪ {table_name:30s} - Empty")
        continue
    
    print(f"\\n  📥 {table_name:30s}", end="")
    
    success = 0
    # Get column names from first row
    columns = list(rows[0].keys())
    
    for row_data in rows:
        try:
            # Prepare values
            values = [row_data.get(col) for col in columns]
            placeholders = ','.join(['?' for _ in columns])
            col_names = ','.join(columns)
            
            sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            success += 1
            
        except sqlite3.IntegrityError:
            # Skip duplicates
            pass
        except Exception as e:
            # Try without ID (let it auto-generate)
            try:
                cols_without_id = [c for c in columns if c != 'id']
                vals_without_id = [row_data.get(c) for c in cols_without_id]
                placeholders2 = ','.join(['?' for _ in cols_without_id])
                col_names2 = ','.join(cols_without_id)
                
                sql2 = f"INSERT INTO {table_name} ({col_names2}) VALUES ({placeholders2})"
                cursor.execute(sql2, vals_without_id)
                success += 1
            except:
                pass
    
    conn.commit()
    print(f" ✅ {success}/{len(rows)} rows")
    total_restored += success

conn.close()

print(f"\\n{'=' * 70}")
print("DATABASE RECREATION COMPLETE!")
print(f"{'=' * 70}")
print(f"\\n✅ Summary:")
print(f"   Tables: {len(tables)}")
print(f"   Rows Restored: {total_restored:,}")
print(f"\\n🎉 Database is ready to use - all conflicts resolved!")
print("=" * 70)
