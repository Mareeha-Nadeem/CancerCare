
# import pandas as pd
# import numpy as np
# from pathlib import Path
# from sklearn.impute import SimpleImputer

# # -------------------------------
# # 0️⃣ Reproducibility
# # -------------------------------
# np.random.seed(42)

# # -------------------------------
# # 1️⃣ Load original dataset
# # -------------------------------
# project_root = Path(__file__).parent.parent
# csv_file = project_root / "data/raw_data.csv"
# orig_df = pd.read_csv(csv_file)

# # Clean column names
# orig_df.columns = (
#     orig_df.columns.str.strip()
#     .str.lower()
#     .str.replace(' ', '_')
#     .str.replace('-', '_')
# )

# # -------------------------------
# # 2️⃣ Generate realistic noisy dataset
# # -------------------------------
# n_total = 5000
# n_orig = orig_df.shape[0]
# n_new = n_total - n_orig

# features = orig_df.drop(columns=['level'])
# target = orig_df['level']

# new_rows = []
# for _ in range(n_new):
#     row = {}
#     for col in features.columns:
#         if features[col].dtype in ['int64', 'float64']:
#             val = np.random.choice(features[col].values)
#             jitter = np.random.randint(-1,3)
#             row[col] = max(0, val + jitter)

#             # if np.random.rand() < 0.02:
#             #     row[col] += np.random.randint(5, 15)  # rare outlier

#         else:  
#             val = np.random.choice(features[col].values)
#             if np.random.rand() < 0.01:
#                 val = val + 'a'
#             row[col] = val

#     # row['level'] = (
#     #     np.random.choice(['Low','Medium','High','Unknown'])
#     #     if np.random.rand() < 0.03 else np.random.choice(target.values)
#     # )
# #     new_rows.append(row)

# # new_df = pd.DataFrame(new_rows)

# # Combine everything
# combined_df = pd.concat([orig_df, new_df], ignore_index=True)
# combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# # Remove Unknown
# combined_df = combined_df[combined_df['level'] != 'Unknown'].reset_index(drop=True)

# # -------------------------------------------------
# # SAVE 5000-row RAW dataset BEFORE any processing
# # -------------------------------------------------
# raw_augmented_path = project_root / "data/raw_data5000.csv"
# combined_df.to_csv(raw_augmented_path, index=False)
# print(f"Raw 5000-row dataset saved at: {raw_augmented_path}")

# # -------------------------------
# # 3️⃣ Missing values (UPGRADED)
# # -------------------------------
# numeric_cols = combined_df.select_dtypes(include=['int64','float64']).columns
# categorical_cols = combined_df.select_dtypes(include=['object']).columns

# num_imputer = SimpleImputer(strategy='median')
# cat_imputer = SimpleImputer(strategy='most_frequent')

# combined_df[numeric_cols] = num_imputer.fit_transform(combined_df[numeric_cols])
# combined_df[categorical_cols] = cat_imputer.fit_transform(combined_df[categorical_cols])

# # -------------------------------
# # 4️⃣ Outlier Clamping
# # -------------------------------
# for col in numeric_cols:
#     combined_df[col] = np.clip(combined_df[col], 0, 100)

# # -------------------------------
# # 5️⃣ Feature Engineering
# # -------------------------------
# combined_df['smoking_vs_passive'] = combined_df['smoking'] / (combined_df['passive_smoker'] + 1)
# combined_df['obesity_vs_diet'] = combined_df['obesity'] / (combined_df['balanced_diet'] + 1)

# # for col in numeric_cols:
# #     combined_df[f"{col}_sq"] = combined_df[col] ** 2

# combined_df['age_genetic_risk'] = combined_df['age'] * combined_df['genetic_risk']

# # -------------------------------
# # 6️⃣ Drop patient_id (requested)
# # -------------------------------
# if 'patient_id' in combined_df.columns:
#     combined_df.drop(columns=['patient_id'], inplace=True)

# # -------------------------------
# # 7️⃣ Save Final Cleaned Dataset
# # -------------------------------
# out_path = project_root / "data/cleaned_data.csv"
# combined_df.to_csv(out_path, index=False)

# print("✅ Preprocessing + feature engineering done!")
# print(f"Preprocessed dataset saved at: {out_path}")
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from pathlib import Path

# --- 1. Load Data ---
project_root = Path(__file__).parent.parent
csv_file = project_root / "data/raw_data.csv"

df = pd.read_csv(csv_file)
print(f"Initial Shape: {df.shape}")

# --- 2. Remove Duplicate Rows ---
initial_rows = df.shape[0]
df.drop_duplicates(inplace=True)
print(f"Removed {initial_rows - df.shape[0]} duplicate rows.")

# --- 3. Define Column Groups ---

numerical_cols = ['Age']

categorical_cols = [
    'Country', 'Gender', 'Smoking_Status', 'Second_Hand_Smoke', 
    'Air_Pollution_Exposure', 'Occupation_Exposure', 'Rural_or_Urban', 
    'Socioeconomic_Status', 'Healthcare_Access', 'Insurance_Coverage', 
    'Screening_Availability', 'Stage_at_Diagnosis', 'Cancer_Type', 
    'Mutation_Type', 'Treatment_Access', 'Clinical_Trial_Access', 
    'Language_Barrier', 'Delay_in_Diagnosis', 'Family_History', 
    'Indoor_Smoke_Exposure', 'Tobacco_Marketing_Exposure'
]

target_cols = [
    'Final_Prediction', 
    'Mortality_Risk', 
    '5_Year_Survival_Probability'
]

# Drop targets from X
X = df.drop(columns=target_cols, errors='ignore')

# --- 4. Preprocessing Pipelines ---

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ],
    remainder='drop'
)

print("Preprocessing pipeline created successfully.")

# --- 5. Fit + Transform ---
print("\n--- Applying Preprocessor ---")
X_processed = preprocessor.fit_transform(X)

# Target Separation
Y_clf = df['Final_Prediction']
Y_reg = df['Mortality_Risk']

# --- 6. Build Final Feature Names ---
feature_names_out = (
    numerical_cols +
    list(preprocessor.named_transformers_['cat']
         ['onehot'].get_feature_names_out(categorical_cols))
)

# Create final clean DataFrame
X_final = pd.DataFrame(X_processed, columns=feature_names_out)

# --- 7. Save Clean Data ---
X_final.to_csv("cleaned_features.csv", index=False)
Y_clf.to_csv("y_classification.csv", index=False)
Y_reg.to_csv("y_regression.csv", index=False)

print("\nPreprocessing Complete!")
print(f"Final Preprocessed Feature Shape: {X_final.shape}")
print("Sample:")
print(X_final.head())
