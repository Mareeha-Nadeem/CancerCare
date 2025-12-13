"""
predict.py
----------
Makes predictions on new patient data using trained pipeline.
Handles single patient or batch predictions.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import json
from datetime import datetime
import sys
from train_model import FeatureEngineer, CategoricalEncoder


# ----------------------
# CONFIG
# ----------------------
PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"
PREDICTIONS_DIR = PROJECT_ROOT / "predictions"

PREDICTIONS_DIR.mkdir(exist_ok=True)


def load_pipeline():
    """Load trained prediction pipeline."""
    
    pipeline_path = MODEL_DIR / "cancer_prediction_pipeline.joblib"
    
    if not pipeline_path.exists():
        raise FileNotFoundError(
            f"Trained model not found at {pipeline_path}.\n"
            f"Please train the model first by running: python train_model.py"
        )
    
    print(f"📦 Loading model from: {pipeline_path}")
    pipeline = joblib.load(pipeline_path)
    
    # Load metadata if available
    metadata_path = MODEL_DIR / "model_metadata.json"
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        print(f"✅ Model loaded (trained on: {metadata.get('trained_on', 'Unknown')})")
    else:
        print("✅ Model loaded")
    
    return pipeline


def validate_input_data(df):
    """Validate that input data has required columns."""
    
    required_cols = [
        'COUNTRY', 'AGE', 'GENDER', 'SMOKING_STATUS', 'SECOND_HAND_SMOKE',
        'AIR_POLLUTION_EXPOSURE', 'OCCUPATION_EXPOSURE', 'RURAL_OR_URBAN',
        'SOCIOECONOMIC_STATUS', 'HEALTHCARE_ACCESS', 'INSURANCE_COVERAGE',
        'SCREENING_AVAILABILITY', 'FAMILY_HISTORY', 'INDOOR_SMOKE_EXPOSURE'
    ]
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"\n⚠️  WARNING: Missing columns: {missing_cols}")
        print("Predictions may be less accurate without all features.\n")
    
    return df


def predict_single_patient(pipeline, patient_data):
    """
    Make prediction for a single patient.
    
    Parameters:
    -----------
    pipeline : sklearn.pipeline.Pipeline
        Trained prediction pipeline
    patient_data : dict
        Dictionary containing patient features
    
    Returns:
    --------
    dict : Prediction result with probability
    """
    
    # Convert dict to DataFrame
    df = pd.DataFrame([patient_data])
    df = validate_input_data(df)
    
    # Make prediction
    prediction = pipeline.predict(df)[0]
    probabilities = pipeline.predict_proba(df)[0]
    confidence = probabilities.max()
    
    result = {
        'prediction': str(prediction),
        'confidence': float(confidence),
        'probabilities': {
            f'class_{i}': float(prob) 
            for i, prob in enumerate(probabilities)
        }
    }
    
    return result


def predict_batch(pipeline, data_path, save_predictions=True):
    """
    Make predictions for multiple patients from CSV file.
    
    Parameters:
    -----------
    pipeline : sklearn.pipeline.Pipeline
        Trained prediction pipeline
    data_path : str or Path
        Path to CSV file containing patient data
    save_predictions : bool
        Whether to save predictions to file
    
    Returns:
    --------
    pd.DataFrame : Original data with predictions added
    """
    
    print(f"\n📂 Loading data from: {data_path}")
    
    # Load data
    df = pd.read_csv(data_path)
    original_df = df.copy()
    
    print(f"✅ Loaded {len(df)} patients")
    
    # Validate input
    df = validate_input_data(df)
    
    # Make predictions
    print("\n🔮 Making predictions...")
    predictions = pipeline.predict(df)
    probabilities = pipeline.predict_proba(df)
    
    # Add predictions to dataframe
    original_df['PREDICTION'] = predictions
    original_df['CONFIDENCE'] = probabilities.max(axis=1)
    
    # Add individual class probabilities
    for i in range(probabilities.shape[1]):
        original_df[f'PROBABILITY_CLASS_{i}'] = probabilities[:, i]
    
    # Categorize confidence levels
    original_df['CONFIDENCE_LEVEL'] = pd.cut(
        original_df['CONFIDENCE'],
        bins=[0, 0.6, 0.8, 1.0],
        labels=['Low', 'Medium', 'High']
    )
    
    print("✅ Predictions complete!")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 PREDICTION SUMMARY")
    print("="*60)
    print(f"\nPrediction Distribution:")
    print(original_df['PREDICTION'].value_counts())
    print(f"\nConfidence Level Distribution:")
    print(original_df['CONFIDENCE_LEVEL'].value_counts())
    print(f"\nAverage Confidence: {original_df['CONFIDENCE'].mean():.2%}")
    
    # Save predictions
    if save_predictions:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = PREDICTIONS_DIR / f"predictions_{timestamp}.csv"
        original_df.to_csv(output_path, index=False)
        print(f"\n💾 Predictions saved to: {output_path}")
    
    print("="*60 + "\n")
    
    return original_df


def predict_from_console():
    """Interactive console-based prediction for single patient."""
    
    print("\n" + "="*60)
    print("🏥 CANCER PRE-DIAGNOSIS RISK PREDICTION")
    print("="*60 + "\n")
    
    pipeline = load_pipeline()
    
    print("Please enter patient information:")
    print("-" * 60)
    
    # Collect patient data
    patient_data = {}
    
    # Define input fields with validation
    fields = {
        'COUNTRY': str,
        'AGE': int,
        'GENDER': str,
        'SMOKING_STATUS': str,  # Smoker, Former Smoker, Non-Smoker
        'SECOND_HAND_SMOKE': str,  # Yes, No
        'AIR_POLLUTION_EXPOSURE': str,  # Low, Medium, High
        'OCCUPATION_EXPOSURE': str,  # Yes, No
        'RURAL_OR_URBAN': str,  # Rural, Urban
        'SOCIOECONOMIC_STATUS': str,  # Low, Middle, High
        'HEALTHCARE_ACCESS': str,  # Poor, Limited, Good
        'INSURANCE_COVERAGE': str,  # Yes, No
        'SCREENING_AVAILABILITY': str,  # Yes, No
        'FAMILY_HISTORY': str,  # Yes, No
        'INDOOR_SMOKE_EXPOSURE': str,  # Yes, No
    }
    
    for field, field_type in fields.items():
        while True:
            try:
                value = input(f"{field.replace('_', ' ').title()}: ")
                if field_type == int:
                    patient_data[field] = int(value)
                else:
                    patient_data[field] = value
                break
            except ValueError:
                print(f"Invalid input. Please enter a valid {field_type.__name__}.")
    
    print("\n🔮 Analyzing patient data...")
    
    # Make prediction
    result = predict_single_patient(pipeline, patient_data)
    
    # Display results
    print("\n" + "="*60)
    print("📊 PREDICTION RESULTS")
    print("="*60)
    print(f"\nPrediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    if result['confidence'] < 0.6:
        confidence_level = "Low ⚠️"
    elif result['confidence'] < 0.8:
        confidence_level = "Medium 🟡"
    else:
        confidence_level = "High ✅"
    
    print(f"Confidence Level: {confidence_level}")
    
    print("\nClass Probabilities:")
    for class_name, prob in result['probabilities'].items():
        print(f"  {class_name}: {prob:.2%}")
    
    print("\n" + "="*60)
    print("⚕️  Note: This is a predictive model and should not replace")
    print("    professional medical advice. Consult a healthcare provider.")
    print("="*60 + "\n")
    
    # Save result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = PREDICTIONS_DIR / f"single_prediction_{timestamp}.json"
    
    output = {
        'patient_data': patient_data,
        'prediction_result': result,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(result_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"💾 Prediction saved to: {result_file}\n")
    
    return result


def main():
    """Main function to handle command-line arguments."""
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  Batch predictions:      python predict.py <path_to_csv>")
        print("  Interactive mode:       python predict.py --interactive")
        print("  Example:                python predict.py data/new_patients.csv\n")
        sys.exit(1)
    
    # Load pipeline
    pipeline = load_pipeline()
    
    if sys.argv[1] == "--interactive":
        # Interactive console mode
        predict_from_console()
    else:
        # Batch prediction mode
        data_path = sys.argv[1]
        
        if not Path(data_path).exists():
            print(f"❌ Error: File not found: {data_path}")
            sys.exit(1)
        
        predictions = predict_batch(pipeline, data_path, save_predictions=True)
        
        # Display first few predictions
        print("\n📋 Sample Predictions (first 5):")
        print("-" * 60)
        display_cols = ['PREDICTION', 'CONFIDENCE', 'CONFIDENCE_LEVEL']
        if all(col in predictions.columns for col in display_cols):
            print(predictions[display_cols].head().to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        predict_from_console()
    else:
        main()