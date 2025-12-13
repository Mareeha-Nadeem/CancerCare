
"""
train_model.py
--------------
Trains cancer pre-diagnosis prediction model with proper evaluation.
Saves trained pipeline for use in testing and prediction.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
from datetime import datetime

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, matthews_corrcoef
)
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import warnings
warnings.filterwarnings('ignore')

# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw_data.csv"
MODEL_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)



TARGET_COL = "FINAL_PREDICTION"

# Post-diagnosis columns (data leakage risk)
DROP_COLS = [
    "STAGE_AT_DIAGNOSIS",
    "CANCER_TYPE",
    "MUTATION_TYPE",
    "TREATMENT_ACCESS",
    "CLINICAL_TRIAL_ACCESS",
    "LANGUAGE_BARRIER",
    "DELAY_IN_DIAGNOSIS",
    "MORTALITY_RISK",
    "5_YEAR_SURVIVAL_PROBABILITY",
    "TOBACCO_MARKETING_EXPOSURE"
]


# ----------------------
# CUSTOM TRANSFORMERS
# ----------------------
class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Creates derived risk features from raw data."""
    
    def __init__(self):
        self.feature_mappings = {}
    
    def fit(self, X, y=None):
        # Store unique values for each categorical column
        for col in X.select_dtypes(include='object').columns:
            self.feature_mappings[col] = X[col].unique().tolist()
        return self
    
    def transform(self, X):
        X = X.copy()
        
        # Smoking Risk Score
        if 'SMOKING_STATUS' in X.columns:
            X['SMOKING_RISK'] = X['SMOKING_STATUS'].map({
                'Smoker': 2, 'Former Smoker': 1, 'Non-Smoker': 0
            }).fillna(0)
            
            if 'SECOND_HAND_SMOKE' in X.columns:
                X['SMOKING_RISK'] += X['SECOND_HAND_SMOKE'].map({'Yes': 1, 'No': 0}).fillna(0)
        
        # Environmental Risk Score
        if 'OCCUPATION_EXPOSURE' in X.columns and 'AIR_POLLUTION_EXPOSURE' in X.columns:
            X['ENVIRONMENTAL_RISK'] = (
                X['OCCUPATION_EXPOSURE'].map({'Yes': 1, 'No': 0}).fillna(0) +
                X['AIR_POLLUTION_EXPOSURE'].map({'Low': 0, 'Medium': 1, 'High': 2}).fillna(0)
            )
        
        # Tobacco Exposure Risk
        if 'INDOOR_SMOKE_EXPOSURE' in X.columns:
            X['TOBACCO_EXPOSURE_RISK'] = X['INDOOR_SMOKE_EXPOSURE'].map({'Yes': 1, 'No': 0}).fillna(0)
        
        # Healthcare Access Risk
        if 'HEALTHCARE_ACCESS' in X.columns:
            X['HEALTHCARE_RISK'] = X['HEALTHCARE_ACCESS'].map({
                'Good': 0, 'Limited': 1, 'Poor': 2
            }).fillna(1)
        
        # Socioeconomic Risk
        if 'SOCIOECONOMIC_STATUS' in X.columns:
            X['SOCIOECONOMIC_RISK'] = X['SOCIOECONOMIC_STATUS'].map({
                'High': 0, 'Middle': 1, 'Low': 2
            }).fillna(1)
        
        # Screening Risk
        if 'SCREENING_AVAILABILITY' in X.columns:
            X['SCREENING_RISK'] = X['SCREENING_AVAILABILITY'].map({'Yes': 0, 'No': 1}).fillna(1)
        
        # Urban/Rural Risk
        if 'RURAL_OR_URBAN' in X.columns:
            X['URBAN_RURAL_RISK'] = X['RURAL_OR_URBAN'].map({'Urban': 0, 'Rural': 1}).fillna(0)
        
        # Age Group
        if 'AGE' in X.columns:
            X['AGE_GROUP'] = pd.cut(
                X['AGE'], 
                bins=[0, 40, 50, 60, 70, 80, 100], 
                labels=[0, 1, 2, 3, 4, 5]
            ).astype(float)
        
        # Drop original categorical columns that were transformed
        drop_cols = [
            'SMOKING_STATUS', 'SECOND_HAND_SMOKE', 'OCCUPATION_EXPOSURE', 
            'AIR_POLLUTION_EXPOSURE', 'INDOOR_SMOKE_EXPOSURE', 
            'HEALTHCARE_ACCESS', 'SOCIOECONOMIC_STATUS', 
            'SCREENING_AVAILABILITY', 'RURAL_OR_URBAN'
        ]
        X.drop(columns=[c for c in drop_cols if c in X.columns], inplace=True)
        
        return X


