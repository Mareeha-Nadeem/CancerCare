"""
Validation utilities for data validation
"""
from typing import Dict, Tuple

def validate_patient(data: Dict) -> Tuple[bool, str]:
    """Validate patient data"""
    required_fields = ['mrn', 'name', 'age', 'gender']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    
    # Validate age
    age = data.get('age')
    if not isinstance(age, int) or age < 0 or age > 150:
        return False, "Invalid age value"
    
    # Validate gender
    gender = data.get('gender')
    if gender not in ['M', 'F', 'Male', 'Female']:
        return False, "Gender must be M/F or Male/Female"
    
    return True, ""

def validate_features(features: Dict) -> Tuple[bool, str]:
    """Validate prediction features"""
    # Basic validation - features can be flexible
    if not features:
        return False, "Features dictionary cannot be empty"
    
    return True, ""

def validate_email(email: str) -> bool:
    """Basic email validation"""
    return '@' in email and '.' in email