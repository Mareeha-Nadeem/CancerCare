"""
ML Service - Lung Cancer Risk Prediction
Loads and uses the trained model from data_science/model_1
"""
import joblib
import json
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "data_science" / "model_1" / "models"
MODEL_PATH = MODEL_DIR / "lung_cancer_pipeline.pkl"
METADATA_PATH = MODEL_DIR / "model_metadata.json"

# Global variables for loaded model
_model = None
_metadata = None

def load_model():
    """Load the trained ML model and metadata."""
    global _model, _metadata
    
    if _model is not None:
        return _model, _metadata
    
    try:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}\n"
                "Please train the model first: python run_ds.py train"
            )
        
        print(f"📦 Loading model from: {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
        
        # Load metadata
        if METADATA_PATH.exists():
            with open(METADATA_PATH, 'r') as f:
                _metadata = json.load(f)
        else:
            _metadata = {}
        
        print(f"✅ Model loaded successfully!")
        return _model, _metadata
        
    except Exception as e:
        print(f"⚠️ Warning: Could not load ML model: {e}")
        print("ℹ️ Predictions will use mock data until model is trained.")
        return None, None

def predict_risk(features: Dict) -> Tuple[str, float, Dict[str, float]]:
    """
    Predict lung cancer risk level.
    
    Args:
        features: Dictionary of patient features
        
    Returns:
        Tuple of (risk_level, confidence, probabilities)
    """
    model, metadata = load_model()
    
    if model is None:
        # Fallback to mock prediction
        return _mock_prediction(features)
    
    try:
        # Expected feature order (15 features)
        feature_names = [
            'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE',
            'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING',
            'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH',
            'SWALLOWING_DIFFICULTY', 'CHEST_PAIN', 'GENDER_M'
        ]
        
        # Convert gender to binary
        gender_m = 1 if features.get('GENDER', 'M') == 'M' else 0
        
        # Build feature vector
        feature_vector = []
        for feat in feature_names[:-1]:  # All except GENDER_M
            value = features.get(feat, 0)
            feature_vector.append(float(value))
        
        # Add gender
        feature_vector.append(float(gender_m))
        
        # Reshape for prediction
        X = np.array([feature_vector])
        
        # Make prediction
        risk_class = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        # Map to risk levels
        risk_levels = metadata.get('classes', ['Low', 'Medium', 'High'])
        risk_level = risk_levels[risk_class]
        
        # Get confidence (max probability)
        confidence = float(np.max(probabilities))
        
        # Build probability dictionary
        prob_dict = {
            level: float(prob)
            for level, prob in zip(risk_levels, probabilities)
        }
        
        return risk_level, confidence, prob_dict
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return _mock_prediction(features)

def _mock_prediction(features: Dict) -> Tuple[str, float, Dict[str, float]]:
    """Fallback mock prediction when model is not available."""
    # Simple rule-based mock prediction
    age = features.get('AGE', 50)
    smoking = features.get('SMOKING', 0)
    
    if age > 60 and smoking > 5:
        risk_level = 'High'
        prob_dict = {'Low': 0.1, 'Medium': 0.3, 'High': 0.6}
    elif age > 50 or smoking > 3:
        risk_level = 'Medium'
        prob_dict = {'Low': 0.2, 'Medium': 0.6, 'High': 0.2}
    else:
        risk_level = 'Low'
        prob_dict = {'Low': 0.7, 'Medium': 0.2, 'High': 0.1}
    
    confidence = prob_dict[risk_level]
    
    return risk_level, confidence, prob_dict

def get_model_info() -> Dict:
    """Get model metadata and information."""
    model, metadata = load_model()
    
    if metadata:
        return {
            'model_type': metadata.get('model_type', 'Unknown'),
            'training_date': metadata.get('training_date', 'Unknown'),
            'accuracy': metadata.get('test_accuracy', 0.0),
            'f1_score': metadata.get('test_f1', 0.0),
            'classes': metadata.get('classes', []),
            'features': metadata.get('features', []),
            'trained': True
        }
    else:
        return {
            'model_type': 'Mock Model',
            'training_date': 'N/A',
            'accuracy': 0.0,
            'f1_score': 0.0,
            'classes': ['Low', 'Medium', 'High'],
            'features': [],
            'trained': False
        }

# MLService class for backward compatibility
class MLService:
    """Wrapper class for ML prediction functions"""
    
    def __init__(self):
        self.model_loaded = False
        try:
            model, metadata = load_model()
            if model is not None:
                self.model_loaded = True
        except:
            pass
    
    def predict(self, features: Dict) -> Dict:
        """
        Predict using the ML model (backward compatible interface)
        Returns dict with risk_level, confidence, probabilities
        """
        risk_level, confidence, probabilities = predict_risk(features)
        return {
            'risk_level': risk_level,
            'confidence': confidence,
            'probabilities': probabilities
        }
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        return get_model_info()

# Create global ml_service instance
ml_service = MLService()

# Preload model on import
try:
    load_model()
except:
    pass  # Will use mock predictions if model fails to load
