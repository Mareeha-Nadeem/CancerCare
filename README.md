# Lung Cancer Risk Prediction System

A complete machine learning pipeline for predicting lung cancer risk levels with advanced feature engineering and a user-friendly interface.

## 📁 Project Structure

```
project/
├── data/
│   ├── raw_data.csv                    # Original dataset
│   ├── processed_features.csv          # Preprocessed features
│   ├── target.csv                      # Target labels
│   └── test_predictions.csv            # Test set results
├── models/
│   ├── lung_cancer_pipeline.pkl        # Complete trained pipeline
│   ├── target_encoder.pkl              # Label encoder
│   └── model_metadata.json             # Model info & metrics
├── results/
│   └── test_predictions.csv            # Evaluation results
├── preprocess.py                       # Data preprocessing
├── feature_engineer.py                 # Feature engineering transformer
├── train_model.py                      # Model training script
├── predict.py                          # Prediction pipeline (advanced)
└── interface.py                        # Simple interface (recommended)
```

## 🚀 Quick Start

### 1. **Preprocess Data**
```python
python preprocess.py
```
This will:
- Load raw data
- Normalize column names
- Handle missing values
- Remove duplicates
- Save processed features and target

### 2. **Train Model**
```python
python train_model.py
```
This will:
- Apply feature engineering
- Train Gradient Boosting model
- Perform 5-fold cross-validation
- Evaluate on test set
- Save complete pipeline

### 3. **Make Predictions**

**Option A: Simple Interface (Recommended)**
```python
from interface import predict_patient, predict_file

# Single patient prediction
result = predict_patient(
    age=65,
    gender='M',
    smoking=7,
    genetic_risk=5,
    chest_pain=6,
    # ... other features
)

# Batch prediction from file
results = predict_file('new_patients.csv', 'predictions.csv')
```

**Option B: Advanced Interface**
```python
from predict import LungCancerPredictor

predictor = LungCancerPredictor()

# Single prediction
patient = {'AGE': 65, 'SMOKING': 7, ...}
result = predictor.predict_single(patient)

# Batch prediction
results = predictor.predict_batch('patients.csv', 'output.csv')
```

## 📊 Features

### Automatic Feature Engineering

The pipeline automatically creates:

1. **Composite Risk Scores**
   - `SMOKING_RISK`: Combined smoking exposure
   - `ENVIRONMENTAL_RISK`: Air quality factors
   - `LIFESTYLE_RISK`: Diet, alcohol, obesity
   - `HEREDITARY_RISK`: Genetic and chronic disease factors
   - `SYMPTOM_SEVERITY`: Average of all symptoms
   - `TOTAL_RISK_SCORE`: Weighted composite of all risks

2. **Age-Based Features**
   - `AGE_RISK`: Risk category based on age brackets
   - `AGE_GROUP`: Age grouping for analysis

3. **Interaction Features**
   - `SMOKING_AGE_INTERACTION`
   - `ENV_SMOKING_INTERACTION`
   - `GENETIC_AGE_INTERACTION`

### Model Pipeline

```
Input Data 
    ↓
Feature Engineering (LungCancerFeatureEngineer)
    ↓
Missing Value Imputation (Median)
    ↓
Standardization (StandardScaler)
    ↓
SMOTE (if imbalanced classes)
    ↓
Gradient Boosting Classifier
    ↓
Predictions + Probabilities
```

## 📖 Usage Examples

### Example 1: Quick Single Prediction

```python
from interface import quick_predict

# Predict with minimal input (uses defaults for other features)
result = quick_predict(
    age=65,
    smoking=7,
    gender='M'
)

print(f"Risk Level: {result['predicted_class']}")
print(f"Confidence: {result['confidence']:.1%}")
```

### Example 2: Detailed Single Prediction

```python
from interface import predict_patient

result = predict_patient(
    age=68,
    gender='M',
    smoking=8,
    passive_smoker=6,
    air_pollution=7,
    alcohol_use=7,
    dust_allergy=5,
    occupational_hazards=6,
    genetic_risk=7,
    chronic_lung_disease=6,
    balanced_diet=2,
    obesity=6,
    chest_pain=7,
    coughing_of_blood=6,
    fatigue=7,
    weight_loss=6,
    shortness_of_breath=8,
    wheezing=7,
    swallowing_difficulty=5,
    clubbing_of_finger_nails=4,
    frequent_cold=6,
    dry_cough=7,
    snoring=5
)

# Access results
print(result['predicted_class'])        # 'High', 'Medium', or 'Low'
print(result['confidence'])              # 0.0 to 1.0
print(result['probabilities'])           # {'Low': 0.1, 'Medium': 0.2, 'High': 0.7}
print(result['risk_interpretation'])     # Human-readable recommendation
```

### Example 3: Batch Prediction

```python
from interface import predict_file

# Process entire CSV file
results = predict_file(
    input_file='patients.csv',
    output_file='predictions.csv',
    verbose=True
)

# results is a DataFrame with:
# - All original columns
# - PREDICTED_CLASS
# - PREDICTED_LEVEL
# - PROB_Low, PROB_Medium, PROB_High
# - CONFIDENCE
# - RISK_INTERPRETATION
```

### Example 4: Check Model Status

```python
from interface import check_model_status

check_model_status()
```

### Example 5: Run Interactive Demo

```python
from interface import interactive_demo

interactive_demo()
```

## 🎯 Input Features

