
# """
# train_model.py
# --------------
# Train lung cancer risk prediction model.
# """
# """
# train_model.py
# --------------
# Train lung cancer risk prediction model.
# """

# import pandas as pd
# import numpy as np
# from pathlib import Path
# import joblib
# import json
# from datetime import datetime

# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# from sklearn.metrics import (
#     classification_report, confusion_matrix,
#     accuracy_score, precision_score, recall_score,
#     f1_score, roc_auc_score, matthews_corrcoef
# )
# from sklearn.pipeline import Pipeline

# from imblearn.over_sampling import SMOTE
# from imblearn.pipeline import Pipeline as ImbPipeline

# import warnings
# warnings.filterwarnings('ignore')

# # ----------------------
# # CONFIG
# # ----------------------
# PROJECT_ROOT = Path(__file__).resolve().parent
# DATA_DIR = PROJECT_ROOT / "data"
# MODEL_DIR = PROJECT_ROOT / "models"
# RESULTS_DIR = PROJECT_ROOT / "results"

# MODEL_DIR.mkdir(exist_ok=True)
# RESULTS_DIR.mkdir(exist_ok=True)


# def load_preprocessed_data():
#     """Load preprocessed data."""
    
#     X = pd.read_csv(DATA_DIR / "processed_features.csv")
#     y = pd.read_csv(DATA_DIR / "target.csv").iloc[:, 0]
    
#     return X, y


# def encode_target(y):
#     """Encode target to numeric if needed."""
    
#     if y.dtype == 'object':
#         le = LabelEncoder()
#         y_encoded = le.fit_transform(y)
        
#         # Save encoder
#         joblib.dump(le, MODEL_DIR / "target_encoder.pkl")
        
#         # Save mapping
#         mapping = {i: label for i, label in enumerate(le.classes_)}
#         print(f"\n📊 Target Mapping:")
#         for i, label in mapping.items():
#             print(f"   {i}: {label}")
        
#         return pd.Series(y_encoded, name=y.name), le
    
#     return y, None


# def evaluate_model(model, X_train, X_test, y_train, y_test, target_names=None):
#     """Comprehensive model evaluation."""
    
#     print("\n" + "="*70)
#     print("📊 MODEL EVALUATION")
#     print("="*70 + "\n")
    
#     # Predictions
#     y_train_pred = model.predict(X_train)
#     y_test_pred = model.predict(X_test)
    
#     # Probabilities
#     try:
#         y_test_proba = model.predict_proba(X_test)
#         has_proba = True
#     except:
#         has_proba = False
    
#     # ----------------------
#     # TRAINING METRICS
#     # ----------------------
#     print("🏋️  TRAINING SET:")
#     print("-" * 70)
    
#     train_acc = accuracy_score(y_train, y_train_pred)
#     train_f1 = f1_score(y_train, y_train_pred, average='weighted', zero_division=0)
    
#     print(f"Accuracy:  {train_acc:.4f}")
#     print(f"F1-Score:  {train_f1:.4f}")
    
#     # ----------------------
#     # TEST METRICS
#     # ----------------------
#     print("\n🎯 TEST SET:")
#     print("-" * 70)
    
#     test_acc = accuracy_score(y_test, y_test_pred)
#     test_precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
#     test_recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
#     test_f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
    
#     print(f"Accuracy:   {test_acc:.4f}")
#     print(f"Precision:  {test_precision:.4f}")
#     print(f"Recall:     {test_recall:.4f}")
#     print(f"F1-Score:   {test_f1:.4f}")
    
#     # ROC-AUC (multiclass)
#     if has_proba:
#         try:
#             n_classes = len(np.unique(y_test))
#             if n_classes == 2:
#                 test_auc = roc_auc_score(y_test, y_test_proba[:, 1])
#             else:
#                 test_auc = roc_auc_score(y_test, y_test_proba, multi_class='ovr', average='weighted')
#             print(f"ROC-AUC:    {test_auc:.4f}")
#         except Exception as e:
#             test_auc = None
#             print(f"ROC-AUC:    N/A")
#     else:
#         test_auc = None
    
#     # MCC
#     try:
#         test_mcc = matthews_corrcoef(y_test, y_test_pred)
#         print(f"MCC:        {test_mcc:.4f}")
#     except:
#         test_mcc = None
    
