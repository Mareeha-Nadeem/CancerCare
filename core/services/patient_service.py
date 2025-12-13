from core.models import Patient
from core.db_config import SessionLocal
from core.validation import validate_patient

def create_patient(data):
    valid, error = validate_patient(data)
    if not valid:
        return None, error
    
    db = SessionLocal()
    
    patient = Patient(**data)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    return patient, None

def get_patient_by_mrn(mrn):
    db = SessionLocal()
    return db.query(Patient).filter_by(mrn=mrn).first()