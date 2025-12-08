
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score, classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE

# -----------------------------------
# 1️⃣ LOAD PREPROCESSED DATA
# -----------------------------------

X_final = pd.read_csv("cleaned_features.csv")
Y_clf = pd.read_csv("y_classification.csv")

# Flatten y if DataFrame
if isinstance(Y_clf, pd.DataFrame):
    Y_clf = Y_clf.iloc[:, 0]

print("Loaded cleaned features:", X_final.shape)
print("Loaded labels:", Y_clf.shape)

X = X_final
y = Y_clf

# -----------------------------------
# 2️⃣ TRAIN-TEST SPLIT
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f"\nTrain size: {X_train.shape}, Test size: {X_test.shape}")

# -----------------------------------
# 3️⃣ SMOTE BALANCING
# -----------------------------------

smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
print("\nAfter SMOTE:\n", pd.Series(y_train_res).value_counts())

# -----------------------------------
# 4️⃣ DETECT FINAL NUMERIC + CATEGORICAL COLUMNS
#     (already encoded — so numeric only!)
# -----------------------------------

numeric_cols = X_train_res.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = []  # because your preprocessing already encoded everything

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols)
    ],
    remainder='drop'
)

# -----------------------------------
# 5️⃣ BASE MODELS
# -----------------------------------

rf = RandomForestClassifier(class_weight='balanced', random_state=42)
gb = GradientBoostingClassifier(random_state=42)
lr = LogisticRegression(max_iter=3000, class_weight='balanced', random_state=42)

# -----------------------------------
# 6️⃣ HYPERPARAM TUNING
# -----------------------------------

rf_params = {
    'n_estimators': [200, 300],
    'max_depth': [10, 20],
    'min_samples_split': [2, 5]
}

gb_params = {
    'n_estimators': [200, 300],
    'learning_rate': [0.05, 0.1],
    'max_depth': [3, 5]
}

# fit-transform train
X_train_processed = preprocessor.fit_transform(X_train_res)

print("\nTuning RF...")
rf_grid = GridSearchCV(rf, rf_params, scoring='f1_macro', cv=5, n_jobs=-1)
rf_grid.fit(X_train_processed, y_train_res)
print("Best RF:", rf_grid.best_params_)

print("\nTuning GB...")
gb_grid = GridSearchCV(gb, gb_params, scoring='f1_macro', cv=5, n_jobs=-1)
gb_grid.fit(X_train_processed, y_train_res)
print("Best GB:", gb_grid.best_params_)

# -----------------------------------
# 7️⃣ STACKING ENSEMBLE
# -----------------------------------

stack = StackingClassifier(
    estimators=[
        ('rf', rf_grid.best_estimator_),
        ('gb', gb_grid.best_estimator_),
        ('lr', lr)
    ],
    final_estimator=RandomForestClassifier(n_estimators=200, random_state=42),
    cv=5,
    n_jobs=-1,
    passthrough=True
)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', stack)
])

# -----------------------------------
# 8️⃣ TRAIN FINAL MODEL
# -----------------------------------

print("\nTraining final model...")
pipeline.fit(X_train_res, y_train_res)
print("Training done!")

# -----------------------------------
# 9️⃣ EVALUATION
# -----------------------------------

y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)

acc = accuracy_score(y_test, y_pred)
f1_macro = f1_score(y_test, y_pred, average='macro')
bal_acc = balanced_accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(pd.get_dummies(y_test), y_prob, average='macro', multi_class='ovr')

print("\n--- RESULTS ---")
print(f"Accuracy: {acc:.4f}")
print(f"F1-macro: {f1_macro:.4f}")
print(f"Balanced Acc: {bal_acc:.4f}")
print(f"ROC AUC: {roc_auc:.4f}")

print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -----------------------------------
# 🔟 SAVE MODEL
# -----------------------------------

out_dir = Path("models")
out_dir.mkdir(exist_ok=True)

out_file = out_dir / "Stacked_Classifier_Early_Detection.pkl"
joblib.dump(pipeline, out_file)

print(f"\nSaved model at: {out_file}")
