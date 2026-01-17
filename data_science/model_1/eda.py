import joblib
import pandas as pd
from pathlib import Path

# Path to the trained pipeline
MODEL_PATH = Path(__file__).resolve().parent / "models" / "lung_cancer_pipeline.pkl"
# Path to processed features (optional, for feature names)
FEATURES_PATH = Path(__file__).resolve().parent / "data" / "processed_features.csv"

# Load the trained model pipeline
pipeline = joblib.load(MODEL_PATH)

# Get feature names after transformation
if FEATURES_PATH.exists():
    X = pd.read_csv(FEATURES_PATH)
    try:
        # Try to get feature names after transformation
        if hasattr(pipeline, "named_steps") and "feature_engineer" in pipeline.named_steps:
            X_trans = pipeline.named_steps["feature_engineer"].transform(X)
            if hasattr(X_trans, "columns"):
                feature_names = X_trans.columns.tolist()
            else:
                feature_names = [f"f{i}" for i in range(X_trans.shape[1])]
        else:
            feature_names = X.columns.tolist()
    except Exception:
        feature_names = X.columns.tolist()
else:
    feature_names = None

# Extract feature importances (works for tree-based models)
try:
    if hasattr(pipeline, "named_steps"):
        model = pipeline.named_steps.get("model", pipeline)
    else:
        model = pipeline
    importances = model.feature_importances_
    if feature_names and len(feature_names) == len(importances):
        feat_imp = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
    else:
        feat_imp = pd.DataFrame({
            'feature': range(len(importances)),
            'importance': importances
        }).sort_values('importance', ascending=False)
    print("Top 15 Most Important Features:")
    print(feat_imp.head(15).to_string(index=False))
    feat_imp.to_csv(Path(__file__).resolve().parent / "results" / "feature_importance.csv", index=False)
    print("Full feature importance saved to results/feature_importance.csv")
except Exception as e:
    print(f"Could not extract feature importance: {e}")
