# # import pandas as pd
# # import joblib
# # from pathlib import Path

# # # ----------------------
# # # CONFIG
# # # ----------------------
# # PROJECT_ROOT = Path(__file__).resolve().parent
# # DATA_DIR = PROJECT_ROOT / "data"
# # MODEL_DIR = PROJECT_ROOT / "models"

# # # ----------------------
# # # LOAD MODEL
# # # ----------------------
# # model_path = MODEL_DIR / "lung_cancer_model_gb_realistic.joblib"
# # pipeline = joblib.load(model_path)
# # print(" Model loaded!\n")

# # # ----------------------
# # # LOAD NEW DATA (or test set)
# # # ----------------------
# # X_new = pd.read_csv(DATA_DIR / "processed_features.csv")  # replace with any new data

# # # ----------------------
# # # MAKE PREDICTIONS
# # # ----------------------
# # preds = pipeline.predict(X_new)

# # # Optional: probabilities
# # try:
# #     probs = pipeline.predict_proba(X_new)
# # except:
# #     probs = None

# # # ----------------------
# # # SHOW RESULTS
# # # ----------------------
# # print(" Predictions:")
# # for i, pred in enumerate(preds[:10]):  # show first 10 predictions
# #     line = f"Sample {i+1}: Predicted = {pred}"
# #     if probs is not None:
# #         prob_str = ", ".join([f"{p:.2f}" for p in probs[i]])
# #         line += f" | Probabilities = [{prob_str}]"
# #     print(line)



# import joblib
# import pandas as pd
# import numpy as np
# from pathlib import Path
# from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
# from sklearn.preprocessing import LabelEncoder

# # ----------------------
# # Paths
# # ----------------------
# PROJECT_ROOT = Path(__file__).parent
# DATA_DIR = PROJECT_ROOT / "data"
# MODEL_DIR = PROJECT_ROOT / "models"

# # ----------------------
# # Load model
# # ----------------------
# model_file = MODEL_DIR / "lung_cancer_model_gb_realistic.joblib"
# pipeline = joblib.load(model_file)
# model = pipeline.named_steps['model']
# print(" Model loaded!\n")

# # ----------------------
# # Load feature CSV
# # ----------------------
# features_file = DATA_DIR / "processed_features.csv"
# X = pd.read_csv(features_file)
# print(f" Loaded {len(X)} samples, {X.shape[1]} features\n")

# # ----------------------
# # Get feature names safely
# # ----------------------
# try:
#     feature_names = pipeline.named_steps['scaler'].feature_names_in_
# except AttributeError:
#     feature_names = X.columns.tolist()

# # ----------------------
# # Feature importances
# # ----------------------
# importances = model.feature_importances_
# feat_imp = pd.DataFrame({
#     'feature': feature_names,
#     'importance': importances
# }).sort_values(by='importance', ascending=False)

# print(" Top 15 Features by Importance:")
# print(feat_imp.head(15).to_string(index=False))
# print("\n")

# # ----------------------
# # Predictions and probabilities
# # ----------------------
# preds = pipeline.predict(X)

# try:
#     probs = pipeline.predict_proba(X)
# except:
#     probs = None

# print(" Sample Predictions (first 10):")
# for i in range(min(10, len(X))):
#     line = f"Sample {i+1}: Predicted = {preds[i]}"
#     if probs is not None:
#         prob_str = ", ".join([f"{p:.2f}" for p in probs[i]])
#         line += f" | Probabilities = [{prob_str}]"
#     print(line)
# print("\n")

# # ----------------------
# # Optional evaluation if target exists
# # ----------------------
# target_file = DATA_DIR / "target.csv"
# if target_file.exists():
#     y_true = pd.read_csv(target_file).iloc[:, 0]

#     # encode if object
#     if y_true.dtype == 'object':
#         le = LabelEncoder()
#         y_true = le.fit_transform(y_true)

#     acc = accuracy_score(y_true, preds)
#     f1 = f1_score(y_true, preds, average='weighted')
#     cm = confusion_matrix(y_true, preds)

