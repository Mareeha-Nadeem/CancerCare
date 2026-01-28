"""
Standalone Database Initialization Script
Adds project root to Python path before importing modules
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import modules
from core.db_config import init_database, get_db_session
from core.models import Patient, Doctor, User
from datetime import datetime
import bcrypt

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def seed_sample_data():
    """Add sample data to database"""
    db = get_db_session()
    
    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("Sample data already exists. Skipping seed.")
            return
        
        print("Seeding sample data...")
        
        # Create sample users
        admin_user = User(
            username="admin",
            email="admin@cancercare.com",
            password_hash=hash_password("admin123"),
            role="admin",
            created_at=datetime.utcnow()
        )
        
        patient_user = User(
            username="john_doe",
            email="john@example.com",
            password_hash=hash_password("patient123"),
            role="patient",
            created_at=datetime.utcnow()
        )
        
        doctor_user = User(
            username="dr_smith",
            email="smith@cancercare.com",
            password_hash=hash_password("doctor123"),
            role="doctor",
            created_at=datetime.utcnow()
        )
        
        db.add_all([admin_user, patient_user, doctor_user])
        
        # Create sample patient
        sample_patient = Patient(
            mrn="MRN001",
            name="John Doe",
            age=65,
            gender="M",
            contact="555-0123",
            email="john@example.com",
            created_at=datetime.utcnow()
        )
        
        db.add(sample_patient)
        
        # Create sample doctor
        sample_doctor = Doctor(
            name="Dr. Emily Smith",
            email="smith@cancercare.com",
            specialization="Oncology",
            phone="555-0456",
            created_at=datetime.utcnow()
        )
        
        db.add(sample_doctor)
        
        db.commit()
        print("✅ Sample data seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("CancerCare Database Initialization")
    print("=" * 60)
    
    # Create tables
    print("\nCreating database tables...")
    try:
        init_database()
        print("✅ All tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)
    
    # Seed sample data
    print("\nSeeding sample data...")
    seed_sample_data()
    
    print("\n" + "=" * 60)
    print("Database initialization complete!")
    print("=" * 60)
    print("\nSample users created:")
    print("  - admin / admin123")
    print("  - john_doe / patient123")
    print("  - dr_smith / doctor123")
