# import pandas as pd
# from pathlib import Path
# import joblib
# from sklearn.preprocessing import LabelEncoder, MinMaxScaler
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.pipeline import Pipeline
# from imblearn.over_sampling import SMOTE
# from sklearn.compose import ColumnTransformer
# from sklearn.base import TransformerMixin, BaseEstimator
# import numpy as np

# PROJECT_ROOT = Path(__file__).resolve().parent
# RAW_DATA_PATH = PROJECT_ROOT / "data/raw_data.csv"
# MODEL_DIR = PROJECT_ROOT / "models"
# DATA_DIR = PROJECT_ROOT / "data"
# MODEL_DIR.mkdir(exist_ok=True)
# DATA_DIR.mkdir(exist_ok=True)
# TARGET_COL = "Final_Prediction"

# DROP_COLS = [
#     "STAGE_AT_DIAGNOSIS",
#     "CANCER_TYPE",
#     "MUTATION_TYPE",
#     "TREATMENT_ACCESS",
#     "CLINICAL_TRIAL_ACCESS",
#     "LANGUAGE_BARRIER",
#     "DELAY_IN_DIAGNOSIS",
#     "MORTALITY_RISK",
#     "5_YEAR_SURVIVAL_PROBABILITY"
# ]

# def feature_engineering(df: pd.DataFrame):
#     df = df.copy()
#     df['SMOKING_RISK'] = df['SMOKING_STATUS'].map({'Smoker':2,'Former Smoker':1,'Non-Smoker':0}) + \
#                          df['SECOND_HAND_SMOKE'].map({'Yes':1,'No':0})
#     df['ENVIRONMENTAL_RISK'] = df['OCCUPATION_EXPOSURE'].map({'Yes':1,'No':0}) + \
#                                 df['AIR_POLLUTION_EXPOSURE'].map({'Low':0,'Medium':1,'High':2})
#     df['TOBACCO_EXPOSURE_RISK'] = df['INDOOR_SMOKE_EXPOSURE'].map({'Yes':1,'No':0}) + \
#                                    df['TOBACCO_MARKETING_EXPOSURE'].map({'Yes':1,'No':0})
#     df['HEALTHCARE_RISK'] = df['HEALTHCARE_ACCESS'].map({'Good':0,'Limited':1,'Poor':2})
#     df['SOCIOECONOMIC_RISK'] = df['SOCIOECONOMIC_STATUS'].map({'High':0,'Middle':1,'Low':2})
#     df['SCREENING_RISK'] = df['SCREENING_AVAILABILITY'].map({'Yes':0,'No':1})
#     df['URBAN_RURAL_RISK'] = df['RURAL_OR_URBAN'].map({'Urban':0,'Rural':1})
#     df['AGE_GROUP'] = pd.cut(df['AGE'], bins=[29,40,50,60,70,80,90], labels=False)
#     drop_cols = [
#         'SMOKING_STATUS','SECOND_HAND_SMOKE','OCCUPATION_EXPOSURE','AIR_POLLUTION_EXPOSURE',
#         'INDOOR_SMOKE_EXPOSURE','TOBACCO_MARKETING_EXPOSURE','HEALTHCARE_ACCESS',
#         'SOCIOECONOMIC_STATUS','SCREENING_AVAILABILITY','RURAL_OR_URBAN','AGE'
#     ]
#     df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)
#     return df

# class LabelEncoderWrapper(BaseEstimator, TransformerMixin):
#     """Encode multiple object columns using sklearn's LabelEncoder per column.
#     Accepts and returns a pandas DataFrame (keeps column names).
#     """
#     def __init__(self):
#         self.encoders_ = {}

#     def fit(self, X, y=None):
#         X = X.copy()
#         for col in X.columns:
#             le = LabelEncoder()
#             le.fit(X[col].astype(str).fillna("##NA##"))
#             self.encoders_[col] = le
#         return self