All features should be provided as integers on a scale (typically 1-8, except AGE):

| Feature | Description | Scale |
|---------|-------------|-------|
| `AGE` | Patient's age | Years |
| `GENDER` | Gender | 'M' or 'F' |
| `SMOKING` | Active smoking level | 1-8 |
| `PASSIVE_SMOKER` | Passive smoking exposure | 1-8 |
| `AIR_POLLUTION` | Air pollution exposure | 1-8 |
| `ALCOHOL_USE` | Alcohol consumption | 1-8 |
| `DUST_ALLERGY` | Dust allergy severity | 1-8 |
| `OCCUPATIONAL_HAZARDS` | Workplace hazards | 1-8 |
| `GENETIC_RISK` | Genetic risk factors | 1-8 |
| `CHRONIC_LUNG_DISEASE` | Chronic lung disease | 1-8 |
| `BALANCED_DIET` | Diet quality (higher=better) | 1-8 |
| `OBESITY` | Obesity level | 1-8 |
| `CHEST_PAIN` | Chest pain severity | 1-8 |
| `COUGHING_OF_BLOOD` | Hemoptysis severity | 1-8 |
| `FATIGUE` | Fatigue level | 1-8 |
| `WEIGHT_LOSS` | Weight loss severity | 1-8 |
| `SHORTNESS_OF_BREATH` | Dyspnea severity | 1-8 |
| `WHEEZING` | Wheezing severity | 1-8 |
| `SWALLOWING_DIFFICULTY` | Dysphagia severity | 1-8 |
| `CLUBBING_OF_FINGER_NAILS` | Finger clubbing | 1-8 |
| `FREQUENT_COLD` | Frequency of colds | 1-8 |
| `DRY_COUGH` | Dry cough severity | 1-8 |
| `SNORING` | Snoring severity | 1-8 |

## 📈 Model Performance

The model is evaluated using:
- **F1 Score** (weighted): Primary metric
- **Accuracy**: Overall correctness
- **Precision**: Positive prediction accuracy
- **Recall**: Sensitivity
- **Confusion Matrix**: Detailed breakdown

View current metrics:
```python
from predict import LungCancerPredictor

predictor = LungCancerPredictor()
predictor.print_model_info()
```

## 🔧 Advanced Configuration

### Custom Model Directory

```python
from predict import LungCancerPredictor

predictor = LungCancerPredictor(model_dir='/path/to/models')
```

### Without Verbose Output

```python
result = predict_patient(..., verbose=False)
results = predict_file(..., verbose=False)
```

### Access Raw Predictor

```python
from predict import LungCancerPredictor

predictor = LungCancerPredictor()

# Get model metadata
info = predictor.get_model_info()

# Direct DataFrame prediction
import pandas as pd
df = pd.read_csv('patients.csv')
predictions = predictor.pipeline.predict(df)
```

## 🛡️ Error Handling

The system handles:
- ✅ Missing columns (filled with defaults)
- ✅ Missing values (imputed)
- ✅ Different column name formats
- ✅ Model not trained (clear error message)

## 📝 Output Format

### Single Prediction Result
```python
{
    'predicted_class': 'High',
    'predicted_level': 2,
    'confidence': 0.87,
    'probabilities': {
        'Low': 0.05,
        'Medium': 0.08,
        'High': 0.87
    },
    'risk_interpretation': 'High risk - Immediate medical evaluation strongly recommended'
}
```

### Batch Prediction DataFrame
```
| AGE | GENDER | SMOKING | ... | PREDICTED_CLASS | CONFIDENCE | RISK_INTERPRETATION |
|-----|--------|---------|-----|-----------------|------------|---------------------|
| 65  | M      | 7       | ... | High           | 0.87       | High risk - ...     |
| 45  | F      | 2       | ... | Low            | 0.92       | Low risk - ...      |
```

## 🎓 Best Practices

1. **Always preprocess** your data before training
2. **Use `interface.py`** for simplest usage
3. **Check model status** before making predictions
4. **Save predictions** to file for record-keeping
5. **Review confidence scores** - low confidence may need manual review

## 🚨 Troubleshooting

### Model Not Found
```bash
# Train the model first
python preprocess.py
python train_model.py
```

### Import Errors
```bash
# Install dependencies
pip install pandas numpy scikit-learn imbalanced-learn joblib
```

### Column Name Mismatch
- The system auto-normalizes column names
- Use uppercase with underscores: `AGE`, `CHEST_PAIN`, etc.

## 📞 Support

For issues or questions:
1. Check that preprocessing completed successfully
2. Verify model training finished without errors
3. Ensure all required features are provided
4. Check model metadata: `predictor.print_model_info()`

## 🔄 Workflow Summary

```
1. Collect Data → raw_data.csv
2. Run preprocess.py → processed_features.csv + target.csv
3. Run train_model.py → lung_cancer_pipeline.pkl
4. Use interface.py → Make predictions!
```

## ⚡ Quick Reference

```python
# Check if ready
from interface import check_model_status
check_model_status()

# Single prediction
from interface import predict_patient
result = predict_patient(age=65, smoking=7, gender='M')

# Batch prediction
from interface import predict_file
results = predict_file('patients.csv', 'output.csv')

# Interactive demo
from interface import interactive_demo
interactive_demo()
```

---

**Note**: This is a risk assessment tool and should not replace professional medical diagnosis. Always consult healthcare professionals for medical decisions.