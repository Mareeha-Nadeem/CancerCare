"""
Authentication Service
Handles user registration, login, and session management
"""
import bcrypt
from sqlalchemy.orm import Session
from core.db_config import get_db_session
from core.models import User
from datetime import datetime
from typing import Tuple, Optional


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception:
            return False
    
    @staticmethod
    def register_user(
        username: str,
        email: str,
        password: str,
        role: str = "admin"
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        Register a new user
        
        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)
            role: User role (admin, doctor, patient)
            
        Returns:
            Tuple of (User object, error message)
        """
        db = get_db_session()
        
        try:
            # Check if username already exists
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:
                return None, "Username already exists"
            
            # Check if email already exists
            existing_email = db.query(User).filter(User.email == email).first()
            if existing_email:
                return None, "Email already registered"
            
            # Validate password strength
            if len(password) < 6:
                return None, "Password must be at least 6 characters"
            
            # Hash password
            password_hash = AuthService.hash_password(password)
            
            # Create new user
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                is_active=True,
                created_at=datetime.utcnow()
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create a dictionary with user data to avoid session binding issues
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at
            }
            
            db.close()
            return user_data, None
            
        except Exception as e:
            db.rollback()
            db.close()
            return None, f"Registration failed: {str(e)}"
    
    @staticmethod
    def login_user(
        username: str,
        password: str
    ) -> Tuple[Optional[User], Optional[str]]:
        """
        Authenticate a user
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            Tuple of (User object, error message)
        """
        db = get_db_session()
        
        try:
            # Find user by username
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                return None, "Invalid username or password"
            
            # Check if user is active
            if not user.is_active:
                return None, "Account is inactive. Please contact administrator"
            
            # Verify password
            if not AuthService.verify_password(password, user.password_hash):
                return None, "Invalid username or password"
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            # Create a dictionary with user data to avoid session binding issues
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'last_login': user.last_login
            }
            
            db.close()
            return user_data, None
            
        except Exception as e:
            db.close()
            return None, f"Login failed: {str(e)}"
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        db = get_db_session()
        try:
            return db.query(User).filter(User.id == user_id).first()
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        db = get_db_session()
        try:
            return db.query(User).filter(User.username == username).first()
        finally:
            db.close()


# Create singleton instance
auth_service = AuthService()