#     def transform(self, X):
#         X = X.copy()
#         for col, le in self.encoders_.items():
#             X[col] = le.transform(X[col].astype(str).fillna("##NA##"))
#         return X

#     def fit_transform(self, X, y=None):
#         return self.fit(X, y).transform(X)

# class CustomScalerEncoder(BaseEstimator, TransformerMixin):
#     """Encode categorical columns and scale numeric columns.
#     - categorical_cols: list of column names to LabelEncode
#     - scaler: scaler instance (MinMaxScaler/StandardScaler). Defaults to MinMaxScaler.
#     Returns a pandas DataFrame with same column order.
#     """
#     def __init__(self, categorical_cols=None, scaler=None):
#         self.categorical_cols = list(categorical_cols) if categorical_cols else []
#         self.scaler = scaler if scaler is not None else MinMaxScaler()
#         self.le_wrapper_ = None
#         self.numeric_cols_ = None

#     def fit(self, X, y=None):
#         X = X.copy()
#         # ensure columns exist
#         self.categorical_cols = [c for c in self.categorical_cols if c in X.columns]
#         # prepare label encoders for categorical columns
#         if self.categorical_cols:
#             self.le_wrapper_ = LabelEncoderWrapper()
#             self.le_wrapper_.fit(X[self.categorical_cols])
#         # numeric cols are the rest
#         self.numeric_cols_ = [c for c in X.columns if c not in self.categorical_cols]
#         if self.numeric_cols_:
#             self.scaler.fit(X[self.numeric_cols_].astype(float).fillna(0))
#         return self

#     def transform(self, X):
#         X = X.copy()
#         if self.categorical_cols and self.le_wrapper_ is not None:
#             X[self.categorical_cols] = self.le_wrapper_.transform(X[self.categorical_cols])
#         if self.numeric_cols_:
#             X[self.numeric_cols_] = self.scaler.transform(X[self.numeric_cols_].astype(float).fillna(0))
#         return X

#     def fit_transform(self, X, y=None):
#         return self.fit(X, y).transform(X)

# # ----------------------------
# # MAIN
# # ----------------------------
# def main():
#     df = pd.read_csv(RAW_DATA_PATH)
#     df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
#     target_upper = TARGET_COL.upper()
#     drop_cols_upper = [c.upper() for c in DROP_COLS]
#     df.drop(columns=[c for c in drop_cols_upper if c in df.columns], inplace=True)
#     df = df[~df[target_upper].isna()]
#     df = feature_engineering(df)

#     # Separate X/y
#     y = df[target_upper]
#     X = df.drop(columns=[target_upper])

#     # Save engineered/encoded features for prediction
#     X.to_csv(DATA_DIR / "cleaned_features.csv", index=False)
#     y.to_csv(DATA_DIR / "y_target.csv", index=False)

#     # Identify categorical columns
#     cat_cols = X.select_dtypes(include="object").columns.tolist()

#     # Preprocessing: encode categorical + scale numerical
#     preprocessor = ColumnTransformer(
#         transformers=[
#             ('cat', LabelEncoderWrapper(), cat_cols),
#         ], remainder='passthrough'
#     )

#     # Train/test split
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#     # Upsample minority with SMOTE
#     smt = SMOTE(random_state=42)
#     X_train_res, y_train_res = smt.fit_resample(X_train, y_train)

#     # Build pipeline
#     pipeline = Pipeline([
#         ('encoder_scaler', CustomScalerEncoder(cat_cols)),
#         ('model', RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42))
#     ])

#     # Train pipeline
#     pipeline.fit(X_train_res, y_train_res)

#     # Save pipeline
#     joblib.dump(pipeline, MODEL_DIR / "RF_Prediction_Pipeline.joblib")
#     print(f"✅ Pipeline trained and saved to {MODEL_DIR / 'RF_Prediction_Pipeline.joblib'}")

# if __name__ == "__main__":
#     main()

