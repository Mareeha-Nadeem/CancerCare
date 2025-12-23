"""
Tumor Marker Service
Handles tumor marker test results, tracking, and trend analysis
"""
from core.models import TumorMarker
from core.db_config import get_db_session
from typing import List, Optional, Dict
from datetime import datetime

# Reference ranges for common tumor markers
TUMOR_MARKER_REFERENCES = {
    'CEA': {'min': 0.0, 'max': 3.0, 'unit': 'ng/mL'},
    'CA 19-9': {'min': 0.0, 'max': 37.0, 'unit': 'U/mL'},
    'CA 125': {'min': 0.0, 'max': 35.0, 'unit': 'U/mL'},
    'PSA': {'min': 0.0, 'max': 4.0, 'unit': 'ng/mL'},
    'AFP': {'min': 0.0, 'max': 10.0, 'unit': 'ng/mL'},
    'CA 15-3': {'min': 0.0, 'max': 30.0, 'unit': 'U/mL'},
    'CA 27-29': {'min': 0.0, 'max': 38.0, 'unit': 'U/mL'},
}

class TumorMarkerService:
    
    @staticmethod
    def record_marker(
        patient_id: int,
        marker_data: Dict,
        post_diagnosis_id: Optional[int] = None
    ) -> tuple[Optional[TumorMarker], Optional[str]]:
        """
        Record a tumor marker test result
        
        Args:
            patient_id: Patient ID
            marker_data: Dictionary containing marker information
            post_diagnosis_id: Optional link to diagnosis
            
        Returns:
            Tuple of (TumorMarker object, error message)
        """
        db = get_db_session()
        
        try:
            marker_name = marker_data.get('marker_name')
            value = marker_data.get('value')
            
            # Get reference range
            ref_range = TUMOR_MARKER_REFERENCES.get(marker_name, {})
            ref_min = ref_range.get('min', 0.0)
            ref_max = ref_range.get('max', 100.0)
            unit = marker_data.get('unit') or ref_range.get('unit', 'ng/mL')
            
            # Check if abnormal
            is_abnormal = value > ref_max or value < ref_min
            
            marker = TumorMarker(
                patient_id=patient_id,
                post_diagnosis_id=post_diagnosis_id,
                marker_name=marker_name,
                value=value,
                unit=unit,
                test_date=marker_data.get('test_date', datetime.utcnow()),
                reference_min=ref_min,
                reference_max=ref_max,
                is_abnormal=is_abnormal,
                lab_name=marker_data.get('lab_name', ''),
                test_method=marker_data.get('test_method', ''),
                notes=marker_data.get('notes', '')
            )
            
            db.add(marker)
            db.commit()
            db.refresh(marker)
            
            return marker, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def get_patient_markers(patient_id: int) -> List[TumorMarker]:
        """Get all tumor marker results for a patient"""
        db = get_db_session()
        try:
            return db.query(TumorMarker).filter_by(
                patient_id=patient_id
            ).order_by(TumorMarker.test_date.desc()).all()
        finally:
            db.close()
    
    @staticmethod
    def get_marker_trend(patient_id: int, marker_name: str) -> List[TumorMarker]:
        """Get trend data for a specific marker"""
        db = get_db_session()
        try:
            return db.query(TumorMarker).filter_by(
                patient_id=patient_id,
                marker_name=marker_name
            ).order_by(TumorMarker.test_date.asc()).all()
        finally:
            db.close()
    
    @staticmethod
    def get_abnormal_markers(patient_id: int) -> List[TumorMarker]:
        """Get all abnormal marker results for a patient"""
        db = get_db_session()
        try:
            return db.query(TumorMarker).filter_by(
                patient_id=patient_id,
                is_abnormal=True
            ).order_by(TumorMarker.test_date.desc()).all()
        finally:
            db.close()
    
    @staticmethod
    def get_latest_marker(patient_id: int, marker_name: str) -> Optional[TumorMarker]:
        """Get most recent result for a specific marker"""
        db = get_db_session()
        try:
            return db.query(TumorMarker).filter_by(
                patient_id=patient_id,
                marker_name=marker_name
            ).order_by(TumorMarker.test_date.desc()).first()
        finally:
            db.close()
    
    @staticmethod
    def check_abnormal(marker_name: str, value: float) -> tuple[bool, str]:
        """
        Check if a marker value is abnormal
        
        Returns:
            Tuple of (is_abnormal, interpretation)
        """
        ref = TUMOR_MARKER_REFERENCES.get(marker_name, {})
        ref_min = ref.get('min', 0.0)
        ref_max = ref.get('max', 100.0)
        
        if value > ref_max:
            excess = ((value - ref_max) / ref_max) * 100
            return True, f"Elevated ({excess:.1f}% above normal)"
        elif value < ref_min:
            return True, f"Below normal range"
        else:
            return False, "Within normal range"
    
    @staticmethod
    def get_reference_ranges() -> Dict:
        """Get all reference ranges"""
        return TUMOR_MARKER_REFERENCES
    
    @staticmethod
    def analyze_trend(patient_id: int, marker_name: str) -> Dict:
        """
        Analyze trend for a marker
        
        Returns:
            Dictionary with trend analysis
        """
        markers = TumorMarkerService.get_marker_trend(patient_id, marker_name)
        
        if len(markers) < 2:
            return {
                'trend': 'insufficient_data',
                'change': 0,
                'interpretation': 'Need at least 2 readings'
            }
        
        # Compare last 2 readings
        latest = markers[-1]
        previous = markers[-2]
        
        change = latest.value - previous.value
        percent_change = (change / previous.value) * 100 if previous.value > 0 else 0
        
        # Determine trend
        if abs(percent_change) < 10:
            trend = 'stable'
            interpretation = 'Marker levels are stable'
        elif change > 0:
            trend = 'increasing'
            interpretation = f'Marker increasing by {percent_change:.1f}%'
        else:
            trend = 'decreasing'
            interpretation = f'Marker decreasing by {abs(percent_change):.1f}%'
        
        return {
            'trend': trend,
            'change': change,
            'percent_change': percent_change,
            'latest_value': latest.value,
            'previous_value': previous.value,
            'interpretation': interpretation
        }
    
    @staticmethod
    def delete_marker(marker_id: int) -> tuple[bool, Optional[str]]:
        """Delete a tumor marker record"""
        db = get_db_session()
        
        try:
            marker = db.query(TumorMarker).filter_by(id=marker_id).first()
            if not marker:
                return False, "Marker not found"
            
            db.delete(marker)
            db.commit()
            
            return True, None
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

# Global service instance
tumor_marker_service = TumorMarkerService()
