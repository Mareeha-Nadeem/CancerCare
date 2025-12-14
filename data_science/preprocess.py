"""
preprocessing.py
----------------
Preprocessing for Lung Cancer Prediction Dataset
All features are pre-diagnosis risk factors.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import sys

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin

# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw_data.csv"
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"

DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

TARGET_COL = "Level"  # Target: Low, Medium, High risk


class LungCancerFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Feature engineering for lung cancer risk prediction.
    Creates composite risk scores from related features.
    """
    
    def __init__(self):
        self.feature_mappings = {}
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X.copy()
        
        # ==========================================
        # ENCODE CATEGORICAL FEATURES TO NUMERIC
        # ==========================================
        
        # Most features are categorical levels (1-8 scale typically)
        # Keep as numeric if already numeric, otherwise encode
        
        for col in X.columns:
            if X[col].dtype == 'object':
                # Try to convert to numeric first
                try:
                    X[col] = pd.to_numeric(X[col])
                except:
                    # If can't convert, use label encoding
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col].astype(str))
        
        # Ensure all numeric
        X = X.apply(pd.to_numeric, errors='coerce')
        
        # ==========================================
        # COMPOSITE RISK SCORES
        # ==========================================
        
        # Smoking Risk Score (smoking + passive smoking)
        if 'SMOKING' in X.columns and 'PASSIVE_SMOKER' in X.columns:
            X['SMOKING_RISK'] = (X['SMOKING'] + X['PASSIVE_SMOKER']) / 2
        
        # Environmental Risk (air pollution + dust + occupational)
        env_features = ['AIR_POLLUTION', 'DUST_ALLERGY', 'OCCUPATIONAL_HAZARDS']
        available_env = [f for f in env_features if f in X.columns]
        if available_env:
            X['ENVIRONMENTAL_RISK'] = X[available_env].mean(axis=1)
        
        # Lifestyle Risk (alcohol + obesity + balanced diet inverted)
        if 'ALCOHOL_USE' in X.columns and 'OBESITY' in X.columns:
            X['LIFESTYLE_RISK'] = X['ALCOHOL_USE'] + X['OBESITY']
            if 'BALANCED_DIET' in X.columns:
                # Higher balanced diet = lower risk (invert)
                max_diet = X['BALANCED_DIET'].max()
                X['LIFESTYLE_RISK'] += (max_diet - X['BALANCED_DIET'])
            X['LIFESTYLE_RISK'] = X['LIFESTYLE_RISK'] / 3
        
        # Genetic + Chronic Disease Risk
        if 'GENETIC_RISK' in X.columns and 'CHRONIC_LUNG_DISEASE' in X.columns:
            X['HEREDITARY_RISK'] = (X['GENETIC_RISK'] + X['CHRONIC_LUNG_DISEASE']) / 2
        
        # Symptom Severity Score (all symptoms combined)
        symptom_features = [
            'CHEST_PAIN', 'COUGHING_OF_BLOOD', 'FATIGUE', 'WEIGHT_LOSS',
            'SHORTNESS_OF_BREATH', 'WHEEZING', 'SWALLOWING_DIFFICULTY',
            'CLUBBING_OF_FINGER_NAILS'
        ]
        available_symptoms = [f for f in symptom_features if f in X.columns]
        if available_symptoms:
            X['SYMPTOM_SEVERITY'] = X[available_symptoms].mean(axis=1)
        
        # Total Risk Score (weighted combination)
        risk_components = []
        weights = []
        
        if 'SMOKING_RISK' in X.columns:
            risk_components.append(X['SMOKING_RISK'])
            weights.append(0.30)  # Smoking is most important
        
        if 'ENVIRONMENTAL_RISK' in X.columns:
            risk_components.append(X['ENVIRONMENTAL_RISK'])
            weights.append(0.20)
        
        if 'LIFESTYLE_RISK' in X.columns:
            risk_components.append(X['LIFESTYLE_RISK'])
            weights.append(0.15)
        
        if 'HEREDITARY_RISK' in X.columns:
            risk_components.append(X['HEREDITARY_RISK'])
            weights.append(0.20)
        
        if 'SYMPTOM_SEVERITY' in X.columns:
            risk_components.append(X['SYMPTOM_SEVERITY'])
            weights.append(0.15)
        
        if risk_components:
            total_risk = sum(comp * weight for comp, weight in zip(risk_components, weights))
            X['TOTAL_RISK_SCORE'] = total_risk
        
        # ==========================================
        # AGE-BASED FEATURES
        # ==========================================
        
        if 'AGE' in X.columns:
            # Age risk increases exponentially
            X['AGE_RISK'] = np.where(
                X['AGE'] < 40, 1,
                np.where(X['AGE'] < 50, 2,
                np.where(X['AGE'] < 60, 3,
                np.where(X['AGE'] < 70, 4, 5)))
            )
            
            # Age groups
            X['AGE_GROUP'] = pd.cut(
                X['AGE'],
                bins=[0, 40, 50, 60, 70, 100],
                labels=[0, 1, 2, 3, 4]
            ).astype(float)
        
        # ==========================================
        # INTERACTION FEATURES
        # ==========================================
        
        # Smoking × Age (critical for lung cancer)
        if 'SMOKING_RISK' in X.columns and 'AGE_RISK' in X.columns:
            X['SMOKING_AGE_INTERACTION'] = X['SMOKING_RISK'] * X['AGE_RISK']
        
        # Environmental × Smoking
        if 'ENVIRONMENTAL_RISK' in X.columns and 'SMOKING_RISK' in X.columns:
            X['ENV_SMOKING_INTERACTION'] = X['ENVIRONMENTAL_RISK'] * X['SMOKING_RISK']
        
        # Genetic × Age
        if 'GENETIC_RISK' in X.columns and 'AGE_RISK' in X.columns:
            X['GENETIC_AGE_INTERACTION'] = X['GENETIC_RISK'] * X['AGE_RISK']
        
        # Fill any NaN values
        X = X.fillna(0)
        
        return X


