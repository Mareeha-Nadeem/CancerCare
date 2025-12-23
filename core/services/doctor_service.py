"""
Doctor Service - Manage doctor records
"""
from core.models import Doctor
from core.db_config import get_db_session
from typing import List, Optional, Dict

class DoctorService:
    
    @staticmethod
    def create_doctor(data: Dict) -> tuple[Optional[Doctor], Optional[str]]:
        """Create a new doctor"""
        db = get_db_session()
        
        try:
            # Check if email already exists
            existing = db.query(Doctor).filter_by(email=data.get('email')).first()
            if existing:
                return None, f"Doctor with email {data.get('email')} already exists"
            
            doctor = Doctor(**data)
            db.add(doctor)
            db.commit()
            db.refresh(doctor)
            
            return doctor, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def get_doctor_by_id(doctor_id: int) -> Optional[Doctor]:
        """Get doctor by ID"""
        db = get_db_session()
        try:
            return db.query(Doctor).filter_by(id=doctor_id).first()
        finally:
            db.close()
    
    @staticmethod
    def get_doctor_by_email(email: str) -> Optional[Doctor]:
        """Get doctor by email"""
        db = get_db_session()
        try:
            return db.query(Doctor).filter_by(email=email).first()
        finally:
            db.close()
    
    @staticmethod
    def get_all_doctors() -> List[Doctor]:
        """Get all doctors"""
        db = get_db_session()
        try:
            return db.query(Doctor).all()
        finally:
            db.close()
    
    @staticmethod
    def update_doctor(doctor_id: int, data: Dict) -> tuple[Optional[Doctor], Optional[str]]:
        """Update doctor information"""
        db = get_db_session()
        
        try:
            doctor = db.query(Doctor).filter_by(id=doctor_id).first()
            if not doctor:
                return None, "Doctor not found"
            
            for key, value in data.items():
                if hasattr(doctor, key) and key != 'id':
                    setattr(doctor, key, value)
            
            db.commit()
            db.refresh(doctor)
            
            return doctor, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def delete_doctor(doctor_id: int) -> tuple[bool, Optional[str]]:
        """Delete a doctor"""
        db = get_db_session()
        
        try:
            doctor = db.query(Doctor).filter_by(id=doctor_id).first()
            if not doctor:
                return False, "Doctor not found"
            
            db.delete(doctor)
            db.commit()
            
            return True, None
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()
    
    @staticmethod
    def search_doctors(query: str) -> List[Doctor]:
        """Search doctors by name or specialization"""
        db = get_db_session()
        try:
            return db.query(Doctor).filter(
                (Doctor.name.ilike(f'%{query}%')) |
                (Doctor.specialization.ilike(f'%{query}%'))
            ).all()
        finally:
            db.close()

doctor_service = DoctorService()