#     print(" Test Metrics:")
#     print(f"Accuracy: {acc:.4f}")
#     print(f"F1 Score: {f1:.4f}")
#     print("Confusion Matrix:")
#     print(cm)
#     print("\nClassification Report:")
#     print(classification_report(y_true, preds))


"""
Unified Inference Pipeline for Lung Cancer Prediction

This module provides a clean, high-level interface for making predictions
without exposing the underlying ML complexity. It handles both single
predictions and batch predictions.

Usage:
    from predict import LungCancerPredictor
    
    # Initialize predictor
    predictor = LungCancerPredictor()
    
    # Single prediction
    patient_data = {'AGE': 65, 'SMOKING': 2, 'GENDER': 'M', ...}
    result = predictor.predict_single(patient_data)
    
    # Batch prediction from CSV
    results = predictor.predict_batch('new_patients.csv')
"""

import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from typing import Dict, List, Union, Optional
import warnings
warnings.filterwarnings('ignore')


class LungCancerPredictor:
    """
    High-level interface for lung cancer risk prediction.
    Abstracts away all ML complexity.
    """
    
    def __init__(self, model_dir: Optional[str] = None):
        """
        Initialize the predictor by loading the trained pipeline.
        
        Args:
            model_dir: Path to model directory (default: auto-detect)
        """
        if model_dir is None:
            self.model_dir = Path(__file__).resolve().parent / "models"
        else:
            self.model_dir = Path(model_dir)
        
        # Load pipeline and metadata
        self._load_model()
        self._load_metadata()
        
    def _load_model(self):
        """Load the trained pipeline"""
        pipeline_path = self.model_dir / "lung_cancer_pipeline.pkl"
        
        if not pipeline_path.exists():
            raise FileNotFoundError(
                f"Model not found at {pipeline_path}. "
                "Please train the model first using train_model.py"
            )
        
        self.pipeline = joblib.load(pipeline_path)
        
        # Load target encoder if it exists
        encoder_path = self.model_dir / "target_encoder.pkl"
        if encoder_path.exists():
            self.target_encoder = joblib.load(encoder_path)
        else:
            self.target_encoder = None
    
    def _load_metadata(self):
        """Load model metadata"""
        metadata_path = self.model_dir / "model_metadata.json"
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
    
    def _prepare_input(self, data: Union[Dict, pd.DataFrame]) -> pd.DataFrame:
        """
        Prepare input data for prediction.
        
        Args:
            data: Either a dictionary (single sample) or DataFrame (batch)
        
        Returns:
            Prepared DataFrame ready for prediction
        """
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            raise TypeError("Input must be a dictionary or pandas DataFrame")
        
        # Normalize column names
        df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")
        
        # Handle missing values for any column that might be missing
        expected_features = self._get_expected_features()
        for col in expected_features:
            if col not in df.columns:
                df[col] = 0  # Add missing column with default value
        
        # Keep only expected features
        df = df[expected_features]
        
        return df
    
    def _get_expected_features(self) -> List[str]:
        """Get list of expected feature names"""
        # Read from processed_features to get original feature names
        data_dir = self.model_dir.parent / "data"
        processed_path = data_dir / "processed_features.csv"
        
        if processed_path.exists():
            sample_df = pd.read_csv(processed_path, nrows=1)
            return list(sample_df.columns)
        else:
            # Fallback: common features
            return [
                'AGE', 'GENDER', 'SMOKING', 'PASSIVE_SMOKER', 'AIR_POLLUTION',
                'ALCOHOL_USE', 'DUST_ALLERGY', 'OCCUPATIONAL_HAZARDS',
                'GENETIC_RISK', 'CHRONIC_LUNG_DISEASE', 'BALANCED_DIET',
                'OBESITY', 'CHEST_PAIN', 'COUGHING_OF_BLOOD', 'FATIGUE',
                'WEIGHT_LOSS', 'SHORTNESS_OF_BREATH', 'WHEEZING',
                'SWALLOWING_DIFFICULTY', 'CLUBBING_OF_FINGER_NAILS',
                'FREQUENT_COLD', 'DRY_COUGH', 'SNORING'
            ]
    
    def predict_single(
        self, 
        patient_data: Dict,
        return_probabilities: bool = True,
        verbose: bool = True
    ) -> Dict:
        """
        Predict lung cancer risk for a single patient.
        
        Args:
            patient_data: Dictionary containing patient information
            return_probabilities: Whether to return class probabilities
            verbose: Whether to print detailed results
        
        Returns:
            Dictionary containing prediction results
        """
        # Prepare input
        df = self._prepare_input(patient_data)
        
        # Make prediction
        prediction = self.pipeline.predict(df)[0]
        
        # Get class label
        if self.target_encoder:
            predicted_class = self.target_encoder.inverse_transform([prediction])[0]
        else:
            predicted_class = str(prediction)
        
        # Build result dictionary
        result = {
            'predicted_class': predicted_class,
            'predicted_level': prediction,
        }
        
        # Add probabilities if requested
        if return_probabilities:
            probabilities = self.pipeline.predict_proba(df)[0]
            target_classes = self.metadata.get('target_classes', [])
            
            result['probabilities'] = {
                class_name: float(prob) 
                for class_name, prob in zip(target_classes, probabilities)
            }
            result['confidence'] = float(max(probabilities))
        
        # Add risk interpretation
        result['risk_interpretation'] = self._interpret_risk(predicted_class)
        
        if verbose:
            self._print_single_result(result)
        
        return result
    
    def predict_batch(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        verbose: bool = True
    ) -> pd.DataFrame:
        """
        Predict lung cancer risk for multiple patients from a CSV file.
        
        Args:
            input_path: Path to input CSV file
            output_path: Path to save results (optional)
            verbose: Whether to print summary statistics
        
        Returns:
            DataFrame with predictions
        """
        # Load data
        df = pd.read_csv(input_path)
        
        if verbose:
            print(f" Loaded {len(df)} patients from {input_path}")
        
        # Prepare input
        df_prepared = self._prepare_input(df)
        
        # Make predictions
        predictions = self.pipeline.predict(df_prepared)
        probabilities = self.pipeline.predict_proba(df_prepared)
        
        # Create results dataframe
        results = df.copy()
        
        # Add predictions
        if self.target_encoder:
            results['PREDICTED_CLASS'] = self.target_encoder.inverse_transform(predictions)
        else:
            results['PREDICTED_CLASS'] = predictions
        
        results['PREDICTED_LEVEL'] = predictions
        
        # Add probabilities
        target_classes = self.metadata.get('target_classes', [])
        for i, class_name in enumerate(target_classes):
            results[f'PROB_{class_name}'] = probabilities[:, i]
        
        # Add confidence and risk interpretation
        results['CONFIDENCE'] = probabilities.max(axis=1)
        results['RISK_INTERPRETATION'] = results['PREDICTED_CLASS'].apply(self._interpret_risk)
        
        # Save if output path provided
        if output_path:
            results.to_csv(output_path, index=False)
            if verbose:
                print(f" Results saved to {output_path}")
        
        if verbose:
            self._print_batch_summary(results)
        
        return results
    
    def _interpret_risk(self, predicted_class: str) -> str:
        """Interpret the risk level"""
        interpretations = {
            'Low': 'Low risk - Regular monitoring recommended',
            'Medium': 'Medium risk - Consultation with healthcare provider advised',
            'High': 'High risk - Immediate medical evaluation strongly recommended'
        }
        return interpretations.get(str(predicted_class), 'Unknown risk level')
    
    def _print_single_result(self, result: Dict):
        """Pretty print single prediction result"""
        print("\n" + "=" * 60)
        print(" LUNG CANCER RISK PREDICTION")
        print("=" * 60)
        print(f"Predicted Risk Level: {result['predicted_class']}")
        print(f"Confidence: {result.get('confidence', 0):.1%}")
        print(f"\n{result['risk_interpretation']}")
        
        if 'probabilities' in result:
            print("\n Risk Probabilities:")
            for class_name, prob in result['probabilities'].items():
                bar = "" * int(prob * 30)
                print(f"  {class_name:10s}: {prob:6.1%} {bar}")
        
        print("=" * 60)
    
    def _print_batch_summary(self, results: pd.DataFrame):
        """Print summary of batch predictions"""
        print("\n" + "=" * 60)
        print(" BATCH PREDICTION SUMMARY")
        print("=" * 60)
        
        # Class distribution
        print("\nPredicted Risk Distribution:")
        class_counts = results['PREDICTED_CLASS'].value_counts()
        for class_name, count in class_counts.items():
            percentage = count / len(results) * 100
            print(f"  {class_name:10s}: {count:4d} ({percentage:5.1f}%)")
        
        # Confidence statistics
        print(f"\nAverage Confidence: {results['CONFIDENCE'].mean():.1%}")
        print(f"Min Confidence: {results['CONFIDENCE'].min():.1%}")
        print(f"Max Confidence: {results['CONFIDENCE'].max():.1%}")
        
        print("=" * 60)
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        info = {
            'model_type': self.metadata.get('model_type', 'Unknown'),
            'training_date': self.metadata.get('trained_on', 'Unknown'),
            'test_accuracy': self.metadata.get('test_metrics', {}).get('accuracy', 'Unknown'),
            'test_f1': self.metadata.get('test_metrics', {}).get('f1_weighted', 'Unknown'),
            'target_classes': self.metadata.get('target_classes', []),
        }
        return info
    
    def print_model_info(self):
        """Print model information in a formatted way"""
        info = self.get_model_info()
        
        print("\n" + "=" * 60)
        print(" MODEL INFORMATION")
        print("=" * 60)
        print(f"Model Type: {info['model_type']}")
        print(f"Training Date: {info['training_date']}")
        print(f"Test Accuracy: {info['test_accuracy']:.4f}" if isinstance(info['test_accuracy'], float) else f"Test Accuracy: {info['test_accuracy']}")
        print(f"Test F1 Score: {info['test_f1']:.4f}" if isinstance(info['test_f1'], float) else f"Test F1 Score: {info['test_f1']}")
        print(f"Risk Classes: {', '.join(info['target_classes'])}")
        print("=" * 60)


