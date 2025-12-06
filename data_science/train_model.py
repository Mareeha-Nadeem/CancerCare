# import pandas as pd
# import numpy as np
# import joblib
# from pathlib import Path
# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score, classification_report, roc_auc_score
# from imblearn.over_sampling import SMOTE

# # -------------------------------
# # 1️⃣ Load preprocessed dataset with feature engineering
# # -------------------------------
# df = pd.read_csv(r"D:\CancerCare\data_science\preprocessed\cancer_patient_preprocessed_final.csv")
# print("Dataset loaded! Shape:", df.shape)

# # Drop identifiers and old index
# for col in ['patient_id', 'index']:
#     if col in df.columns:
#         df.drop(columns=[col], inplace=True)

# # -------------------------------
# # 2️⃣ Split features & target
# # -------------------------------
# label_col = 'level'
# X = df.drop(columns=[label_col])
# y = df[label_col]

# # -------------------------------
# # 3️⃣ Train-test split (stratified)
# # -------------------------------
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, stratify=y, random_state=42
# )
# print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

# # -------------------------------
# # 4️⃣ Handle class imbalance with SMOTE
# # -------------------------------
# smote = SMOTE(random_state=42)
# X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
# print("After SMOTE, class distribution:\n", pd.Series(y_train_res).value_counts())

# # -------------------------------
# # 5️⃣ Identify numeric & categorical features
# # -------------------------------
# numeric_cols = X_train_res.select_dtypes(include=['int64', 'float64']).columns.tolist()
# categorical_cols = X_train_res.select_dtypes(include=['object']).columns.tolist()

# preprocessor = ColumnTransformer([
#     ('num', StandardScaler(), numeric_cols),
#     ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
# ])

# # -------------------------------
# # 6️⃣ Define base models
# # -------------------------------
# rf = RandomForestClassifier(n_estimators=300, max_depth=None, class_weight='balanced', random_state=42)
# gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, random_state=42)
# lr = LogisticRegression(max_iter=2000, class_weight='balanced', random_state=42)

# # -------------------------------
# # 7️⃣ Stacking ensemble
# # -------------------------------
# stack = StackingClassifier(
#     estimators=[('rf', rf), ('gb', gb), ('lr', lr)],
#     final_estimator=RandomForestClassifier(n_estimators=200, random_state=42),
#     cv=5,
#     n_jobs=-1,
#     passthrough=True
# )

# # -------------------------------
# # 8️⃣ Full pipeline
# # -------------------------------
# pipeline = Pipeline([
#     ('preprocessor', preprocessor),
#     ('classifier', stack)
# ])

# # -------------------------------
# # 9️⃣ Cross-validation for F1-macro
# # -------------------------------
# cv_scores = cross_val_score(pipeline, X_train_res, y_train_res, cv=5, scoring='f1_macro', n_jobs=-1)
# print(f"CV F1-macro scores: {cv_scores}")
# print(f"Mean CV F1-macro: {cv_scores.mean():.4f}")

# # -------------------------------
# # 🔟 Train pipeline
# # -------------------------------
# pipeline.fit(X_train_res, y_train_res)

# # -------------------------------
# # 1️⃣1️⃣ Evaluate on test set
# # -------------------------------
# y_pred = pipeline.predict(X_test)
# y_prob = pipeline.predict_proba(X_test)

# acc = accuracy_score(y_test, y_pred)
# f1_macro = f1_score(y_test, y_pred, average='macro')
# bal_acc = balanced_accuracy_score(y_test, y_pred)
# try:
#     roc_auc = roc_auc_score(pd.get_dummies(y_test), y_prob, average='macro', multi_class='ovr')
# except:
#     roc_auc = "N/A"

# print("\nModel Evaluation:")
# print(f"Accuracy: {acc:.4f} | F1-macro: {f1_macro:.4f} | Balanced Acc: {bal_acc:.4f} | ROC AUC: {roc_auc}")
# print("\nClassification Report:\n", classification_report(y_test, y_pred))

