"""
test_model.py
-------------
Tests trained model on held-out test set or new data.
Provides detailed performance metrics and error analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from train_model import FeatureEngineer, CategoricalEncoder

from sklearn.metrics import (
    classification_report, confusion_matrix, 
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, matthews_corrcoef,
    roc_curve, precision_recall_curve, auc
)

# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
PLOTS_DIR = RESULTS_DIR / "plots"

PLOTS_DIR.mkdir(exist_ok=True, parents=True)

TARGET_COL = "FINAL_PREDICTION"


def load_model_and_metadata():
    """Load trained pipeline and metadata."""
    
    pipeline_path = MODEL_DIR / "cancer_prediction_pipeline.joblib"
    metadata_path = MODEL_DIR / "model_metadata.json"
    
    if not pipeline_path.exists():
        raise FileNotFoundError(f"Model not found at {pipeline_path}. Train model first!")
    
    print(f"📦 Loading model from: {pipeline_path}")
    pipeline = joblib.load(pipeline_path)
    
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        print(f"📄 Model metadata loaded")
        print(f"   Trained on: {metadata.get('trained_on', 'Unknown')}")
        print(f"   Test F1-Score: {metadata.get('test_f1', 'N/A'):.4f}")
    else:
        metadata = {}
    
    return pipeline, metadata


def plot_confusion_matrix(cm, labels, save_path):
    """Plot and save confusion matrix."""
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📊 Confusion matrix saved to: {save_path}")


def plot_roc_curve(y_true, y_proba, save_path):
    """Plot and save ROC curve."""
    
    if len(np.unique(y_true)) == 2:
        # Convert y_true to binary 0/1
        y_bin = pd.Series(y_true).map({'No': 0, 'Yes': 1}).values
        
        fpr, tpr, _ = roc_curve(y_bin, y_proba[:, 1])
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                 label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"📊 ROC curve saved to: {save_path}")


def plot_precision_recall_curve(y_true, y_proba, save_path):
    """Plot and save precision-recall curve."""
    
    if len(np.unique(y_true)) == 2:
        y_bin = pd.Series(y_true).map({'No': 0, 'Yes': 1}).values
        precision, recall, _ = precision_recall_curve(y_bin, y_proba[:, 1])
        pr_auc = auc(recall, precision)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2,
                 label=f'PR curve (AUC = {pr_auc:.2f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend(loc="lower left")
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"📊 Precision-Recall curve saved to: {save_path}")


def analyze_errors(X_test, y_test, y_pred, y_proba, save_path):
    """Analyze misclassified samples."""
    
    misclassified_mask = y_test != y_pred
    
    if misclassified_mask.sum() == 0:
        print("✅ No misclassifications!")
        return
    
    misclassified = X_test[misclassified_mask].copy()
    misclassified['TRUE_LABEL'] = y_test[misclassified_mask].values
    misclassified['PREDICTED_LABEL'] = y_pred[misclassified_mask]
    misclassified['CONFIDENCE'] = y_proba[misclassified_mask].max(axis=1)
    
    misclassified = misclassified.sort_values('CONFIDENCE', ascending=False)
    misclassified.to_csv(save_path, index=False)
    
    print(f"\n❌ ERROR ANALYSIS:")
    print(f"   Total errors: {len(misclassified)}")
    print(f"   Error rate: {len(misclassified) / len(y_test):.2%}")
    print(f"   High confidence errors (>0.8): {(misclassified['CONFIDENCE'] > 0.8).sum()}")
    print(f"📄 Error details saved to: {save_path}")


def test_model(data_path=None, generate_plots=True):
    """Test trained model on test data."""
    
    print("\n" + "="*60)
    print("🧪 MODEL TESTING")
    print("="*60 + "\n")
    
    pipeline, metadata = load_model_and_metadata()
    
    if data_path is None:
        data_path = DATA_DIR / "test_set.csv"
    
    if not Path(data_path).exists():
        raise FileNotFoundError(f"Test data not found at {data_path}")
    
    print(f"📂 Loading test data from: {data_path}")
    df_test = pd.read_csv(data_path)
    df_test.columns = df_test.columns.str.strip().str.upper().str.replace(" ", "_")
    
    target_upper = TARGET_COL.upper()
    if target_upper not in df_test.columns:
        raise ValueError(f"Target column '{target_upper}' not found in test data!")
    
    y_test = df_test[target_upper]
    X_test = df_test.drop(columns=[target_upper])
    
    print(f"✅ Loaded test data: {X_test.shape}")
    print(f"   Target distribution:\n{y_test.value_counts()}\n")
    
    print("🔮 Making predictions...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)
    
    print("\n" + "="*60)
    print("📊 TEST SET PERFORMANCE")
    print("="*60 + "\n")
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    mcc = matthews_corrcoef(y_test, y_pred)
    
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"MCC:       {mcc:.4f}")
    
    try:
        if len(np.unique(y_test)) == 2:
            y_bin = pd.Series(y_test).map({'No': 0, 'Yes': 1}).values
            roc_auc = roc_auc_score(y_bin, y_proba[:, 1])
        else:
            roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted')
        print(f"ROC-AUC:   {roc_auc:.4f}")
    except:
        roc_auc = None
    
    print("\n📋 DETAILED CLASSIFICATION REPORT:")
    print("-" * 60)
    print(classification_report(y_test, y_pred, zero_division=0))
    
    print("\n🔢 CONFUSION MATRIX:")
    print("-" * 60)
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    if generate_plots:
        print("\n📊 Generating visualizations...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        labels = sorted(y_test.unique())
        plot_confusion_matrix(cm, labels, PLOTS_DIR / f"confusion_matrix_{timestamp}.png")
        
        if len(np.unique(y_test)) == 2:
            plot_roc_curve(y_test, y_proba, PLOTS_DIR / f"roc_curve_{timestamp}.png")
            plot_precision_recall_curve(y_test, y_proba, PLOTS_DIR / f"precision_recall_{timestamp}.png")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    analyze_errors(X_test, y_test, y_pred, y_proba, RESULTS_DIR / f"misclassified_samples_{timestamp}.csv")
    
    results = {
        'test_metrics': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'mcc': float(mcc),
            'roc_auc': float(roc_auc) if roc_auc else None
        },
        'confusion_matrix': cm.tolist(),
        'classification_report': classification_report(y_test, y_pred, output_dict=True, zero_division=0),
        'n_samples': len(y_test),
        'n_errors': int((y_test != y_pred).sum()),
        'error_rate': float((y_test != y_pred).mean()),
        'tested_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    results_file = RESULTS_DIR / f"test_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {results_file}")
    print("\n" + "="*60)
    print("✅ TESTING COMPLETE")
    print("="*60 + "\n")
    
    return results


if __name__ == "__main__":
    results = test_model(data_path=None, generate_plots=True)

# import shap
# import pandas as pd
# import joblib

# # Load model
# pipeline = joblib.load(r'D:\CancerCare\data_science\models\cancer_prediction_pipeline.joblib')

# # Load test data
# df_test = pd.read_csv(r'D:\CancerCare\data_science\data\test_set.csv')
# X_test = df_test.drop(columns=['FINAL_PREDICTION'])
# y_test = df_test['FINAL_PREDICTION']

# # Get model inside pipeline
# model = pipeline.named_steps['classifier']
# preprocessor = pipeline[:-1]  # everything before classifier

# # Transform features
# X_test_transformed = preprocessor.transform(X_test)

# # SHAP explainer
# explainer = shap.TreeExplainer(model)
# shap_values = explainer.shap_values(X_test_transformed)

# # Convert to DataFrame for easy viewing
# feature_names = X_test.columns.tolist()  # or adjust if preprocessor changes names
# shap_df = pd.DataFrame(shap_values[1], columns=feature_names)  # [1] = for 'Yes' class

# # Example: show top 5 contributing features for first 5 samples
# for i in range(5):
#     print(f"\nSample {i}: Actual={y_test.iloc[i]}")
#     top_features = shap_df.iloc[i].abs().sort_values(ascending=False).head(5)
#     print("Top contributing features:")
#     print(top_features)