# ----------------------
# EXAMPLE USAGE
# ----------------------
def main():
    """Example usage of the predictor"""
    
    # Initialize predictor
    print(" Initializing Lung Cancer Predictor...")
    predictor = LungCancerPredictor()
    
    # Show model info
    predictor.print_model_info()
    
    # Example 1: Single prediction
    print("\n" + "=" * 60)
    print("EXAMPLE 1: SINGLE PATIENT PREDICTION")
    print("=" * 60)
    
    patient = {
        'AGE': 65,
        'GENDER': 'M',
        'SMOKING': 2,
        'PASSIVE_SMOKER': 1,
        'AIR_POLLUTION': 3,
        'ALCOHOL_USE': 4,
        'DUST_ALLERGY': 2,
        'OCCUPATIONAL_HAZARDS': 3,
        'GENETIC_RISK': 5,
        'CHRONIC_LUNG_DISEASE': 4,
        'BALANCED_DIET': 2,
        'OBESITY': 4,
        'CHEST_PAIN': 7,
        'COUGHING_OF_BLOOD': 5,
        'FATIGUE': 6,
        'WEIGHT_LOSS': 5,
        'SHORTNESS_OF_BREATH': 7,
        'WHEEZING': 6,
        'SWALLOWING_DIFFICULTY': 4,
        'CLUBBING_OF_FINGER_NAILS': 3,
        'FREQUENT_COLD': 5,
        'DRY_COUGH': 6,
        'SNORING': 4
    }
    
    result = predictor.predict_single(patient)
    
    # Example 2: Batch prediction (if test file exists)
    print("\n" + "=" * 60)
    print("EXAMPLE 2: BATCH PREDICTION")
    print("=" * 60)
    
    data_dir = Path(__file__).resolve().parent / "data"
    test_file = data_dir / "processed_features.csv"
    
    if test_file.exists():
        # Predict on first 10 samples
        df_sample = pd.read_csv(test_file).head(10)
        output_file = data_dir / "example_predictions.csv"
        
        results = predictor.predict_batch(
            test_file.as_posix(),
            output_path=output_file.as_posix(),
            verbose=True
        )
        
        print(f"\n Batch prediction complete!")
    else:
        print(f"  Test file not found at {test_file}")
        print("   Run preprocessing first to generate test data")


if __name__ == "__main__":
    main()