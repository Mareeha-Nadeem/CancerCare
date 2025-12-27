"""
Complete PostgreSQL Setup - Handles Password Issues Automatically
"""
import os
import sys
from pathlib import Path

def print_header(msg):
    print("\n" + "="*70)
    print(f"  {msg}")
    print("="*70 + "\n")

def main():
    print_header("🔬 CancerCare - Complete PostgreSQL Setup")
    
    print("IMPORTANT: PostgreSQL Password Issues")
    print("-" * 70)
    print("\nYour PostgreSQL password is NOT working. Here's how to fix it:\n")
    
    print("METHOD 1: Find Your Password (Quickest)")
    print("  1. Check where you wrote it down during PostgreSQL installation")
    print("  2. Common passwords to try:")
    print("     - postgres")
    print("     - admin")  
    print("     - root")
    print("     - (blank - just press Enter)")
    print("     - 1234")
    
    print("\nMETHOD 2: Reset PostgreSQL Password")
    print("  Windows:")
    print("    1. Open pgAdmin (PostgreSQL GUI)")
    print("    2. Right-click server → Properties → Connection")
    print("    3. Or use psql: ALTER USER postgres WITH PASSWORD 'newpassword';")
    
    print("\nMETHOD 3: Use Trust Authentication (Temporary)")
    print("  1. Find pg_hba.conf file:")
    print("     C:\\Program Files\\PostgreSQL\\16\\data\\pg_hba.conf")
    print("  2. Change this line:")
    print("     host    all    all    127.0.0.1/32    scram-sha-256")
    print("     TO:")
    print("     host    all    all    127.0.0.1/32    trust")
    print("  3. Restart PostgreSQL service")
    print("  4. Run db_wizard.py (will work without password)")
    print("  5. Change back to 'scram-sha-256' after setup")
    
    print("\n" + "="*70)
    
    # Offer to create .env with user input
    print("\nLet's create/update your .env file:")
    
    env_path = Path(".env")
    
    print("\nWhat is your ACTUAL PostgreSQL password?")
    print("(If you don't know, use METHOD 2 or 3 above first)")
    password = input("\nPostgreSQL Password: ").strip()
    
    if not password:
        print("\n❌ No password provided.")
        print("Please use METHOD 2 or 3 above to reset/bypass password.")
        return
    
    # Create .env file
    database_url = f"postgresql+psycopg2://postgres:{password}@localhost:5432/cancercare"
    
    env_content = f"""# Database Configuration
DATABASE_URL={database_url}

# Security Keys
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-change-in-production

# Application Settings
DEBUG=True
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ .env file created/updated: {env_path.absolute()}")
    
    # Test connection
    print("\nTesting PostgreSQL connection...")
    
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"\n✅ SUCCESS! Connected to PostgreSQL!")
            print(f"   Version: {version.split(',')[0]}")
            
            # Create database if needed
            print("\nChecking if 'cancercare' database exists...")
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'cancercare'"))
            if not result.fetchone():
                print("   Creating database...")
                # Need to use autocommit for CREATE DATABASE
                engine2 = create_engine(
                    f"postgresql+psycopg2://postgres:{password}@localhost:5432/postgres",
                    isolation_level="AUTOCOMMIT"
                )
                with engine2.connect() as conn2:
                    conn2.execute(text("CREATE DATABASE cancercare"))
                print("   ✅ Database 'cancercare' created!")
            else:
                print("   ✅ Database 'cancercare' exists!")
            
            # Create tables
            print("\nCreating tables...")
            from core.models import Base
            from core.db_config import engine as app_engine
            
            Base.metadata.create_all(app_engine)
            print("   ✅ All tables created!")
            
            # Verify tables
            from sqlalchemy import inspect
            inspector = inspect(app_engine)
            tables = inspector.get_table_names()
            print(f"\n   Tables: {', '.join(tables)}")
            
            print("\n" + "="*70)
            print("  ✅ SETUP COMPLETE!")
            print("="*70)
            print("\nNext steps:")
            print("  1. Run: streamlit run app.py")
            print("  2. Open: http://localhost:8501")
            print("\n")
            
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nThe password is still incorrect.")
        print("Please use METHOD 2 or 3 above to fix it, then run this script again.")
        return

if __name__ == "__main__":
    main()
