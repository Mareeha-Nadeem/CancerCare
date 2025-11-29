import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

def create_pipeline(df, label_col='level'):
    # Identify categorical and numeric columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    numeric_cols = [c for c in df.select_dtypes(include=['int64', 'float64']).columns if c != label_col]

    # Numeric pipeline: fill missing + scale
    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='ffill')),  # forward fill
        ('scaler', StandardScaler())
    ])

    # Categorical pipeline: fill missing + encode
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Combine numeric + categorical
    preprocessor = ColumnTransformer([
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

    # Full pipeline: preprocessing + model
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier())
    ])

    return pipeline


# 1️ Load dataset
try:
    df = pd.read_csv("../dataset/cancer patient data sets.csv")
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: File not found. Check the path.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: File is empty.")
    exit()
except Exception as e:
    print(f"Unexpected error: {e}")
    exit()

# 2️ Explore dataset
try:
    print("\nFirst 5 rows:\n", df.head())
    print("\nShape:", df.shape)
    print("\nInfo:\n", df.info())
    print("\nDescribe:\n", df.describe())
except Exception as e:
    print(f"Error exploring data: {e}")

# 3️ Fix column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
print("\nFixed column names:\n", df.columns)

# Drop non-feature columns so ml model is not confused
non_features = ['index', 'Patient_Id']  # adjust if necessary
df = df.drop(columns=[col for col in non_features if col in df.columns], errors='ignore')

# 4️ Handle missing values
try:
    print("\nMissing values before fill:\n", df.isnull().sum())
    df.ffill(inplace=True)  # forward fill missing values
    print("Missing values after fill:\n", df.isnull().sum())
except Exception as e:
    print(f"Error handling missing values: {e}")

# 5️ Encode categorical features
try:
    le = LabelEncoder()
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
    print("\nCategorical columns encoded successfully.")
except Exception as e:
    print(f"Error encoding categorical columns: {e}")

# 6️ Scale numeric columns
try:
    label_col = "level"
    numeric_cols = [c for c in df.select_dtypes(include=['int64','float64']).columns if c != label_col]
    # numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    print("\nNumeric columns scaled successfully.")
except Exception as e:
    print(f"Error scaling numeric columns: {e}")

# 7️ Save preprocessed dataset
try:
    df.to_csv("../preprocessed/cancer_patient_preprocessed.csv", index=False)
    print("\nPreprocessed dataset saved successfully!")
except Exception as e:
    print(f"Error saving dataset: {e}")
