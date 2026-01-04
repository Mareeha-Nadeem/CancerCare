import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder

class LungCancerFeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self, debug=True):                                          # for print do debug =true
        self.debug = debug

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        # --------------------
        # Encode categorical
        # --------------------
        if self.debug:
            print(" Encoding categorical features...")
        # for col in X.columns:
        #     if X[col].dtype == 'object':
        #         try:
        #             X[col] = pd.to_numeric(X[col])
        #         except:
        #             X[col] = LabelEncoder().fit_transform(X[col].astype(str))
        for col in X.columns:
            if X[col].dtype == 'object':
                X[col] = pd.to_numeric(X[col], errors='coerce')


        X = X.apply(pd.to_numeric, errors='coerce')

        # --------------------
        # Composite Risk Scores
        # --------------------
        if 'SMOKING' in X.columns and 'PASSIVE_SMOKER' in X.columns:
            X['SMOKING_RISK'] = (X['SMOKING'] + X['PASSIVE_SMOKER']) / 2
            if self.debug: print(" SMOKING_RISK created")

        env_features = ['AIR_POLLUTION', 'DUST_ALLERGY', 'OCCUPATIONAL_HAZARDS']
        available_env = [f for f in env_features if f in X.columns]
        if available_env:
            X['ENVIRONMENTAL_RISK'] = X[available_env].mean(axis=1)
            if self.debug: print(" ENVIRONMENTAL_RISK created")

        if 'ALCOHOL_USE' in X.columns and 'OBESITY' in X.columns:
            X['LIFESTYLE_RISK'] = X['ALCOHOL_USE'] + X['OBESITY']
            if 'BALANCED_DIET' in X.columns:
                max_diet = X['BALANCED_DIET'].max()
                X['LIFESTYLE_RISK'] += (max_diet - X['BALANCED_DIET'])
            X['LIFESTYLE_RISK'] = X['LIFESTYLE_RISK'] / 3
            if self.debug: print(" LIFESTYLE_RISK created")

        if 'GENETIC_RISK' in X.columns and 'CHRONIC_LUNG_DISEASE' in X.columns:
            X['HEREDITARY_RISK'] = (X['GENETIC_RISK'] + X['CHRONIC_LUNG_DISEASE']) / 2
            if self.debug: print(" HEREDITARY_RISK created")

        symptom_features = [
            'CHEST_PAIN', 'COUGHING_OF_BLOOD', 'FATIGUE', 'WEIGHT_LOSS',
            'SHORTNESS_OF_BREATH', 'WHEEZING', 'SWALLOWING_DIFFICULTY',
            'CLUBBING_OF_FINGER_NAILS', 'FREQUENT_COLD', 'DRY_COUGH', 'SNORING'
        ]
        available_symptoms = [f for f in symptom_features if f in X.columns]
        if available_symptoms:
            X['SYMPTOM_SEVERITY'] = X[available_symptoms].mean(axis=1)
            if self.debug: print(" SYMPTOM_SEVERITY created")

        # Total Risk Score (weighted)
        risk_components = []
        weights = []
        for col, weight in [('SMOKING_RISK', 0.3), ('ENVIRONMENTAL_RISK', 0.2),
                            ('LIFESTYLE_RISK', 0.15), ('HEREDITARY_RISK', 0.2),
                            ('SYMPTOM_SEVERITY', 0.15)]:
            if col in X.columns:
                risk_components.append(X[col])
                weights.append(weight)
        if risk_components:
            X['TOTAL_RISK_SCORE'] = sum(comp * w for comp, w in zip(risk_components, weights))
            if self.debug: print(" TOTAL_RISK_SCORE created")

        # Age features
        if 'AGE' in X.columns:
            X['AGE_RISK'] = np.where(
                X['AGE'] < 40, 1,
                np.where(X['AGE'] < 50, 2,
                np.where(X['AGE'] < 60, 3,
                np.where(X['AGE'] < 70, 4, 5)))
            )
            X['AGE_GROUP'] = pd.cut(
                X['AGE'], bins=[0,40,50,60,70,100], labels=[0,1,2,3,4]
            ).astype(float)
            if self.debug: print(" AGE_RISK and AGE_GROUP created")

        # Interaction features
        if 'SMOKING_RISK' in X.columns and 'AGE_RISK' in X.columns:
            X['SMOKING_AGE_INTERACTION'] = X['SMOKING_RISK'] * X['AGE_RISK']
            if self.debug: print(" SMOKING_AGE_INTERACTION created")
        if 'ENVIRONMENTAL_RISK' in X.columns and 'SMOKING_RISK' in X.columns:
            X['ENV_SMOKING_INTERACTION'] = X['ENVIRONMENTAL_RISK'] * X['SMOKING_RISK']
            if self.debug: print(" ENV_SMOKING_INTERACTION created")
        if 'GENETIC_RISK' in X.columns and 'AGE_RISK' in X.columns:
            X['GENETIC_AGE_INTERACTION'] = X['GENETIC_RISK'] * X['AGE_RISK']
            if self.debug: print(" GENETIC_AGE_INTERACTION created")

        if self.debug:
            print(f"\n Transformed features shape: {X.shape}")
            print(f"Columns: {list(X.columns)}")

        return X
    
#################################  for demo only  #####################################
if __name__ == "__main__":
    # Demo: create a small sample dataframe
    data = pd.DataFrame({
        'AGE': [25, 55, 65],
        'SMOKING': [1, 3, 2],
        'PASSIVE_SMOKER': [0, 1, 0],
        'AIR_POLLUTION': [3, 2, 4],
        'DUST_ALLERGY': [1, 0, 2],
        'OCCUPATIONAL_HAZARDS': [2, 1, 1],
        'ALCOHOL_USE': [1, 2, 1],
        'OBESITY': [0, 1, 1],
        'BALANCED_DIET': [3, 2, 1],
        'GENETIC_RISK': [0, 1, 1],
        'CHRONIC_LUNG_DISEASE': [0, 1, 1],
        'CHEST_PAIN': [0, 1, 0],
        'COUGHING_OF_BLOOD': [0, 0, 1]
    })

    fe = LungCancerFeatureEngineer(debug=True)
    X_transformed = fe.fit_transform(data)
    print("\n Feature engineering demo complete!")

