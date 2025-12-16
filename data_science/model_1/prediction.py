# import pandas as pd
# import joblib
# from pathlib import Path

# # ----------------------
# # CONFIG
# # ----------------------
# PROJECT_ROOT = Path(__file__).resolve().parent
# DATA_DIR = PROJECT_ROOT / "data"
# MODEL_DIR = PROJECT_ROOT / "models"

# # ----------------------
# # LOAD MODEL
# # ----------------------
# model_path = MODEL_DIR / "lung_cancer_model_gb_realistic.joblib"
# pipeline = joblib.load(model_path)
# print("✅ Model loaded!\n")

# # ----------------------
# # LOAD NEW DATA (or test set)
# # ----------------------
# X_new = pd.read_csv(DATA_DIR / "processed_features.csv")  # replace with any new data

# # ----------------------
# # MAKE PREDICTIONS
# # ----------------------
# preds = pipeline.predict(X_new)

# # Optional: probabilities
# try:
#     probs = pipeline.predict_proba(X_new)
# except:
#     probs = None

# # ----------------------
# # SHOW RESULTS
# # ----------------------
# print("📊 Predictions:")
# for i, pred in enumerate(preds[:10]):  # show first 10 predictions
#     line = f"Sample {i+1}: Predicted = {pred}"
#     if probs is not None:
#         prob_str = ", ".join([f"{p:.2f}" for p in probs[i]])
#         line += f" | Probabilities = [{prob_str}]"
#     print(line)



import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

# ----------------------
# Paths
# ----------------------
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"

# ----------------------
# Load model
# ----------------------
model_file = MODEL_DIR / "lung_cancer_model_gb_realistic.joblib"
pipeline = joblib.load(model_file)
model = pipeline.named_steps['model']
print("✅ Model loaded!\n")

# ----------------------
# Load feature CSV
# ----------------------
features_file = DATA_DIR / "processed_features.csv"
X = pd.read_csv(features_file)
print(f"📊 Loaded {len(X)} samples, {X.shape[1]} features\n")

# ----------------------
# Get feature names safely
# ----------------------
try:
    feature_names = pipeline.named_steps['scaler'].feature_names_in_
except AttributeError:
    feature_names = X.columns.tolist()

# ----------------------
# Feature importances
# ----------------------
importances = model.feature_importances_
feat_imp = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values(by='importance', ascending=False)

print("🔥 Top 15 Features by Importance:")
print(feat_imp.head(15).to_string(index=False))
print("\n")

# ----------------------
# Predictions and probabilities
# ----------------------
preds = pipeline.predict(X)

try:
    probs = pipeline.predict_proba(X)
except:
    probs = None

print("📊 Sample Predictions (first 10):")
for i in range(min(10, len(X))):
    line = f"Sample {i+1}: Predicted = {preds[i]}"
    if probs is not None:
        prob_str = ", ".join([f"{p:.2f}" for p in probs[i]])
        line += f" | Probabilities = [{prob_str}]"
    print(line)
print("\n")

# ----------------------
# Optional evaluation if target exists
# ----------------------
target_file = DATA_DIR / "target.csv"
if target_file.exists():
    y_true = pd.read_csv(target_file).iloc[:, 0]

    # encode if object
    if y_true.dtype == 'object':
        le = LabelEncoder()
        y_true = le.fit_transform(y_true)

    acc = accuracy_score(y_true, preds)
    f1 = f1_score(y_true, preds, average='weighted')
    cm = confusion_matrix(y_true, preds)

    print("📊 Test Metrics:")
    print(f"Accuracy: {acc:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(classification_report(y_true, preds))
