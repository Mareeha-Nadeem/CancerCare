import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)
TOP_N_FEATURES = 15

print("=" * 60)
print("FEATURE IMPORTANCE ANALYZER")
print("=" * 60)

print("\nLoading model...")
model_path = MODEL_DIR / "lung_cancer_pipeline.pkl"
pipeline = joblib.load(model_path)

if hasattr(pipeline, 'named_steps'):
    model = pipeline.named_steps['model']
else:
    model = pipeline

print("Loading feature names...")
features_path = DATA_DIR / "processed_features.csv"
if features_path.exists():
    feature_df = pd.read_csv(features_path, nrows=1)
    base_feature_names = feature_df.columns.tolist()
else:
    base_feature_names = [
        'AGE', 'GENDER', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
        'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE', 'ALLERGY',
        'WHEEZING', 'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH',
        'SWALLOWING_DIFFICULTY', 'CHEST_PAIN'
    ]

print("Extracting importance...")
try:
    importances = model.feature_importances_
    
    # Get feature names after transformation
    if hasattr(pipeline, 'named_steps') and 'feature_engineer' in pipeline.named_steps:
        # Transform base features to get actual feature names
        import pandas as pd
        sample_df = pd.DataFrame([{f: 0 for f in base_feature_names}])
        transformed = pipeline.named_steps['feature_engineer'].transform(sample_df)
        feature_names = list(transformed.columns)
    else:
        feature_names = base_feature_names
    
    # Ensure lengths match
    if len(feature_names) != len(importances):
        print(f"Warning: {len(feature_names)} feature names but {len(importances)} importances")
        feature_names = feature_names[:len(importances)] + [f'Feature_{i}' for i in range(len(feature_names), len(importances))]
    
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    })
    importance_df = importance_df.sort_values('Importance', ascending=False)
    top_features = importance_df.head(TOP_N_FEATURES)
except AttributeError:
    print("Error: Model doesn't support feature importance")
    exit(1)

print("Creating visualization...")
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Blues_r")
fig, ax = plt.subplots(figsize=(10, 8))

bars = ax.barh(range(len(top_features)), 
               top_features['Importance'].values,
               color='#1f77b4',
               edgecolor='navy',
               linewidth=1.2)

ax.set_yticks(range(len(top_features)))
ax.set_yticklabels(top_features['Feature'].values, fontsize=11)
ax.set_xlabel('Importance', fontsize=12, fontweight='bold')
ax.set_ylabel('Features', fontsize=12, fontweight='bold')
ax.set_title('Feature Importance - Lung Cancer Risk Prediction Model', 
             fontsize=14, fontweight='bold', pad=20)

for i, (idx, row) in enumerate(top_features.iterrows()):
    ax.text(row['Importance'], i, f" {row['Importance']:.3f}", 
            va='center', fontsize=9, fontweight='bold')

ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)
plt.tight_layout()

output_path = RESULTS_DIR / "feature_importance.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Saved to: {output_path}")

plt.show()

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE ANALYSIS")
print("=" * 60)

print(f"\nTop {TOP_N_FEATURES} Most Important Features:")
print("-" * 60)

for i, (idx, row) in enumerate(top_features.iterrows(), 1):
    importance_pct = row['Importance'] * 100
    print(f"{i:2d}. {row['Feature']:25s} | {row['Importance']:.4f} ({importance_pct:.2f}%)")

cumulative_importance = top_features['Importance'].cumsum()
total_importance = importance_df['Importance'].sum()

print(f"\nKey Insights:")
print("-" * 60)
print(f"  Top feature: {top_features.iloc[0]['Feature']}")
print(f"  Top feature importance: {top_features.iloc[0]['Importance']:.4f}")
print(f"  Top 5 features cover: {cumulative_importance.iloc[4]/total_importance*100:.1f}% of total")
print(f"  Top 10 features cover: {cumulative_importance.iloc[9]/total_importance*100:.1f}% of total")

csv_path = RESULTS_DIR / "feature_importance_detailed.csv"
importance_df.to_csv(csv_path, index=False)
print(f"\nDetailed results saved to: {csv_path}")

print("\nFeatures by Category:")
print("-" * 60)

categories = {
    'Lifestyle': ['SMOKING', 'ALCOHOL_CONSUMING', 'PEER_PRESSURE'],
    'Physical Symptoms': ['CHEST_PAIN', 'SHORTNESS_OF_BREATH', 'COUGHING', 
                          'WHEEZING', 'SWALLOWING_DIFFICULTY', 'YELLOW_FINGERS'],
    'Medical History': ['CHRONIC_DISEASE', 'ALLERGY'],
    'General Health': ['FATIGUE', 'ANXIETY'],
    'Demographics': ['AGE', 'GENDER']
}

category_importance = {}
for category, features in categories.items():
    cat_importance = importance_df[importance_df['Feature'].isin(features)]['Importance'].sum()
    category_importance[category] = cat_importance

for category, importance in sorted(category_importance.items(), key=lambda x: x[1], reverse=True):
    pct = importance / total_importance * 100
    print(f"  {category:20s}: {importance:.4f} ({pct:.1f}%)")

print("\nCreating category comparison chart...")
fig2, ax2 = plt.subplots(figsize=(10, 6))

categories_sorted = sorted(category_importance.items(), key=lambda x: x[1], reverse=True)
cat_names = [x[0] for x in categories_sorted]
cat_values = [x[1] for x in categories_sorted]

colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(cat_names)))
bars = ax2.bar(cat_names, cat_values, color=colors, edgecolor='navy', linewidth=1.5)

ax2.set_xlabel('Feature Category', fontsize=12, fontweight='bold')
ax2.set_ylabel('Total Importance', fontsize=12, fontweight='bold')
ax2.set_title('Feature Importance by Category', fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()

category_output = RESULTS_DIR / "feature_importance_by_category.png"
plt.savefig(category_output, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Category chart saved to: {category_output}")

plt.show()

print("\n" + "=" * 60)
print("COMPLETE")
print("=" * 60)
