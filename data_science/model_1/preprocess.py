
# preprocess.py
# preprocessing_train.py
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "model_1/data/raw_data.csv"
DATA_DIR = PROJECT_ROOT / "model_1/data"
MODEL_DIR = PROJECT_ROOT / "model_1/models"

# DATA_DIR.mkdir(exist_ok=True)
# MODEL_DIR.mkdir(exist_ok=True)

TARGET_COL = "Level"
COLS_TO_DROP = ["index", "Patient Id"]

def run_preprocessing(debug=True):
    # ----------------------
    # LOAD DATA
    # ----------------------
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        if debug:
            print(f"✅ Loaded data: {df.shape}")
            print(f"Columns: {list(df.columns)}")
    except FileNotFoundError:
        print(f"❌ File not found: {RAW_DATA_PATH}")
        sys.exit(1)

    # Normalize column names
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    if debug:
        print(f"📋 Columns after normalization: {list(df.columns)}")

    # Drop non-feature columns
    # cols_to_drop_upper = [c.upper() for c in COLS_TO_DROP if c.upper() in df.columns]
    # df = df.drop(columns=cols_to_drop_upper, errors='ignore')
    # if debug:
    #     print(f"🗑️ Dropped columns: {cols_to_drop_upper}")
    #     print(f"Shape after drop: {df.shape}")

    # Drop non-feature columns
# Normalize drop list to uppercase and underscores
    cols_to_drop_upper = [c.strip().upper().replace(" ", "_") for c in COLS_TO_DROP]

# Keep only those actually in the dataframe
    cols_found = [c for c in cols_to_drop_upper if c in df.columns]

    df = df.drop(columns=cols_found, errors='ignore')

    if debug:
        print(f"🗑️ Dropped columns: {cols_found}")
        print(f"Shape after drop: {df.shape}")


    # Remove duplicates
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    if debug:
        print(f"🧹 Removed {initial_rows - len(df)} duplicates")

    # Fill missing values
    missing_before = df.isnull().sum().sum()
    df = df.fillna(df.median(numeric_only=True))
    missing_after = df.isnull().sum().sum()
    if debug:
        print(f"⚠️ Missing before: {missing_before}, after: {missing_after}")

    # Separate features and target
    target_upper = TARGET_COL.upper()
    if target_upper not in df.columns:
        print(f"❌ Target column '{target_upper}' not found!")
        sys.exit(1)
    
    y = df[target_upper]
    X = df.drop(columns=[target_upper])
    
    if debug:
        print(f"📊 Features shape: {X.shape}")
        print(f"Target distribution:\n{y.value_counts()}")

    # Save processed data
    X.to_csv(DATA_DIR / "processed_features.csv", index=False)
    y.to_csv(DATA_DIR / "target.csv", index=False)
    
    if debug:
        print(f"💾 Saved processed_features.csv and target.csv in {DATA_DIR}")
    
    return X, y

if __name__ == "__main__":
    X, y = run_preprocessing()
