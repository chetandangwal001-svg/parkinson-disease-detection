import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


DATA_PATH = "data.csv"
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


def load_data(path):
    df = pd.read_csv(path)
    X = df[FEATURE_COLUMNS]
    y = df["status"]
    return X, y


def train_and_save():
    X, y = load_data(DATA_PATH)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Model accuracy - Train: {train_acc:.3f}, Test: {test_acc:.3f}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)
    print("Training complete. Saved model and scaler.")


if __name__ == "__main__":
    train_and_save()
