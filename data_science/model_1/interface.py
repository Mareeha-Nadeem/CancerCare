"""
test_model.py
-------------
Test trained lung cancer prediction model on test set or new data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
from datetime import datetime

from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, matthews_corrcoef
)

import warnings
warnings.filterwarnings('ignore')

# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)


def load_model_and_metadata():
    """Load the trained model and its metadata."""
    model_dir = PROJECT_ROOT / "models"
    model_path = model_dir / "lung_cancer_pipeline.pkl"
    metadata_path = model_dir / "model_metadata.json"
    
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}\n"
            "Please train the model first: python train_model.py"
        )
    
    print(f"📂 Loading model from {model_path}")
    model = joblib.load(model_path)
    
    # Load metadata = {}
    metadata = {}
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        print(f"✅ Model loaded (trained: {metadata.get('trained_on', 'Unknown')})")
    
    # Load target encoder if exists
    target_encoder = None
    encoder_path = MODEL_DIR / "target_encoder.pkl"
    if encoder_path.exists():
        target_encoder = joblib.load(encoder_path)
    
    return model, metadata, target_encoder


def test_model(test_data_path=None):
    """
    Test model on test set or custom data.
    
    Parameters:
    -----------
    test_data_path : str or Path, optional
        Path to test data CSV. If None, uses saved test set.
    """
    
    print("\n" + "="*70)
    print("🧪 MODEL TESTING")
    print("="*70 + "\n")
    
    # ----------------------
    # LOAD MODEL
    # ----------------------
    model, metadata, target_encoder = load_model_and_metadata()
    
    # ----------------------
    # LOAD TEST DATA
    # ----------------------
    if test_data_path is None:
        test_data_path = DATA_DIR / "test_set.csv"
    
    if not Path(test_data_path).exists():
        raise FileNotFoundError(f"Test data not found at {test_data_path}")
    
    print(f"📂 Loading test data from: {test_data_path}")
    df_test = pd.read_csv(test_data_path)
    
    # Separate features and target
    if 'TARGET' in df_test.columns:
        y_test = df_test['TARGET']
        X_test = df_test.drop(columns=['TARGET'])
        has_labels = True
    else:
        X_test = df_test
        y_test = None
        has_labels = False
    
    print(f"✅ Loaded: {X_test.shape}")
    
    # ----------------------
    # MAKE PREDICTIONS
    # ----------------------
    print("\n🔮 Making predictions...")
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    # Decode predictions if encoder exists
    if target_encoder:
        y_pred_labels = target_encoder.inverse_transform(y_pred)
        target_names = target_encoder.classes_.tolist()
        if has_labels:
            y_test_labels = target_encoder.inverse_transform(y_test)
    else:
        y_pred_labels = y_pred
        target_names = metadata.get('target_classes', None)
        if has_labels:
            y_test_labels = y_test
    
    print("✅ Predictions complete")
    
    # ----------------------
    # EVALUATE (if labels available)
    # ----------------------
    if has_labels:
        print("\n" + "="*70)
        print("📊 TEST SET PERFORMANCE")
        print("="*70 + "\n")
        
        # Metrics
        test_acc = accuracy_score(y_test, y_pred)
        test_precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        test_recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        test_f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"Accuracy:   {test_acc:.4f}")
        print(f"Precision:  {test_precision:.4f}")
        print(f"Recall:     {test_recall:.4f}")
        print(f"F1-Score:   {test_f1:.4f}")
        
        # ROC-AUC
        try:
            n_classes = len(np.unique(y_test))
            if n_classes == 2:
                test_auc = roc_auc_score(y_test, y_proba[:, 1])
            else:
                test_auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted')
            print(f"ROC-AUC:    {test_auc:.4f}")
        except:
            test_auc = None
        
        # MCC
        try:
            test_mcc = matthews_corrcoef(y_test, y_pred)
            print(f"MCC:        {test_mcc:.4f}")
        except:
            test_mcc = None
        
        # Classification Report
        print("\n📋 CLASSIFICATION REPORT:")
        print("-" * 70)
        print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0))
        
        # Confusion Matrix
        print("🔢 CONFUSION MATRIX:")
        print("-" * 70)
        cm = confusion_matrix(y_test, y_pred)
        
        if target_names:
            print(f"\n{'':12}", end='')
            for name in target_names:
                print(f"{name:>12}", end='')
            print()
            
            for i, name in enumerate(target_names):
                print(f"{name:12}", end='')
                for j in range(len(target_names)):
                    print(f"{cm[i,j]:>12}", end='')
                print()
        else:
            print(cm)
        
        # Per-class accuracy
        print(f"\n📈 PER-CLASS ACCURACY:")
        for i, name in enumerate(target_names or range(len(cm))):
            class_acc = cm[i,i] / cm[i].sum() if cm[i].sum() > 0 else 0
            print(f"   {name}: {class_acc:.4f} ({class_acc:.1%})")
        
        # Save results
        results = {
            'test_accuracy': float(test_acc),
            'test_precision': float(test_precision),
            'test_recall': float(test_recall),
            'test_f1': float(test_f1),
            'test_auc': float(test_auc) if test_auc else None,
            'test_mcc': float(test_mcc) if test_mcc else None,
            'confusion_matrix': cm.tolist(),
            'n_samples': len(y_test),
            'tested_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_path = RESULTS_DIR / f"test_results_{timestamp}.json"
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_path}")
    
    # ----------------------
    # SAVE PREDICTIONS
    # ----------------------
    print("\n📊 SAVING PREDICTIONS...")
    
    # Add predictions to dataframe
    predictions_df = X_test.copy()
    predictions_df['PREDICTED_CLASS'] = y_pred_labels
    predictions_df['CONFIDENCE'] = y_proba.max(axis=1)
    
    # Add probability for each class
    for i, class_name in enumerate(target_names or range(y_proba.shape[1])):
        predictions_df[f'PROB_{class_name}'] = y_proba[:, i]
    
    if has_labels:
        predictions_df['ACTUAL_CLASS'] = y_test_labels
        predictions_df['CORRECT'] = (y_pred == y_test).astype(int)
    
    # Save predictions
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pred_path = RESULTS_DIR / f"predictions_{timestamp}.csv"
    predictions_df.to_csv(pred_path, index=False)
    
    print(f"💾 Predictions saved to: {pred_path}")
    
    # Prediction summary
    print(f"\n📊 PREDICTION SUMMARY:")
    pred_counts = pd.Series(y_pred_labels).value_counts()
    for class_name, count in pred_counts.items():
        print(f"   {class_name}: {count} ({count/len(y_pred_labels)*100:.1f}%)")
    
    print("\n" + "="*70)
    print("✅ TESTING COMPLETE")
    print("="*70 + "\n")
    
    return predictions_df


if __name__ == "__main__":
    # Test on saved test set
    predictions = test_model()
    
    # Or test on custom data:
    # predictions = test_model("path/to/custom_test_data.csv")