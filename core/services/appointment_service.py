"""
Appointment Service with Priority Queue integration
Demonstrates DSA: Priority Queue for appointment scheduling
"""
from core.models import Appointment, Patient, Doctor
from core.db_config import get_db_session
from typing import List, Optional, Dict
from datetime import datetime
import sys
from pathlib import Path

# Add dsa to path
dsa_path = Path(__file__).parent.parent.parent / "dsa"
sys.path.insert(0, str(dsa_path))

class AppointmentService:
    
    @staticmethod
    def create_appointment(data: Dict) -> tuple[Optional[Appointment], Optional[str]]:
        """Create a new appointment"""
        db = get_db_session()
        
        try:
            appointment = Appointment(**data)
            db.add(appointment)
            db.commit()
            db.refresh(appointment)
            
            return appointment, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def get_appointment_by_id(appointment_id: int) -> Optional[Appointment]:
        """Get appointment by ID"""
        db = get_db_session()
        try:
            return db.query(Appointment).filter_by(id=appointment_id).first()
        finally:
            db.close()
    
    @staticmethod
    def get_patient_appointments(patient_id: int) -> List[Appointment]:
        """Get all appointments for a patient"""
        db = get_db_session()
        try:
            return db.query(Appointment).filter_by(
                patient_id=patient_id
            ).order_by(Appointment.appointment_date.desc()).all()
        finally:
            db.close()
    
    @staticmethod
    def get_doctor_appointments(doctor_id: int, status: Optional[str] = None) -> List[Appointment]:
        """Get all appointments for a doctor"""
        db = get_db_session()
        try:
            query = db.query(Appointment).filter_by(doctor_id=doctor_id)
            if status:
                query = query.filter_by(status=status)
            return query.order_by(Appointment.appointment_date).all()
        finally:
            db.close()
    
    @staticmethod
    def get_all_appointments(status: Optional[str] = None) -> List[Appointment]:
        """Get all appointments"""
        db = get_db_session()
        try:
            query = db.query(Appointment)
            if status:
                query = query.filter_by(status=status)
            return query.order_by(Appointment.appointment_date.desc()).all()
        finally:
            db.close()
    
    
    @staticmethod
    def update_appointment(appointment_id: int, data: Dict) -> tuple[Optional[Appointment], Optional[str]]:
        """Update appointment details"""
        db = get_db_session()
        
        try:
            appointment = db.query(Appointment).filter_by(id=appointment_id).first()
            if not appointment:
                return None, "Appointment not found"
            
            # Update fields
            for key, value in data.items():
                if hasattr(appointment, key) and key != 'id':
                    setattr(appointment, key, value)
            
            db.commit()
            db.refresh(appointment)
            
            return appointment, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def update_appointment_status(appointment_id: int, status: str) -> tuple[Optional[Appointment], Optional[str]]:
        """Update appointment status"""
        db = get_db_session()
        
        try:
            appointment = db.query(Appointment).filter_by(id=appointment_id).first()
            if not appointment:
                return None, "Appointment not found"
            
            appointment.status = status
            db.commit()
            db.refresh(appointment)
            
            return appointment, None
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()
    
    @staticmethod
    def cancel_appointment(appointment_id: int) -> tuple[bool, Optional[str]]:
        """Cancel an appointment"""
        appointment, error = AppointmentService.update_appointment_status(appointment_id, "cancelled")
        if error:
            return False, error
        return True, None
    
    @staticmethod
    def complete_appointment(appointment_id: int) -> tuple[bool, Optional[str]]:
        """Mark appointment as completed"""
        appointment, error = AppointmentService.update_appointment_status(appointment_id, "completed")
        if error:
            return False, error
        return True, None
    
    @staticmethod
    def delete_appointment(appointment_id: int) -> tuple[bool, Optional[str]]:
        """Delete an appointment permanently"""
        db = get_db_session()
        
        try:
            appointment = db.query(Appointment).filter_by(id=appointment_id).first()
            if not appointment:
                return False, "Appointment not found"
            
            db.delete(appointment)
            db.commit()
            
            return True, None
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()
    
    @staticmethod
    def get_appointment_stats() -> Dict:
        """Get appointment statistics"""
        db = get_db_session()
        try:
            total = db.query(Appointment).count()
            scheduled = db.query(Appointment).filter_by(status="scheduled").count()
            completed = db.query(Appointment).filter_by(status="completed").count()
            cancelled = db.query(Appointment).filter_by(status="cancelled").count()
            
            return {
                'total': total,
                'scheduled': scheduled,
                'completed': completed,
                'cancelled': cancelled
            }
        finally:
            db.close()
    
    @staticmethod
    def get_upcoming_appointments(limit: int = 10) -> List[Appointment]:
        """Get upcoming scheduled appointments"""
        db = get_db_session()
        try:
            return db.query(Appointment).filter(
                Appointment.status == "scheduled",
                Appointment.appointment_date >= datetime.utcnow()
            ).order_by(Appointment.appointment_date).limit(limit).all()
        finally:
            db.close()

appointment_service = AppointmentService()