# # -------------------------------
# # 1️⃣2️⃣ Save pipeline (preprocessing + model)
# # -------------------------------
# out_dir = Path(r"D:\CancerCare\data_science\models")
# out_dir.mkdir(parents=True, exist_ok=True)
# out_file = out_dir / "Stacked_Model_pipeline.pkl"
# joblib.dump(pipeline, out_file)
# print(f"Best pipeline saved at: {out_file}")


import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score, classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
from pathlib import Path

# -------------------------------
# 1️⃣ Load preprocessed dataset
# -------------------------------
BASE_DIR = Path(__file__).parent.parent  # assumes script in scripts/
DATA_FILE = BASE_DIR / "data_science/preprocessed/cancer_patient_preprocessed_final.csv"

df = pd.read_csv(DATA_FILE)
print("Dataset loaded! Shape:", df.shape)

# Drop identifiers
for col in ['patient_id', 'index']:
    if col in df.columns:
        df.drop(columns=[col], inplace=True)

# -------------------------------
# 2️⃣ Split features & target
# -------------------------------
label_col = 'level'
X = df.drop(columns=[label_col])
y = df[label_col]

# -------------------------------
# 3️⃣ Train-test split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

# -------------------------------
# 4️⃣ SMOTE for balancing
# -------------------------------
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
print("After SMOTE, class distribution:\n", pd.Series(y_train_res).value_counts())

# -------------------------------
# 5️⃣ Identify numeric & categorical features
# -------------------------------
numeric_cols = X_train_res.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X_train_res.select_dtypes(include=['object']).columns.tolist()

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
])

# -------------------------------
# 6️⃣ Base models with tuned params
# -------------------------------
rf = RandomForestClassifier(class_weight='balanced', random_state=42)
gb = GradientBoostingClassifier(random_state=42)
lr = LogisticRegression(max_iter=3000, class_weight='balanced', random_state=42)

# -------------------------------
# 7️⃣ Hyperparameter grid for tuning
# -------------------------------
rf_params = {
    'n_estimators': [200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
}
gb_params = {
    'n_estimators': [200, 300],
    'learning_rate': [0.05, 0.1],
    'max_depth': [3, 5],
}

# GridSearchCV for RandomForest
rf_grid = GridSearchCV(rf, rf_params, scoring='f1_macro', cv=5, n_jobs=-1)
rf_grid.fit(preprocessor.fit_transform(X_train_res), y_train_res)
print("Best RF params:", rf_grid.best_params_)

# GridSearchCV for GradientBoosting
gb_grid = GridSearchCV(gb, gb_params, scoring='f1_macro', cv=5, n_jobs=-1)
gb_grid.fit(preprocessor.fit_transform(X_train_res), y_train_res)
print("Best GB params:", gb_grid.best_params_)

# -------------------------------
# 8️⃣ Stacking ensemble with tuned models
# -------------------------------
stack = StackingClassifier(
    estimators=[('rf', rf_grid.best_estimator_), ('gb', gb_grid.best_estimator_), ('lr', lr)],
    final_estimator=RandomForestClassifier(n_estimators=200, random_state=42),
    cv=5,
    n_jobs=-1,
    passthrough=True
)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', stack)
])

# -------------------------------
# 9️⃣ Train final pipeline
# -------------------------------
pipeline.fit(X_train_res, y_train_res)

# -------------------------------
# 🔟 Evaluate
# -------------------------------
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)

acc = accuracy_score(y_test, y_pred)
f1_macro = f1_score(y_test, y_pred, average='macro')
bal_acc = balanced_accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(pd.get_dummies(y_test), y_prob, average='macro', multi_class='ovr')

print("\nModel Evaluation:")
print(f"Accuracy: {acc:.4f} | F1-macro: {f1_macro:.4f} | Balanced Acc: {bal_acc:.4f} | ROC AUC: {roc_auc}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -------------------------------
# 1️⃣1️⃣ Save pipeline
# -------------------------------
out_dir = Path(r"D:\CancerCare\data_science\models")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "Stacked_Model_pipeline_tuned.pkl"
joblib.dump(pipeline, out_file)
print(f"Best tuned pipeline saved at: {out_file}")
