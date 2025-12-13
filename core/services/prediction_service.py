from core.models import Prediction
from core.validation import validate_features
from core.db_config import SessionLocal
from data_science.prediction import predict_lung_cancer

def generate_prediction(patient, features):
    valid, error = validate_features(features)
    if not valid:
        return None, error
    
    result = predict_lung_cancer(features)
    
    db = SessionLocal()
    pred = Prediction(
        patient_id=patient.id,
        malignancy = result["malignancy"],
        probability=result["probability"],
        stage=result.get("stage")
    )
    
    db.add(pred)
    db.commit()
    db.refresh(pred)
    
    return pred, None