def run_preprocessing():
    """
    Main preprocessing function.
    """
    
    print("\n" + "="*70)
    print("🔧 LUNG CANCER DATA PREPROCESSING")
    print("="*70 + "\n")
    
    # ----------------------
    # LOAD DATA
    # ----------------------
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"✅ Loaded data: {df.shape}")
    except FileNotFoundError:
        print(f"❌ File not found: {RAW_DATA_PATH}")
        print(f"   Please download the dataset and place it in: {DATA_DIR}")
        sys.exit(1)
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    print(f"📋 Columns: {list(df.columns)}\n")
    
    # ----------------------
    # DATA CLEANING
    # ----------------------
    
    # Remove duplicates
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    print(f"🧹 Removed {initial_rows - len(df)} duplicates")
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"\n⚠️  Missing values found:")
        print(missing[missing > 0])
    else:
        print("✅ No missing values")
    
    # ----------------------
    # TARGET VARIABLE
    # ----------------------
    
    target_upper = TARGET_COL.upper()
    if target_upper not in df.columns:
        print(f"\n❌ Target column '{target_upper}' not found!")
        print(f"Available columns: {list(df.columns)}")
        sys.exit(1)
    
    print(f"\n📊 Target Distribution:")
    print(df[target_upper].value_counts())
    
    # Separate features and target
    y = df[target_upper]
    X = df.drop(columns=[target_upper])
    
    print(f"\n📊 Dataset Info:")
    print(f"   Features: {X.shape}")
    print(f"   Samples: {len(X)}")
    
    # ----------------------
    # FEATURE ENGINEERING
    # ----------------------
    
    print(f"\n🔧 Applying feature engineering...")
    
    feature_engineer = LungCancerFeatureEngineer()
    X_engineered = feature_engineer.fit_transform(X)
    
    print(f"✅ Engineered features: {X_engineered.shape}")
    print(f"   Original features: {X.shape[1]}")
    print(f"   New features: {X_engineered.shape[1] - X.shape[1]}")
    
    # ----------------------
    # SAVE OUTPUTS
    # ----------------------
    
    X_engineered.to_csv(DATA_DIR / "processed_features.csv", index=False)
    y.to_csv(DATA_DIR / "target.csv", index=False)
    
    # Save feature engineer
    joblib.dump(feature_engineer, MODEL_DIR / "feature_engineer.pkl")
    
    # Save feature names
    feature_names = X_engineered.columns.tolist()
    with open(MODEL_DIR / "feature_names.txt", 'w') as f:
        f.write('\n'.join(feature_names))
    
    # Save metadata
    metadata = {
        'n_samples': len(X_engineered),
        'n_features': X_engineered.shape[1],
        'target_classes': y.value_counts().to_dict(),
        'feature_names': feature_names
    }
    
    import json
    with open(MODEL_DIR / "preprocessing_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print("✅ PREPROCESSING COMPLETE")
    print(f"{'='*70}")
    print(f"📁 Features saved to: {DATA_DIR / 'processed_features.csv'}")
    print(f"📁 Target saved to: {DATA_DIR / 'target.csv'}")
    print(f"📁 Feature engineer saved to: {MODEL_DIR / 'feature_engineer.pkl'}")
    print(f"{'='*70}\n")
    
    return X_engineered, y


if __name__ == "__main__":
    X, y = run_preprocessing()