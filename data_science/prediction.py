# import pandas as pd
# from pathlib import Path
# import joblib
# import sys

# DATA_DIR = Path(__file__).resolve().parent / "data"
# MODEL_DIR = Path(__file__).resolve().parent / "models"

# PIPELINE_FILENAME = "RF_Prediction_Pipeline.joblib"
# PIPELINE_PATH = MODEL_DIR / PIPELINE_FILENAME
# CLEANED_FEATURES = DATA_DIR / "cleaned_features.csv"
# Y_TARGET = DATA_DIR / "y_target.csv"

# def main():
#     print(f"--- 🚀 Starting Prediction Test using {PIPELINE_FILENAME} ---")

#     try:
#         pipeline = joblib.load(PIPELINE_PATH)
#         print("✅ Pipeline loaded successfully.")
#     except FileNotFoundError:
#         print("❌ ERROR: Pipeline not found. Run train_model.py first.")
#         sys.exit(1)

#     X = pd.read_csv(CLEANED_FEATURES)
#     y = pd.read_csv(Y_TARGET).squeeze()

#     # Take a sample for testing
#     X_test_sample = X.iloc[[0]]
#     y_true = y.iloc[0]

#     pred = pipeline.predict(X_test_sample)[0]
#     prob = pipeline.predict_proba(X_test_sample)[0][1]

#     print("\n--- 🎯 Prediction Results ---")
#     print(f"RAW Features Shape: {X_test_sample.shape}")
#     print(f"True Label: {y_true} ({'High Risk' if y_true == 1 else 'No Risk'})")
#     print(f"Predicted Risk: **{'HIGH RISK' if pred == 1 else 'NO RISK'}** (Prob: {prob:.4f})")
#     print(f"Prediction Status: {'✅ CORRECT' if pred == y_true else '❌ INCORRECT'}")

# if __name__ == "__main__":
#     main()
import pandas as pd
from pathlib import Path
import joblib

DATA_DIR = Path(__file__).resolve().parent / "data"
MODEL_PATH = Path(__file__).resolve().parent / "models/RF_Prediction_Pipeline.joblib"
CLEANED_FEATURES = DATA_DIR / "cleaned_features.csv"

def main():
    print("--- 🚀 Starting Prediction Test ---")
    pipeline = joblib.load(MODEL_PATH)
    print("✅ Pipeline loaded successfully.")

    # Load a sample input for prediction
    X = pd.read_csv(CLEANED_FEATURES)
    sample = X.sample(1, random_state=42)  # pick a random row to predict
    pred = pipeline.predict(sample)[0]
    print(f"Predicted class for the sample: {pred}")

if __name__ == "__main__":
    main()
