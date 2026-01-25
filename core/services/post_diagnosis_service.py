"""
Post-Diagnosis Service
Handles post-diagnosis patient information, treatment tracking, and progress monitoring
"""
from core.models import PostDiagnosis
from core.db_config import get_db_session
from typing import List, Optional, Dict
from datetime import datetime

class PostDiagnosisService:
    
    @staticmethod
    def create_diagnosis(patient_id: int, data: Dict) -> tuple[Optional[PostDiagnosis], Optional[str]]:
        """
        Create new post-diagnosis record
        
        Args:
            patient_id: Patient ID
            data: Dictionary containing diagnosis information
            
        Returns:
            Tuple of (PostDiagnosis object, error message)
        """
        db = get_db_session()
        
        try:
            diagnosis = PostDiagnosis(
                patient_id=patient_id,
                diagnosis_date=data.get('diagnosis_date', datetime.utcnow()),
                cancer_type=data.get('cancer_type'),
                stage=data.get('stage'),
                tumor_size_mm=data.get('tumor_size_mm'),
                lymph_nodes_affected=data.get('lymph_nodes_affected', 0),
                metastasis_status=data.get('metastasis_status', 'None'),
                treatment_plan=data.get('treatment_plan', ''),
                notes=data.get('notes', '')
            )
            
            db.add(diagnosis)
            db.commit()
            db.refresh(diagnosis)
            
            return diagnosis, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def update_diagnosis(diagnosis_id: int, data: Dict) -> tuple[Optional[PostDiagnosis], Optional[str]]:
        """Update existing diagnosis record"""
        db = get_db_session()
        
        try:
            diagnosis = db.query(PostDiagnosis).filter_by(id=diagnosis_id).first()
            if not diagnosis:
                return None, "Diagnosis not found"
            
            # Update fields
            for key, value in data.items():
                if hasattr(diagnosis, key) and key != 'id':
                    setattr(diagnosis, key, value)
            
            diagnosis.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(diagnosis)
            
            return diagnosis, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def get_patient_diagnoses(patient_id: int) -> List[PostDiagnosis]:
        """Get all diagnosis records for a patient"""
        db = get_db_session()
        try:
            return db.query(PostDiagnosis).filter_by(
                patient_id=patient_id
            ).order_by(PostDiagnosis.diagnosis_date.desc()).all()
        finally:
            db.close()
    
    @staticmethod
    def get_latest_diagnosis(patient_id: int) -> Optional[PostDiagnosis]:
        """Get most recent diagnosis for a patient"""
        db = get_db_session()
        try:
            return db.query(PostDiagnosis).filter_by(
                patient_id=patient_id
            ).order_by(PostDiagnosis.diagnosis_date.desc()).first()
        finally:
            db.close()
    
    @staticmethod
    def delete_diagnosis(diagnosis_id: int) -> tuple[bool, Optional[str]]:
        """Delete a diagnosis record"""
        db = get_db_session()
        
        try:
            diagnosis = db.query(PostDiagnosis).filter_by(id=diagnosis_id).first()
            if not diagnosis:
                return False, "Diagnosis not found"
            
            db.delete(diagnosis)
            db.commit()
            
            return True, None
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

# Global service instance
post_diagnosis_service = PostDiagnosisService()
