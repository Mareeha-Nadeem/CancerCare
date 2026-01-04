"""
Simple Database Initialization without SQLAlchemy-utils
Creates tables using SQLAlchemy only
"""
from core.models import Base
from core.db_config import engine
from core.models import Patient, Doctor, User
import bcrypt
from datetime import datetime

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def init_database():
    """Initialize database tables"""
    print("=" * 70)
    print("  Creating Database Tables")
    print("=" * 70)
    
    try:
        print("\n Creating all tables...")
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
        print(f"\n Error: {e}")
        print("\n Make sure PostgreSQL is running and database 'cancercare' exists")
        print("   You can create it with: CREATE DATABASE cancercare;")
        return False

def seed_sample_data():
    """Add sample data"""
    from core.db_config import get_db_session
    
    db = get_db_session()
    
    try:
        # Check if data exists
        if db.query(User).count() > 0:
            print("\n Sample data already exists")
            return True
        
        print("\n Adding sample data...")
        
        # Create users
        admin = User(
            username="admin",
            email="admin@cancercare.com",
            password_hash=hash_password("admin123"),
            role="admin"
        )
        
        patient_user = User(
            username="john_doe",
            email="john@example.com",
            password_hash=hash_password("patient123"),
            role="patient"
        )
        
        doctor_user = User(
            username="dr_smith",
            email="smith@cancercare.com",
            password_hash=hash_password("doctor123"),
            role="doctor"
        )
        
        db.add_all([admin, patient_user, doctor_user])
        
        # Create sample patient
        patient = Patient(
            mrn="MRN001",
            name="John Doe",
            age=65,
            gender="M",
            contact="555-0123"
        )
        db.add(patient)
        
        # Create sample doctor
        doctor = Doctor(
            name="Dr. Emily Smith",
            email="smith@cancercare.com",
            specialization="Oncology",
            phone="555-0456"
        )
        db.add(doctor)
        
        db.commit()
        print(" Sample data added!")
        
        return True
    except Exception as e:
        print(f"  Error adding sample data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("""
    
                                                                      
               CancerCare Database Initialization                   
                                                                      
    
    """)
    
    if init_database():
        print("\n" + "=" * 70)
        choice = input("\nAdd sample data? (y/n): ").strip().lower()
        
        if choice == 'y':
            seed_sample_data()
        
        print("\n" + "=" * 70)
        print(" Database setup complete!")
        print("\nYou can now run: streamlit run app.py")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print(" Setup failed. Please check the error messages above.")
        print("=" * 70)
