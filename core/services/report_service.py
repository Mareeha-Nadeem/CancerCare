from core.report_stroage import save_file
from core.models import Report
from core.db_config import SessionLocal

def upload_report(patient, file):
    db = SessionLocal()
    
    path, filename = save_file(file)
    
    report = Report(
        patient_id=patient.id,
        filenamme=filename,
        file_path=path    
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return report