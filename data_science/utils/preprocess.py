
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# -------------------------------
# 0️⃣ Reproducibility
# -------------------------------
np.random.seed(42)

# -------------------------------
# 1️⃣ Load original dataset
# -------------------------------
orig_path = r'D:\CancerCare\data_science\dataset\cancer patient data sets.csv'
orig_df = pd.read_csv(orig_path)

# Clean column names
orig_df.columns = orig_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

# -------------------------------
# 2️⃣ Generate realistic noisy dataset
# -------------------------------
n_total = 5000
n_orig = orig_df.shape[0]
n_new = n_total - n_orig

features = orig_df.drop(columns=['level'])
target = orig_df['level']

new_rows = []
for _ in range(n_new):
    row = {}
    for col in features.columns:
        if features[col].dtype in ['int64', 'float64']:
            val = np.random.choice(features[col].values)
            jitter = np.random.randint(-3, 8)
            row[col] = max(0, val + jitter)
            if np.random.rand() < 0.02:
                row[col] += np.random.randint(5, 15)  # occasional outlier
        else:
            val = np.random.choice(features[col].values)
            if np.random.rand() < 0.01:
                val = val + 'a'  # tiny typo
            row[col] = val
    row['level'] = np.random.choice(['Low', 'Medium', 'High', 'Unknown']) if np.random.rand() < 0.03 else np.random.choice(target.values)
    new_rows.append(row)

new_df = pd.DataFrame(new_rows)

# Combine original + new rows, shuffle, reset index
combined_df = pd.concat([orig_df, new_df], ignore_index=True)
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
# Drop rows where target is 'Unknown'
combined_df = combined_df[combined_df['level'] != 'Unknown'].reset_index(drop=True)
# -------------------------------
# 3️⃣ Handle missing values & feature engineering
# -------------------------------
combined_df.ffill(inplace=True)  # forward-fill missing values

# Keep patient_id separate
identifiers = ['patient_id']
label_col = 'level'

# List of numeric columns
numeric_cols = [
    'age','air_pollution','alcohol_use','dust_allergy','occupational_hazards',
    'genetic_risk','chronic_lung_disease','balanced_diet','obesity','smoking',
    'passive_smoker','chest_pain','coughing_of_blood','fatigue','weight_loss',
    'shortness_of_breath','wheezing','swallowing_difficulty','clubbing_of_finger_nails',
    'frequent_cold','dry_cough','snoring'
]

# --- Feature engineering ---
# Ratios
combined_df['smoking_vs_passive'] = combined_df['smoking'] / (combined_df['passive_smoker'] + 1)
combined_df['obesity_vs_diet'] = combined_df['obesity'] / (combined_df['balanced_diet'] + 1)

# Squared features
for col in numeric_cols:
    combined_df[f'{col}_sq'] = combined_df[col] ** 2

# Interactions
combined_df['age_genetic_risk'] = combined_df['age'] * combined_df['genetic_risk']

# -------------------------------
# 4️⃣ Remove old index column & reset index
# -------------------------------
if 'index' in combined_df.columns:
    combined_df.drop(columns=['index'], inplace=True)
combined_df.reset_index(drop=True, inplace=True)

# -------------------------------
# 5️⃣ Split features for pipeline
# -------------------------------
feature_cols = [c for c in combined_df.columns if c not in identifiers + [label_col]]
numeric_cols = combined_df[feature_cols].select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = combined_df[feature_cols].select_dtypes(include=['object']).columns.tolist()

# -------------------------------
# 6️⃣ Preprocessing pipeline
# -------------------------------
pipeline = Pipeline([
    ('preprocessor', ColumnTransformer([
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ]))
])

# -------------------------------
# 7️⃣ Save preprocessed dataset
# -------------------------------
preproc_dir = Path("D:/CancerCare/data_science/preprocessed")
preproc_dir.mkdir(parents=True, exist_ok=True)
out_path = preproc_dir / "cancer_patient_preprocessed_final.csv"
combined_df.to_csv(out_path, index=False)
print("✅ Preprocessing + feature engineering done!")
print(f"Preprocessed dataset saved at: {out_path}")
