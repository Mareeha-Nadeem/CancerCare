"""
predict.py
----------
Make prediction for single lung cancer patient (demo).
"""

import pandas as pd
from pathlib import Path
import joblib

# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"

# ----------------------
# LOAD PIPELINE
# ----------------------
feature_engineer = joblib.load(MODEL_DIR / "feature_engineer.pkl")
model = joblib.load(MODEL_DIR / "lung_cancer_model.joblib")

# Load feature names from preprocessing metadata
with open(MODEL_DIR / "feature_names.txt") as f:
    training_columns = [line.strip() for line in f.readlines()]

# ----------------------
# DUMMY PATIENT DATA
# ----------------------
patient_data = {
    "AGE": 56,
    "GENDER": "Male",
    "AIR_POLLUTION": 7,
    "ALCOHOL_USE": 1,
    "DUST_ALLERGY": 7,
    "OCCUPATIONAL_HAZARDS": 7,
    "GENETIC_RISK": 1,
    "CHRONIC_LUNG_DISEASE": 7,
    "BALANCED_DIET": 7,
    "OBESITY": 7,
    "SMOKING": 7,
    "PASSIVE_SMOKER": 7,
    "CHEST_PAIN": 7,
    "COUGHING_OF_BLOOD": 7,
    "FATIGUE": 7,
    "WEIGHT_LOSS": 7,
    "SHORTNESS_OF_BREATH": 7,
    "WHEEZING": 7,
    "SWALLOWING_DIFFICULTY": 7,
    "CLUBBING_OF_FINGER_NAILS": 7,
    "DRY_COUGH": 0,
    "FREQUENT_COLD": 0,
    "SNORING": 0
}

# ----------------------
# PREPARE DATAFRAME
# ----------------------
df = pd.DataFrame([patient_data])

# Normalize column names to match training
df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

# Reindex to match training columns, missing columns filled with 0
df = df.reindex(columns=training_columns, fill_value=0)

# Transform features
df_engineered = feature_engineer.transform(df)

# ----------------------
# MAKE PREDICTION
# ----------------------
prediction = model.predict(df_engineered)[0]
probabilities = model.predict_proba(df_engineered)[0]
confidence = max(probabilities)

# ----------------------
# DISPLAY RESULTS
# ----------------------
print("\n🎯 Predicted Risk Level:", prediction)
print(f"📊 Confidence: {confidence:.1%}")
print("📈 Probabilities:")
for i, prob in enumerate(probabilities):
    print(f"   Class {i}: {prob:.1%}")
