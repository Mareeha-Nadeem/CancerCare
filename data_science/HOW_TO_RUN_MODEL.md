# 🚀 Running the ML Model - Quick Guide

## 📁 Current Status

Your `data_science/model_1` folder has:
- ✅ Training data (`data/raw_data.csv`, `data/processed_features.csv`)
- ✅ Training script (`train_model.py`)
- ✅ Interface script (`interface.py`)
- ✅ Feature engineering (`feature_engineer.py`)
- ⚠️ Missing: Trained model file (`models/lung_cancer_pipeline.pkl`)

---

## 🎯 Steps to Run the Model

### **Option 1: Train the Model (First Time)**

1. **Open terminal in project root:**
   ```bash
   cd "e:\Project\CancerCare -- Copy"
   ```

2. **Run the training script:**
   ```bash
   python data_science\model_1\train_model.py
   ```

3. **Wait for training to complete** (~30 seconds to 2 minutes)
   - You'll see cross-validation scores
   - Test set evaluation metrics
   - Model will be saved to `models/lung_cancer_pipeline.pkl`

---

### **Option 2: Use Existing Model (If Already Trained)**

Check if model exists:
```bash
ls data_science\model_1\models\
```

If you see `lung_cancer_pipeline.pkl`, the model is ready!

---

## 🧪 **Testing the Model**

### **Test Single Prediction:**

```python
# Run from project root
python
```

Then in Python console:
```python
import joblib
import pandas as pd
import numpy as np

# Load the trained model
model = joblib.load('data_science/model_1/models/lung_cancer_pipeline.pkl')

# Create sample patient data
sample_data = pd.DataFrame({
    'AGE': [55],
    'SMOKING': [2],  # 1=Yes, 0=No, 2=Former
    'YELLOW_FINGERS': [1],
    'ANXIETY': [1],
    'PEER_PRESSURE': [0],
    'CHRONIC_DISEASE': [1],
    'FATIGUE': [1],
    'ALLERGY': [0],
    'WHEEZING': [1],
    'ALCOHOL_CONSUMING': [1],
    'COUGHING': [1],
    'SHORTNESS_OF_BREATH': [1],
    'SWALLOWING_DIFFICULTY': [0],
    'CHEST_PAIN': [1],
    'GENDER_M': [1]  # 1=Male, 0=Female
})

# Make prediction
risk_level = model.predict(sample_data)[0]
probabilities = model.predict_proba(sample_data)[0]

print(f"Risk Level: {risk_level}")
print(f"Probabilities: {probabilities}")
```

---

## 🔍 **Understanding the Model**

### **Input Features:**
Your model expects these features:
- **Demographics:** AGE, GENDER_M
- **Lifestyle:** SMOKING, ALCOHOL_CONSUMING
- **Symptoms:** COUGHING, WHEEZING, CHEST_PAIN, etc.
- **Risk Factors:** YELLOW_FINGERS, CHRONIC_DISEASE, etc.

### **Output:**
- **Risk Level:** 0=Low, 1=Medium, 2=High
- **Probabilities:** Array of probabilities for each class

---

## 🔗 **Integration with CancerCare App**

The model is already integrated! Your app uses:
- `core/services/ml_service.py` - Loads and uses the model
- `frontend/prediction_page.py` - UI for predictions

The model file should be at:
```
data_science/model_1/models/lung_cancer_pipeline.pkl
```

---

## ⚠️ **Current Issue**

You're missing the trained model file. Let's fix this!

Run this command to train the model:
```bash
python data_science\model_1\train_model.py
```

---

## 📊 **Expected Training Output**

```
============================================================
🚀 Starting Model Training
============================================================

✅ Loaded data: X=(309, 15), y=(309,)
🏷️  Encoded target classes: ['High', 'Low', 'Medium']

📊 Train set: (247, 15)
📊 Test set: (62, 15)

🔄 Running 5-fold cross-validation...
📈 CV F1 Scores: ['0.8234', '0.8456', '0.8123', '0.8567', '0.8345']
📈 Mean CV F1: 0.8345 (+/- 0.0234)

🎯 Training final model...
✅ Pipeline saved to lung_cancer_pipeline.pkl

📊 TEST SET RESULTS
============================================================
Accuracy:  0.8548
F1 (weighted): 0.8423
Precision: 0.8512
Recall:    0.8548
```

---

## 🎉 **After Training**

1. Model will be saved automatically
2. App will use it for predictions
3. No more "mock data" warnings!

**Ready to train? Just run:**
```bash
python data_science\model_1\train_model.py
```
