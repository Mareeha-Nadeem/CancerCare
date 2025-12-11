# import pandas as pd
# from pathlib import Path
# import joblib
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, f1_score
# from imblearn.over_sampling import SMOTE
# from sklearn.utils import resample

# DATA_DIR = Path(__file__).resolve().parent / "data"
# PIPELINE_PATH = Path(__file__).resolve().parent / "models/RF_Prediction_Pipeline.joblib"
# CLEANED_FEATURES = DATA_DIR / "cleaned_features.csv"
# Y_TARGET = DATA_DIR / "y_target.csv"

# # ----------------------------
# # Optional: Stratified Equal Sampling
# # ----------------------------
# def stratified_eq_sampling(X, y):
#     df = pd.concat([X, y], axis=1)
#     grouped = df.groupby(y.name)
#     n_samples = len(y)
#     per_group = max(1, n_samples // len(grouped))
#     sampled = grouped.apply(lambda x: resample(x, n_samples=per_group, replace=True))
#     sampled = sampled.droplevel(0).reset_index(drop=True)
#     return sampled.drop(columns=[y.name]), sampled[y.name]

# def main():
#     print("--- 🚀 Testing Saved Pipeline ---")

#     # Load saved pipeline
#     pipeline = joblib.load(PIPELINE_PATH)
#     print("✅ Pipeline loaded successfully.")

#     # Load features & target
#     X = pd.read_csv(CLEANED_FEATURES)
#     y = pd.read_csv(Y_TARGET).squeeze()

#     # --- Create a balanced test set for evaluation ---
#     X_sampled, y_sampled = stratified_eq_sampling(X, y)
#     smt = SMOTE(random_state=42)
#     X_bal, y_bal = smt.fit_resample(X_sampled, y_sampled)

#     # Split into test set (30%)
#     _, X_test, _, y_test = train_test_split(X_bal, y_bal, test_size=0.3, random_state=42)

#     # Predict
#     y_pred = pipeline.predict(X_test)

#     print("\n--- 🎯 Test Results (Balanced Set) ---")
#     print(classification_report(y_test, y_pred, zero_division=0))
#     print(f"F1 Score: {f1_score(y_test, y_pred):.3f}")

# if __name__ == "__main__":
#     main()

import pandas as pd
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score

DATA_DIR = Path(__file__).resolve().parent / "data"
MODEL_PATH = Path(__file__).resolve().parent / "models/RF_Prediction_Pipeline.joblib"
CLEANED_FEATURES = DATA_DIR / "cleaned_features.csv"
Y_TARGET = DATA_DIR / "y_target.csv"

def main():
    print("--- 🚀 Testing Saved Pipeline ---")
    pipeline = joblib.load(MODEL_PATH)
    print("✅ Pipeline loaded successfully.")

    X = pd.read_csv(CLEANED_FEATURES)
    y = pd.read_csv(Y_TARGET).squeeze()

    # Split for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    y_pred = pipeline.predict(X_test)

    print("\n--- 🎯 Test Results ---")
    f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
+   print(f"F1 Score (macro): {f1:.3f}")
# ...existing code...

if __name__ == "__main__":
    main()

