"""
Database Migration - Add Notifications and Messages Tables
"""
from core.db_config import engine
from core.models import Base, Notification, Message
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    """Create notifications and messages tables"""
    try:
        logger.info("🔄 Creating notifications and messages tables...")
        
        # Create all tables (will skip existing ones)
        Base.metadata.create_all(engine)
        
        logger.info("✅ Migration complete! Tables created:")
        logger.info("   - notifications")
        logger.info("   - messages")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()
