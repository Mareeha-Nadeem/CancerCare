# Lung Cancer Risk Prediction System

A complete machine learning pipeline for predicting lung cancer risk based on pre-diagnosis factors including smoking history, environmental exposure, genetics, and symptoms.

## 📁 Project Structure

```
lung-cancer-prediction/
├── data/
│   ├── cancer patient data sets.csv    # Original dataset
│   ├── processed_features.csv          # Engineered features
│   ├── target.csv                       # Target variable
│   └── test_set.csv                     # Hold-out test set
├── models/
│   ├── lung_cancer_model.joblib         # Trained model
│   ├── feature_engineer.pkl             # Feature engineering pipeline
│   ├── target_encoder.pkl               # Target label encoder
│   └── model_metadata.json              # Model information
├── results/
│   ├── feature_importance.csv           # Feature rankings
│   ├── training_results_*.json          # Training metrics
│   └── test_results_*.json              # Testing metrics
├── predictions/
│   └── predictions_*.csv                # Saved predictions
├── preprocessing.py                     # Data preprocessing
├── train_model.py                       # Model training
├── test_model.py                        # Model testing
└── predict.py                           # Make predictions
```

## 🚀 Quick Start

### 1. Installation

```bash
pip install pandas numpy scikit-learn imbalanced-learn joblib
```

### 2. Download Dataset

Download the dataset from Kaggle:
https://www.kaggle.com/datasets/thedevastator/cancer-patients-and-air-pollution-a-new-link

Place `cancer patient data sets.csv` in the `data/` folder.

### 3. Run the Pipeline

```bash
# Step 1: Preprocess data
python preprocessing.py

# Step 2: Train model
python train_model.py

# Step 3: Test model
python test_model.py

# Step 4: Make predictions
python predict.py --interactive
```

## 📊 Dataset Features

### Risk Factors (23 features):
- **Demographics:** Age, Gender
- **Environmental:** Air Pollution, Dust Allergy, Occupational Hazards
- **Lifestyle:** Smoking, Passive Smoker, Alcohol use, Balanced Diet, Obesity
- **Medical:** Genetic Risk, Chronic Lung Disease
- **Symptoms:** Chest Pain, Coughing of Blood, Fatigue, Weight Loss, Shortness of Breath, Wheezing, Swallowing Difficulty, Clubbing of Finger Nails, Snoring

### Target Variable:
- **Level:** Low, Medium, High (lung cancer risk)

## 🔧 What Each Script Does

### `preprocessing.py`

**Purpose:** Transform raw data into ML-ready features

**Features Created:**
- **Composite Risk Scores:**
  - Smoking Risk (smoking + passive smoking)
  - Environmental Risk (pollution + dust + occupational)
  - Lifestyle Risk (alcohol + obesity - balanced diet)
  - Hereditary Risk (genetic + chronic disease)
  - Symptom Severity (average of all symptoms)
  
- **Total Risk Score:** Weighted combination (30% smoking, 20% environmental, etc.)

- **Age Features:**
  - Age Risk (exponential scale)
  - Age Groups (5 categories)

- **Interaction Features:**
  - Smoking × Age
  - Environmental × Smoking
  - Genetic × Age

**Output:**
- `processed_features.csv` - Engineered features
- `target.csv` - Target labels
- `feature_engineer.pkl` - Fitted transformer

**Usage:**
```bash
python preprocessing.py
```

---

### `train_model.py`

**Purpose:** Train and evaluate the prediction model

**Model:** Random Forest Classifier (200 trees)

**Techniques:**
- ✅ Feature engineering
- ✅ Standard scaling
- ✅ SMOTE for class balancing (if imbalanced)
- ✅ 5-fold cross-validation
- ✅ Class weighting
- ✅ Feature importance analysis

**Output:**
- `lung_cancer_model.joblib` - Complete trained pipeline
- `model_metadata.json` - Performance metrics
- `feature_importance.csv` - Feature rankings
- `test_set.csv` - Held-out test data

