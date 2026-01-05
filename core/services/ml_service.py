"""
ML Service - Lung Cancer Risk Prediction
Loads and uses the trained model from data_science/model_1
"""
import sys
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

# Add data_science/model_1 to Python path for feature_engineer imports
DS_PATH = PROJECT_ROOT / "data_science" / "model_1"
if str(DS_PATH) not in sys.path:
    sys.path.insert(0, str(DS_PATH))

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
        
        print(f" Loading model from: {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
        
        # Load metadata
        if METADATA_PATH.exists():
            with open(METADATA_PATH, 'r') as f:
                _metadata = json.load(f)
        else:
            _metadata = {}
        
        print(f" Model loaded successfully!")
        return _model, _metadata
        
    except Exception as e:
        print(f" Warning: Could not load ML model: {e}")
        print("ℹ Predictions will use mock data until model is trained.")
        return None, None

def predict_risk(features: Dict) -> Tuple[str, float, Dict[str, float]]:
    """
    Predict lung cancer risk level.
    
    Args:
        features: Dictionary of patient features (case-insensitive)
        
    Returns:
        Tuple of (risk_level, confidence, probabilities)
    """
    model, metadata = load_model()
    
    if model is None:
        # Fallback to mock prediction
        return _mock_prediction(features)
    
    try:
        import pandas as pd
        
        # Convert all keys to uppercase (frontend sends lowercase, model expects uppercase)
        features_upper = {k.upper(): v for k, v in features.items()}
        
        # Create DataFrame with feature names (expected by the pipeline)
        # The model expects all 23 features with exact column names from training
        feature_data = {
            'AGE': features_upper.get('AGE', 50),
            'GENDER': features_upper.get('GENDER', 1),  # 1=M, 2=F
            'AIR_POLLUTION': features_upper.get('AIR_POLLUTION', 3),
            'ALCOHOL_USE': features_upper.get('ALCOHOL_USE', 3),
            'DUST_ALLERGY': features_upper.get('DUST_ALLERGY', 3),
            'OCCUPATIONAL_HAZARDS': features_upper.get('OCCUPATIONAL_HAZARDS', 3),
            'GENETIC_RISK': features_upper.get('GENETIC_RISK', 3),
            'CHRONIC_LUNG_DISEASE': features_upper.get('CHRONIC_LUNG_DISEASE', 3),
            'BALANCED_DIET': features_upper.get('BALANCED_DIET', 5),
            'OBESITY': features_upper.get('OBESITY', 3),
            'SMOKING': features_upper.get('SMOKING', 3),
            'PASSIVE_SMOKER': features_upper.get('PASSIVE_SMOKER', 3),
            'CHEST_PAIN': features_upper.get('CHEST_PAIN', 3),
            'COUGHING_OF_BLOOD': features_upper.get('COUGHING_OF_BLOOD', 2),
            'FATIGUE': features_upper.get('FATIGUE', 3),
            'WEIGHT_LOSS': features_upper.get('WEIGHT_LOSS', 2),
            'SHORTNESS_OF_BREATH': features_upper.get('SHORTNESS_OF_BREATH', 3),
            'WHEEZING': features_upper.get('WHEEZING', 3),
            'SWALLOWING_DIFFICULTY': features_upper.get('SWALLOWING_DIFFICULTY', 2),
            'CLUBBING_OF_FINGER_NAILS': features_upper.get('CLUBBING_OF_FINGER_NAILS', 2),
            'FREQUENT_COLD': features_upper.get('FREQUENT_COLD', 3),
            'DRY_COUGH': features_upper.get('DRY_COUGH', 3),
            'SNORING': features_upper.get('SNORING', 3),
        }
        
        # Create DataFrame (single row)
        X = pd.DataFrame([feature_data])
        
        # Make prediction
        risk_class_raw = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        # CRITICAL: Ensure risk_class is an integer
        risk_class = int(risk_class_raw)
        
        print(f" DEBUG: raw prediction = {risk_class_raw} (type: {type(risk_class_raw)})")
        print(f" DEBUG: as integer = {risk_class}")
        print(f" DEBUG: probabilities = {probabilities}")
        
        # CRITICAL FIX: Explicit mapping of numeric classes to risk levels
        # The trained model uses numeric labels: 0='High', 1='Low', 2='Medium' (alphabetical)
        # We need to map these integers to human-readable strings
        
        # Try to get the model's class ordering
        model_classes = None
        if hasattr(model, 'classes_'):
            model_classes = list(model.classes_)
            print(f" DEBUG: Model classes_: {model_classes} (types: {[type(c) for c in model_classes]})")
        elif hasattr(model, 'named_steps'):
            classifier = model.named_steps.get('classifier', None)
            if classifier and hasattr(classifier, 'classes_'):
                model_classes = list(classifier.classes_)
                print(f" DEBUG: Pipeline classifier classes_: {model_classes}")
        
        # Create the mapping
        # The model was trained with labels that are either integers (0,1,2) or strings
        # Map them to proper risk level strings
        if model_classes and len(model_classes) == 3:
            # Convert model classes to strings
            str_classes = [str(c) for c in model_classes]
            print(f" DEBUG: String classes: {str_classes}")
            
            # Check if they're numeric strings
            if all(c.isdigit() for c in str_classes):
                # Model has numeric classes - CORRECTED MAPPING
                # Based on actual model behavior: Higher class number = Higher risk
                # 0 = Low Risk, 1 = Medium Risk, 2 = High Risk
                numeric_to_risk = {'0': 'Low', '1': 'Medium', '2': 'High'}
                risk_levels = [numeric_to_risk.get(str(i), 'Unknown') for i in range(3)]
                print(f"🔧 DEBUG: Using CORRECTED numeric mapping: {risk_levels}")
            else:
                # Model has text classes already
                risk_levels = str_classes
                print(f" DEBUG: Using model's text classes: {risk_levels}")
        else:
            # Fallback: use standard alphabetical order
            risk_levels = ['High', 'Low', 'Medium']
            print(f" DEBUG: Using default alphabetical classes")
        
        # Validate index
        if risk_class < 0 or risk_class >= len(risk_levels):
            print(f" ERROR: Invalid risk_class {risk_class} for {len(risk_levels)} classes")
            risk_class = 1  # Default to 'Low' (middle risk)
        
        # Get the risk level string
        risk_level = risk_levels[risk_class]
        
        # Ensure it's a valid risk level
        if risk_level not in ['Low', 'Medium', 'High']:
            print(f" WARNING: Invalid risk_level '{risk_level}', mapping to standard...")
            # Try to map numeric strings to text
            if risk_level in ['0', 0]:
                risk_level = 'High'
            elif risk_level in ['1', 1]:
                risk_level = 'Low'
            elif risk_level in ['2', 2]:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'  # Safe default
        
        # Ensure final type is string
        risk_level = str(risk_level)
        
        # Get confidence (max probability)
        confidence = float(np.max(probabilities))
        
        # Build probability dictionary with proper labels
        prob_dict = {
            'Low': float(probabilities[risk_levels.index('Low')] if 'Low' in risk_levels else 0.33),
            'Medium': float(probabilities[risk_levels.index('Medium')] if 'Medium' in risk_levels else 0.33),
            'High': float(probabilities[risk_levels.index('High')] if 'High' in risk_levels else 0.33)
        }
        
        print(f" ==================================")
        print(f" PREDICTION RESULT:")
        print(f" Raw class: {risk_class}")
        print(f" Risk Level: {risk_level}")
        print(f" Confidence: {confidence:.2%}")
        print(f" Probabilities: {prob_dict}")
        print(f" Type check: {type(risk_level)} = '{risk_level}'")
        print(f" ==================================")
        
        return risk_level, confidence, prob_dict
        
    except Exception as e:
        print(f" Prediction error: {e}")
        import traceback
        traceback.print_exc()
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
            'confidence': confidence * 100,  # Convert to percentage (0-100)
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
