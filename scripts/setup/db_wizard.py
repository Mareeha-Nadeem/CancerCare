"""
Database Wizard - Automated PostgreSQL Setup
This script handles all database initialization for CancerCare project
"""
import os
import sys
from pathlib import Path
from getpass import getpass
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError, ProgrammingError
import time

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def print_success(message):
    """Print success message"""
    print(f" {message}")

def print_error(message):
    """Print error message"""
    print(f" {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ  {message}")

def print_step(step_num, message):
    """Print step message"""
    print(f"\n[Step {step_num}] {message}")

class DatabaseWizard:
    def __init__(self):
        self.host = "localhost"
        self.port = "5432"
        self.username = "postgres"
        self.password = None
        self.database_name = "cancercare"
        self.admin_engine = None
        self.db_engine = None
        
    def welcome(self):
        """Show welcome message"""
        print_header(" CancerCare Database Setup Wizard")
        print("This wizard will:")
        print("  1. Test PostgreSQL connection")
        print("  2. Create database (if not exists)")
        print("  3. Create all required tables")
        print("  4. Optionally add sample data")
        print("  5. Update .env configuration")
        print("\nPress Ctrl+C at any time to cancel.\n")
        
    def get_credentials(self):
        """Get PostgreSQL credentials from user"""
        print_step(1, "PostgreSQL Connection Details")
        
        # Host
        host_input = input(f"PostgreSQL Host (default: localhost): ").strip()
        if host_input:
            self.host = host_input
            
        # Port
        port_input = input(f"PostgreSQL Port (default: 5432): ").strip()
        if port_input:
            self.port = port_input
            
        # Username
        username_input = input(f"PostgreSQL Username (default: postgres): ").strip()
        if username_input:
            self.username = username_input
            
        # Password
        self.password = getpass("PostgreSQL Password: ")
        
        if not self.password:
            print_error("Password is required!")
            return False
            
        # Database name
        db_input = input(f"Database Name (default: cancercare): ").strip()
        if db_input:
            self.database_name = db_input
            
        return True
        
    def test_connection(self):
        """Test connection to PostgreSQL server"""
        print_step(2, "Testing PostgreSQL Connection")
        
        try:
            # Connect to default postgres database
            url = f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/postgres"
            self.admin_engine = create_engine(url, isolation_level="AUTOCOMMIT")
            
            # Test connection
            with self.admin_engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print_success("Connected to PostgreSQL successfully!")
                print_info(f"Version: {version.split(',')[0]}")
                return True
                
        except OperationalError as e:
            print_error(f"Connection failed: {e}")
            print_info("Please check:")
            print_info("  - PostgreSQL is running")
            print_info("  - Username and password are correct")
            print_info("  - Host and port are accessible")
            return False
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            return False
            
    def create_database(self):
        """Create the database if it doesn't exist"""
        print_step(3, f"Creating Database '{self.database_name}'")
        
        try:
            # Check if database exists
            with self.admin_engine.connect() as conn:
                result = conn.execute(
                    text(f"SELECT 1 FROM pg_database WHERE datname = '{self.database_name}'")
                )
                exists = result.fetchone() is not None
                
                if exists:
                    print_info(f"Database '{self.database_name}' already exists")
                    return True
                else:
                    # Create database
                    conn.execute(text(f"CREATE DATABASE {self.database_name}"))
                    print_success(f"Database '{self.database_name}' created successfully!")
                    return True
                    
        except Exception as e:
            print_error(f"Failed to create database: {e}")
            return False
            
    def create_tables(self):
        """Create all required tables"""
        print_step(4, "Creating Database Tables")
        
        try:
            # Connect to the new database
            url = f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"
            self.db_engine = create_engine(url)
            
            # Import models
            from core.models import Base
            
            # Create all tables
            Base.metadata.create_all(self.db_engine)
            
            # Verify tables were created
            inspector = inspect(self.db_engine)
            tables = inspector.get_table_names()
            
            print_success("All tables created successfully!")
            print_info("Tables created:")
            for table in tables:
                print(f"    - {table}")
                
            return True
            
        except Exception as e:
            print_error(f"Failed to create tables: {e}")
            print_info("Make sure core/models.py is properly configured")
            return False
            
    def add_sample_data(self):
        """Optionally add sample data"""
        print_step(5, "Sample Data")
        
        response = input("\nAdd sample data for testing? (y/n): ").strip().lower()
        
        if response != 'y':
            print_info("Skipping sample data")
            return True
            
        try:
            from core.services.patient_service import patient_service
            from core.services.doctor_service import doctor_service
            from datetime import datetime
            
            print_info("Adding sample patients...")
            
            # Add sample patients
            sample_patients = [
                {"mrn": "MRN001", "name": "John Doe", "age": 65, "gender": "M", "contact": "555-0101"},
                {"mrn": "MRN002", "name": "Jane Smith", "age": 58, "gender": "F", "contact": "555-0102"},
                {"mrn": "MRN003", "name": "Bob Johnson", "age": 72, "gender": "M", "contact": "555-0103"},
            ]
            
            for patient_data in sample_patients:
                patient, error = patient_service.create_patient(patient_data)
                if not error:
                    print(f"     Added patient: {patient_data['name']}")
                    
            print_info("Adding sample doctors...")
            
            # Add sample doctors
            sample_doctors = [
                {"name": "Dr. Sarah Wilson", "email": "s.wilson@hospital.com", "specialization": "Oncology", "phone": "555-0201"},
                {"name": "Dr. Michael Chen", "email": "m.chen@hospital.com", "specialization": "Pulmonology", "phone": "555-0202"},
            ]
            
            for doctor_data in sample_doctors:
                doctor, error = doctor_service.create_doctor(doctor_data)
                if not error:
                    print(f"     Added doctor: {doctor_data['name']}")
                    
            print_success("Sample data added successfully!")
            return True
            
        except Exception as e:
            print_error(f"Failed to add sample data: {e}")
            return False
            
    def update_env_file(self):
        """Update .env file with database configuration"""
        print_step(6, "Updating .env Configuration")
        
        try:
            env_path = Path(__file__).parent / ".env"
            
            # Create DATABASE_URL
            database_url = f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"
            
            # Read existing .env or create new
            if env_path.exists():
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                    
                # Update DATABASE_URL line
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith('DATABASE_URL='):
                        lines[i] = f'DATABASE_URL={database_url}\n'
                        updated = True
                        break
                        
                if not updated:
                    lines.append(f'\nDATABASE_URL={database_url}\n')
                    
                with open(env_path, 'w') as f:
                    f.writelines(lines)
            else:
                # Create new .env file
                with open(env_path, 'w') as f:
                    f.write(f'DATABASE_URL={database_url}\n')
                    f.write('SECRET_KEY=your-secret-key-change-this\n')
                    f.write('JWT_SECRET_KEY=your-jwt-secret-change-this\n')
                    
            print_success(".env file updated successfully!")
            print_info(f"Database URL saved to: {env_path}")
            return True
            
        except Exception as e:
            print_error(f"Failed to update .env: {e}")
            return False
            
    def verify_setup(self):
        """Verify the complete setup"""
        print_step(7, "Verifying Setup")
        
        try:
            # Test connection to database
            with self.db_engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM patients"))
                count = result.fetchone()[0]
                print_success(f"Database connection verified!")
                print_info(f"Patients in database: {count}")
                
            # Verify tables
            inspector = inspect(self.db_engine)
            tables = inspector.get_table_names()
            
            required_tables = ['patients', 'predictions', 'doctors', 'appointments']
            missing = [t for t in required_tables if t not in tables]
            
            if missing:
                print_error(f"Missing tables: {missing}")
                return False
            else:
                print_success("All required tables present!")
                return True
                
        except Exception as e:
            print_error(f"Verification failed: {e}")
            return False
            
    def show_summary(self):
        """Show setup summary"""
        print_header(" Setup Complete!")
        
        print("Database Configuration:")
        print(f"  Host:     {self.host}")
        print(f"  Port:     {self.port}")
        print(f"  Database: {self.database_name}")
        print(f"  Username: {self.username}")
        
        print("\n Configuration saved to: .env")
        
        print("\n Next Steps:")
        print("  1. Run the application:")
        print("     streamlit run app.py")
        print("\n  2. Application will open at:")
        print("     http://localhost:8501")
        
        print("\n Documentation:")
        print("  - README.md - General information")
        print("  - DATABASE_ISSUES_EXPLAINED.md - Troubleshooting")
        print("  - FINAL_FEATURES.md - Feature guide")
        
        print("\n" + "=" * 70)
        
    def run(self):
        """Run the complete setup wizard"""
        try:
            self.welcome()
            
            # Get credentials
            if not self.get_credentials():
                return False
                
            # Test connection
            if not self.test_connection():
                return False
                
            # Create database
            if not self.create_database():
                return False
                
            # Create tables
            if not self.create_tables():
                return False
                
            # Add sample data
            if not self.add_sample_data():
                return False
                
            # Update .env
            if not self.update_env_file():
                return False
                
            # Verify setup
            if not self.verify_setup():
                return False
                
            # Show summary
            self.show_summary()
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n Setup cancelled by user")
            return False
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Close connections
            if self.admin_engine:
                self.admin_engine.dispose()
            if self.db_engine:
                self.db_engine.dispose()

def main():
    """Main entry point"""
    wizard = DatabaseWizard()
    success = wizard.run()
    
    if success:
        print("\n Database setup completed successfully!")
        sys.exit(0)
    else:
        print("\n Database setup failed. Please fix errors and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
