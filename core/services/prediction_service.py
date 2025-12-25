"""
Enhanced Prediction Service with ML integration
"""
from core.models import Prediction
from core.db_config import get_db_session
from core.services.ml_service import ml_service
from typing import List, Optional, Dict
import json
from datetime import datetime

class PredictionService:
    
    @staticmethod
    def generate_prediction(patient_id: int, features: Dict) -> tuple[Optional[Prediction], Optional[str]]:
        """
        Generate lung cancer risk prediction for a patient
        
        Parameters:
        -----------
        patient_id : int
            ID of the patient
        features : dict
            Dictionary of patient features for prediction
        
        Returns:
        --------
        tuple: (Prediction object, error message)
        """
        try:
            # Call ML service for prediction
            result = ml_service.predict(features)
            
            # Store prediction in database
            db = get_db_session()
            
            try:
                pred = Prediction(
                    patient_id=patient_id,
                    risk_level=result['risk_level'],
                    confidence=result['confidence'],
                    probabilities=json.dumps(result['probabilities']),
                    created_at=datetime.utcnow()
                )
                
                db.add(pred)
                db.commit()
                db.refresh(pred)
                
                return pred, None
            except Exception as e:
                db.rollback()
                return None, str(e)
            finally:
                db.close()
        
        except Exception as e:
            return None, f"Prediction failed: {str(e)}"
    
    @staticmethod
    def get_prediction_by_id(prediction_id: int) -> Optional[Prediction]:
        """Get prediction by ID"""
        db = get_db_session()
        try:
            return db.query(Prediction).filter_by(id=prediction_id).first()
        finally:
            db.close()
    
    @staticmethod
    def get_patient_predictions(patient_id: int) -> List[Prediction]:
        """Get all predictions for a patient"""
        db = get_db_session()
        try:
            return db.query(Prediction).filter_by(
                patient_id=patient_id
            ).order_by(Prediction.created_at.desc()).all()
        finally:
            db.close()
    
    @staticmethod
    def get_latest_prediction(patient_id: int) -> Optional[Prediction]:
        """Get the most recent prediction for a patient"""
        db = get_db_session()
        try:
            return db.query(Prediction).filter_by(
                patient_id=patient_id
            ).order_by(Prediction.created_at.desc()).first()
        finally:
            db.close()
    
    @staticmethod
    def get_all_predictions(limit: int = 100) -> List[Prediction]:
        """Get all predictions with limit"""
        db = get_db_session()
        try:
            return db.query(Prediction).order_by(
                Prediction.created_at.desc()
            ).limit(limit).all()
        finally:
            db.close()
    
    @staticmethod
    def get_risk_distribution() -> Dict:
        """Get distribution of risk levels"""
        db = get_db_session()
        try:
            predictions = db.query(Prediction).all()
            
            distribution = {'Low': 0, 'Medium': 0, 'High': 0}
            for pred in predictions:
                risk = pred.risk_level
                if risk in distribution:
                    distribution[risk] += 1
            
            total = sum(distribution.values())
            if total > 0:
                distribution_percent = {
                    k: round(v / total * 100, 1)
                    for k, v in distribution.items()
                }
            else:
                distribution_percent = distribution
            
            return {
                'counts': distribution,
                'percentages': distribution_percent,
                'total': total
            }
        finally:
            db.close()

prediction_service = PredictionService()