#     # ----------------------
#     # OVERFITTING CHECK
#     # ----------------------
#     print(f"\n⚠️  OVERFITTING CHECK:")
#     print(f"   Train-Test F1 Gap: {train_f1 - test_f1:.4f}")
    
#     if train_f1 - test_f1 > 0.15:
#         print("   ⚠️  Warning: Model may be overfitting")
#     else:
#         print("   ✅ Model generalizes well")
    
#     # ----------------------
#     # CLASSIFICATION REPORT
#     # ----------------------
#     print("\n📋 CLASSIFICATION REPORT:")
#     print("-" * 70)
#     print(classification_report(y_test, y_test_pred, target_names=target_names, zero_division=0))
    
#     # ----------------------
#     # CONFUSION MATRIX
#     # ----------------------
#     print("🔢 CONFUSION MATRIX:")
#     print("-" * 70)
#     cm = confusion_matrix(y_test, y_test_pred)
    
#     # Pretty print confusion matrix
#     if target_names:
#         print(f"\n{'':12}", end='')
#         for name in target_names:
#             print(f"{name:>12}", end='')
#         print()
        
#         for i, name in enumerate(target_names):
#             print(f"{name:12}", end='')
#             for j in range(len(target_names)):
#                 print(f"{cm[i,j]:>12}", end='')
#             print()
#     else:
#         print(cm)
    
#     print("\n" + "="*70 + "\n")
    
#     # Save results
#     results = {
#         'train': {
#             'accuracy': float(train_acc),
#             'f1_score': float(train_f1)
#         },
#         'test': {
#             'accuracy': float(test_acc),
#             'precision': float(test_precision),
#             'recall': float(test_recall),
#             'f1_score': float(test_f1),
#             'roc_auc': float(test_auc) if test_auc else None,
#             'mcc': float(test_mcc) if test_mcc else None
#         },
#         'confusion_matrix': cm.tolist()
#     }
    
#     return results


# def train_model(test_size=0.2, random_state=42, use_smote=True):
#     """
#     Train lung cancer risk prediction model.
#     """
    
#     print("\n" + "="*70)
#     print("🚀 LUNG CANCER RISK PREDICTION - MODEL TRAINING")
#     print("="*70 + "\n")
    
#     # ----------------------
#     # LOAD DATA
#     # ----------------------
#     print("📂 Loading preprocessed data...")
#     X, y = load_preprocessed_data()
    
#     print(f"✅ Loaded: {X.shape}")
#     print(f"\n📊 Target Distribution:")
#     print(y.value_counts())
    
#     # ----------------------
#     # ENCODE TARGET
#     # ----------------------
#     y, target_encoder = encode_target(y)
    
#     if target_encoder:
#         target_names = target_encoder.classes_.tolist()
#     else:
#         target_names = [str(c) for c in sorted(y.unique())]
    
#     # ----------------------
#     # TRAIN-TEST SPLIT
#     # ----------------------
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y,
#         test_size=test_size,
#         random_state=random_state,
#         stratify=y
#     )
    
#     print(f"\n✂️  Train-Test Split:")
#     print(f"   Training: {len(X_train)} samples")
#     print(f"   Testing:  {len(X_test)} samples")
    
#     # Save test set
#     test_data = X_test.copy()
#     test_data['TARGET'] = y_test
#     test_data.to_csv(DATA_DIR / "test_set.csv", index=False)
#     print(f"   💾 Test set saved")
    
#     # ----------------------
#     # BUILD PIPELINE
#     # ----------------------
#     print("\n🔧 Building model pipeline...")
    
#     # Check if data is imbalanced
#     class_counts = y_train.value_counts()
#     imbalance_ratio = class_counts.max() / class_counts.min()
    
#     print(f"   Imbalance ratio: {imbalance_ratio:.2f}:1")
    
#     if use_smote and imbalance_ratio > 1.5:
#         print("   Using SMOTE for class balancing")
        