import pandas as pd
from pathlib import Path
import joblib
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_PATH = PROJECT_ROOT / "data/raw_data.csv"
MODEL_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
TARGET_COL = "Final_Prediction"

DROP_COLS = [
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

def feature_engineering(df: pd.DataFrame):
    df = df.copy()
    df['SMOKING_RISK'] = df['SMOKING_STATUS'].map({'Smoker':2,'Former Smoker':1,'Non-Smoker':0}) + \
                         df['SECOND_HAND_SMOKE'].map({'Yes':1,'No':0})
    df['ENVIRONMENTAL_RISK'] = df['OCCUPATION_EXPOSURE'].map({'Yes':1,'No':0}) + \
                                df['AIR_POLLUTION_EXPOSURE'].map({'Low':0,'Medium':1,'High':2})
    df['TOBACCO_EXPOSURE_RISK'] = df['INDOOR_SMOKE_EXPOSURE'].map({'Yes':1,'No':0}) + \
                                   df['TOBACCO_MARKETING_EXPOSURE'].map({'Yes':1,'No':0})
    df['HEALTHCARE_RISK'] = df['HEALTHCARE_ACCESS'].map({'Good':0,'Limited':1,'Poor':2})
    df['SOCIOECONOMIC_RISK'] = df['SOCIOECONOMIC_STATUS'].map({'High':0,'Middle':1,'Low':2})
    df['SCREENING_RISK'] = df['SCREENING_AVAILABILITY'].map({'Yes':0,'No':1})
    df['URBAN_RURAL_RISK'] = df['RURAL_OR_URBAN'].map({'Urban':0,'Rural':1})
    df['AGE_GROUP'] = pd.cut(df['AGE'], bins=[29,40,50,60,70,80,90], labels=False)

    drop_cols = [
        'SMOKING_STATUS','SECOND_HAND_SMOKE','OCCUPATION_EXPOSURE','AIR_POLLUTION_EXPOSURE',
        'INDOOR_SMOKE_EXPOSURE','TOBACCO_MARKETING_EXPOSURE','HEALTHCARE_ACCESS',
        'SOCIOECONOMIC_STATUS','SCREENING_AVAILABILITY','RURAL_OR_URBAN','AGE'
    ]
    df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)
    return df

class Preprocess:
    def encode(self, df: pd.DataFrame):
        df = df.copy()
        cat_cols = df.select_dtypes(include="object").columns
        for col in cat_cols:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))
        return df

    def scale(self, X: pd.DataFrame):
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        return pd.DataFrame(X_scaled, columns=X.columns)

def main():
    df = pd.read_csv(RAW_DATA_PATH)
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    target_upper = TARGET_COL.upper()
    drop_cols_upper = [c.upper() for c in DROP_COLS]
    df.drop(columns=[c for c in drop_cols_upper if c in df.columns], inplace=True)
    df = df[~df[target_upper].isna()]

    df = feature_engineering(df)

    # Separate X/y
    y = df[target_upper]
    X = df.drop(columns=[target_upper])

    # Preprocess
    prep = Preprocess()
    X_encoded = prep.encode(X)
    X_scaled = prep.scale(X_encoded)

    # Save engineered/encoded features for prediction
    X_scaled.to_csv(DATA_DIR / "cleaned_features.csv", index=False)
    y.to_csv(DATA_DIR / "y_target.csv", index=False)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    # Upsample minority with SMOTE
    smt = SMOTE(random_state=42)
    X_train_res, y_train_res = smt.fit_resample(X_train, y_train)

    # Train model
    model = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42)
    model.fit(X_train_res, y_train_res)

    # Save model
    joblib.dump(model, MODEL_DIR / "RF_Prediction_Pipeline.joblib")
    print(f"✅ Pipeline trained and saved to {MODEL_DIR / 'RF_Prediction_Pipeline.joblib'}")

if __name__ == "__main__":
    main()
