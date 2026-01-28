import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import joblib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("CONFUSION MATRIX GENERATOR")
print("=" * 60)

# Load model
print("\nLoading model...")
model_path = MODEL_DIR / "lung_cancer_pipeline.pkl"
pipeline = joblib.load(model_path)

# Load encoder
encoder_path = MODEL_DIR / "target_encoder.pkl"
if encoder_path.exists():
    target_encoder = joblib.load(encoder_path)
    class_names = target_encoder.classes_.tolist()
else:
    class_names = ['Low', 'Medium', 'High']
    target_encoder = None

print(f"Class labels: {class_names}")

# Load test data
print("Loading test data...")
test_results_path = RESULTS_DIR / "test_predictions.csv"
if test_results_path.exists():
    test_df = pd.read_csv(test_results_path)
    y_true = test_df['TRUE_LABEL'].values
    y_pred = test_df['PREDICTED_LABEL'].values
else:
    X = pd.read_csv(DATA_DIR / "processed_features.csv")
    y = pd.read_csv(DATA_DIR / "target.csv").iloc[:, 0]
    
    if target_encoder and y.dtype == 'object':
        y_true = target_encoder.transform(y)
    else:
        y_true = y.values
    
    y_pred = pipeline.predict(X)

print(f"Loaded {len(y_true)} samples")

# Generate confusion matrix
cm = confusion_matrix(y_true, y_pred)
print(f"Confusion matrix shape: {cm.shape}")

# Visualize
print("Creating visualization...")
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True, square=True,
            linewidths=2, linecolor='white', ax=ax, cbar_kws={'label': 'Count'},
            annot_kws={'size': 14, 'weight': 'bold'})

ax.set_xlabel('Predicted Label', fontsize=14, fontweight='bold', labelpad=10)
ax.set_ylabel('True Label', fontsize=14, fontweight='bold', labelpad=10)
ax.set_title('Confusion Matrix - Lung Cancer Risk Prediction Model', 
             fontsize=16, fontweight='bold', pad=20)

ax.set_xticklabels(class_names, fontsize=12, rotation=0)
ax.set_yticklabels(class_names, fontsize=12, rotation=0)

plt.tight_layout()

output_path = RESULTS_DIR / "confusion_matrix.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Saved to: {output_path}")

plt.show()

# Calculate metrics
print("\n" + "=" * 60)
print("MODEL PERFORMANCE METRICS")
print("=" * 60)

accuracy = accuracy_score(y_true, y_pred)
print(f"\nOverall Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print("-" * 60)
target_names = class_names if target_encoder else [str(c) for c in class_names]
print(classification_report(y_true, y_pred, target_names=target_names))

print("\nConfusion Matrix Values:")
print("-" * 60)
cm_df = pd.DataFrame(cm, index=[f'True {c}' for c in class_names],
                     columns=[f'Pred {c}' for c in class_names])
print(cm_df)

print("\nPer-Class Accuracy:")
print("-" * 60)
for i, class_name in enumerate(class_names):
    class_accuracy = cm[i, i] / cm[i, :].sum()
    print(f"  {class_name}: {class_accuracy:.2%} ({cm[i, i]}/{cm[i, :].sum()})")

print("\nKey Insights:")
print("-" * 60)

max_error = 0
max_error_pair = None
for i in range(len(class_names)):
    for j in range(len(class_names)):
        if i != j and cm[i, j] > max_error:
            max_error = cm[i, j]
            max_error_pair = (class_names[i], class_names[j])

if max_error_pair:
    print(f"  Most common confusion: {max_error_pair[0]} -> {max_error_pair[1]} ({max_error} cases)")

total_correct = np.trace(cm)
total_incorrect = cm.sum() - total_correct
print(f"  Correct: {total_correct} | Incorrect: {total_incorrect}")

print("\n" + "=" * 60)
print("COMPLETE")
print("=" * 60)