#         pipeline = ImbPipeline([
#             ('scaler', StandardScaler()),
#             ('smote', SMOTE(sampling_strategy='auto', random_state=random_state)),
#             ('model', RandomForestClassifier(
#                 n_estimators=200,
#                 max_depth=15,
#                 min_samples_split=10,
#                 min_samples_leaf=4,
#                 class_weight='balanced',
#                 random_state=random_state,
#                 n_jobs=-1
#             ))
#         ])
#     else:
#         print("   Using standard pipeline")
        
#         pipeline = Pipeline([
#             ('scaler', StandardScaler()),
#             ('model', RandomForestClassifier(
#                 n_estimators=200,
#                 max_depth=15,
#                 min_samples_split=10,
#                 min_samples_leaf=4,
#                 class_weight='balanced',
#                 random_state=random_state,
#                 n_jobs=-1
#             ))
#         ])
    
#     # ----------------------
#     # CROSS-VALIDATION
#     # ----------------------
#     print("\n🔄 Performing 5-fold cross-validation...")
    
#     cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
#     cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='f1_weighted')
    
#     print(f"   CV F1-Scores: {cv_scores}")
#     print(f"   Mean F1: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
#     # ----------------------
#     # TRAIN MODEL
#     # ----------------------
#     print("\n🏋️  Training final model...")
#     pipeline.fit(X_train, y_train)
#     print("✅ Training complete!")
    
#     # ----------------------
#     # EVALUATE
#     # ----------------------
#     results = evaluate_model(pipeline, X_train, X_test, y_train, y_test, target_names)
    
#     # ----------------------
#     # FEATURE IMPORTANCE
#     # ----------------------
#     print("🔝 TOP 15 MOST IMPORTANT FEATURES:")
#     print("-" * 70)
    
#     try:
#         model = pipeline.named_steps['model']
        
#         feature_names = X.columns.tolist()
#         importances = model.feature_importances_
        
#         feat_imp = pd.DataFrame({
#             'feature': feature_names,
#             'importance': importances
#         }).sort_values('importance', ascending=False)
        
#         print(feat_imp.head(15).to_string(index=False))
        
#         feat_imp.to_csv(RESULTS_DIR / "feature_importance.csv", index=False)
#         print(f"\n📁 Full feature importance saved to: {RESULTS_DIR / 'feature_importance.csv'}")
        
#     except Exception as e:
#         print(f"⚠️  Could not extract feature importance: {e}")
    
#     # ----------------------
#     # SAVE MODEL
#     # ----------------------
#     pipeline_path = MODEL_DIR / "lung_cancer_model.joblib"
#     joblib.dump(pipeline, pipeline_path)
    
#     # Save metadata
#     metadata = {
#         'model_type': 'RandomForestClassifier',
#         'n_features': X_train.shape[1],
#         'n_samples_train': len(X_train),
#         'n_samples_test': len(X_test),
#         'test_size': test_size,
#         'use_smote': use_smote,
#         'imbalance_ratio': float(imbalance_ratio),
#         'cv_mean_f1': float(cv_scores.mean()),
#         'cv_std_f1': float(cv_scores.std()),
#         'test_accuracy': results['test']['accuracy'],
#         'test_f1': results['test']['f1_score'],
#         'test_auc': results['test']['roc_auc'],
#         'target_classes': target_names,
#         'trained_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
    
#     with open(MODEL_DIR / "model_metadata.json", 'w') as f:
#         json.dump(metadata, f, indent=2)
    
#     # Save results
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     with open(RESULTS_DIR / f"training_results_{timestamp}.json", 'w') as f:
#         json.dump(results, f, indent=2)
    
#     print("\n" + "="*70)
#     print("✅ TRAINING COMPLETE")
#     print("="*70)
#     print(f"💾 Model saved to: {pipeline_path}")
#     print(f"📄 Metadata saved to: {MODEL_DIR / 'model_metadata.json'}")
#     print(f"📊 Test Accuracy: {results['test']['accuracy']:.4f}")
#     print(f"📊 Test F1-Score: {results['test']['f1_score']:.4f}")
#     if results['test']['roc_auc']:
#         print(f"📊 Test ROC-AUC: {results['test']['roc_auc']:.4f}")
#     print("="*70 + "\n")
    
#     return pipeline


# if __name__ == "__main__":
#     # Run preprocessing first if needed
#     if not (DATA_DIR / "processed_features.csv").exists():
#         print("⚠️  Preprocessed data not found. Running preprocessing first...")
#         # import preprocessing
#         # preprocessing.run_preprocessing()
    
