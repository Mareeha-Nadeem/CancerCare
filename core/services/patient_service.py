"""
Patient Service - Manage patient records
Complete CRUD operations
"""
from core.models import Patient
from core.db_config import get_db_session
from typing import List, Optional, Dict

class PatientService:
    
    @staticmethod
    def create_patient(data: Dict) -> tuple[Optional[Patient], Optional[str]]:
        """Create a new patient"""
        db = get_db_session()
        
        try:
            # Check if MRN already exists
            existing = db.query(Patient).filter_by(mrn=data.get('mrn')).first()
            if existing:
                return None, f"Patient with MRN {data.get('mrn')} already exists"
            
            patient = Patient(**data)
            db.add(patient)
            db.commit()
            db.refresh(patient)
            
            return patient, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def get_patient_by_id(patient_id: int) -> Optional[Patient]:
        """Get patient by ID"""
        db = get_db_session()
        try:
            return db.query(Patient).filter_by(id=patient_id).first()
        finally:
            db.close()
    
    @staticmethod
    def get_patient_by_mrn(mrn: str) -> Optional[Patient]:
        """Get patient by MRN"""
        db = get_db_session()
        try:
            return db.query(Patient).filter_by(mrn=mrn).first()
        finally:
            db.close()
    
    @staticmethod
    def get_all_patients(limit: int = 1000, offset: int = 0) -> List[Patient]:
        """Get all patients with pagination"""
        db = get_db_session()
        try:
            return db.query(Patient).offset(offset).limit(limit).all()
        finally:
            db.close()
    
    @staticmethod
    def update_patient(patient_id: int, data: Dict) -> tuple[Optional[Patient], Optional[str]]:
        """Update patient information"""
        db = get_db_session()
        
        try:
            patient = db.query(Patient).filter_by(id=patient_id).first()
            if not patient:
                return None, "Patient not found"
            
            # Update fields
            for key, value in data.items():
                if hasattr(patient, key) and key != 'id':
                    setattr(patient, key, value)
            
            db.commit()
            db.refresh(patient)
            
            return patient, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def delete_patient(patient_id: int) -> tuple[bool, Optional[str]]:
        """Delete a patient"""
        db = get_db_session()
        
        try:
            patient = db.query(Patient).filter_by(id=patient_id).first()
            if not patient:
                return False, "Patient not found"
            
            db.delete(patient)
            db.commit()
            
            return True, None
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()
    
    @staticmethod
    def search_patients(query: str) -> List[Patient]:
        """Search patients by name or MRN"""
        db = get_db_session()
        try:
            return db.query(Patient).filter(
                (Patient.name.ilike(f'%{query}%')) |
                (Patient.mrn.ilike(f'%{query}%'))
            ).all()
        finally:
            db.close()
    
    @staticmethod
    def get_patient_count() -> int:
        """Get total patient count"""
        db = get_db_session()
        try:
            return db.query(Patient).count()
        finally:
            db.close()

patient_service = PatientService()