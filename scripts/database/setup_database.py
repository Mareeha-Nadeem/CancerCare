"""
Simple database recreation script
Uses the existing database_init.py module
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.db_config import init_database, get_session
from core.database_init import seed_sample_data
from core.models import User, Message, Notification

print("=" * 60)
print("CancerCare Database Setup")
print("=" * 60)

# Step 1: Initialize all tables
print("\n1. Creating database tables...")
try:
    init_database()
    print("   ✓ All tables created successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Step 2: Check existing data
print("\n2. Checking existing data...")
session = get_session()
try:
    user_count = session.query(User).count()
    message_count = session.query(Message).count()
    notification_count = session.query(Notification).count()
    
    print(f"   - Users: {user_count}")
    print(f"   - Messages: {message_count}")
    print(f"   - Notifications: {notification_count}")
    
    if user_count == 0:
        print("\n3. Seeding sample data...")
        seed_sample_data()
        print("   ✓ Sample data created")
    else:
        print("\n3. Sample data already exists, skipping seed")
        
finally:
    session.close()

print("\n" + "=" * 60)
print("Database setup complete!")
print("=" * 60)
print("\nYou can now use the messaging and notification features.")