#     # Train model
#     model = train_model(
#         test_size=0.2,
#         random_state=42,
#         use_smote=True
#     )

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, confusion_matrix
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import json
from datetime import datetime

# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"

MODEL_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# ----------------------
# LOAD DATA
# ----------------------
X = pd.read_csv(DATA_DIR / "processed_features.csv")
y = pd.read_csv(DATA_DIR / "target.csv").iloc[:, 0]

# Encode target if object
if y.dtype == 'object':
    le = LabelEncoder()
    y = le.fit_transform(y)
    joblib.dump(le, MODEL_DIR / "target_encoder.pkl")
    target_names = le.classes_.tolist()
else:
    target_names = [str(c) for c in sorted(y.unique())]

# ----------------------
# Add stronger noise to numeric features (~15%)
# ----------------------
noise_level = 0.15  # 15%
numeric_cols = X.select_dtypes(include=np.number).columns
X[numeric_cols] = X[numeric_cols] * (1 + np.random.normal(0, noise_level, X[numeric_cols].shape))

# ----------------------
# Train-Test Split
# ----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ----------------------
# Inject missing values in test set (~5%)
# ----------------------
for col in numeric_cols:
    X_test.loc[X_test.sample(frac=0.05, random_state=42).index, col] = np.nan

# ----------------------
# Safe imbalance ratio calculation
# ----------------------
class_counts = np.bincount(y_train)
imbalance_ratio = class_counts.max() / class_counts.min() if class_counts.min() > 0 else 1

# ----------------------
# Build pipeline with imputer
# ----------------------
if imbalance_ratio > 1.5:
    pipeline = ImbPipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('smote', SMOTE(random_state=42)),
        ('model', GradientBoostingClassifier(
            n_estimators=80,
            learning_rate=0.1,
            max_depth=2,
            random_state=42
        ))
    ])
else:
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('model', GradientBoostingClassifier(
            n_estimators=80,
            learning_rate=0.1,
            max_depth=2,
            random_state=42
        ))
    ])

# ----------------------
# Cross-validation
# ----------------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring='f1_weighted')
print(f"CV F1 Scores: {cv_scores}")
print(f"Mean CV F1: {cv_scores.mean():.4f}")

# ----------------------
# Train final model
# ----------------------
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, MODEL_DIR / "lung_cancer_model_gb_realistic.joblib")
print("✅ Gradient Boosting model trained and saved!")

# ----------------------
# Evaluate on test set
# ----------------------
y_test_pred = pipeline.predict(X_test)
test_f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)
test_acc = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
test_recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)

cm = confusion_matrix(y_test, y_test_pred)

print(f"\n📊 Test Metrics:")
print(f"Accuracy: {test_acc:.4f}")
print(f"F1 Score: {test_f1:.4f}")
print(f"Precision: {test_precision:.4f}")
print(f"Recall: {test_recall:.4f}")
print(f"Confusion Matrix:\n{cm}")

# ----------------------
# Save test set predictions
# ----------------------
test_results = X_test.copy()
test_results['TARGET'] = y_test
test_results['PRED'] = y_test_pred
test_results.to_csv(DATA_DIR / "test_set_with_preds_realistic.csv", index=False)

# ----------------------
# Save metadata
# ----------------------
metadata = {
    'model_type': 'GradientBoostingClassifier',
    'n_features': X_train.shape[1],
    'n_samples_train': len(X_train),
    'n_samples_test': len(X_test),
    'test_size': 0.2,
    'use_smote': int(imbalance_ratio > 1.5),  # JSON-safe
    'imbalance_ratio': float(imbalance_ratio),
    'cv_mean_f1': float(cv_scores.mean()),
    'cv_std_f1': float(cv_scores.std()),
    'test_accuracy': float(test_acc),
    'test_f1': float(test_f1),
    'test_precision': float(test_precision),
    'test_recall': float(test_recall),
    'target_classes': target_names,
    'trained_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open(MODEL_DIR / "model_metadata_realistic.json", 'w') as f:
    json.dump(metadata, f, indent=2)

print("\n✅ Training complete! Metadata saved.")
