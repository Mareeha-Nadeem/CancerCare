def validate_patient(data):
    required = ["mrn", "name", "age", "gender"]
    for f in required:
        if f not in data:
            return False, f"Missing: {f}"
    return True, None

def validate_features(features):
    if not isinstance(features, dict):
        return False, "Invalid feature format"
    if "age" in features and features["age"] <= 0:
        return False, "Age must be positive"
    return True, None