"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:1234@localhost:5432/cancercare"
    )
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
    
    # File Upload
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'dcm', 'txt'}
    
    # Application
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8501"))
    
    # Email
    EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "False").lower() == "true"
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    # Network Monitoring
    ENABLE_NETWORK_LOGGING = os.getenv("ENABLE_NETWORK_LOGGING", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()
