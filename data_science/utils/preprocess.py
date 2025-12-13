import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import sys

from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline

# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw_data.csv"
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

# Post-diagnosis columns to exclude (for pre-diagnosis prediction)
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
]

TARGET_COL = "FINAL_PREDICTION"


def run_preprocessing(handle_imbalance="smote", sampling_strategy="auto"):
    """
    Preprocess cancer dataset for pre-diagnosis prediction.
    
    Parameters:
    -----------
    handle_imbalance : str
        Method to handle imbalanced data: 'smote', 'undersample', 'combined', or None
    sampling_strategy : str or float
        Sampling strategy for resampling (default: 'auto')
    """
    print("\n" + "="*60)
    print("⚙️  CANCER PRE-DIAGNOSIS DATA PREPROCESSING")
    print("="*60 + "\n")

    # ----------------------
    # LOAD DATA
    # ----------------------
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"✅ Loaded data: {df.shape}")
    except FileNotFoundError:
        print(f"❌ File not found: {RAW_DATA_PATH.resolve()}")
        sys.exit(1)

    # Normalize column names
    df.columns = [col.upper().replace(" ", "_") for col in df.columns]
    print(f"📋 Columns: {list(df.columns)}\n")

    # ----------------------
    # DATA CLEANING
    # ----------------------
    # Drop duplicates
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    print(f"🧹 Removed {initial_rows - len(df)} duplicate rows")

    # Drop ID columns
    id_cols = ["PATIENT_ID", "ID", "INDEX"]
    id_cols_found = [col for col in id_cols if col in df.columns]
    if id_cols_found:
        df.drop(columns=id_cols_found, inplace=True)
        print(f"🗑️  Dropped ID columns: {id_cols_found}")

    # Drop post-diagnosis columns
    drop_cols = [c for c in EXCLUDE_COLS if c in df.columns]
    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)
        print(f"🗑️  Dropped post-diagnosis columns: {drop_cols}")

    # ----------------------
    # TARGET VALIDATION
    # ----------------------
    if TARGET_COL not in df.columns:
        print(f"\n❌ ERROR: Target column '{TARGET_COL}' not found!")
        print(f"Available columns: {list(df.columns)}")
        sys.exit(1)

    # Separate features and target
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    print(f"\n📊 Dataset Info:")
    print(f"   Features: {X.shape}")
    print(f"   Target distribution:")
    print(y.value_counts())
    print(f"   Class imbalance ratio: {y.value_counts().max() / y.value_counts().min():.2f}:1")

    # ----------------------
    # FEATURE TYPES
    # ----------------------
    numerical_cols = [c for c in X.columns if X[c].dtype in [np.int64, np.float64]]
    categorical_cols = [c for c in X.columns if c not in numerical_cols]

    print(f"\n🔢 Numerical features ({len(numerical_cols)}): {numerical_cols}")
    print(f"📝 Categorical features ({len(categorical_cols)}): {categorical_cols}")

    # ----------------------
    # PREPROCESSING PIPELINES
    # ----------------------
    num_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
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

    print("\n🔧 Applying preprocessing transformations...")

    # ----------------------
    # TARGET ENCODING
    # ----------------------
    if y.dtype == object or y.dtype.name == "category":
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        y = pd.Series(y_encoded, index=y.index, name=TARGET_COL)
        print(f"✅ Target encoded → classes: {list(le.classes_)}")
        joblib.dump(le, MODEL_DIR / "label_encoder.pkl")
        
        # Save class mapping
        class_mapping = {i: cls for i, cls in enumerate(le.classes_)}
        print(f"   Mapping: {class_mapping}")

    # ----------------------
    # FEATURE TRANSFORMATION
    # ----------------------
    X_processed = preprocessor.fit_transform(X)
    
    # Get feature names
    feature_names = []
    for name in preprocessor.get_feature_names_out():
        # Clean up feature names
        clean_name = name.split("__")[-1]
        feature_names.append(clean_name)
    
    X_final = pd.DataFrame(X_processed, columns=feature_names, index=X.index)
    print(f"✅ Features transformed: {X_final.shape}")

    # ----------------------
    # HANDLE IMBALANCED DATA
    # ----------------------
    if handle_imbalance:
        print(f"\n⚖️  Handling class imbalance using: {handle_imbalance.upper()}")
        print(f"   Before: {dict(y.value_counts())}")
        
        if handle_imbalance == "smote":
            sampler = SMOTE(sampling_strategy=sampling_strategy, random_state=42)
            X_final, y = sampler.fit_resample(X_final, y)
            
        elif handle_imbalance == "undersample":
            sampler = RandomUnderSampler(sampling_strategy=sampling_strategy, random_state=42)
            X_final, y = sampler.fit_resample(X_final, y)
            
        elif handle_imbalance == "combined":
            # First oversample minority, then undersample majority
            over = SMOTE(sampling_strategy=0.5, random_state=42)
            under = RandomUnderSampler(sampling_strategy=0.8, random_state=42)
            X_final, y = over.fit_resample(X_final, y)
            X_final, y = under.fit_resample(X_final, y)
        
        y = pd.Series(y, name=TARGET_COL)
        X_final = pd.DataFrame(X_final, columns=feature_names)
        print(f"   After: {dict(y.value_counts())}")
        print(f"✅ Balanced dataset: {X_final.shape}")

    # ----------------------
    # SAVE OUTPUTS
    # ----------------------
    X_final.to_csv(DATA_DIR / "cleaned_features.csv", index=False)
    y.to_csv(DATA_DIR / "y_target.csv", index=False, header=["TARGET"])
    joblib.dump(preprocessor, MODEL_DIR / "preprocessor.pkl")

    # Save metadata
    metadata = {
        "n_samples": len(X_final),
        "n_features": len(feature_names),
        "numerical_features": numerical_cols,
        "categorical_features": categorical_cols,
        "feature_names": feature_names,
        "target_distribution": dict(y.value_counts()),
        "imbalance_method": handle_imbalance
    }
    joblib.dump(metadata, MODEL_DIR / "preprocessing_metadata.pkl")

    print(f"\n{'='*60}")
    print("✅ PREPROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"📊 Final dataset shape: {X_final.shape}")
    print(f"📁 Features saved to: {DATA_DIR / 'cleaned_features.csv'}")
    print(f"📁 Target saved to: {DATA_DIR / 'y_target.csv'}")
    print(f"📁 Preprocessor saved to: {MODEL_DIR / 'preprocessor.pkl'}")
    print(f"📁 Metadata saved to: {MODEL_DIR / 'preprocessing_metadata.pkl'}")
    print(f"{'='*60}\n")

    return X_final, y, preprocessor


if __name__ == "__main__":
    # Run preprocessing with SMOTE to handle imbalanced data
    X, y, preprocessor = run_preprocessing(
        handle_imbalance="smote",  # Options: 'smote', 'undersample', 'combined', None
        sampling_strategy="auto"    # 'auto' balances all classes
    )