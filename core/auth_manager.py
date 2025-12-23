"""
Authentication and Session Management
Demonstrates Computer Networks concepts: Session management, JWT tokens, Security
"""
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict
from config import config

class AuthManager:
    def __init__(self):
        self.secret_key = config.JWT_SECRET_KEY
        self.algorithm = config.JWT_ALGORITHM
        self.expiration_minutes = config.JWT_EXPIRATION_MINUTES
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed.encode('utf-8')
        )
    
    def create_access_token(self, user_data: Dict) -> str:
        """
        Create JWT access token
        Demonstrates Computer Networks: Token-based authentication
        """
        payload = {
            'user_id': user_data.get('id'),
            'username': user_data.get('username'),
            'email': user_data.get('email'),
            'role': user_data.get('role'),
            'exp': datetime.utcnow() + timedelta(minutes=self.expiration_minutes),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode JWT token
        Returns user data if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def create_session(self, user_data: Dict) -> Dict:
        """Create a new user session"""
        token = self.create_access_token(user_data)
        
        return {
            'token': token,
            'user': {
                'id': user_data.get('id'),
                'username': user_data.get('username'),
                'email': user_data.get('email'),
                'role': user_data.get('role')
            },
            'expires_at': (
                datetime.utcnow() + timedelta(minutes=self.expiration_minutes)
            ).isoformat()
        }

# Global auth manager instance
auth_manager = AuthManager()
