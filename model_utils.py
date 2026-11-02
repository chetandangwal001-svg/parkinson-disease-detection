import os
import pickle
import numpy as np

MODEL_PATH = "model_knn.pkl"
SCALER_PATH = "scaling.pkl"

FEATURE_COLUMNS = [
    "MDVP:Fo(Hz)",
    "MDVP:Fhi(Hz)",
    "MDVP:Flo(Hz)",
    "MDVP:Jitter(%)",
    "MDVP:Jitter(Abs)",
    "MDVP:RAP",
    "MDVP:PPQ",
    "Jitter:DDP",
    "MDVP:Shimmer",
    "Shimmer:APQ5",
    "MDVP:APQ",
    "Shimmer:DDA",
    "NHR",
    "HNR",
]


def load_model_and_scaler():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError("Model or scaler file not found. Run training first.")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(SCALER_PATH, "rb") as f:
        scaler = pickle.load(f)

    return model, scaler


def predict_from_features(model, scaler, feature_dict):
    features = [feature_dict[col] for col in FEATURE_COLUMNS]
    X = np.array([features], dtype=float)
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    return int(prediction[0])
