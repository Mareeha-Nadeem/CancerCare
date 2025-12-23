"""
Simple database initialization script for post-diagnosis tables
Creates the 3 new tables: post_diagnosis, medical_images, tumor_markers
"""
from core.db_config import engine
from core.models import Base, PostDiagnosis, MedicalImage, TumorMarker

def init_post_diagnosis_tables():
    """Initialize post-diagnosis related tables"""
    
    print("\n" + "="*60)
    print("  Initializing Post-Diagnosis Tables")
    print("="*60 + "\n")
    
    try:
        # Create all tables (will skip existing ones)
        print("🔨 Creating tables...")
        Base.metadata.create_all(engine)
        
        print("\n✅ Post-diagnosis tables created successfully!")
        print("\nNew tables:")
        print("  - post_diagnosis")
        print("  - medical_images")
        print("  - tumor_markers")
        
        return True
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    init_post_diagnosis_tables()
