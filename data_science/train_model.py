import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from pathlib import Path

# Load PREPROCESSED dataset (already scaled + encoded)
df = pd.read_csv(r"D:\CancerCare\data_science\preprocessed\cancer_patient_preprocessed.csv")
print("Preprocessed dataset loaded! Shape:", df.shape)

# Split features & labels
label_col = 'level'
X = df.drop(columns=[label_col])
y = df[label_col]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Train size:", X_train.shape, "Test size:", X_test.shape)

# Define models (NO preprocessing needed - data already preprocessed)
models = {
    "RandomForest": RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42
    ),
    "DecisionTree": DecisionTreeClassifier(
        max_depth=6,
        class_weight="balanced",
        random_state=42
    ),
    "LogisticRegression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    ),
    "GradientBoosting": GradientBoostingClassifier(
        n_estimators=100,
        random_state=42
    )
}

# Train + Evaluate
results = {}
for name, model in models.items():
    print(f"\n==============================")
    print(f" Training {name}")
    print(f"==============================")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    try:
        probs = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, probs)
    except:
        auc = "N/A"

    print(f"Model: {name}")
    print("Accuracy:", acc)
    print("ROC AUC:", auc)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    results[name] = {
        "model": model,
        "accuracy": acc,
        "auc": auc
    }

# Pick best
best_model_name = max(results, key=lambda x: results[x]["accuracy"])
best_model = results[best_model_name]["model"]

print("\n=====================================")
print(" BEST MODEL SELECTED:", best_model_name)
print(" Accuracy:", results[best_model_name]["accuracy"])
print("=====================================")

# Save best model
out_dir = Path(r"D:\CancerCare\data_science\models")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / f"{best_model_name}_model.pkl"
joblib.dump(best_model, out_file)
print(f"Model saved at: {out_file}")
