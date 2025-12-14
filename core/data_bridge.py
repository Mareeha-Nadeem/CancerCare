from core.models import Patient, Report, Prediction
from core.report_stroage import save_report, read_report_csv
from sqlalchemy import create_engine
from sqlalchemy.orm import session_maker
import datetime

engine = create_engine("sqlite:///cancercare.db)
Session = session_maker(bind=engine)

def add_patient(data):
    session = Session()
    
    patient = Patient(
        mrn=data["mrn"],
        name=data["name"],
        age=data["age"],
        gender=data["gender"],
        contact=data["contact"],
    )
    session.add(patient)
    session.commit()
    session.refresh(patient)
    
    session.close()
    return Patient

def upload_report(patient_id, uploaded_file):
    session = Session()
    
    path, filename = save_report(uploaded_file)
    
    report = Report(
        patient_id = patient_id,
        filename=filename,
        file_path=path,
        uploaded_at=datetime.datetime.utcnow()
    )
    session.add(report)
    session.commit()
    session.refresh(report)
    session.close()
    
    return report
    
def run_prediction(patient_id, features):
    session = Session
    
    result = predict_lung_cancer(features)
    
    pred = Prediction(
        patient_id=patient_id,
        malignancy=result["malignancy"],
        probability=result["probability"],
        stage=result["stage"],
        created_at=datetime.datetime.utcnow()
    )
    
    session.add(pred)
    session.commit()
    session.refresh(pred)
    session.close()
    
    return result