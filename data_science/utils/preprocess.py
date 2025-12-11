import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import sys

from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw_data.csv"
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

EXCLUDE_COLS = [
    "STAGE_AT_DIAGNOSIS",
    "CANCER_TYPE",
    "MUTATION_TYPE",
    "TREATMENT_ACCESS",
    "CLINICAL_TRIAL_ACCESS",
    "LANGUAGE_BARRIER",
    "DELAY_IN_DIAGNOSIS",
    "MORTALITY_RISK",
    "5_YEAR_SURVIVAL_PROBABILITY"
    "TOBACCO_MARKETING_EXPOSURE"
]

TARGET_COL = "FINAL_PREDICTION"


def run_preprocessing(sampling=None, n_samples=None):
    print("\n--- ⚙️ Running Preprocessing ---\n")

    # ----------------------
    # LOAD DATA
    # ----------------------
    try:
        df = pd.read_csv(RAW_DATA_PATH)
    except FileNotFoundError:
        print(f"❌ File not found: {RAW_DATA_PATH.resolve()}")
        sys.exit(1)

    # Normalize column names
    df.columns = [col.upper().replace(" ", "_") for col in df.columns]

    # Drop duplicates and IDs
    df.drop_duplicates(inplace=True)
    for col in ["PATIENT_ID", "ID", "INDEX"]:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Drop post-diagnosis columns
    drop_now = [c for c in EXCLUDE_COLS if c in df.columns]
    df.drop(columns=drop_now, inplace=True)
    print(f"Dropped columns: {drop_now}")

    # Check target
    if TARGET_COL not in df.columns:
        print(f"❌ Target column '{TARGET_COL}' missing!")
        sys.exit(1)

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    # ----------------------
    # FEATURE TYPES
    # ----------------------
    numerical_cols = [c for c in X.columns if X[c].dtype in [np.int64, np.float64]]
    categorical_cols = [c for c in X.columns if c not in numerical_cols]

    # ----------------------
    # PREPROCESSING PIPELINES
    # ----------------------
    num_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    cat_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", num_transformer, numerical_cols),
        ("cat", cat_transformer, categorical_cols)
    ])

    print("\n🔧 Applying preprocessing...\n")

    # ----------------------
    # TARGET ENCODING
    # ----------------------
    if y.dtype == object or y.dtype.name == "category":
        le = LabelEncoder()
        y = pd.Series(le.fit_transform(y), index=y.index)
        print(f"Target encoded → classes: {le.classes_}")
        joblib.dump(le, MODEL_DIR / "label_encoder.pkl")

    # ----------------------
    # FEATURE TRANSFORMATION
    # ----------------------
    X_processed = preprocessor.fit_transform(X)
    feature_names = [name.split("__")[-1] for name in preprocessor.get_feature_names_out()]
    X_final = pd.DataFrame(X_processed, columns=feature_names)

    # ----------------------
    # OPTIONAL SAMPLING
    # ----------------------
    if sampling == "stratified" and n_samples:
        from sklearn.utils import resample
        # ensure the target series has the expected column name
        if y.name != TARGET_COL:
            y = y.rename(TARGET_COL)

        # align indices and concat safely
        df_combined = pd.concat([X_final.reset_index(drop=True), y.reset_index(drop=True)], axis=1)
        grouped = df_combined.groupby(TARGET_COL)

        # compute per-group sample size (at least 1)
        per_group = max(1, n_samples // len(grouped))
        sampled = grouped.apply(lambda x: resample(x, n_samples=per_group, replace=True))
        sampled = sampled.droplevel(0).reset_index(drop=True)
        X_final = sampled.drop(columns=[TARGET_COL])
        y = sampled[TARGET_COL]
        print(f"Applied stratified sampling → {X_final.shape[0]} samples")

    # ----------------------
    # SAVE OUTPUTS
    # ----------------------
    X_final.to_csv(DATA_DIR / "cleaned_features.csv", index=False)
    y.to_csv(DATA_DIR / "y_target.csv", index=False, header=["TARGET"])
    joblib.dump(preprocessor, MODEL_DIR / "preprocessor.pkl")

    print(f"✅ Saved features: {X_final.shape}")
    print(f"📁 Saved to {DATA_DIR}")
    print(f"📁 Preprocessor saved to {MODEL_DIR}/preprocessor.pkl\n")


if __name__ == "__main__":
    run_preprocessing(sampling="stratified", n_samples=500)  # optional
