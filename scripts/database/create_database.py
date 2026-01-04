"""
Automatic Database Setup Script
Creates PostgreSQL database and initializes all tables
"""
import sys
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
import os

def create_postgres_database():
    """Create PostgreSQL database if it doesn't exist"""
    
    print("=" * 70)
    print("  CANCERCARE DATABASE SETUP")
    print("=" * 70)
    print()
    
    # Get PostgreSQL credentials
    print(" PostgreSQL Configuration")
    print("-" * 70)
    
    # Default values
    default_user = "postgres"
    default_host = "localhost"
    default_port = "5432"
    default_db = "cancercare"
    
    print(f"\nPress Enter to use default values shown in [brackets]\n")
    
    user = input(f"PostgreSQL Username [{default_user}]: ").strip() or default_user
    password = input(f"PostgreSQL Password: ").strip()
    
    if not password:
        print("\n  No password provided. Trying without password (Windows Auth)...")
        password = ""
    
    host = input(f"PostgreSQL Host [{default_host}]: ").strip() or default_host
    port = input(f"PostgreSQL Port [{default_port}]: ").strip() or default_port
    db_name = input(f"Database Name [{default_db}]: ").strip() or default_db
    
    # Create connection URL
    if password:
        base_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}"
        db_url = f"{base_url}/{db_name}"
    else:
        base_url = f"postgresql+psycopg2://{user}@{host}:{port}"
        db_url = f"{base_url}/{db_name}"
    
    print("\n" + "=" * 70)
    print("  CREATING DATABASE")
    print("=" * 70)
    
    try:
        # Check if database exists
        if database_exists(db_url):
            print(f"\n Database '{db_name}' already exists")
            use_existing = input("\nUse existing database? (y/n): ").strip().lower()
            
            if use_existing != 'y':
                print(" Aborted by user")
                return None
        else:
            print(f"\n Creating database '{db_name}'...")
            create_database(db_url)
            print(f" Database '{db_name}' created successfully!")
        
        # Test connection
        print("\n Testing connection...")
        engine = create_engine(db_url, echo=False)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f" Connected successfully!")
            print(f"   PostgreSQL version: {version.split(',')[0]}")
        
        # Update .env file
        print("\n Updating .env file...")
        env_path = ".env"
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('DATABASE_URL='):
                        f.write(f'DATABASE_URL={db_url}\n')
                    else:
                        f.write(line)
            
            print(f" Updated .env with connection string")
        else:
            print("  .env file not found, creating new one...")
            with open(env_path, 'w') as f:
                f.write(f'DATABASE_URL={db_url}\n')
            print(f" Created .env file")
        
        return db_url
        
    except Exception as e:
        print(f"\n Error: {e}")
        print("\n Troubleshooting tips:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Check your username and password")
        print("  3. Verify the host and port are correct")
        print("  4. Ensure PostgreSQL allows connections from localhost")
        return None


def initialize_tables(db_url):
    """Create all database tables"""
    
    print("\n" + "=" * 70)
    print("  INITIALIZING TABLES")
    print("=" * 70)
    
    try:
        # Import models to register them
        print("\n Loading database models...")
        from core.models import Base
        from core.db_config import engine
        
        print(" Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        print("\n All tables created successfully!")
        print("\nTables created:")
        print("  - patients")
        print("  - doctors")
        print("  - appointments")
        print("  - predictions")
        print("  - users")
        print("  - reports")
        
        return True
        
    except Exception as e:
        print(f"\n Error creating tables: {e}")
        return False


def seed_sample_data():
    """Add sample data to database"""
    
    print("\n" + "=" * 70)
    print("  SEEDING SAMPLE DATA")
    print("=" * 70)
    
    seed = input("\nDo you want to add sample data? (y/n): ").strip().lower()
    
    if seed == 'y':
        try:
            from core.database_init import seed_sample_data as seed_func
            seed_func()
            print(" Sample data added successfully!")
            return True
        except Exception as e:
            print(f"  Warning: Could not seed data: {e}")
            return False
    else:
        print("⏭  Skipped sample data seeding")
        return True


def main():
    """Main setup function"""
    
    print("""
    
                                                                      
               CancerCare Database Setup Wizard                     
                                                                      
    
    """)
    
    # Step 1: Create database
    db_url = create_postgres_database()
    if not db_url:
        print("\n Database setup failed. Please try again.")
        return False
    
    # Step 2: Initialize tables
    if not initialize_tables(db_url):
        print("\n Table initialization failed.")
        return False
    
    # Step 3: Seed sample data
    seed_sample_data()
    
    # Success!
    print("\n" + "=" * 70)
    print("   DATABASE SETUP COMPLETE!")
    print("=" * 70)
    print("""
     Your database is ready to use!
    
    Next steps:
    1. Run the application: streamlit run app.py
    2. Access it at: http://localhost:8501
    3. Start using CancerCare!
    
     Database connection saved to .env file
    """)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n Unexpected error: {e}")
        sys.exit(1)
