"""
Database Verification and Repair Script
Checks the cancercare.db database for issues and recreates if needed
"""
import sqlite3
import os
from pathlib import Path

def check_database():
    """Check database for corruption and schema issues"""
    db_path = Path(__file__).parent / 'cancercare.db'
    
    print("=" * 60)
    print("CancerCare Database Verification")
    print("=" * 60)
    
    if not db_path.exists():
        print("❌ Database file not found!")
        return False
    
    print(f"\n✓ Database file exists: {db_path}")
    print(f"  Size: {db_path.stat().st_size:,} bytes")
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check integrity
        print("\n1. Checking database integrity...")
        result = cursor.execute('PRAGMA integrity_check;').fetchone()
        if result[0] == 'ok':
            print("  ✓ Database integrity: OK")
        else:
            print(f"  ❌ Database integrity: {result[0]}")
            return False
        
        # List tables
        print("\n2. Checking tables...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print(f"  ✓ Found {len(tables)} tables:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"    - {table[0]}: {count} records")
        else:
            print("  ⚠ No tables found in database")
        
        # Expected tables based on models
        expected_tables = [
            'patients', 'reports', 'predictions', 'doctors', 'appointments',
            'users', 'post_diagnosis', 'medical_images', 'tumor_markers',
            'treatment_records', 'notifications', 'messages'
        ]
        
        existing_tables = [t[0] for t in tables]
        missing_tables = [t for t in expected_tables if t not in existing_tables]
        
        if missing_tables:
            print(f"\n  ⚠ Missing tables: {', '.join(missing_tables)}")
        else:
            print(f"\n  ✓ All expected tables present")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("Database check complete!")
        print("=" * 60)
        
        return len(missing_tables) == 0
        
    except Exception as e:
        print(f"\n❌ Error checking database: {e}")
        return False

def backup_database():
    """Backup existing database"""
    import shutil
    from datetime import datetime
    
    db_path = Path(__file__).parent / 'cancercare.db'
    if db_path.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = Path(__file__).parent / f'cancercare_backup_{timestamp}.db'
        shutil.copy2(db_path, backup_path)
        print(f"✓ Backup created: {backup_path.name}")
        return backup_path
    return None

def recreate_database():
    """Recreate database using models"""
    print("\n" + "=" * 60)
    print("Recreating Database")
    print("=" * 60)
    
    # Backup first
    backup = backup_database()
    
    # Import and initialize
    from core.db_config import init_database
    
    print("\nInitializing database tables...")
    init_database()
    print("✓ Database recreated successfully")
    
    # Verify
    if check_database():
        print("\n✓ Database verification passed!")
        return True
    else:
        print("\n❌ Database verification failed")
        return False

if __name__ == "__main__":
    is_healthy = check_database()
    
    if not is_healthy:
        print("\n⚠ Database has issues. Recreate? (y/n): ", end="")
        choice = input().lower()
        if choice == 'y':
            recreate_database()
        else:
            print("Skipping recreation. Run 'python core/database_init.py' to fix.")