**Expected Performance:**
- **Accuracy:** 85-95%
- **F1-Score:** 0.80-0.92
- **ROC-AUC:** 0.90-0.98

**Usage:**
```bash
python train_model.py
```

---

### `test_model.py`

**Purpose:** Evaluate model on test set or new data

**Metrics:**
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC, Matthews Correlation Coefficient
- Confusion Matrix
- Per-class accuracy

**Output:**
- `test_results_*.json` - Detailed metrics
- `predictions_*.csv` - Test predictions with probabilities

**Usage:**
```bash
# Test on saved test set
python test_model.py

# Or test on custom data (in Python)
from test_model import test_model
results = test_model("path/to/custom_data.csv")
```

---

### `predict.py`

**Purpose:** Make predictions for new patients

**Two Modes:**

#### 1. Interactive Mode (Single Patient)
```bash
python predict.py --interactive
```

Prompts for patient information and provides immediate risk assessment.

#### 2. Batch Mode (Multiple Patients)
```bash
python predict.py data/new_patients.csv
```

Processes CSV file and saves predictions.

**Output:**
- Risk level (Low/Medium/High)
- Confidence score
- Probability for each risk level
- Saved to `predictions/` folder

---

## 📈 Feature Importance

Top predictive features (typical results):

1. **Smoking Risk** (30% importance) - Most critical factor
2. **Age Risk** (18% importance) - Increases with age
3. **Symptom Severity** (12% importance) - Combined symptoms
4. **Total Risk Score** (10% importance) - Overall assessment
5. **Genetic Risk** (8% importance) - Family history
6. **Environmental Risk** (7% importance) - Pollution exposure
7. **Smoking × Age Interaction** (6% importance) - Compound effect
8. **Chronic Lung Disease** (5% importance) - Pre-existing condition
9. **Lifestyle Risk** (4% importance) - Diet and habits
10. Other features...

## 🎯 Model Performance Interpretation

### Confusion Matrix Example:
```
                Low    Medium    High
Low             450      12       3
Medium           15     380      22
High              2      18     425
```

### What to Look For:

✅ **Good Model:**
- Accuracy > 85%
- F1-Score > 0.80
- ROC-AUC > 0.90
- Low misclassification between Low ↔ High

⚠️ **Needs Improvement:**
- Accuracy < 75%
- Frequent Low ↔ High misclassifications
- Low confidence scores

## 💡 Usage Examples

### Example 1: Single Patient Assessment

```python
from predict import predict_single_patient, load_pipeline

# Load pipeline
fe, model, encoder, metadata = load_pipeline()

# Patient data
patient = {
    'Age': 65,
    'Gender': 'Male',
    'Air Pollution': 7,
    'Alcohol use': 6,
    'Dust Allergy': 4,
    'OccuPational Hazards': 3,
    'Genetic Risk': 5,
    'chronic Lung Disease': 6,
    'Balanced Diet': 3,
    'Obesity': 6,
    'Smoking': 8,
    'Passive Smoker': 2,
    'Chest Pain': 5,
    'Coughing of Blood': 4,
    'Fatigue': 7,
    'Weight Loss': 6,
    'Shortness of Breath': 7,
    'Wheezing': 6,
    'Swallowing Difficulty': 3,
    'Clubbing of Finger Nails': 5
}

# Predict
result = predict_single_patient(fe, model, encoder, patient)

print(f"Risk Level: {result['predicted_class']}")
print(f"Confidence: {result['confidence']:.1%}")
print(f"Probabilities: {result['probabilities']}")
```

**Output:**
```
Risk Level: High
Confidence: 92.3%
Probabilities: {'Low': 0.02, 'Medium': 0.06, 'High': 0.92}
```

---

### Example 2: Batch Prediction

