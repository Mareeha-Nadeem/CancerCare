"""
Setup and Run Script for CancerCare Application
"""
import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    try:
        print("📦 Installing packages from requirements.txt...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def initialize_database():
    """Initialize the database"""
    print_header("Database Initialization")
    
    print("""
    📋 Before proceeding, ensure PostgreSQL is running with the following configuration:
    
    Database Name: cancercare
    Username: postgres
    Password: 1234
    Host: localhost
    Port: 5432
    
    You can change these settings in the .env file or database configuration.
    """)
    
    proceed = input("Do you want to initialize the database now? (y/n): ")
    
    if proceed.lower() == 'y':
        try:
            print("\n🔧 Initializing database...")
            from core.database_init import init_database, seed_sample_data
            
            init_database()
            
            seed = input("\nDo you want to add sample data? (y/n): ")
            if seed.lower() == 'y':
                seed_sample_data()
            
            print("✅ Database initialized successfully")
            return True
        except Exception as e:
            print(f"⚠️  Database initialization failed: {e}")
            print("   You can initialize it later by running: python core/database_init.py")
            return True  # Continue anyway
    else:
        print("⏭️  Skipping database initialization")
        return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    print_header("Environment Configuration")
    
    if not os.path.exists('.env'):
        print("Creating .env file from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example:
                with open('.env', 'w') as env:
                    env.write(example.read())
            print("✅ .env file created")
        else:
            print("⚠️  .env.example not found, skipping")
    else:
        print("✅ .env file already exists")
    
    return True

def run_application():
    """Run the Streamlit application"""
    print_header("Starting CancerCare Application")
    
    print("""
    🚀 Starting Streamlit application...
    
    The application will open in your default browser.
    If it doesn't open automatically, navigate to: http://localhost:8501
    
    To stop the application, press Ctrl+C
    """)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║               🫁 CancerCare Setup & Run Script                   ║
    ║                                                                  ║
    ║     Full Stack Lung Cancer Risk Prediction System               ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Create .env file
    if not create_env_file():
        return
    
    # Step 3: Install dependencies
    install = input("\nDo you want to install/update dependencies? (y/n): ")
    if install.lower() == 'y':
        if not install_dependencies():
            return
    
    # Step 4: Initialize database
    if not initialize_database():
        return
    
    print_header("Setup Complete!")
    print("""
    ✅ All setup tasks completed successfully!
    
    📌 What's been set up:
       • Dependencies installed
       • Environment configured
       • Database initialized
    
    🎯 Next Steps:
       • The application will start now
       • Access it at http://localhost:8501
       • Explore the features:
         - AI-Powered Predictions
         - Patient Management
         - Doctor Portal
         - Network Statistics
    """)
    
    start = input("\nStart the application now? (y/n): ")
    if start.lower() == 'y':
        run_application()
    else:
        print("""
    To start the application later, run:
        python run.py
    
    Or manually:
        streamlit run app.py
        """)

if __name__ == "__main__":
    main()
