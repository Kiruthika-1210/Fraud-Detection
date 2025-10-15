# api/services/fraud_model.py
import joblib
import os
import pandas as pd

MODEL_PATH = "models/xgb_model.pkl"
FEATURE_ORDER_PATH = "models/feature_order.csv"  # CSV with a column 'feature' listing all 31 features in order

def load_model():
    """Load the trained XGBoost model."""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def load_feature_order():
    """Load the correct feature order for the model."""
    if os.path.exists(FEATURE_ORDER_PATH):
        df = pd.read_csv(FEATURE_ORDER_PATH)
        return df['feature'].tolist()
    return []

def predict(features: dict):
    """
    Predict the fraud risk score for a transaction.
    Missing features are automatically filled with 0.
    """
    model = load_model()
    order = load_feature_order()

    if not model:
        return 0.0  # Model not loaded

    if not order:
        raise ValueError("Feature order file not found. Cannot predict.")

    # Fill missing features with 0
    input_features = [features.get(f, 0) for f in order]

    return model.predict_proba([input_features])[0][1]