```python
from predict import predict_batch, load_pipeline

# Load pipeline
fe, model, encoder, metadata = load_pipeline()

# Make predictions
predictions_df = predict_batch(
    fe, model, encoder,
    "data/new_patients.csv"
)

# View results
print(predictions_df[['PREDICTED_RISK', 'CONFIDENCE', 'PROB_High']].head())
```

---

### Example 3: Model Evaluation

```python
from test_model import test_model

# Test model
results = test_model("data/test_set.csv")

# View metrics
print(f"Accuracy: {results['test_accuracy']:.4f}")
print(f"F1-Score: {results['test_f1']:.4f}")
```

---

## 🔍 Understanding Predictions

### Risk Levels:

**Low Risk:**
- Minimal symptoms
- No smoking history
- Good lifestyle factors
- Low environmental exposure

**Medium Risk:**
- Some risk factors present
- Former smoker or passive exposure
- Moderate symptoms
- Mixed lifestyle factors

**High Risk:**
- Multiple risk factors
- Current smoker
- Significant symptoms
- High environmental exposure
- Genetic predisposition

### Confidence Scores:

- **High (>80%):** Model is very confident
- **Medium (60-80%):** Moderate confidence
- **Low (<60%):** Uncertain, review manually

## ⚠️ Important Notes

### Medical Disclaimer:
This system is for **research and educational purposes only**. 

❌ **NOT for:**
- Clinical diagnosis
- Treatment decisions
- Replacing medical professionals

✅ **Use for:**
- Risk assessment research
- Population screening studies
- Educational demonstrations
- ML model development

### Data Privacy:
- Ensure patient data is handled according to HIPAA/GDPR
- Remove personally identifiable information
- Use secure storage and transmission

## 🛠️ Troubleshooting

### Problem: Low accuracy (<75%)

**Solutions:**
1. Check data quality and missing values
2. Increase training data size
3. Adjust SMOTE sampling strategy
4. Try different model (GradientBoosting, XGBoost)

### Problem: Model predicts mostly one class

**Solutions:**
1. Check class balance in training data
2. Ensure SMOTE is working
3. Verify class weights are applied
4. Check for data leakage

### Problem: High training accuracy, low test accuracy

**Solutions:**
1. Model is overfitting
2. Reduce max_depth (try 10 instead of 15)
3. Increase min_samples_split (try 20 instead of 10)
4. Use more training data

## 📚 Technical Details

### Model Architecture:
```
Input (23 features)
    ↓
Feature Engineering (→40+ features)
    ↓
Standard Scaling
    ↓
SMOTE Balancing (if needed)
    ↓
Random Forest (200 trees, depth=15)
    ↓
Output (Low/Medium/High risk)
```

### Hyperparameters:
- n_estimators: 200
- max_depth: 15
- min_samples_split: 10
- min_samples_leaf: 4
- class_weight: balanced
- random_state: 42

## 🔄 Model Retraining

To retrain with new data:

1. Add new data to `cancer patient data sets.csv`
2. Run preprocessing: `python preprocessing.py`
3. Train new model: `python train_model.py`
4. Compare performance with previous model
5. Deploy if better

## 📊 Expected Dataset Performance

With the lung cancer dataset:

| Metric | Expected Range | Excellent |
|--------|---------------|-----------|
| Accuracy | 80-95% | >90% |
| Precision | 0.75-0.90 | >0.85 |
| Recall | 0.75-0.90 | >0.85 |
| F1-Score | 0.75-0.92 | >0.85 |
| ROC-AUC | 0.85-0.98 | >0.93 |

## 🤝 Contributing

Improvements welcome:
- Better feature engineering
- Alternative models (XGBoost, Neural Networks)
- Hyperparameter optimization
- Visualization tools
- Web interface

## 📄 License

MIT License - Free for research and educational use

## 📧 Support

For issues or questions:
1. Check troubleshooting section
2. Review error messages
3. Verify data format matches expected structure

---

**Last Updated:** December 2025  
**Version:** 1.0.0  
**Dataset:** Kaggle Lung Cancer Prediction Dataset