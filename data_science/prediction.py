# # prediction.py
# import pandas as pd
# import joblib
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# from pathlib import Path

# # -----------------------------
# # 1️⃣ Load dataset (preprocessed or new)
# # -----------------------------
# data_path = "../preprocessed/cancer_patient_preprocessed.csv"  # replace if new data
# df = pd.read_csv(data_path)
# print("Dataset loaded! Shape:", df.shape)

# # -----------------------------
# # 2️⃣ Split features & labels
# # -----------------------------
# label_col = "level"
# X = df.drop(columns=[label_col])
# y = df[label_col]

# # -----------------------------
# # 3️⃣ Load trained model
# # -----------------------------
# model_path = "../models/cancer_model.pkl"
# model = joblib.load(model_path)
# print("Trained model loaded!")

# # -----------------------------
# # 4️⃣ Make predictions
# # -----------------------------
# y_pred = model.predict(X)
# df['predicted_level'] = y_pred

# # -----------------------------
# # 5️⃣ Evaluate model
# # -----------------------------
# print("Accuracy:", accuracy_score(y, y_pred))
# print("\nClassification Report:\n", classification_report(y, y_pred))

# cm = confusion_matrix(y, y_pred)
# print("\nConfusion Matrix:\n", cm)

# # # -----------------------------
# # # 6️⃣ Save predictions (optional)
# # # -----------------------------
# # df.to_csv("predictions/cancer_predictions.csv", index=False)
# # print("Predictions saved at: data_science/predictions/cancer_predictions.csv")


import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from pathlib import Path

# -----------------------------
# 1️⃣ Load dataset (preprocessed)
# -----------------------------
data_path = r"D:\CancerCare\data_science\preprocessed\cancer_patient_preprocessed.csv"
try:
    df = pd.read_csv(data_path)
    print("Dataset loaded! Shape:", df.shape)
except FileNotFoundError:
    print("Error: File not found at", data_path)
    exit()

# -----------------------------
# 2️⃣ Split features & labels
# -----------------------------
label_col = "level"
X = df.drop(columns=[label_col])
y = df[label_col]

# -----------------------------
# 3️⃣ Load trained model
# -----------------------------
model_path = r"D:\CancerCare\data_science\models\cancer_model.pkl"
try:
    model = joblib.load(model_path)
    print("Trained model loaded!")
except FileNotFoundError:
    print("Error: Model file not found at", model_path)
    exit()

# -----------------------------
# 4️⃣ Make predictions
# -----------------------------
y_pred = model.predict(X)  # Use X (features only), not df
df['predicted_level'] = y_pred

print("\nPredictions added to dataframe:")
print(df.head())

# -----------------------------
# 5️⃣ Evaluate model
# -----------------------------
print("\nAccuracy:", accuracy_score(y, y_pred))
print("\nClassification Report:\n", classification_report(y, y_pred))

cm = confusion_matrix(y, y_pred)
print("\nConfusion Matrix:\n", cm)

# -----------------------------
# 6️⃣ Save predictions
# -----------------------------
pred_dir = Path(r"D:\CancerCare\data_science\predictions")
pred_dir.mkdir(parents=True, exist_ok=True)

output_path = pred_dir / "cancer_predictions.csv"
df.to_csv(output_path, index=False)
print(f"\nPredictions saved at: {output_path}")