class CategoricalEncoder(BaseEstimator, TransformerMixin):
    """Encodes remaining categorical features."""
    
    def __init__(self):
        self.encoders = {}
    
    def fit(self, X, y=None):
        X = X.copy()
        cat_cols = X.select_dtypes(include='object').columns
        
        for col in cat_cols:
            le = LabelEncoder()
            le.fit(X[col].astype(str))
            self.encoders[col] = le
        
        return self
    
    def transform(self, X):
        X = X.copy()
        
        for col, encoder in self.encoders.items():
            if col in X.columns:
                # Handle unknown categories
                X[col] = X[col].astype(str).apply(
                    lambda x: x if x in encoder.classes_ else encoder.classes_[0]
                )
                X[col] = encoder.transform(X[col])
        
        return X


# ----------------------
# EVALUATION FUNCTIONS
# ----------------------
def evaluate_model(model, X_train, X_test, y_train, y_test, save_results=True):
    """Comprehensive model evaluation."""
    
    print("\n" + "="*60)
    print("📊 MODEL EVALUATION")
    print("="*60 + "\n")
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Probabilities (if available)
    try:
        y_train_proba = model.predict_proba(X_train)
        y_test_proba = model.predict_proba(X_test)
        has_proba = True
    except:
        has_proba = False
    
    results = {}
    
    # ----------------------
    # TRAINING METRICS
    # ----------------------
    print("🏋️  TRAINING SET PERFORMANCE:")
    print("-" * 60)
    
    train_acc = accuracy_score(y_train, y_train_pred)
    train_precision = precision_score(y_train, y_train_pred, average='weighted', zero_division=0)
    train_recall = recall_score(y_train, y_train_pred, average='weighted', zero_division=0)
    train_f1 = f1_score(y_train, y_train_pred, average='weighted', zero_division=0)
    
    print(f"Accuracy:  {train_acc:.4f}")
    print(f"Precision: {train_precision:.4f}")
    print(f"Recall:    {train_recall:.4f}")
    print(f"F1-Score:  {train_f1:.4f}")
    
    results['train'] = {
        'accuracy': train_acc,
        'precision': train_precision,
        'recall': train_recall,
        'f1_score': train_f1
    }
    
    # ----------------------
    # TEST METRICS
    # ----------------------
    print("\n🎯 TEST SET PERFORMANCE:")
    print("-" * 60)
    
    test_acc = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
    test_recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
    test_f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
    test_mcc = matthews_corrcoef(y_test, y_test_pred)
    
    print(f"Accuracy:  {test_acc:.4f}")
    print(f"Precision: {test_precision:.4f}")
    print(f"Recall:    {test_recall:.4f}")
    print(f"F1-Score:  {test_f1:.4f}")
    print(f"MCC:       {test_mcc:.4f}")
    
    results['test'] = {
        'accuracy': test_acc,
        'precision': test_precision,
        'recall': test_recall,
        'f1_score': test_f1,
        'mcc': test_mcc
    }
    
    # ROC-AUC (if binary or multi-class with probabilities)
    if has_proba:
        try:
            if len(np.unique(y_test)) == 2:
                test_auc = roc_auc_score(y_test, y_test_proba[:, 1])
            else:
                test_auc = roc_auc_score(y_test, y_test_proba, multi_class='ovr', average='weighted')
            print(f"ROC-AUC:   {test_auc:.4f}")
            results['test']['roc_auc'] = test_auc
        except:
            pass
    
    # ----------------------
    # OVERFITTING CHECK
    # ----------------------
    print("\n⚠️  OVERFITTING ANALYSIS:")
    print("-" * 60)
    
    acc_diff = train_acc - test_acc
    f1_diff = train_f1 - test_f1
    
    print(f"Accuracy Gap (Train - Test):  {acc_diff:.4f}")
    print(f"F1-Score Gap (Train - Test):  {f1_diff:.4f}")
    
    if acc_diff > 0.1 or f1_diff > 0.1:
        print("⚠️  WARNING: Model may be overfitting!")
    else:
        print("✅ Model shows good generalization")
    
    results['overfitting'] = {
        'accuracy_gap': acc_diff,
        'f1_gap': f1_diff
    }
    
    # ----------------------
    # CLASSIFICATION REPORT
    # ----------------------
    print("\n📋 DETAILED CLASSIFICATION REPORT (TEST SET):")
    print("-" * 60)
    print(classification_report(y_test, y_test_pred, zero_division=0))
    
    # ----------------------
    # CONFUSION MATRIX
    # ----------------------
    print("\n🔢 CONFUSION MATRIX (TEST SET):")
    print("-" * 60)
    cm = confusion_matrix(y_test, y_test_pred)
    print(cm)
    
    results['confusion_matrix'] = cm.tolist()
    results['classification_report'] = classification_report(
        y_test, y_test_pred, output_dict=True, zero_division=0
    )
    
    # ----------------------
    # SAVE RESULTS
    # ----------------------
    if save_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = RESULTS_DIR / f"evaluation_results_{timestamp}.json"
        
        # Convert numpy types to Python types for JSON serialization
        def convert_to_serializable(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        results_serializable = json.loads(
            json.dumps(results, default=convert_to_serializable)
        )
        
        with open(results_file, 'w') as f:
            json.dump(results_serializable, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
    
    print("\n" + "="*60 + "\n")
    
    return results


def cross_validate_model(pipeline, X, y, cv=5):
    """Perform stratified k-fold cross-validation."""
    
    print("\n" + "="*60)
    print("🔄 CROSS-VALIDATION")
    print("="*60 + "\n")
    
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    
    cv_scores = cross_val_score(pipeline, X, y, cv=skf, scoring='f1_weighted', n_jobs=-1)
    
    print(f"Cross-Validation F1-Scores: {cv_scores}")
    print(f"Mean F1-Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return cv_scores


# ----------------------
# MAIN TRAINING FUNCTION
# ----------------------
def train_model(test_size=0.2, random_state=42, use_smote=True, cv_folds=5):
    """
    Train cancer pre-diagnosis prediction model with proper evaluation.
    
    Parameters:
    -----------
    test_size : float
        Proportion of data for testing
    random_state : int
        Random seed for reproducibility
    use_smote : bool
        Whether to use SMOTE for handling imbalanced data
    cv_folds : int
        Number of cross-validation folds
    """
    
    print("\n" + "="*60)
    print("🚀 CANCER PRE-DIAGNOSIS MODEL TRAINING")
    print("="*60 + "\n")
    
    # ----------------------
    # LOAD DATA
    # ----------------------
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"✅ Loaded data: {df.shape}")
    except FileNotFoundError:
        print(f"❌ File not found: {RAW_DATA_PATH}")
        return None
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    
    # Drop post-diagnosis columns (prevent data leakage)
    drop_cols_upper = [c.upper() for c in DROP_COLS]
    leakage_cols_found = [c for c in drop_cols_upper if c in df.columns]
    
    if leakage_cols_found:
        df.drop(columns=leakage_cols_found, inplace=True)
        print(f"🛡️  Removed {len(leakage_cols_found)} post-diagnosis columns (data leakage prevention)")
    
    # Remove missing targets
    target_upper = TARGET_COL.upper()
    if target_upper not in df.columns:
        print(f"❌ Target column '{target_upper}' not found!")
        return None
    
    df = df[~df[target_upper].isna()]
    
    # ----------------------
    # SEPARATE FEATURES AND TARGET
    # ----------------------
    y = df[target_upper]
    X = df.drop(columns=[target_upper])
    
    print(f"\n📊 Dataset Overview:")
    print(f"   Samples: {len(X)}")
    print(f"   Features: {X.shape[1]}")
    print(f"   Target distribution:\n{y.value_counts()}")
    
    # ----------------------
    # TRAIN-TEST SPLIT (BEFORE ANY TRANSFORMATION!)
    # ----------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state,
        stratify=y
    )
    
    print(f"\n✂️  Train-Test Split:")
    print(f"   Training: {len(X_train)} samples")
    print(f"   Testing:  {len(X_test)} samples")
    
    # Save test set for later testing
    test_data = X_test.copy()
    test_data[target_upper] = y_test
    test_data.to_csv(DATA_DIR / "test_set.csv", index=False)
    print(f"💾 Test set saved to: {DATA_DIR / 'test_set.csv'}")
    
    # ----------------------
    # BUILD PIPELINE
    # ----------------------
    print("\n🔧 Building preprocessing and model pipeline...")
    
    if use_smote:
        pipeline = ImbPipeline([
            ('feature_engineer', FeatureEngineer()),
            ('encoder', CategoricalEncoder()),
            ('scaler', StandardScaler()),
            ('smote', SMOTE(random_state=random_state)),
            ('classifier', RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=10,
                min_samples_leaf=4,
                class_weight='balanced',
                random_state=random_state,
                n_jobs=-1
            ))
        ])
    else:
        pipeline = Pipeline([
            ('feature_engineer', FeatureEngineer()),
            ('encoder', CategoricalEncoder()),
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=10,
                min_samples_leaf=4,
                class_weight='balanced',
                random_state=random_state,
                n_jobs=-1
            ))
        ])
    
    print("✅ Pipeline components:")
    for step in pipeline.named_steps.keys():
        print(f"   → {step}")
    
    # ----------------------
    # CROSS-VALIDATION
    # ----------------------
    cv_scores = cross_validate_model(pipeline, X_train, y_train, cv=cv_folds)
    
    # ----------------------
    # TRAIN FINAL MODEL
    # ----------------------
    print("\n🏋️  Training final model...")
    pipeline.fit(X_train, y_train)
    print("✅ Model trained successfully!")
    
    # ----------------------
    # EVALUATE MODEL
    # ----------------------
    results = evaluate_model(pipeline, X_train, X_test, y_train, y_test)
    
    # ----------------------
    # FEATURE IMPORTANCE
    # ----------------------
    try:
        model = pipeline.named_steps['classifier']
        
        # Get feature names after all transformations
        X_train_sample = X_train.head(10)
        X_transformed = pipeline[:-1].transform(X_train_sample)
        
        if hasattr(X_transformed, 'columns'):
            feature_names = X_transformed.columns.tolist()
        else:
            feature_names = [f"feature_{i}" for i in range(X_transformed.shape[1])]
        
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        print("\n🔝 TOP 10 MOST IMPORTANT FEATURES:")
        print("-" * 60)
        print(feature_importance_df.head(10).to_string(index=False))
        
        feature_importance_df.to_csv(RESULTS_DIR / "feature_importance.csv", index=False)
        
    except Exception as e:
        print(f"⚠️  Could not extract feature importance: {e}")
    
    # ----------------------
    # SAVE PIPELINE
    # ----------------------
    pipeline_path = MODEL_DIR / "cancer_prediction_pipeline.joblib"
    joblib.dump(pipeline, pipeline_path)
    
    # Save metadata
    metadata = {
        'model_type': 'RandomForestClassifier',
        'n_features': X_train.shape[1],
        'n_samples_train': len(X_train),
        'n_samples_test': len(X_test),
        'test_size': test_size,
        'use_smote': use_smote,
        'cv_folds': cv_folds,
        'cv_mean_f1': float(cv_scores.mean()),
        'cv_std_f1': float(cv_scores.std()),
        'test_accuracy': results['test']['accuracy'],
        'test_f1': results['test']['f1_score'],
        'trained_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'random_state': random_state
    }
    
    with open(MODEL_DIR / "model_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE")
    print("="*60)
    print(f"💾 Pipeline saved to: {pipeline_path}")
    print(f"📄 Metadata saved to: {MODEL_DIR / 'model_metadata.json'}")
    print(f"📊 Results saved to: {RESULTS_DIR}")
    print(f"🧪 Test set saved to: {DATA_DIR / 'test_set.csv'}")
    print("="*60 + "\n")
    
    return pipeline


if __name__ == "__main__":
    # Train model
    pipeline = train_model(
        test_size=0.2,
        random_state=42,
        use_smote=True,
        cv_folds=5
    )